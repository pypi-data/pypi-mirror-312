#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, ItemsView, Iterable, Iterator, KeysView, Optional, Sequence, Type, TypeVar, Tuple, Union, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from ..ecs import Entity, Component
from .target import Target


#------------------------------------------------------------------------
# 전역 상수 목록.
#------------------------------------------------------------------------
LINEFEED: str = "\n"
READTEXT: str = "rt"
READBINARY: str = "rb"
WRITETEXT: str = "wt"
WRITEBINARY: str = "wb"
UTF8: str = "utf-8"
TAB: str = "\t"


#------------------------------------------------------------------------
# 작업 공정.
#------------------------------------------------------------------------
class Task(Entity):
	#------------------------------------------------------------------------
	# 멤버 변수 목록.
	#------------------------------------------------------------------------


	#------------------------------------------------------------------------
	# 생성됨.
	#------------------------------------------------------------------------
	def OnCreate(self, *arguments, **keywordArguments) -> None:
		base = super()
		base.OnCreate(*arguments, **keywordArguments)
		

	#------------------------------------------------------------------------
	# 파괴됨.
	#------------------------------------------------------------------------
	def OnDestroy(self) -> None:
		base = super()
		base.OnDestroy()


	#------------------------------------------------------------------------
	# 시작됨.
	#------------------------------------------------------------------------
	def OnStart(self, target: Target) -> None:
		return


	#------------------------------------------------------------------------
	# 종료됨.
	#------------------------------------------------------------------------
	def OnComplete(self, target: Target, resultCode: int) -> None:
		return


	#------------------------------------------------------------------------
	# 실행됨.
	#------------------------------------------------------------------------
	def OnExecute(self, target: Target, *arguments, **keywordArguments) -> int:
		return 0
	

	#------------------------------------------------------------------------
	# 실행.
	#------------------------------------------------------------------------
	def Execute(self, target: Target, *arguments, **keywordArguments) -> int:
		try:
			self.OnStart(target)
			resultCode = self.OnExecute(target, *arguments, **keywordArguments)
			self.OnComplete(target, resultCode)
			return resultCode
		except Exception as exception:
			raise
