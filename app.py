import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px




df = pd.read_csv("jobs_clean_final.csv")


# -------------------------
# TITLE
# -------------------------
st.title("Data Analyst Market Dashboard")

st.markdown("""
Explore salaries, skills, and hiring trends across the IT job market.

This dashboard helps aspiring Data Analysts understand what companies are looking for in terms of:
- Skills
- Salaries
- Career paths
- Market demand
""")


# -------------------------
# SIDEBAR FILTER
# -------------------------
st.sidebar.header("Filters")

selected_role = st.sidebar.selectbox(
    "Search IT Role",
    sorted(df["role_category"].dropna().unique())
)

filtered_df = df[df["role_category"] == selected_role]



skills_cols = ["python", "sql", "excel", "tableau", "powerbi"]


# -------------------------
# KPI SECTION
# -------------------------

avg_salary = int(filtered_df["normalized_salary"].mean())

top_skill = (
    filtered_df[skills_cols]
    .mean()
    .sort_values(ascending=False)
    .index[0]
)

col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(filtered_df))
col2.metric("Average Salary", f"${avg_salary:,}")
col3.metric("Top Skill", top_skill.upper())


# -------------------------
# OVERVIEW SECTION
# -------------------------
st.subheader("Overview by Role")

role_stats = df.groupby("role_category").agg(
    avg_salary=("med_salary", "mean"),
    job_count=("role_category", "size")
).sort_values("avg_salary", ascending=False)


st.bar_chart(role_stats["avg_salary"])


# -------------------------
# SALARY CHART
# -------------------------
st.subheader("Role Comparison")

role_stats_display = role_stats.reset_index().rename(columns={
    "role_category": "Role",
    "avg_salary": "Average Salary",
    "job_count": "Job Count"
})

role_stats_display["Average Salary"] = role_stats_display["Average Salary"].apply(lambda x: f"${x:,.0f}")
role_stats_display["Job Count"] = role_stats_display["Job Count"].astype(int)

st.dataframe(role_stats_display, use_container_width=True)

st.subheader("Average Salary by Role")

st.bar_chart(role_stats["avg_salary"])


# -------------------------
# SELECTED ROLE DATA
# -------------------------
st.subheader(f"Jobs for:  {selected_role}")

st.write("Total jobs:", len(filtered_df))

jobs_table = filtered_df[[
    "title",
    "company_name",
    "location",
    "normalized_salary",
    "description"
]].head(20)

jobs_table.columns = [
    "Job Title",
    "Company",
    "Location",
    "Salary",
    "Job Description"
]

jobs_table["Job Description"] = (
    jobs_table["Job Description"]
    .astype(str)
    .str[:150] + "..."
)

st.dataframe(jobs_table)




st.subheader("Top Skills in Job Postings (%)")

skills_cols = ["python", "sql", "excel", "tableau", "powerbi"]

skills_data = filtered_df[skills_cols].mean() * 100

st.bar_chart(skills_data)

role_counts = df["role_category"].value_counts()



 

fig = px.pie(
    values=role_counts.values,
    names=role_counts.index,
    title="Market Share of IT Roles"
)

st.plotly_chart(fig)

fig.update_traces(textposition='inside', textinfo='percent+label')



