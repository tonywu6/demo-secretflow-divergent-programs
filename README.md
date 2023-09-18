# Demo: SecretFlow with divergent programs

A 2-party computation in SecretFlow where submitted functions are different.

## Install

Requires Python 3.8. Virtualenv recommended.

```bash
pip install -r requirements.lock -r requirements-dev.lock
```

## Start Ray instances

Spin up 2 Ray instances, both locally, on port 32400 and 32401.

```bash
./start_ray.sh
```

## Run the demo

In two separate terminals, run `alice.py` and `bob.py`:

```bash
python alice.py
```

```bash
python bob.py
```

Both should eventually print out:

```
[ 0.  -0.5 -1.  -1.5 -2.  -2.5 -3.  -3.5 -4.  -4.5]
```

However, the functions submitted are different:

In `alice.py`:

```python
def multiply(x, y):
    return jnp.negative(jnp.multiply(x, y))
```

In `bob.py`:

```python
def multiply(x, y):
    return jnp.multiply(x, y)
```
