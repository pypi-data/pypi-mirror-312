#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, ItemsView, Iterable, Iterator, KeysView, Optional, Sequence, Type, TypeVar, Tuple, Union, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from ..core import ManagedObject, WeakedReference


#--------------------------------------------------------------------------------
# 기본 기능 객체.
# - 특정 데이터와 기능을 보유하고 엔티티에 종속되는 객체.
#--------------------------------------------------------------------------------
class Component(ManagedObject):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__ownerIdentifer: str


	#--------------------------------------------------------------------------------
	# 소유자 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Owner(self) -> WeakedReference[ManagedObject]:
		return ManagedObject.FindObject(self.__ownerIdentifer)


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def OnCreate(self, *arguments, **keywordArguments) -> None:
		base = super()
		base.OnCreate(*arguments, **keywordArguments)
		self.__ownerIdentifer = keywordArguments.get("ownerIdentifer")


	#--------------------------------------------------------------------------------
	# 파괴됨.
	#--------------------------------------------------------------------------------
	def OnDestroy(self) -> None:
		base = super()
		base.OnDestroy()
