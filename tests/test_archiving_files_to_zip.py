import os
from zipfile import ZipFile

from const import TMP_DIR


def test_archiving_files_to_zip():
    files_to_zip = [f'{TMP_DIR}/example.pdf', f'{TMP_DIR}/example.csv', f'{TMP_DIR}/example.xlsx']
    with ZipFile(f'{TMP_DIR}/my_homework.zip', 'w') as archive:
        for file in files_to_zip:
            archive.write(file, arcname=os.path.basename(file))
    assert os.path.exists(f'{TMP_DIR}/my_homework.zip')


def test_read_files_in_zip():
    with ZipFile(f'{TMP_DIR}/my_homework.zip', 'r') as archive:
        assert 'example.pdf' in archive.namelist()
        assert 'example.csv' in archive.namelist()
        assert 'example.xlsx' in archive.namelist()
