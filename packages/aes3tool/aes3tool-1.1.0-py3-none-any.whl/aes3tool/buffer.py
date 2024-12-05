##################################################
## SMPTE 2110-3x AES3 PCM testing toolkit       ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

from .const import AUDIO_BUFFER_SIZE_SECONDS
from .data import Am824Frame
import threading

class ReceiverAudioBuffer:
    def __init__(self):
        self.size = (48000 * 3 * AUDIO_BUFFER_SIZE_SECONDS)
        self.data = bytearray(self.size)
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self.flush()

    @property
    def empty(self) -> bool:
        with self._lock:
            return (self._read_pos == self._write_pos)

    def flush(self) -> None:
        self._write_pos = 0
        self._read_pos = 0
        self._len = 0
        self._signal_level = 0

    def push_bytes(self, value:bytes, size:int) -> bool:
        with self._condition:
            if ((self._len + size) > self.size) or (size > self.size):
                return False
            remaining = (self.size - self._write_pos)
            write1 = min(size, remaining)
            self.data[self._write_pos:self._write_pos + write1] = value[0:write1]
            if write1 < size:
                self._write_pos = size - write1
                self.data[0:size - write1] = value[write1:]
            else:
                self._write_pos = (self._write_pos + size) % self.size

            self._len += size
            if (self._signal_level != 0) and (self._len >= self._signal_level):
                self._condition.notify()
        return True

    def push(self, value: Am824Frame) -> bool:
        return self.push_bytes(value.audio_sample, 3)

    def pop(self, size:int, wait:bool=False) -> bytearray:
        with self._condition:
            # not enough data available in the buffer
            if (self._len < size):
                if wait:
                    self._signal_level = size
                    if not self._condition.wait(timeout=0.1):
                        self._signal_level = 0
                        return None
                    self._signal_level = 0
                else:
                    return None
            first = min(self.size - self._read_pos, size)
            if first < size:
                # copy
                rv = self.data[self._read_pos:self._read_pos + first] + self.data[0:(size - first)]
                self._read_pos = (size - first)
            else:
                # no-copy
                rv = memoryview(self.data[self._read_pos:self._read_pos + first])
                self._read_pos = (self._read_pos + size)
            self._len -= size
        return rv

    def __len__(self) -> int:
        with self._lock:
            return self._len