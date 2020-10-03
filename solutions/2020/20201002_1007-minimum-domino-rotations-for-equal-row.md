# #1007. 最小旋转次数使两行相等 / Minimum Domino Rotations For Equal Row

> 难度：中等 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-domino-rotations-for-equal-row/)

---

## 题目（英文原版）

**Description**

In a row of dominoes, tops[i] and bottoms[i] represent the top and bottom halves of the ith domino. (A domino is a tile with two numbers from 1 to 6 - one on each half of the tile.)
We may rotate the ith domino, so that tops[i] and bottoms[i] swap values.
Return the minimum number of rotations so that all the values in tops are the same, or all the values in bottoms are the same.
If it cannot be done, return -1.

**Examples**

**Example 1:**

```
Input: tops = [2,1,2,4,2,2], bottoms = [5,2,6,2,3,2]
Output: 2
Explanation: 
The first figure represents the dominoes as given by tops and bottoms: before we do any rotations.
If we rotate the second and fourth dominoes, we can make every value in the top row equal to 2, as indicated by the second figure.
```

**Example 2:**

```
Input: tops = [3,5,1,2,3], bottoms = [3,6,3,3,4]
Output: -1
Explanation: 
In this case, it is not possible to rotate the dominoes to make one row of values equal.
```

**Constraints**

- 2 <= tops.length <= 2 * 104
- bottoms.length == tops.length
- 1 <= tops[i], bottoms[i] <= 6

---

## 题目（中文翻译）

在一排多米诺骨牌（dominoes）中，`tops[i]` 和 `bottoms[i]` 分别表示第 `i` 张多米诺骨牌的上半部和下半部。（一张多米诺骨牌是一块由 1 到 6 的数字组成的棋子，每个半面各有一个数字。）  
我们可以旋转第 `i` 张多米诺骨牌，使 `tops[i]` 与 `bottoms[i]` 的数值互换。  
返回使所有 `tops` 中的数值全部相同，或所有 `bottoms` 中的数值全部相同所需的最小旋转次数。  
如果无法完成，则返回 `-1`。

### 示例

#### 示例 1
```
输入: tops = [2,1,2,4,2,2], bottoms = [5,2,6,2,3,2]
输出: 2
解释:
第一幅图展示了给定的 `tops` 与 `bottoms` 所对应的多米诺骨牌排列：在进行任何旋转之前的状态。  
如果旋转第 2 张和第 4 张多米诺骨牌，就可以使上行的所有数值都变为 `2`，如第二幅图所示。
```

#### 示例 2
```
输入: tops = [3,5,1,2,3], bottoms = [3,6,3,3,4]
输出: -1
解释:
在这种情况下，无论如何旋转多米诺骨牌，都无法使任意一行的数值全部相同。
```

### 约束条件
- `2 <= tops.length <= 2 * 10^4`
- `bottoms.length == tops.length`
- `1 <= tops[i], bottoms[i] <= 6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举每一种可能的目标数字**，看把所有牌翻到该数字需要几次旋转。  
因为每个多米诺的上下两个数都在 `[1,6]` 之间，目标数字只能是 `1~6` 中的一个。  

具体步骤：

1. 取候选目标 `candidate` 为 `1~6` 中的每个数。  
2. 对于每个位置 `i`（从 `0` 到 `n-1`）检查：
   - 如果 `tops[i] == candidate` 或 `bottoms[i] == candidate`，说明这块牌**可以**通过（可能）翻转得到 `candidate`，继续往后走；
   - 否则这块牌根本没有 `candidate`，说明以 `candidate` 为目标是不可能的，直接放弃这个 `candidate`。
3. 当所有牌都能得到 `candidate` 时，统计需要翻转的次数：
   - 把所有 **上面** 不是 `candidate` 的牌翻转（即 `bottoms[i] == candidate`）得到的次数记为 `rotations_top`；
   - 把所有 **下面** 不是 `candidate` 的牌翻转（即 `tops[i] == candidate`）得到的次数记为 `rotations_bottom`；
   - 两者取最小值就是以 `candidate` 为目标时的最少旋转次数。
4. 最后把所有可行 `candidate` 的最小旋转次数取最小，即为答案；如果没有任何 `candidate` 可行，返回 `-1`。

> **类比**：把 `candidate` 想成一本字典里要找的词，`tops[i]`、`bottoms[i]` 就像是两本不同的字典的同一页。如果某一页两本都没有这个词，那这本词根本不存在，直接跳过。

#### 代码（Python）

```python
from typing import List

def minDominoRotations_bruteforce(tops: List[int], bottoms: List[int]) -> int:
    n = len(tops)
    answer = float('inf')                 # 用来保存全局最小的旋转次数

    # 目标数字只能是 1~6 之间的整数
    for candidate in range(1, 7):
        rotations_top = 0   # 把所有上面弄成 candidate 需要的翻转次数
        rotations_bottom = 0  # 把所有下面弄成 candidate 需要的翻转次数
        possible = True

        for i in range(n):
            # 如果当前这块牌的上下都不是 candidate，直接判定不可行
            if tops[i] != candidate and bottoms[i] != candidate:
                possible = False
                break

            # 统计翻转次数
            if tops[i] != candidate:          # 需要把这块牌翻到上面
                rotations_top += 1
            if bottoms[i] != candidate:       # 需要把这块牌翻到下面
                rotations_bottom += 1

        if possible:
            # 该 candidate 可行，取两种方式的最小值更新全局答案
            answer = min(answer, rotations_top, rotations_bottom)

    return -1 if answer == float('inf') else answer
```

#### 复杂度

- **时间复杂度**：`O(6 * n) = O(n)`  
  解释：外层循环遍历 6 个可能的目标数字（常数），内层遍历 `n` 块牌。虽然写成 `O(6n)`，但常数 6 可以忽略，整体随 `n` 线性增长。

- **空间复杂度**：`O(1)`  
  只用了若干个计数变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解已经是 `O(n)` 了，已经相当快。这里再**进一步简化**，把不必要的遍历去掉，只检查 **两个最有可能的候选数字**。

**关键观察**：

- 若要让所有上面（或下面）统一为同一个数字 `x`，那么 `x` 必须出现在**每一块牌的上面或下面**。也就是说，`x` 必须是**第一块牌的上面或下面的数字**之一。  
- 证明：设最终目标是把所有上面变成 `x`，则第 `0` 块牌必须在最终状态上面为 `x`，而这块牌只能是原来的 `tops[0]`（不翻）或 `bottoms[0]`（翻转）得到 `x`，所以 `x` 必定是 `tops[0]` 或 `bottoms[0]`。同理，如果目标是把所有下面统一，也同样只会是这两个数。

因此，只需要尝试 **至多两个候选数字**：`tops[0]` 和 `bottoms[0]`（若相同则只算一次）。对每个候选数字，统计把整行变成该数字需要的最少翻转次数；若两者都不可行则返回 `-1`。

**实现细节**：

- 编写一个辅助函数 `check(candidate)`，遍历所有牌：
  - 若 `candidate` 同时不在 `tops[i]`、`bottoms[i]` 中，直接返回 `-1`（不可行）。
  - 否则统计 `rot_top`（把上面全变为 `candidate`）和 `rot_bottom`（把下面全变为 `candidate`）的翻转次数。
- 对 `candidate = tops[0]`、`candidate = bottoms[0]` 调用 `check`，取其中的最小非负值即为答案。

> **类比**：把每块牌想成一把钥匙，钥匙只有两种形状（上面的数字或下面的数字）。如果我们想让所有钥匙都统一成一种形状，只能选第一把钥匙的形状，因为其他钥匙必须通过旋转才能匹配它。

#### 代码（Python）

```python
from typing import List

def minDominoRotations(tops: List[int], bottoms: List[int]) -> int:
    """
    贪心+一次遍历求解
    只检测 tops[0] 和 bottoms[0] 两个可能的目标数字
    """
    def check(candidate: int) -> int:
        """返回把所有上面或所有下面统一为 candidate 所需的最少翻转次数，若不可能返回 -1"""
        rot_top = 0      # 把上面全部变成 candidate 需要的翻转次数
        rot_bottom = 0   # 把下面全部变成 candidate 需要的翻转次数

        for t, b in zip(tops, bottoms):
            # 若当前牌的上下都不是 candidate，则无法达成目标
            if t != candidate and b != candidate:
                return -1
            # 统计翻转次数
            if t != candidate:      # 上面不是 candidate，需要翻转到上面
                rot_top += 1
            if b != candidate:      # 下面不是 candidate，需要翻转到下面
                rot_bottom += 1

        # 两种方式取最少的翻转次数
        return min(rot_top, rot_bottom)

    # 可能的目标数字只有 tops[0] 和 bottoms[0]（若相同只算一次）
    candidates = {tops[0], bottoms[0]}
    ans = float('inf')
    for c in candidates:
        res = check(c)
        if res != -1:
            ans = min(ans, res)

    return -1 if ans == float('inf') else ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历两次（最多两次 `check`），每次线性扫描 `n` 块牌。常数因子比暴力解更小。

- **空间复杂度**：`O(1)`  
  只使用常数个计数变量。

---

## 心得

- **核心技巧**：**贪心 + 只检查第一块牌的两种可能**。通过观察目标数字必须出现在每块牌的上或下，进一步缩小候选范围，从而实现一次或两次线性扫描即可得到答案。

- **适用的题型**  
  1. “把所有元素统一为同一个值” 类的题目（例如 `Minimum Swaps To Make All Elements Equal`）。  
  2. “只允许局部操作（翻转、交换）使数组满足某种全局约束”的题目（例如 `Stone Game VII` 中的局部取子）。  
  3. “候选答案数量极小，只需要枚举常数个可能”的题目（例如 `Find the Town Judge`）。

- **一句话总结**：**先把搜索空间压到常数级，再用一次遍历验证即可**。

---

## 反思

- **拿到题目第一反应**：直接想到“枚举所有 1~6 的数字”，因为数字范围小，先把最朴素的办法写出来验证思路是否正确。

- **最容易踩的坑**  
  1. **遗漏两种统一方式**：只考虑把上面统一，却忘了把下面统一也可能更少翻转。  
  2. **特殊情况**：当 `tops[0] == bottoms[0]` 时，候选集合只能是一个数字，若不去重会重复计算。  
  3. **返回值处理**：若所有候选均不可行，需要返回 `-1`，而不是 `0` 或 `inf`。

- **下次遇到同类题的第一步**：先**找出必须出现的候选值**（通常是第一元素或极少数元素），再**用一次线性扫描验证**，这样可以立刻把时间复杂度控制在 `O(n)`。