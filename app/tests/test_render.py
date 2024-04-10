import os

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.render import create_images_file

client = TestClient(app)


@pytest.mark.asyncio
async def test_images_json():
    import json

    from fastapi import UploadFile

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
