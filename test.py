import summarization.ya_gpt.programm as summ
from summarization.utils import read_file_text, write_text_to_file
import VAR

res = summ.run(VAR.key, VAR.folder, read_file_text("extracted_text.txt"))#args.iam_token, args.folder_id, args.user_text)
print(res)



write_text_to_file("result.txt", res)