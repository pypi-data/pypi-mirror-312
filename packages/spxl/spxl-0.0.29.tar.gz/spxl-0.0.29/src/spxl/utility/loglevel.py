#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, ItemsView, Iterable, Iterator, KeysView, Optional, Sequence, Type, TypeVar, Tuple, Union, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from enum import Enum



#--------------------------------------------------------------------------------
# 로그 종류.
#--------------------------------------------------------------------------------
class LogLevel(Enum):
	NONE = 0
	DEBUG = 10
	INFO = 20
	WARNING = 30
	ERROR = 40
	CRITICAL = 50