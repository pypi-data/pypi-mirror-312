from funasr import AutoModel


def vad_main():
    model = AutoModel(model="fsmn-vad", max_silence_duration=0.2)

    file = f"{model.model_path}/example/vad_example.wav"
    file = "/home/jiang/py/asr/assets/audio/德云社_02m.mp3"
    res = model.generate(input=file)
    print(res)


# 注：VAD模型输出格式为：[[beg1, end1], [beg2, end2], .., [begN, endN]]，
# 其中begN/endN表示第N个有效音频片段的起始点/结束点， 单位为毫秒。


def fa_main():
    model = AutoModel(model="fa-zh")

    file = "/home/jiang/py/asr/assets/audio/德云社_02m.mp3"
    wav_file = f"{model.model_path}/example/asr_example.wav"
    text_file = f"{model.model_path}/example/text.txt"
    print("text_file:", text_file)
    print("wav_file:", wav_file)
    res = model.generate(input=(wav_file, text_file), data_type=("sound", "text"))
    print(res)


if __name__ == '__main__':
    vad_main()
