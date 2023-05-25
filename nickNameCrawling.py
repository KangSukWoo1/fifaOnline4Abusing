#!/usr/bin/env python
# coding: utf-8
import os
import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
import concurrent.futures
import requests
import time
import aiohttp 
import asyncio
from dotenv import load_dotenv
load_dotenv(verbose=True)


load_dotenv(verbose=True)
headers = {
    "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    "Authorization" : os.environ['API_KEY']
}
async def get_ranker_ids(session, page):
    url = f"https://fifaonline4.nexon.com/datacenter/rank?n4pageno={page}"
    async with session.get(url) as response:
        soup = BeautifulSoup(await response.text(), 'html.parser')
        span_elements = soup.find_all('span', class_='name profile_pointer')
        ranker_ids = [span.string for span in span_elements]
        return ranker_ids

async def get_nickname(session, rankerid):
    url = f'https://api.nexon.co.kr/fifaonline4/v1.0/users?nickname={rankerid}'
    async with session.get(url, headers = headers) as response:
        ranker_info = await response.json()
        return ranker_info

async def get_market_data(session, accessId):
    buy_url = f"https://api.nexon.co.kr/fifaonline4/v1.0/users/{accessId}/markets?tradetype=buy&offset=0&limit=100"
    sell_url = f"https://api.nexon.co.kr/fifaonline4/v1.0/users/{accessId}/markets?tradetype=sell&offset=0&limit=100"
    
    async with session.get(buy_url, headers=headers) as buy_response:
        buy_data = await buy_response.json()
    
    async with session.get(sell_url, headers=headers) as sell_response:
        sell_data = await sell_response.json()

    return {'accessId': accessId, 'buy': buy_data, 'sell': sell_data}

async def get_api_data():
    ranker_ids = []
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [get_ranker_ids(session, page) for page in range(1, 500)]
        results = await asyncio.gather(*tasks)
        for ranker_ids_page in results:
            ranker_ids.extend(ranker_ids_page)

        nicknames = []
        tasks = [get_nickname(session, rankerid) for rankerid in ranker_ids]
        nickname_values = pd.read_json('rankerInfo.json')['nickname'].values
        coroutines = [get_nickname(session, nickname) for nickname in nickname_values]
        tasks.extend([asyncio.ensure_future(coroutine) for coroutine in coroutines])
        results = await asyncio.gather(*tasks)
        nicknames.extend(results)

        access_ids = [nickname.get('accessId') for nickname in nicknames]
        
        buy_data = []
        tasks = [get_market_data(session, access_id) for access_id in access_ids]
        results = await asyncio.gather(*tasks)
        buy_data.extend(results)
    buy_data_decomposition = []
    for one_data in buy_data:
        try : 
            if one_data['accessId'] is None : 
                continue
            access_id = one_data['accessId']
            for b in one_data['buy']:
                buy_data_decomposition.append({'accessId': access_id, **b, 'type': 'buy'})
            for s in one_data['sell']:
                buy_data_decomposition.append({'accessId': access_id, **s, 'type': 'sell'})
        except TypeError:
            continue
    api_data = pd.DataFrame(buy_data_decomposition)

    return api_data

async def main():
    api_data = await get_api_data()

if __name__ == "__main__":
    asyncio.run(main())