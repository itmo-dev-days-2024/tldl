from summarization import utils
import summarization.ya_gpt.programm as ya_gpt
import summarization.giga_chat.programm as gigachat
from summarization.utils import read_file_text, write_text_to_file
import VAR

res = ya_gpt.process_text(utils.read_file_text("extracted_text.txt"), 220)
# res = gigachat.get_summarization("extracted_text.txt")
# print(res)



# write_text_to_file("result.txt", res)