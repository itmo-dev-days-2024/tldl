from langchain.chains.summarize import load_summarize_chain
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chat_models.gigachat import GigaChat
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models.gigachat import GigaChat
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.gigachat import GigaChatEmbeddings

# from ml.summarization import get_summarization
from langchain.text_splitter import RecursiveCharacterTextSplitter
credentials = 'ZmQ1ZTQyN2YtODJmNy00YzE0LWIzMTAtMzk4NmY5MDQ3MGQzOmJjNTRjZGI5LWRhZWQtNGMzMS04MTFjLTYzM2NjNTVjOTFlOQ=='
# from PyPDF2 import PdfFileReader
llm = GigaChat(credentials=credentials, verify_ssl_certs=False, scope="GIGACHAT_API_PERS")
embeddings = GigaChatEmbeddings(credentials=credentials, verify_ssl_certs=False, scope="GIGACHAT_API_PERS")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=50,
)
settings_init =  {"llm": llm, "embeddings": embeddings, "text_splitter": text_splitter}



llm = GigaChat(credentials=credentials, verify_ssl_certs=False, scope="GIGACHAT_API_PERS")


# def parse_pdf_text_to_txt(pdf_filename, txt_filename):
#     extracted_text = ""
    
#     # Открытие PDF-файла для чтения
#     with open(pdf_filename, "rb") as pdf_file:
#         pdf_reader = PdfFileReader(pdf_file)
        
#         # Извлечение текста из каждой страницы
#         for page_num in range(pdf_reader.numPages):
#             page = pdf_reader.getPage(page_num)
#             page_text = page.extractText()
#             extracted_text += page_text
    
#     # Запись извлеченного текста в файл txt
#     with open(txt_filename, "w", encoding="utf-8") as txt_file:
#         txt_file.write(extracted_text)


def get_summarization(filename: str, llm: GigaChat):

    # Пример использования функции
    # parse_pdf_text_to_txt(filename, "extracted_text.txt")

    loader = TextLoader("extracted_text.txt", encoding="utf-8")
    doc = loader.load()

    split_docs = RecursiveCharacterTextSplitter(chunk_size=8000, chunk_overlap=1500).split_documents(
        doc
    )

    map_prompt = PromptTemplate(
    template="Оставить только 5 самых важных с указанием секунды, когда они были произнесены. Входные данные:\n{text} ",
    input_variables=["text"]
    )

    chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=map_prompt)
    res = chain.run(split_docs)

    return {'text': res}

print(get_summarization("", settings_init["llm"])["text"])

