import requests
from bs4 import BeautifulSoup
import time
import json

re_headers = {
    "User-Agent": "Chrome/58.0.3029.110"
}

stat_categories = ['passing', 'rushing', 'receiving']
years = [str(x) for x in range(2002,2023)]

player_stats_json = {}
total_player_count = 0
for year in years:
    player_stats_json[year] = {'passing': [], 'rushing': [], 'receiving': []}
    for stat_category in stat_categories:
        print(f"Scraping {year} {stat_category} stats...  ", end= '\r')
        url = f'https://www.pro-football-reference.com/years/{year}/{stat_category}.htm'
        time.sleep(3)
        page = requests.get(url=url, headers=re_headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        rows = soup.find('tbody').find_all('tr')
        for row in rows:
            stats = row.find_all('td')
            stat_obj = {}
            for stat in stats:
                stat_name = stat.get('data-stat')
                stat_content = stat.text
                if stat_name == 'player' and (("*" in stat_content) or ('+' in stat_content)):
                    stat_content = str(stat_content).replace("*","")
                    stat_content = str(stat_content).replace("+","")
                stat_obj[stat_name] = stat_content
            if len(stat_obj) > 0:
                player_stats_json[year][stat_category].append(stat_obj)
                total_player_count += 1

    with open('player_stats.json', 'w') as out_json:
        json.dump(player_stats_json, out_json)
print(f"Data collected for {total_player_count} players.")
