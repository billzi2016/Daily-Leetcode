# #2546. 通过位运算使字符串相等 / Apply Bitwise Operations to Make Strings Equal

> 难度：中等 · 标签：String、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/apply-bitwise-operations-to-make-strings-equal/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed binary strings s and target of the same length n. You can do the following operation on s any number of times:
For example, if s = "0110", you can choose i = 0 and j = 2, then simultaneously replace s[0] with (s[0] OR s[2] = 0 OR 1 = 1), and s[2] with (s[0] XOR s[2] = 0 XOR 1 = 1), so we will have s = "1110".
Return true if you can make the string s equal to target, or false otherwise.

**Examples**

**Example 1:**

```
Input: s = "1010", target = "0110"
Output: true
Explanation: We can do the following operations:
- Choose i = 2 and j = 0. We have now s = "0010".
- Choose i = 2 and j = 1. We have now s = "0110".
Since we can make s equal to target, we return true.
```

**Example 2:**

```
Input: s = "11", target = "00"
Output: false
Explanation: It is not possible to make s equal to target with any number of operations.
```

**Constraints**

- n == s.length == target.length
- 2 <= n <= 105
- s and target consist of only the digits 0 and 1.

---

## 题目（中文翻译）

给定两个 **0 索引（0-indexed）** 的二进制字符串（binary strings）`s` 与 `target`，两者长度相同为 `n`。你可以对 `s` 任意次执行以下操作（operation）：

- 选择两个下标 `i` 与 `j`（`i != j`），同时将  
  `s[i]` 替换为 `s[i] OR s[j]`（按位或），  
  `s[j]` 替换为 `s[i] XOR s[j]`（按位异或）。

例如，若 `s = "0110"`，选择 `i = 0`、`j = 2`，则同时把 `s[0]` 替换为 `0 OR 1 = 1`，`s[2]` 替换为 `0 XOR 1 = 1`，得到 `s = "1110"`。

如果能够通过若干次上述操作使得 `s` 与 `target` 相等，则返回 `true`；否则返回 `false`。

## 示例

### 示例 1
**输入**  
```
s = "1010", target = "0110"
```
**输出**  
```
true
```
**解释**  
我们可以按如下顺序进行操作：
- 选择 `i = 2`、`j = 0`，此时 `s = "0010"`。  
- 选择 `i = 2`、`j = 1`，此时 `s = "0110"`。

因为可以把 `s` 变为 `target`，返回 `true`。

### 示例 2
**输入**  
```
s = "11", target = "00"
```
**输出**  
```
false
```
**解释**  
无论进行多少次操作，都无法把 `s` 变为 `target`，因此返回 `false`。

## 约束条件

- `n == s.length == target.length`
- `2 <= n <= 10^5`
- `s` 和 `target` 仅由字符 `0` 和 `1` 组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的操作** 都枚举一遍，看能否一步步把 `s` 变成 `target`。  
我们可以把每一次「选 i、j」看成一次状态转移：

| 原始位 (a, b) | 经过操作后的位 (a', b') |
|--------------|--------------------------|
| (0, 0)       | (0, 0)   （什么也不变） |
| (0, 1) / (1, 0) | (1, 1)   （两个位置都变成 1） |
| (1, 1)       | (1, 0)   （把一个 1 “搬走”） |

于是我们可以把 **每一种二进制字符串** 当成图中的一个节点，**一次合法操作** 当成一条有向边。  
从起点 `s` 出发，用 **宽度优先搜索（BFS）** 或 **深度优先搜索（DFS）** 遍历整个图，若遍历过程中出现 `target`，则返回 `True`，否则返回 `False`。

> **类比**：想象你在一座城市里，街道就是所有可能的「一次位操作」，每到一个交叉口（一个字符串），你可以继续沿着街道走，最终能否抵达目标地点（`target`）？

#### 代码（Python）

```python
from collections import deque

def can_convert_bruteforce(s: str, target: str) -> bool:
    n = len(s)
    # BFS 用队列保存待探索的字符串
    q = deque([s])
    visited = {s}                     # 防止重复遍历

    while q:
        cur = q.popleft()
        if cur == target:             # 找到目标
            return True

        # 枚举所有 i、j（i != j）
        for i in range(n):
            for j in range(i + 1, n):
                a, b = cur[i], cur[j]

                # 根据上表计算新位
                a_new = str(int(a) | int(b))          # OR
                b_new = str(int(a) ^ int(b))          # XOR

                # 生成新字符串
                nxt = list(cur)
                nxt[i], nxt[j] = a_new, b_new
                nxt = ''.join(nxt)

                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)

    # BFS 结束仍未找到 target
    return False
```

> **注意**：代码里每一步都在把字符 `'0'/'1'` 转成整数再做位运算，随后再转回字符，保证可读性。

#### 复杂度  

- **时间复杂度**：`O(2^n)`（指数级）  
  解释：每个二进制字符串都是图中的一个节点，节点数最多是 `2^n`（所有可能的 0/1 组合），而我们最坏情况下可能要遍历全部节点。对初学者来说，`O(2^n)` 就相当于“随着 n 增长，计算量会像翻倍一样疯狂增长”，在 n=20 以后就已经不可接受了。

- **空间复杂度**：`O(2^n)`  
  解释：需要保存已经访问过的所有字符串，同样是指数级的空间。

> **结论**：暴力搜索只能在 `n` 极小（比如 ≤10）时勉强跑得完，根本不适合本题的约束（`n` 可达 10⁵）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **状态空间太大**，所以我们必须寻找 **直接的数学规律**，不去真的模拟每一次操作。

观察位操作的三种情况：

| (a, b) | 结果 (a', b') | 1 的数量变化 |
|--------|--------------|--------------|
| (0, 0) | (0, 0)       | 0 → 0，保持不变 |
| (0, 1) / (1, 0) | (1, 1) | +1（从 1 个 1 变成 2 个） |
| (1, 1) | (1, 0)       | -1（从 2 个 1 变成 1 个） |

> **关键观察 1**：只要字符串中 **至少有一个 `1`**，我们就可以 **把 `1` 复制**（通过 `(0,1)` → `(1,1)`）或 **把两个 `1` 合并成一个 `0`**（通过 `(1,1)` → `(1,0)`）。于是 **`1` 的总数量** 可以 **任意增减**，但每次增减的幅度只能是 **1**。

> **关键观察 2**：如果整个字符串 **全是 `0`**，任意两位都是 `(0,0)`，操作根本不会改变任何位。也就是说 **全 0 的串是“死状态”，永远只能保持全 0**。

> **关键观察 3**：要把 **最后一个 `1`** 消除，需要把它和另一个 `1` 配对成 `(1,1) → (1,0)`，这会留下 **仍然是一个 `1`**。所以 **只要还有至少一个 `1`，我们永远无法把所有 `1` 完全消掉**，除非一开始就是全 0。

把这三条观察组合起来，就得到 **判定条件**：

- **如果 `s` 与 `target` 中恰好有一个是全 0、另一个不是全 0 → 不可能**（因为全 0 永远动弹不得，而非全 0 必须保留至少一个 `1`）。
- **其他所有情况都是可能的**。因为只要两串都含有至少一个 `1`，我们可以：
  1. 把 `s` 中的 `1` 复制到任意位置，制造出足够多的 `1`；
  2. 再把多余的 `1` 两两配对消掉，最终把 `s` 调整成和 `target` 完全相同的形状。

> **类比**：把 `1` 看成“一颗种子”。只要花园里还有一颗种子，你就可以 **播种**（复制）或 **拔除**（两颗合并成一颗），但如果花园里根本没有种子（全 0），你就永远只能保持空地。

#### 代码（Python）

```python
def canConvert(s: str, target: str) -> bool:
    """
    判断是否能通过题目定义的位操作把 s 变成 target。
    思路：只要两串同时含有 1，或者两串都是全 0，答案必定为 True；
          否则为 False。
    """
    has_one_s = '1' in s          # s 中是否至少有一个 1
    has_one_t = '1' in target     # target 中是否至少有一个 1

    # 两者“是否全 0”的状态不相同 → 不可能
    if has_one_s != has_one_t:
        return False
    # 状态相同（都全 0 或都至少有一个 1） → 必然可达
    return True
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只需要遍历两遍字符串（各一次 `in` 检查），相当于线性时间。`O(n)` 意味着 **当 `n` 增大到 10⁵ 时，程序仍然跑得很快**（只需要几毫秒）。

- **空间复杂度**：`O(1)`  
  只使用了常数个布尔变量，不随输入规模增长。

> 与暴力解相比，最优解把指数级的搜索直接压缩成 **常数级的判断**，实现了巨大的性能提升。

---

## 心得

- **核心技巧**：**把位操作的全局影响抽象为“是否存在 `1`”**，从而把复杂的状态转移简化为对“是否全 0”这一全局属性的判定。
- **适用的题型**  
  1. **只关心是否全 0 / 是否包含 1 的字符串题**（例如 “Make Two Strings Equal With Operations” 等）。  
  2. **只涉及局部位运算但整体不变性的题**（如 “Flip Bits to Make All Zeros”）。  
  3. **需要判断可达性的图论题**，但图的结构可以用全局不变量来快速判断（如 “Transform String With Swaps”）。
- **一句话总结解题钥匙**：**只要两个字符串的“是否全 0”状态相同，就一定可以相互转化**。

---

## 反思

- **第一反应**：先想到 BFS/DFS 暴力搜索，想把每一步都模拟出来。
- **最容易踩的坑**  
  - 忽略 **全 0 串的不可动性**，导致误判可以把 `111…1` 变成 `000…0`。  
  - 没有注意到 **只能一次增减 1**，以为只要有相同的 `1` 个数就一定可以相等（实际上只要两串都至少有一个 `1` 即可）。  
  - 边界条件：`n = 2` 时仍然适用，同样要检查全 0 情况。
- **下次遇到同类题**，第一步应该 **找出全局不变量**（比如是否全 0、是否全 1、奇偶性等），判断这些不变量是否在起始状态和目标状态之间保持一致，若不一致直接返回 `False`，否则再考虑构造性证明。