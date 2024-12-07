#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, ItemsView, Iterable, Iterator, KeysView, Optional, Sequence, Type, TypeVar, Tuple, Union, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
from enum import Enum
import logging
from logging import Logger as PythonStandardLogger
from logging import StreamHandler, FileHandler, Formatter
from logging.handlers import QueueHandler, QueueListener
import os
from queue import Queue
# from asyncio import Queue
from ..environment import Path
from .loglevel import LogLevel



#--------------------------------------------------------------------------------
# 로그 클래스.
#--------------------------------------------------------------------------------
class Logger():
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__name: str
	__filePath: str
	__level: LogLevel
	__logger: PythonStandardLogger
	__consoleHandler: StreamHandler
	__fileHandler: FileHandler
	__formatter: Formatter
	# __queue: Queue
	# __queueHandler: QueueHandler
	# __queueListener: QueueListener


	#--------------------------------------------------------------------------------
	# 로거 이름.
	#--------------------------------------------------------------------------------
	@property
	def Name(self) -> str:
		return self.__name
	

	#--------------------------------------------------------------------------------
	# 로그 파일 위치.
	#--------------------------------------------------------------------------------
	@property
	def FilePath(self) -> str:
		return self.__filePath


	#--------------------------------------------------------------------------------
	# 로그 수준.
	#--------------------------------------------------------------------------------
	@property
	def Level(self) -> LogLevel:
		return self.__level


	#--------------------------------------------------------------------------------
	# 프로세스 아이디.
	#--------------------------------------------------------------------------------
	@property
	def ProcessID(self) -> int:
		return os.getpid()
	

	#--------------------------------------------------------------------------------
	# 생성됨.
	# - 로그파일을 None 을 입력하면 
	#--------------------------------------------------------------------------------
	def __init__(self, name: str, filePath: str, level: LogLevel = LogLevel.DEBUG, 
			  useShowProcessID: bool = False, useShowName: bool = False) -> None:
		self.__name = name
		self.__filePath = filePath
		self.__level = level
	
		# 이름이 없다면 파일명에서 이름을 가져옴.
		if not name:
			if not filePath:
				raise NameError(name)
			else:
				_, fileName = Path.GetPathAndFileNameFromFileFullPath(filePath)
				name = os.path.splitext(fileName)

		self.__logger: PythonStandardLogger = logging.getLogger(name)
		self.__logger.setLevel(level.value)

		# 포맷 설정.
		if useShowProcessID:
			if useShowName:
				self.__formatter = Formatter("[%(asctime)s][%(name)s][%(process)d][%(levelname)s]%(message)s")
			else:
				self.__formatter = Formatter("[%(asctime)s][%(process)d][%(levelname)s]%(message)s")
		else:
			if useShowName:
				self.__formatter = Formatter("[%(asctime)s][%(name)s][%(process)d][%(levelname)s]%(message)s")
			else:
				self.__formatter = Formatter("[%(asctime)s][%(process)d][%(levelname)s]%(message)s")

		# 콘솔 로그.
		self.__consoleHandler = StreamHandler()
		self.__consoleHandler.setLevel(level.value)
		self.__consoleHandler.setFormatter(self.__formatter)
		self.__logger.addHandler(self.__consoleHandler) # 큐 핸들러 사용시 제외.

		# 파일 로그.
		if filePath:
			self.__fileHandler = FileHandler(filePath)
			self.__fileHandler.setLevel(level.value)
			self.__fileHandler.setFormatter(self.__formatter)
			self.__logger.addHandler(self.__fileHandler) # 큐 핸들러 사용시 제외.

		# # 큐 로그.
		# self.__queue = Queue()
		# self.__queueHandler = QueueHandler(self.__queue)
		# self.__logger.addHandler(self.__queueHandler)

		# # 큐 리스너.
		# handlers = list()
		# handlers.append(self.__consoleHandler)
		# if filePath:
		# 	handlers.append(self.__fileHandler)
		# self.__queueListener = QueueListener(self.__queue, *handlers)
		# self.__queueListener.start()


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def __Log(self, level: LogLevel, message: object) -> None:
		if isinstance(message, str):
			if not message.startswith("["):
				message = f" {message}"
		else:
			text = str(message)
			if not text.startswith("["):
				message = f" {text}"

		self.__logger.log(level.value, message)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogDebug(self, message: object) -> None:
		self.__Log(LogLevel.DEBUG, message)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogInfo(self, message: object) -> None:
		self.__Log(LogLevel.INFO, message)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogWarning(self, message: object) -> None:
		self.__Log(LogLevel.WARNING, message)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogError(self, message: object) -> None:
		self.__Log(LogLevel.ERROR, message)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogException(self, message: object, *arguments) -> None:
		self.__logger.exception(message, *arguments, True, True, 8)


	#--------------------------------------------------------------------------------
	# 기록.
	#--------------------------------------------------------------------------------
	def LogCritical(self, message: object) -> None:
		self.__Log(LogLevel.CRITICAL, message)