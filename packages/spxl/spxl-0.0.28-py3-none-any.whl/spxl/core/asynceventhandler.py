#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, ItemsView, Iterable, Iterator, KeysView, Optional, Sequence, Type, TypeVar, Tuple, Union, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import asyncio
from .baseclass import BaseClass


#--------------------------------------------------------------------------------
# 비동기 이벤트 핸들러.
#--------------------------------------------------------------------------------
class AsyncEventHandler(BaseClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__callbacks: Set[Callable[..., Awaitable[None]]]


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, callbacks: Optional[List[Callable[..., Awaitable[None]]]] = None) -> None:
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
	def Add(self, callable: Callable[..., Awaitable[None]]) -> None:
		if self.Contains(callable):
			return
		self.__callbacks.add(callable)


	#--------------------------------------------------------------------------------
	# 제거.
	#--------------------------------------------------------------------------------
	def Remove(self, callable: Callable[..., Awaitable[None]]) -> None:
		if not self.Contains(callable):
			return
		self.__callbacks.remove(callable)


	#--------------------------------------------------------------------------------
	# 포함 여부.
	#--------------------------------------------------------------------------------
	def Contains(self, callback: Callable[..., Awaitable[None]]) -> bool:
		if callback not in self.__callbacks:
			return False
		return True


	#--------------------------------------------------------------------------------
	# 등록된 비동기 함수 실행.
	#--------------------------------------------------------------------------------
	async def Execute(self, *arguments, **keywordArguments) -> None:
		tasks: List[Awaitable] = list()
		for callback in self.__callbacks:
			awaitable: Awaitable = callback(*arguments, **keywordArguments)
			tasks.append(awaitable)
		# asyncio.gather는 개별인자로 테스크를 취급하므로 언패킹해서 집어넣음.
		await asyncio.gather(*tasks)