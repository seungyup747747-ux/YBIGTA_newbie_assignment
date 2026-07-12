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
- 일단 Trie부터 구현하기
- count 구현하기
- main 구현하기
"""


def count(trie: Trie, query_seq: str) -> int:
    """
    trie - 이름 그대로 trie
    query_seq - 단어 ("hello", "goodbye", "structures" 등)

    returns: query_seq의 단어를 입력하기 위해 버튼을 눌러야 하는 횟수
    """
    pointer = 0
    cnt = 0

    for element in query_seq:
        if len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1

        new_index = -1
        
        for child_index in trie[pointer].children:
            if trie[child_index].body == element:
                new_index = child_index
                break
        
        assert new_index != -1
        pointer = new_index

    return cnt + int(len(trie[0].children) == 1)


def main() -> None:
    lines = sys.stdin.read().splitlines()
    idx = 0
    answers = []
    
    while idx < len(lines):
        n = int(lines[idx])
        idx += 1
        
        words = lines[idx:idx+n]
        idx += n
        
        trie: Trie[str] = Trie()
        
        for word in words:
            trie.push(word)
            
        total = 0
        
        for word in words:
            total += count(trie, word)
            
        answers.append(f"{total / n:.2f}")
    
    print("\n".join(answers))


if __name__ == "__main__":
    main()