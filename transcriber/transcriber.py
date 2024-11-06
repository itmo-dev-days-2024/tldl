from faster_whisper import WhisperModel
model_size = "large-v3"

model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe("cpp_lecture.mp4", language="ru", beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

out_file = open('CPP_transcribe.txt', 'w')
for segment in segments:
    line = "[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text)
    print(line)
    out_file.write(line + '\n')