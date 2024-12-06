from funasr.runtime.python import FunASR
import librosa

def convert_to_srt(results, sample_rate):
    srt_content = ""
    start_time = 0.0
    for idx, res in enumerate(results):
        text = res['text']
        end_time = start_time + len(res['audio']) / sample_rate
        start_time_str = format_time(start_time)
        end_time_str = format_time(end_time)
        srt_content += f"{idx + 1}\n{start_time_str} --> {end_time_str}\n{text}\n\n"
        start_time = end_time
    return srt_content

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def main():

    model_dir = "iic/SenseVoiceSmall"

    # 初始化模型
    model_path = "path/to/funasr/model"  # 替换为你的模型路径
    asr = FunASR(model_path)

    # 加载音频文件
    audio_file = "example.mp3"
    audio, sr = librosa.load(audio_file, sr=None)

    # 进行语音识别
    result = asr(audio)

    # 转换为 SRT 格式的字幕
    srt_content = convert_to_srt(result, sr)

    # 保存为 SRT 文件
    with open("output.srt", "w", encoding="utf-8") as f:
        f.write(srt_content)

if __name__ == '__main__':
    main()