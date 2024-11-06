import summarization.ya_gpt.programm as summ
from summarization.utils import read_file_text, write_text_to_file
import VAR

res = summ.read_and_process_chunks("extracted_text.txt", 220)
print(res)



write_text_to_file("result.txt", res)