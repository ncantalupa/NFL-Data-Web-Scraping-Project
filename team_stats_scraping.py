import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json

re_headers = {
    "User-Agent": "Chrome/58.0.3029.110"
}

years = [str(x) for x in range(2023,2024)]

team_stats_json = {}
for year in years:
    team_stats_json[year] = {}
    print(f"Scraping {year} stats...  ", end= '\r')
    url = f'https://www.pro-football-reference.com/years/{year}/index.htm'
    time.sleep(2)
    page = requests.get(url=url, headers=re_headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    afc_team_WL = soup.find('table', id="AFC").find('tbody').find_all('tr')
    nfc_team_WL = soup.find('table', id="NFC").find('tbody').find_all('tr')
    for i in range(15, -1, -5):
        afc_team_WL.pop(i)
        nfc_team_WL.pop(i)
    NFL_team_WL = afc_team_WL + nfc_team_WL
    for team in NFL_team_WL:
        team_name = str(team.find('th').text)
        team_name = team_name.replace("*", "")
        team_name = team_name.replace("+", "")
        team_stats_json[year][team_name] = {}
        stats = team.find_all('td')
        for i, stat in enumerate(stats):
            if i >= 7: break
            stat_name = stat.get('data-stat')
            stat_content = stat.text
            team_stats_json[year][team_name][stat_name] = stat_content

    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html)
    driver.quit()

    team_stats = soup.find('table', id="team_stats").find('tbody').find_all('tr')
    for row in team_stats:
        stats = row.find_all('td')
        team_name = str(stats[0].text)
        stats.pop(0)
        for stat in stats:
            stat_name = stat.get('data-stat')
            stat_content = stat.text
            team_stats_json[year][team_name][stat_name] = stat_content

    with open('team_stats.json', 'w') as out:
        json.dump(team_stats_json, out)
        
    
