# #2209. 最少白色瓷砖数（Minimum White Tiles After Covering With Carpets） / Minimum White Tiles After Covering With Carpets

> 难度：困难 · 标签：String、Dynamic Programming、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-white-tiles-after-covering-with-carpets/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed binary string floor, which represents the colors of tiles on a floor:
You are also given numCarpets and carpetLen. You have numCarpets black carpets, each of length carpetLen tiles. Cover the tiles with the given carpets such that the number of white tiles still visible is minimum. Carpets may overlap one another.
Return the minimum number of white tiles still visible.

**Examples**

**Example 1:**

```
Input: floor = "10110101", numCarpets = 2, carpetLen = 2
Output: 2
Explanation: 
The figure above shows one way of covering the tiles with the carpets such that only 2 white tiles are visible.
No other way of covering the tiles with the carpets can leave less than 2 white tiles visible.
```

**Example 2:**

```
Input: floor = "11111", numCarpets = 2, carpetLen = 3
Output: 0
Explanation: 
The figure above shows one way of covering the tiles with the carpets such that no white tiles are visible.
Note that the carpets are able to overlap one another.
```

**Constraints**

- 1 <= carpetLen <= floor.length <= 1000
- floor[i] is either '0' or '1'.
- 1 <= numCarpets <= 1000

---

## 题目（中文翻译）

给定一个 **0 索引的二进制字符串（binary string）** `floor`，表示地板上每块瓷砖的颜色（'0' 为白色，'1' 为黑色）。  
同时给定整数 `numCarpets` 和 `carpetLen`。你拥有 `numCarpets` 张 **黑色地毯（black carpets）**，每张的长度为 `carpetLen` 块瓷砖。  
请使用这些地毯覆盖瓷砖，使得仍然可见的白色瓷砖数量最少。地毯之间可以**重叠（overlap）**。  
返回最少的可见白色瓷砖数。

---

### 示例

**示例 1**  
Input: `floor = "10110101", numCarpets = 2, carpetLen = 2`  
Output: `2`  
**解释**：上图展示了一种覆盖方案，使得仅剩 2 块白色瓷砖可见。不存在其他覆盖方式能够使可见白色瓷砖少于 2 块。

**示例 2**  
Input: `floor = "11111", numCarpets = 2, carpetLen = 3`  
Output: `0`  
**解释**：上图展示了一种覆盖方案，使得所有白色瓷砖都被覆盖而不可见。需要注意的是，地毯可以相互重叠。

---

### 约束条件

- `1 <= carpetLen <= floor.length <= 1000`
- `floor[i]` 只能是 `'0'` 或 `'1'`
- `1 <= numCarpets <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的铺毯方式**，然后挑选出使剩余白色砖块最少的方案。  
可以把每块地砖想象成一排 **“零一牌”**（`0` 表白色，`1` 表黑色），我们有若干块**黑色地毯**（长度固定 `carpetLen`），可以把它们随意放在这排牌上，甚至可以互相覆盖。  

暴力解的步骤：

1. 从左到右遍历每个起始位置 `i`（`0 ≤ i < n`），决定**是否在这里放一块地毯**。  
2. 如果决定放，就把从 `i` 开始、长度为 `carpetLen` 的这段牌全部“隐藏”。  
3. 递归地处理剩下的地毯数量 `numCarpets-1` 和后面的牌。  
4. 当所有地毯都用完或已经遍历到字符串末尾时，统计剩下的白色牌（即字符 `'0'` 的个数），作为一种方案的代价。  
5. 取所有方案中的最小代价。

> **类比**：把地毯想成一本厚厚的《字典》，每次把它盖在一段文字上，下面的文字就看不见了。我们要找一种盖法，使得“看不见的白字”最多，也就是剩下的白字最少。

**为什么正确**：我们把所有可能的覆盖方式都遍历了一遍，最小的白色砖块数必然在其中。

**时间/空间复杂度**：

- 设字符串长度为 `n`，地毯数量为 `k`（即 `numCarpets`），每块地毯可以放在 `n` 个位置（实际上是 `n` 种起始位置），所以**状态树的分支数是 `O(n^k)`**，这在最坏情况下是指数级的。  
- 每一次递归只需要记录当前的索引和剩余地毯数，使用 **`O(k)` 的递归栈空间**。

> **大白话**：`O(n^k)` 就像把 `n` 块巧克力装进 `k` 层盒子里，每层都有 `n` 种选法，组合起来会非常非常多，根本算不过来。

#### 代码（Python）

```python
def minWhiteTiles_bruteforce(floor: str, numCarpets: int, carpetLen: int) -> int:
    n = len(floor)

    # 递归函数：从位置 i 开始，手里还有 j 块地毯
    def dfs(i: int, j: int) -> int:
        # 已经到最右边，剩下的都是原始颜色
        if i >= n:
            return 0
        # 没有地毯可用了，只能把后面的白砖直接计数
        if j == 0:
            # 统计 i..n-1 中的 '0' 个数
            return floor[i:].count('0')

        # 方案 1：不在 i 位置放地毯，当前砖块如果是白色就要计数
        cnt_not_put = (1 if floor[i] == '0' else 0) + dfs(i + 1, j)

        # 方案 2：在 i 位置放一块地毯（如果还能放的话），覆盖 i~i+carpetLen-1
        # 地毯可以超出右边界，直接把 i 移到 n 即可
        next_i = min(n, i + carpetLen)
        cnt_put = dfs(next_i, j - 1)

        # 取两种方案的最小值
        return min(cnt_not_put, cnt_put)

    return dfs(0, numCarpets)
```

> 代码中每一行都加了中文注释，直接复制运行即可。  

#### 复杂度

- **时间复杂度**：`O(n^k)`（指数级），因为每块地毯都有 `n` 种放法，递归会产生 `n` 的 `k` 次方个分支。  
- **空间复杂度**：`O(k)`，递归深度最多是 `k`（地毯的数量），每层只保存几个整数。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **两大瓶颈**：

1. **重复计算**：同样的子区间会被多次递归访问，导致指数级的时间。  
2. **遍历所有起始位置**：在每一步都尝试把地毯放在当前位置，等价于在 `O(carpetLen)` 的范围内做一次“跳转”，其实我们只需要**知道从当前位置起，覆盖一段后会去哪里**，不必遍历每个内部格子。

**关键观察**：  
- 当我们在位置 `i` **放一块地毯** 时，**这段长度 `carpetLen` 的砖块全部被隐藏**，不再计数。于是从 `i` 跳到 `i + carpetLen`（如果超过右边界就直接到 `n`），剩下的子问题与“是否放地毯”无关。  
- 当我们 **不放地毯** 时，只需要把当前位置的颜色计入答案（如果是白色 `0` 就 +1），然后继续处理 `i+1`。  

因此我们可以用 **动态规划（DP）** 从右往左填表：

```
dp[i][j] = 用至多 j 块地毯覆盖从 i 开始到末尾，剩余的最少白砖数
```

转移方程（i 从 n-1 → 0，j 从 1 → numCarpets）：

```
# 方案 A：不放地毯
cand1 = (floor[i] == '0') + dp[i+1][j]

# 方案 B：放一块地毯（如果还能放）
next = min(n, i + carpetLen)          # 跳到覆盖后的位置
cand2 = dp[next][j-1]                 # 这段被隐藏，不加任何白砖

dp[i][j] = min(cand1, cand2)
```

**为什么只需要 O(1) 的状态转移**：

- `dp[i+1][j]` 已经在更右边算好，直接使用。  
- `dp[next][j-1]` 同样是更右边的状态。  

我们不需要**前缀和**来统计被覆盖区间内的白砖数，因为**覆盖后这些砖块不再计数**，直接跳过去即可。  
（如果题目要求统计被覆盖的白砖数，前缀和可以在 `O(1)` 时间内求区间 `'0'` 的数量，原理类似：`pre[i] = pre[i-1] + (floor[i]=='0')`，但这里并不需要。）

**空间优化**：只和 `i+1`、`i+carpetLen` 两行有关，使用两层滚动数组即可把空间降到 `O(numCarpets)`。

> **类比**：想象我们在走一条路，每一步可以**普通走一步**（如果这一步是白砖就要付费），也可以**一次跨 `carpetLen` 步**（使用一块地毯，跨过去的路段免费）。我们要在费用最少的情况下走到终点，这正是 DP 在做的事。

#### 代码（Python）

```python
def minWhiteTiles(floor: str, numCarpets: int, carpetLen: int) -> int:
    n = len(floor)

    # dp[j] 表示在当前位置 i 右侧，用至多 j 块地毯的最小白砖数
    # 初始时 i == n（已经走到最右边），所有 dp 都是 0
    dp = [0] * (numCarpets + 1)

    # 从右往左遍历每个位置
    for i in range(n - 1, -1, -1):
        # 为了在本轮计算中不覆盖掉上一轮的值，先拷贝一份旧的 dp
        new_dp = dp[:]                     # new_dp 对应的是位置 i 的状态
        for j in range(1, numCarpets + 1):
            # 方案 A：不放地毯，当前砖如果是白色就要 +1
            cand1 = (1 if floor[i] == '0' else 0) + dp[j]

            # 方案 B：放一块地毯，直接跳到 i+carpetLen（或 n）
            nxt = min(n, i + carpetLen)
            cand2 = dp[j - 1] if nxt == n else dp[j - 1]  # dp 已经是 nxt 位置的值

            # 取最小
            new_dp[j] = min(cand1, cand2)

        dp = new_dp                        # 把本轮结果保存，进入下一个 i

    # dp[numCarpets] 即为答案
    return dp[numCarpets]
```

**代码要点解释**：

| 行号 | 说明 |
|------|------|
| `dp = [0] * (numCarpets + 1)` | 初始化：当已经走到字符串末尾时，剩余白砖数为 0（无论剩余多少地毯）。 |
| `for i in range(n - 1, -1, -1):` | 从右往左遍历，每次都在考虑“从 i 开始”。 |
| `new_dp = dp[:]` | 为当前位置保存新的状态，防止在同一轮中覆盖掉还需要的旧值。 |
| `cand1 = (1 if floor[i] == '0' else 0) + dp[j]` | 不放地毯时，如果当前位置是白砖则加 1，后面的子问题是 `i+1`（已在 `dp[j]` 中）。 |
| `nxt = min(n, i + carpetLen)` | 放地毯后跳到的位置，超出右边界时直接设为 `n`（相当于已经结束）。 |
| `cand2 = dp[j - 1]` | 用掉一块地毯后，子问题是 `nxt` 位置，已在 `dp[j-1]` 中。 |
| `new_dp[j] = min(cand1, cand2)` | 取两种方案的最小值。 |
| `dp = new_dp` | 结束本轮，准备进入更左侧的 i。 |

> 这段代码的时间复杂度是 `O(n * numCarpets)`，在本题的约束 (`n ≤ 1000`, `numCarpets ≤ 1000`) 完全可以接受。

#### 复杂度

- **时间复杂度**：`O(n * numCarpets)`  
  - 直观解释：我们遍历了 `n`（最多 1000）个位置，对于每个位置又检查了最多 `numCarpets`（同样最多 1000）种剩余地毯数的状态。  
  - 与暴力解的 `O(n^k)` 相比，指数级的时间被压缩成了“线性乘线性”，几乎瞬间跑完。

- **空间复杂度**：`O(numCarpets)`  
  - 只保存当前行和上一行的 DP 值（即一个长度为 `numCarpets+1` 的数组），相当于只需要几千个整数的内存，远比 `O(n * numCarpets)` 的二维表省空间。

---

## 心得

- **核心技巧**：**动态规划 + 状态压缩**（从右往左的 DP），把“是否使用一块地毯”抽象成两条转移路径。  
- **适用的题型**：  
  1. “在一维序列上使用有限资源（如地毯、跳跃、删除）来最小化/最大化某个代价”——例如 *“最小化删除字符数”*、*“跳跃游戏 II”*（每次跳跃固定长度）等。  
  2. “覆盖区间的最优子结构”——如 *“用最少的子数组覆盖所有 1”*、*“最小化涂色次数”* 等。  
- **一句话总结解题钥匙**：**把“覆盖一段”视作一次“跳过”操作，用 DP 记录“从当前位置起、剩余多少资源时的最优代价”。**

---

## 反思

- **第一反应**：看到“地毯可以覆盖且可以重叠”，立刻想到“枚举每块地毯的起始位置”，于是写出了指数级的递归。  
- **最容易踩的坑**：  
  - 忘记处理地毯跨出右边界的情况，需要 `min(n, i+carpetLen)`。  
  - DP 的状态顺序错误：必须从右向左（或从左向右并使用 `i+carpetLen` 的状态），否则转移时会依赖还未计算的值。  
  - 当 `carpetLen` 很大时，直接遍历区间会导致 `O(n * carpetLen * numCarpets)`，所以要用“一次跳过”而不是逐格检查。  
- **下次类似题的第一步**：先问自己“**这一步是否可以一次性跳过一段**”，如果答案是“可以”，就立刻尝试把它抽象成 DP 中的“转移到更远位置”，而不是逐个枚举。这样往往能把指数级时间降到多项式。