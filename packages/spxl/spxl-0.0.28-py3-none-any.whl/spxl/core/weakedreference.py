#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, ItemsView, Iterable, Iterator, KeysView, Optional, Sequence, Type, TypeVar, Tuple, Union, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
import weakref
from .baseclass import BaseClass


#--------------------------------------------------------------------------------
# 오브젝트의 약한 참조 개체.
#--------------------------------------------------------------------------------
T = TypeVar("T", bound = BaseClass)
class WeakedReference(BaseClass, Generic[T]):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__weakedReference: weakref.ReferenceType[T]


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, target: T) -> None:
		base = super()
		base.__init__()
		self.__weakedReference = weakref.ref(target)


	#--------------------------------------------------------------------------------
	# 호출됨.
	#--------------------------------------------------------------------------------
	def __call__(self) -> Optional[T]:
		return self.__weakedReference
	

	#--------------------------------------------------------------------------------
	# 속성 반환.
	#--------------------------------------------------------------------------------
	def __getattr__(self, name: str) -> Any:
		try:
			target = self.__weakedReference()
			if not target:
				raise ReferenceError()
			return builtins.getattr(target, name)
		except Exception as exception:
			raise