from lib import Trie
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