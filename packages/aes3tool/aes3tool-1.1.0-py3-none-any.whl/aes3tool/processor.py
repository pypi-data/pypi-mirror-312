##################################################
## SMPTE 2110-3x AES3 PCM testing toolkit       ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

from abc import ABC, abstractmethod
import asyncio
from .config import Aes3ToolConfig
from .const import VERSION
from .network import ConnectionBase
import time

class Aes3Processor(ABC):
    def __init__(self, config:Aes3ToolConfig) -> None:
        self._config = config
        self._stop = False
        self.last_join = time.time()

    @property
    def config(self) -> Aes3ToolConfig:
        return self._config

    @property
    def version(self) -> str:
        return VERSION

    @abstractmethod
    async def start(self) -> None:
        ''' coroutine that runs the processor '''

    async def close(self) -> None:
        ''' close the processor '''
        self._stop = True

    @property
    def stopping(self) -> bool:
        return self._stop

    @abstractmethod
    def read_counters(self) -> tuple[int, int, int]:
        ''' returns read/write counters since the last call: (bytes, frames, samples) '''

    @property
    @abstractmethod
    def connection(self) -> ConnectionBase:
        pass

    async def check_reset_igmp(self) -> None:
        if (self.config.reset_igmp_seconds > 0):
            while not self.stopping:
                now = time.time()
                if ((now - self.last_join) >= self.config.reset_igmp_seconds):
                    self.connection.reset_igmp()
                    self.last_join = now
                await asyncio.sleep(1)

    @abstractmethod
    def __str__(self) -> str:
        ''' description for this processor '''

    def __repr__(self) -> str:
        return str(self)
