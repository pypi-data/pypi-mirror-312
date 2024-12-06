from pathlib import Path
from cli_logger.logger import setup_logger
from pytoolbox.config import LOGGER_CONFIG

logger = setup_logger(__name__, LOGGER_CONFIG)

def ensure_folder_exists(folder_path: str | Path) -> None:
    folder = Path(folder_path)

    if not folder.exists():
        logger.info(f"Folder does not exist. Creating: {folder}")
        folder.mkdir(parents=True, exist_ok=True)

    if not folder.is_dir():
        logger.error(f"Path is not a directory: {folder}")
        raise NotADirectoryError(f"Path is not a directory: {folder}")

    logger.info("Folder is ready.")
