import os
import shelve

from typing import List, Optional
from tian_drivers.src.driver import Driver
from typing import Any, AnyStr, Dict, List, NoReturn, Optional, Tuple


class MemoryStorage(Driver):
    POLICY_FILE = "policies"
    def __init__(
        self
    ):
        self._index_map = {}

    def query(self, **kwargs) -> List[Tuple]:
       return None

    def query_one(self, **kwargs) -> Tuple:
         with shelve.open(self._file, flag='r') as curr:
            # policy_json = curr.get(uid, None)
            # policy = Policy.from_json(policy_json) if policy_json else None
            # return policy
            pass

    def query_none(self, **kwargs) -> NoReturn:
        pass
    
    def add(self, ):
        """
            Store a policy
        """
        with shelve.open(self._file, flag='c', writeback=True) as curr:
            # if policy.uid in curr:
            #     raise PolicyExistsError(policy.uid)
            # curr[policy.uid] = policy.to_json()
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
        return None
    
    def execute(self, **kwargs) -> Any:
        return None
    
    def __str__(self):
        return f"FileStorage({str(self.__params)})"
    
    def __repr__(self):
        return f"FileStorage({str(self.__params)})"
    
