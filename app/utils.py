import logging

def setup_logging():
    """
    Настройка конфигурации логирования.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger

# Создаем логгер для использования в других частях приложения
logger = setup_logging()
