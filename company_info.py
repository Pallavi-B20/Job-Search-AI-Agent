# utils/company_info.py

def get_company_info(company):
    """
    Simple company info lookup
    """
    data = {
        "Google": "Tech company, good salary, global",
        "Infosys": "Indian IT company, large workforce",
        "TCS": "Large IT services company, India-based"
    }
    return data.get(company, "No info available")
