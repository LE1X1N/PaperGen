# Pagergen 论文主体生成服务
An automonous pipeline for generating thesis' body.


```
PaperGen-Paper-Service
├─ app.py                    # 入口文件
├─ conf
│  └─ service_config.yaml    # 配置文件
├─ README.md
├─ requirements.txt
└─ src
    ├─ config
    │  └─ __init__.py        # 配置初始化
    ├─ llm
    │  ├─ client.py          # LLM服务器连接
    │  ├─ prompt.py          # 提示词相关
    │  └─ __init__.py
    ├─ service
    │  ├─ doc
    │  │  ├─ composer.py     # 文档组装
    │  │  └─ styles.py       # 文档风格控制
    │  └─ gen_funcs.py       # 与文档内容生成有关函数
    └─ utils
        └─ common.py
```