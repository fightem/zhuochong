# -*- coding: utf-8 -*-
import requests
import pyaudio

def play_text_audio(character_name,text):
    # 流式传输音频的URL，你可以自由改成Post
    stream_url = f'http://127.0.0.1:5000/tts?cha_name={character_name}&text={text}&stream=true'

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

# 测试函数
if __name__ == "__main__":
    text = "こんにちは、私は刻琴と申します。"
    character_name = '刻琴'
    play_text_audio(character_name, text)
