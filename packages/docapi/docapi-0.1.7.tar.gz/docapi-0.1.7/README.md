![image](assets/logo.png)

![Python Version](https://img.shields.io/badge/python-3.8+-aff.svg)
![OS](https://img.shields.io/badge/os-linux%20|%20macOS-blue)
![Lisence](https://img.shields.io/badge/license-Apache%202-dfd.svg)
[![PyPI](https://img.shields.io/pypi/v/docapi)](https://pypi.org/project/docapi/)
[![GitHub pull request](https://img.shields.io/badge/PRs-welcome-blue)](https://github.com/Shulin-Zhang/docapi/pulls)

\[ English | [中文](README_zh.md) \]

DocAPI is a Python package that uses LLM to automatically generate API documentation.

## Features

- The Flask framework supports automatic scanning of the routing structure of API services;

- Supports a variety of mainstream commercial and open source models at home and abroad;

- Supports automatic document generation and partial document update;

- Support API documentation in multiple languages ​​(requires large model support);

- Supports web page deployment to display API documentation.

## Changelog

- [2024-11-17] Support Zhipu AI, Baidu Qianfan model, optimize document structure, and add javascript code examples; Remove the execution mode that uses the configuration file.

- [2024-11-20] Support custom document templates.

- [2024-11-24] Support multi-threaded acceleration requests.

- [2024-11-26] Support .env to load environment variables and multi-language documents.

## Installation

```bash
pip install -U docapi
```

or

```bash
pip install -U docapi -i https://pypi.org/simple
```

#### GitHub source code installation

```bash
pip install git+https://github.com/Shulin-Zhang/docapi
```

## Usage

**Automatically scan the routing structure. This is only valid for flask projects and must be used in the environment of api projects.**

**OpenAI:**
```bash
export OPENAI_API_KEY=api_key

export OPENAI_API_MODEL=gpt-4o-mini

# Generate documents
docapi generate server.py --lang en

# Update documents
docapi update server.py --lang en

# Start web service
docapi serve
```

**Azure OpenAI:**
```bash
export AZURE_OPENAI_API_KEY=api_key

export AZURE_OPENAI_ENDPOINT=endpoint

export OPENAI_API_VERSION=version

export AZURE_OPENAI_MODEL=gpt-4o-mini

# 生成文档
docapi generate server.py --template <template_path>

# 更新文档
docapi update server.py --template <template_path>

# 启动web服务
docapi serve docs --ip 0.0.0.0 --port 9000
```

**Qianwen, Open source deployment:**
```bash
export OPENAI_API_KEY=api_key

export OPENAI_API_BASE=api_base_url

export OPENAI_API_MODEL=model_name

# Generate documents
docapi generate server.py --lang en --workers 6

# Update documents
docapi update server.py --lang en --workers 6

# Start web service
docapi serve
```

**Baidu Qianfan:**
```bash
export QIANFAN_ACCESS_KEY=access_key

export QIANFAN_SECRET_KEY=secret_key

export QIANFAN_MODEL=ERNIE-3.5-8K

# Generate documents
docapi generate server.py --lang en

# Update documents
docapi update server.py --lang en

# Start web service
docapi serve
```

**ZhipuAI:**
```bash
export ZHIPUAI_API_KEY=api_key

export ZHIPUAI_MODEL=glm-4-flash

# Generate documents
docapi generate server.py

# Update documents
docapi update server.py

# Start web service
docapi serve
```

**.env environment variable file:**

```.env
# .env
OPENAI_API_KEY='xxx'
OPENAI_API_BASE='xxx'
OPENAI_API_MODEL='xxx'
```

```bash
# Generate documents
docapi generate server.py --env .env
```

## Code calls
```python
import os
from docapi import DocAPI

os.environ['OPENAI_API_KEY'] = "api_key"
os.environ['OPENAI_API_BASE'] = "api_base"
os.environ['OPENAI_API_MODEL'] = "model_name"

docapi = DocAPI.build(lang="en")

docapi.generate("flask_project/flask_server.py", "docs")

# docapi.update("flask_project/flask_server.py", "docs")

# docapi.serve("docs", ip="127.0.0.1", port=8080)
```

## Supported Models

- OpenAI

- AzureOpenAI

- Tongyi Qianwen

- Zhipu AI

- Baidu Qianfan

- Open source model

## Supported API Frameworks

- Flask
  
Automatic scanning is only valid for the Flask framework and is recommended for use on Flask services.

## API Web Page

![image](assets/example1.png)

## TODO

- ~~Supports large models such as Wenxin Yiyan and Zhipu AI.~~

- ~~Supports online web page display of documents.~~

- ~~Supports custom document templates.~~

- ~~Multithreading accelerates requests.~~

- Supports automatic scanning of frameworks such as Django.

- Import to postman.

- Support Windows operating system.
