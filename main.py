from cathoScraper import get_catho
from database import insert_many_silver
from ai_scoring import score_silver_jobs_from_db, get_client

print("Scraping jobs from Catho...")
jobs = get_catho()
print(f"✓ Scraped {len(jobs)} jobs\n")

print("Inserting to Silver collection...")
insert_many_silver(jobs)
print("✓ Inserted to database\n")

print("Scoring jobs with AI...")
client = get_client()
scored_jobs = score_silver_jobs_from_db("entry_ai_web", client, limit=10)
print(f"✓ Scored {len(scored_jobs)} jobs\n")

print("=" * 60)
for job in scored_jobs:
    if job.get('score') > 0:
        message = f"Ótima oportunidade para quem está buscando {job.get('opportunity_type')}, na área de {job.get('area')} como foco em {job.get('focus')}, utilizando {', '.join(job.get('tools', []))}"
        print(f"{job.get('title')}\n{message}\nLink: {job.get('url')}\n")


