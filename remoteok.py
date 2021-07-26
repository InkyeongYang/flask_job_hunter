import requests
from bs4 import BeautifulSoup as bs


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
URL = "https://remoteok.io"

def extract_jobs(search_word):
    words = search_word.replace('%2B', '-plus').replace('%23', '-sharp')
    res = requests.get(f"{URL}/remote-{words}-jobs", headers=headers)
    soup = bs(res.text, "html.parser")
    table = soup.find("table")
    jobs = []
    if table:
        results = table.find_all("tr", {"class":"job"})
        for result in results:
            job = {}
            content = result.find("td", {"class":"company"})
            link = content.find("a", {"class": "preventLink"})
            if link:
                job['link'] = f"{URL}{link.attrs['href']}"
            title = content.find("h2", {"itemprop": "title"})
            if title:
                job['title'] = title.get_text(strip=True)
            company = content.find("h3", {"itemprop": "name"})
            if company:
                job['company'] = company.get_text(strip=True)
            location = content.find("div", {"class": "location"})
            if location:
                job['location'] = location.get_text(strip=True)
            jobs.append(job)
    return jobs
