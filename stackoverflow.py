import requests
from bs4 import BeautifulSoup as bs


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
URL = "https://stackoverflow.com"

def extract_pages(url):
    max_page = ""
    res = requests.get(url, headers=headers)
    soup = bs(res.text, 'html.parser')
    pagination = soup.find("div", {"class": "s-pagination"})
    if pagination:
        max_page = pagination.find_all("span")[-2].get_text()
    return int(max_page)

def extract_job(html):
    job = {}
    main = html.find("h2", {"class":"mb4"}).find("a")
    detail = html.find("h3", {"class":"mb4"}).find_all("span")
    if main and detail:
        job = {
            "link": f"{URL}{main.attrs['href']}",
            "title": main.attrs['title'],
            "company": detail[0].get_text(strip=True),
            "location": detail[1].get_text(strip=True)
        }
    return job

def extract_jobs(search_word):
    jobs = []
    max_page = extract_pages(f"{URL}/jobs?q={search_word}")
    if max_page:
        for page in range(1, max_page+1):
            dstn = f"{URL}/jobs?q={search_word}&pg={page}"
            res = requests.get(dstn, headers=headers)
            soup = bs(res.text, 'html.parser')
            results = soup.find_all("div", {"class": "-job"})
            for result in results:
                job = extract_job(result)
                if job:
                    jobs.append(job)
    return jobs
