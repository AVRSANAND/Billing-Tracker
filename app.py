# ============================================================================
# FILE: app.py (NO PANDAS VERSION - FIXED)
# ============================================================================
from flask import Flask, render_template, jsonify, request
from data_manager import DataManager
from utils import *
from config import Config
from datetime import datetime
import traceback

app = Flask(__name__)
app.config.from_object(Config)

# Initialize data manager
data_manager = DataManager(app.config['EXCEL_FILE_PATH'])

@app.route('/')
def index():
    """Homepage with three project sections"""
    try:
        # Get all projects
        ongoing = data_manager.get_projects(status='Ongoing')
        upcoming = data_manager.get_projects(status='Upcoming')
        completed = data_manager.get_projects(status='Completed')
        
        return render_template('index.html',
                             ongoing_projects=ongoing,
                             upcoming_projects=upcoming,
                             completed_projects=completed,
                             tools=Config.TOOLS,
                             active_page='home')
    except Exception as e:
        return f"Error: {str(e)}<br>{traceback.format_exc()}", 500

@app.route('/api/project/<int:project_id>')
def project_details(project_id):
    """Get project details with team members grouped by tool"""
    try:
        data = data_manager.load_data()
        
        # Get project info
        project = None
        for p in data['projects']:
            if p.get('Project_ID') == project_id:
                project = p.copy()
                break
        
        if not project:
            return jsonify({'success': False, 'error': 'Project not found'}), 404
        
        # Format dates
        if project.get('Start_Date'):
            project['Start_Date'] = project['Start_Date'].strftime('%Y-%m-%d')
        if project.get('End_Date'):
            project['End_Date'] = project['End_Date'].strftime('%Y-%m-%d')
        
        # Get project members
        members_list = data_manager.get_project_members(project_id)
        
        # Group by tool
        grouped_members = {}
        for tool in Config.TOOLS:
            tool_members = [m for m in members_list if m.get('Tool') == tool]
            
            members_formatted = []
            for member in tool_members:
                billed_days = count_billed_days(
                    data['daily_billing'],
                    member.get('Employee_ID'),
                    project_id,
                    data['assignments']
                )
                
                members_formatted.append({
                    'Employee_ID': int(member.get('Employee_ID', 0)),
                    'Employee_Name': member.get('Employee_Name', 'Unknown'),
                    'Role': member.get('Role', 'N/A'),
                    'Billing_Start_Date': member.get('Billing_Start_Date').strftime('%Y-%m-%d') if member.get('Billing_Start_Date') else 'N/A',
                    'Billing_End_Date': member.get('Billing_End_Date').strftime('%Y-%m-%d') if member.get('Billing_End_Date') else 'N/A',
                    'billed_days': billed_days
                })
            
            if members_formatted:
                grouped_members[tool] = members_formatted
        
        return jsonify({
            'success': True,
            'project': project,
            'members': grouped_members
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/tool/<tool_name>')
def tool_dashboard(tool_name):
    """Tool-specific dashboard"""
    try:
        if tool_name not in Config.TOOLS:
            return "Invalid tool", 404
        
        data = data_manager.load_data()
        employees = data_manager.get_employees(tool=tool_name)
        
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # Calculate metrics for each employee
        members_data = []
        for emp in employees:
            emp_id = emp.get('Employee_ID')
            
            # Current month billability
            current_billability = calculate_monthly_billability(
                data['daily_billing'], emp_id, current_year, current_month
            )
            
            # Yearly billability
            yearly_billability = calculate_yearly_billability(
                data['daily_billing'], emp_id, current_year
            )
            
            # Monthly trend
            trend = get_monthly_trend(
                data['daily_billing'], emp_id, current_year
            )
            
            # Project counts
            current_projects = get_current_projects_count(
                data['assignments'], data['projects'], emp_id
            )
            
            yearly_projects = get_yearly_projects_count(
                data['assignments'], data['projects'], emp_id, current_year
            )
            
            members_data.append({
                'Employee_ID': int(emp_id),
                'Employee_Name': emp.get('Employee_Name', 'Unknown'),
                'Role': emp.get('Role', 'N/A'),
                'current_billability': current_billability,
                'yearly_billability': yearly_billability,
                'trend': trend,
                'current_projects': current_projects,
                'yearly_projects': yearly_projects
            })
        
        # Sort by yearly billability
        members_data.sort(key=lambda x: x['yearly_billability'], reverse=True)
        
        # Calculate average billability for the tool
        avg_billability = round(
            sum(m['current_billability'] for m in members_data) / len(members_data), 1
        ) if members_data else 0
        
        return render_template('tool_dashboard.html',
                             tool_name=tool_name,
                             members=members_data,
                             total_members=len(members_data),
                             avg_billability=avg_billability,
                             tools=Config.TOOLS,
                             active_page=tool_name)
    
    except Exception as e:
        return f"Error: {str(e)}<br>{traceback.format_exc()}", 500

@app.route('/member/<int:employee_id>')
def member_profile(employee_id):
    """Individual member profile page"""
    try:
        data = data_manager.load_data()
        
        # Get employee details
        employee = None
        for emp in data['employees']:
            if emp.get('Employee_ID') == employee_id:
                employee = emp
                break
        
        if not employee:
            return "Employee not found", 404
        
        current_year = datetime.now().year
        
        # Get all projects
        projects_list = data_manager.get_employee_projects(employee_id, current_year)
        
        projects_formatted = []
        for proj in projects_list:
            billed_days = count_billed_days(
                data['daily_billing'],
                employee_id,
                proj.get('Project_ID'),
                data['assignments']
            )
            
            projects_formatted.append({
                'Project_ID': int(proj.get('Project_ID', 0)),
                'Project_Name': proj.get('Project_Name', 'Unknown'),
                'Project_Status': proj.get('Project_Status', 'N/A'),
                'Start_Date': proj.get('Billing_Start_Date').strftime('%Y-%m-%d') if proj.get('Billing_Start_Date') else 'N/A',
                'End_Date': proj.get('Billing_End_Date').strftime('%Y-%m-%d') if proj.get('Billing_End_Date') else 'N/A',
                'billed_days': billed_days
            })
        
        # Monthly billability
        monthly_trend = get_monthly_trend(
            data['daily_billing'], employee_id, current_year
        )
        
        # Yearly grid
        yearly_grid = generate_yearly_grid(
            data['daily_billing'], employee_id, current_year
        )
        
        # Overall stats
        yearly_billability = calculate_yearly_billability(
            data['daily_billing'], employee_id, current_year
        )
        
        return render_template('member_profile.html',
                             employee={
                                 'Employee_ID': int(employee_id),
                                 'Employee_Name': employee.get('Employee_Name', 'Unknown'),
                                 'Tool': employee.get('Tool', 'N/A'),
                                 'Role': employee.get('Role', 'N/A'),
                                 'Joining_Date': employee.get('Joining_Date').strftime('%Y-%m-%d') if employee.get('Joining_Date') else 'N/A'
                             },
                             projects=projects_formatted,
                             monthly_trend=monthly_trend,
                             yearly_grid=yearly_grid,
                             yearly_billability=yearly_billability,
                             tools=Config.TOOLS,
                             active_page='profile')
    
    except Exception as e:
        return f"Error: {str(e)}<br>{traceback.format_exc()}", 500

@app.route('/api/reload')
def reload_data():
    """Force reload Excel data"""
    try:
        data_manager.load_data(force_reload=True)
        return jsonify({'success': True, 'message': 'Data reloaded successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)