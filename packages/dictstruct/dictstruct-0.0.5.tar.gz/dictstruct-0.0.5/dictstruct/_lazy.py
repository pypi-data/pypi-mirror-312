from dictstruct._main import DictStruct


class LazyDictStruct(DictStruct, frozen=True):  # type: ignore [call-arg,misc]
    """
    A subclass of :class:`DictStruct` that supports Just-In-Time (JIT) decoding of field values.

    `LazyDictStruct` is designed for developers who need to efficiently handle large or complex data structures, particularly when working with serialized data formats like JSON. By storing field values in a raw, undecoded format, this class allows for deferred decoding, meaning that data is only decoded when accessed. This approach can lead to significant performance improvements and reduced memory usage, especially in scenarios where not all fields are always needed.

    Key Features:
    - **JIT Decoding**: Decode data only when accessed, saving processing time and memory.
    - **Immutable Structure**: As a frozen dataclass, instances are immutable, ensuring data integrity after creation.
    - **Compatibility**: Inherits from :class:`DictStruct`, making it compatible with the standard dictionary API, allowing for easy integration with existing codebases that rely on dictionary-like data structures.

    Use Cases:
    - Handling large JSON responses from APIs where only a subset of the data is needed at any given time.
    - Optimizing applications that process data lazily, improving startup times and reducing resource consumption.

    Example:
        >>> import msgspec
        >>> from functools import cached_property
        >>> class MyStruct(LazyDictStruct):
        ...     _myField: msgspec.Raw = msgspec.field(name='myField')
        ...     @cached_property
        ...     def myField(self) -> YourGiantJsonObject:
        ...         '''Decode the raw JSON data into a python object when accessed.'''
        ...         return msgspec.json.decode(self._myField, type=YourGiantJsonObject)
        ...
        >>> # Encode data into a raw JSON format
        >>> raw_data = msgspec.json.encode({"myField": "some value"})
        >>> # Create an instance of MyStruct with the raw data
        >>> my_struct = MyStruct(_myField=raw_data)
        >>> # Access the decoded field value
        >>> print(my_struct.myField)
        "some value"

    See Also:
        :class:`DictStruct` for the base class implementation.
    """

    def __init_subclass__(cls, *args, **kwargs):
        """
        Initialize a subclass of :class:`LazyDictStruct`.

        This method resolves any lazy field names (prefixed with an underscore) and overwrites
        `cls.__struct_fields__` so it contains the names of the materialized properties
        defined on your subclass.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        See Also:
            :class:`DictStruct` for the base class implementation.
        """
        super().__init_subclass__(*args, **kwargs)

        if cls.__name__ == "StructMeta":
            return

        try:
            struct_fields = cls.__struct_fields__
        except AttributeError:
            # TODO: debug this
            # raise TypeError(cls, dir(cls), issubclass(cls, Struct))
            return

        resolved_fields = tuple(
            field[1:] if field[0] == "_" else field for field in struct_fields
        )
        cls.__struct_fields__ = resolved_fields
