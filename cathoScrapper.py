import json
from datetime import datetime

from playwright.sync_api import sync_playwright

profile_skills = []
base_url = "https://www.catho.com.br/vagas/ti/?lastDays=30"
current_time = datetime.now()

SAVE_RAW_JSON = False


def get_catho():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        #creating a new browser context
        context = browser.new_context(
            viewport={
                "width": 800,
                "height": 600
            },
            bypass_csp=True
        )
        page = context.new_page()
        page.goto(base_url)

        jobs_cards = page.locator('.search-result-custom_jobItem__OGz3a').all()
        jobs = []
        for job in jobs_cards:
            
            title = job.locator('h2').inner_text()
            company_el = job.locator('p').first
            company = company_el.evaluate("el => el.firstChild.textContent.trim()")
            salary = job.locator('.custom-styled_salaryText__oSvPo').inner_text() if job.locator('.custom-styled_salaryText__oSvPo').count() > 0 else 'N/A'
            description = job.locator('.job-description').inner_text() if job.locator('.job-description').count() > 0 else 'N/A'
            published = job.locator('.custom-styled_cardJobTime__ZvAIb').inner_text() if job.locator('.custom-styled_cardJobTime__ZvAIb').count() > 0 else 'N/A'
            url = job.locator('h2 a').get_attribute('href')
            jobs.append({
                "title": title,
                "company": company,
                "salary": salary,
                "description": description,
                "published": published,
                "url": url,
                "source": "Catho",
                "scraped_at": current_time,
            })
        if SAVE_RAW_JSON:
            json_data = json.dumps(jobs, indent=4, ensure_ascii=False)
            
            with open("jobs.json", "w", encoding='utf-8') as f:
                f.write(json_data)
        
        browser.close()
        return jobs
