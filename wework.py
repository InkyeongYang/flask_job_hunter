import requests
from bs4 import BeautifulSoup as bs


URL = "https://weworkremotely.com"

def extract_jobs(search_word):
    jobs = []
    res = requests.get(f"{URL}/remote-jobs/search?term={search_word}&button=")
    soup = bs(res.text, 'html.parser')
    container = soup.find("div", id="job_list")
    exist_check = container.find("div", {"class": "no_results"})
    if not exist_check:
        results = container.find_all("li")
        for result in results:
            if "view-all" in result['class']:
                continue
            else:
                item = result.find_all("a")[-1]
                link = item.attrs['href']
                title = item.find("span", {"class": "title"})
                company = item.find("span")
                loc = item.find("span", {"class": "region"})
                if title and link and company and loc:
                    job = {
                        "link": f"{URL}{link}",
                        "title": title.get_text(strip=True),
                        "company": company.get_text(strip=True),
                        "location": loc.get_text(strip=True)
                    }
                    jobs.append(job)
    return jobs