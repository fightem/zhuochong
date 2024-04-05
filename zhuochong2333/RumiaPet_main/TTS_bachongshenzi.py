# -*- coding: utf-8 -*-
import requests
import pyaudio
import pyttsx3


def tts_and_play(text):
    # engine = pyttsx3.init()
    # engine.say(text)
    # engine.runAndWait()

    from VoiceSettingUI import  get_latest_pet_sound
    character_name = get_latest_pet_sound()
    print(f'当前声音{character_name}')
    # 流式传输音频的URL，你可以自由改成Post
    stream_url = f'  http://127.0.0.1:5000/tts?cha_name={character_name}&text={text}&stream=true'

    # 初始化pyaudio
    p = pyaudio.PyAudio()

    # 打开音频流
    stream = p.open(format=p.get_format_from_width(2),
                    channels=1,
                    rate=32000,
                    output=True)

    # 使用requests获取音频流，你可以自由改成Post
    response = requests.get(stream_url, stream=True)

    # 读取数据块并播放
    for data in response.iter_content(chunk_size=1024):
        stream.write(data)

    # 停止和关闭流
    stream.stop_stream()
    stream.close()

    # 终止pyaudio
    p.terminate()

if __name__ == '__main__':
    tts_and_play('您好，我叫做八重身子')