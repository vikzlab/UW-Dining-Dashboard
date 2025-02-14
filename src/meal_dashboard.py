import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Sample dataset for meal ratings, including Starbucks & The HUB
data = {
    "Dining Hall": ["Husky Den", "Local Point", "Center Table", "The 8", "Denny Dining", 
                    "Starbucks", "The HUB", "District Market", "Pagliacci Pizza", "Taco Truck"],
    "Meal Rating (Avg)": [3.8, 4.2, 3.5, 4.0, 3.7, 4.5, 4.1, 3.9, 4.3, 3.6],
    "Total Feedback": [150, 120, 200, 180, 160, 300, 250, 130, 190, 110],
    "Service Speed (Avg, min)": [12, 10, 15, 13, 14, 8, 9, 11, 10, 12],
    "Affordability Score (1-5)": [3, 4, 3, 4, 3, 2, 3, 4, 3, 4]
}

df = pd.DataFrame(data)

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
wordcloud = WordCloud(width=1000, height=500, background_color="white", colormap="coolwarm").generate(feedback_text)

# Streamlit UI Setup
st.set_page_config(page_title="UW Dining Dashboard", layout="wide")
st.title("📊 UW Dining Experience Dashboard")
st.write("This dashboard provides insights into meal ratings, affordability, service speed, and student feedback trends across various UW dining locations.")

# Sidebar Filter for Dining Hall Selection
selected_dining_hall = st.sidebar.selectbox("Select a Dining Hall to View:", ["All"] + df["Dining Hall"].tolist())

# Apply Filter
if selected_dining_hall == "All":
    filtered_df = df
else:
    filtered_df = df[df["Dining Hall"] == selected_dining_hall]

# 📈 **Bar Chart: Meal Ratings**
st.subheader("📈 Average Meal Ratings by Dining Hall")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="Meal Rating (Avg)", y="Dining Hall", data=filtered_df, palette="viridis", ax=ax)
ax.set_xlabel("Average Rating")
ax.set_ylabel("Dining Hall / Food Service")
ax.set_title("Meal Ratings Across UW Dining Locations")
st.pyplot(fig)

# ⏳ **Scatter Plot: Service Speed vs. Affordability**
st.subheader("⏳ Service Speed vs. Affordability")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x="Service Speed (Avg, min)", y="Affordability Score (1-5)", hue="Dining Hall",
                size="Meal Rating (Avg)", sizes=(50, 300), data=filtered_df, palette="coolwarm", alpha=0.8, ax=ax)
ax.set_xlabel("Service Speed (Avg. Minutes)")
ax.set_ylabel("Affordability Score (1-5)")
ax.set_title("Comparison of Service Speed and Affordability")
ax.legend(loc="best", bbox_to_anchor=(1, 1))
st.pyplot(fig)

# 💬 **Word Cloud: Common Feedback Trends**
st.subheader("💬 Common Student Feedback Trends")
fig, ax = plt.subplots(figsize=(12, 6))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
ax.set_title("Most Frequent Student Comments About Dining Services")
st.pyplot(fig)

# 📋 **Display Filtered Data Table**
st.subheader("📋 Dining Hall Details")
st.dataframe(filtered_df)

st.write("🔍 Use the filter in the sidebar to explore specific dining locations!")
