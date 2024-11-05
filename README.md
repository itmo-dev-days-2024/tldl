# TLDL

## Полезные команды ffmpeg'а

Посмотреть информацию о медиапотоках в файле
```shell
ffprobe [filename]
```

Вытащить часть аудио-дорожки из видео под vosk
```shell
ffmpeg -i in.mp4 -ss 00:26:05 -t 00:05:00.0 -map 0:a -ar 16000 -ac 1 out.wav
```