# PySPX-SLHDSA

This repository contains a Python package that provides bindings for [SPHINCS+](https://github.com/sphincs/sphincsplus). It provides support for the pure standardized parameter sets for SLH-DSA (i.e. simple variants, SPHINCS+ version 3.1 derivative).

Derived from [PySPX](https://github.com/sphincs/pyspx) with the minor changes required to support [SLH-DSA](https://doi.org/10.6028/NIST.FIPS.205). This includes making `sign` and `verify` provide an optional context string as input, and exposing new functions for the internal implementations for testing.

Tested to support Sign/Verify for SLH-DSA as well, passes verify and sign tests for the internal interface from ACVP.

### Installation

```
git clone https://github.com/tmcqueen-materials/pyspx-slhdsa.git
cd pyspx-slhdsa
git submodule init
git submodule update
sudo pip install .
```

### API

After installing the package, import a specific instance of SPHINCS+ SLH-DSA as follows (e.g. for `SLH-DSA-SHAKE-128f`):

```
import pyspx_slhdsa.shake_128f
```

This exposes the following straight-forward functions. All parameters are assumed to be `bytes` objects. Similarly, the returned keys and signatures are `bytes`. The `verify` function returns a boolean indicating success or failure.

```
>>> public_key, secret_key = pyspx_slhdsa.shake_128f.generate_keypair(seed)
>>> signature = pyspx_slhdsa.shake_128f.sign(message, secret_key)
>>> pyspx_slhdsa.shake_128f.verify(message, signature, public_key)
True
```

Additionally, the following attributes expose the expected sizes, as a consequence of the selected parameter set:

```
>>> pyspx_slhdsa.shake_128f.crypto_sign_BYTES
17088
>>> pyspx_slhdsa.shake_128f.crypto_sign_PUBLICKEYBYTES
32
>>> pyspx_slhdsa.shake_128f.crypto_sign_SECRETKEYBYTES
64
>>> pyspx_slhdsa.shake_128f.crypto_sign_SEEDBYTES
48
```

### Security

There has been no security analysis of this package. It primarily exists to provide seed-based deterministic key generation until supported by common libraries.
