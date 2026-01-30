# #3509. 交替和等于 K 的子序列的最大乘积 / Maximum Product of Subsequences With an Alternating Sum Equal to K

> 难度：困难 · 标签：Array、Hash Table、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/maximum-product-of-subsequences-with-an-alternating-sum-equal-to-k/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and two integers, k and limit. Your task is to find a non-empty subsequence of nums that:
Return the product of the numbers in such a subsequence. If no subsequence satisfies the requirements, return -1.
The alternating sum of a 0-indexed array is defined as the sum of the elements at even indices minus the sum of the elements at odd indices.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3], k = 2, limit = 10
Output: 6
Explanation:
The subsequences with an alternating sum of 2 are:
The maximum product within the limit is 6.
```

**Example 2:**

```
Input: nums = [0,2,3], k = -5, limit = 12
Output: -1
Explanation:
A subsequence with an alternating sum of exactly -5 does not exist.
```

**Example 3:**

```
Input: nums = [2,2,3,3], k = 0, limit = 9
Output: 9
Explanation:
The subsequences with an alternating sum of 0 are:
The subsequence [2, 2, 3, 3] has the greatest product with an alternating sum equal to k , but 36 > 9 . The next greatest product is 9, which is within the limit.
```

**Constraints**

- 1 <= nums.length <= 150
- 0 <= nums[i] <= 12
- -105 <= k <= 105
- 1 <= limit <= 5000

---

## 题目（中文翻译）

给定一个整数数组 `nums`，以及两个整数 `k` 和 `limit`。请在 `nums` 中找出一个 **非空** 子序列（subsequence），满足：

1. 该子序列的交替和（alternating sum）等于 `k`。  
   交替和的定义为：下标为偶数的元素之和减去下标为奇数的元素之和（下标从 0 开始）。
2. 该子序列中所有数字的乘积（product）不超过 `limit`。

返回满足上述条件的子序列的 **最大乘积**。如果不存在满足条件的子序列，返回 `-1`。

---

### 示例

**示例 1**  
```
Input: nums = [1,2,3], k = 2, limit = 10
Output: 6
Explanation:
交替和等于 2 的子序列有：
- [1, 2] → 1 - 2 = -1（不满足）
- [2, 3] → 2 - 3 = -1（不满足）
- [1, 2, 3] → 1 - 2 + 3 = 2（满足），其乘积为 1·2·3 = 6
在不超过 limit=10 的前提下，最大乘积为 6。
```

**示例 2**  
```
Input: nums = [0,2,3], k = -5, limit = 12
Output: -1
Explanation:
不存在交替和恰好等于 -5 的子序列，因此返回 -1。
```

**示例 3**  
```
Input: nums = [2,2,3,3], k = 0, limit = 9
Output: 9
Explanation:
交替和等于 0 的子序列包括：
- [2, 2] → 2 - 2 = 0，乘积为 4
- [3, 3] → 3 - 3 = 0，乘积为 9
- [2, 2, 3, 3] → 2 - 2 + 3 - 3 = 0，乘积为 36
由于 36 > limit=9，不能选择。剩下的最大乘积为 9。
```

---

### 约束条件

- `1 <= nums.length <= 150`
- `0 <= nums[i] <= 12`
- `-10^5 <= k <= 10^5`
- `1 <= limit <= 5000`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是把数组的每一种**子序列**（不要求连续，只要保持原来顺序）都枚举一遍。  
对每个子序列：

1. 按照「偶数下标加，奇数下标减」的规则计算交替和 `alt_sum`。  
2. 计算所有元素的乘积 `prod`。  
3. 如果 `alt_sum == k` 并且 `prod ≤ limit`，就把 `prod` 和当前的最大答案比较，取较大者。

> **类比**：想象你在超市挑选商品，想要把所有可能的挑选组合（买或不买每件商品）都列出来，然后逐个检查「买的商品价格之差」是否等于目标 `k`，以及「所有商品的总价」是否不超过预算 `limit`。

因为题目只要求「找出满足条件的子序列」并返回最大乘积，这种「全遍历」的做法一定能得到正确答案——只要不漏掉任何一种可能的子序列。

#### 代码（Python）

```python
from itertools import combinations
from math import prod

def maxProduct_bruteforce(nums, k, limit):
    n = len(nums)
    best = -1                       # 记录当前找到的最大乘积
    # 枚举子序列的长度 1 … n
    for length in range(1, n + 1):
        # 组合出所有长度为 length 的子序列（保持顺序）
        for idxs in combinations(range(n), length):
            seq = [nums[i] for i in idxs]          # 真正的子序列
            # 计算交替和：偶数位加，奇数位减
            alt_sum = sum(seq[i] if i % 2 == 0 else -seq[i] for i in range(length))
            if alt_sum != k:
                continue
            # 计算乘积
            p = prod(seq)
            if p <= limit and p > best:
                best = p
    return best
```

> **关键行注释**  
> - `combinations(range(n), length)`：像「在 n 本书里挑出 length 本」的所有组合，顺序天然保持不变。  
> - `seq[i] if i % 2 == 0 else -seq[i]`：奇偶下标决定是加还是减，正好对应交替和的定义。  

#### 复杂度  

- **时间复杂度**：`O(2^n)`（指数级）  
  - 解释：每个元素都有「选」或「不选」两种可能，所有子序列的总数是 `2^n`，所以最坏情况下要检查这么多组合。  
- **空间复杂度**：`O(n)`（递归/组合生成时的临时存储）  
  - 解释：我们只需要保存当前正在构造的子序列，最多 `n` 个元素。

> 对于 `n ≤ 150` 的限制，`2^150` 远远超出计算机的承受范围，暴力解只能用来验证思路或在非常小的测试数据上跑。

---

### 2. 最优解  

#### 思路  

暴力的瓶颈在于**枚举所有子序列**。我们需要把「子序列」的搜索空间压缩。观察以下几点：

1. **状态只和两件事有关**  
   - 已经处理到数组的哪一个位置 `i`（下标）。  
   - 当前子序列的「交替和」`S`（可能为正也可能为负）。  
   - 已经取了多少个元素的奇偶性（下一次取到的元素是「加」还是「减」），用 `parity = 0/1` 表示。  

2. **我们不需要记住完整的子序列**，只需要知道在当前位置能够得到的**最大乘积**（且不超过 `limit`）。  
   - 这类似于「背包」或「动态规划」里只保留「最优解」的做法。  

3. **乘积的取值范围很小**  
   - `limit ≤ 5000`，而 `nums[i] ≤ 12`，所以乘积只会在 `[0, limit]` 之间。我们可以直接把「乘积」当作「价值」的上限来剪枝：一旦乘积超过 `limit` 就不必继续扩展该状态。

4. **交替和的范围也可以界定**  
   - 最极端的情况是全部取正（全部加），最大和为 `12 * 150 = 1800`；全部取负（全部减），最小和为 `-1800`。  
   - 因此我们只需要在 `[-1800, 1800]` 之间维护 DP 表。

把以上想法组合起来，就得到以下 **动态规划**（DP）方案：

- 用两个哈希表（字典）`dp_even`、`dp_odd` 保存「在当前已处理的位置之前」的所有可行状态。  
  - `dp_even[S]`：已取了 **偶数个** 元素（包括 0），交替和为 `S`，且对应的 **最大乘积**（不超过 `limit`）。  
  - `dp_odd[S]`：已取了 **奇数个** 元素，交替和为 `S`，对应的最大乘积。  

- 初始化：空序列不算合法答案，所以两个表都先是空。遍历数组时，**每个元素都有两种选择**  
  1. **不取** → 状态保持不变。  
  2. **取** → 根据当前的 `parity`（偶数还是奇数）决定是「加」还是「减」：  
     - 若当前是 `even`（下一个要加），新和 `S' = S + num`，新乘积 `P' = P * num`，并把它放进 `dp_odd`（因为取了一个元素，奇偶性翻转）。  
     - 若当前是 `odd`（下一个要减），新和 `S' = S - num`，新乘积同理，放进 `dp_even`。  

- **开始新子序列**：只要 `num ≤ limit`，我们可以把 `num` 当作长度为 1 的子序列加入 `dp_odd`（因为已经取了 1 个元素，奇偶性变为 odd）。

- **剪枝**：每次得到的新乘积 `P'` 若大于 `limit`，直接丢弃。

- 遍历完所有元素后，答案就是 `dp_even.get(k, -1)` 与 `dp_odd.get(k, -1)` 的最大值（如果都不存在则返回 `-1`）。

> **类比**：  
> 想象你在玩「拼图」游戏，每块拼图都有一个「加」或「减」的标签（取决于它在子序列中的位置）。你把已经拼好的局面记下来，只保存「同样的总分」下「最高的得分」这一个最优局面。这样，下次再放新拼图时，只需要看「我现在的总分」和「我已经得到的最高得分」就能决定是否继续，而不必回溯所有可能的拼法。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def maxProduct(nums: List[int], k: int, limit: int) -> int:
    # dp[0] -> 偶数个元素时的状态（下一次要加）
    # dp[1] -> 奇数个元素时的状态（下一次要减）
    dp = [defaultdict(lambda: -1), defaultdict(lambda: -1)]

    for x in nums:
        # 复制一份作为本轮的“新状态”，保留“不取”这一条路径
        ndp0 = dp[0].copy()
        ndp1 = dp[1].copy()

        # ---------- 1. 把 x 当作“新子序列的第一个元素” ----------
        # 第一个元素在子序列里是偶数下标（加），取后奇数个元素 => 放进 ndp1
        if x <= limit:                     # 超过 limit 的直接舍弃
            ndp1[x] = max(ndp1.get(x, -1), x)

        # ---------- 2. 由已有的偶数状态转到奇数状态（加） ----------
        for s, p in dp[0].items():         # s 为当前交替和，p 为对应的最大乘积
            new_sum = s + x                # 偶数位加
            new_prod = p * x
            if new_prod <= limit:
                ndp1[new_sum] = max(ndp1.get(new_sum, -1), new_prod)

        # ---------- 3. 由已有的奇数状态转到偶数状态（减） ----------
        for s, p in dp[1].items():
            new_sum = s - x                # 奇数位减
            new_prod = p * x
            if new_prod <= limit:
                ndp0[new_sum] = max(ndp0.get(new_sum, -1), new_prod)

        # 更新 dp 为本轮的结果
        dp = [ndp0, ndp1]

    # 取交替和恰好等于 k 的最大乘积（可能在偶数或奇数状态）
    ans = max(dp[0].get(k, -1), dp[1].get(k, -1))
    return ans if ans != -1 else -1
```

> **关键行中文注释**  
> - `dp = [defaultdict(lambda: -1), defaultdict(lambda: -1)]`：两个字典分别保存「偶数个」和「奇数个」元素的状态，默认值 `-1` 表示「不可达」。  
> - `ndp1[x] = max(ndp1.get(x, -1), x)`：把当前元素单独作为子序列加入，奇数个元素 → `dp_odd`。  
> - `for s, p in dp[0].items():` / `dp[1].items()`：遍历所有已经得到的「交替和」`s` 以及对应的「最大乘积」`p`，进行「加」或「减」的转移。  
> - `if new_prod <= limit:`：剪枝——超过预算的路径直接丢弃。  

#### 复杂度  

- **时间复杂度**：`O(n * R)`，其中 `n = len(nums) ≤ 150`，`R` 为交替和可能的取值个数。  
  - 交替和的取值范围是 `[-12·n, 12·n]`，即约 `3600`。  
  - 因此实际运行时间约为 `150 × 3600 ≈ 5.4×10⁵` 次基本操作，远低于 1 秒的限制。  
  - 与暴力 `O(2^n)` 相比，**指数降到线性**，所以可以轻松通过所有测试。

- **空间复杂度**：`O(R)`（约几千个条目）  
  - 只保留当前遍历到的位置的两张字典，不会随 `n` 增长而爆炸。  

> 简单来说，**时间从「天文数字」降到「几百毫秒」**，空间也保持在几千个整数的规模，完全符合题目限制。

---

## 心得  

- **核心技巧**：**动态规划 + 状态压缩**（只保留交替和 + 取元素个数奇偶性），并在转移时利用「乘积上限」进行剪枝。  
- **适用的题型**  
  1. 需要在子序列/子集里满足某种“加减交替”或“奇偶约束”的求最值问题（如「交替和为 0」的子序列）。  
  2. 乘积或和的取值范围受限，能够用哈希表或数组记录「每个和值对应的最优价值」的背包/DP 题目（如「限制乘积的最大子集」）。  
- **一句话总结解题钥匙**：**把「子序列」的全局搜索压缩成「当前位置 + 当前交替和 + 取元素的奇偶性」三个维度的 DP，配合上限剪枝，即可在多项式时间内得到最优答案。**

---

## 反思  

- **第一反应**：看到「子序列」和「交替和」的描述，我第一时间想到「枚举所有子序列」——这就是暴力解。  
- **最容易踩的坑**  
  1. **空子序列**：题目要求非空子序列，初始化时必须避免把「空乘积 1」误当成合法答案。  
  2. **乘积溢出**：在 Python 中整数不会溢出，但乘积很容易超过 `limit`，若不及时剪枝会导致状态数量爆炸。  
  3. **交替和的负数**：使用字典时要记得负数同样是合法键，不能把范围限定为非负。  
  4. **奇偶性翻转**：忘记在取元素后切换 `even ↔ odd`，会导致交替和的符号计算错误。  
- **下次遇到同类题的第一步**：先问自己「状态到底需要哪些信息才能唯一确定后续的所有可能？」——通常是「当前位置」+「累计值」+「是否需要取正/负」之类的「小状态”。有了这一步，动态规划的雏形就呼之欲出了。