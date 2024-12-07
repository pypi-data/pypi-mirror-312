#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, ItemsView, Iterable, Iterator, KeysView, Optional, Sequence, Type, TypeVar, Tuple, Union, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from .baseclass import BaseClass


#--------------------------------------------------------------------------------
# 이벤트 핸들러.
#--------------------------------------------------------------------------------
class EventHandler(BaseClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__callbacks: Set[Callable[..., None]]


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, callbacks: Optional[List[Callable[..., None]]] = None) -> None:
		self.__callbacks = set()
		if callbacks:
			self.__callbacks.update(callbacks)


	#--------------------------------------------------------------------------------
	# 전체 제거.
	#--------------------------------------------------------------------------------
	def Clear(self) -> None:
		self.__callbacks.clear()


	#--------------------------------------------------------------------------------
	# 추가.
	#--------------------------------------------------------------------------------
	def Add(self, callback: Callable[..., None]) -> None:
		if self.Contains(callback):
			return
		self.__callbacks.add(callback)


	#--------------------------------------------------------------------------------
	# 제거.
	#--------------------------------------------------------------------------------
	def Remove(self, callback: Callable[..., None]) -> None:
		if not self.Contains(callback):
			return
		self.__callbacks.remove(callback)


	#--------------------------------------------------------------------------------
	# 포함 여부.
	#--------------------------------------------------------------------------------
	def Contains(self, callback: Callable[..., None]) -> bool:
		if callback not in self.__callbacks:
			return False
		return True


	#--------------------------------------------------------------------------------
	# 등록된 함수 실행.
	#--------------------------------------------------------------------------------
	def Execute(self, *arguments, **keywordArguments) -> None:
		for callable in self.__callbacks:
			callable(*arguments, **keywordArguments)