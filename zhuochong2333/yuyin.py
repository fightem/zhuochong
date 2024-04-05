import edge_tts
import asyncio
import os
from playsound import playsound
import tempfile

def text_to_speech_and_play(msg):
    """
    将输入的文本转换为语音，并播放生成的临时语音文件。
    """
    # 设置语音模型和其他参数
    voice = 'zh-CN-YunjianNeural'
    rate = '+0%'
    volume = '+0%'

    async def my_function(text):
        # 使用临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmpfile:
            output_file = tmpfile.name
            # 创建文本到语音对象，并保存为 MP3 文件
            tts = edge_tts.Communicate(text=text, voice=voice, rate=rate, volume=volume)
            await tts.save(output_file)
            return output_file

    async def speak_async(text):
        # 调用异步函数生成语音文件并获取文件路径
        output_file = await my_function(text)
        # 播放生成的语音文件
        playsound(output_file)
        # 删除临时文件
        os.remove(output_file)

    # 异步执行生成语音文件的过程
    asyncio.run(speak_async(msg))

# 测试
