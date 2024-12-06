# cfinterface

![tests](https://github.com/rjmalves/cfi/workflows/tests/badge.svg)
[![codecov](https://codecov.io/gh/rjmalves/cfi/branch/main/graph/badge.svg?token=86ZXJGB854)](https://codecov.io/gh/rjmalves/cfi)

Python package that contains a framework for dealing with custom file formats, modulating reading, data formatting and writing in a scalable and modular way.

## Summary

`cfinterface` is a framework for designing low-level interfaces that depends on complex text or binary file parsing. It provides components for modeling lines, registers, blocks and sections in a declarative way and aggregate these blocks as components for defining files.

Suppose that a complex text file needs to be parsed and the contents of lines with a specific identifier must be extracted and validated. For instance, the line follows the format:

```
DATA_HIGH  ID001   sudo.user  10/20/2025  901.25
```

If `DATA_HIGH` is the identifier that specifies the lines to be read, than one can model it with the `Register` class in the `cfinterface` framework.

```python
class DataHigh(Register):
    IDENTIFIER = "DATA_HIGH"
    IDENTIFIER_DIGITS = 9
    LINE = Line(
        [
            LiteralField(size=6, starting_position=11),
            LiteralField(size=9, starting_position=19),
            DatetimeField(size=10, starting_position=30, format="%M/$d/%Y"),
            FloatField(size=6, starting_position=42, decimal_digits=2),
        ]
    )
```

A `Register` depends on the definition of a `Line` object, that is composed of `Field` objects. By modeling these elements on a declarative way, the user gains access to reading / writing functions on the fly, and the `Register` may be added to a `RegisterFile` object, so that it can be read / written together with many other registers to files.

Despite the `Register` model, files can also be composed of `Blocks` and `Sections`, and their interfaces can be done to `text` or `binary` formats. For more information, the docs are available [here](https://rjmalves.github.io/cfinterface).

## Install

`cfinterface` requires python >= 3.10. It this requirement is met, than one may install the framework with

```
python -m pip install cfinterface
```

## Documentation

Guides, tutorials and references may be found at the package's official site: https://rjmalves.github.io/cfinterface
