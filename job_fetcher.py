import requests

def get_jobs(role):
    url = f"https://remotive.com/api/remote-jobs?search={role}"
    
    response = requests.get(url)
    data = response.json()
    
    jobs = []
    
    for job in data["jobs"]:
        title = job["title"]
        company = job["company_name"]
        jobs.append(title + " - " + company)
    
    return jobs