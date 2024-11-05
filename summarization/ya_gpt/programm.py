import requests
from summarization.utils import read_file_text
# import argparse

URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

def run(iam_token, folder_id, user_text):    
    prompt = {
    "modelUri": f"gpt://{folder_id}/yandexgpt-lite",
    "completionOptions": {
        "stream": False,
        "temperature": 0.6,
        "maxTokens": "2000"
    },
    "messages": [
            {
                "role": "system",
                "text": "Ты программа, которая должна обрабатывать входящие транскрипции видео и суммаризировать их, выбирая самые важные моменты. Ответ необходимо отправлять в том же формате с указанием временных меток."
            },
            {
                "role": "user",
                "text": f"Предоствавь суммаризацию этой транскрипции: {user_text}"
            }
        ]
    }   


    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {iam_token}"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()

    return result['result']['alternatives'][0]['message']['text']


# if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--iam_token", required=True, help="IAM token")
    # parser.add_argument("--folder_id", required=True, help="Folder id")
    # parser.add_argument("--user_text", required=True, help="User text")
    # args = parser.parse_args()
    
    # print(result)
    
    
