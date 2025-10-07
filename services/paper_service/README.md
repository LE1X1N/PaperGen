# Pagergen 论文主体生成服务
An automonous pipeline for generating thesis' body.


```
PaperGen-Paper-Service
├─ app.py                        # 入口文件
├─ conf
│  └─ service_config.yaml        # 配置文件
├─ README.md  
├─ requirements.txt
└─ src
    ├─ config
    │  └─ __init__.py            # 配置初始化
    ├─ llm
    │  ├─ client.py              # LLM服务器连接
    │  ├─ prompt.py              # 提示词相关
    │  └─ __init__.py
    ├─ service
    │  ├─ content
    │  │  ├─ json_generator.py    # 文档相关JSON生成，如目录JSON，需求图片JSON等
    │  │  ├─ section_generator.py # 主内容生成
    │  │  └─ __init__.py
    │  └─ doc
    │     ├─ composer.py          # 文档组装
    │     ├─ style_controller.py  # 文档样式控制
    │     └─ __init__.py
    └─ utils
        └─ common.py
```