import json
import os
import subprocess
import tempfile
from typing import Any

from fastapi import UploadFile

from app.core.exceptions import ConversionException, JSONException, TemplatingException


async def create_images_file(image_files: list[UploadFile]) -> tuple[str, list[str]]:
    """Create a JSON file with uploaded images metadata

    Args:
        image_files (list[UploadFile]): Images uploaded with the POST request.

    Returns:
        tuple[str, list[str]]: The name of temporary file created as a string and in a list.
    """
    image_file_dict: dict[str, dict[str, Any]] = {}
    tempfiles: list[str] = []
    for image_file in image_files:
        with tempfile.NamedTemporaryFile(delete=False) as temp_image_file:
            temp_image_file.write(await image_file.read())
        tempfiles.append(temp_image_file.name)
        if not image_file.filename:
            # Files without filenames will not be injected in the template
            continue
        image_file_dict[image_file.filename] = _get_image_file_data(
            temp_image_file.name
        )

    with tempfile.NamedTemporaryFile(delete=False) as images_file:
        images_file.write(json.dumps(image_file_dict).encode())
    tempfiles.append(images_file.name)

    return images_file.name, tempfiles


def create_data_file(json_data: str) -> tuple[str, list[str]]:
    """Write the content to be inserted in the template to a temporary JSON file.

    Args:
        json_data (str): Valid JSON content as a string.

    Raises:
        JSONException: Application specific exception if JSON is not valid.

    Returns:
        tuple[str, list[str]]: The name of temporary file created as a string and in a list.
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False) as data_file:
            data_file.write(json.dumps(json.loads(json_data)).encode())

        return data_file.name, [data_file.name]
    except Exception as e:
        raise JSONException(detail=str(e))


async def create_template_file(docx_file: UploadFile) -> tuple[str, list[str]]:
    with tempfile.NamedTemporaryFile(delete=False) as template_file:
        template_file.write(await docx_file.read())

    return template_file.name, [template_file.name]


def reserve_docx_result_file() -> tuple[str, list[str]]:
    result_file_docx = tempfile.NamedTemporaryFile(delete=False)

    return result_file_docx.name, [result_file_docx.name]


def _get_image_file_data(media_path: str) -> dict[str, Any]:
    """Create a dict of an image metadata

    Args:
        media_path (str): Path to the image.

    Returns:
        dict: A dict with width, height, file path and mime type
    """
    from PIL import Image

    width = height = 0
    format = ""

    try:
        with Image.open(media_path) as img:
            width, height = img.size
            format = img.format.lower()
    except:
        pass

    return {
        "width": width,
        "height": height,
        "source": media_path,
        "format": format,
    }


def to_pdf(docx_file: str) -> str:
    """Converts a docx file to pdf using LibreOffice

    Args:
        docx_file (str): Path to the input docx file.

    Raises:
        ConversionException: App specific exception if the conversion fails.

    Returns:
        str: Path to the output pdf file.
    """

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
        raise ConversionException(detail={"out": result.stdout, "err": result.stderr})

    return result_file_pdf_name_full


def to_docx(
    template_file_name: str,
    data_file_name: str,
    images_file_name: str,
    result_file_docx_name: str,
) -> None:
    """Create a docx document from a template and inputs using easy-template-x

    Args:
        template_file_name (str): Path to the docx template.
        data_file_name (str): Path to the JSON file containing tags.
        images_file_name (str): Path to the JSON file with images metadata.
        result_file_docx_name (str): Path to the docx output file.

    Raises:
        TemplatingException: Application specific exception if running easy-template-x fails.
    """

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
        raise TemplatingException(detail={"out": result.stdout, "err": result.stderr})
