##################################################
## SMPTE 2110-3x AES3 PCM testing toolkit       ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

from abc import ABC, abstractmethod
from .buffer import ReceiverAudioBuffer
from .config import Aes3ToolConfig
from .const import *
from .data import Am824Frame
import logging
import pyaudio
import threading
import wave
import time

# log output
_LOGGER = logging.getLogger(__name__)

AUDIO_QUEUE = ReceiverAudioBuffer()
_underrun_callback:callable = None

def _audio_output_callback(in_data, frame_count, time_info, status_flags):
    ''' audio output callback to read data, called by pyAudio '''
    rv = AUDIO_QUEUE.pop(size=frame_count * 6, wait=True) # frame = (left + right) * 24 bits
    if rv is None:
        if _underrun_callback is not None:
            _underrun_callback()
        return (bytes(bytearray(frame_count * 6)), pyaudio.paContinue)
    return (bytes(rv), pyaudio.paContinue)

class ReceiverOutput(ABC):
    def __init__(self, config:Aes3ToolConfig) -> None:
        self.config = config

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def write_bytes(self, value:bytes, size:int, sample_rate:int, audio_channels:int, sample_width:int) -> bool:
        pass

    def pause_stream(self) -> None:
        pass

    def on_frame_failed(self) -> None:
        pass

class ReceiverOutputSound(ReceiverOutput):
    _stream_sample_rate = 0
    _stream_nb_channels = 0
    _stream_width = 0
    _started = False
    _stream = None

    ''' send capture audio to the default audio output '''
    def __init__(self, config:Aes3ToolConfig, blocking:bool=False, underrun_callback:callable=None) -> None:
        global _underrun_callback
        ReceiverOutput.__init__(self, config=config)
        self._audio = pyaudio.PyAudio()
        self._blocking = blocking
        _underrun_callback = underrun_callback
        self._writer_thread:threading.Thread = None
        self._start_time = None
        self._open_stream(sample_rate=config.audio_sample_rate, audio_channels=config.audio_channels, sample_width=config.audio_sample_width)

    def __del__(self) -> None:
        self.close()

    @property
    def name(self) -> str:
        return "soundcard"

    def close(self) -> None:
        self._started = False
        if (self._stream is not None):
            _LOGGER.debug('closing audio output')
            self._stream.close()
            self._stream = None
        if (self._writer_thread is not None):
            self._writer_thread.join()
            self._writer_thread = None

    def _audio_writer_thread(self) -> None:
        self._stream.start_stream()
        while self._started:
            framebuffer = bytes()
            cnt = 2000
            while cnt >= 0:
                frame:Am824Frame = AUDIO_QUEUE.pop()
                if frame is not None:
                    framebuffer += frame.audio_sample
                    cnt -= 1
            self._stream.write(frames=bytes(framebuffer), num_frames=2000)
        AUDIO_QUEUE.flush()

    def _should_start(self) -> bool:
        return not self._started and (len(AUDIO_QUEUE) >= self.config.audio_min_queue_level)

    def _open_stream(self, sample_rate:int, audio_channels:int, sample_width:int) -> bool:
        if  (self._stream is not None) and \
                (self._stream_sample_rate == sample_rate) and \
                (self._stream_nb_channels == audio_channels) and \
                (self._stream_width == sample_width):
            return True
        _LOGGER.debug(f"open stream rate {sample_rate} channels {audio_channels} width {sample_width}")
        if (self._stream is not None):
            self._stream.close()
        self._stream = self._audio.open(rate=sample_rate,
                                        channels=audio_channels,
                                        format=pyaudio.get_format_from_width(sample_width),
                                        output=True,
                                        start=False,
                                        frames_per_buffer=1024,
                                        stream_callback=(_audio_output_callback if not self._blocking else None))
        if (self._stream is not None):
            self._stream_sample_rate = sample_rate
            self._stream_nb_channels = audio_channels
            self._stream_width = sample_width
            return True
        return False

    def on_frame_failed(self) -> None:
        # reset output?
        pass

    def pause_stream(self) -> None:
        if (self._stream is not None):
            self._stream.stop_stream()
            self._stream = None

    def write_bytes(self, value:bytes, size:int, sample_rate:int, audio_channels:int, sample_width:int) -> bool:
        # pass to the audio output
        if not self._open_stream(sample_rate=sample_rate, audio_channels=audio_channels, sample_width=sample_width):
            # failed to open output
            return False
        if self._start_time is None:
            self._start_time = time.time()
        AUDIO_QUEUE.push_bytes(value=value, size=size)

        if self._should_start():
            # start streaming when we've reached the minimum buffer level
            _LOGGER.debug(f'starting audio output, buffer level = {len(AUDIO_QUEUE)} bytes, {round(time.time() - self._start_time, 1)} seconds spent buffering')
            self._started = True
            if not self._blocking:
                self._stream.start_stream()
            else:
                self._writer_thread = threading.Thread(target=self._audio_writer_thread)
                self._writer_thread.start()
        return True

class ReceiverOutputWav(ReceiverOutput):
    ''' wave file output '''
    def __init__(self, config:Aes3ToolConfig, path:str) -> None:
        self._path = path
        self._file = None

    @property
    def name(self) -> str:
        return f"wav({self._path})"

    def close(self) -> None:
        _LOGGER.debug('closing wav output')
        self._file.close()
        self._file = None

    def write_bytes(self, value:bytes, size:int, sample_rate:int, audio_channels:int, sample_width:int) -> bool:
        if self._file is None:
            self._file = wave.open(self._path, 'wb')
            self._file.setframerate(sample_rate)
            self._file.setnchannels(audio_channels)
            self._file.setsampwidth(sample_width)
        self._file.writeframes(value)
        return True

class ReceiverOutputStreamDump(ReceiverOutput):
    ''' stream dump file output '''
    def __init__(self, config:Aes3ToolConfig, path:str) -> None:
        self._path = path
        self._file = open(path, 'wb')

    @property
    def name(self) -> str:
        return f"wav({self._path})"

    def close(self) -> None:
        _LOGGER.debug('closing wav output')
        self._file.close()
        self._file = None

    def write_bytes(self, value:bytes, size:int, sample_rate:int, audio_channels:int, sample_width:int) -> bool:
        self._file.write(value)
        return True
