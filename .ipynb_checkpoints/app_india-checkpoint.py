import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="India Data Science Job Market 2025",
    page_icon="🇮🇳",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/india_jobs_cleaned.csv')
    return df

df = load_data()

# Title
st.title(" India Data Science Job Market Analysis 2025")
st.markdown("""
Comprehensive analysis of **1,600+ data science job postings** in India, revealing:
- 💰 Salary trends across seniority levels and roles
- 🛠️ Most in-demand skills in Indian market
- 📊 Job category distribution
- 🏢 Top hiring companies
""")

st.divider()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Job Category filter
all_categories = sorted(df['job_category'].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Job Categories",
    all_categories,
    default=all_categories[:3]
)

# Seniority filter
seniority_options = ['All'] + sorted(df['seniority'].unique().tolist())
selected_seniority = st.sidebar.selectbox("Seniority Level", seniority_options)

# Salary filter
min_sal = float(df['avg_salary_lpa'].min())
max_sal = float(df['avg_salary_lpa'].max())
salary_range = st.sidebar.slider(
    "Salary Range (₹ LPA)", 
    min_sal, max_sal, (min_sal, max_sal)
)

# Experience filter
max_exp = int(df['min_experience_clean'].max())
exp_range = st.sidebar.slider(
    "Experience (years)",
    0, max_exp, (0, max_exp)
)

# Apply filters
filtered_df = df[
    (df['job_category'].isin(selected_categories)) &
    (df['avg_salary_lpa'].between(salary_range[0], salary_range[1])) &
    (df['min_experience_clean'].between(exp_range[0], exp_range[1]))
]

if selected_seniority != 'All':
    filtered_df = filtered_df[filtered_df['seniority'] == selected_seniority]

st.sidebar.metric("Jobs Matching Filters", len(filtered_df))

# Main metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Jobs", len(filtered_df))

with col2:
    median_salary = filtered_df['avg_salary_lpa'].median()
    st.metric("Median Salary", f"₹{median_salary:.1f} LPA")

with col3:
    unique_companies = filtered_df['company'].nunique()
    st.metric("Unique Companies", unique_companies)

with col4:
    avg_exp = filtered_df['min_experience_clean'].mean()
    st.metric("Avg Experience Required", f"{avg_exp:.1f} yrs")

st.divider()

# Row 1: Salary Analysis
st.header("💰 Salary Analysis")

col1, col2 = st.columns(2)

with col1:
    # Salary distribution
    fig_salary = px.histogram(
        filtered_df,
        x='avg_salary_lpa',
        nbins=30,
        title='Salary Distribution',
        labels={'avg_salary_lpa': 'Salary (₹ LPA)'},
        color_discrete_sequence=['#FF6B35']
    )
    fig_salary.add_vline(x=median_salary, line_dash="dash", line_color="red",
                         annotation_text=f"Median: ₹{median_salary:.1f}L")
    fig_salary.update_layout(
        xaxis_title="Annual Salary (₹ LPA)",
        yaxis_title="Number of Jobs",
        showlegend=False
    )
    st.plotly_chart(fig_salary, use_container_width=True)

with col2:
    # Salary by seniority
    salary_by_seniority = filtered_df.groupby('seniority')['avg_salary_lpa'].median().reset_index()
    salary_by_seniority = salary_by_seniority.sort_values('avg_salary_lpa')
    
    fig_seniority = px.bar(
        salary_by_seniority,
        x='avg_salary_lpa',
        y='seniority',
        orientation='h',
        title='Median Salary by Seniority Level',
        labels={'avg_salary_lpa': 'Median Salary (₹ LPA)', 'seniority': 'Seniority Level'},
        color='avg_salary_lpa',
        color_continuous_scale='Oranges',
        text='avg_salary_lpa'
    )
    fig_seniority.update_traces(texttemplate='₹%{text:.1f}L', textposition='outside')
    fig_seniority.update_layout(showlegend=False)
    st.plotly_chart(fig_seniority, use_container_width=True)

# Salary by job category
cat_salary = filtered_df.groupby('job_category').agg({
    'avg_salary_lpa': 'median',
    'job_title': 'count'
}).rename(columns={'job_title': 'count'}).reset_index()
cat_salary = cat_salary[cat_salary['count'] >= 5].sort_values('avg_salary_lpa', ascending=False).head(10)

fig_cat_sal = px.bar(
    cat_salary,
    x='avg_salary_lpa',
    y='job_category',
    orientation='h',
    title='Median Salary by Job Category (min 5 jobs)',
    labels={'avg_salary_lpa': 'Median Salary (₹ LPA)', 'job_category': 'Job Category'},
    color='avg_salary_lpa',
    color_continuous_scale='RdYlGn',
    text='avg_salary_lpa'
)
fig_cat_sal.update_traces(texttemplate='₹%{text:.1f}L', textposition='outside')
fig_cat_sal.update_layout(showlegend=False, height=500)
st.plotly_chart(fig_cat_sal, use_container_width=True)

st.divider()

# Row 2: Skills Analysis
st.header("🛠️ Skills Analysis")

skill_cols = [col for col in filtered_df.columns if col.startswith('skill_')]
skill_counts = {}
for col in skill_cols:
    skill_name = col.replace('skill_', '').replace('_', ' ').title()
    count = filtered_df[col].sum()
    if count > 0:
        skill_counts[skill_name] = count

top_skills = dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:12])

if len(top_skills) > 0:
    skills_df = pd.DataFrame({
        'Skill': list(top_skills.keys()),
        'Count': list(top_skills.values())
    })
    skills_df['Percentage'] = (skills_df['Count'] / len(filtered_df) * 100).round(1)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_skills = px.bar(
            skills_df,
            x='Count',
            y='Skill',
            orientation='h',
            title='Top 12 Most In-Demand Skills',
            labels={'Count': 'Number of Jobs'},
            color='Count',
            color_continuous_scale='Blues',
            text='Count'
        )
        fig_skills.update_traces(textposition='outside')
        fig_skills.update_layout(showlegend=False, height=500)
        st.plotly_chart(fig_skills, use_container_width=True)
    
    with col2:
        st.subheader("Skills Demand")
        st.dataframe(
            skills_df[['Skill', 'Percentage']].rename(columns={'Percentage': '% of Jobs'}),
            hide_index=True,
            height=500
        )
else:
    st.info("No skill data available for the selected filters.")

st.divider()

# Row 3: Job Categories
st.header("📊 Job Category Distribution")

col1, col2 = st.columns(2)

with col1:
    # Job category distribution
    job_cats = filtered_df['job_category'].value_counts().head(8).reset_index()
    job_cats.columns = ['Category', 'Count']
    
    fig_cats = px.pie(
        job_cats,
        values='Count',
        names='Category',
        title='Top 8 Job Categories',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_cats.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_cats, use_container_width=True)

with col2:
    # Seniority distribution
    seniority_dist = filtered_df['seniority'].value_counts().reset_index()
    seniority_dist.columns = ['Level', 'Count']
    
    fig_sen = px.bar(
        seniority_dist,
        x='Count',
        y='Level',
        orientation='h',
        title='Distribution by Seniority Level',
        color='Count',
        color_continuous_scale='Greens',
        text='Count'
    )
    fig_sen.update_traces(textposition='outside')
    fig_sen.update_layout(showlegend=False)
    st.plotly_chart(fig_sen, use_container_width=True)

st.divider()

# Row 4: Top Companies
st.header("🏢 Top Hiring Companies")

top_companies = filtered_df['company'].value_counts().head(15).reset_index()
top_companies.columns = ['Company', 'Jobs']

fig_companies = px.bar(
    top_companies,
    x='Jobs',
    y='Company',
    orientation='h',
    title='Top 15 Companies Hiring Data Professionals',
    color='Jobs',
    color_continuous_scale='Purples',
    text='Jobs'
)
fig_companies.update_traces(textposition='outside')
fig_companies.update_layout(showlegend=False, height=600)
st.plotly_chart(fig_companies, use_container_width=True)

st.divider()

# Row 5: Experience Analysis
st.header("📈 Experience Requirements")

col1, col2 = st.columns(2)

with col1:
    # Experience distribution
    exp_dist = filtered_df['min_experience_clean'].value_counts().sort_index().head(15).reset_index()
    exp_dist.columns = ['Experience (years)', 'Jobs']
    
    fig_exp = px.bar(
        exp_dist,
        x='Experience (years)',
        y='Jobs',
        title='Job Distribution by Experience Required',
        color='Jobs',
        color_continuous_scale='Teal'
    )
    fig_exp.update_layout(showlegend=False)
    st.plotly_chart(fig_exp, use_container_width=True)

with col2:
    # Salary vs Experience
    exp_salary = filtered_df.groupby('min_experience_clean')['avg_salary_lpa'].median().reset_index()
    exp_salary = exp_salary[exp_salary['min_experience_clean'] <= 15]
    
    fig_exp_sal = px.line(
        exp_salary,
        x='min_experience_clean',
        y='avg_salary_lpa',
        title='Median Salary by Years of Experience',
        labels={'min_experience_clean': 'Years of Experience', 'avg_salary_lpa': 'Median Salary (₹ LPA)'},
        markers=True
    )
    fig_exp_sal.update_traces(line_color='#E74C3C', marker=dict(size=10))
    st.plotly_chart(fig_exp_sal, use_container_width=True)

st.divider()

# Key Insights
st.header("💡 Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💰 Salary by Level")
    for level in ['Junior', 'Mid-Level', 'Senior']:
        level_data = filtered_df[filtered_df['seniority'] == level]['avg_salary_lpa']
        if len(level_data) > 0:
            st.metric(level, f"₹{level_data.median():.1f}L", f"{len(level_data)} jobs")

with col2:
    st.subheader("🛠️ Must-Have Skills")
    top_3 = list(top_skills.keys())[:3] if len(top_skills) >= 3 else list(top_skills.keys())
    for i, skill in enumerate(top_3, 1):
        pct = (top_skills[skill] / len(filtered_df)) * 100
        st.write(f"**{i}. {skill}** - {pct:.0f}% of jobs")

with col3:
    st.subheader("📊 Market Snapshot")
    top_cat = filtered_df['job_category'].mode()[0] if len(filtered_df) > 0 else "N/A"
    top_cat_count = len(filtered_df[filtered_df['job_category'] == top_cat])
    
    st.metric("Top Category", top_cat)
    st.write(f"**{top_cat_count} openings**")
    
    if len(filtered_df[filtered_df['avg_salary_lpa'].notna()]) > 0:
        salary_range = f"₹{filtered_df['avg_salary_lpa'].min():.1f}L - ₹{filtered_df['avg_salary_lpa'].max():.1f}L"
        st.write(f"**Salary Range:** {salary_range}")

# Additional context
st.divider()
st.subheader("📌 Market Insights")

col1, col2 = st.columns(2)

with col1:
    st.write("**Salary Growth Potential:**")
    junior_sal = filtered_df[filtered_df['seniority'] == 'Junior']['avg_salary_lpa'].median()
    senior_sal = filtered_df[filtered_df['seniority'] == 'Senior']['avg_salary_lpa'].median()
    
    if pd.notna(junior_sal) and pd.notna(senior_sal) and junior_sal > 0:
        growth_pct = ((senior_sal - junior_sal) / junior_sal) * 100
        st.write(f"- Junior to Senior: +{growth_pct:.0f}% (₹{senior_sal - junior_sal:.1f}L increase)")
        st.write(f"- Entry level starts at ₹{junior_sal:.1f}L")
        st.write(f"- Senior level reaches ₹{senior_sal:.1f}L")

with col2:
    st.write("**Job Market Composition:**")
    for cat in filtered_df['job_category'].value_counts().head(3).index:
        count = len(filtered_df[filtered_df['job_category'] == cat])
        pct = (count / len(filtered_df)) * 100
        st.write(f"- {cat}: {pct:.1f}% of market")

# Footer
st.divider()
st.markdown("""
---
### 📊 About This Analysis

**Data Source:** Indian Data Science Job Postings (1,600+ jobs)  
**Analysis Period:** 2024-2025  
**Coverage:** Major Indian cities and companies  

**Methodology:**
- Data extracted from multiple job portals
- Salary ranges standardized to LPA format
- Skills categorized from job titles and descriptions
- Seniority levels classified automatically
- Outliers removed (salaries < ₹1L or > ₹100L)

---


---

*This dashboard helps data science professionals understand the Indian job market. Use filters to explore salaries, skills, and opportunities.*

⭐ **Found this helpful? Star the project on GitHub!**
""")