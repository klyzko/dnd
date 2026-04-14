import logging
from pathlib import Path


def setup_logger(name: str = "app") -> logging.Logger:
    """Настройка и возврат логгера"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    log_dir = Path(__file__).parent / 'logs'
    log_dir.mkdir(exist_ok=True)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    file_handler = logging.FileHandler(log_dir / 'app.log', encoding='utf-8')
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Создаём глобальный экземпляр логгера
logg = setup_logger()