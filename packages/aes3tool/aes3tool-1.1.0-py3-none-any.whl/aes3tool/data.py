##################################################
## SMPTE 2110-3x AES3 PCM testing toolkit       ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

import logging
import time

# log output
_LOGGER = logging.getLogger(__name__)

def _parity_value(audio_sample:bytes, channel:bool, user_data:bool) -> int:
    data = audio_sample[0] << 16 | audio_sample[1] << 8 | audio_sample[2]
    parity = 1 if channel else 0
    if user_data:
        parity ^= 1
    pos = 0
    while (data != 0):
        pos += 1
        if pos <= 4:
            continue
        if ((data & 1) == 1):
            parity ^= 1
        data >>= 1
    return 1 if parity != 0 else 0

class Aes3ExtraData:
    _ptr = 0
    _data = 0
    _last = 0
    def __init__(self, label:str='extra') -> None:
        self._label = label

    def reset(self) -> None:
        self._ptr = 0
        self._data = 0

    def push(self, b:int) -> None:
        if b:
            self._data |= (1 << self._ptr)
        self._ptr += 1

    def on_block_start(self) -> None:
        if self._data != self._last:
            _LOGGER.info(f"{self._label} = {self._data:x}")
            self._last = self._data
        self.reset()

    def get(self) -> int:
        return self._data

class Am824Frame:
    ''' 4 byte Am824 frame containing an AES3 subframe '''
    def __init__(self, data: bytes) -> None:
        self.meta = data[0]
        self._audio = data[1:4][::-1] # byte order is reversed

    @property
    def data(self) -> bytes:
        return bytes([self.meta, self._audio[2], self._audio[1], self._audio[0]])

    def construct(audio:bytes|memoryview, block_start:bool=False, frame_start:bool=False, channel:bool=False, user_data:bool=False):
        ''' Construct a new AM824 audio frame '''
        data = [
            (
                (0x01) |
                (0x02 if user_data else 0) |
                (0x04 if channel else 0) |
                (0x10 if frame_start else 0) |
                (0x20 if block_start else 0)
            ),
            audio[2],
            audio[1],
            audio[0]]
        if _parity_value(audio_sample=data[1:], channel=channel, user_data=user_data):
            data[0] |= 0x08
        return Am824Frame(data=bytes(data))

    @property
    def block_start(self) -> bool:
        ''' start of a 192 subframe block '''
        return ((self.meta & 0x20) != 0)

    @property
    def frame_start(self) -> bool:
        ''' start of a frame with one or more audio sample (left, right, ...)'''
        return ((self.meta & 0x10) != 0)

    @property
    def parity(self) -> int:
        ''' even parity '''
        return 1 if ((self.meta & 0x8) != 0) else 0

    @property
    def channel(self) -> bool:
        ''' channel bit '''
        return ((self.meta & 0x4) != 0)

    @property
    def user_data(self) -> bool:
        ''' user data bit '''
        return ((self.meta & 0x2) != 0)

    @property
    def valid(self) -> bool:
        ''' frame contains valid data '''
        return ((self.meta & 0x1) != 0)

    @property
    def audio_sample(self) -> bytes:
        ''' the audio sample (24 bits) '''
        return self._audio

    @property
    def parity_valid(self) -> bool:
        ''' parity bit valid or not '''
        return (_parity_value(audio_sample=self.audio_sample, channel=self.channel, user_data=self.user_data) == self.parity)

    def __str__(self) -> str:
        if not self.parity_valid:
            return "INVALID"
        if self.block_start:
            return f"block {1 if self.channel else 0}"
        if self.frame_start:
            return f"frame {1 if self.channel else 0}:{self.audio_sample}"
        return f"{1 if self.channel else 0}:{self.audio_sample}"

class Aes3Frame:
    ''' AES3 RTP payload, containing one or more Am824Frame '''
    def __init__(self, data: bytes) -> None:
        self.len = len(data)
        if (self.len % 4 != 0):
            raise Exception(f"invalid frame len {self.len}")
        self.data = data
        self._subframes:list[Am824Frame] = []
        self._processed_frames = False

    def append(self, frame:Am824Frame) -> None:
        self._process_frames()
        self.data += frame.data
        self._subframes.append(frame)

    def _process_frames(self) -> None:
        if not self._processed_frames:
            l = self.len
            data = self.data
            while l != 0:
                self._subframes.append(Am824Frame(data=data))
                l -= 4
                data = data[4:]
            self._processed_frames = True

    def push_channel_data(self, data:Aes3ExtraData) -> None:
        for frame in self.sub_frames:
            if frame.block_start:
                data.on_block_start()
            data.push(frame.channel)

    def push_user_data(self, data:Aes3ExtraData) -> None:
        for frame in self.sub_frames:
            if frame.block_start:
                data.on_block_start()
            data.push(frame.user_data)

    @property
    def sub_frames(self) -> list[Am824Frame]:
        self._process_frames()
        return self._subframes

    @property
    def nb_sub_frames(self) -> int:
        return int(self.len / 4)

    @property
    def sub_frame_samples(self) -> bytes:
        '''extract audio samples without constructing new Am824Frame instances'''
        rv:bytes = None
        for idx in range(self.nb_sub_frames):
            if idx == 0:
                rv = self.data[1:4][::-1]
            else:
                rv += self.data[(idx * 4) + 1:(idx * 4) + 4][::-1]
        return rv

    @property
    def sub_frame_samples2(self) -> bytes:
        '''extract audio samples without constructing new Am824Frame instances'''
        rv:bytes = None
        for idx in range(self.nb_sub_frames):
            if idx == 0:
                rv = self.data[1:4]
            else:
                rv += self.data[(idx * 4) + 1:(idx * 4) + 4]
        return rv

    @property
    def block_start(self) -> list[Am824Frame]:
        rv = []
        add = False
        for frame in self.sub_frames:
            if add or frame.block_start:
                rv.append(frame)
                add = True
        return rv

    def __len__(self) -> int:
        return self.nb_sub_frames * 3

    def __str__(self) -> str:
        rv = ""
        for frame in self.sub_frames:
            rv += f"[{str(frame)}]"
        return f"frame: {rv}"

class RtpPacket:
    ''' RTP packet, potentially containing an Aes3Frame '''
    def __init__(self, data: bytes) -> None:
        self.set_data(data=data)
        self._timestamp = ((int(self.data[4]) << 24) | (int(self.data[5]) << 16) | (int(self.data[6]) << 8) | int(self.data[7]))
        if (self._timestamp == 0):
            self._timestamp = int(time.time() * 1000)

    def set_data(self, data: bytes) -> None:
        self.data = data
        if len(self.data) < 12:
            raise Exception(f"invalid packet len {len(self.data)}")

    def construct(frame:Aes3Frame, type:int, sequence:int, timestamp:int=0, sync_source_id:int=0) -> 'RtpPacket':
        return RtpPacket(bytes([
            0x80,
            (type & 0x7F),
            ((sequence >> 8) & 0xFF), (sequence & 0xFF),
            ((timestamp >> 24) & 0xFF), ((timestamp >> 16) & 0xFF), ((timestamp >> 8) & 0xFF), (timestamp & 0xFF),
            ((sync_source_id >> 24) & 0xFF), ((sync_source_id >> 16) & 0xFF), ((sync_source_id >> 8) & 0xFF), (sync_source_id & 0xFF)]) + frame.data)

    @property
    def rfc1889_version(self) -> int:
        return ((int(self.data[0]) >> 6) & 0xFF)

    @property
    def padding(self) -> bool:
        return ((int(self.data[0]) & 0x20) != 0)

    @property
    def extension(self) -> bool:
        return ((int(self.data[0]) & 0x10) != 0)

    @property
    def source_id_count(self) -> int:
        return (int(self.data[0]) & 0xF)

    @property
    def payload_type(self) -> int:
        return (int(self.data[1]) & 0x7F)

    @property
    def marker(self) -> bool:
        return ((int(self.data[1]) & 0x80) != 0)

    @property
    def sequence(self) -> int:
        return ((int(self.data[2]) << 8) | int(self.data[3]))

    @property
    def timestamp(self) -> int:
        return self._timestamp

    def time_diff(self, previous:'RtpPacket') -> int:
        if (self.timestamp > previous.timestamp):
            return (self.timestamp - previous.timestamp)
        return (0xFFFFFFFF - previous.timestamp + self.timestamp)

    @property
    def sync_source_id(self) -> int:
        return ((int(self.data[8]) << 24) | (int(self.data[9]) << 16) | (int(self.data[10]) << 8) | int(self.data[11]))

    @property
    def payload(self) -> bytes:
        return self.data[12:]

    @property
    def aes3_payload(self) -> Aes3Frame | None:
        try:
            return Aes3Frame(data=self.payload)
        except:
            return None

    def check_sequence(self, previous:'RtpPacket') -> bool:
        if (self.sequence != ((previous.sequence + 1) & 0xFFFF)):
            _LOGGER.warning(f"sequence error - current:{self.sequence} != previous:{((previous.sequence + 1) & 0xFFFF)}")
            return False
        return True
