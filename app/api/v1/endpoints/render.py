import os

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

import app.services.render as render_service

router = APIRouter(
    prefix="/render",
    tags=["render"],
)


@router.get("/")
async def root():
    return "Render is running"


def cleanup(files):
    for filename in files:
        try:
            os.unlink(filename)
        except:
            pass


async def _render(
    json_data: str = Form(...),
    docx_file: UploadFile = File(...),
    image_files: list[UploadFile] = File([]),
    pdf: bool = True,
) -> None:
    data_file_name, data_file_name_temp = render_service.create_data_file(json_data)
    (
        template_file_name,
        template_file_name_temp,
    ) = await render_service.create_template_file(docx_file)
    images_file_name, images_file_temp = await render_service.create_images_file(
        image_files
    )
    result_file_docx_name, result_file_docx_name_temp = (
        render_service.reserve_docx_result_file()
    )

    tempfiles = (
        data_file_name_temp
        + template_file_name_temp
        + images_file_temp
        + result_file_docx_name_temp
    )

    render_service.to_docx(
        template_file_name, data_file_name, images_file_name, result_file_docx_name
    )

    if pdf:
        result_file_pdf_name_full = render_service.to_pdf(result_file_docx_name)
        tempfiles.append(result_file_pdf_name_full)
        return result_file_pdf_name_full, tempfiles
    else:
        return result_file_docx_name, tempfiles


@router.post("/to_pdf")
async def render_to_pdf(
    json_data: str = Form(...),
    docx_file: UploadFile = File(...),
    image_files: list[UploadFile] = File([]),
):
    result_file, tempfiles = await _render(json_data, docx_file, image_files, pdf=True)

    return FileResponse(
        result_file,
        media_type="application/pdf",
        background=BackgroundTask(cleanup, tempfiles),
    )


@router.post("/to_docx")
async def render_to_docx(
    json_data: str = Form(...),
    docx_file: UploadFile = File(...),
    image_files: list[UploadFile] = File([]),
):
    result_file, tempfiles = await _render(json_data, docx_file, image_files, pdf=False)

    return FileResponse(
        result_file,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        background=BackgroundTask(cleanup, tempfiles),
    )
