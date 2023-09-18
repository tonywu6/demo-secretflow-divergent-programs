import jax.numpy as jnp
import secretflow
from spu import spu_pb2

self_party: str = "alice"
peer_party: str = "bob"
self_ray_port: int = 32400
peer_ray_port: int = 32401
self_secretflow_port: int = 8880
peer_secretflow_port: int = 8881
self_spu_port: int = 8890
peer_spu_port: int = 8891

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

alice = secretflow.PYU(self_party)
bob = secretflow.PYU(peer_party)
spu = secretflow.SPU(**spu_config)


def multiply(x, y):
    return jnp.negative(jnp.multiply(x, y))


array = alice(lambda x: x)(jnp.arange(10))
array = array.to(spu)

multiplier = bob(lambda x: x)(...)
multiplier = multiplier.to(spu)

result = spu(multiply)(array, multiplier)

result_for_alice = result.to(alice)
result_for_bob = result.to(bob)

print(secretflow.reveal(result_for_alice))
