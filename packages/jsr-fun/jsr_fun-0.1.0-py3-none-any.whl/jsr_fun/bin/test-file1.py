from logging import info
from pathlib import Path

from loguru import logger
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
import time


def main():
    file = '/home/jiang/ml/speech/郭德纲/封神之作.mp3'
    file = "/home/jiang/py/asr/assets/audio/德云社_02m.mp3"

    model_dir = "iic/SenseVoiceSmall"
    # model_dir = "paraformer-zh"

    model = AutoModel(
        model=model_dir,
        trust_remote_code=True,
        # remote_code="./model.py", # 加载失败
        vad_model="fsmn-vad",  # 与spk_model不能同时使用
        vad_kwargs={
            "max_single_segment_time": 30000,
            "max_silence_duration": 0.2 # 好像没效果
        },
        merge_vad=True,
        merge_length_s=15,
        # spk_model="cam++",
        device="cuda:0",
    )

    logger.info(f"model: {model.model_path}")

    # file = Path(model.model_path, "example/asr_example.wav")

    # en
    for i in range(1):
        start_time = time.time()
        res = model.generate(
            # input=f"{model.model_path}/example/zh.mp3",
            input=str(file),
            cache={},
            language="auto",  # "zn", "en", "yue", "ja", "ko", "nospeech"
            #use_itn=True,
            batch_size_s=60,
            # merge_vad=True,  #
            # merge_length_s=15,
        )
        print("res:", type(res))

        print("res:", res)

        text = rich_transcription_postprocess(res[0]["text"])
        print(text)
        print(f"{model.model_path}/example/en.mp3")
        print(f"Transcribe: {time.time() - start_time} s")


if __name__ == '__main__':
    main()
