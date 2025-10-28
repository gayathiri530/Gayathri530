import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Title & Description
# -------------------------------
st.title("🏥 Breast Cancer Dashboard")
st.write("Enter an age and stage to find the number of persons in that category.")

# -------------------------------
# Load Dataset
# -------------------------------
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    # Sample dataset
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
predict_button = st.button("🔍 Predict / Show Result")

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

# -------------------------------
# When button is clicked
# -------------------------------
if predict_button:
    age_group = find_age_group(age)
    filtered = data[(data["Age_Group"] == age_group) & (data["Stage"] == stage)]

    st.subheader("📊 Result")

    if not filtered.empty:
        # Exact record found
        count = int(filtered["Count"].sum())
        st.success(f"✅ Number of persons aged {age_group} in {stage}: **{count}**")
        st.dataframe(filtered)
    else:
        # Age is valid, but no data for that combo → show 0 count, not warning
        known_age_groups = data["Age_Group"].unique()
        if age_group in known_age_groups:
            st.info(f"ℹ️ No data recorded for age group {age_group} and {stage}. Estimated count: **0**")
            st.dataframe(pd.DataFrame({
                "Age_Group": [age_group],
                "Stage": [stage],
                "Count": [0]
            }))
        else:
            # Truly invalid or missing group → show warning
            st.warning("⚠️ No such record exists or the age is outside the dataset range.")

    # -------------------------------
    # Chart
    # -------------------------------
    st.subheader("📈 Stage-wise Distribution")
    fig, ax = plt.subplots()
    data.groupby("Stage")["Count"].sum().plot(kind="bar", ax=ax)
    ax.set_ylabel("Number of Persons")
    ax.set_title("Stage-wise Count Distribution")
    st.pyplot(fig)
