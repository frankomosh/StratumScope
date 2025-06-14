import time
from collections import defaultdict

# Keeps last few jobs per source
job_cache = defaultdict(list)

# Comparison results
diff_log = []

MAX_HISTORY = 5


def update_jobs(entry):
    source = entry['source']
    job_cache[source].append(entry)
    if len(job_cache[source]) > MAX_HISTORY:
        job_cache[source].pop(0)

    compare_jobs()

def compare_jobs():
    job_sets = {}
    for source, jobs in job_cache.items():
        job_sets[source] = set(j['job_id'] for j in jobs if j and j.get('job_id'))

    sources = list(job_sets.keys())
    for i in range(len(sources)):
        for j in range(i + 1, len(sources)):
            s1, s2 = sources[i], sources[j]
            diff = job_sets[s1].symmetric_difference(job_sets[s2])
            if diff:
                diff_log.append({
                    'source_1': s1,
                    'source_2': s2,
                    'difference': list(diff),
                    'timestamp': time.time()
                })

def get_latest_jobs():
    return job_cache

def get_differences():
    return diff_log[-10:]
