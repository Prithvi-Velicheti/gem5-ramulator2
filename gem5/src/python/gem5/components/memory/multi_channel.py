# Copyright (c) 2021 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from typing import Optional

from .abstract_memory_system import AbstractMemorySystem
from .dram_interfaces.ddr3 import (
    DDR3_1600_8x8,
    DDR3_2133_8x8,
)
from .dram_interfaces.ddr4 import DDR4_2400_8x8
from .dram_interfaces.hbm import HBM_1000_4H_1x64
from .dram_interfaces.lpddr3 import LPDDR3_1600_1x32
from .memory import ChanneledMemory


def DualChannelDDR3_1600(
    size: Optional[str] = None,
) -> AbstractMemorySystem:
    """
    A dual channel memory system using DDR3_1600_8x8 based DIMM.
    """
    return ChanneledMemory(DDR3_1600_8x8, 2, 64, size=size)


def DualChannelDDR3_2133(
    size: Optional[str] = None,
) -> AbstractMemorySystem:
    """
    A dual channel memory system using DDR3_2133_8x8 based DIMM.
    """
    return ChanneledMemory(DDR3_2133_8x8, 2, 64, size=size)


def DualChannelDDR4_2400(
    size: Optional[str] = None,
) -> AbstractMemorySystem:
    """
    A dual channel memory system using DDR4_2400_8x8 based DIMM.
    """
    return ChanneledMemory(DDR4_2400_8x8, 2, 64, size=size)


def QuadChannelDDR4_2400(
    size: Optional[str] = None,
) -> AbstractMemorySystem:
    """
    A quad channel memory system using DDR4_2400_8x8 based DIMM.
    """
    return ChanneledMemory(DDR4_2400_8x8, 4, 64, size=size)


def DualChannelLPDDR3_1600(
    size: Optional[str] = None,
) -> AbstractMemorySystem:
    return ChanneledMemory(LPDDR3_1600_1x32, 2, 64, size=size)
