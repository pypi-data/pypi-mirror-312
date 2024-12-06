import pytest
from pathlib import Path
from pytoolbox.folder import ensure_folder_exists
import tempfile

def test_create_folder():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_folder = Path(temp_dir) / "test_folder"

        ensure_folder_exists(test_folder)

        assert test_folder.is_dir()

def test_not_a_directory():
    with tempfile.NamedTemporaryFile() as temp_file:
        test_file = Path(temp_file.name)

        with pytest.raises(NotADirectoryError):
            ensure_folder_exists(test_file)
