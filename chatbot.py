from job_fetcher import get_jobs

def chat(role, location):
    jobs = get_jobs(role)

    # 1️⃣ Try exact match
    filtered = []
    for job in jobs:
        if role.lower() in job.lower():
            filtered.append(job)

    if filtered:
        return filtered[:5]

    # 2️⃣ Try partial match (split words)
    role_words = role.lower().split()
    partial = []

    for job in jobs:
        if any(word in job.lower() for word in role_words):
            partial.append(job)

    if partial:
        return ["⚠️ Showing related jobs:"] + partial[:5]

    # 3️⃣ FINAL fallback (dynamic, not fixed)
    general_jobs = get_jobs("job")

    return [" Showing general jobs:"] + general_jobs[:5]