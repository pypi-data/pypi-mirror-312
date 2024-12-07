#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, ItemsView, Iterable, Iterator, KeysView, Optional, Sequence, Type, TypeVar, Tuple, Union, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
from ..core import Builtins, BaseClass
# from threading import Lock
# from asyncio import Lock


#--------------------------------------------------------------------------------
# 저장소에 들어가는 항목.
#--------------------------------------------------------------------------------
class InternalRepositoryItem(BaseClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	type: type
	instance: object


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		base = super()
		base.__init__()
		self.type = None
		self.instance = None


#--------------------------------------------------------------------------------
# 기본 저장소 클래스.
# - 저장소 클래스를 통해 객체를 호출하면 최초 1회 할당 이후 계속 같은 객체를 반환한다.
# - 저장소 클래스 내부에서 생성되는 탓에 생성시 인자가 없는 객체여야 한다.
# - 만일 생성시 인자가 들어간다면 최초 생성인지 사용자가 판단해서 인자를 넣어주어야 한다.
# - 혹은 Link() 를 통해 외부에서 할당한 인스턴스를 넣어둘 수 있다.
# - 이 클래스를 상속받아서 독자적인 저장소 클래스를 만들 수 있다.
#--------------------------------------------------------------------------------
T = TypeVar("T", bound = Any)
class BaseRepository(BaseClass):
	#--------------------------------------------------------------------------------
	# 클래스 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__IsInitialized: bool = False
	__TargetInstances: Dict[type, InternalRepositoryItem] = dict()


	#--------------------------------------------------------------------------------
	# 이벤트 체크.
	#--------------------------------------------------------------------------------
	@classmethod
	def CheckEvent(classType) -> None:
		if not classType.__IsInitialized:
			classType.OnInitialize()
			classType.__IsInitialized = True


	#--------------------------------------------------------------------------------
	# 초기화됨.
	#--------------------------------------------------------------------------------
	@classmethod
	def OnInitialize(classType) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 파괴됨.
	#--------------------------------------------------------------------------------
	@classmethod
	def OnFinalize(classType) -> None:
		classType.__TargetInstances.clear()


	#--------------------------------------------------------------------------------
	# 저장소에 모든 인스턴스 제거.
	#--------------------------------------------------------------------------------
	@classmethod
	def Cleanup(classType) -> None:
		classType.CheckEvent()
		classType.__TargetInstances.clear()
	

	#--------------------------------------------------------------------------------
	# 저장소에 기존 인스턴스 설정 (기존 것이 있다면 제거 후 설정).
	#--------------------------------------------------------------------------------
	@classmethod
	def Link(classType, instance: T) -> bool:
		classType.CheckEvent()
		if not instance:
			return False
		
		isType: bool = Builtins.IsInstanceType(instance, type)
		if isType:
			return False

		instanceClassType: Type[T] = instance.__class__
		if instanceClassType in classType.__TargetInstances:
			del classType.__TargetInstances[instanceClassType]
		classType.__TargetInstances[instanceClassType] = instance
		return True
	

	#--------------------------------------------------------------------------------
	# 저장소에 신규 인스턴스 생성 (기존 것이 있다면 제거 후 생성).
	# - 생성자에 값을 넣기 위해 args와 kwargs 값을 넣어주어야 한다.
	# - 물론 값을 넣지 않아도 상관없으며 그 경우 인자 없는 생성자가 호출된다. (생성자에 인자가 존재한다면 주의)
	#--------------------------------------------------------------------------------
	@classmethod
	def Set(classType, targetClassType: Type[T], *args: Any, **kwargs: Any) -> T:
		classType.CheckEvent()
		if classType.Contains(targetClassType):
			del classType.__TargetInstances[targetClassType]

		item = InternalRepositoryItem()
		item.type = targetClassType
		item.instance = targetClassType(*args, **kwargs)
		classType.__TargetInstances[targetClassType] = item
		return item.instance
	

	#--------------------------------------------------------------------------------
	# 저장소에 존재하는 인스턴스 반환.
	# - 없다면 신규 생성하며 이 때 생성자에 값을 넣기 위해 args와 kwargs 값을 넣어주어야 한다.
	# - 물론 값을 넣지 않아도 상관없으며 그 경우 인자 없는 생성자가 호출된다. 생성자에 인자가 존재한다면 주의)
	#--------------------------------------------------------------------------------
	@classmethod
	def Get(classType, targetClassType: Type[T], *args: Any, **kwargs: Any) -> T:
		classType.CheckEvent()
		if classType.Contains(targetClassType):
			item: InternalRepositoryItem = classType.__TargetInstances[targetClassType]
			return item.instance
		else:
			item: InternalRepositoryItem = InternalRepositoryItem()
			item.type = targetClassType
			item.instance = targetClassType(*args, **kwargs)
			classType.__TargetInstances[targetClassType] = item
			return item.instance

	#--------------------------------------------------------------------------------
	# 저장소에 해당 인스턴스가 존재하는지 여부.
	#--------------------------------------------------------------------------------
	@classmethod
	def Contains(classType, targetClassType: Type[T]) -> bool:
		classType.CheckEvent()
		if targetClassType not in classType.__TargetInstances:
			return False
		return True
	

	#--------------------------------------------------------------------------------
	# 저장소에 존재하는 인스턴스 반환.
	# - Get과 동일하나 부모를 인자로 넣으면 자식이 있을 경우 그 자식을 가져온다.
	# - 따라서 없으면 자동으로 대상을 추가 할 수가 없어서 안에 없다면 None을 뱉는다.
	#--------------------------------------------------------------------------------
	@classmethod
	def GetInherited(classType, targetClassType: Type[T]) -> T:
		classType.CheckEvent()
		if classType.Contains(targetClassType):
			item: InternalRepositoryItem = classType.__TargetInstances[targetClassType]
			return item.instance
		else:
			for instanceClassType in classType.__TargetInstances:
				if not issubclass(instanceClassType, targetClassType): # instanceClassType의 부모가 targetClassType일 때 참.
					continue
				item: InternalRepositoryItem = classType.__TargetInstances[instanceClassType]
				return item.instance
			return None