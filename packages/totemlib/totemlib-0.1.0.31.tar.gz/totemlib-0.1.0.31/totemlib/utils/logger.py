# # Utilitarios generales
# # Creado por: Totem Bear
# # Fecha: 23-Ago-2023

# # ****************************************************************
# # *********** Manage the logs ***********

import logging
from logging.handlers import RotatingFileHandler


# Dictionary to manage the log levels
logLevels = {
    'NOTSET': 0,
    'DEBUG': 10,
    'INFO': 20,
    'WARNING': 30,
    'ERROR': 40,
    'CRITICAL': 50,
    'notset': 0,
    'debug': 10,
    'info': 20,
    'warning': 30,
    'error': 40,
    'critical': 50
}

def setup_logger(log_file_name, level=None, format=None, max_bytes=5*1024*1024, backup_count=3):
    """
    Configura el logger para escribir en un archivo con rotación basada en tamaño.

    Args:
        log_file_name (str): Nombre del archivo de log.
        level (str, opcional): Nivel de log.
        format (str, opcional): Formato de los mensajes de log.
        max_bytes (int, opcional): Tamaño máximo del archivo de log en bytes antes de rotar.
        backup_count (int, opcional): Número de archivos de respaldo a mantener.
    """
    logger = logging.getLogger()
    logger.setLevel(logLevels.get(level, logging.INFO))

    # Crear el manejador de rotación
    handler = RotatingFileHandler(
        log_file_name,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    formatter = logging.Formatter(format if format else '%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Evitar agregar múltiples manejadores si ya existen
    if not logger.handlers:
        logger.addHandler(handler)

    return logger

    # logging.basicConfig(filename=log_file_name, level=level if level in logLevels else 'INFO',
    #                     format=format if format else '%(asctime)s - %(levelname)s - %(message)s')
    
    # return logging.getLogger()


# To use logger in the application - function printLogger or:
# utils.logger.debug('Este es un mensaje de registro de nivel DEBUG')
# utils.logger.info('Este es un mensaje de registro de nivel INFO')
# utils.logger.warning('Este es un mensaje de registro de nivel WARNING')
# utils.logger.error('Este es un mensaje de registro de nivel ERROR')
# utils.logger.critical('Este es un mensaje de registro de nivel CRITICAL')


# Print the msg into the logger file "logFileStr" by level and encrypt
def printLog(log_file_name: str, msg: str, level: str):
    # TODO: remove this print
    print(f"***** printLog: log_file_name={log_file_name} - msg={msg}")
    if level in logLevels:
        logging.log(logLevels[level], msg)
    else:
        logging.info(msg)
