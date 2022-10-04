from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from requests import get
from bs4 import BeautifulSoup


def get_page_count(keyword):
    results = []
    base_url = "https://kr.indeed.com/jobs?q="

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)
    browser.get(f"{base_url}{keyword}")

    response = browser.page_source

    soup = BeautifulSoup(response, "html.parser")
    pagination = soup.find("ul", class_="pagination-list")
    if pagination == None:
        return 1
    pages = pagination.find_all("li", recursive=False)
    count = len(pages)
    if count >= 5:
        return 5
    else:
        return count


def extract_indeed_jobs(keyword):
    print("Start [indeed.com] Scrapping...")
    results = []
    pages = get_page_count(keyword)
    print("Found", pages, "pages.")
    for page in range(pages):
        print("Page", page+1, "scrapping...")
        base_url = "https://kr.indeed.com/jobs"
        final_url = f"{base_url}?q={keyword}&start={page*10}"
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        browser = webdriver.Chrome(options=options)
        browser.get(final_url)

        response = browser.page_source

        soup = BeautifulSoup(response, "html.parser")
        job_list = soup.find("ul", class_="jobsearch-ResultsList")
        jobs = job_list.find_all("li", recursive=False)
        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                link = anchor['href']
                title = anchor['aria-label']
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")

                job_data = {
                    "link": f"https://kr.indeed.com{link}",
                    "company": company.string,
                    "location": location.string,
                    "position": title
                }
                for data in job_data:
                    if job_data[data] != None:
                        job_data[data] = job_data[data].replace(",", " ")
                results.append(job_data)
    print("Indeed scrapping finished.")
    return results
