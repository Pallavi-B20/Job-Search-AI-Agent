class JobSearchAgent:

    def chat_with_agent(self, question):
        return "This is a demo AI response for: " + question

    def search_jobs(self, keyword, location, experience):
        # dummy jobs
        return [
            {"title": "Software Engineer", "company": "TCS", "location": "Bangalore"},
            {"title": "Data Analyst", "company": "Infosys", "location": "Mumbai"},
        ]

    def match_jobs(self, jobs, skills):
        matched = []
        for job in jobs:
            for skill in skills:
                if skill.lower() in job["title"].lower():
                    matched.append(job)
                    break
        return matched

    def company_info(self, company_name):
        return f"{company_name} is a reputed company with good work culture."

    def parse_resume(self, file):
        return "Resume parsed successfully (demo)"