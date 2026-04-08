# hw04 文本生成-声音克隆-语音识别闭环实现
本目录包含大模型文稿生成、剪映声音克隆、开源ASR调研与实现全链路作业文件，按任务分模块组织，所有代码可复现。

## 目录结构
├── text_gen.md          # 任务一：大模型生成文稿（含标题、正文、模型/Prompt说明）
├── jianying.md          # 任务二：剪映声音克隆（步骤、产出、文件说明）
├── asr_report.md        # 任务三：ASR方案对比、选型理由
├── asr_code/            # 任务三：ASR可复现代码（含requirements.txt、运行脚本）
│   ├── main.py
│   ├── requirements.txt
│   └── run.sh           # 快速运行脚本
├── experiment_log.md    # 任务三：ASR实验记录（环境、测试结果、错误率等）
├── audio/               # 音频文件目录（剪映配音、测试音频、识别源音频）
│   ├── clone_voice.mp3  # 剪映声音克隆配音音频（任务一生成文稿）
│   └── test_mic.wav     # 麦克风实时录制测试音频
└── README.md            # 本总览文件