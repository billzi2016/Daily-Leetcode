# #1785. 使数组和等于给定值的最少添加元素数 / Minimum Elements to Add to Form a Given Sum

> 难度：中等 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-elements-to-add-to-form-a-given-sum/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and two integers limit and goal. The array nums has an interesting property that abs(nums[i]) <= limit.
Return the minimum number of elements you need to add to make the sum of the array equal to goal. The array must maintain its property that abs(nums[i]) <= limit.
Note that abs(x) equals x if x >= 0, and -x otherwise.

**Examples**

**Example 1:**

```
Input: nums = [1,-1,1], limit = 3, goal = -4
Output: 2
Explanation: You can add -2 and -3, then the sum of the array will be 1 - 1 + 1 - 2 - 3 = -4.
```

**Example 2:**

```
Input: nums = [1,-10,9,1], limit = 100, goal = 0
Output: 1
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= limit <= 106
- -limit <= nums[i] <= limit
- -109 <= goal <= 109

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `nums` 和两个整数 `limit`、`goal`。数组 `nums` 满足一个特殊属性：`abs(nums[i]) <= limit`。  
返回为使数组的所有元素之和等于 `goal` 所需添加的最少元素个数。添加的元素仍必须满足 `abs(nums[i]) <= limit`。  
注意，`abs(x)` 在 `x >= 0` 时等于 `x`，否则等于 `-x`。

**示例 1**  
```text
Input: nums = [1,-1,1], limit = 3, goal = -4
Output: 2
Explanation: 你可以添加 -2 和 -3，则数组的和为 1 - 1 + 1 - 2 - 3 = -4。
```

**示例 2**  
```text
Input: nums = [1,-10,9,1], limit = 100, goal = 0
Output: 1
```

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= limit <= 10^6`  
- `-limit <= nums[i] <= limit`  
- `-10^9 <= goal <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **“要让数组的和等于 goal”** 看成“从现在的数组出发，不断往里塞新元素，直到和恰好等于 goal”。  

- 先算出原数组的和 `s = sum(nums)`。  
- 设还差 `diff = goal - s`。如果 `diff = 0`，说明已经满足目标，不需要再加任何元素。  
- 否则我们可以把 **每一次** 加的元素当作一次“选择”。因为题目限制每个元素的绝对值不能超过 `limit`，所以合法的选择范围是 `[-limit, …, -1, 0, 1, …, limit]`（就像在字典里查单词，键是数值，值是它是否在范围内）。  
- 我们可以用 **深度优先搜索 (DFS)** 或 **广度优先搜索 (BFS)**，枚举所有可能的添加序列，看看最少需要几次才能把 `diff` 消掉。

> **为什么这个方法能得到正确答案？**  
> 因为搜索遍历了 **所有** 合法的添加方式，只要有一种方式可以让和等于 goal，搜索一定会找到；而我们在搜索时记录最少的步数，自然得到最小值。

> **这一步的缺点在哪里？**  
> 枚举的组合数会指数级爆炸。假设 `limit = 3`，每次可以选 7（-3…3）个数；如果答案需要 10 个元素，搜索空间就是 `7^10 ≈ 2.8×10⁸`，根本跑不完。

#### 代码（Python）

```python
from collections import deque

def minElements_bruteforce(nums, limit, goal):
    """
    暴力 BFS：每次向数组里加入一个合法的数，直到和等于 goal。
    只适合极小的输入（演示思路），实际会超时。
    """
    s = sum(nums)                     # 现在的和
    if s == goal:
        return 0                      # 已经达标

    diff = goal - s                    # 还差多少
    # BFS 用队列保存 (当前差值, 已经加的元素个数)
    q = deque()
    q.append((diff, 0))
    visited = set([diff])              # 防止重复状态

    while q:
        cur, steps = q.popleft()
        # 尝试把下一个数放进来，范围是 [-limit, limit]
        for x in range(-limit, limit + 1):
            nxt = cur - x               # 加入 x 后，差值会变成 cur - x
            if nxt == 0:                # 正好消掉差值
                return steps + 1
            if nxt not in visited:
                visited.add(nxt)
                q.append((nxt, steps + 1))
    # 理论上这里不会到达，因为总能用足够多的 limit/-limit 把差值消掉
    return -1
```

> **关键行注释**  
> - `s = sum(nums)`: 计算原数组的总和。  
> - `for x in range(-limit, limit + 1)`: 枚举所有合法的新增元素。  
> - `nxt = cur - x`: 加上 `x` 后，剩余需要补的差值更新。  

#### 复杂度  

- **时间复杂度**：`O((2·limit+1)^k)`，其中 `k` 是答案的最小元素个数。可以想象成“一棵 2·limit+1 分叉的树，深度是 k”。当 `k` 稍大时，这个数字会非常大，实际不可接受。  
- **空间复杂度**：`O((2·limit+1)^k)` 用于保存 BFS 队列和 visited 集合，同样会爆炸。

---

### 2. 最优解  

#### 思路  

从暴力思路可以看出，**搜索的瓶颈**在于我们一次只考虑 **“加入一个任意值”**，于是要尝试很多组合。其实我们并不需要关心每一次具体加入哪个数，只要知道 **“一次最多能改变量多少”** 就行。

1. **把原数组先“归零”**  
   设 `s = sum(nums)`，我们把原数组的贡献先移走，问题等价于：**在空数组里，用若干个数（每个的绝对值 ≤ limit）凑出 `goal - s`**。这一步叫 **“归一化”**，因为只剩下一个目标差值 `diff = goal - s`，而不必再关心原数组里有什么。

2. **一次能改多少**  
   - 每个新元素的绝对值最多是 `limit`，所以**一次加入的数最多能把差值减少 `limit`**（如果差值是正的，我们加 `limit`；如果是负的，我们加 `-limit`）。  
   - 因此，**只要把差值的绝对值除以 `limit`，向上取整**，就得到最少需要的元素个数。  
   - 向上取整的公式可以写成整数除法的“技巧”：  
     \[
     \text{ceil}(a / b) = \frac{a + b - 1}{b}
     \]  
     这里的 `a = |diff|`，`b = limit`。

3. **公式**  
   \[
   \text{answer} = \left\lceil \frac{|goal - \text{sum}(nums)|}{\text{limit}} \right\rceil
                = \frac{|goal - \text{sum}(nums)| + \text{limit} - 1}{\text{limit}}
   \]

4. **类比**  
   把 `limit` 想象成“一把最大长度为 limit 的木棍”。我们要用若干根这样的木棍拼成一段长度等于 `|diff|`，最少需要几根？显然是把整段尽量用长木棍填满，最后剩下的不足一根的那段仍然需要再加一根（即向上取整）。

#### 代码（Python）

```python
def minElements(nums, limit, goal):
    """
    最优解：只用 O(1) 时间算出答案。
    思路：把原数组的和先抵消，剩下的差值 diff 必须用若干个
          绝对值不超过 limit 的数来凑齐。一次最多改动 limit，
          所以答案是 ceil(|diff| / limit)。
    """
    total = sum(nums)                # 原数组的和
    diff = abs(goal - total)         # 还差多少（取绝对值，方向不重要）

    # 向上取整的整数写法： (diff + limit - 1) // limit
    # // 是整数除法，保证返回的是整数而不是浮点数
    return (diff + limit - 1) // limit
```

> **关键行注释**  
> - `total = sum(nums)`: 先把原数组的贡献算出来。  
> - `diff = abs(goal - total)`: 归一化后，只剩下要填的距离，取绝对值是因为方向可以随意（正加负减）。  
> - `(diff + limit - 1) // limit`: 实现向上取整的技巧，保证即使 `diff` 不是 `limit` 的整数倍，也会多加一根“木棍”。

#### 复杂度  

- **时间复杂度**：`O(n)`，其中 `n = len(nums)`，只需要一次遍历求和。对比暴力的指数级，这已经是线性时间了。  
- **空间复杂度**：`O(1)`，只用了常数个额外变量（和、差值），不随输入规模增长。

---

## 心得  

- **核心技巧**：把已有数组的贡献“抵消”，只关注差值；随后使用 **向上取整** 计算最少的 “限幅” 元素个数。  
- **适用场景**：  
  1. **“最少次数使数组和达到目标”**（如本题）。  
  2. **“用最大步长走到指定位置”**（如 `minimum moves to reach target`）。  
  3. **“用固定容量的容器装满一定体积”**（如装水、装箱问题的简化版）。  
- **一句话总结**：**把问题转化为“用长度为 limit 的木棍拼出剩余距离”，答案就是向上取整的木棍根数。**

---

## 反思  

- **第一反应**：看到“abs(nums[i]) ≤ limit”立刻想到每个数都有上限，于是想把所有数都取极限值 `±limit`，再看看差多少。  
- **最容易踩的坑**：  
  - 忘记先把原数组的和算出来，直接对 `goal` 取整会出错。  
  - 忽略负数的情况，直接用 `goal // limit`（向下取整）会导致答案偏小。  
  - 在 Python 中使用 `/` 会得到浮点数，导致精度问题或返回非整数，需要改用 `//` 并加上向上取整的技巧。  
- **下次类似题的第一步**：**把已有的贡献全部消掉，只剩下一个“还差多少”。** 然后检查单次操作的最大幅度，直接用除法向上取整得到最少步数。