##################################################
## SMPTE 2110-3x AES3 PCM testing toolkit       ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

from .const import *

class Aes3ToolConfig:
    # audio source port
    audio_source_port = AUDIO_SOURCE_PORT

    # audio sample rate
    audio_sample_rate = AUDIO_SAMPLE_RATE

    # number of audio channels
    audio_channels = AUDIO_CHANNELS

    # audio sample width in bytes
    audio_sample_width = AUDIO_SAMPLE_WIDTH

    # audio rtp payload type
    rtp_payload_type = RTP_PAYLOAD_TYPE

    # start the audio output after we've buffered this many frames (approximate level)
    # increase this value if you experience stuttering. audio delay will increase as a result
    audio_min_queue_level = AUDIO_MIN_QUEUE_LEVEL

    # number of samples to buffer before starting to transmit
    # 0     disable buffering
    # >0    number of samples to buffer before starting to transmit
    # <0    buffer all samples before starting to transmit (default)
    tx_buffer_samples = TX_BUFFER_FRAMES

    # send an igmp leave and join after this many seconds, to deal with missing igmp queriers
    reset_igmp_seconds:int = 0

    stats_callback:callable = None

    detect_bitstreams = True