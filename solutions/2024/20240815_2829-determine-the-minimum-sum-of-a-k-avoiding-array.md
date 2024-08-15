# #2829. 确定 k-avoiding 数组的最小和 / Determine the Minimum Sum of a k-avoiding Array

> 难度：中等 · 标签：Math、Greedy · [LeetCode 链接](https://leetcode.com/problems/determine-the-minimum-sum-of-a-k-avoiding-array/)

---

## 题目（英文原版）

**Description**

You are given two integers, n and k.
An array of distinct positive integers is called a k-avoiding array if there does not exist any pair of distinct elements that sum to k.
Return the minimum possible sum of a k-avoiding array of length n.

**Examples**

**Example 1:**

```
Input: n = 5, k = 4
Output: 18
Explanation: Consider the k-avoiding array [1,2,4,5,6], which has a sum of 18.
It can be proven that there is no k-avoiding array with a sum less than 18.
```

**Example 2:**

```
Input: n = 2, k = 6
Output: 3
Explanation: We can construct the array [1,2], which has a sum of 3.
It can be proven that there is no k-avoiding array with a sum less than 3.
```

**Constraints**

- 1 <= n, k <= 50

---

## 题目（中文翻译）

**描述**  
给定两个整数 `n` 和 `k`。  
如果一个由互不相同的正整数构成的数组中不存在任意一对不同元素的和等于 `k`，则称该数组为 **k-avoiding 数组**（k-avoiding array）。  
返回长度为 `n` 的 k-avoiding 数组的最小可能和。

**示例 1**  
**输入**: `n = 5, k = 4`  
**输出**: `18`  
**解释**: 考虑 k-avoiding 数组 `[1,2,4,5,6]`，其和为 `18`。可以证明不存在和小于 `18` 的 k-avoiding 数组。

**示例 2**  
**输入**: `n = 2, k = 6`  
**输出**: `3`  
**解释**: 我们可以构造数组 `[1,2]`，其和为 `3`。可以证明不存在和小于 `3` 的 k-avoiding 数组。

**约束条件**  
- `1 <= n, k <= 50`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**枚举所有可能的数组**，挑出满足「任意两数之和不等于 k」且长度为 `n` 的数组，再在这些合法数组里找最小的和。  
- 为了枚举，我们可以先限定一个上界（比如 `1 … 2·k + n`），把每个整数看成一张卡片。  
- 然后从这些卡片中挑出 `n` 张（相当于从卡片堆里抽 `n` 张），检查抽出来的 `n` 张卡片里有没有两张的数字之和恰好是 `k`。  
- 这里用到的 **集合（Set）** 可以类比为「字典」：我们把已经抽到的数字放进集合，想检查「是否存在一对数之和为 k」时，只要看 `k - 当前数字` 是否已经在集合里就行了。  

这种做法一定能得到正确答案，因为我们把 **所有** 合法数组都遍历了一遍。  

**为什么会慢**  
- 组合的数量是指数级的：从 `m`（上界） 个数里挑 `n` 个，需要检查 `C(m, n)` 种可能，`m` 稍大一点，组合数就会爆炸。  
- 每检查一个组合都要遍历 `n` 次来判断是否有冲突，整体时间会非常大。

#### 代码（Python）  

```python
from itertools import combinations

def min_sum_bruteforce(n: int, k: int) -> int:
    # 设一个足够大的上界，这里取 2*k + n，确保一定能找出 n 个数
    upper = 2 * k + n
    best = float('inf')

    # 枚举所有从 1..upper 中挑 n 个的组合
    for comb in combinations(range(1, upper + 1), n):
        ok = True
        seen = set()
        for x in comb:
            # 如果已经有一个数 y，使得 x + y = k，则不合法
            if (k - x) in seen:
                ok = False
                break
            seen.add(x)
        if ok:
            best = min(best, sum(comb))
    return best
```

#### 复杂度  

- **时间复杂度**：`O(C(upper, n) * n)`，其中 `C` 是组合数。  
  - 组合数在最坏情况下会是指数级的（比如 `upper≈n` 时约为 `2^n`），所以这就是“暴力”解的本质——非常慢。  
- **空间复杂度**：`O(n)`，仅用到一个集合保存当前组合的元素。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**我们真正关心的只是“能不能把一个数加入”**，而不是所有组合。  
把数字从小到大一个一个考察：

1. **从 1 开始**，因为我们希望数组的总和尽可能小。  
2. 当考虑数字 `i` 时，唯一会导致冲突的情况是：已经选过的数组里有 `k - i`（且 `k - i > 0`），因为 `i + (k-i) = k`。  
3. 因此，只要 `k - i` 不在已经选过的集合里，我们就可以安全地把 `i` 加进去。  

这样我们每次都把**当前还能选的最小数字**加入数组，**贪心**地构造出长度为 `n` 的最小和数组。  
**为什么贪心是正确的**（交换论证）：

- 假设在最优解中，某个位置本应该是更大的数 `x`，而我们贪心选了更小的 `y (y < x)`。  
- 因为 `y` 没有和已选的数形成和为 `k` 的冲突，`x` 也一定不会比 `y` 更早产生冲突（冲突只取决于已有的数）。  
- 用 `y` 替换掉 `x`，数组仍然合法且和更小，违背了“最优解”的假设。  
- 因此，贪心每一步选最小合法数必然得到全局最小和。

实现细节：

- 用一个 `set selected` 记录已经加入的数，查找 `k - i` 是否已经出现只需要 **O(1)** 时间。  
- 循环从 `i = 1` 开始，直到选满 `n` 个数为止。  
- 由于 `n, k ≤ 50`，循环的上界不会很大（最多到 `k + n`），时间几乎是常数级。

#### 代码（Python）  

```python
def min_sum_greedy(n: int, k: int) -> int:
    """
    贪心构造最小和的 k-avoiding 数组
    :param n: 数组长度
    :param k: 不能出现两数之和的目标值
    :return: 最小可能的总和
    """
    selected = set()          # 已经放进数组的数，类似查字典的“已有词”
    total = 0                 # 当前数组的和
    i = 1                     # 从最小的正整数开始尝试

    while len(selected) < n:  # 只要还没选够 n 个，就继续
        # 如果 k-i 是正数且已经在集合里，说明 i 和它会凑成 k，不能选 i
        if (k - i) > 0 and (k - i) in selected:
            i += 1
            continue

        # 否则 i 是当前能选的最小合法数，加入集合并累加到答案
        selected.add(i)
        total += i
        i += 1                # 继续尝试更大的数

    return total
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 我们最多检查大约 `n + k` 个整数（因为每次都往前走一步），每一步的判断是集合的 `O(1)` 查找。  
  - 与暴力解的指数级时间相比，线性时间几乎是瞬间完成。  

- **空间复杂度**：`O(n)`  
  - 需要存放已经选的 `n` 个数的集合，除此之外只用常数级额外空间。  

---

## 心得  

- **核心技巧**：**贪心 + 哈希集合（Set）**。  
  - 通过把「不能出现的配对」抽象为「已经出现的数」来快速判断。  
- **适用的题型**  
  1. “避免某种配对” 类问题，如 **“数组中不存在两数之和为 target”** 的构造题。  
  2. 需要 **最小/最大** 和或乘积的构造题，常常可以用从小到大（或从大到小）贪心加集合过滤。  
  3. **“避免相邻冲突”** 的序列生成（比如避免相同颜色相邻）也可以用类似思路。  

> **解题钥匙**：**从最小的正整数开始尝试，只要它不和已经选的数形成冲突，就一定是最优选择。**  

---

## 反思  

- **第一反应**：直接想到枚举所有可能的数组（暴力），因为题目描述比较直接。  
- **最容易踩的坑**  
  - 忘记排除 **非正数**：`k - i` 可能为负或零，这时根本不构成冲突。  
  - 误以为 `k/2` 不能出现（因为 `k/2 + k/2 = k`），实际上元素必须**互不相同**，单独出现是允许的。  
  - 没考虑到 `k` 很大时，实际只需要检查到 `k + n` 左右就可以停止循环。  
- **下次类似题**：第一步先 **画出冲突关系**（配对图），再想 **“从最小/最大的未冲突数”** 逐个加入，看是否能贪心完成。这样可以快速跳过暴力枚举，直达最优解。