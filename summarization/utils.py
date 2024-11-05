def read_file_text(file_path):

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        return "Файл не найден."
    except Exception as e:
        return f"Произошла ошибка при чтении файла: {e}"
    
    
def write_text_to_file(file_path, text):

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print("Текст успешно записан в файл.")
    except Exception as e:
        print(f"Произошла ошибка при записи в файл: {e}")