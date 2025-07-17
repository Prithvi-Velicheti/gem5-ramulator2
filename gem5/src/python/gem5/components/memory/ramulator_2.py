import os
import configparser

from m5.objects import Ramulator2, AddrRange, Port, MemCtrl
from m5.util.convert import toMemorySize

from ...utils.override import overrides
from ..boards.abstract_board import AbstractBoard
from .abstract_memory_system import AbstractMemorySystem

from typing import Optional, Tuple, Sequence, List
###
from .memory import _isPow2
from math import log 

class Ramulator2MemCtrl(Ramulator2):
    """
    A Ramulator2 Memory Controller.

    The class serves as a SimObject object wrapper, utilizing the Ramulator2 
    configuratons.
    """

    def __init__(self, config_path: str) -> None:
        """
        :param mem_name: The name of the type  of memory to be configured.
        :param num_chnls: The number of channels.
        """
        super().__init__()
        self.config_path = config_path



class Ramulator2System (AbstractMemorySystem):

    def __init__(self, config_path: str, size: Optional[str]):
        """
        :param mem_name: The name of the type  of memory to be configured.
        :param num_chnls: The number of channels.
        """
        super().__init__()
        self.mem_ctrl = Ramulator2MemCtrl(config_path)
        self._size = toMemorySize(size)

        if not size:
            raise NotImplementedError(
                "Ramulator2 memory controller requires a size parameter."
            )

    @overrides(AbstractMemorySystem)
    def incorporate_memory(self, board: AbstractBoard) -> None:
        pass

    @overrides(AbstractMemorySystem)
    def get_mem_ports(self) -> Tuple[Sequence[AddrRange], Port]:
        return [(self.mem_ctrl.range, self.mem_ctrl.port)]

    @overrides(AbstractMemorySystem)
    def get_memory_controllers(self) -> List[MemCtrl]:
        return [self.mem_ctrl]

    @overrides(AbstractMemorySystem)
    def get_size(self) -> int:
        return self._size

    @overrides(AbstractMemorySystem)
    def set_memory_range(self, ranges: List[AddrRange]) -> None:
        if len(ranges)!=1 or ranges[0].size() != self._size:
            raise Exception(
                "Single channel Ramulator2 memory controller requires a single "
                "range which matches the memory's size."
            )
        #self._mem_range = ranges[0]
        #self.mem_ctrl.range = AddrRange(
        #    start=self._mem_range.start,
        #    size=self._mem_range.size(),
        #    intlvHighBit=6+0-1,
        #    xorHighBit=0,
        #    intlvBits=0,
        #    intlvMatch=0,
        #)
        self.mem_ctrl.range = ranges[0]        


###
class Ramulator2ChanneledMemory(AbstractMemorySystem):
    """Multi-channel memory system using Ramulator2 controllers"""
    
    def __init__(
        self,
        config_path: str,
        num_channels: int,
        interleaving_size: int,
        size: str
    ):
        """
        :param config_path: Path to Ramulator2 YAML configuration
        :param num_channels: Number of memory channels
        :param interleaving_size: Address interleaving block size
        :param size: Total memory size
        """
        super().__init__()
        self._num_channels = num_channels
        self._intlv_size = interleaving_size
        self._size = toMemorySize(size)
        #self.config_path = config_path
        
        if not _isPow2(interleaving_size):
            raise ValueError("Interleaving size must be power of 2")
        
        # Create memory controllers
        self.mem_ctrl = [
            Ramulator2MemCtrl(config_path) 
            for _ in range(num_channels)
        ]
    
    def _interleave_addresses(self):
        intlv_low_bit = log(self._intlv_size, 2)
        intlv_bits = log(self._num_channels, 2)
        
        for i, ctrl in enumerate(self.mem_ctrl):
            ctrl.range = AddrRange(
                start=self._mem_range.start,
                size=self._mem_range.size(),
                intlvHighBit=intlv_low_bit + intlv_bits - 1,
                xorHighBit=0,
                intlvBits=intlv_bits,
                intlvMatch=i
            )
    
    @overrides(AbstractMemorySystem)
    def incorporate_memory(self, board: AbstractBoard) -> None:
        if self._intlv_size < int(board.get_cache_line_size()):
            raise ValueError(
                f"Interleaving size ({self._intlv_size}) must be >= "
                f"cache line size ({board.get_cache_line_size()})"
            )
    
    @overrides(AbstractMemorySystem)
    def get_mem_ports(self) -> Sequence[Tuple[AddrRange, Port]]:
        return [(ctrl.range, ctrl.port) for ctrl in self.mem_ctrl]
    
    @overrides(AbstractMemorySystem)
    def get_memory_controllers(self) -> List[MemCtrl]:
        return self.mem_ctrl
    
    @overrides(AbstractMemorySystem)
    def get_size(self) -> int:
        return self._size
    
    @overrides(AbstractMemorySystem)
    def set_memory_range(self, ranges: List[AddrRange]) -> None:
        if len(ranges) != 1 or ranges[0].size() != self._size:
            raise ValueError(
                "Requires single range matching total memory size\n"
                f"Expected size: {self._size}, Actual: {ranges[0].size()}"
            )
        self._mem_range = ranges[0]
        self._interleave_addresses()

"""
def DualChannelRamulator(
    config_path:str,
    size: Optional[str] = None,
) -> AbstractMemorySystem:
    return Ramulator2ChanneledMemory(config_path, 2, 64, size)


def QuadChannelRamulator(
    config_path:str,
    size: Optional[str] = None,
) -> AbstractMemorySystem:
    return Ramulator2ChanneledMemory(config_path, 4, 64, size)

"""
