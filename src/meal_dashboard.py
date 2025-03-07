import streamlit as st  # type: ignore
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # type: ignore
from wordcloud import WordCloud  # type: ignore
import os

# Ensure Matplotlib uses the correct backend
import matplotlib
matplotlib.use("Agg")

# File for storing reviews
REVIEWS_FILE = "reviews.csv"

# Sample dataset for meal ratings, affordability, and wait times
data = {
    "Dining Hall": ["Husky Den", "Local Point", "Center Table", "The 8", "Denny Dining", 
                    "Starbucks", "The HUB", "District Market", "Pagliacci Pizza", "Taco Truck"],
    "Meal Rating (Avg)": [3.8, 4.2, 3.5, 4.0, 3.7, 4.5, 4.1, 3.9, 4.3, 3.6],
    "Total Feedback": [150, 120, 200, 180, 160, 300, 250, 130, 190, 110],
    "Service Speed (Avg, min)": [12, 10, 15, 13, 14, 8, 9, 11, 10, 12],
    "Affordability Score (1-5)": [3, 4, 3, 4, 3, 2, 3, 4, 3, 4]
}

df = pd.DataFrame(data)

# Map affordability score to dollar signs ($, $$, $$$)
df["Affordability ($)"] = df["Affordability Score (1-5)"].map({1: "$", 2: "$", 3: "$$", 4: "$$", 5: "$$$"})

# Load existing reviews if file exists
if os.path.exists(REVIEWS_FILE):
    reviews_df = pd.read_csv(REVIEWS_FILE)
else:
    reviews_df = pd.DataFrame(columns=["Dining Hall", "Rating", "Affordability", "Wait Time"])

# Ensure numerical columns are properly formatted
reviews_df["Rating"] = pd.to_numeric(reviews_df["Rating"], errors="coerce")
reviews_df["Affordability"] = pd.to_numeric(reviews_df["Affordability"], errors="coerce")
reviews_df["Wait Time"] = pd.to_numeric(reviews_df["Wait Time"], errors="coerce")

# Aggregate new ratings and update values if there are reviews
if not reviews_df.empty:
    updated_ratings = reviews_df.groupby("Dining Hall", as_index=False).agg({
        "Rating": "mean",
        "Affordability": "mean",
        "Wait Time": "mean"
    })

    # Rename aggregated columns before merging
    updated_ratings.rename(columns={"Rating": "New Rating", 
                                    "Affordability": "New Affordability", 
                                    "Wait Time": "New Wait Time"}, inplace=True)

    # Merge updated values into df
    df = df.merge(updated_ratings, on="Dining Hall", how="left")

    # Apply new values only where available
    df["Meal Rating (Avg)"] = df["New Rating"].combine_first(df["Meal Rating (Avg)"])
    df["Affordability Score (1-5)"] = df["New Affordability"].combine_first(df["Affordability Score (1-5)"])
    df["Service Speed (Avg, min)"] = df["New Wait Time"].combine_first(df["Service Speed (Avg, min)"])

    # Drop temporary columns
    df.drop(columns=["New Rating", "New Affordability", "New Wait Time"], inplace=True, errors="ignore")

# Sample common feedback text for word cloud
feedback_text = """
great coffee, long lines, loved the sandwiches, overpriced drinks, needs more seating, dry chicken, excellent dessert, 
long wait times, fresh ingredients, better portion sizes, amazing burgers, overcooked vegetables, more vegan options, 
friendly staff, healthier choices, soggy fries, tasty seafood, too greasy, undercooked rice, love the new menu, 
fast service, inconsistent quality, great study spot, limited menu, cozy atmosphere, better customer service, mobile ordering, 
needs more gluten-free options, expensive but worth it, love the late-night menu, should add more drink choices, food trucks rock, 
improve portion consistency, more protein options, vegetarian meals taste bland, customizable orders would be great, 
online ordering system is confusing, reduce waste with sustainable packaging, wish they accepted more meal plan options.
"""

# Generate word cloud
wordcloud = WordCloud(width=1000, height=500, background_color="white", colormap="cividis").generate(feedback_text)

# Streamlit UI Setup
st.set_page_config(page_title="UW Dining Dashboard", layout="wide")

# Sidebar Navigation
page = st.sidebar.radio("Navigation", ["Home", "Meal Ratings", "Affordability", "Wait Times", "Feedback Trends", "Submit a Review"])

# **Homepage**
if page == "Home":
    st.title("🏠 Welcome to the UW Dining Experience Dashboard!")
    st.write(
        """
        This interactive dashboard provides insights into meal ratings, affordability, wait times, and student feedback 
        trends across various dining halls at the University of Washington. Use the navigation sidebar to explore different 
        aspects of campus dining. You can also submit your own review to contribute to the data!
        """
    ) 
    st.subheader("🔍 How to Use This Dashboard:")
    st.markdown(
        """
        - **Meal Ratings:** View average ratings of different dining halls.
        - **Affordability:** Compare meal pricing based on student affordability ratings.
        - **Wait Times:** Check estimated service times for various locations.
        - **Feedback Trends:** Explore common themes in student feedback using word clouds.
        - **Submit a Review:** Add your own feedback and ratings to help improve dining experiences!
        """
    )

# **Submit a Review**
elif page == "Submit a Review":
    st.subheader("✍️ Submit a Review")
    dining_hall = st.selectbox("Select Dining Hall:", df["Dining Hall"])
    rating = st.slider("Rate the Meal (1-5):", 1, 5, 3)
    affordability = st.slider("Affordability (1-5):", 1, 5, 3)
    wait_time = st.slider("Service Speed (Minutes):", 5, 20, 10)

    if st.button("Submit Review"):
        new_review = pd.DataFrame([[dining_hall, rating, affordability, wait_time]], columns=["Dining Hall", "Rating", "Affordability", "Wait Time"])
        new_review.to_csv(REVIEWS_FILE, mode="a", header=not os.path.exists(REVIEWS_FILE), index=False)
        st.success(f"Review submitted! The new average rating for {dining_hall} will be updated.")

# **Other Pages**
else:
    selected_dining_hall = st.sidebar.selectbox("Select a Dining Hall to View:", ["All"] + df["Dining Hall"].tolist())
    filtered_df = df if selected_dining_hall == "All" else df[df["Dining Hall"] == selected_dining_hall]

    if page == "Meal Ratings":
        st.subheader("📈 Average Meal Ratings by Dining Hall")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="Meal Rating (Avg)", y="Dining Hall", data=filtered_df, palette="viridis", ax=ax)
        st.pyplot(fig)

    elif page == "Affordability":
        st.subheader("💲 Affordability of Dining Locations")
        st.dataframe(filtered_df[["Dining Hall", "Affordability ($)"]])

    elif page == "Wait Times":
        st.subheader("⏳ Estimated Wait Times")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="Service Speed (Avg, min)", y="Dining Hall", data=filtered_df, palette="rocket", ax=ax)
        st.pyplot(fig)

    elif page == "Feedback Trends":
        st.subheader("💬 Common Student Feedback Trends")
        st.image(wordcloud.to_array(), use_column_width=True)
