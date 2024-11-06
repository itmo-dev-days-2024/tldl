from faster_whisper import WhisperModel

def transcribe(source_filename) -> str:

    model_size = "large-v3"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(source_filename, language="ru", beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    str_list = []

    result = ''
    # out_file = open('CPP_transcribe.txt', 'w')
    for segment in segments:
        line = "[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text)
        str_list.append(line)

        # print(line)
        # out_file.write(line + '\n')
    for line_elem in str_list:
        result.join(line_elem)
    
    return result