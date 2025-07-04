import streamlit as st
import pandas as pd
import altair as alt
import os

# Page setup
st.set_page_config(page_title="Himalayan Expedition Analytics", layout="wide")
st.title("\U0001F3D4️ Himalayan Expedition Analytics Dashboard")

st.markdown("""
### \U0001F5C2️ Project Overview

This dataset, based on the archives of Elizabeth Hawley, provides a comprehensive record of mountaineering expeditions in the Nepalese Himalaya, spanning from 1905 to 2024. It includes detailed information on 89,000+ members across 11,000+ expeditions and 480 mountain peaks, including dates, successes, and significant events.

#### Recommended Analysis
- ✅ What percentage of peaks have been climbed?
- ✅ Which person has been a part of the most successful expeditions?
- ✅ Are there any notable trends and patterns in climbing over time?
- ✅ How many people have successfully climbed Mount Everest?
""")

# Load data
@st.cache_data
def load_data(base_path):
    exped = pd.read_csv(os.path.join(base_path, "exped.csv"), low_memory=False)
    members = pd.read_csv(os.path.join(base_path, "members.csv"), low_memory=False)
    peaks = pd.read_csv(os.path.join(base_path, "peaks.csv"))
    refer = pd.read_csv(os.path.join(base_path, "refer.csv"), encoding="cp1252")
    data_dict = pd.read_csv(os.path.join(base_path, "himalayan_data_dictionary.csv"))

    for df in [exped, members, peaks, refer, data_dict]:
        df.columns = df.columns.str.strip()

    # Handle missing values
    exped.fillna({"success1": "unknown"}, inplace=True)
    members.fillna({"peakid": "UNKNOWN", "citizen": "UNKNOWN"}, inplace=True)
    peaks.fillna({"pkname": "UNKNOWN"}, inplace=True)
    return exped, members, peaks, refer, data_dict

# Upload or use default dataset
st.sidebar.header("\U0001F4C2 Upload Your Data (Optional)")
uploaded = st.sidebar.file_uploader("Upload exped.csv", type=["csv"])
custom_path = st.sidebar.text_input("Or use a local path (folder)", r"C:\\Users\\Henry Morgan\\Downloads\\Himalayan+Expeditions")

if uploaded:
    st.warning("Custom file upload is not fully supported for all tables yet. Using default path for now.")
    exped, members, peaks, refer, data_dict = load_data(custom_path)
else:
    exped, members, peaks, refer, data_dict = load_data(custom_path)

# Filters
st.sidebar.header("\U0001F50D Filters")
years = exped["year"].dropna().unique()
selected_year = st.sidebar.selectbox("Select Year", sorted(years, reverse=True))

countries = members["citizen"].dropna().unique()
selected_country = st.sidebar.selectbox("Select Country", sorted(countries))

# Filtered data
filtered_exped = exped[exped["year"] == selected_year]
filtered_members = members[members["citizen"] == selected_country]

# Sample data preview
st.subheader("\U0001F4CA Sample Data")
tabs = st.tabs(["Expeditions", "Members", "Peaks", "References", "Data Dictionary"])
with tabs[0]: st.dataframe(filtered_exped.head())
with tabs[1]: st.dataframe(filtered_members.head())
with tabs[2]: st.dataframe(peaks.head())
with tabs[3]: st.dataframe(refer.head())
with tabs[4]: st.dataframe(data_dict.head())

# Top 5 most climbed peaks (chart)
st.subheader("\U0001F3D4️ Top 5 Most Climbed Peaks")

if "peakid" in members.columns and "peakid" in peaks.columns:
    top_peaks = members["peakid"].value_counts().reset_index()
    top_peaks.columns = ["peakid", "num_climbers"]
    top_peaks = top_peaks.merge(peaks[["peakid", "pkname"]], on="peakid", how="left")
    top5 = top_peaks.head(5)

    st.altair_chart(
        alt.Chart(top5).mark_bar().encode(
            x=alt.X("num_climbers:Q", title="Number of Climbers"),
            y=alt.Y("pkname:N", sort="-x", title="Peak"),
            tooltip=["pkname", "num_climbers"]
        ).properties(height=300),
        use_container_width=True
    )
    st.dataframe(top5)
else:
    st.error("❌ Required columns ('peakid', 'pkname') missing.")

# Dataset dimensions
st.subheader("📐 Dataset Dimensions")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Expeditions", f"{exped.shape[0]} rows", f"{exped.shape[1]} columns")
col2.metric("Members", f"{members.shape[0]} rows", f"{members.shape[1]} columns")
col3.metric("Peaks", f"{peaks.shape[0]} rows", f"{peaks.shape[1]} columns")
col4.metric("References", f"{refer.shape[0]} rows", f"{refer.shape[1]} columns")

# ✅ Analysis Section
st.header("📈 Recommended Analysis")

# 1. Percentage of peaks climbed
peaks_climbed = members["peakid"].dropna().nunique()
total_peaks = peaks["peakid"].nunique()
climbed_pct = (peaks_climbed / total_peaks) * 100
st.metric("% of Peaks Climbed", f"{climbed_pct:.2f}%")

# 2. Most successful climber
name_cols = [col for col in members.columns if 'name' in col.lower()]
success_cols = [col for col in members.columns if 'success' in col.lower()]

if name_cols and success_cols:
    name_col = name_cols[0]
    success_col = success_cols[0]
    successful_members = members[members[success_col].astype(str).str.lower().isin(['true', '1', 'y', 'yes'])]
    if not successful_members.empty:
        most_successful = successful_members[name_col].value_counts().idxmax()
        st.metric("Most Successful Climber", most_successful)
    else:
        st.warning("No successful climbs found in the data.")
else:
    st.warning("❌ Could not find suitable 'name' or 'success' columns in members.csv.")

# 3. Climbing trends over time
st.subheader("📅 Climbing Trends Over Time")
if "year" in exped.columns:
    yearly_summary = exped.groupby("year").agg(
        total_expeditions=pd.NamedAgg(column="expid", aggfunc="count"),
        successful_expeditions=pd.NamedAgg(column="success1", aggfunc=lambda x: (x == "success").sum())
    ).reset_index()

    trend_data = pd.melt(yearly_summary, id_vars="year", value_vars=["total_expeditions", "successful_expeditions"],
                         var_name="Metric", value_name="Count")

    trend_chart = alt.Chart(trend_data).mark_line(point=True).encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("Count:Q", title="Number of Expeditions"),
        color=alt.Color("Metric:N", title=""),
        tooltip=["year", "Metric", "Count"]
    ).properties(height=400)

    st.altair_chart(trend_chart, use_container_width=True)
else:
    st.warning("`year` column not found in exped.csv")

# 4. Successful Everest climbers
if 'peakid' in members.columns and success_cols:
    success_col = success_cols[0]
    everest_id = peaks[peaks['pkname'].str.contains("Everest", case=False, na=False)]["peakid"].values
    everest_climbers = members[(members["peakid"].isin(everest_id)) & (members[success_col].astype(str).str.lower().isin(['true', '1', 'y', 'yes']))]
    st.metric("Successful Everest Climbers", f"{everest_climbers.shape[0]:,}")
else:
    st.warning("Columns `peakid` or success not found.")

# Final note
st.success("✅ Dashboard loaded and analyses complete.")
