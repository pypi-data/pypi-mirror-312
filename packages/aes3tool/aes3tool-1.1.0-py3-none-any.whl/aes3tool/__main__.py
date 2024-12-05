#!/usr/bin/python3

##################################################
## SMPTE 2110-3x AES3 PCM testing toolkit       ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################
import logging

# log output
_LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def _sanitise_input(src:str|None) -> str|None:
    if src is None:
        return None
    return str(src).strip()

def main():
    import argparse
    import asyncio
    import aes3tool as ae
    import signal
    import sys
    from .const import NAME, VERSION

    processor:ae.Aes3Processor = None
    config = ae.Aes3ToolConfig()
    argparser = argparse.ArgumentParser(description=f"{NAME} {VERSION}")
    argparser.add_argument("-s", dest='audio_source', help='source file to stream to the network. start in listening mode if this parameter is not provided', required=False, type=str)
    argparser.add_argument("-n", dest='network_interface', help='network interface ip address to send the igmp join on', required=True, type=str)
    argparser.add_argument("-a", dest='audio_mcast_ip', help='audio source multicast address', required=True, type=str)
    argparser.add_argument("-p", dest='audio_port', help='audio source udp port number. defaults to 50022', required=False, type=int)
    argparser.add_argument("-f", dest='file_path', help='store the received audio stream as .wav instead of playing it', required=False, type=str)
    argparser.add_argument("-r", dest='reset_igmp', help='send an igmp leave and join every RESET_IGMP seconds. useful if the network doesn\'t have an igmp querier. this may cause brief audio drop/underruns', required=False, type=int)
    argparser.add_argument("-rt", dest='payload_type', help='rtp payload type. defaults to 97', required=False, type=int)
    argparser.add_argument("-ar", dest='audio_rate', help='audio sample rate. defaults to 48000', required=False, type=int)
    argparser.add_argument("-ac", dest='audio_channels', help='number of audio channels. defaults to 2', required=False, type=int)
    argparser.add_argument("-aw", dest='audio_width', help='audio sample width. defaults to 3 (24 bits)', required=False, type=int)
    argparser.add_argument("-aq", dest='queue_level', help='number of samples to buffer before starting to play back audio. only relevant in playback mode. defaults to 256', required=False, type=int)
    args = argparser.parse_args()

    if args.audio_port is not None:
        config.audio_source_port = args.audio_port
    if args.payload_type is not None:
        config.rtp_payload_type = args.payload_type
    if args.audio_rate is not None:
        config.audio_sample_rate = args.audio_rate
    if args.audio_channels is not None:
        config.audio_channels = args.audio_channels
    if args.audio_width is not None:
        config.audio_sample_width = args.audio_width
    if args.reset_igmp is not None:
        config.reset_igmp_seconds = args.reset_igmp
    if args.queue_level is not None:
        config.audio_min_queue_level = args.queue_level

    def sig_handler(sig, frame):
        if processor is not None:
            asyncio.get_event_loop().run_until_complete(processor.close())
        sys.exit(1)
    signal.signal(signal.SIGINT, sig_handler)

    _LOGGER.info(f"{NAME} {VERSION}")

    if args.audio_source is None:
        # no source file provided. start listening
        fp = _sanitise_input(args.file_path)
        processor = ae.Aes3Receiver(config=config, source_ip=_sanitise_input(args.audio_mcast_ip), interface_ip=_sanitise_input(args.network_interface), capture_file=_sanitise_input(fp))
    else:
        processor = ae.Aes3Transmitter(config=config, target_ip=_sanitise_input(args.audio_mcast_ip), interface_ip=_sanitise_input(args.network_interface), source_file=_sanitise_input(args.audio_source))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(processor.start())
    loop.run_forever()
    loop.run_until_complete(processor.close())
    loop.close()
