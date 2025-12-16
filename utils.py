# ============================================================================
# FILE: utils.py (NO PANDAS VERSION)
# ============================================================================
from datetime import datetime, date, timedelta
from calendar import monthrange
from typing import List, Dict

def calculate_working_days(year: int, month: int) -> int:
    """Calculate working days (Mon-Fri) in a month"""
    _, last_day = monthrange(year, month)
    working_days = 0
    
    for day in range(1, last_day + 1):
        d = date(year, month, day)
        if d.weekday() < 5:  # Monday=0, Sunday=6
            working_days += 1
    
    return working_days

def calculate_monthly_billability(billing_records: List[Dict], 
                                  employee_id: int, 
                                  year: int, 
                                  month: int) -> float:
    """Calculate billability % for an employee in a specific month"""
    
    # Filter billing records for this employee and month
    billed_days = 0
    for record in billing_records:
        if (record.get('Employee_ID') == employee_id and 
            record.get('Date') and
            record.get('Date').year == year and
            record.get('Date').month == month and
            record.get('Is_Billed') == 'Yes'):
            billed_days += 1
    
    working_days = calculate_working_days(year, month)
    
    if working_days == 0:
        return 0.0
    
    return round((billed_days / working_days) * 100, 1)

def get_monthly_trend(billing_records: List[Dict], 
                     employee_id: int, 
                     year: int) -> List[Dict]:
    """Get monthly billability from Jan to current month"""
    current_month = datetime.now().month if year == datetime.now().year else 12
    trend = []
    
    for month in range(1, current_month + 1):
        billability = calculate_monthly_billability(
            billing_records, employee_id, year, month
        )
        trend.append({
            'month': month,
            'month_name': date(year, month, 1).strftime('%b'),
            'billability': billability
        })
    
    return trend

def calculate_yearly_billability(billing_records: List[Dict], 
                                 employee_id: int, 
                                 year: int) -> float:
    """Calculate overall billability for the year"""
    trend = get_monthly_trend(billing_records, employee_id, year)
    
    if not trend:
        return 0.0
    
    avg_billability = sum(t['billability'] for t in trend) / len(trend)
    return round(avg_billability, 1)

def generate_yearly_grid(billing_records: List[Dict], 
                        employee_id: int, 
                        year: int) -> List[Dict]:
    """Generate GitHub-style contribution grid for the year"""
    
    # Create a set of billed dates for quick lookup
    billed_dates = set()
    for record in billing_records:
        if (record.get('Employee_ID') == employee_id and 
            record.get('Date') and
            record.get('Date').year == year and
            record.get('Is_Billed') == 'Yes'):
            billed_dates.add(record['Date'].strftime('%Y-%m-%d'))
    
    # Generate grid
    start_date = date(year, 1, 1)
    end_date = min(date(year, 12, 31), date.today())
    
    grid = []
    current = start_date
    
    while current <= end_date:
        date_str = current.strftime('%Y-%m-%d')
        is_weekend = current.weekday() >= 5
        
        grid.append({
            'date': date_str,
            'is_billed': 1 if date_str in billed_dates else 0,
            'is_weekend': is_weekend,
            'day_of_week': current.weekday(),
            'week': current.isocalendar()[1]
        })
        
        current += timedelta(days=1)
    
    return grid

def count_billed_days(billing_records: List[Dict], 
                     employee_id: int, 
                     project_id: int,
                     assignments: List[Dict]) -> int:
    """Count billed days for an employee on a specific project"""
    
    # Get assignment dates
    assignment = None
    for a in assignments:
        if (a.get('Employee_ID') == employee_id and 
            a.get('Project_ID') == project_id):
            assignment = a
            break
    
    if not assignment:
        return 0
    
    start_date = assignment.get('Billing_Start_Date')
    end_date = assignment.get('Billing_End_Date')
    
    # Count billed days in this range
    billed_count = 0
    for record in billing_records:
        if (record.get('Employee_ID') == employee_id and
            record.get('Date') and
            record.get('Date') >= start_date and
            record.get('Date') <= end_date and
            record.get('Is_Billed') == 'Yes'):
            billed_count += 1
    
    return billed_count

def get_current_projects_count(assignments: List[Dict], 
                               projects: List[Dict],
                               employee_id: int) -> int:
    """Count current active projects for an employee"""
    
    # Get employee assignments
    employee_assignments = [a for a in assignments 
                           if a.get('Employee_ID') == employee_id]
    
    # Count projects with status 'Ongoing'
    current_count = 0
    for assignment in employee_assignments:
        proj_id = assignment.get('Project_ID')
        for project in projects:
            if (project.get('Project_ID') == proj_id and 
                project.get('Project_Status') == 'Ongoing'):
                current_count += 1
                break
    
    return current_count

def get_yearly_projects_count(assignments: List[Dict],
                              projects: List[Dict],
                              employee_id: int,
                              year: int) -> int:
    """Count all projects worked on in a year"""
    
    # Get employee assignments
    employee_assignments = [a for a in assignments 
                           if a.get('Employee_ID') == employee_id]
    
    # Count projects that overlap with the year
    yearly_projects = set()
    for assignment in employee_assignments:
        proj_id = assignment.get('Project_ID')
        for project in projects:
            if project.get('Project_ID') == proj_id:
                start_date = project.get('Start_Date')
                end_date = project.get('End_Date')
                
                if start_date and end_date:
                    if start_date.year == year or end_date.year == year:
                        yearly_projects.add(proj_id)
                break
    
    return len(yearly_projects)