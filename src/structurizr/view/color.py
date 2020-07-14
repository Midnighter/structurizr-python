import pydantic.color


class Color(pydantic.color.Color):
    def as_hex(self) -> str:
        """
        Hex string representing the color
        """
        values = [pydantic.color.float_to_255(c) for c in self._rgba[:3]]
        if self._rgba.alpha is not None:
            values.append(pydantic.color.float_to_255(self._rgba.alpha))

        as_hex = "".join(f"{v:02x}" for v in values)
        return "#" + as_hex

    def __str__(self) -> str:
        return self.as_hex()
