
# FastDocx-API

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![typedlib_mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://www.mypy-lang.org)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![GitHub Actions Workflow Status](https://github.com/mbging/fastdocx-api/actions/workflows/docker-hub.yaml/badge.svg)
![GitHub Actions Workflow Status](https://github.com/mbging/fastdocx-api/actions/workflows/lint.yaml/badge.svg)


A FastAPI based project to generate DOCX and PDF documents from a DOCX template, JSON data and images.

The project uses `easy-template-x` to fill the DOCX template: all tags and filters provided by this project are available.

- [Example](#example)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Running Locally](#running-locally)
- [Swagger Documentation](#swagger-documentation)
- [Development Environment](#development-environment)
- [Testing](#testing)
- [Sample Commands](#sample-commands)
- [Docker](#docker)
- [References](#references)

### Example
!["LibreOffice to PDF"](/app/tests/sample_data/preview.png)

## System Requirements

Python 3, NodeJS and LibreOffice must be installed globally.

The Docker image will install all requirements when built.

## Installation

Create and activate a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

Install requirements
```
pip install -r requirements.txt
```

Then setup the Node package with
```
cd app/scripts/
npm install
```

## Running Locally

```
uvicorn app.main:app --reload
```

## Swagger Documentation

Install and run locally then visit http://localhost:8000/docs.

## Development Environment

For development and testing, install additional requirements
```
pip install -r requirements.dev.txt
```

## Testing

Install the development dependencies, then run `pytest` from the project root.

## Sample Commands

Use the sample files in `app/tests/sample_data`.

```
cd app/tests/sample_data

curl -X POST http://localhost:8000/api/v1/render/to_docx \
  -F 'json_data={"hello": "Bonjour", "world": "à tous"}' \
  -F 'docx_file=@./1_hello_world.docx' > result_1.docx

curl -X POST http://localhost:8000/api/v1/render/to_pdf \
  -F 'json_data={
    "sample_document_header": "FastDocxAPI sample document",
    "title": "FastDocxAPI - A Full Sample",
    "heading_1": "Style",
    "paragraph_1": "All Libreoffice features are available. Style is not modified by templating, and images can be included too!",
    "heading_2": "Lorem Ipsum",
    "paragraph_2": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    "table_first": [
        {
            "first_col": "Monday",
            "second_col": "Tuesday",
            "third_col": "Other..."
        },
        {
            "first_col": "Hello",
            "second_col": "World",
            "third_col": "Good Bye"
        },
        {
            "first_col": "Alice",
            "second_col": "Bob",
            "third_col": "Charlie"
        }
    ],
		"other_table": [
        {
            "value_1": "Something",
            "value_2": "to"
        },
        {
            "value_1": "test",
            "value_2": "here."
        }
    ],
		"simplelist": [
			{"item": "one"},
			{"item": "two"},
			{"item": "and more"}
		],
		"otherlist": [
			{"level_main": "Top", "sub_levels": [{"content": "a"}, {"content": "b"}]},
			{"level_main": "Not top", "sub_levels": [{"content": "fgh"}, {"content": "ijk"}]}
		]
}' \
  -F 'docx_file=@./2_all_features.docx' \
  -F 'image_files=@./image.jpg' \
  -F 'image_files=@./logo.png' > result_2.pdf
```

## Docker

Build the image: this can take several minutes to install LibreOffice and NodeJS.
```
docker build -t fastdocxapi
```

Run with `docker run -p 8000:80 fastdocxapi`.

The latest build can be found on [Docker Hub](https://hub.docker.com/repository/docker/mjbourgeon/fastdocx-api).

## References
1. [FastAPI official docs](https://fastapi.tiangolo.com/)
2. [easy-template-x repository](https://github.com/alonrbar/easy-template-x)
3. [LibreOffice website](https://www.libreoffice.org/)
