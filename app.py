import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Breast Cancer Dashboard", layout="wide")
sns.set_style("whitegrid")

st.title("Tamil Nadu Breast Cancer Dashboard 🩷")
st.markdown("Select **Age Group** and **Stage** below to view filtered data and charts.")

# ---- SIDEBAR: Upload Dataset ----
st.sidebar.header("📂 Data Upload")
uploaded_file = st.sidebar.file_uploader("Upload your dataset (CSV)", type=["csv"])

@st.cache_data
def load_data(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return pd.DataFrame()

# ---- Load data ----
if uploaded_file is not None:
    data = load_data(uploaded_file)
else:
    st.info("No file uploaded. Using sample dataset.")
    data = pd.DataFrame({
        "Age_Group": ["30-39", "40-49", "50-59", "60-69", "70+"],
        "Stage": ["Stage I", "Stage II", "Stage III", "Stage II", "Stage III"],
        "Year": [2018, 2019, 2020, 2021, 2022],
        "Count": [12, 25, 18, 22, 15]
    })

# ---- Verify dataset ----
if data.empty:
    st.error("No data available. Please upload a valid CSV file.")
    st.stop()

# ---- Dropdown filters ----
st.subheader("🔽 Select filters")

age_groups = sorted(data["Age_Group"].dropna().unique().tolist())
stages = sorted(data["Stage"].dropna().unique().tolist())

col1, col2, col3 = st.columns([3,3,2])

with col1:
    age_group = st.selectbox("Select Age Group", options=["All"] + age_groups)
with col2:
    stage = st.selectbox("Select Stage", options=["All"] + stages)
with col3:
    submit = st.button("Show Results")

# ---- Filter logic ----
if submit:
    filtered = data.copy()
    if age_group != "All":
        filtered = filtered[filtered["Age_Group"] == age_group]
    if stage != "All":
        filtered = filtered[filtered["Stage"] == stage]

    st.subheader("📊 Filtered Data")
    st.dataframe(filtered)

    # ---- Chart 1: Stage Distribution ----
    st.markdown("### Stage Distribution")
    fig, ax = plt.subplots()
    sns.countplot(data=filtered, x="Stage", ax=ax)
    ax.set_xlabel("Stage")
    ax.set_ylabel("Count")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ---- Chart 2: Yearly Trend ----
    if "Year" in filtered.columns:
        st.markdown("### Yearly Trend")
        fig2, ax2 = plt.subplots()
        if "Count" in filtered.columns:
            sns.lineplot(data=filtered, x="Year", y="Count", marker="o", ax=ax2)
        else:
            sns.countplot(data=filtered, x="Year", ax=ax2)
        plt.xticks(rotation=45)
        st.pyplot(fig2)

    # ---- Summary ----
    st.markdown("### Summary Statistics")
    st.write(filtered.describe(include="all"))

else:
    st.info("Please select filters and click **Show Results**.")
