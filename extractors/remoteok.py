import requests
from bs4 import BeautifulSoup


def extract_remoteok_jobs(keyword):
    print("Start [remoteok.com] Scrapping")
    BASE_URL = "https://remoteok.com"
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"
    }
    request = requests.get(f"{BASE_URL}/remote-{keyword}-jobs",
                           headers=headers)
    if request.status_code != 200:
        print("Can't request website!")

    else:
        results = []
        soup = BeautifulSoup(request.text, "html.parser")
        trs = soup.find_all("tr", {"class": "job"})

        print("Start Scrapping...")

        for tr in trs:
            title = tr.find("h2").string
            company = tr.find("h3").string
            job_info = tr.find("div", {"class": "location"}).string
            job_link = tr.find("a", {"itemprop": "url"})["href"]

            job_data = {
                "link": f"{BASE_URL}{job_link}".replace("\n", ""),
                "company": company.replace("\n", ""),
                "location": job_info.replace("\n", ""),
                "position": title.replace("\n", ""),
            }
            for data in job_data:
                if job_data[data] != None:
                    job_data[data] = job_data[data].replace(",", " ")
            results.append(job_data)
        print("Remoteok scrapping Finished.")
        return results
