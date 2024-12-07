#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, ItemsView, Iterable, Iterator, KeysView, Optional, Sequence, Type, TypeVar, Tuple, Union, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from .builtins import Builtins
from .baseagent import BaseAgent as Agent


#--------------------------------------------------------------------------------
# 기본 컴포넌트.
#--------------------------------------------------------------------------------
class BaseBehaviour(Agent):
	def OnCreate(self) -> None:
		pass
	def OnDestroy(self) -> None:
		pass