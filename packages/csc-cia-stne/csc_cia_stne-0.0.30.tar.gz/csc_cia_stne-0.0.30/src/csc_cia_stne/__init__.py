import os
from dotenv import load_dotenv

# Carrega .env
load_dotenv()
logger = None  # Inicializa como None
#if os.getenv('ambiente_de_execucao') is not None and os.getenv('ambiente_de_execucao') == "karavela":
#    from .logger_json import logger
#else:
#    from .logger_rich import logger


if os.getenv('ambiente_de_execucao') is not None and os.getenv('ambiente_de_execucao') == "karavela":
    from .logger_json import get_logger as get_logger_json
    def logger():
        return get_logger_json()
else:
    from .logger_rich import get_logger as get_logger_rich
    def logger():
        return get_logger_rich()




from .karavela import Karavela
#from .utilitarios.classes import Util
from .servicenow import ServiceNow
from .stne_admin import StoneAdmin
from .bc_sta import BC_STA
from .bc_correios import BC_Correios
from .gcp_bigquery import BigQuery
from .email import Email
#from .utilitarios.functions import titulo
# Define os itens disponíveis para importação
__all__ = [
    "titulo",
    "BigQuery",
    "BC_Correios",
    "BC_STA",
    "StoneAdmin",
    "ServiceNow",
    "Util",
    "logger",
    "Email"
]