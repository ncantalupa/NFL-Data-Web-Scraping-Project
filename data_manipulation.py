import json
import pandas as pd

def team_json_to_csv():
    with open('team_stats_2003_2023.json', 'r') as f:
        team_json = json.load(f)

    rows = []
    for year in team_json:
        for team in team_json[year]:
            for stat in team_json[year][team]:
                if "." in team_json[year][team][stat]:
                    team_json[year][team][stat] = float(team_json[year][team][stat])
                else:
                    team_json[year][team][stat] = int(team_json[year][team][stat])

    for year in team_json:
        for team in team_json[year]:
            row_dict = {"year": int(year), "team": team}
            row_dict.update(team_json[year][team])
            rows.append(row_dict)


    team_df = pd.DataFrame(rows)
    team_df.to_csv('team_stats_2003_2023.csv', index=False)
    print(team_df.head())

def player_json_to_csv():
    with open("player_stats.json", 'r') as f:
        players_json = json.load(f)
    passing_rows = []
    rushing_rows = []
    receiving_rows = []
    for year in players_json:
        for category in players_json[year]:
            for player in players_json[year][category]:
                for stat in player:
                    try: 
                        if "." in player[stat]:
                            player[stat] = float(player[stat])
                        else:
                            player[stat] = int(player[stat])
                    except:
                        pass
                player["year"] = int(year)
                if category == "passing":
                    passing_rows.append(player)
                elif category == "rushing":
                    rushing_rows.append(player)
                elif category == "receiving":
                    receiving_rows.append(player)
    
    players_passing_df = pd.DataFrame(passing_rows)
    players_passing_df.to_csv("passing_stats.csv", index=False)
    players_rushing_df = pd.DataFrame(rushing_rows)
    players_rushing_df.to_csv("rushing_stats.csv", index=False)
    players_receiving_df = pd.DataFrame(receiving_rows)
    players_receiving_df.to_csv("receiving_stats.csv", index=False)

def main():
    team_json_to_csv()
    pass

main()