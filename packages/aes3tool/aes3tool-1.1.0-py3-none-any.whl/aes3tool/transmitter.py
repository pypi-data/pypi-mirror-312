##################################################
## SMPTE 2110-3x AES3 PCM testing toolkit       ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

import asyncio
from abc import ABC, abstractmethod
from .config import Aes3ToolConfig
from .const import *
from .data import RtpPacket, Am824Frame, Aes3Frame
import logging
from .network import ConnectionBase, ConnectionAsync, ConnectionThread
import numpy as np
from .processor import Aes3Processor
from .stats import Aes3ProcessorStats
import pyaudio
from pydub import AudioSegment
import resampy
import signal
import threading
import time

# log output
_LOGGER = logging.getLogger(__name__)

class TerminateTasks(Exception):
    '''terminate background tasks'''

class Aes3TxBuffer(ABC):
    _bs_counter = 0
    _sequence = 0xFFFF
    _rtp_packets:asyncio.Queue[RtpPacket] = asyncio.Queue()

    def __init__(self, rtp_payload_type:int) -> None:
        self._rtp_payload_type = rtp_payload_type

    @abstractmethod
    def prepared(self) -> bool:
        pass

    def qsize(self) -> int:
        return self._rtp_packets.qsize()

    def get(self) -> RtpPacket:
        return self._rtp_packets.get_nowait()

    def construct_rtp(self, data:bytes|memoryview, sample_width:int) -> RtpPacket:
        aes_frame = Aes3Frame(data=bytes([]))
        # 6 stereo frames per rtp packet
        for ptr in range(STEREO_SAMPLES_PER_PACKET):
            try:
                aes_frame.append(Am824Frame.construct(audio=data[(ptr * sample_width * 2):], block_start=(self._bs_counter == 0), frame_start=True))
                aes_frame.append(Am824Frame.construct(audio=data[(ptr * sample_width * 2) + sample_width:]))
                self._bs_counter += 2
                if self._bs_counter >= AES3_SUBFRAMES_PER_BLOCK:
                    self._bs_counter -= AES3_SUBFRAMES_PER_BLOCK
            except Exception as e:
                _LOGGER.warning(f"failed to construct frame: {e}")
                return None
        self._sequence = ((self._sequence + 1) & 0xFFFF)
        return RtpPacket.construct(type=self._rtp_payload_type, sequence=self._sequence, frame=aes_frame)

class Aes3TxBufferFile(Aes3TxBuffer, threading.Thread):
    ''' AES3 audio transmit buffer '''
    def __init__(self, config:Aes3ToolConfig, source_file:str) -> None:
        threading.Thread.__init__(self)
        Aes3TxBuffer.__init__(self, rtp_payload_type=config.rtp_payload_type)
        self._config = config
        self._source_file = source_file
        self._data_read = False
        self._prepared = False
        self._stop_process = False
        self.seek_start()

    @property
    def prepared(self) -> bool:
        return self._prepared

    def read_and_resample(self):
        if self._data_read:
            return
        _LOGGER.debug(f"reading data from {self._source_file}")
        data = AudioSegment.from_file(self._source_file)
        self._data = np.array(data.get_array_of_samples())
        self._frame_rate = data.frame_rate
        if data.channels == 2:
            # reshape stereo
            self._data = self._data.reshape((-1, 2))

        # boost volume by 6dB
        self._data += 6

        # resample to the output rate
        if self._frame_rate != self._config.audio_sample_rate:
            _LOGGER.debug(f"resampling audio from {self._frame_rate} to {self._config.audio_sample_rate}")
            self._data = resampy.resample(self._data, self._frame_rate, self._config.audio_sample_rate)
            self._frame_rate = self._config.audio_sample_rate

        _LOGGER.debug(f"rate = {self._frame_rate}, type = {str(self._data.dtype)}, samples = {str(len(self._data))}")
        self._data_read = True

    def run(self):
        start = time.time()
        self.read_and_resample()
        self.seek_start()
        while not self._stop_process:
            try:
                data = []
                for _ in range(6):
                    data.append(self._data[self._read_pointer][0])
                    data.append(self._data[self._read_pointer][1])
                    self._read_pointer += 1
                pkt = self.construct_rtp(data=data)
                if pkt is None:
                    self._prepared = True
                    _LOGGER.debug(f"finished buffering rtp data in {int(time.time() - start)} seconds. {self._rtp_packets.qsize()} rtp packets buffered")
                    return
                self._rtp_packets.put_nowait(pkt)
                time.sleep(0)
            except Exception as e:
                _LOGGER.warning("failed to prepare data")
                raise e

    def close(self) -> None:
        self._stop_process = True
        self.join()
 
    def seek_start(self):
        self._read_pointer = 0

class Aes3TxBufferLive(Aes3TxBuffer):
    _lock = threading.Lock()
    _stop_event = threading.Event()
    _sample_width = 3

    def __init__(self, config:Aes3ToolConfig) -> None:
        Aes3TxBuffer.__init__(self, config.rtp_payload_type)
        self._condition = threading.Condition(self._lock)
        self._signal_level = -1
        self.audio = pyaudio.PyAudio()
        default_input = self.audio.get_default_input_device_info()
        self.in_stream = self.audio.open(format=pyaudio.paInt24,
                                     channels=2,
                                     rate=config.audio_sample_rate,
                                     input_device_index=default_input["index"],
                                     input=True)

    def __del__(self) -> None:
        self.close()

    @property
    def prepared(self) -> bool:
        return (self.in_stream is not None)

    def close(self) -> None:
        if self._stop_event.is_set():
            return
        self._stop_event.set()
        try:
            self.audio.close(self.in_stream)
        except:
            pass

    def wait_for_level(self, level:int, timeout:float|None=None) -> None:
        with self._lock:
            self._signal_level = level
            self._condition.wait(timeout=timeout)

    def _record(self) -> None:
        while not self._stop_event.is_set():
            try:
                nb_frames = int(self.in_stream.get_read_available() / STEREO_SAMPLES_PER_PACKET)
                if (nb_frames == 0):
                    continue
                data = self.in_stream.read(nb_frames * STEREO_SAMPLES_PER_PACKET)
                assert((nb_frames * STEREO_SAMPLES_PER_PACKET * self._sample_width * 2) == len(data))
                for idx in range(nb_frames):
                    pkt = self.construct_rtp(data=data[idx * STEREO_SAMPLES_PER_PACKET * self._sample_width * 2:], sample_width=3)
                    if pkt is None:
                        _LOGGER.info("NO MORE DATA")
                        return
                    self._rtp_packets.put_nowait(pkt)
                with self._lock:
                    if (self._signal_level > 0) and (self._rtp_packets.qsize() >= self._signal_level):
                        self._condition.notify()
            except Exception:
                raise

    def start(self) -> None:
        self.t = threading.Thread(target=self._record)
        self.t.start()

class Aes3Transmitter(Aes3Processor):
    ''' AES3 audio transmitter '''
    def __init__(self, config:Aes3ToolConfig, target_ip:str, interface_ip:str, source_file:str|None=None, threaded:bool=False) -> None:
        Aes3Processor.__init__(self, config=config)
        self._source_file = source_file
        self.threaded = threaded
        if self.threaded:
            self._connection = ConnectionThread(callback=self, ip=target_ip, port=config.audio_source_port, listen_if=interface_ip)
        else:
            self._connection = ConnectionAsync(callback=self, ip=target_ip, port=config.audio_source_port, listen_if=interface_ip)
        if (source_file is not None):
            self._buffer = Aes3TxBufferFile(config=config, source_file=source_file)
        else:
            self._buffer = Aes3TxBufferLive(config=config)
        self._stats = Aes3ProcessorStats()

    @property
    def connection(self) -> ConnectionBase:
        return self._connection

    def transmit(self, pkt:RtpPacket) -> None:
        data = pkt.data
        self._stats.increase_values(vsamples=12, vframes=1, vbytes=(len(data) + 42))
        self.connection.transmit(data=data)

    async def stream(self) -> None:
        if self.config.tx_buffer_samples < 0:
            while not self._buffer.prepared:
                await asyncio.sleep(0)
        elif TX_BUFFER_FRAMES > 0:
            self._buffer.wait_for_level(level=self.config.tx_buffer_samples)
            _LOGGER.info(f"waited, queue size {self._buffer.qsize()}")

        # open the tx socket
        await self.connection.start_tx_async()

        sig_rate = (1.0 / (self.config.audio_sample_rate / STEREO_SAMPLES_PER_PACKET))
        next = time.time()
        while not self._stop:
            next += sig_rate
            try:
                self.transmit(pkt=self._buffer.get())
                wait = next - time.time()
                if wait > 0:
                    await asyncio.sleep(wait)
            except:
                _LOGGER.warning(f"QUEUE EMPTY")
                self._buffer.wait_for_level(level=self.config.tx_buffer_samples)
                next = time.time()

    def _on_stats_callback(self, kbytes_read:int, frames_read:int, samples_read:int, underruns:int, sequence_errors:int, codec:str, codec_rate:int, sample_rate:int, audio_channels:int) -> None:
        _LOGGER.debug(f"TX stats: {kbytes_read}KB/s underruns={underruns}")
        if (self.config.stats_callback is not None):
            self.config.stats_callback(kbytes_read, frames_read, samples_read, underruns, sequence_errors, codec, codec_rate, sample_rate, audio_channels)

    async def _check_exit(self):
        while not self._stop:
            await asyncio.sleep(0.1)
        raise TerminateTasks()

    async def start(self) -> None:
        _LOGGER.debug("transmitter starting")
        self._buffer.start()
        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(self._check_exit())
                tg.create_task(self.stream())
                tg.create_task(self.check_reset_igmp())
                tg.create_task(self._stats.stats_reader(callback=self._on_stats_callback, sample_width=self.config.audio_sample_width))
        except:
            return
        finally:
            self._stop = False

    def read_counters(self) -> tuple[int, int, int, int, int]:
        return self._stats.read()

    async def close(self) -> None:
        self._stop = True
        if self._connection is not None:
            self._connection.close()
        self._buffer.close()
        await Aes3Processor.close(self)
        _LOGGER.debug("transmitter exited")

    def __str__(self) -> str:
        return f"AES3 Transmitter (source={self._source_file})"
