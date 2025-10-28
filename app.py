import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------
# 🎨 Page Setup
# --------------------------
st.set_page_config(
    page_title="Breast Cancer Stage Predictor",
    page_icon="🩷",
    layout="centered"
)

st.title("🩷 Tamil Nadu Breast Cancer Stage Predictor")
st.markdown("Enter a patient's **age** below to predict the most likely **cancer stage**.")

# --------------------------
# 📂 Load Dataset
# --------------------------
uploaded_file = st.file_uploader("📁 Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    st.info("Using sample dataset for demonstration.")
    data = pd.DataFrame({
        "Age_Group": ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70+"],
        "Stage": ["Stage I", "Stage II", "Stage III", "Stage I", "Stage II", "Stage III", "Stage II", "Stage III"],
        "Count": [2, 5, 10, 14, 22, 18, 25, 12]
    })

# --------------------------
# 🧠 Helper Function to Find Age Group
# --------------------------
def get_age_group(age):
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

# --------------------------
# 🔢 Input Age
# --------------------------
age = st.number_input("Enter Age", min_value=1, max_value=120, step=1)

# --------------------------
# 🧮 Predict Button
# --------------------------
if st.button("🔍 Predict Stage"):
    # Find the corresponding group
    age_group = get_age_group(age)
    st.write(f"**Detected Age Group:** {age_group}")

    # Filter dataset
    filtered_df = data[data['Age_Group'] == age_group]

    # If no data available for that group
    if filtered_df.empty or age < 30:
        st.error("⚠️ No data available for this age group.")
    else:
        # Find most frequent stage for that age group
        predicted_stage = (
            filtered_df['Stage']
            .value_counts()
            .idxmax()
        )

        st.success(f"✅ Predicted Stage: **{predicted_stage}**")

        # Show small chart
        st.subheader("📊 Stage Distribution for this Age Group")
        fig, ax = plt.subplots()
        filtered_df['Stage'].value_counts().plot(kind='bar', ax=ax)
        ax.set_ylabel("Count")
        ax.set_title(f"Stage Distribution — Age Group {age_group}")
        st.pyplot(fig)
