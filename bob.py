import secretflow
from spu import spu_pb2

self_party: str = "bob"
peer_party: str = "alice"
self_ray_port: int = 32401
peer_ray_port: int = 32400
self_secretflow_port: int = 8881
peer_secretflow_port: int = 8880
self_spu_port: int = 8891
peer_spu_port: int = 8890

secretflow_config = dict(
    address=f"localhost:{self_ray_port}",
    cluster_config=dict(
        parties={
            self_party: dict(address=f"127.0.0.1:{self_secretflow_port}"),
            peer_party: dict(address=f"127.0.0.1:{peer_secretflow_port}"),
        },
        self_party=self_party,
    ),
)

spu_config = dict(
    cluster_def=dict(
        nodes=[
            dict(party=self_party, address=f"127.0.0.1:{self_spu_port}"),
            dict(party=peer_party, address=f"127.0.0.1:{peer_spu_port}"),
        ],
        runtime_config=dict(
            protocol=spu_pb2.SEMI2K,
            field=spu_pb2.FM128,
        ),
    )
)


secretflow.init(**secretflow_config)

bob = secretflow.PYU(self_party)
alice = secretflow.PYU(peer_party)
spu = secretflow.SPU(**spu_config)


def noop():
    return


array = alice(lambda x: x)(...)
array = array.to(spu)

multiplier = bob(lambda x: x)(0.5)
multiplier = multiplier.to(spu)

result = spu(noop)(array, multiplier)

result_for_alice = result.to(alice)
result_for_bob = result.to(bob)

print(secretflow.reveal(result_for_bob))
