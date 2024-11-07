import requests
from summarization.keys import folder_ya_gpt, key_ya_gpt
# import argparse

URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"


prompts = [
    """Ты программа, которая должна сократить транскрипцию, которая подается на входе. 
    Выдели самые важные момента из этой записи и расскажи об этом в 2-3 предложениях. """,
    """Ты программа, котрая должна дать название текста, который поадается на вход. В ответе дай только название в формате `<name>`
    """
    
]
    
def run(iam_token, folder_id, user_text, prompt):    
    prompt = {
    "modelUri": f"gpt://{folder_id}/yandexgpt",
    "completionOptions": {
        "stream": False,
        "temperature": 0.3,
        "maxTokens": "2000"
    },
    "messages": [
            {
                "role": "system",
                "text": prompt
            },
            {
                "role": "user",
                "text": f"Входные данные: {user_text}"
            }
        ]
    }   
    # Ты сокращаешь общее число временных промежутков. Ответ даешь одной строчкой в формате `[<time start>s -> <time end>s]  <summarization text>`

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {iam_token}"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()

    return result['result']['alternatives'][0]['message']['text']

def read_file_and_process_chunks(file_path, chunk_size):

    try:
        result = []
        i = 0
        with open(file_path, 'r', encoding='utf-8') as file:
            while True:
                
                lines = [file.readline().rstrip('\n') for _ in range(chunk_size)]
                
                lines = list(filter(None, lines))
                
                time_start = int(lines[0].split("] ")[0].split(".")[0][1:])
                time_end = int(lines[0].split("] ")[0].split(" -> ")[1].split(".")[0])
                if not lines:
                    break
                cur_summ = run(key_ya_gpt, folder_ya_gpt,'\n'.join(lines), prompts[0])
                cur_name = run(key_ya_gpt, folder_ya_gpt,'\n'.join(lines), prompts[1])
                # print(cur_result)
                # print(i)
                i +=1
                result.append([cur_name, cur_summ, time_start, time_end])
                print(f"start: {time_start} end: {time_end}\nName: {cur_name}\nSummary: {cur_summ}\n")
                
        return result
    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        
        
def process_batch(batch):
    time_start = int(batch[0].split("] ")[0].split(".")[0])
    time_end = int(batch[-1].split("] ")[0].split(" -> ")[1].split(".")[0])
    cur_summ = run(key_ya_gpt, folder_ya_gpt,'\n'.join(batch), prompts[0])
    cur_name = run(key_ya_gpt, folder_ya_gpt,'\n'.join(batch), prompts[1])
    print(f"start: {time_start} end: {time_end}\nName: {cur_name}\nSummary: {cur_summ}\n")
    return [cur_name, cur_summ, time_start, time_end]
    
        
def process_text(text, size):
    # def run(batch):
        # print(f"Processing batch with {len(batch)} lines")

    lines = text.split('[')
    result = []

    batch = []
    if(len(lines) <= size*2):
        size = len(lines)/3

    for line in lines:
        if line.strip(): 
            batch.append(line)
        
        if len(batch) == size:
            result.append(process_batch(batch=batch))
            # run(batch)
            batch = []

    if batch:
        result.append(process_batch(batch=batch))
        # run(batch)
        
    return result




    
    
