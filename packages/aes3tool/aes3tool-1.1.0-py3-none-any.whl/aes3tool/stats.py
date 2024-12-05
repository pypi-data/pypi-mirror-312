import asyncio
import threading

class Aes3ProcessorStats:
    _lock = threading.Lock()

    def __init__(self) -> None:
        self.reset()

    def increase_sequence_errors(self, value:int=1) -> None:
        with self._lock:
            self._sequence_errors += value

    def increase_underruns(self, value:int=1) -> None:
        with self._lock:
            self._underruns += value

    def set_output_codec(self, name:str, rate:int) -> None:
        self._codec = name
        self._codec_rate = rate

    def increase_samples(self, value:int, sample_rate:int, audio_channels:int) -> None:
        with self._lock:
            self._sample_counter += value
            self._sample_rate = sample_rate
            self._audio_channels = audio_channels

    def increase_frames(self, value:int=1) -> None:
        with self._lock:
            self._frame_counter += value

    def increase_bytes(self, value:int=1) -> None:
        with self._lock:
            self._bytes_counter += value

    def increase_values(self, vsamples:int=0, vframes:int=0, vbytes:int=0, vsequence:int=0, vunderruns:int=0) -> None:
        with self._lock:
            self._sample_counter += vsamples
            self._frame_counter += vframes
            self._bytes_counter += vbytes
            self._sequence_errors += vsequence
            self._underruns += vunderruns

    def read(self) -> tuple[int, int, int, int, int]:
        with self._lock:
            rv = (self._bytes_counter, self._frame_counter, self._sample_counter, self._underruns, self._sequence_errors)
            self._frame_counter = 0
            self._bytes_counter = 0
            self._sample_counter = 0
            self._underruns = 0
            self._sequence_errors = 0
            return rv

    def close(self) -> None:
        self.stopping = True

    def reset(self) -> None:
        self._sample_rate = 0
        self._audio_channels = 0
        self._sample_counter = 0
        self._frame_counter = 0
        self._bytes_counter = 0
        self._sequence_errors = 0
        self._codec_rate = 0
        self._underruns = 0
        self.stopping = False
        self._codec = 'PCM'

    async def stats_reader(self, callback:callable, sample_width:int) -> None:
        if callback is None:
            return
        sleep_time = 1
        self.reset()
        while not self.stopping:
            await asyncio.sleep(sleep_time)
            (bytes_read, frames_read, samples_read, underruns, sequence_errors) = self.read()
            callback(round(bytes_read / (sleep_time*1024)),
                     round(frames_read / sleep_time),
                     round(samples_read / sleep_time),
                     round(underruns / sleep_time),
                     round(sequence_errors / sleep_time),
                     self._codec,
                     self._codec_rate if (self._codec_rate > 0) else round((samples_read * sample_width) / 1000),
                     self._sample_rate,
                     self._audio_channels)
