import os
from zipfile import ZipFile
from pypdf import PdfReader
from io import BytesIO
from const import TMP_DIR
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


def test_read_pdf_file_from_zip():
    with ZipFile(f"{TMP_DIR}/my_homework.zip", mode="r") as archive:
        assert 'example.pdf' in archive.namelist()
        pdf_stream = BytesIO(archive.read('example.pdf'))
        pdf_file = PdfReader(pdf_stream)
        assert isinstance(pdf_file, PdfReader)
        assert pdf_file.pdf_header == "%PDF-1.5"
        assert pdf_file.is_encrypted == False
        assert len(pdf_file.pages) == 1
        assert 'Document file type: PDF' in pdf_file.get_page(0).extract_text()
        assert 'Purpose: Provide example of this file type' in pdf_file.get_page(0).extract_text()
        assert 'File created by http://www.online-convert.com' in pdf_file.get_page(0).extract_text()
        assert pdf_file.is_encrypted == False


def test_read_csv_file_from_zip():
    with ZipFile(f"{TMP_DIR}/my_homework.zip", mode="r") as archive:
        assert 'example.csv' in archive.namelist()
        csv_stream = BytesIO(archive.read('example.csv'))
        csv_file = pd.read_csv(csv_stream)
        assert csv_file.shape == (24, 6)
        assert isinstance(csv_file, pd.DataFrame)
        assert ['CSV test file', 'Unnamed: 1', 'Unnamed: 2',
                'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5'] == list(csv_file.columns)


def test_read_xlsx_file_from_zip():
    with ZipFile(f"{TMP_DIR}/my_homework.zip", mode="r") as archive:
        assert 'example.xlsx' in archive.namelist()
        xlsx_file = pd.read_excel(archive.read('example.xlsx'), engine='openpyxl')
        assert xlsx_file.shape == (16, 7)
        assert isinstance(xlsx_file, pd.DataFrame)
        assert 'XLSX test file' in xlsx_file



