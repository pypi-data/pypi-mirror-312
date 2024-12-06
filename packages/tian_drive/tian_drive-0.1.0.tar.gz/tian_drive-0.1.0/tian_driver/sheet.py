import os
import shelve

from typing import List, Optional
from tian_drivers.src.driver import Driver
from typing import Any, AnyStr, Dict, List, NoReturn, Optional, Tuple


class SheetStorage(Driver):
    POLICY_FILE = "policies"
    def __init__(
        self,
        storage_dir: Optional[AnyStr] = None
    ):
        os.makedirs(storage_dir, exist_ok=True)
        self._file = "{}/{}".format(os.path.abspath(storage_dir), self.POLICY_FILE)

    def query(self, **kwargs) -> List[Tuple]:
       return None

    def query_one(self, **kwargs) -> Tuple:
        pass

    def query_none(self, **kwargs) -> NoReturn:
        pass
    
    def add(self, ):
        """
            Store a policy
        """
        pass

    def commit(self) -> NoReturn:
        pass

    def rollback(self) -> NoReturn:
        pass

    def close(self) -> NoReturn:
        pass

    def get_real_driver(self) -> Any:
       return None

    def placeholder(self, **kwargs) -> AnyStr:
        return '%s'

    def reset_placeholder(self) -> NoReturn:
        """Reset place holder status (do nothing)"""

    def information(self) -> Any:
        return None

    def short_information(self) -> Dict[str, Any]:
        return {
            "name": "SheetStorage",
            "type": "file",
            "path": "aaaa"
        }
    
    def execute(self, **kwargs) -> Any:
        return None
    
    def __str__(self):
        return f"SheetStorage({str(self.__params)})"
    
    def __repr__(self):
        return f"SheetStorage({str(self.__params)})"
    