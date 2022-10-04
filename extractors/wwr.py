from requests import get
from bs4 import BeautifulSoup


def extract_wwr_jobs(keyword):
    print("Start [weworkremotely.com] Scrapping...")
    base_url = "https://weworkremotely.com/remote-jobs/search&term="

    response = get(f"{base_url}{keyword}")

    if response.status_code != 200:
        print("Can't request website!")
    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("section", class_="jobs")
        for job_section in jobs:
            job_posts = job_section.find_all("li")
            job_posts.pop(-1)
            for post in job_posts:
                anchors = post.find_all("a")
                anchor = anchors[1]
                link = anchor["href"]
                job_info = anchor.find_all("span", class_="company")
                company = job_info[0].string
                if len(job_info) == 2:
                    location = "No information"
                elif len(job_info) == 3:
                    location = job_info[2].string
                else:
                    pass
                title = anchor.find("span", class_="title").string
                job_data = {
                    "link": f"https://weworkremotely.com{link}",
                    "company": company,
                    "location": location,
                    "position": title
                }
                for data in job_data:
                    if job_data[data] != None:
                        job_data[data] = job_data[data].replace(",", " ")
                results.append(job_data)
        print("Wwr scrapping finished.")
        return results
