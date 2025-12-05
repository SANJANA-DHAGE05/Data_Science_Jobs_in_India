# Data_Science_Jobs_in_India
# 🇮🇳 India Data Science Job Market Analysis 2025



**🔗 Live Dashboard:**
https://datasciencejobsinindia.streamlit.app/

A detailed analysis of **1600+ Data Science job postings in India**, covering salary insights, hiring trends, top skills, role-wise demand, and company-wise analytics.  
This project helps job seekers, data science aspirants, and working professionals understand the real Indian job market.

---

## 🎯 Project Objectives

- Analyze India’s **data science job market** using real job posting data  
- Understand **role-wise demand** (Data Scientist, Analyst, ML Engineer, etc.)  
- Extract **skills, salaries, experience**, and **company insights**  
- Build an interactive **Streamlit dashboard**  
- Present data insights clearly for career decision-making  

---

## 📈 Key Insights

- Salary trends across **entry, mid, senior** levels  
- Top technical skills: **Python, SQL, Machine Learning, Data Visualization**  
- Role-wise job distribution  
- Hiring patterns across companies and industries  
- Correlation between experience and salary  
- Skill frequency analysis  

---

## 🧰 Tech Stack Used

- **Python**
- **Pandas**, **NumPy**
- **Matplotlib**, **Seaborn**
- **Plotly** (interactive graphs)
- **Streamlit** (dashboard)
- **Jupyter Notebook**

---

## 🗂️ Project Structure
India-Data-Science-Jobs-Analysis/
├── data/
│ ├── raw/
│ │ └── Data_Science_Jobs_in_India.csv
│ └── processed/
│ └── india_jobs_cleaned.csv
├── notebooks/
│ ├── 01_india_data_exploration.ipynb
│ ├── 02_india_data_cleaning.ipynb
│ └── 03_india_analysis.ipynb
├── outputs/
│ └── plots/
├── app_india.py
├── requirements.txt
└── README.md


---

## 🔧 Installation & Run Locally

1️⃣ **Clone the repository**
```bash
git clone https://github.com/yourusername/india-data-science-job-market-analysis.git
cd india-data-science-job-market-analysis

2️⃣ Install dependencies

pip install -r requirements.txt


3️⃣ Run Streamlit app

streamlit run app_india.py


App opens at: http://localhost:8501

🧪 Steps Performed in the Project
 **Data Cleaning

Removed duplicates & missing values

Cleaned text fields

Standardized salary formats

Extracted experience, location, job role

**Feature Engineering

Skill extraction (Python, SQL, ML, Excel, etc.)

Seniority classification

Experience bucket categorization

Salary normalization

Role segmentation

Company extraction

** Exploratory Data Analysis (EDA)

Salary distributions

Skill frequency

Experience vs salary correlation

Company-wise hiring

Job category comparisons

** Dashboard Development

Built an interactive Streamlit app with:

Filters for skills, roles, salary, company

Interactive Plotly charts

Clean UI/UX for insights presentation

** Features of the Streamlit Dashboard

📌 Salary breakdown by role

📌 Skill frequency heatmap

📌 Top hiring companies

📌 Experience vs salary trend

📌 Role-wise job availability

📌 Interactive charts with filters

📌 Clean and simple UI

** Future Enhancements

City-wise job market breakdown

Remote vs onsite salary comparison

Sector-wise insights (IT, Finance, E-commerce)

Trend analysis over time

Job recommendation engine based on user skills

