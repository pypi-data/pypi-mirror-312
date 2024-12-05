##################################################
## SMPTE 2110-3x AES3 PCM testing toolkit       ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

from abc import ABC, abstractmethod
import asyncio
import logging
import os
import socket
import threading
from typing import Coroutine, Tuple

# log output
_LOGGER = logging.getLogger(__name__)

class UdpCallback(ABC):
    @abstractmethod
    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        ''' UDP datagram received '''

class ConnectionBase(ABC):
    def __init__(self, callback:UdpCallback, ip:str, port:int, listen_if:str) -> None:
        self.callback = callback
        self.ip = ip
        self.port = port
        self.listen_if = listen_if
        self.tx_mode = False

    @abstractmethod
    def close(self) -> None:
        '''close the connection'''

    @property
    @abstractmethod
    def socket(self) -> socket.socket:
        '''return the active socket'''

    def reset_igmp(self) -> None:
        # deal with missing querier, send join every minute
        _LOGGER.info("resetting igmp membership")
        self.igmp_leave()
        self.igmp_join()

    def igmp_leave(self) -> None:
        self.socket.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP,
                    socket.inet_aton(self.ip) + socket.inet_aton(self.listen_if))

    def igmp_join(self) -> None:
        self.socket.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                    socket.inet_aton(self.ip) + socket.inet_aton(self.listen_if))

    def __str__(self) -> str:
        return f"{self.ip}:{self.port}"

    def __repr__(self) -> str:
        return str(self)

class ConnectionThread(ConnectionBase):
    def __init__(self, callback:UdpCallback, ip:str, port:int, listen_if:str) -> None:
        ConnectionBase.__init__(self, callback=callback, ip=ip, port=port, listen_if=listen_if)
        self._socket:socket.socket = None
        self._reader_thread:threading.Thread = None
        self._close = False

    def _reader(self) -> None:
        _LOGGER.info(f"start listening for audio from {self.ip}:{self.port} (threaded)")
        while not self._close:
            try:
                data, addr = self._socket.recvfrom(1500)
                self.callback.datagram_received(data, addr)
            except Exception as e:
                return

    def start_srv(self) -> bool:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self._socket.bind(('', self.port))
        self._socket.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                    socket.inet_aton(self.ip) + socket.inet_aton(self.listen_if))
        self._reader_thread = threading.Thread(target=self._reader)
        self._reader_thread.start()
        return (self._reader_thread is not None)

    def close(self) -> None:
        '''close the connection'''
        self._close = True
        if (self.socket is not None):
            self.socket.close()
            self._socket = None
        if (self._reader_thread is not None):
            self._reader_thread.join()

    def transmit(self, data: bytes) -> None:
        self._socket.sendto(data)

    @property
    def socket(self) -> socket.socket:
        return self._socket

class ConnectionAsync(asyncio.DatagramProtocol, ConnectionBase):
    def __init__(self, callback:UdpCallback, ip:str, port:int, listen_if:str) -> None:
        assert(isinstance(ip, str))
        assert(isinstance(port, int))
        assert(isinstance(listen_if, str))
        asyncio.DatagramProtocol.__init__(self)
        ConnectionBase.__init__(self, callback=callback, ip=ip, port=port, listen_if=listen_if)
        self._transport:asyncio.DatagramTransport = None

    @property
    def socket(self) -> socket.socket:
        return self._transport.get_extra_info('socket')

    async def start_srv_async(self) -> Coroutine:
        _LOGGER.debug(f"start listening for audio from {self.ip}:{self.port} (asyncio@{self.listen_if})")
        self.tx_mode = False
        return await asyncio.get_event_loop().create_datagram_endpoint(
                lambda: self, local_addr=(self.ip, self.port))
    
    async def start_tx_async(self) -> Coroutine:
        _LOGGER.debug(f"start transmitting audio to {self.ip}:{self.port} (asyncio@{self.listen_if})")
        self.tx_mode = True
        return await asyncio.get_event_loop().create_datagram_endpoint(
                lambda: self, local_addr=(self.listen_if, 0), remote_addr=(self.ip, self.port))

    def close(self) -> None:
        if self._transport is not None:
            self._transport.close()

    def connection_made(self, transport:asyncio.DatagramTransport) -> None:
        self._transport = transport
        sock = self.socket
        if self.tx_mode:
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 3)
            if (os.name == 'posix'):
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            _LOGGER.debug(f"transmitting to {self.ip}:{self.port} (asyncio)")
        else:
            self.igmp_join()
            _LOGGER.debug(f"listening for {self.ip}:{self.port} (asyncio)")

    def transmit(self, data: bytes) -> None:
        self._transport.sendto(data)

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        self.callback.datagram_received(data, addr)
