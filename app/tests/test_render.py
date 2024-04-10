import json
import os

import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient

from app.main import app
from app.services.render import create_images_file

client = TestClient(app)


@pytest.mark.asyncio
async def test_images_json():
    filename = ""
    tempfiles = []

    image_files = [
        UploadFile(open("./app/tests/sample_data/logo.png", "rb"), filename="logo.png"),
        UploadFile(
            open("./app/tests/sample_data/image.jpg", "rb"), filename="image.jpg"
        ),
    ]

    try:
        filename, tempfiles = await create_images_file(image_files)

        content = json.loads(open(filename, "r").read())
        assert "logo.png" in content
        assert "image.jpg" in content
        assert content["logo.png"]["width"] == 57
        assert content["image.jpg"]["height"] == 313
        assert "source" in content["logo.png"]
        assert content["logo.png"]["format"] == "png"

        assert len(tempfiles) == 3
    finally:
        if os.path.exists(filename):
            os.remove(filename)


def test_query_json_invalid():
    response = client.post(
        "/api/v1/render/to_pdf",
        files={
            "docx_file": (
                "sample.docx",
                open("./app/tests/sample_data/1_hello_world.docx", "rb").read(),
            ),
            "image_files": (
                "logo.png",
                open("./app/tests/sample_data/logo.png", "rb").read(),
            ),
            "image_files": (
                "image.jpg",
                open("./app/tests/sample_data/image.jpg", "rb").read(),
            ),
        },
        data={"json_data": '{"sample": "value", []}'},
    )

    assert response.status_code == 400
    assert "detail" in json.loads(response.text)


def test_query_pdf_valid():
    response = client.post(
        "/api/v1/render/to_pdf",
        files={
            "docx_file": (
                "sample.docx",
                open("./app/tests/sample_data/1_hello_world.docx", "rb").read(),
            ),
        },
        data={"json_data": '{"hello": "Bonjour", "world": "à tous"}'},
    )

    assert response.status_code == 200
    assert response.content[:4] == b"%PDF"
    assert len(response.content) > 10000


def test_query_docx_valid():
    response = client.post(
        "/api/v1/render/to_docx",
        files={
            "docx_file": (
                "sample.docx",
                open("./app/tests/sample_data/1_hello_world.docx", "rb").read(),
            ),
        },
        data={"json_data": '{"hello": "Bonjour", "world": "à tous"}'},
    )

    assert response.status_code == 200
    assert response.content[:4] == b"PK\x03\x04"
    assert len(response.content) > 4000
