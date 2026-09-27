# Punjab Annual School Census Dashboard

An interactive data analysis and visualization dashboard for the Punjab Annual School Census (October 2018). Built with Python, Streamlit, SQLite, and Plotly.

## 📊 Project Overview

This project processes and visualizes school infrastructure and demographic data from the Punjab (Pakistan) Annual School Census. The dashboard provides insights into:

- **Infrastructure access**: Electricity, drinking water, toilets, boundary walls
- **Resource availability**: Computers, books, science labs, internet
- **Staffing metrics**: Student-teacher ratios, teacher counts
- **Enrollment patterns**: By district, school type, and gender
- **District-level comparisons**: Rankings and gap analysis

## 🗂️ Project Structure

```
Punjab Annual School Census/
├── app.py                    # Streamlit dashboard application
├── main.py                   # Data processing & ETL pipeline
├── punjab_schools.db         # SQLite database (cleaned data)
├── public-census_oct_2018.xlsx  # Raw census data (October 2018)
└── testing.ipynb             # Exploratory analysis notebook
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Required packages (install via pip):
  ```bash
  pip install streamlit pandas sqlite3 plotly openpyxl
  ```

### Running the Dashboard

1. **Process the raw data** (first time only):
   ```bash
   python main.py
   ```
   This reads the Excel file, cleans/transforms the data, and creates `punjab_schools.db`.

2. **Launch the dashboard**:
   ```bash
   streamlit run app.py
   ```
   Opens at `http://localhost:8501`

## 📈 Dashboard Features

### Three Interactive Views

| View | Trigger | Shows |
|------|---------|-------|
| **District Overview** | No filters selected | All-district comparison charts & rankings |
| **District Detail** | District selected, no school | School-level breakdown within district |
| **School Detail** | Specific school selected | Individual school metrics & full record |

### Key Visualizations

1. **Electricity & Water Access by District** — % schools without electricity/water
2. **Infrastructure: Boys vs Girls Schools** — Boundary walls, average toilets by gender
3. **Resources by School Type** — Avg computers, books, science labs by school category
4. **Student-Teacher Ratio by District** — Overcrowding hotspots (ranked)
5. **District Enrollment Rankings** — Top districts by total enrollment

### Filters

- **District dropdown**: Filter to a specific district
- **School dropdown**: Drill down to individual school (enabled after district selection)

## 🔧 Data Processing Pipeline (`main.py`)

The ETL script performs:

1. **Reads raw Excel** (`public-census_oct_2018.xlsx`)
2. **Cleans binary columns** — Maps 0/1/2 to "No"/"Yes"/"Partial"
3. **Standardizes categorical data** — Security status, district names
4. **Enforces numeric types** — Enrollment, teachers, computers, books, toilets
5. **Groups school types** — Consolidates rare categories into "Other"
6. **Filters invalid rows** — Drops records missing district or enrollment
7. **Loads to SQLite** — Creates `punjab_schools.db` with `schools` table

## 📋 Database Schema

The `schools` table contains:

| Column | Type | Description |
|--------|------|-------------|
| `school_name` | TEXT | School name |
| `district` | TEXT | District name |
| `school_gender` | TEXT | Boys / Girls / Co-ed |
| `school_type` | TEXT | Original school type |
| `school_type_grouped` | TEXT | Grouped: Govt/ Model/ PSSP/ Community/ Other |
| `enrollment` | INTEGER | Total student enrollment |
| `Teachers` | INTEGER | Number of teachers |
| `NonTeachers` | INTEGER | Non-teaching staff |
| `electricity` | TEXT | Yes / No |
| `drink_water` | TEXT | Yes / No / Partial |
| `boundary_wall` | TEXT | Yes / No |
| `toilets` | TEXT | Yes / No / Partial |
| `total_toilets` | INTEGER | Total toilet count |
| `usable_toilets` | INTEGER | Usable toilet count |
| `total_computers` | INTEGER | Computer count |
| `total_books` | INTEGER | Book count |
| `internet` | TEXT | Yes / No |
| `science_lab` | TEXT | Yes / No |
| `security_clean` | TEXT | Security status |

## 🎯 Use Cases

- **Policy makers**: Identify infrastructure gaps by district
- **Education planners**: Target resources to overcrowded/under-resourced areas
- **Researchers**: Analyze gender disparities in school facilities
- **NGOs**: Prioritize interventions for schools lacking basics (water, electricity, toilets)

## 📦 Data Source

**Punjab Annual School Census — October 2018**  
Public dataset covering all registered schools in Punjab province, Pakistan.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project uses public census data. The analysis code is open for educational and research purposes.

---

*Built with Streamlit, Plotly, and SQLite • Data from Punjab Annual School Census 2018*