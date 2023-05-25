#
import sys
import os
import nickNameCrawling
import uploadToBigquery
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import asyncio

sys.path.append("/root/git/study/fifaOnlineAbusing/fifaOnlineAbusing/")
sys.path.append('/git/study/fifaOnlineAbusing/fifaOnlineAbusing/')
load_dotenv(verbose=True)

user_id = '@goldenbooma'
client = WebClient(token=os.environ['SLACK_TOKEN'])
async def main():
    try:
        message = 'fifaOnlinedataUpload is Loading...'
        response = client.chat_postMessage(channel=user_id, text=message)

        apiData = await nickNameCrawling.get_api_data()
        uploadToBigquery.upload(apiData)

        message = 'uploadToBigquery Complete'
        response = client.chat_postMessage(channel=user_id, text=message)

    except Exception as e:
        response = client.chat_postMessage(channel=user_id, text=f"fifaOnline errorMessage : {e}")

if __name__ == "__main__":
    asyncio.run(main())