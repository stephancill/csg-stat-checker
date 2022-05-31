# CSGO Stat Checker
Checks the HLTV rating of all players in the server when you connect.

## Prerequisites
- Python 3
- Pipenv
- `-netconport 2121` launch option in CSGO

## Usage
Install dependencies
```
pipenv install
```
Run script
```
pipenv run python src/main.py
```

Once connected, it should show something like
```
Connected: "Slndy"
rating not found
('"Slndy"', 1111111111111111, 0)
Connected: "player 1"
('"player 1"', 1111111111111111, '1.32')
Connected: "GHOST"
('"GHOST"', 1111111111111111, '0.82')
Connected: "sTank"
('"sTank"', 1111111111111111, '0.99')
Connected: "Bloodshed"
('"Bloodshed"', 1111111111111111, '0.26')
```
