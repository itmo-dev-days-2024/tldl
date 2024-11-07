

from tldl.logic.base import Chapter, TranscribeToken, AbstractHandler, TldlContext
import requests
from tldl.settings import settings


#GigaChain libs

from langchain.chains.summarize import load_summarize_chain
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chat_models.gigachat import GigaChat
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models.gigachat import GigaChat
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from summarization.keys import key_gigachat
# from ml.summarization import get_summarization
from langchain.text_splitter import RecursiveCharacterTextSplitter


#utils
#----------------------------------------------------------------------------------------------------------------------------
def read_file_text(file_path):

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        return "Файл не найден."
    except Exception as e:
        return f"Произошла ошибка при чтении файла: {e}"
    
    
#YaGPT
#----------------------------------------------------------------------------------------------------------------------------

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

def process_batch(batch):
    
    time_start = int(batch[0].split("] ")[0].split(".")[0])
    time_end = int(batch[-1].split("] ")[0].split(" -> ")[1].split(".")[0])
    cur_summ = run(settings.key_ya_gpt, settings.folder_ya_gpt,'\n'.join(batch), prompts[0])
    cur_name = run(settings.key_ya_gpt, settings.folder_ya_gpt,'\n'.join(batch), prompts[1])
    print(f"start: {time_start} end: {time_end}\nName: {cur_name}\nSummary: {cur_summ}\n")
    return [cur_name, cur_summ, time_start, time_end]
    
        
def process_text(text, size):
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



#GigaChain
#----------------------------------------------------------------------------------------------------------------------------

credentials = key_gigachat
# from PyPDF2 import PdfFileReader
llm = GigaChat(credentials=credentials, verify_ssl_certs=False, scope="GIGACHAT_API_PERS")
embeddings = GigaChatEmbeddings(credentials=credentials, verify_ssl_certs=False, scope="GIGACHAT_API_PERS")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=50,
)
settings_init =  {"llm": llm, "embeddings": embeddings, "text_splitter": text_splitter}
llm = GigaChat(credentials=credentials, verify_ssl_certs=False, scope="GIGACHAT_API_PERS")

def get_summarization(filename: str):
    llm = settings_init["llm"]

    # Пример использования функции
    # parse_pdf_text_to_txt(filename, "extracted_text.txt")

    loader = TextLoader(filename, encoding="utf-8")
    doc = loader.load()

    split_docs = RecursiveCharacterTextSplitter(chunk_size=8000, chunk_overlap=1500).split_documents(
        doc
    )

    map_prompt = PromptTemplate(
    template="Вкраце расскажи о том, что обсуждалось на лекции. Входные данные:\n{text} ",
    input_variables=["text"]
    )

    chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=map_prompt)
    res = chain.run(split_docs)

    return res




class SummarizerHandler(AbstractHandler):

    def handle(self, context: TldlContext) -> TldlContext:
        # here context gets populated for Chapters
        transcript_file = open('transcript_tmp.txt','w+')
        for chunk in context.transcribed_text:
            transcript_file.write(str(chunk))
        transcript_file.seek(0)
        context.summary = get_summarization(transcript_file.name)
        all_file_content = read_file_text(transcript_file.name)
        charpers_from_yagpt = process_text(all_file_content, 220)
        context.chapters = [
            Chapter(ch[0], ch[1], ch[2], ch[3]) for ch in charpers_from_yagpt
        ]
        # print(context.summary)
        # print(context.chapters)
        return super().handle(context)