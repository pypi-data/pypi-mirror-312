##################################################
## SMPTE 2110-3x AES3 PCM testing toolkit       ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

# toolkit version
VERSION = "1.1.0"
__version__ = VERSION

# toolkit name
NAME = "SMPTE 2110-3x AES3 PCM testing toolkit"

# default audio source port
AUDIO_SOURCE_PORT = 50022

# audio rtp payload type
RTP_PAYLOAD_TYPE = 97

# default 48000Hz sample rate
AUDIO_SAMPLE_RATE = 48000

# default 2 channels of audio
AUDIO_CHANNELS = 2

# 24 bits per sample (3 bytes)
AUDIO_SAMPLE_WIDTH = 3

# number of samples (left + right) to buffer before starting playback, increase this value if you experience stuttering. audio delay will increase as a result. defaults to 0.5s
AUDIO_MIN_QUEUE_LEVEL = int(AUDIO_SAMPLE_RATE)

# buffer 1 second @ 48KHz
TX_BUFFER_FRAMES = 8000

STEREO_SAMPLES_PER_PACKET = 6

# every block contains 192 subframes
AES3_SUBFRAMES_PER_BLOCK = 192

# rx buffer size in seconds
AUDIO_BUFFER_SIZE_SECONDS = 5