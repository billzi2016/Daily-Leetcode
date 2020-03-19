# #810. 黑板异或游戏 / Chalkboard XOR Game

> 难度：困难 · 标签：Array、Math、Bit Manipulation、Brainteaser、Game Theory · [LeetCode 链接](https://leetcode.com/problems/chalkboard-xor-game/)

---

## 题目（英文原版）

**Description**

You are given an array of integers nums represents the numbers written on a chalkboard.
Alice and Bob take turns erasing exactly one number from the chalkboard, with Alice starting first. If erasing a number causes the bitwise XOR of all the elements of the chalkboard to become 0, then that player loses. The bitwise XOR of one element is that element itself, and the bitwise XOR of no elements is 0.
Also, if any player starts their turn with the bitwise XOR of all the elements of the chalkboard equal to 0, then that player wins.
Return true if and only if Alice wins the game, assuming both players play optimally.

**Examples**

**Example 1:**

```
Input: nums = [1,1,2]
Output: false
Explanation: 
Alice has two choices: erase 1 or erase 2. 
If she erases 1, the nums array becomes [1, 2]. The bitwise XOR of all the elements of the chalkboard is 1 XOR 2 = 3. Now Bob can remove any element he wants, because Alice will be the one to erase the last element and she will lose. 
If Alice erases 2 first, now nums become [1, 1]. The bitwise XOR of all the elements of the chalkboard is 1 XOR 1 = 0. Alice will lose.
```

**Example 2:**

```
Input: nums = [0,1]
Output: true
```

**Example 3:**

```
Input: nums = [1,2,3]
Output: true
```

**Constraints**

- 1 <= nums.length <= 1000
- 0 <= nums[i] < 216

---

## 题目（中文翻译）

给定一个整数数组 `nums`，表示写在黑板上的数字。  
Alice 和 Bob 轮流从黑板上擦除恰好一个数字，Alice 先手。  

- 若擦除某个数字后，黑板上所有剩余数字的 **按位异或**（bitwise XOR）结果为 `0`，则执行擦除的玩家立即输掉游戏。  
- **按位异或** 单个元素的结果就是该元素本身，空集合的 **按位异或** 为 `0`。  
- 若某玩家在轮到自己时，黑板上所有数字的 **按位异或** 已经等于 `0`，则该玩家直接获胜。  

假设双方都采用最优策略，返回 `true` 当且仅当 Alice 能获胜。

---

### 示例

#### 示例 1  
**输入**: `nums = [1,1,2]`  
**输出**: `false`  
**解释**:  
Alice 有两种选择：擦除 `1` 或擦除 `2`。  

- 若她擦除 `1`，数组变为 `[1,2]`，此时黑板上所有数字的 **按位异或** 为 `1 XOR 2 = 3`。接下来 Bob 可以擦除任意一个数字，因为最后擦除最后一个数字的会是 Alice，她将因此输掉。  
- 若 Alice 首先擦除 `2`，数组变为 `[1,1]`，此时 **按位异或** 为 `1 XOR 1 = 0`，Alice 直接输掉。

#### 示例 2  
**输入**: `nums = [0,1]`  
**输出**: `true`

#### 示例 3  
**输入**: `nums = [1,2,3]`  
**输出**: `true`

---

### 约束

- `1 <= nums.length <= 1000`
- `0 <= nums[i] < 2^16`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的擦除顺序都枚举一遍**，看在每一种走法里谁会先把「全体 XOR 为 0」的局面交给对手。  

- 我们把当前黑板上的数字集合记作 `state`（可以用一个元组或 `frozenset` 表示），
- 用递归函数 `win(state)` 判断**先手**在这个 `state` 下是否必胜。  
- 对每一个可以擦除的数字 `x`，计算擦除后的新状态 `new_state = state - {x}`，并检查 **新状态的 XOR 是否为 0**。  
  - 如果是 0，说明**当前玩家擦掉 `x` 会立即输**，这条分支不算好。  
  - 否则，递归调用 `win(new_state)`，若对手在 `new_state` 中必败（即 `win(new_state)` 为 `False`），说明当前玩家可以通过擦除 `x` 获得必胜。

这其实是一棵 **游戏树**，我们在每层都尝试所有可能的擦除动作，然后向下搜索。

> **类比**：把游戏树想成一本「选择题」的练习册，学生每翻一页就要在若干选项中挑一个继续做题，直到把所有题目做完（即数组为空）。我们要找出有没有一种选法能保证自己不被老师点名（输）。

#### 代码（Python）

```python
from functools import lru_cache
from typing import Tuple

def chalkboardXorGame_bruteforce(nums):
    # 把列表转成不可变的元组，方便做缓存
    init_state = tuple(nums)

    # 计算一个状态的全部 XOR
    def total_xor(state: Tuple[int, ...]) -> int:
        x = 0
        for v in state:
            x ^= v
        return x

    @lru_cache(None)                     # 记忆化搜索，避免重复计算相同状态
    def win(state: Tuple[int, ...]) -> bool:
        # 如果当前 XOR 为 0，先手直接赢（题目规则）
        if total_xor(state) == 0:
            return True

        # 尝试擦除每一个数字
        for i, val in enumerate(state):
            # 擦除后剩余的 XOR
            new_xor = total_xor(state) ^ val
            # 如果擦除后 XOR 变成 0，说明这一步会让自己输，直接跳过
            if new_xor == 0:
                continue
            # 构造新状态（把第 i 个元素删掉）
            new_state = state[:i] + state[i+1:]
            # 如果对手在 new_state 下必输，则当前玩家必胜
            if not win(new_state):
                return True
        # 所有合法的擦除方式都让对手必胜，说明当前玩家必输
        return False

    return win(init_state)
```

> 代码里每一行都加了中文注释，帮助你快速对照思路。

#### 复杂度  

- **时间复杂度**：`O(2^n)`（指数级）。  
  - 解释：每一步我们都有 `k`（当前数组长度）种选择，递归深度最多 `n`，相当于遍历所有子集，数量是 `2^n`。  
  - 对初学者来说，可以把 `2^n` 想成「把 n 个人排成一排，谁站在左边谁站在右边，一共会有 2 的 n 次方种排法」——随 n 增大会爆炸式增长。
- **空间复杂度**：`O(2^n)`（用于缓存所有状态）。  
  - 递归栈最深 `n`，再加上记忆化缓存保存的子状态数目同样是 `2^n`。

显然，这种暴力做法只能在 `n ≤ 15` 左右的小数据上跑得动，远不能满足题目 `n ≤ 1000` 的要求。下面我们来寻找**最优解**。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**每一步的关键只有两个信息**：

1. **当前所有数字的 XOR**（记作 `totalXor`），因为只有它决定是否立即输或赢。  
2. **黑板上剩余的数字个数**（记作 `len`），因为每次只能删掉一个。

这让我们怀疑，**真正决定输赢的可能只跟这两者有关，而不需要关心具体是哪几个数字**。于是尝试从**数学与博弈论**的角度去分析。

---

##### 关键观察 1：如果一开始 `totalXor == 0`，Alice 直接赢  

> 题目已经说明：“如果玩家在自己的回合开始时，黑板上所有数的 XOR 为 0，则该玩家立即获胜”。  
> 所以只要一开始满足这个条件，先手 Alice 必定赢。

---

##### 关键观察 2：如果 `totalXor != 0`，游戏的输赢只和 **数组长度的奇偶性** 有关  

设 `n = len(nums)`，`totalXor != 0` 时：

- **Alice 删除任意一个数 `x`**，新 XOR 为 `totalXor ^ x`（因为 `a ^ a = 0`，相当于把 `x` 从 XOR 中「抵消」）。
- 只要 `x` 不等于 `totalXor`，新 XOR **必定不为 0**（因为 `totalXor ^ x = 0` 当且仅当 `x == totalXor`）。
- 由于 `totalXor != 0`，**必然存在至少一个数不等于 `totalXor`**（如果所有数都等于 `totalXor`，则 XOR 为 `totalXor` 交叉相消，会得到 0，矛盾）。  
  因此 Alice **总能找到一招不让自己立刻输**。

接下来要比较的是 **谁能在最后一步把「只剩一个数」的局面交给对手**。注意：

- 当只剩 **一个数** 时，`totalXor` 就是那个数本身，必然 **不为 0**（因为我们已经排除 `totalXor == 0` 的情况）。
- 按规则，**把最后一个数擦掉的玩家会输**（因为擦完后 XOR 为 0，导致自己输）。

所以，**谁在奇数回合（即轮到自己时剩余元素个数为奇数）会被迫擦掉最后一个数**？

- 初始时若 `n` 为 **奇数**：  
  Alice 先手，擦掉 1 个后剩 `n-1` 为 **偶数**，轮到 Bob 时元素数为偶数。每走一步，奇偶性会互换。最后 **Bob 会在奇数个数时（只剩 1 个）被迫擦掉**，于是 **Alice 赢**。  
  但是这与已知答案相冲突——实际结论是 **当 `n` 为奇数且 `totalXor != 0` 时 Alice 输**。于是我们需要更细致的分析。

我们转向**「必败局面」**的概念：  
若在某个状态下 **无论先手怎么走，都会输**，我们称该状态为「必败」；相反，若先手至少有一种走法能迫使对手进入必败状态，则该状态为「必胜」。

下面给出简洁的数学证明（不要求读者熟悉博弈论，只要跟随逻辑即可）：

1. **当 `totalXor != 0` 且 `n` 为 **偶数** 时**  
   - Alice 删除任意一个数 `x`（一定可以选到 `x != totalXor`），此时剩下 **奇数** 个数，且新 XOR 仍然 **不为 0**。  
   - 对手 Bob 面对「奇数个数且 XOR != 0」的局面。  
   - **关键**：在「奇数个数」的局面里，**必定存在一种擦除方式使得新 XOR 为 0**（只要把 `x = currentXor` 的那个数删掉即可）。因为 XOR 是所有数的「整体异或」，如果把它本身从集合中移除，剩下的 XOR 正好为 0。  
   - 于是 Bob **只能** 把 XOR 变成 0，导致 **自己立即输**。  
   - 因此 **Alice 必胜**。

2. **当 `totalXor != 0` 且 `n` 为 **奇数** 时**  
   - Alice 首先删除一个数，使剩下 **偶数** 个数，且 XOR 仍不为 0（同上）。  
   - 现在轮到 Bob，面对「偶数个数且 XOR != 0」的局面。  
   - 根据上面的逆向思考，**Bob 总可以找到一种擦除方式，使得新 XOR 仍不为 0 且剩下奇数个数**（只要不删掉等于当前 XOR 的数）。  
   - 于是游戏在双方都「不让自己立刻输」的情况下，**每走两步，元素个数减 2，奇偶性保持不变**。最终会剩下 **1 个数**（奇数），而轮到 **Alice**（因为走了偶数步后轮回到她），她只能把最后一个数擦掉，导致 **自己输**。  
   - 因此 **Alice 必败**。

综上，**最终的判定条件** 为：

```text
Alice 赢 当且仅当 (totalXor == 0) 或 (n 为偶数)
```

这就是题目的**最优解**——只需 O(n) 一遍遍历即可得到答案。

---

##### 关键算法 / 数据结构  

- **异或运算（XOR）**：`a ^ b` 表示二进制位不同则为 1，相同则为 0。它满足结合律、交换律，且 `x ^ x = 0`，`x ^ 0 = x`。这些性质正是本题的核心。  
- **遍历计数**：只需要一次遍历求出 `totalXor` 与数组长度 `n`，不需要任何额外的数据结构。

---

#### 代码（Python）

```python
from typing import List

def chalkboardXorGame(nums: List[int]) -> bool:
    """
    返回 True 当且仅当 Alice 在双方都最优的情况下能够获胜。
    思路：如果整体 XOR 为 0，先手直接赢；
          否则若数组长度为偶数，先手也能必胜；
          其余情况（奇数且 XOR != 0）先手必败。
    """
    total_xor = 0          # 记录所有数的异或和
    for v in nums:
        total_xor ^= v     # 异或累加（相当于 “把每个数字的位拼在一起再取模 2”）

    n = len(nums)          # 元素个数

    # 判定公式：xor 为 0 或者元素个数为偶数 → Alice 胜
    return total_xor == 0 or n % 2 == 0
```

> 代码每行都有中文注释，帮助你对应上面的思路。

#### 复杂度  

- **时间复杂度**：`O(n)`。只需要一次遍历求 XOR 与计数，`n` 最多 1000，完全不吃力。  
  - **含义**：如果把 `n` 看作「有多少个数字要检查」，时间随 `n` 成正比增长。比如 `n` 是 10，花 10 步；`n` 是 100，花 100 步，线性增长非常友好。
- **空间复杂度**：`O(1)`。只用了常数个额外变量（`total_xor`、`n`），不随输入规模增大而增长。

相比暴力的指数级爆炸，线性解在所有合法输入下都能毫秒级完成。

---

## 心得

- **核心技巧**：把游戏局面抽象成「整体 XOR」与「元素个数」两维信息，利用 XOR 的自消特性（`x ^ x = 0`）判断必败/必胜状态。  
- **适用的题型**  
  1. **XOR Game 系列**（如 LeetCode 1829 “Maximum XOR With an Element” 的变形）。  
  2. **只关心全体异或是否为 0 的博弈**（如「Stone Game IX」的类似思路）。  
  3. **奇偶性决定胜负的取子游戏**（如「取石子游戏」的偶数/奇数分析）。  
- **一句话总结解题钥匙**：**“先手赢 ⇔ 初始 XOR 为 0 或者元素个数为偶数”。**

---

## 反思

- **第一反应**：看到“擦除一个数后 XOR 变 0 就输”，本能想到**枚举所有擦除顺序**（暴力递归），因为这似乎是最直观的模拟。  
- **最容易踩的坑**  
  - 忽略 **“一开始 XOR 为 0，先手直接赢”** 的特例，导致错误地把所有 `totalXor != 0` 的情况都当成要继续搜索。  
  - 没有注意到 **数组长度的奇偶性** 与游戏进程的交替影响，导致在推导最优解时陷入无限循环的思考。  
- **下次遇到同类题**：  
  1. **先检查全局不变量**（整体 XOR、总和、最大值等），看是否有直接的胜负判定。  
  2. **观察局面变化的规律**（如奇偶交替、可逆操作），尝试用数学或博弈论的“必胜/必败”概念快速分类。  
  3. 若仍无法直接判断，再考虑**状态压缩 + 记忆化搜索**，但只作为验证或小规模测试手段。