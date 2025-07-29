import os
from zipfile import ZipFile
from pypdf import PdfReader
from io import BytesIO, TextIOWrapper
from const import TMP_DIR
import csv
import pandas as pd


def test_archiving_files_to_zip():
    files_to_zip = [f'{TMP_DIR}/example.pdf', f'{TMP_DIR}/example.csv', f'{TMP_DIR}/example.xlsx']
    with ZipFile(f"{TMP_DIR}/my_homework.zip", 'w') as archive:
        for file in files_to_zip:
            archive.write(file, arcname=os.path.basename(file))
    assert os.path.exists(f'{TMP_DIR}/my_homework.zip')


def test_check_existing_files_in_zip():
    with ZipFile(f"{TMP_DIR}/my_homework.zip", mode="r") as archive:
        assert 'example.pdf' in archive.namelist()
        assert 'example.csv' in archive.namelist()
        assert 'example.xlsx' in archive.namelist()


def test_read_pdf_file():
    with ZipFile(f"{TMP_DIR}/my_homework.zip", mode="r") as archive:
        assert 'example.pdf' in archive.namelist()
        pdf_stream = BytesIO(archive.read('example.pdf'))
        pdf_file = PdfReader(pdf_stream)
        assert len(pdf_file.pages) == 1


def test_read_csv_file():
    with ZipFile(f"{TMP_DIR}/my_homework.zip", mode="r") as archive:
        assert 'example.csv' in archive.namelist()
        csv_stream = BytesIO(archive.read('example.csv'))
        csv_file = pd.read_csv(csv_stream)
        assert isinstance(csv_file, pd.DataFrame)
        assert csv_file.shape == (24, 6)


def test_read_xlsx_file():
    with ZipFile(f"{TMP_DIR}/my_homework.zip", mode="r") as archive:
        assert 'example.xlsx' in archive.namelist()
        xlsx_stream = BytesIO(archive.read('example.xlsx'))
        xlsx_file = pd.read_excel(xlsx_stream)
        assert isinstance(xlsx_file, pd.DataFrame)
        assert xlsx_file.shape == (16, 7)


