import requests
import json
with open('config.json','r', encoding = 'utf-8') as file:
    config = json.load(file)
api_key = config['data']['API_KEY']
HEADERS = {"Authorization" : api_key}
seasonId = requests.get('https://static.api.nexon.co.kr/fifaonline4/latest/seasonid.json', headers = HEADERS).json()
spid = requests.get("https://static.api.nexon.co.kr/fifaonline4/latest/spid.json", headers = HEADERS).json()