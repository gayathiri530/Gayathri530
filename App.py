# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

st.set_page_config(page_title="Breast Cancer Dashboard", layout="wide")
sns.set_style("whitegrid")

st.title("Tamil Nadu Breast Cancer — Flexible Dashboard")
st.markdown(
    "Upload your dataset (CSV) or use the sample. You can type any Age Group / Stage (even if it's not in the dataset)."
)

# -- Sidebar: dataset upload or sample use
st.sidebar.header("Data Options")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
use_sample = st.sidebar.checkbox("Use sample dataset (if no upload)", value=True)

@st.cache_data
def load_sample():
    # small sample to let the app run if user has no file.
    sample = pd.DataFrame({
        "Age_Group": ["30-39","40-49","50-59","60-69","70+"],
        "Stage": ["Stage I","Stage II","Stage III","Stage II","Stage III"],
        "Year": [2018,2019,2020,2021,2022],
        "Count": [12, 25, 18, 22, 15]
    })
    return sample

def load_csv(file) -> pd.DataFrame:
    try:
        return pd.read_csv(file)
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return pd.DataFrame()

# Load data
if uploaded_file is not None:
    data = load_csv(uploaded_file)
    st.sidebar.success("CSV uploaded")
elif use_sample:
    data = load_sample()
    st.sidebar.info("Using sample dataset")
else:
    st.warning("Please upload a CSV or enable 'Use sample dataset'.")
    data = pd.DataFrame()

# Check required columns
expected_cols = {"Age_Group", "Stage"}
missing = expected_cols - set(data.columns)
if missing:
    st.warning(f"Dataset missing columns: {', '.join(missing)}. The app will still work with inputs, but some charts may be limited.")

# -- Main inputs: free text (accept values not in dataset)
st.subheader("Enter filter / input values")
col1, col2, col3 = st.columns([3,3,2])
with col1:
    age_input = st.text_input("Age Group (type anything)", placeholder="e.g. 70+, 25-29, Other")
with col2:
    stage_input = st.text_input("Stage (type anything)", placeholder="e.g. Stage II, Stage IV, Unknown")
with col3:
    submit = st.button("Show Output")

# If no submit pressed, optionally show full data or instructions
if not submit:
    st.info("Type Age Group and/or Stage and click **Show Output** to view results.")
    if not data.empty:
        with st.expander("Preview dataset (first 10 rows)"):
            st.dataframe(data.head(10))
    st.stop()

# When button clicked: filtering logic
filtered = data.copy() if not data.empty else pd.DataFrame()

# Apply filters only if non-empty strings provided
if age_input:
    if "Age_Group" in filtered.columns:
        filtered = filtered[filtered["Age_Group"].astype(str) == age_input]
    else:
        filtered = pd.DataFrame()  # no Age_Group column: result will be empty

if stage_input:
    if "Stage" in filtered.columns:
        filtered = filtered[filtered["Stage"].astype(str) == stage_input]
    else:
        filtered = pd.DataFrame()

# If filtered is empty -> create a new row from inputs
if filtered.empty:
    st.warning("No matching rows found in dataset. Creating a new row from your inputs.")
    new_row = {"Age_Group": age_input if age_input else None,
               "Stage": stage_input if stage_input else None}
    # Attempt to include other columns with NaN if they exist
    cols = list(data.columns) if not data.empty else ["Age_Group", "Stage"]
    # Ensure Age_Group and Stage present as first two columns
    if not data.empty:
        new_row_full = {c: (new_row.get(c) if c in new_row else pd.NA) for c in cols}
        filtered = pd.DataFrame([new_row_full])
    else:
        filtered = pd.DataFrame([new_row])

# Display filtered / input data
st.subheader("Filtered / Input Data")
st.dataframe(filtered.reset_index(drop=True))

# Download button for filtered data
csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered data as CSV", data=csv_bytes, file_name="filtered_data.csv", mime="text/csv")

# ---- Charts ----
st.subheader("Visualizations")

# 1) Stage distribution (bar)
colA, colB = st.columns(2)
with colA:
    st.markdown("**Stage distribution**")
    if "Stage" in filtered.columns:
        stage_counts = filtered["Stage"].value_counts()
        if not stage_counts.empty:
            fig, ax = plt.subplots(figsize=(6,3))
            sns.barplot(x=stage_counts.index.astype(str), y=stage_counts.values, ax=ax)
            ax.set_ylabel("Count")
            ax.set_xlabel("Stage")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.info("No Stage data to plot.")
    else:
        st.info("No 'Stage' column present in data.")

# 2) If Year column exists -> trend
with colB:
    if "Year" in filtered.columns:
        st.markdown("**Year-wise trend**")
        try:
            # if Count column exists, aggregate else count rows per year
            if "Count" in filtered.columns:
                yearly = filtered.groupby("Year")["Count"].sum().reset_index()
                st.line_chart(yearly.rename(columns={"Year":"index"}).set_index("Year"))
            else:
                yearly = filtered.groupby("Year").size().rename("Count").reset_index()
                yearly = yearly.set_index("Year")
                st.line_chart(yearly)
        except Exception as e:
            st.info(f"Could not plot year trend: {e}")
    else:
        st.info("No 'Year' column found for trend chart.")

# 3) Quick summary stats
st.subheader("Summary")
with st.expander("Show summary statistics"):
    try:
        st.write(filtered.describe(include="all"))
    except Exception as e:
        st.write("Summary not available:", e)

st.success("Done — use the inputs and charts as needed. Save your CSV using the Download button.")
