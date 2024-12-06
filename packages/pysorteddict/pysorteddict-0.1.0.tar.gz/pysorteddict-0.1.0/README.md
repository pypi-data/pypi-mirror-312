# pysorteddict

Provides `SortedDict`, which is a Python sorted dictionary: a Python dictionary in which the keys are always in
ascending order.

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)

[![style](https://github.com/tfpf/pysorteddict/actions/workflows/style.yml/badge.svg)](https://github.com/tfpf/pysorteddict/actions/workflows/style.yml)
[![package](https://github.com/tfpf/pysorteddict/actions/workflows/package.yml/badge.svg)](https://github.com/tfpf/pysorteddict/actions/workflows/package.yml)

<p align="center">
 <img src="https://github.com/user-attachments/assets/e9d1e78e-c0fd-4d87-93f6-e293ddef31ba" />
</p>

## Installation

[pysorteddict is available on PyPI.](https://pypi.org/project/pysorteddict/) It requires Python 3.10 or newer. Built
distributions (binary wheels) are provided for Linux, macOS and Windows, so installing is straightforward.

```shell
pip install pysorteddict
```

If you are on any other platform, install the Python development headers and libraries before running the above
command.

## Usage

All keys in a sorted dictionary must be of the same type, which must be passed to the constructor. The values, though,
can be of any type.

```python
from pysorteddict import SortedDict

sorted_dict = SortedDict(int)
sorted_dict[5659] = "gaining weight is"
sorted_dict[1992] = 31.692
sorted_dict[24274] = "times easier than"
sorted_dict[9765] = ["losing", "weight"]
print(sorted_dict)
```

This program should output
`{1992: 31.692, 5659: 'gaining weight is', 9765: ['losing', 'weight'], 24274: 'times easier than'}`. Note that the keys
are in ascending order.

## Implementation Details

pysorteddict is implemented entirely in C++. `SortedDict` provides a Python interface to
`std::map<PyObject*, PyObject*, _>`.

## Documentation

### Constructor

#### `SortedDict(key_type: type) -> SortedDict`

Create a new sorted dictionary in which the keys are of type `key_type`. As of the current version, `key_type` must be
`int`. Support for some more types will be added in due course.

### Magic Methods

#### `key in d`

Return whether `key` is present in the sorted dictionary `d`.

#### `len(d)`

Return the number of key-value pairs in the sorted dictionary `d`.

#### `d[key]`

Return the value mapped to `key` in the sorted dictionary `d`.

* If `type(key)` is not the same as `key_type` passed to the constructor, raise `TypeError`.
* If `key` is not present in `d`, raise `KeyError`.

#### `d[key] = value`

Map `value` to `key` in the sorted dictionary `d`, replacing the previously-mapped value (if any).

* If `type(key)` is not the same as `key_type` passed to the constructor, raise `TypeError`.

#### `del d[key]`

Remove `key` and the value mapped to it from the sorted dictionary `d`.

* If `type(key)` is not the same as `key_type` passed to the constructor, raise `TypeError`.
* If `key` is not present in `d`, raise `KeyError`.

#### `str(d)`

Return a human-readable representation of the sorted dictionary `d`.

### Other Methods

#### `d.clear()`

Remove all key-value pairs in the sorted dictionary `d`.

#### `d.items() -> list[tuple[object, object]]`

Create and return a new list containing the key-value pairs in the sorted dictionary ``d``. This list will be sorted.

#### `d.keys() -> list[object]`

Create and return a new list containing the keys in the sorted dictionary ``d``. This list will be sorted.

#### `d.values() -> list[object]`

Create and return a new list containing the values in the sorted dictionary ``d``. This list will be sorted by the keys
which the values are mapped to.
