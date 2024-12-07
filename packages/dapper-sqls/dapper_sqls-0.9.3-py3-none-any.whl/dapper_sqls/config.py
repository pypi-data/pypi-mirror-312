# -*- coding: latin -*-
from .models import ConnectionStringData
import sys
from _typeshed import ReadableBuffer, Unused
from types import TracebackType
from typing import Any, Final, Literal, final, overload
from typing_extensions import Self, TypeAlias

if sys.platform == "win32":
    # Though this class has a __name__ of PyHKEY, it's exposed as HKEYType for some reason
    @final
    class HKEYType:
        def __bool__(self) -> bool: ...
        def __int__(self) -> int: ...
        def __enter__(self) -> Self: ...
        def __exit__(
            self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
        ) -> bool | None: ...
        def Close(self) -> None: ...
        def Detach(self) -> int: ...
        def __hash__(self) -> int: ...
        @property
        def handle(self) -> int: ...

    _KeyType: TypeAlias = HKEYType | int
    def CloseKey(hkey: _KeyType, /) -> None: ...
    def ConnectRegistry(computer_name: str | None, key: _KeyType, /) -> HKEYType: ...
    def CreateKey(key: _KeyType, sub_key: str | None, /) -> HKEYType: ...
    def CreateKeyEx(key: _KeyType, sub_key: str | None, reserved: int = 0, access: int = 131078) -> HKEYType: ...
    def DeleteKey(key: _KeyType, sub_key: str, /) -> None: ...
    def DeleteKeyEx(key: _KeyType, sub_key: str, access: int = 256, reserved: int = 0) -> None: ...
    def DeleteValue(key: _KeyType, value: str, /) -> None: ...
    def EnumKey(key: _KeyType, index: int, /) -> str: ...
    def EnumValue(key: _KeyType, index: int, /) -> tuple[str, Any, int]: ...
    def ExpandEnvironmentStrings(string: str, /) -> str: ...
    def FlushKey(key: _KeyType, /) -> None: ...
    def LoadKey(key: _KeyType, sub_key: str, file_name: str, /) -> None: ...
    def OpenKey(key: _KeyType, sub_key: str, reserved: int = 0, access: int = 131097) -> HKEYType: ...
    def OpenKeyEx(key: _KeyType, sub_key: str, reserved: int = 0, access: int = 131097) -> HKEYType: ...
    def QueryInfoKey(key: _KeyType, /) -> tuple[int, int, int]: ...
    def QueryValue(key: _KeyType, sub_key: str | None, /) -> str: ...
    def QueryValueEx(key: _KeyType, name: str, /) -> tuple[Any, int]: ...
    def SaveKey(key: _KeyType, file_name: str, /) -> None: ...
    def SetValue(key: _KeyType, sub_key: str, type: int, value: str, /) -> None: ...
    @overload  # type=REG_DWORD|REG_QWORD
    def SetValueEx(
        key: _KeyType, value_name: str | None, reserved: Unused, type: Literal[4, 5], value: int | None, /
    ) -> None: ...
    @overload  # type=REG_SZ|REG_EXPAND_SZ
    def SetValueEx(
        key: _KeyType, value_name: str | None, reserved: Unused, type: Literal[1, 2], value: str | None, /
    ) -> None: ...
    @overload  # type=REG_MULTI_SZ
    def SetValueEx(
        key: _KeyType, value_name: str | None, reserved: Unused, type: Literal[7], value: list[str] | None, /
    ) -> None: ...
    @overload  # type=REG_BINARY and everything else
    def SetValueEx(
        key: _KeyType,
        value_name: str | None,
        reserved: Unused,
        type: Literal[0, 3, 8, 9, 10, 11],
        value: ReadableBuffer | None,
        /,
    ) -> None: ...
    @overload  # Unknown or undocumented
    def SetValueEx(
        key: _KeyType,
        value_name: str | None,
        reserved: Unused,
        type: int,
        value: int | str | list[str] | ReadableBuffer | None,
        /,
    ) -> None: ...
    def DisableReflectionKey(key: _KeyType, /) -> None: ...
    def EnableReflectionKey(key: _KeyType, /) -> None: ...
    def QueryReflectionKey(key: _KeyType, /) -> bool: ...

    HKEY_CLASSES_ROOT: int
    HKEY_CURRENT_USER: int
    HKEY_LOCAL_MACHINE: int
    HKEY_USERS: int
    HKEY_PERFORMANCE_DATA: int
    HKEY_CURRENT_CONFIG: int
    HKEY_DYN_DATA: int

    KEY_ALL_ACCESS: Final = 983103
    KEY_WRITE: Final = 131078
    KEY_READ: Final = 131097
    KEY_EXECUTE: Final = 131097
    KEY_QUERY_VALUE: Final = 1
    KEY_SET_VALUE: Final = 2
    KEY_CREATE_SUB_KEY: Final = 4
    KEY_ENUMERATE_SUB_KEYS: Final = 8
    KEY_NOTIFY: Final = 16
    KEY_CREATE_LINK: Final = 32

    KEY_WOW64_64KEY: Final = 256
    KEY_WOW64_32KEY: Final = 512

    REG_BINARY: Final = 3
    REG_DWORD: Final = 4
    REG_DWORD_LITTLE_ENDIAN: Final = 4
    REG_DWORD_BIG_ENDIAN: Final = 5
    REG_EXPAND_SZ: Final = 2
    REG_LINK: Final = 6
    REG_MULTI_SZ: Final = 7
    REG_NONE: Final = 0
    REG_QWORD: Final = 11
    REG_QWORD_LITTLE_ENDIAN: Final = 11
    REG_RESOURCE_LIST: Final = 8
    REG_FULL_RESOURCE_DESCRIPTOR: Final = 9
    REG_RESOURCE_REQUIREMENTS_LIST: Final = 10
    REG_SZ: Final = 1

    REG_CREATED_NEW_KEY: Final = 1  # undocumented
    REG_LEGAL_CHANGE_FILTER: Final = 268435471  # undocumented
    REG_LEGAL_OPTION: Final = 31  # undocumented
    REG_NOTIFY_CHANGE_ATTRIBUTES: Final = 2  # undocumented
    REG_NOTIFY_CHANGE_LAST_SET: Final = 4  # undocumented
    REG_NOTIFY_CHANGE_NAME: Final = 1  # undocumented
    REG_NOTIFY_CHANGE_SECURITY: Final = 8  # undocumented
    REG_NO_LAZY_FLUSH: Final = 4  # undocumented
    REG_OPENED_EXISTING_KEY: Final = 2  # undocumented
    REG_OPTION_BACKUP_RESTORE: Final = 4  # undocumented
    REG_OPTION_CREATE_LINK: Final = 2  # undocumented
    REG_OPTION_NON_VOLATILE: Final = 0  # undocumented
    REG_OPTION_OPEN_LINK: Final = 8  # undocumented
    REG_OPTION_RESERVED: Final = 0  # undocumented
    REG_OPTION_VOLATILE: Final = 1  # undocumented
    REG_REFRESH_HIVE: Final = 2  # undocumented
    REG_WHOLE_HIVE_VOLATILE: Final = 1  # undocumented

    error = OSError

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
            raise ValueError("The value assigned to api_environment must be of type boolean")
        self._api_environment = value

    @property
    def default_attempts(self):
        return self._default_attempts

    @default_attempts.setter
    def default_attempts(self, value):
        if not isinstance(value, int):
            raise ValueError("The value assigned to default_attempts must be of type integer")
        self._default_attempts = value

    @property
    def default_wait_timeout(self):
        return self._default_wait_timeout

    @default_wait_timeout.setter
    def default_wait_timeout(self, value):
        if not isinstance(value, int):
            raise ValueError("The value assigned to default_wait_timeout must be of type integer")
        self._default_wait_timeout = value

    @property
    def connectionStringDataQuery(self):
        return self._connectionStringDataQuery

    @connectionStringDataQuery.setter
    def connectionStringDataQuery(self, value):
        if not isinstance(value, ConnectionStringData):
            raise ValueError("The value assigned to connectionStringDataQuery must be of type ConnectionStringData")
        self._connectionStringDataQuery = value

    @property
    def connectionStringDataStored(self):
        return self._connectionStringDataStored

    @connectionStringDataStored.setter
    def connectionStringDataStored(self, value):
        if not isinstance(value, ConnectionStringData):
            raise ValueError("The value assigned to connectionStringDataStored must be of type ConnectionStringData")
        self._connectionStringDataStored = value

    @property
    def sql_version(self):
        return self._sql_version

    @sql_version.setter
    def sql_version(self, value):
        if not isinstance(value, int) and value is not None:
            raise ValueError("The value assigned to sql_version must be of type integer or None")
        self._sql_version = value


    @staticmethod
    def get_all_odbc_driver_versions():
        driver_versions = []
        try:
            key_path = r"SOFTWARE\ODBC\ODBCINST.INI"
            key = OpenKey(HKEY_LOCAL_MACHINE, key_path)

            i = 0
            while True:
                try:
                    subkey_name = EnumKey(key, i)
                    subkey = OpenKey(key, subkey_name)

                    try:
                        driver_name, _ = QueryValueEx(subkey, "Driver")
                        if subkey_name.startswith('ODBC Driver'):
                            driver_versions.append(subkey_name)
                    
                    except FileNotFoundError:
                        pass  

                    i += 1
                except OSError:
                    break

        except Exception as e:
            print(f"Erro ao acessar o registro: {e}")

        return sorted(driver_versions, key=lambda x: int(x.split()[-4]), reverse=True)




