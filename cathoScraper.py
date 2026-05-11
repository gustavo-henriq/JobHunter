import json
from datetime import datetime
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

profile_skills = []
base_url = "https://www.catho.com.br/vagas/estagio-na-area-de-desenvolvimento-de-software/sao-paulo-sp/"
current_time = datetime.now()

SAVE_RAW_JSON = False


def get_text(locator, default="N/A"):
    if locator.count() == 0:
        return default
    return locator.first.inner_text().strip()


def get_description_preview(page):
    description = get_text(
        page.locator(".detail_offer div.text-16:has-text('Sobre a vaga')")
    )
    return description.replace("Sobre a vaga", "", 1).strip() or "N/A"


def dismiss_cookie_banner(page):
    page.evaluate(
        """() => {
            document.querySelector("#lgpd-consent-widget")?.remove();
            document.querySelectorAll(".widget-overlay, .widget-container")
                .forEach((element) => element.remove());
        }"""
    )


def select_job_preview(page, job, title):
    dismiss_cookie_banner(page)
    job.scroll_into_view_if_needed()
    dismiss_cookie_banner(page)
    job.click(timeout=5000)
    page.wait_for_function(
        """(title) => {
            const heading = document.querySelector(".detail_offer h1");
            return heading && heading.innerText.trim() === title;
        }""",
        arg=title,
        timeout=5000,
    )


def get_catho():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path="/snap/bin/chromium",
            headless=True,
        )
        #creating a new browser context
        context = browser.new_context(
            viewport={
                "width": 1366,
                "height": 768
            },
            bypass_csp=True,
            locale="pt-BR",
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
            ),
            extra_http_headers={
                "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8"
            },
        )
        page = context.new_page()
        page.goto(base_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_selector("article.offer", timeout=15000)
        dismiss_cookie_banner(page)

        jobs_cards = page.locator("article.offer").all()
        jobs = []
        for job in jobs_cards:
            title = get_text(job.locator("h2.title_offer"))
            company = get_text(job.locator("span.text-12"))
            salary = get_text(job.locator("p:has(.i_salary)"))
            published = get_text(job.locator("span.tag"))
            url = job.locator("h2.title_offer a").get_attribute("href")
            select_job_preview(page, job, title)
            description = get_description_preview(page)

            jobs.append({
                "title": title,
                "company": company,
                "salary": salary,
                "description": description,
                "published": published,
                "url": urljoin(base_url, url),
                "source": "Catho",
                "scraped_at": current_time,
            })
        if SAVE_RAW_JSON:
            json_data = json.dumps(jobs, indent=4, ensure_ascii=False)
            
            with open("jobs.json", "w", encoding='utf-8') as f:
                f.write(json_data)
        
        browser.close()
        return jobs
