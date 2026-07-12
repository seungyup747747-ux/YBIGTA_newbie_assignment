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


import sys


"""
TODO:
- 일단 lib.py의 Trie Class부터 구현하기
- main 구현하기

힌트: 한 글자짜리 자료에도 그냥 str을 쓰기에는 메모리가 아깝다...
"""


def main() -> None:
    MOD = 1_000_000_007

    input = sys.stdin.readline

    n = int(input())

    trie: Trie[int] = Trie()

    for _ in range(n):
        name = input().strip()
        trie.push(ord(ch) - ord("A") for ch in name)

    factorial = [1] * (n + 1)

    for i in range(1, n + 1):
        factorial[i] = factorial[i - 1] * i % MOD

    def dfs(node_index: int) -> int:
        node = trie[node_index]

        group_count = len(node.children)

        if node.is_end:
            group_count += 1

        result = factorial[group_count]

        for child_index in node.children:
            result *= dfs(child_index)
            result %= MOD

        return result

    print(dfs(0))


if __name__ == "__main__":
    main()