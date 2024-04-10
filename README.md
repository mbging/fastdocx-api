
# FastDocx-API

## Description

A FastAPI based project to generate DOCX and PDF documents from a DOCX template, JSON data and images.

## Prerequisites

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

## Running local

```
uvicorn app.main:app --reload
```

## Swagger documentation

Install and run locally then visit http://localhost:8000/docs.

## Development environment

For development and testing, install additional requirements
```
pip install -r requirements.dev.txt
```

## Testing

Install the development dependencies, then run `pytest` from the project root.

## Docker

Build the image: this can take several minutes to install LibreOffice and NodeJS.
```
docker build -t fastdocxapi
```

Run with `docker run -p 8000:80 fastdocxapi`.

## References
1. [FastAPI official docs](https://fastapi.tiangolo.com/)
2. [easy-template-x repository](https://github.com/alonrbar/easy-template-x)
3. [LibreOffice website](https://www.libreoffice.org/)
