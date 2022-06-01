from telnet_client import CSGOTelnetClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chromium.options import ChromiumOptions
import time

ranks = {
    0: "none",
    1:"S1",     2:"S2",     3:"S3",     4:"S4",     5:"SE",     6:"SEM",    # Silver
    7:"GN1",    8:"GN2",    9:"GN3",    10:"GNM",                           # Gold Nova
    11:"MG1",   12:"MG2",   13:"MGE",   14:"DMG",                           # Master Guardian       
    15:"LE",    16:"LEM",                                                   # Legendary Eagle            
    17:"SMFC",                                                              # Supreme
    18:"GE"                                                                 # Global 
}

def steamid_to_commid(steamid):
    sid_split = steamid.split(':')
    commid = int(sid_split[2]) * 2

    if sid_split[1] == '1':
        commid += 1

    commid += 76561197960265728
    return commid

def get_player(id, name, driver):
    # TODO: Get player info
    rating = 0
    rank = 0
    wins = 0
    csgostats_url = f"https://csgostats.gg/player/{id}"
    driver.get(csgostats_url)
    print(csgostats_url)
    try:
        rating_el = driver.find_element(by=By.ID, value="rating")
        rating_span = rating_el.find_element(by=By.TAG_NAME, value="span")
        rating = rating_span.text 
        rank_el = driver.find_element(by=By.CLASS_NAME, value="player-ranks")
        
        rank_img = rank_el.find_element(by=By.TAG_NAME, value="img")
        rank = rank_img.get_attribute("src").split("/")[-1].split(".png")[0]

        wins_el = driver.find_element(by=By.ID, value="competitve-wins")        
        wins_span = wins_el.find_element(by=By.TAG_NAME, value="span")
        
        wins = wins_span.text
    except:
        print("rating not found")
            
    player = (name, id, rating, ranks[int(rank)], wins, csgostats_url)

    return player

def main():
    
    telnet_client = CSGOTelnetClient()
    telnet_client.connect()
    
    options = ChromiumOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)    


    players = []

    while len(players) < 10:
        r = telnet_client.run("status")
        raw = r.split("# userid name uniqueid connected ping loss state rate")[1].split("#end")[0]
        player_lines = [x.strip() for x in raw.split("\n")[:-1] if "#" in x and x.split(" ")[::-1][2] != 'BOT' and x]
        player_lines = [x for x in player_lines if x]

        steam_ids = [x.replace("  ", " ").split(" ")[::-1][5] for x in player_lines]        
        steam64_ids = [steamid_to_commid(x) for x in steam_ids]
        names = [x[x.index('"'):len(x)-x[::-1].index('"')] for x in player_lines]

        current_player_ids = [x[1] for x in players]
        for i, steam_id64 in enumerate(steam64_ids):
            if not steam_id64 in current_player_ids:
                print("Connected:", names[i])
                        
                player = get_player(steam_id64, names[i], driver)
                
                print(player)
                players.append(player)
                time.sleep(1)
        # print("waiting", f"{len(players)}/10")
        time.sleep(1)

    for player in players:
        print(player)

if __name__ == "__main__":
    main()
    # options = ChromiumOptions()
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)    

    # print(get_player(76561198049532825, "", driver))
    
    
    
    
    