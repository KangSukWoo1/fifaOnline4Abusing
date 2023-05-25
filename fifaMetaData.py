import requests
import os
import sys
from dotenv import load_dotenv
sys.path.append("/home/ubuntu/Study/fifaOnline4Abusing")
load_dotenv(verbose=True)
api_key = os.environ['API_KEY']
HEADERS = {"Authorization" : api_key}
seasonId = requests.get('https://static.api.nexon.co.kr/fifaonline4/latest/seasonid.json', headers = HEADERS).json()
spid = requests.get("https://static.api.nexon.co.kr/fifaonline4/latest/spid.json", headers = HEADERS).json()