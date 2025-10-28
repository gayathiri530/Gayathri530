
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Tamil Nadu Breast Cancer Dashboard", layout="wide")
sns.set_style("whitegrid")

st.title("Tamil Nadu Breast Cancer Dashboard 🩷")
st.markdown("Select **Age Group** and **Stage** to view or create results — even if not in your dataset.")

# ---- Sidebar: Upload dataset ----
st.sidebar.header("📂 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return pd.DataFrame()

# ---- Load dataset ----
if uploaded_file is not None:
    data = load_data(uploaded_file)
else:
    st.info("No dataset uploaded. Using sample dataset for demo.")
    data = pd.DataFrame({
        "Age_Group": ["30-39", "40-49", "50-59", "60-69", "70+"],
        "Stage": ["Stage I", "Stage II", "Stage III", "Stage II", "Stage III"],
        "Year": [2018, 2019, 2020, 2021, 2022],
        "Count": [12, 25, 18, 22, 15]
    })

if data.empty:
    st.error("No data found. Please upload a valid dataset.")
    st.stop()

# ---- Dropdown filters ----
st.subheader("🔽 Select Age Group and Stage")

# get dropdown values safely
age_groups = sorted(data["Age_Group"].dropna().unique().tolist())
stages = sorted(data["Stage"].dropna().unique().tolist())

col1, col2, col3 = st.columns([3, 3, 2])
with col1:
    age_group = st.selectbox("Select Age Group", options=age_groups + ["(Other)"])
with col2:
    stage = st.selectbox("Select Stage", options=stages + ["(Other)"])
with col3:
    submit = st.button("Show Output")

# ---- Logic ----
if submit:
    filtered = data.copy()

    if age_group != "(Other)":
        filtered = filtered[filtered["Age_Group"] == age_group]
    else:
        new_age = st.text_input("Enter new Age Group:", placeholder="Type new age group (e.g. 25-29)")
        if new_age:
            age_group = new_age

    if stage != "(Other)":
        filtered = filtered[filtered["Stage"] == stage]
    else:
        new_stage = st.text_input("Enter new Stage:", placeholder="Type new stage (e.g. Stage IV)")
        if new_stage:
            stage = new_stage

    # ---- If dataset has no matching rows ----
    if filtered.empty:
        st.warning("No matching rows found — creating new entry.")
        new_row = {
            "Age_Group": age_group,
            "Stage": stage
        }

        # preserve dataset columns
        for col in data.columns:
            if col not in new_row:
                new_row[col] = None

        filtered = pd.DataFrame([new_row])

    # ---- Display Results ----
    st.subheader("📋 Filtered / Created Data")
    st.dataframe(filtered.reset_index(drop=True))

    # ---- Download button ----
    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download this data", data=csv_bytes, file_name="filtered_data.csv", mime="text/csv")

    # ---- Charts ----
    st.subheader("📊 Visualization")

    colA, colB = st.columns(2)

    with colA:
        st.markdown("**Stage Distribution**")
        if "Stage" in data.columns:
            fig, ax = plt.subplots(figsize=(5, 3))
            sns.countplot(x="Stage", data=data, ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.info("No 'Stage' column found for chart.")

    with colB:
        if "Year" in data.columns and "Count" in data.columns:
            st.markdown("**Yearly Trend**")
            fig2, ax2 = plt.subplots(figsize=(5, 3))
            sns.lineplot(data=data, x="Year", y="Count", marker="o", ax=ax2)
            st.pyplot(fig2)
        else:
            st.info("No 'Year' or 'Count' column found for trend chart.")

    # ---- Summary ----
    with st.expander("📈 Summary Statistics"):
        try:
            st.write(filtered.describe(include="all"))
        except Exception as e:
            st.write("Summary not available:", e)

else:
    st.info("Select filters and click **Show Output** to view or create results.")
