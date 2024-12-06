import hashlib
import types
from typing import Any, Callable, Tuple

import pandas as pd
import pyarrow as pa

import federleicht.args as args
from federleicht.config import CACHE

__salt__: bytes = None


def salt() -> bytes:
    """Generate a salt based on the main dependency versions.

    Returns:
        bytes: The first 8 characters of the package version encoded as bytes.
    """

    global __salt__

    if __salt__ is None:

        dependencies = {
            "pandas": pd.__version__,
            "pyarrow": pa.__version__,
        }

        versions = ";".join(f"{key}={value}" for key, value in dependencies.items())

        __salt__ = hashlib.blake2s(
            versions.encode(),
            digest_size=8,
            salt=CACHE.version.encode()[:8],
        ).digest()

    return __salt__


def hash_wrapped(
    function: types.FunctionType,
    arguments: Tuple[Any, ...],
) -> hashlib.blake2s:
    """Generate a BLAKE2s hash for all arguments and also the functions byte-code.

    Args:
        function (types.FunctionType): wrapped function.
        arguments (Tuple[Any, ...]): *args and **kwargs of wrapped function

    Returns:
        hashlib.blake2s: The BLAKE2s hash object.
    """

    binarydata = args.unique(*arguments).digest()

    hash = hashlib.blake2s(
        binarydata,
        digest_size=CACHE.digest,
        salt=salt(),
    )

    hash.update(function.__qualname__.encode())
    hash.update(function.__code__.co_code)

    return hash


def function(
    function: types.FunctionType,
    arguments: Tuple[Any, ...],
    pepper: Callable[[], bytes] = None,
) -> str:
    """Generate a BLAKE2s hash for all arguments and also the functions byte-code.

    Args:
        function (types.FunctionType): wrapped function.
        arguments (Tuple[Any, ...]): *args and **kwargs of wrapped function
        pepper (Callable[[], bytes], optional): A function that returns a salt.
            Defaults to None.

    Returns:
        str: The hexadecimal digest of the BLAKE2s hash.
    """

    hash = hash_wrapped(function, arguments)

    if callable(pepper):
        hash.update(pepper())

    return hash.hexdigest()
