import sys
import sherpa_onnx
import pyaudio
import numpy as np

# 配置Vosk Sherpa-ONNX中文模型（自动下载轻量版，无需手动下载）
config = sherpa_onnx.OfflineRecognizerConfig.from_transducer(
    encoder=sherpa_onnx.OfflineModelConfig(
        model="sherpa-onnx-zipformer-mandarin-small-2024-09-16/encoder.onnx",
        num_threads=4,
    ),
    decoder=sherpa_onnx.OfflineModelConfig(
        model="sherpa-onnx-zipformer-mandarin-small-2024-09-16/decoder.onnx",
        num_threads=4,
    ),
    joiner=sherpa_onnx.OfflineModelConfig(
        model="sherpa-onnx-zipformer-mandarin-small-2024-09-16/joiner.onnx",
        num_threads=4,
    ),
    tokens="sherpa-onnx-zipformer-mandarin-small-2024-09-16/tokens.txt",
)
recognizer = sherpa_onnx.OfflineRecognizer(config)

# 音频文件识别函数（支持mp3/wav，适配任务二clone_voice.mp3）
def recognize_audio(file_path):
    print(f"开始识别音频文件：{file_path}")
    result = recognizer.decode_file(file_path)
    print(f"音频识别结果：{result.text}")
    return result.text

# 麦克风实时流式识别函数（采样率16000，单声道，16bit）
def recognize_mic():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("麦克风实时识别已启动，开始说话（按Ctrl+C停止）...")

    # 流式识别配置
    streaming_config = sherpa_onnx.StreamingRecognizerConfig.from_transducer(
        encoder=sherpa_onnx.StreamingModelConfig(
            model="sherpa-onnx-zipformer-mandarin-small-2024-09-16/encoder-epoch-99-avg-1.onnx",
            num_threads=4,
        ),
        decoder=sherpa_onnx.OfflineModelConfig(
            model="sherpa-onnx-zipformer-mandarin-small-2024-09-16/decoder.onnx",
            num_threads=4,
        ),
        joiner=sherpa_onnx.OfflineModelConfig(
            model="sherpa-onnx-zipformer-mandarin-small-2024-09-16/joiner.onnx",
            num_threads=4,
        ),
        tokens="sherpa-onnx-zipformer-mandarin-small-2024-09-16/tokens.txt",
        sample_rate=RATE,
        feature_dim=80,
    )
    streaming_recognizer = sherpa_onnx.StreamingRecognizer(streaming_config)
    streamer = streaming_recognizer.create_stream()

    try:
        while True:
            data = stream.read(CHUNK)
            samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            streamer.accept_waveform(RATE, samples)
            streaming_recognizer.decode_stream(streamer)
            result = streamer.result()
            if result.is_final:
                print(f"实时识别结果（最终）：{result.text}")
                streamer.reset()
            else:
                print(f"实时识别结果（中间）：{result.text}", end="\r")
    except KeyboardInterrupt:
        print("\n麦克风识别已停止")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

# 主函数：运行时传参选择模式，1=音频文件识别，2=麦克风实时识别
if __name__ == "__main__":
    if len(sys.argv) != 3 and sys.argv[1] == "1":
        print("使用方法：")
        print("1. 音频文件识别：python main.py 1 音频文件路径（如../audio/clone_voice.mp3）")
        print("2. 麦克风实时识别：python main.py 2")
        sys.exit(1)
    if sys.argv[1] == "1":
        recognize_audio(sys.argv[2])
    elif sys.argv[1] == "2":
        recognize_mic()
    else:
        print("参数错误，1=音频文件识别，2=麦克风实时识别")
        sys.exit(1)