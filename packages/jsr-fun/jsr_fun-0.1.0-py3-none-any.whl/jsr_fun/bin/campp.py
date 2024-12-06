from funasr import AutoModel

def main():

    file = "https://isv-data.oss-cn-hangzhou.aliyuncs.com/ics/MaaS/ASR/test_audio/asr_example_zh.wav"
    #file = "/home/jiang/py/asr/assets/audio/德云社_02m.mp3"

    model = AutoModel(model="iic/speech_campplus_sv_zh-cn_16k-common")

    res = model.generate(
        input=file
    )
    print(res)
    print("len:", len(res[0]["spk_embedding"][0]))


if __name__ == '__main__':
    main()