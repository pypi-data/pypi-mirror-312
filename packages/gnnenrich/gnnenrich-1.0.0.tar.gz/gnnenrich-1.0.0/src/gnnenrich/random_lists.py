"""Random lists generation."""
# pylint: disable=unknown-option-value
from __future__ import annotations # For list[str] type hint in 3.7
import random
import typing

class RandomListsGenerator:
    """Generator of random lists.

    Generates random lists of string items (usually proteins or genes).

    Args:
        items: An iterable containing the string items.
        size: The size of each generated list.
        keep: When sets to True, stores the generated lists, that can be later
              retrieved with the get_lists() method.
        offset: If > 0, start by throwing away this number of random lists. This
                is useful for testing purposes, when using a single seed for
                random numbers and running in parallel, making sure each process
                or thread generates a unique set of random lists.
        length: If negative, never stops generating random lists. If positive,
                stops after having generated this number of lists.
    """

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def __init__(self, items: typing.Iterable[str], size: int,
                 keep: bool=False, offset: int=0, length: int=-1) -> None:

        self._items = list(items)
        self._size = size
        self._keep = keep
        self._offset = offset
        self._length = length
        self._count = 0
        if self._keep:
            self._lists: typing.List[typing.List[str]] = []

        if self._size > len(self._items):
            raise ValueError(f"The number of elements to sample ({self._size})"
                + " is greater than the number of available elements"
                + " ({len(self._items)}).")

        # Skip first lists
        for _ in range(self._offset):
            random.sample(self._items, self._size)

    @property
    def length(self) -> int:
        """The number of random lists configured."""
        return self._length

    @property
    def count(self) -> int:
        """The number of random lists generated up to now."""
        return self._count

    @property
    def offset(self) -> int:
        """The configured offset."""
        return self._offset

    @property
    def size(self) -> int:
        """The configured size."""
        return self._size

    def __iter__(self) -> 'RandomListsGenerator':
        """Gets the iterator on the random lists.

        Returns:
            Itself as an iterator.
        """
        return self

    def __next__(self) -> list[str]:
        """Generates a random list.
        
        Returns:
            A random list of <size> items.
        """

        # Done
        if self._length >= 0 and self._count >= self._length:
            raise StopIteration

        # Generate a new list
        lst = random.sample(self._items, self._size)
        self._count += 1

        # Keep the new list in memory
        if self._keep:
            self._lists.append(lst)

        return lst

    def get_lists(self) -> typing.List[typing.List[str]]:
        """Gets the generated random lists.
        
        If <keep> was set to True, returns the generated random lists, otherwise
        returns None.

        Returns:
            A list of all generated random lists up to now.
        """
        if self._keep:
            return self._lists
        return []

def generate_random_lists(items: list[str], n: int, m: int) -> \
        list[list[str]]:
    """Generates a series of random lists.

    Takes a list of string items, and randomly build n lists of m items.

    Args:
        items: an iterable containing the items.
        n: number of lists.
        m: the size of each generated list.
        
    Returns:
        A list of n lists of m items randomly chosen between the provided items.
    """
    random_lists = []
    gen = RandomListsGenerator(items, size=m, length=n)

    # Generate n lists
    for lst in gen:
        random_lists.append(lst)

    return random_lists
