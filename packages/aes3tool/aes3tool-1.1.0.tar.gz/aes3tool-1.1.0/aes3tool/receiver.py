##################################################
## SMPTE 2110-3x AES3 PCM testing toolkit       ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

import asyncio
from .bitstream import BitStream, BitStreamReader, BitStreamInfo
from .config import Aes3ToolConfig
from .const import *
from .data import RtpPacket, Am824Frame, Aes3Frame, Aes3ExtraData
import logging
from .network import ConnectionBase, ConnectionThread, ConnectionAsync
from .output import ReceiverOutput, ReceiverOutputSound, ReceiverOutputWav, ReceiverOutputStreamDump
from .processor import Aes3Processor
from .stats import Aes3ProcessorStats
import time

# log output
_LOGGER = logging.getLogger(__name__)

class TerminateTasks(Exception):
    '''terminate background tasks'''

class Aes3Timing:
    _nb_frames = 0
    _start_time = 0
    _timing = 0
    _nb_samples = 0

    def reset(self) -> None:
        self._have_timing = False
        self._nb_frames = 0
        self._start_time = 0

    def on_packet(self, frame:'Aes3Frame') -> bool:
        nb_samples = frame.nb_sub_frames
        if (self._timing != 0):
            return True
        if (self._nb_frames == 0):
            self._start_time = (time.time() *  1000)
            self._nb_samples = nb_samples
            # _LOGGER.info(f"new detect start, nb_samples {nb_samples}, size {size}")
        elif (self._nb_samples != nb_samples):
            # invalid
            _LOGGER.info(f"different nb sample: {self._nb_samples} != {nb_samples}")
            return False
        self._nb_frames += 1
        # _LOGGER.info(f"frame {self._nb_frames}")
        if self._nb_frames == 192:
            # full block
            self._timing = (((time.time() * 1000) - self._start_time) / (self._nb_frames * nb_samples))
            # XXX
            self._timing *= 2
            _LOGGER.info(f'full block, diff = {((time.time() * 1000) - self._start_time)} samples = {self._nb_frames * nb_samples} timing = {self._timing} rate {int(1.0 / self._timing)} -> {self.rate}')
            if self.rate == 0:
                #invalid
                self.reset()
                return False
        return True

    @property
    def rate(self) -> int:
        if (self._timing == 0):
            return 0
        rate = 1.0 / self._timing
        if (rate >= 7) and (rate <= 9):
            return 8000
        if (rate >= 10) and (rate <= 12):
            return 11025
        if (rate >= 20) and (rate <= 24):
            return 22050
        if (rate >= 30) and (rate <= 34):
            return 32000
        if (rate >= 42) and (rate < 46):
            return 44100
        if (rate >= 46) and (rate <= 50):
            return 48000
        if (rate >= 92) and (rate <= 100):
            return 96000
        return 0

    @property
    def timing(self) -> int:
        return self._timing

class Aes3Receiver(Aes3Processor):
    _output:ReceiverOutput = None
    _stats = Aes3ProcessorStats()
    _started = False
    _last_rtp_packet:RtpPacket = None
    _user_data = Aes3ExtraData("user")
    _channel_data = Aes3ExtraData("channel")
    last_join = time.time()
    _timing = Aes3Timing()
    _bitstream_processor = BitStreamReader()
    _bitstream_info:BitStreamInfo = None
    _exit = False

    ''' AES3 audio receiver '''
    def __init__(self, config:Aes3ToolConfig, source_ip:str, interface_ip:str, capture_file:str=None, threaded:bool=False) -> None:
        Aes3Processor.__init__(self, config=config)
        self._bitstream = BitStream(demux_callback=self._demux_bitstream)
        if capture_file is None:
            self._output = ReceiverOutputSound(config=config, underrun_callback=self._on_underrun)
        else:
            self._output = ReceiverOutputWav(config=config, path=capture_file)
        # self._output = ReceiverOutputStreamDump(config=config, path='/tmp/dump.bin')
        self.threaded = threaded
        if self.threaded:
            self._connection = ConnectionThread(callback=self, ip=source_ip, port=config.audio_source_port, listen_if=interface_ip)
        else:
            self._connection = ConnectionAsync(callback=self, ip=source_ip, port=config.audio_source_port, listen_if=interface_ip)

    def _demux_bitstream(self, data:bytes) -> None:
        info = self._bitstream_processor.on_packet(data=data)
        if (info is None):
            if (self._bitstream_info is not None):
                _LOGGER.debug(f'lost {self._bitstream_info.name} stream')
            self._bitstream_info = info
        elif (self._bitstream_info is None) or (self._bitstream_info != info):
            self._bitstream_info = info
            _LOGGER.debug(f'detected {info.name}: bit rate = {info.bit_rate}, sample rate = {info.sample_rate}, channels = {info.channels}')
            # TODO

    @property
    def connection(self) -> ConnectionBase:
        return self._connection

    def _on_underrun(self) -> None:
        self._stats.increase_underruns()

    def _on_invalid_packet(self) -> None:
        self._timing.reset()
        self._started = False # wait for a new block start

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        self._stats.increase_values(vsamples=0, vframes=1, vbytes=(len(data) + 42)) # ethernet header size
        rtp_packet = RtpPacket(data=data)
        if (rtp_packet.payload_type != self.config.rtp_payload_type):
            # ignore other types/data
            _LOGGER.debug(f"invalid payload type {rtp_packet.payload_type}")
            return

        # check for sequence errors
        last_rtp_packet = self._last_rtp_packet
        self._last_rtp_packet = rtp_packet
        if (last_rtp_packet is not None):
            if not rtp_packet.check_sequence(previous=last_rtp_packet):
                self._stats.increase_sequence_errors()
                self._on_invalid_packet()
                return

        frame = rtp_packet.aes3_payload
        if frame is None:
            _LOGGER.warning(f"invalid rtp packet received: {rtp_packet}")
            return

        if not self._started:
            # wait for block start
            bs = frame.block_start
            if len(bs) == 0:
                return

            self._started = True
            write_value = b''.join([f.audio_sample for f in bs])
            write_len = len(write_value)
        else:
            # use all frames
            write_value = frame.sub_frame_samples
            write_len = len(frame)
        if not self._timing.on_packet(frame=frame):
            # invalid size, reset
            self._on_invalid_packet()
            return

        # TODO
        # frame.push_user_data(self._user_data)
        # frame.push_channel_data(self._channel_data)

        if (self._timing.rate == 0):
            self._bitstream.reset()
            self._output.pause_stream()
        else:
            # check for bitstreams
            if self.config.detect_bitstreams:
                self._bitstream.write(value=memoryview(write_value), len=write_len)
            if self.config.detect_bitstreams and (self._bitstream.bit_depth != 0):
                # bitstream detected. we can't output these atm
                self._output.pause_stream()
                # TODO
                if (self._bitstream_info is None):
                    self._stats.set_output_codec('ST337', 0)
                    self._stats.increase_samples(value=frame.nb_sub_frames, sample_rate=round(self._timing.rate / 1000), audio_channels=0)
                else:
                    self._stats.set_output_codec(self._bitstream_info.name, self._bitstream_info.bit_rate)
                    self._stats.increase_samples(value=frame.nb_sub_frames, sample_rate=self._bitstream_info.sample_rate, audio_channels=self._bitstream_info.channels)
            else:
                # write to the buffer
                self._stats.set_output_codec('PCM', 0)
                if not self._output.write_bytes(value=memoryview(write_value), size=write_len, sample_rate=self._timing.rate, audio_channels=2, sample_width=self.config.audio_sample_width):
                    self._on_invalid_packet()
                else:
                    self._stats.increase_samples(value=frame.nb_sub_frames, sample_rate=self._timing.rate, audio_channels=2)

    def read_counters(self) -> tuple[int, int, int]:
        return self._stats.read()

    def _on_stats_callback(self, kbytes_read:int, frames_read:int, samples_read:int, underruns:int, sequence_errors:int, codec:str, codec_rate:int, sample_rate:int, audio_channels:int) -> None:
        if (frames_read == 0):
            self._output.pause_stream()
        if (self.config.stats_callback is not None):
            self.config.stats_callback(kbytes_read, frames_read, samples_read, underruns, sequence_errors, codec, codec_rate, sample_rate, audio_channels)

    async def start(self, threaded:bool=False) -> None:
        if self.threaded:
            self._connection.start_srv()
        try:
            async with asyncio.TaskGroup() as tg:
                if not self.threaded:
                    tg.create_task(self._connection.start_srv_async())
                tg.create_task(self._check_exit())
                tg.create_task(self._bitstream.start())
                tg.create_task(self.check_reset_igmp())
                tg.create_task(self._stats.stats_reader(callback=self._on_stats_callback, sample_width=self.config.audio_sample_width))
        except Exception:
            return
        finally:
            self._exit = False

    async def _check_exit(self):
        while not self._exit:
            await asyncio.sleep(0.1)
        raise TerminateTasks()

    async def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
        self._output.close()
        self._bitstream.stop()
        await Aes3Processor.close(self)
        self._exit = True
        while self._exit:
            await asyncio.sleep(0.1)

    def __str__(self) -> str:
        return f"AES3 Receiver [source={str(self.connection)}, output={self._output.name}]"
