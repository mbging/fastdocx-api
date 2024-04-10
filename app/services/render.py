import json
import os
import subprocess
import tempfile

from fastapi import UploadFile

from app.core.exceptions import ConversionException, TemplatingException


async def create_images_file(image_files: list[UploadFile]) -> tuple[str, list[str]]:
    image_file_dict: dict[str, str] = {}
    tempfiles: list[str] = []
    for image_file in image_files:
        with tempfile.NamedTemporaryFile(delete=False) as temp_image_file:
            temp_image_file.write(await image_file.read())
            tempfiles.append(temp_image_file.name)
            image_file_dict[image_file.filename] = _get_image_file_data(
                temp_image_file.name
            )

    with tempfile.NamedTemporaryFile(delete=False) as images_file:
        images_file.write(json.dumps(image_file_dict).encode())
        tempfiles.append(images_file.name)

    return images_file.name, tempfiles


def create_data_file(json_data: str) -> tuple[str, list[str]]:
    with tempfile.NamedTemporaryFile(delete=False) as data_file:
        data_file.write(json.dumps(json.loads(json_data)).encode())

    return data_file.name, [data_file.name]


async def create_template_file(docx_file: UploadFile) -> tuple[str, list[str]]:
    with tempfile.NamedTemporaryFile(delete=False) as template_file:
        template_file.write(await docx_file.read())

    return template_file.name, [template_file.name]


def reserve_docx_result_file() -> tuple[str, list[str]]:
    with tempfile.NamedTemporaryFile(delete=False) as result_file_docx:
        result_filename = result_file_docx.name

    return result_file_docx.name, [result_file_docx.name]


def _get_image_file_data(media_path: str) -> dict:
    from PIL import Image

    width = height = 0
    format = ""

    try:
        with Image.open(media_path) as img:
            width, height = img.size
        format = media_path.split(".")[-1].lower()
    except:
        pass

    return {
        "width": width,
        "height": height,
        "source": media_path,
        "format": format,
    }


def to_pdf(docx_file: str) -> str:
    result_file_pdf_name = os.path.splitext(os.path.basename(docx_file))[0] + ".pdf"
    result_file_pdf_name_full = os.path.join(
        os.path.dirname(docx_file),
        result_file_pdf_name,
    )

    result = subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            docx_file,
            "--outdir",
            os.path.dirname(docx_file),
        ]
    )

    if result.stdout or result.stderr:
        raise ConversionException(detail=result)

    return result_file_pdf_name_full


def to_docx(
    template_file_name: str,
    data_file_name: str,
    images_file_name: str,
    result_file_docx_name: str,
) -> None:
    result = subprocess.run(
        [
            "node",
            "app/scripts/render_docx.js",
            template_file_name,
            data_file_name,
            images_file_name,
            result_file_docx_name,
        ],
        capture_output=True,
    )

    if len(result.stdout):
        raise TemplatingException(detail=result)
