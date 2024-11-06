import requests
from summarization.utils import read_file_text
import VAR
# import argparse

URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

def run(iam_token, folder_id, user_text):    
    prompt = {
    "modelUri": f"gpt://{folder_id}/yandexgpt-lite",
    "completionOptions": {
        "stream": False,
        "temperature": 0.3,
        "maxTokens": "2000"
    },
    "messages": [
            {
                "role": "system",
                "text": """Ты программа, которая должна обрабатывать входящие транскрипции видео и суммаризировать их, 
                    выбирая самые важные моменты. Ответ необходимо давать в формате `[<time start>s -> <time end>s]  <summarization text>`"""
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

def read_and_process_chunks(file_path, chunk_size):

    try:
        result = ""
        i = 0
        with open(file_path, 'r', encoding='utf-8') as file:
            while True:
                
                lines = [file.readline().rstrip('\n') for _ in range(chunk_size)]
                lines = list(filter(None, lines))
                if not lines:
                    break
                cur_result = run(VAR.key, VAR.folder,'\n'.join(lines))#['result']['alternatives'][0]['message']['text']
                print(cur_result)
                print(i)
                i +=1
                result += cur_result + '\n'
                
        return result
    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
# if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--iam_token", required=True, help="IAM token")
    # parser.add_argument("--folder_id", required=True, help="Folder id")
    # parser.add_argument("--user_text", required=True, help="User text")
    # args = parser.parse_args()
    
    # print(result)
    
    
