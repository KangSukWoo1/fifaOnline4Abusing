#
import sys
import os
import nickNameCrawling
import firstUploadToBigquery
import bigqueryUpsert
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import asyncio 

sys.path.append("/home/ubuntu/Study/fifaOnline4Abusing")
load_dotenv(verbose=True)

user_id = '@goldenbooma'
client = WebClient(token=os.environ['SLACK_TOKEN'])
async def main():
    try:
        message = 'fifaOnlinedataUpload is Loading...'
        response = client.chat_postMessage(channel=user_id, text=message)

        apiData = await nickNameCrawling.get_api_data()
        bigqueryUpsert.upload(apiData)
        bigqueryUpsert.merge()
#         firstUploadToBigquery.upload(apiData) <- 첫 번째 업로드라면 bigqueryUpsert를 제거하고 해당 행을 실행시키면 된다!

        message = 'uploadToBigquery Complete'
        response = client.chat_postMessage(channel=user_id, text=message)

    except Exception as e:
        response = client.chat_postMessage(channel=user_id, text=f"fifaOnline errorMessage : {e}")

if __name__ == "__main__":
    asyncio.run(main())