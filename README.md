NGO Analytics Portfolio
End-to-End Data Analytics Project Using Python, SQL, Excel & Power BI
An end-to-end Data Analytics portfolio project focused on analyzing NGO operations, donation performance, fundraising campaigns, donor behavior, and volunteer activity.
This project demonstrates how raw business data can be transformed into actionable insights using Python, SQL, Excel, and Power BI.
The project follows a practical analytics workflow:
Data Generation → Data Preparation → SQL Database → Exploratory Data Analysis → Segmentation → Excel Analysis → Power BI Dashboard → Business Insights
________________________________________
Project Overview
Non-governmental organizations (NGOs) manage donations, fundraising campaigns, volunteers, and multiple operational activities.
The objective of this project is to analyze these areas and answer important business questions such as:
•	How are donations performing over time?
•	Which campaigns generate the highest donation value?
•	Which NGOs receive the most donations?
•	What are the major donation trends?
•	How do donor behaviors differ?
•	How can donors or entities be segmented using data?
•	How can volunteer activity be analyzed?
•	What KPIs can help management monitor fundraising performance?
•	How can analytical findings be presented through an interactive dashboard?
The project combines multiple analytics technologies to create a complete data analysis workflow.
________________________________________
Business Objectives
The main objectives of this project are:
1.	Analyze donation and fundraising performance.
2.	Identify important trends and patterns in donation data.
3.	Compare NGO and campaign performance.
4.	Analyze donor behavior and contribution patterns.
5.	Segment entities based on relevant behavioral metrics.
6.	Analyze volunteer participation.
7.	Build reusable analytical datasets and database tables.
8.	Create an Excel-based donation analysis.
9.	Develop an interactive Power BI dashboard.
10.	Generate business-oriented insights from the analysis.
________________________________________
Dataset Overview
The project uses a synthetically generated dataset designed to simulate a realistic NGO analytics environment.
Dataset Size
Dataset	Records
NGOs	10
Dates	1,826
Campaigns	61
Donations	6,000
Volunteers	1,500
Simulated Donation Value
Approximately ₹13.13 Crore in total donation transactions.
Note: The data is synthetic and created for educational, analytical, and portfolio demonstration purposes. It does not represent real NGO financial records.
________________________________________
Tech Stack
Programming & Analysis
•	Python
•	Pandas
•	NumPy
•	Matplotlib
•	Scikit-learn
Database & SQL
•	SQLite
•	SQL
Spreadsheet Analysis
•	Microsoft Excel
•	Pivot Tables
•	Data Analysis
•	Charts
Business Intelligence
•	Microsoft Power BI
•	DAX
•	Data Modeling
•	Interactive Dashboard Development
Development Tools
•	VS Code
•	Git
•	GitHub
•	SQLite Viewer
________________________________________
Project Architecture
Raw / Synthetic Data
        │
        ▼
Python Data Generation
        │
        ▼
Data Cleaning & Preparation
        │
        ├──────────────► Exploratory Data Analysis
        │                         │
        │                         ▼
        │                  Statistical Insights
        │
        ▼
SQLite Database
        │
        ▼
SQL Analysis
        │
        ├──────────────► Excel Analysis
        │
        └──────────────► Power BI Data Model
                                  │
                                  ▼
                           DAX Measures
                                  │
                                  ▼
                         Interactive Dashboard
                                  │
                                  ▼
                           Business Insights
________________________________________
Project Structure
NGO_Analytics_Portfolio/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│   └── ngo_analytics.db
│
├── scripts/
│   ├── 01_generate_synthetic_data.py
│   ├── 02_build_sqlite_db.py
│   ├── 03_exploratory_analysis.py
│   ├── 04_ngo_segmentation_clustering.py
│   └── 05_build_donations_excel.py
│
├── excel/
│   └── donations_analysis.xlsx
│
├── powerbi/
│   ├── star_schema/
│   ├── DAX_measures.txt
│   └── POWERBI_BUILD_GUIDE.md
│
├── docs/
│
├── screenshots/
│
└── README.md
Folder names may vary slightly depending on the final repository structure.
________________________________________
Python Analysis
Python is used as the primary analysis and data-processing layer.
Key Python Tasks
•	Synthetic dataset generation
•	Data preparation
•	Data validation
•	Exploratory Data Analysis
•	Aggregation and transformation
•	Trend analysis
•	Statistical exploration
•	Donor/entity segmentation
•	Exporting analytical datasets
Main Python Scripts
01_generate_synthetic_data.py
Generates the synthetic NGO ecosystem including:
•	NGO records
•	Campaign records
•	Donation transactions
•	Volunteer records
•	Date information
________________________________________
02_build_sqlite_db.py
Creates the SQLite database and loads the generated datasets into structured database tables.
________________________________________
03_exploratory_analysis.py
Performs exploratory analysis to identify:
•	Donation trends
•	Distribution patterns
•	Campaign performance
•	NGO-level performance
•	Donation behavior
•	Key relationships within the dataset
________________________________________
04_ngo_segmentation_clustering.py
Applies clustering techniques using Scikit-learn to identify groups based on selected analytical features.
This demonstrates the application of unsupervised machine learning in a business analytics context.
________________________________________
05_build_donations_excel.py
Processes donation data and creates an Excel-based analytical workbook for further business analysis.
________________________________________
SQL Analysis
SQLite is used to create a structured analytical database.
The SQL layer demonstrates practical skills such as:
•	SELECT statements
•	Filtering
•	Sorting
•	GROUP BY
•	Aggregations
•	JOIN operations
•	Date-based analysis
•	Business KPI calculations
•	Entity-level comparisons
The database provides a structured environment for analyzing donations, campaigns, NGOs, volunteers, and related dimensions.
________________________________________
Excel Analysis
Excel is used as an additional business analysis and reporting layer.
The analysis includes:
•	Donation summaries
•	Campaign performance
•	NGO comparisons
•	Aggregated metrics
•	Pivot-based analysis
•	Charts and visual summaries
This demonstrates the ability to convert analytical data into a format commonly used by business teams.
________________________________________
Power BI Dashboard
Power BI is used to create an interactive business intelligence layer.
The dashboard is designed around key NGO fundraising and operational metrics.
Dashboard Areas
•	Donation KPIs
•	Donation trends
•	NGO performance
•	Campaign performance
•	Donation distribution
•	Donor/entity analysis
•	Volunteer insights
•	Interactive filtering
Power BI Skills Demonstrated
•	Data loading
•	Data transformation
•	Star schema modeling
•	Relationships
•	DAX measures
•	KPI development
•	Interactive visualizations
•	Dashboard design
•	Business-focused storytelling
________________________________________
Data Modeling
The Power BI implementation uses a star-schema-oriented approach.
The model separates analytical facts from descriptive dimensions to improve:
•	Data organization
•	Relationship management
•	Reporting flexibility
•	DAX calculations
•	Dashboard performance
Example conceptual model:
              ┌──────────────┐
              │  Dim Date    │
              └──────┬───────┘
                     │
                     │
┌──────────────┐     │     ┌────────────────┐
│  Dim NGO     │─────┤─────│ Fact Donations │
└──────────────┘     │     └───────┬────────┘
                     │             │
              ┌──────┴──────┐      │
              │ Dim Campaign│──────┘
              └─────────────┘
The final model can be extended with additional dimensions depending on reporting requirements.
________________________________________
DAX & KPI Development
DAX is used to create reusable analytical measures.
Examples of KPI categories include:
•	Total Donations
•	Donation Count
•	Average Donation
•	Campaign Performance
•	NGO Performance
•	Time-based Donation Trends
•	Comparative Metrics
•	Contribution Analysis
The repository contains the DAX measures used for the Power BI implementation.
________________________________________
Exploratory Data Analysis
The exploratory analysis focuses on understanding the structure and behavior of the data before building the final reporting layer.
Key areas include:
Donation Analysis
•	Total donation value
•	Donation frequency
•	Average donation
•	Donation distribution
•	Time-based trends
Campaign Analysis
•	Campaign contribution
•	Campaign-level comparisons
•	Donation volume
•	Fundraising patterns
NGO Analysis
•	NGO-level donation performance
•	Contribution comparison
•	Activity patterns
Volunteer Analysis
•	Volunteer participation
•	Activity distribution
•	Operational patterns
________________________________________
Segmentation Analysis
The project also explores segmentation using clustering techniques.
The purpose is to identify groups with similar characteristics rather than manually assigning categories.
The workflow includes:
Feature Selection
      ↓
Data Preparation
      ↓
Scaling / Transformation
      ↓
Clustering Algorithm
      ↓
Cluster Assignment
      ↓
Cluster Interpretation
This demonstrates how machine learning techniques can support exploratory business analytics.
________________________________________
Key Analytical Questions
This project is designed to answer questions such as:
Donation Performance
•	What is the overall donation value?
•	How many donation transactions were recorded?
•	What is the average donation?
•	How does donation activity change over time?
Campaign Performance
•	Which campaigns contribute significantly to fundraising?
•	How does donation activity vary between campaigns?
•	Which campaign characteristics are associated with higher contribution?
NGO Performance
•	How do NGOs compare based on donation activity?
•	Which NGOs have higher contribution levels?
•	How is donation activity distributed across organizations?
Donor / Entity Behavior
•	What patterns can be observed in contribution behavior?
•	Can entities be grouped based on similar characteristics?
•	What differences exist between identified segments?
Volunteer Analysis
•	How is volunteer activity distributed?
•	Which patterns can be observed in volunteer participation?
•	How can volunteer data support operational decision-making?
________________________________________
Business Insights
The analytical workflow is designed to transform transaction-level data into business-oriented insights.
Examples of insight categories include:
•	Donation trends and seasonality
•	Campaign contribution patterns
•	NGO performance differences
•	Donation concentration
•	Behavioral segments
•	Volunteer activity patterns
•	KPI-based performance monitoring
The final insights should be interpreted in the context of the synthetic dataset and should not be treated as conclusions about real NGOs.
________________________________________
Data Analytics Workflow
The complete project follows a practical analyst workflow:
1. Data Generation
Create realistic synthetic business data.
2. Data Preparation
Validate, transform, and organize datasets.
3. Database Development
Load structured data into SQLite.
4. Exploratory Analysis
Use Python to investigate trends and relationships.
5. Segmentation
Apply clustering to selected analytical features.
6. Excel Reporting
Create spreadsheet-based analysis.
7. Data Modeling
Prepare a reporting-friendly Power BI model.
8. DAX Development
Create reusable business measures.
9. Dashboard Development
Build interactive Power BI visualizations.
10. Business Interpretation
Convert analytical results into understandable business insights.
________________________________________
How to Run the Project
1. Clone the Repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
2. Navigate to the Project
cd NGO_Analytics_Portfolio
3. Create a Virtual Environment
python -m venv .venv
4. Activate the Virtual Environment
Windows
.venv\Scripts\activate
5. Install Required Libraries
pip install pandas numpy matplotlib scikit-learn openpyxl
6. Run the Scripts
Run the scripts in the following order:
python scripts/01_generate_synthetic_data.py
python scripts/02_build_sqlite_db.py
python scripts/03_exploratory_analysis.py
python scripts/04_ngo_segmentation_clustering.py
python scripts/05_build_donations_excel.py
File paths may need to be adjusted depending on the final repository structure.
________________________________________
Tools & Skills Demonstrated
Area	Skills
Python	Pandas, NumPy, Matplotlib, Data Processing
Statistics	Descriptive Analysis, Distribution Analysis
SQL	Queries, Aggregations, Joins, Filtering
SQLite	Database Creation & Management
Excel	Pivot Analysis, Reporting, Charts
Power BI	Data Modeling, Visualization, Dashboarding
DAX	Measures & KPI Calculations
Machine Learning	Clustering / Segmentation
Data Visualization	Charts, KPIs, Interactive Reports
Business Analytics	Performance & Trend Analysis
GitHub	Version Control & Portfolio Presentation
________________________________________
Project Highlights
•	End-to-end analytics workflow
•	Multi-tool data analysis project
•	Python-based data processing
•	SQL database implementation
•	Excel reporting
•	Power BI dashboard development
•	DAX-based KPI calculations
•	Star-schema-oriented data modeling
•	Clustering-based segmentation
•	Business-focused analytical questions
•	Portfolio-ready documentation
________________________________________
Limitations
This project uses synthetic data.
Therefore:
•	The records do not represent real NGO organizations.
•	Financial figures are simulated.
•	Patterns may not reflect real-world fundraising behavior.
•	Insights are intended for demonstration and learning purposes.
•	Results should not be used for actual financial or operational decisions.
________________________________________
Future Improvements
Possible future enhancements include:
•	Automated data pipelines
•	Real-world public NGO datasets
•	Advanced donor segmentation
•	Predictive donation modeling
•	Donation forecasting
•	Campaign response prediction
•	Automated Power BI refresh
•	Cloud database integration
•	Data quality monitoring
•	Advanced statistical testing
•	Deployment of analytical dashboards
________________________________________
Portfolio Purpose
This project was developed as part of my Data Analytics portfolio to demonstrate practical experience across the complete analytics lifecycle.
It focuses on not only performing technical analysis but also communicating results through structured databases, spreadsheets, dashboards, KPIs, and business-oriented insights.
________________________________________
Author
Mohd Azeem
Aspiring Data Analyst | Python | SQL | Excel | Power BI
This project represents my practical learning and application of data analytics concepts through an end-to-end portfolio project.
________________________________________
Connect With Me
LinkedIn:
https://www.linkedin.com/in/mohd-azeem-597a55230/
GitHub:
Add your GitHub profile/repository link here.
________________________________________
⭐ If You Find This Project Useful
Feel free to explore the repository, review the analysis, and provide feedback.
Thank you for visiting my NGO Analytics Portfolio!

