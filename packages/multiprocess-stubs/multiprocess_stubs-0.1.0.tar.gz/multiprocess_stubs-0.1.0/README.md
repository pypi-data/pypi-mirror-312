# multiprocess-stubs

[![image](https://img.shields.io/pypi/v/multiprocess-stubs)](https://pypi.python.org/pypi/multiprocess-stubs)
[![image](https://img.shields.io/pypi/l/multiprocess-stubs)](https://github.com/zhou13/multiprocess-stubs/blob/master/LICENSE.txt)

Type stubs for the `multiprocess` library.

## Installation

```bash
pip install multiprocess-stubs
```

## Purpose

This package provides type stubs (`.pyi`) for the `multiprocess` library, enabling better type checking and IDE support for Python's multiprocessing functionality.

## Usage

Simply install the stubs, and your type checker (mypy, pyright) will use these type definitions when analyzing code that uses `multiprocess`.

## Compatibility

- Compatible with Python 3.8+
- Matches the type signature of the standard library `multiprocessing` module

## Development

Right now, most of this package is copied from https://github.com/python/typeshed/tree/main/stdlib/multiprocessing. Contributions to improve the type annotations are welcome.

## License

MIT License
