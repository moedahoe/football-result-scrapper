import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        return {
            "Home_team" : obj.Home.Team,
            "Away_team" : obj.Away.Team,
            "Home_stats": {
                "Goals" : obj.Home.Goals,
                "Possession" : obj.Home.Posession,
                "Goal_Attempts": obj.Home.Goal_Attempts,
                "Shots_on_Goal": obj.Home.Shots_on_Goal,
                "Shots_off_Goal": obj.Home.Shots_off_Goal,
                "free_kicks": obj.Home.free_kicks,
                "Corners": obj.Home.Corners,
                "Offsides": obj.Home.Offsides,
                "GK_saves": obj.Home.GK_saves,
                "Fouls": obj.Home.Fouls,
                "Red_cards": obj.Home.Red_cards,
                "Yellow_cards": obj.Home.Yellow_cards,
                "Passes": obj.Home.Passes,
                "Attacks": obj.Home.Attacks,
                "Dangerous_attacks": obj.Home.Dangerous_attacks
            },
            "Away_stats": {
                "Goals" : obj.Away.Goals,
                "Possession" : obj.Away.Posession,
                "Goal_Attempts": obj.Away.Goal_Attempts,
                "Shots_on_Goal": obj.Away.Shots_on_Goal,
                "Shots_off_Goal": obj.Away.Shots_off_Goal,
                "free_kicks": obj.Away.free_kicks,
                "Corners": obj.Away.Corners,
                "Offsides": obj.Away.Offsides,
                "GK_saves": obj.Away.GK_saves,
                "Fouls": obj.Away.Fouls,
                "Red_cards": obj.Away.Red_cards,
                "Yellow_cards": obj.Away.Yellow_cards,
                "Passes": obj.Away.Passes,
                "Attacks": obj.Away.Attacks,
                "Dangerous_attacks": obj.Away.Dangerous_attacks
            }
        }
class Stats:
    def __init__(self):
        self.Team = str("")
        self.Goals = int(0)
        self.Posession = float(0)
        self.Goal_Attempts = int(0)
        self.Shots_on_Goal = int(0)
        self.Shots_off_Goal = int(0)
        self.free_kicks = int(0)
        self.Corners = int(0)
        self.Offsides = int(0)
        self.GK_saves = int(0)
        self.Fouls = int(0)
        self.Red_cards = int(0)
        self.Yellow_cards = int(0)
        self.Passes = int(0)
        self.Attacks = int(0)
        self.Dangerous_attacks = int(0)
class Match:
    def __init__(self,Home,Away):
        self.Home = Home
        self.Away = Away


opt = webdriver.ChromeOptions()
# opt.add_argument("--headless")
driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),  chrome_options=opt)
driver.get("https://www.flashresultats.fr/")
links = list()
matches = driver.find_elements_by_class_name("event__match")
for m in matches:
    matchid = m.get_attribute("id")[4:]
    links.append("https://www.flashresultats.fr/match/"+ matchid + "/#tete-a-tete;overall")

for i in range(len(links)):
    driver.get(links[i])
    time.sleep(2)
    ts = driver.find_elements_by_class_name("highlight")
    matches = list()
    for t in ts:
        matches.append("https://www.flashresultats.fr/match/"+ t.get_attribute("onclick")[84:92] + "/#statistiques-du-match;0")
    Data = list()
    for match in matches:
        print(match)
        time.sleep(5)
        driver.get(match)
        stats = driver.find_element_by_id("tab-statistics-0-statistic")
        rows = stats.find_elements_by_class_name("statRow")
        homeStats = Stats()
        awayStats = Stats()
        homeStats.Team = driver.find_elements_by_class_name("participant-imglink")[1].get_attribute("innerHTML")
        awayStats.Team = driver.find_elements_by_class_name("participant-imglink")[3].get_attribute("innerHTML")
        homeStats.Goals = driver.find_elements_by_class_name("scoreboard")[0].get_attribute("innerHTML")
        awayStats.Goals = driver.find_elements_by_class_name("scoreboard")[1].get_attribute("innerHTML")
        for row in rows:
            title = row.find_element_by_class_name("statText--titleValue").get_attribute("innerHTML")
            if (title == "Possession de balle"):
                homeStats.Posession = row.find_element_by_class_name("statText--homeValue").get_attribute("innerHTML")[0:2]
                awayStats.Posession = row.find_element_by_class_name("statText--awayValue").get_attribute("innerHTML")[0:2]
            elif(title == "Tirs au but"):
                homeStats.Goal_Attempts = row.find_element_by_class_name("statText--homeValue").get_attribute("innerHTML")
                awayStats.Goal_Attempts = row.find_element_by_class_name("statText--awayValue").get_attribute("innerHTML")
            elif(title == "Tirs cadrés"):
                homeStats.Shots_on_Goal = row.find_element_by_class_name("statText--homeValue").get_attribute("innerHTML")
                awayStats.Shots_on_Goal = row.find_element_by_class_name("statText--awayValue").get_attribute("innerHTML")
            elif(title == "Tirs non cadrés"):
                homeStats.Shots_off_Goal = row.find_element_by_class_name("statText--homeValue").get_attribute("innerHTML")
                awayStats.Shots_off_Goal = row.find_element_by_class_name("statText--awayValue").get_attribute("innerHTML")
            elif(title == "Coup francs"):
                homeStats.free_kicks = row.find_element_by_class_name("statText--homeValue").get_attribute("innerHTML")
                awayStats.free_kicks = row.find_element_by_class_name("statText--awayValue").get_attribute("innerHTML")
            elif(title == "Corners"):
                homeStats.Corners = row.find_element_by_class_name("statText--homeValue").get_attribute("innerHTML")
                awayStats.Corners = row.find_element_by_class_name("statText--awayValue").get_attribute("innerHTML")
            elif(title == "Hors-jeu"):
                homeStats.Offsides = row.find_element_by_class_name("statText--homeValue").get_attribute("innerHTML")
                awayStats.Offsides = row.find_element_by_class_name("statText--awayValue").get_attribute("innerHTML")
            elif(title == "Sauvetages du gardien"):
                homeStats.GK_saves = row.find_element_by_class_name("statText--homeValue").get_attribute("innerHTML")
                awayStats.GK_saves = row.find_element_by_class_name("statText--awayValue").get_attribute("innerHTML")
            elif(title == "Fautes"):
                homeStats.Fouls = row.find_element_by_class_name("statText--homeValue").get_attribute("innerHTML")
                awayStats.Fouls = row.find_element_by_class_name("statText--awayValue").get_attribute("innerHTML")
            elif(title == "Cartons Rouges"):
                homeStats.Red_cards = row.find_element_by_class_name("statText--homeValue").get_attribute("innerHTML")
                awayStats.Red_cards = row.find_element_by_class_name("statText--awayValue").get_attribute("innerHTML")
            elif(title == "Cartons Jaunes"):
                homeStats.Yellow_cards = row.find_element_by_class_name("statText--homeValue").get_attribute("innerHTML")
                awayStats.Yellow_cards = row.find_element_by_class_name("statText--awayValue").get_attribute("innerHTML")
            elif(title == "Passes"):
                homeStats.Passes = row.find_element_by_class_name("statText--homeValue").get_attribute("innerHTML")
                awayStats.Passes = row.find_element_by_class_name("statText--awayValue").get_attribute("innerHTML")
            elif(title == "Attaques"):
                homeStats.Attacks = row.find_element_by_class_name("statText--homeValue").get_attribute("innerHTML")
                awayStats.Attacks = row.find_element_by_class_name("statText--awayValue").get_attribute("innerHTML")
            elif(title == "Attaques dangereuses"):
                homeStats.Dangerous_attacks = row.find_element_by_class_name("statText--homeValue").get_attribute("innerHTML")
                awayStats.Dangerous_attacks = row.find_element_by_class_name("statText--awayValue").get_attribute("innerHTML")
        Data.append(Match(homeStats,awayStats))
    with open("/Users/moerradi/Desktop/football results api/data"+ i +".json",'w+',encoding='utf8') as file:
        json.dump([ob for ob in Data] ,file,indent=4,ensure_ascii=False,cls=MyEncoder)
