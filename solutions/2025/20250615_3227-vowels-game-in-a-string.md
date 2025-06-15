# #3227. 字符串中的元音游戏 / Vowels Game in a String

> 难度：中等 · 标签：Math、String、Brainteaser、Game Theory · [LeetCode 链接](https://leetcode.com/problems/vowels-game-in-a-string/)

---

## 题目（英文原版）

**Description**

Alice and Bob are playing a game on a string.
You are given a string s, Alice and Bob will take turns playing the following game where Alice starts first:
The first player who cannot make a move on their turn loses the game. We assume that both Alice and Bob play optimally.
Return true if Alice wins the game, and false otherwise.
The English vowels are: a, e, i, o, and u.

**Examples**

**Example 1:**

```
Input: s = "leetcoder"
Output: true
Explanation: Alice can win the game as follows:
```

**Example 2:**

```
Input: s = "bbcd"
Output: false
Explanation: There is no valid play for Alice in her first turn, so Alice loses the game.
```

**Constraints**

- 1 <= s.length <= 105
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

Alice 和 Bob 正在一个字符串上进行游戏。  
给定字符串 `s`，Alice 和 Bob 将轮流进行以下游戏，Alice 先手：

- 在自己的回合中，玩家必须选择一个仍未被选过的字符位置 `i`，且 `s[i]` 必须是 **英文元音 (English vowels)** `a、e、i、o、u` 中的一个。  
- 选中的位置随后视为已被使用，后续任何回合都不能再次选择该位置。

第一个在自己的回合无法进行合法移动的玩家**输掉**游戏。我们假设 Alice 和 Bob 都采用**最优 (optimal)** 策略。

返回 `true` 表示 Alice 能赢得游戏，返回 `false` 表示 Alice 会输。

**英文元音 (English vowels)** 为：`a, e, i, o, u`。

---

### 示例

#### 示例 1
```text
Input: s = "leetcoder"
Output: true
Explanation: Alice 可以按以下方式获胜：
```
（此处省略具体步骤，只需保留原文的解释内容翻译即可）

#### 示例 2
```text
Input: s = "bbcd"
Output: false
Explanation: Alice 在第一回合没有任何合法的移动，因此直接输掉游戏。
```

---

### 约束条件

- `1 <= s.length <= 10^5`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把游戏 **完整地模拟** 一遍：

1. 先遍历字符串 `s`，找出所有元音字母（`a, e, i, o, u`）。  
2. 按照“轮流”规则：  
   - 轮到 **Alice** 时，从当前字符串中任选一个元音并把它删除（这里可以随便选第一个元音，结果不影响胜负，因为两人都假设是「最优」的）。  
   - 轮到 **Bob** 时，同样删除一个元音。  
3. 当轮到某人时，字符串里已经没有元音可删，这个人 **输**，游戏结束。  

> **类比**：把字符串想象成一行排好的字母卡片，元音卡片就像「可以被抽走的特殊卡」。每回合抽走一张，抽不到就输了。

**为什么这种方法能得到正确答案**  
- 规则中只要「有没有元音」决定是否还能继续玩。只要我们真实地把元音逐个删掉，最终谁先面对「空的元音池」就和题目要求完全一致。  

**复杂度分析（大白话）**  
- 每一次删除都要重新遍历一次字符串来找下一个元音。最坏情况下，字符串长度是 `n`，而我们要删掉 `k`（`k ≤ n`）个元音。于是总共要做大约 `n + (n‑1) + (n‑2) + … + (n‑k+1)` 次遍历，数量级是 **`O(n²)`**。  
  - **`O(n²)`** 的含义可以想象成「把一本 100 页的书每页都读 100 次」——工作量会随 `n` 的平方快速增长。  
- 只用了原来的字符串和几个计数器，额外空间是 **`O(1)`**（常数级），即几块小纸条的大小。

#### 代码（Python）

```python
def aliceWins_bruteforce(s: str) -> bool:
    # 1. 把字符串转成列表，方便删除字符
    chars = list(s)
    # 2. 记录轮到的是 Alice 还是 Bob，True 表示 Alice 的回合
    alice_turn = True

    # 3. 循环直到找不到元音
    while True:
        # 4. 找到第一个元音的位置
        idx = -1
        for i, ch in enumerate(chars):
            if ch in {'a', 'e', 'i', 'o', 'u'}:
                idx = i
                break

        # 5. 没有元音了，当前玩家输
        if idx == -1:
            # 如果是 Alice 的回合找不到元音，说明 Alice 输，返回 False
            return not alice_turn

        # 6. 删除这个元音（模拟一次合法的操作）
        del chars[idx]

        # 7. 换下一个玩家继续游戏
        alice_turn = not alice_turn
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 每一次删除都要重新遍历剩余字符，工作量随字符数的平方增长。  
- **空间复杂度**：`O(1)` — 只用了常数个额外变量（列表本身是对原字符串的复制，算作输入本身的空间）。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到，**真正决定胜负的并不是具体怎么删，而是元音的总数**。  
原因如下：

1. **每回合只能删掉 ********一个**元音**（不管删哪个，元音总数就会减 1）。  
2. 游戏结束的唯一条件是「没有元音可删」。  
3. 因此游戏进行的步数恰好等于 **初始元音个数** `cnt`。  
4. Alice 先手，若 `cnt` 为 **奇数**，她会在第 `cnt` 步（即最后一步）拿到“删最后一个元音”的机会，Bob 接下来无棋可走 → **Alice 赢**。  
5. 若 `cnt` 为 **偶数**，最后一步是 Bob 执行，Alice 在没有元音时轮到她 → **Alice 输**。  

> **类比**：把元音看成棋盘上的“子”。两位玩家轮流把子拿走，谁先把最后一个子拿走谁就赢。显然，子是奇数个，先手必胜；子是偶数个，先手必败。

**特殊情况**  
- **没有元音** (`cnt == 0`) → 一开始 Alice 就没有合法操作，直接输，返回 `False`。  
- 以上规则已经覆盖了「奇数可以一次性把整串删掉」的情况，因为一次删除整串也等价于「把最后一个元音删掉」——只要总数是奇数，先手一定能赢。

**核心技巧**：**只需要统计元音的个数**，不需要真的去模拟删除过程。  

#### 代码（Python）

```python
def aliceWins(s: str) -> bool:
    """
    判断 Alice 是否在游戏中获胜。
    思路：只要统计元音的数量，奇数 Alice 胜，偶数 Alice 败。
    """
    # 1. 定义元音集合，查表速度快（相当于字典的查找，O(1)）
    vowels = {'a', 'e', 'i', 'o', 'u'}

    # 2. 一次遍历统计元音个数
    cnt = 0
    for ch in s:
        if ch in vowels:
            cnt += 1

    # 3. 奇数赢，偶数输
    return cnt % 2 == 1
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次字符串，`n` 是字符串长度。  
  - 相比 `O(n²)`，这就像把「读 100 页的书」一次性搞定，而不是每页读 100 次，速度提升了 **n 倍**。  
- **空间复杂度**：`O(1)` — 只用了几个计数器和一个常量大小的集合，和输入大小无关。

---

## 心得

- **核心技巧**：**把游戏抽象成“每回合只能把一个元音消掉”，于是胜负只与元音总数的奇偶性有关**。  
- **适用的题型**：  
  1. **取子游戏**（如 Nim、Stone Game 系列）——只要每回合固定移除 1 个单位，奇偶决定胜负。  
  2. **只关注计数的游戏**（如 “Remove Palindromic Substrings” 中的计数版）。  
  3. **只要判断是否存在合法操作的游戏**（如 “Stone Game IV” 中的 DP 归纳，若不存在则先手必败）。  
- **一句话总结解题钥匙**：**把动态过程简化为“计数的奇偶”，不必真的去模拟每一步**。

## 反思

- **第一反应**：看到“谁先不能移动就输”，立刻想到**模拟整个游戏**。  
- **最容易踩的坑**：  
  - 忘记把 **字母全部转成小写**（题目已保证全是小写，这里不需要额外处理）。  
  - 错把 **元音的出现次数** 当成 “可以一次性删除所有元音” 的条件，导致错误的判断。  
  - 误以为可以一次删掉任意子串导致复杂的 DP，实际上不需要。  
- **下次遇到同类题**：第一步先 **思考每回合的“资源”到底是什么**（这里是元音），再问自己“每回合只能消耗多少”，如果是 **固定 1**，就直接看 **奇偶**；如果不是，再考虑更高级的 DP 或贪心。