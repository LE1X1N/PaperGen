⚠️🚧 This repo is under HEAVY development. 🚧⚠️

```
PaperGen
├─ .devcontainer
│  └─ devcontainer.json
├─ docker
│  ├─ .env
│  └─ docker-compose.yml
├─ README.md
└─ services
   ├─ figure_service
   │  ├─ conf
   │  │  └─ service_config.yaml
   │  ├─ Dockerfile
   │  ├─ docs
   │  │  ├─ 接口文档.md
   │  │  ├─ 测试输入JSON
   │  │  │  ├─ app
   │  │  │  │  ├─ 基于Android+XAMPP+MySQL的家校互动平台设计与实现.json
   │  │  │  │  ├─ 基于Android农产品商城交易设计与实现.json
   │  │  │  │  ├─ 基于Android的学生教师考勤签到请假系统.json
   │  │  │  │  ├─ 基于Android的考试系统设计与实现.json
   │  │  │  │  └─ 基于Android的背单词系统设计与实现.json
   │  │  │  ├─ web
   │  │  │  │  └─ 基于springboot的小区物业管理系统设计与实现.json
   │  │  │  └─ wechat
   │  │  │     ├─ 基于node+vue+uniapp的心理咨询预约小程序.json
   │  │  │     ├─ 基于springboot+uniapp的图书馆座位预约小程序.json
   │  │  │     ├─ 基于uniapp的学生宿舍管理小程序.json
   │  │  │     ├─ 基于uniapp的药品商城外卖小程序.json
   │  │  │     └─ 基于协同过滤算法的电影推荐小程序.json
   │  │  └─ 测试返回.json
   │  ├─ README.md
   │  ├─ requirements.txt
   │  ├─ src
   │  │  ├─ api
   │  │  │  ├─ routes.py
   │  │  │  ├─ validator
   │  │  │  │  └─ json_validator.py
   │  │  │  └─ __init__.py
   │  │  ├─ app.py
   │  │  ├─ config
   │  │  │  ├─ loader.py
   │  │  │  └─ __init__.py
   │  │  ├─ domain
   │  │  │  ├─ pipeline.py
   │  │  │  └─ services
   │  │  │     ├─ data_parser.py
   │  │  │     ├─ prompt_builder.py
   │  │  │     ├─ tmpl_parser.py
   │  │  │     └─ __init__.py
   │  │  ├─ errors.py
   │  │  ├─ infrastructure
   │  │  │  ├─ browser
   │  │  │  │  ├─ manager.py
   │  │  │  │  └─ __init__.py
   │  │  │  ├─ db
   │  │  │  │  ├─ client.py
   │  │  │  │  └─ __init__.py
   │  │  │  ├─ llm
   │  │  │  │  ├─ client.py
   │  │  │  │  └─ __init__.py
   │  │  │  ├─ renderer
   │  │  │  │  ├─ gradio_renderer.py
   │  │  │  │  └─ __init__.py
   │  │  │  └─ storage
   │  │  │     ├─ local_storage.py
   │  │  │     ├─ minio_storage.py
   │  │  │     └─ __init__.py
   │  │  ├─ repository
   │  │  │  ├─ progress_repository.py
   │  │  │  ├─ storage_factory.py
   │  │  │  └─ storage_repository.py
   │  │  └─ utils
   │  │     ├─ common.py
   │  │     ├─ image_utils.py
   │  │     ├─ logger.py
   │  │     └─ __init__.py
   │  ├─ templates
   │  │  ├─ app
   │  │  │  └─ 模板1.jsx
   │  │  ├─ web
   │  │  │  ├─ 上中下布局
   │  │  │  │  ├─ 模板1.jsx
   │  │  │  │  ├─ 模板10.jsx
   │  │  │  │  ├─ 模板2.jsx
   │  │  │  │  ├─ 模板3.jsx
   │  │  │  │  ├─ 模板4.jsx
   │  │  │  │  ├─ 模板5.jsx
   │  │  │  │  ├─ 模板6.jsx
   │  │  │  │  └─ 模板8.jsx
   │  │  │  ├─ 侧边布局
   │  │  │  │  ├─ 模板1.jsx
   │  │  │  │  ├─ 模板2.jsx
   │  │  │  │  ├─ 模板3.jsx
   │  │  │  │  ├─ 模板4.jsx
   │  │  │  │  ├─ 模板5.jsx
   │  │  │  │  ├─ 模板6.jsx
   │  │  │  │  └─ 模板8.jsx
   │  │  │  └─ 顶部-侧边布局
   │  │  │     ├─ 模板1.jsx
   │  │  │     ├─ 模板2.jsx
   │  │  │     ├─ 模板3.jsx
   │  │  │     ├─ 模板4.jsx
   │  │  │     ├─ 模板5.jsx
   │  │  │     ├─ 模板6.jsx
   │  │  │     ├─ 模板7.jsx
   │  │  │     └─ 模板8.jsx
   │  │  └─ wechat
   │  │     └─ 模板1.jsx
   │  ├─ uwsgi_service.ini
   │  └─ wsgi.py
   └─ paper_service
      ├─ app.py
      ├─ conf
      │  └─ service_config.yaml
      ├─ README.md
      ├─ requirements.txt
      └─ src
         ├─ config
         │  └─ __init__.py
         ├─ llm
         │  ├─ client.py
         │  ├─ prompt.py
         │  └─ __init__.py
         ├─ service
         │  ├─ content
         │  │  ├─ json_generator.py
         │  │  ├─ section_generator.py
         │  │  └─ __init__.py
         │  └─ doc
         │     ├─ composer.py
         │     ├─ style_controller.py
         │     └─ __init__.py
         └─ utils
            └─ common.py

```