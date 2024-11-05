import os

LOG_FILE_NAME = '_uploaded_log.json'  # Будет создан в src/data после импорта
DATA_DIR = os.path.join(os.path.dirname(
    os.path.abspath(__file__)),
    'src',
    'data'
)
