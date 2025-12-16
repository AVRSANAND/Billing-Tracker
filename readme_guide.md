# 📊 Billability Tracking System - Complete Setup Guide

A production-ready Flask web application for tracking team billability across multiple tools using Excel as the single source of truth.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Project Structure](#project-structure)
- [Running the Application](#running-the-application)
- [Using the Application](#using-the-application)
- [Customizing Your Data](#customizing-your-data)
- [Troubleshooting](#troubleshooting)
- [Features Overview](#features-overview)

---

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (Python package installer - comes with Python)
- A text editor or IDE (VS Code, PyCharm, or any editor)
- A web browser (Chrome, Firefox, Safari, etc.)

### Check Your Python Installation

```bash
# Check Python version
python --version
# or
python3 --version

# Check pip version
pip --version
# or
pip3 --version
```

---

## 🚀 Installation Steps

### Step 1: Create Project Directory

```bash
# Create main project folder
mkdir billability_tracker
cd billability_tracker

# Create subdirectories
mkdir data
mkdir static
mkdir static/css
mkdir static/js
mkdir templates
```

### Step 2: Install Required Python Packages

```bash
# Install all dependencies
pip install flask pandas openpyxl

# Or if using pip3
pip3 install flask pandas openpyxl
```

**Package Details:**
- `flask` - Web framework
- `pandas` - Data processing and Excel handling
- `openpyxl` - Excel file reading/writing

### Step 3: Create Project Files

Create the following files in your project directory with the content from the artifact:

#### **Root Directory Files:**

1. **config.py**
```python
import os

class Config:
    SECRET_KEY = 'dev-secret-key'
    EXCEL_FILE_PATH = os.path.join('data', 'billability_data.xlsx')
    CACHE_TIMEOUT = 300
    
    COLORS = {
        'primary': '#0070AD',
        'secondary': '#12ABDB',
        'success': '#00A885',
        'warning': '#FFB81C',
        'danger': '#E4032E',
        'dark': '#001E50',
        'light': '#F8F9FA'
    }
    
    TOOLS = ['CAP360', 'BREAD', 'DCC']
```

2. **data_manager.py** - Copy from artifact (Excel data loading logic)

3. **utils.py** - Copy from artifact (Calculation utilities)

4. **app.py** - Copy from artifact (Main Flask application)

5. **create_sample_data.py** - Copy from artifact (Sample data generator)

#### **templates/ Directory:**

6. **templates/base.html** - Copy from artifact
7. **templates/index.html** - Copy from artifact
8. **templates/tool_dashboard.html** - Copy from artifact
9. **templates/member_profile.html** - Copy from artifact

#### **static/css/ Directory:**

10. **static/css/style.css** - Copy from artifact

### Step 4: Generate Sample Data

```bash
# Generate sample Excel file with test data
python create_sample_data.py
```

**This creates:**
- `data/billability_data.xlsx` with 4 sheets:
  - **Employees** (30 sample employees)
  - **Projects** (20 sample projects)
  - **Project_Assignments** (employee-project mappings)
  - **Daily_Billing** (daily billing records)

**Expected Output:**
```
✅ Sample Excel file created: data/billability_data.xlsx
   - 30 Employees
   - 20 Projects
   - XX Project Assignments
   - XXXX Daily Billing Records
```

---

## ▶️ Running the Application

### Start the Flask Server

```bash
# Run the application
python app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

Or:
```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

After setup, your directory should look like this:

```
billability_tracker/
│
├── data/
│   └── billability_data.xlsx          # Excel data file (generated)
│
├── static/
│   ├── css/
│   │   └── style.css                  # Custom styles
│   └── js/
│       └── (optional JavaScript files)
│
├── templates/
│   ├── base.html                      # Base template with sidebar
│   ├── index.html                     # Homepage
│   ├── tool_dashboard.html            # Tool-specific dashboard
│   └── member_profile.html            # Member profile page
│
├── config.py                          # Configuration settings
├── data_manager.py                    # Excel data handling
├── utils.py                           # Utility functions
├── app.py                             # Main Flask application
└── create_sample_data.py              # Sample data generator
```

---

## 🎯 Using the Application

### Homepage (`/`)

**Three Main Sections:**

1. **Ongoing Projects** (Green indicator)
   - Shows currently active projects
   - Click any card to see team members and billed days

2. **Upcoming Projects** (Yellow indicator)
   - Shows projects starting in the future
   - View expected team assignments

3. **Completed Projects** (Gray indicator)
   - Historical projects
   - View final billing data

### Sidebar Navigation

**Tool Dashboards:**
- Click **CAP360**, **BREAD**, or **DCC** to view tool-specific data

**Each Tool Dashboard Shows:**
- Total members count
- Average current month billability
- Search bar to find members
- Member cards with:
  - Current month billability %
  - Monthly trend chart
  - Active projects count
  - Total yearly projects

### Member Profiles

Click any member card to view:
- **Basic Information**: Name, role, tool, joining date
- **Monthly Billability Chart**: Bar chart showing Jan-Current month
- **Projects Table**: All projects with billed days
- **Yearly Calendar Grid**: GitHub-style contribution grid
  - 🔴 Red = Billed day
  - 🟢 Green = Not billed
  - ⬜ Gray = Weekend

### Reload Data Button

- Located in sidebar
- Refreshes data from Excel file
- Use after updating the Excel file

---

## 🔧 Customizing Your Data

### Option 1: Modify Sample Data

Edit `data/billability_data.xlsx` directly in Excel:

1. Open the file in Excel/LibreOffice
2. Modify any sheet (Employees, Projects, etc.)
3. Save the file
4. Click "Reload Data" in the app or wait 5 minutes for auto-refresh

### Option 2: Create Your Own Excel File

**Required Sheet Structure:**

#### Sheet 1: Employees
| Employee_ID | Employee_Name | Tool | Role | Joining_Date |
|-------------|---------------|------|------|--------------|
| 1 | John Doe | CAP360 | Engineer | 2023-01-15 |
| 2 | Jane Smith | BREAD | Lead | 2022-06-20 |

#### Sheet 2: Projects
| Project_ID | Project_Name | Tool | Project_Status | Start_Date | End_Date |
|------------|--------------|------|----------------|------------|----------|
| 1 | Portal V2 | CAP360 | Ongoing | 2024-01-01 | 2024-12-31 |
| 2 | Dashboard | BREAD | Completed | 2023-06-01 | 2024-03-31 |

**Project_Status values:** `Ongoing`, `Upcoming`, `Completed`

#### Sheet 3: Project_Assignments
| Employee_ID | Project_ID | Billing_Start_Date | Billing_End_Date | Billability_Percentage |
|-------------|------------|-------------------|------------------|----------------------|
| 1 | 1 | 2024-01-15 | 2024-12-31 | 85 |
| 2 | 2 | 2023-06-01 | 2024-03-31 | 100 |

#### Sheet 4: Daily_Billing (Optional)
| Employee_ID | Date | Is_Billed |
|-------------|------|-----------|
| 1 | 2024-01-15 | Yes |
| 1 | 2024-01-16 | Yes |

**Note:** If Daily_Billing sheet is missing, the app auto-generates it from Project_Assignments.

### Important Rules:

✅ **Date Format**: Use `YYYY-MM-DD` (e.g., 2024-12-31)
✅ **Tool Names**: Must match exactly: `CAP360`, `BREAD`, or `DCC`
✅ **Employee_ID**: Must be unique integers
✅ **Project_ID**: Must be unique integers
✅ **Is_Billed**: Use `Yes` or `No`

---

## 🐛 Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
# Install missing packages
pip install flask pandas openpyxl
```

### Issue: "Excel file not found"

**Solution:**
```bash
# Generate sample data
python create_sample_data.py

# Or check file location
# File must be at: data/billability_data.xlsx
```

### Issue: Port 5000 already in use

**Solution:**
```python
# Edit app.py, change the last line to:
if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Use different port
```

Then access: `http://localhost:8000`

### Issue: Excel file won't open/corrupt

**Solution:**
```bash
# Delete and regenerate
rm data/billability_data.xlsx
python create_sample_data.py
```

### Issue: Data not updating

**Solution:**
1. Click "Reload Data" button in sidebar
2. Or restart the Flask server:
   - Press `CTRL+C` to stop
   - Run `python app.py` again

### Issue: Charts not displaying

**Solution:**
- Check internet connection (Chart.js loads from CDN)
- Try a different browser
- Clear browser cache

### Issue: Python command not recognized

**Solution:**
```bash
# Try using python3 instead
python3 app.py
python3 create_sample_data.py

# Or check Python installation
which python
which python3
```

---

## ✨ Features Overview

### 🎨 User Interface
- ✅ Clean, professional Capgemini-branded design
- ✅ Responsive layout (works on mobile/tablet/desktop)
- ✅ Interactive cards and modals
- ✅ Smooth animations and transitions

### 📊 Analytics
- ✅ Real-time billability calculations
- ✅ Monthly trends (Jan to current month)
- ✅ Yearly averages and totals
- ✅ Working days calculation (excludes weekends)

### 🔍 Navigation
- ✅ Tool-based filtering (CAP360/BREAD/DCC)
- ✅ Member search functionality
- ✅ Project detail modals
- ✅ Breadcrumb navigation

### 📈 Visualizations
- ✅ Line charts for monthly trends
- ✅ Bar charts for billability
- ✅ GitHub-style contribution calendar
- ✅ Progress bars with color coding

### 💾 Data Management
- ✅ Excel as single source of truth
- ✅ 5-minute automatic cache refresh
- ✅ Manual reload capability
- ✅ No database required

### 🎯 Business Logic
- ✅ Multi-project assignments
- ✅ Tool-wise team organization
- ✅ Status-based project filtering
- ✅ Date-range validations

---

## 🔐 Production Deployment

### Security Recommendations

1. **Change SECRET_KEY in config.py:**
```python
import secrets
SECRET_KEY = secrets.token_hex(32)
```

2. **Use environment variables:**
```bash
export SECRET_KEY='your-secret-key-here'
export FLASK_ENV='production'
```

3. **Use a production WSGI server:**
```bash
pip install gunicorn
gunicorn app:app
```

### Performance Tips

1. **Increase cache timeout for production:**
```python
# config.py
CACHE_TIMEOUT = 600  # 10 minutes
```

2. **Enable gzip compression**
3. **Use a reverse proxy (nginx)**
4. **Monitor Excel file size (<10MB recommended)**

---

## 📞 Support

### Common Commands Reference

```bash
# Start application
python app.py

# Generate new sample data
python create_sample_data.py

# Install dependencies
pip install -r requirements.txt

# Check Python version
python --version

# View running processes
ps aux | grep python

# Stop the server
CTRL+C (in terminal)
```

### File Locations

- **Excel Data:** `data/billability_data.xlsx`
- **Main App:** `app.py`
- **Templates:** `templates/*.html`
- **Styles:** `static/css/style.css`
- **Configuration:** `config.py`

---

## 🎓 Next Steps

1. ✅ **Run the sample application**
2. ✅ **Explore all features**
3. ✅ **Update Excel with your real data**
4. ✅ **Customize colors in config.py**
5. ✅ **Add more tools if needed**
6. ✅ **Deploy to production server**

---

## 📝 Notes

- The application automatically handles weekends (excludes from working days)
- Billability is calculated as: `(Billed Days / Working Days) × 100`
- All dates in Excel must use format: `YYYY-MM-DD`
- Data caches for 5 minutes to improve performance
- No login/authentication included (add if needed)

---

## 🏆 Success Checklist

- [ ] Python 3.8+ installed
- [ ] All packages installed (`flask`, `pandas`, `openpyxl`)
- [ ] Project structure created
- [ ] All 10 files created correctly
- [ ] Sample data generated successfully
- [ ] Application runs without errors
- [ ] Can access http://localhost:5000
- [ ] All three tool dashboards work
- [ ] Member profiles display correctly
- [ ] Charts render properly

---

**🎉 Congratulations! Your billability tracking system is now ready to use!**

For questions or issues, review the Troubleshooting section above.