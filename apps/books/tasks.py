import os
from pdf2image import convert_from_path
from celery import shared_task

from root.settings import BASE_DIR


@shared_task
def convert_pdf_to_jpg(pdf_url, image_url, image_name):
    url_pdf = f"{BASE_DIR}/{pdf_url}"
    url_jpg = f"{BASE_DIR}/media/{image_url}"

    if not os.path.exists(url_jpg) and not os.path.isdir(url_jpg):
        os.makedirs(url_jpg)

    convert_from_path(
        pdf_path=url_pdf,
        dpi=500,
        output_folder=url_jpg,
        output_file="".join(image_name.split('.jpg')[0:-1]),
        fmt='jpeg',
        first_page=1,
        single_file=True
    )
