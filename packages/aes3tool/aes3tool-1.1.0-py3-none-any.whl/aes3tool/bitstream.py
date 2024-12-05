import asyncio
import logging
from abc import ABC, abstractmethod
import time
import threading

_LOGGER = logging.getLogger(__name__)

class BitStreamDump:
    def __init__(self, path:str) -> None:
        self._file = open(path, 'wb')

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        self._file.close()

    def on_packet(self, data:bytes) -> None:
        self._file.write(data)

class ShiftBuffer:
    _buf:bytes = None
    def __init__(self, size:int) -> None:
        self._size = size

    def push(self, value:bytes) -> bytes:
        if self._buf is None:
            self._buf = value
        else:
            self._buf = self._buf[(-1) * (self._size - 1):] + value
        return self._buf

class BitStreamInfo:
    def __init__(self, name:str, magic:bytes) -> None:
        self.name = name
        self.magic = magic
        self.magic_len = len(magic)

    name:str = 'Unknown'
    sample_rate:int = 0
    frame_size:int = 0
    bit_rate:int = 0
    channels:int = 0
    mode:str = ''

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BitStreamInfo):
            return False
        return (self.name == value.name) and \
            (self.sample_rate == value.sample_rate) and \
            (self.frame_size == value.frame_size) and \
            (self.bit_rate == value.bit_rate) and \
            (self.channels == value.channels) and \
            (self.mode == value.mode)

class BitStreamProcessor(ABC):
    def __init__(self, name:str, magic:bytes) -> None:
        self._info = BitStreamInfo(name=name, magic=magic)

    @property
    def info(self) -> BitStreamInfo:
        return self._info

    def check_magic(self, buf:bytes, size:int, check_size:int) -> bool:
        info = self.info
        for ptr in range(check_size):
            if (info.magic_len + ptr + 8) <= size:
                if (buf[ptr:ptr+info.magic_len] == info.magic):
                    # _LOGGER.debug(f"found {info.name} header")
                    return self.process(buf[ptr:size])
        return False

    def process(self, buf:bytes) -> bool:
        pass

class BitStreamProcessorAC3(BitStreamProcessor):
    def __init__(self) -> None:
        BitStreamProcessor.__init__(self, name='AC3', magic=bytes([0x0B, 0x77]))

    def process(self, buf:bytes) -> bool:
        sync_code = buf[4]
        fscod = ((sync_code >> 6) & 0x03)
        sample_rate = self.SAMPLE_RATES[fscod]
        if (sample_rate is None):
            # invalid/reserved
            return False

        frame_size_entry = (sync_code & 0x3F)
        if (frame_size_entry >= len(self.FRAME_SIZES)):
            # out of range
            return False

        bsmod = buf[5] & 0x7
        if (bsmod >= len(self.BITSTREAM_MODES)):
            # out of range
            return False

        acmod = (buf[6] >> 5) & 0x7
        self.info.channels = self.CHANNEL_MODES[acmod][0]
        ch_bits = 0
        if ((acmod & 0x01) and not (acmod == 0x01)):
            # 3 front channels (cmixlev)
            ch_bits += 2
        if (acmod & 0x04):
            # surround channel exists (surmixlev)
            ch_bits += 4
        if (acmod == 0x02):
            # 2/0 mode (dsurmod)
            ch_bits += 2

        ch_info = (((buf[6] & 0x1F) << 8) + buf[7])
        if ((ch_info >> (12 - ch_bits)) & 0x01):
            # LFE channel present
            self.info.channels += 1

        frame_size_entry = self.FRAME_SIZES[frame_size_entry]
        self._info.sample_rate = sample_rate
        self._info.frame_size = frame_size_entry[1][fscod]
        self._info.bit_rate = frame_size_entry[0]
        self._info.mode = self.BITSTREAM_MODES[bsmod]
        return True

    SAMPLE_RATES = [
        48000,
        44100,
        32000,
        None,
    ]

    FRAME_SIZES = [
        ( 32, (  64,   69,   96)),
        ( 32, (  64,   70,   96)),
        ( 40, (  80,   87,  120)),
        ( 40, (  80,   88,  120)),
        ( 48, (  96,  104,  144)),
        ( 48, (  96,  105,  144)),
        ( 56, ( 112,  121,  168)),
        ( 56, ( 112,  122,  168)),
        ( 64, ( 128,  139,  192)),
        ( 64, ( 128,  140,  192)),
        ( 80, ( 160,  174,  240)),
        ( 80, ( 160,  175,  240)),
        ( 96, ( 192,  208,  288)),
        ( 96, ( 192,  209,  288)),
        (112, ( 224,  243,  336)),
        (112, ( 224,  244,  336)),
        (128, ( 256,  278,  384)),
        (128, ( 256,  279,  384)),
        (160, ( 320,  348,  480)),
        (160, ( 320,  349,  480)),
        (192, ( 384,  417,  576)),
        (192, ( 384,  418,  576)),
        (224, ( 448,  487,  672)),
        (224, ( 448,  488,  672)),
        (256, ( 512,  557,  768)),
        (256, ( 512,  558,  768)),
        (320, ( 640,  696,  960)),
        (320, ( 640,  697,  960)),
        (384, ( 768,  835, 1152)),
        (384, ( 768,  836, 1152)),
        (448, ( 896,  975, 1344)),
        (448, ( 896,  976, 1344)),
        (512, (1024, 1114, 1536)),
        (512, (1024, 1115, 1536)),
        (576, (1152, 1253, 1728)),
        (576, (1152, 1254, 1728)),
        (640, (1280, 1393, 1920)),
        (640, (1280, 1394, 1920)),
    ]

    BITSTREAM_MODES = [
        "complete main",
        "music and effects",
        "visually impaired",
        "hearing impaired",
        "dialogue",
        "commentary",
        "emergency",
        "other"
    ]

    CHANNEL_MODES = [
        (2, "2CH"),
        (1, "C"),
        (2, "L+R"),
        (3, "L+C+R"),
        (3, "L+R+S"),
        (4, "L+C+R+S"),
        (4, "L+R+SL+SR"),
        (5, "L+C+R+SL+SR")
    ]

class BitStreamProcessorDTS(BitStreamProcessor):
    def __init__(self) -> None:
        BitStreamProcessor.__init__(self, name='DTS', magic=bytes([0x7F, 0xFE, 0x80, 0x01]))

    def process(self, buf:bytes) -> bool:
        # TODO
        return False

class BitStreamReader:
    _stream_type = None
    _buf = ShiftBuffer(32)
    _processors:list[BitStreamProcessor] = []

    def __init__(self) -> None:
        self._processors = [
            BitStreamProcessorAC3(),
            BitStreamProcessorDTS(),
        ]

    def on_packet(self, data:bytes) -> BitStreamInfo:
        current = self._buf.push(data)
        current_len = len(current)
        new_len = len(data)
        for processor in self._processors:
            if processor.check_magic(buf=current, size=current_len, check_size=new_len):
                self._stream_type = processor.info
                break
        return self._stream_type

class BitStream:
    '''bitstream processing for LE sources. demux for 24 bit containers'''
    _current = bytes([])
    _bit_depth = 0
    _stream_bits = 0
    _bytes_buf = []
    _bytes_buf_20 = False
    _detect_time = 0
    _run = True
    _lock = threading.Lock()
    _event = asyncio.Event()

    def __init__(self, demux_callback:callable=None) -> None:
        self._demux_callback = demux_callback

    def _reset_demux(self):
        self._bytes_buf = []

    def _demux(self, value:int) -> bytes|None:
        self._bytes_buf.append(value)
        _bytes_pos = len(self._bytes_buf)
        buf = None

        if (_bytes_pos == 3) and self._bytes_buf_20:
            self._bytes_buf_20 = False
            buf = bytearray([
                self._bytes_buf[2],
                self._bytes_buf[1],
                (self._bytes_buf[0] & 0xF0) | (self._bytes_buf[5] >> 4),
            ])
            self._reset_demux()
        elif (_bytes_pos == 6):
            if (self._stream_bits == 24):
                buf = bytearray([
                    self._bytes_buf[2],
                    self._bytes_buf[1],
                    self._bytes_buf[0],
                    self._bytes_buf[5],
                    self._bytes_buf[4],
                    self._bytes_buf[3],
                ])
            elif (self._stream_bits == 20):
                self._bytes_buf_20 = True
                buf = bytearray([
                    self._bytes_buf[2],
                    self._bytes_buf[1],
                    (self._bytes_buf[0] & 0xF0) | (self._bytes_buf[5] >> 4),
                    (self._bytes_buf[5] << 4) | (self._bytes_buf[4] >> 4),
                    (self._bytes_buf[4] << 4) | (self._bytes_buf[3] >> 4),
                    self._bytes_buf[3],
                ])
            elif (self._stream_bits == 16):
                buf = bytearray([
                    self._bytes_buf[2],
                    self._bytes_buf[1],
                    self._bytes_buf[5],
                    self._bytes_buf[4],
                ])
            self._reset_demux()
        if (buf is not None) and (self._demux_callback is not None):
            if isinstance(self._demux_callback, list):
                for cb in self._demux_callback:
                    cb(buf)
            else:
                self._demux_callback(buf)
        return buf

    MAGIC = [
        ((32, 24), bytes([0x00, 0x72, 0xF8, 0x96, 0x00, 0x1F, 0x4E, 0xA5])),
        ((32, 20), bytes([0x00, 0x20, 0x87, 0x6F, 0x00, 0xF0, 0xE1, 0x54])),
        ((32, 16), bytes([0x00, 0x00, 0x72, 0xF8, 0x00, 0x00, 0x1F, 0x4E])),
        ((24, 24), bytes([0x72, 0xF8, 0x96, 0x1F, 0x4E, 0xA5])),
        ((24, 20), bytes([0x20, 0x87, 0x6F, 0xF0, 0xE1, 0x54])),
        ((24, 16), bytes([0x00, 0x72, 0xF8, 0x00, 0x1F, 0x4E])),
        ((32, 24), bytes([0x72, 0xF8, 0xF6, 0xE1, 0x54])),
        ((32, 24), bytes([0x72, 0xF8, 0x1F, 0x4E])),
    ]
    def _find_magic(self) -> tuple[int, int]:
        with self._lock:
            current = self._current
        for cfg, magic in self.MAGIC:
            if (current.find(magic) != -1):
                return cfg
        return (0, 0)

    def _demux_bytes(self, value:bytes) -> None:
        if (self._bit_depth == 24):
            # we only support 24 bits containers atm
            for b in value:
                self._demux(value=b)

    def write(self, value:bytes, len:int) -> bool:
        with self._lock:
            self._current = self._current[-8:] + value
        self._event.set()

        if (self._bit_depth != 0):
            # this is a bitstream
            self._demux_bytes(value=value)
            return True

        return False

    @property
    def bit_depth(self) -> int:
        with self._lock:
            return self._bit_depth

    def _check_magic(self) -> None:
        (bit_depth, stream_bits) = self._find_magic()
        if (bit_depth != 0) and (stream_bits != 0):
            if (self._bit_depth != bit_depth) or (self._stream_bits != stream_bits):
                _LOGGER.debug(f'detected st337: bit depth = {bit_depth} stream bits = {stream_bits}')
            self._bit_depth = bit_depth
            self._stream_bits = stream_bits
            self._detect_time = time.time()
        elif ((self._bit_depth != 0) or (self._stream_bits != 0)) and ((time.time() - self._detect_time) > 0.1):
            _LOGGER.debug(f'st337 stream dropped')
            self._bit_depth = 0
            self._stream_bits = 0
            self._reset_demux()

    async def start(self) -> None:
        while self._run:
            await self._event.wait()
            self._event.clear()
            if self._run:
                self._check_magic()

    def stop(self) -> None:
        self._run = False
        self._event.set()

    def reset(self) -> None:
        with self._lock:
            self._current = bytes([])
            self._bit_depth = 0
            self._stream_bits = 0
            self._reset_demux()
