from telnet_client import CSGOTelnetClient
import requests

def steamid_to_commid(steamid):
  sid_split = steamid.split(':')
  commid = int(sid_split[2]) * 2
  
  if sid_split[1] == '1':
      commid += 1
  
  commid += 76561197960265728
  return commid

if __name__ == "__main__":
    telnet_client = CSGOTelnetClient()
    telnet_client.connect()

    r = telnet_client.run("status")
    raw = r.split("# userid name uniqueid connected ping loss state rate")[1].split("#end")[0]
    player_lines = [x.strip() for x in raw.split("\n")[:-1] if "#" in x and x.split(" ")[::-1][2] != 'BOT']
    print(player_lines)

    steam_ids = [x.split(" ")[::-1][5] for x in player_lines]
    steam64_ids = [steamid_to_commid(x) for x in steam_ids]
    names = [x[x.index('"'):len(x)-x[::-1].index('"')] for x in player_lines]

    for i in range(len(names)):
        csgostats_url = f"https://csgostats.gg/player/{steam64_ids[i]}"
        print(names[i], csgostats_url)
    
    