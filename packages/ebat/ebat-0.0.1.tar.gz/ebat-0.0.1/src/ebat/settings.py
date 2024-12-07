import os
from pathlib import Path

try:
    from local_settings import *
except:
    pass

PROJECT_ROOT = Path(os.path.abspath(os.path.dirname(__file__)))

DATASET_LINKS = {
    "medba": "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/Behaviouralbiometrics/iot_dataset.zip"
}

try:
    from local_settings import *
except:
    pass
