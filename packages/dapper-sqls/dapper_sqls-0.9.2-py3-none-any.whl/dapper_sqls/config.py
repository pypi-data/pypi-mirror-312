# -*- coding: latin -*-
from .models import ConnectionStringData
import winreg

class Config(object):
    def __init__(self, server: str, database: str, username: str, password: str, sql_version: int = None, api_environment=False, default_attempts=1, default_wait_timeout=2):
        self._api_environment = api_environment
        self._default_attempts = default_attempts
        self._default_wait_timeout = default_wait_timeout
        self._connectionStringDataQuery = ConnectionStringData(server, database, username, password)
        self._connectionStringDataStored = ConnectionStringData(server, database, username, password)
        self._sql_version = sql_version

    @property
    def api_environment(self):
        return self._api_environment

    @api_environment.setter
    def api_environment(self, value):
        if not isinstance(value, bool):
            raise ValueError("O valor atribuído a api_environment deve ser do tipo booleano")
        self._api_environment = value

    @property
    def default_attempts(self):
        return self._default_attempts

    @default_attempts.setter
    def default_attempts(self, value):
        if not isinstance(value, int):
            raise ValueError("O valor atribuído a default_attempts deve ser do tipo inteiro")
        self._default_attempts = value

    @property
    def default_wait_timeout(self):
        return self._default_wait_timeout

    @default_wait_timeout.setter
    def default_wait_timeout(self, value):
        if not isinstance(value, int):
            raise ValueError("O valor atribuído a default_wait_timeout deve ser do tipo inteiro")
        self._default_wait_timeout = value

    @property
    def connectionStringDataQuery(self):
        return self._connectionStringDataQuery

    @connectionStringDataQuery.setter
    def connectionStringDataQuery(self, value):
        if not isinstance(value, ConnectionStringData):
            raise ValueError("O valor atribuído a connectionStringDataQuery deve ser do tipo ConnectionStringData")
        self._connectionStringDataQuery = value

    @property
    def connectionStringDataStored(self):
        return self._connectionStringDataStored

    @connectionStringDataStored.setter
    def connectionStringDataStored(self, value):
        if not isinstance(value, ConnectionStringData):
            raise ValueError("O valor atribuído a connectionStringDataStored deve ser do tipo ConnectionStringData")
        self._connectionStringDataStored = value

    @property
    def sql_version(self):
        return self._sql_version

    @sql_version.setter
    def sql_version(self, value):
        if not isinstance(value, int) and value is not None:
            raise ValueError("O valor atribuído a sql_version deve ser do tipo inteiro ou None")
        self._sql_version = value

    @staticmethod
    def get_all_odbc_driver_versions():
        driver_versions = []
        try:
            # Abrir a chave onde as informações sobre os drivers ODBC estão armazenadas
            key_path = r"SOFTWARE\ODBC\ODBCINST.INI"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)

            # Iterar sobre as subchaves para encontrar os drivers específicos
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)

                    # Verificar se a subchave contém o valor 'Driver'
                    try:
                        driver_name, _ = winreg.QueryValueEx(subkey, "Driver")
                        if subkey_name.startswith('ODBC Driver'):
                            driver_versions.append(subkey_name)
                    
                    except FileNotFoundError:
                        pass  # A subchave não possui a entrada 'Driver'

                    i += 1
                except OSError:
                    break

        except Exception as e:
            print(f"Erro ao acessar o registro: {e}")

        return sorted(driver_versions, key=lambda x: int(x.split()[-4]), reverse=True)




