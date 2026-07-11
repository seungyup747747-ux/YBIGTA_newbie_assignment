from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable


"""
TODO:
- Trie.push 구현하기
- (필요할 경우) Trie에 추가 method 구현하기
"""


T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: list[int] = field(default_factory=lambda: [])
    is_end: bool = False


class Trie(list[TrieNode[T]]):
    def __init__(self) -> None:
        super().__init__()
        self.append(TrieNode(body=None))

    def push(self, seq: Iterable[T]) -> None:
        current = 0

        for element in seq:
            new_index: Optional[int] = None

            for child_index in self[current].children:
                if self[child_index].body == element:
                    new_index = child_index
                    break

            if new_index is None:
                self.append(TrieNode(body=element))
                new_index = len(self) - 1
                self[current].children.append(new_index)
                
            current = new_index

        self[current].is_end = True

    # 구현하세요!