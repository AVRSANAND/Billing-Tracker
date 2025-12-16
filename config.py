import os

class Config:
    SECRET_KEY = 'dev-secret-key'
    EXCEL_FILE_PATH = os.path.join('data', 'billability_data.xlsx')
    
    # Cache settings
    CACHE_TIMEOUT = 300  # 5 minutes
    
    # Capgemini colors
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
