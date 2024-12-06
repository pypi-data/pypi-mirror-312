from typing import IO
from cfinterface.components.section import Section


class DefaultSection(Section):
    """
    A class for representing a default section, which contains no data
    and is used for representing empty data.
    """

    __slots__ = []

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, DefaultSection):
            return False
        return self.data == o.data

    def read(self, file: IO, *args, **kwargs) -> bool:
        self.data = file.readline()
        return True

    def write(self, file: IO, *args, **kwargs) -> bool:
        if len(self.data) > 0:
            file.write(self.data)
        return True
