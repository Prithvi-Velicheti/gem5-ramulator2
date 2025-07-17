"""
Eiger : 1 fabric chiplet with 4 io chiplet

Kevin 2025/06/12

"""

from m5.objects import (
    GarnetExtLink,
    GarnetIntLink,
    GarnetNetwork,
    GarnetNetworkInterface,
    GarnetRouter,
)


class MyRouter(GarnetRouter):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.latency = 3
        self._name = name

class Eiger(GarnetNetwork):
    def __init__(self, ruby_system):
        super().__init__()
        self.ruby_system = ruby_system
        # There's definitely something wrong with something if I have to
        # do this to get it to work.
        self.ni_flit_size = 64
        self.vcs_per_vnet = 16

    def connectControllers(
        self, l1i_ctrls, l1d_ctrls, l2_ctrls, mem_ctrls, dma_ctrls
    ):
        # Assertions
        assert len(l1i_ctrls) == 4
        assert len(l1d_ctrls) == 4
        assert len(l2_ctrls) == 4
        assert len(mem_ctrls) == 4, (
            "This topology requires exactly 4 memory controllers. "
            f"Received {len(mem_ctrls)}"
        )

        # Layer 2: CPU Routers (r0-r3)
        self.cpu_routers = [MyRouter(name=f"R_C_{i}", router_id=i) for i in range(4)]

        # Layer 3: IO Routers (r4-r7)
        self.io_routers = [
            MyRouter(name=f"R_IO_{i}", router_id=4 + i) for i in range(4)
        ]

        # Layer 4: Mem Routers (r8-r11)
        self.mem_routers = [
            MyRouter(name=f"R_MC_{i}", router_id=8 + i) for i in range(4)
        ]

        # External Links (Connecting Layers to Endpoints)
        ext_links = []
        link_id_counter = 0

        # Row 1 -> Row 2: L1/L2 Caches to CPU Routers
        for i, c in enumerate(l1i_ctrls):
            ext_links.append(
                GarnetExtLink(
                    link_id=link_id_counter,
                    ext_node=c,
                    int_node=self.cpu_routers[i],
                )
            )
            link_id_counter += 1

        for i, c in enumerate(l1d_ctrls):
            ext_links.append(
                GarnetExtLink(
                    link_id=link_id_counter,
                    ext_node=c,
                    int_node=self.cpu_routers[i],
                )
            )
            link_id_counter += 1

        for i, c in enumerate(l2_ctrls):
            ext_links.append(
                GarnetExtLink(
                    link_id=link_id_counter,
                    ext_node=c,
                    int_node=self.cpu_routers[i],
                )
            )
            link_id_counter += 1

        # Row 4 -> Row 5: Mem Routers to Memory Controllers
        for i, c in enumerate(mem_ctrls):
            ext_links.append(
                GarnetExtLink(
                    link_id=link_id_counter,
                    ext_node=c,
                    int_node=self.mem_routers[i],
                )
            )
            link_id_counter += 1

        if dma_ctrls:
            for i, c in enumerate(dma_ctrls):
                ext_links.append(
                    GarnetExtLink(
                        link_id=link_id_counter,
                        ext_node=c,
                        int_node=self.io_routers[0],
                    )
                )
                link_id_counter += 1

        self.ext_links = ext_links

        # Internal Links (Connecting Router Layers)
        int_links = []

        # Row 2 -> Row 3: CPU Routers to IO Routers
        for i in range(4):
            int_links.append(
                GarnetIntLink(
                    link_id=link_id_counter,
                    src_node=self.cpu_routers[i],
                    dst_node=self.io_routers[i],
                )
            )
            link_id_counter += 1

            int_links.append(
                GarnetIntLink(
                    link_id=link_id_counter,
                    src_node=self.io_routers[i],
                    dst_node=self.cpu_routers[i],
                )
            )
            link_id_counter += 1

        # Row 3 <-> Row 4: IO Routers to Mem Routers (Bidirectional)
        for io_router in self.io_routers:
            for mem_router in self.mem_routers:
                int_links.append(
                    GarnetIntLink(
                        link_id=link_id_counter,
                        src_node=io_router,
                        dst_node=mem_router,
                    )
                )
                link_id_counter += 1
                int_links.append(
                    GarnetIntLink(
                        link_id=link_id_counter,
                        src_node=mem_router,
                        dst_node=io_router,
                    )
                )
                link_id_counter += 1

        self.int_links = int_links

        # Finalize Network Components
        self.routers = (
            self.cpu_routers + self.io_routers + self.mem_routers
        )
        self.netifs = [
            GarnetNetworkInterface(id=i)
            for (i, n) in enumerate(self.ext_links)
        ]
