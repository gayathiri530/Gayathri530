import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Title & Description
# -------------------------------
st.title("🏥 Breast Cancer Dashboard")
st.write("Enter an age and stage to find or predict the number of persons in that category.")

# -------------------------------
# Load Dataset
# -------------------------------
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    # Sample dataset for demo
    data = pd.DataFrame({
        "Age_Group": ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70+"],
        "Stage": ["Stage I", "Stage II", "Stage III", "Stage I", "Stage II", "Stage III", "Stage II", "Stage III"],
        "Count": [2, 5, 10, 14, 22, 18, 25, 12]
    })
    st.info("Using sample dataset for demo.")

# -------------------------------
# Input Section
# -------------------------------
age = st.number_input("Enter Age (in years):", min_value=0, max_value=120, value=25)
stage = st.selectbox("Select Stage:", sorted(data["Stage"].unique()))

# -------------------------------
# Function: Convert age → group
# -------------------------------
def find_age_group(age):
    if age < 10:
        return "0-9"
    elif age < 20:
        return "10-19"
    elif age < 30:
        return "20-29"
    elif age < 40:
        return "30-39"
    elif age < 50:
        return "40-49"
    elif age < 60:
        return "50-59"
    elif age < 70:
        return "60-69"
    else:
        return "70+"

age_group = find_age_group(age)

# -------------------------------
# Filter dataset
# -------------------------------
filtered = data[(data["Age_Group"] == age_group) & (data["Stage"] == stage)]

st.subheader("📊 Result")

# -------------------------------
# Exact Match
# -------------------------------
if not filtered.empty:
    count = int(filtered["Count"].sum())
    st.success(f"✅ Number of persons aged {age_group} in {stage}: **{count}**")
    st.dataframe(filtered)

# -------------------------------
# No Exact Match → Nearest Suggestion
# -------------------------------
else:
    st.warning("⚠️ No exact record found. Finding nearest match...")

    # Find nearest age group (closest to given age)
    def group_to_mid(age_group_str):
        if '+' in age_group_str:
            return int(age_group_str.replace('+', ''))
        low, high = age_group_str.split('-')
        return (int(low) + int(high)) / 2

    data["mid_age"] = data["Age_Group"].apply(group_to_mid)
    nearest_row = data.iloc[(data["mid_age"] - age).abs().argsort()].head(1)

    predicted_count = int(nearest_row["Count"].values[0])
    nearest_group = nearest_row["Age_Group"].values[0]
    nearest_stage = nearest_row["Stage"].values[0]

    st.info(
        f"🔮 Predicted based on nearest group: **{nearest_group}**, "
        f"Stage: **{nearest_stage}** → Estimated Persons: **{predicted_count}**"
    )
    st.dataframe(nearest_row.drop(columns=["mid_age"]))

# -------------------------------
# Chart Section
# -------------------------------
st.subheader("📈 Stage-wise Distribution")
fig, ax = plt.subplots()
data.groupby("Stage")["Count"].sum().plot(kind="bar", ax=ax)
ax.set_ylabel("Number of Persons")
ax.set_title("Stage-wise Count Distribution")
st.pyplot(fig)
