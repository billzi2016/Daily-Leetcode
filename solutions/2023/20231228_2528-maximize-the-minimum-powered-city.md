# #2528. 最大化最小供电城市 / Maximize the Minimum Powered City

> 难度：困难 · 标签：Array、Binary Search、Greedy、Queue、Sliding Window、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximize-the-minimum-powered-city/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array stations of length n, where stations[i] represents the number of power stations in the ith city.
Each power station can provide power to every city in a fixed range. In other words, if the range is denoted by r, then a power station at city i can provide power to all cities j such that |i - j| <= r and 0 <= i, j <= n - 1.
The power of a city is the total number of power stations it is being provided power from.
The government has sanctioned building k more power stations, each of which can be built in any city, and have the same range as the pre-existing ones.
Given the two integers r and k, return the maximum possible minimum power of a city, if the additional power stations are built optimally.
Note that you can build the k power stations in multiple cities.

**Examples**

**Example 1:**

```
Input: stations = [1,2,4,5,0], r = 1, k = 2
Output: 5
Explanation: 
One of the optimal ways is to install both the power stations at city 1. 
So stations will become [1,4,4,5,0].
- City 0 is provided by 1 + 4 = 5 power stations.
- City 1 is provided by 1 + 4 + 4 = 9 power stations.
- City 2 is provided by 4 + 4 + 5 = 13 power stations.
- City 3 is provided by 5 + 4 = 9 power stations.
- City 4 is provided by 5 + 0 = 5 power stations.
So the minimum power of a city is 5.
Since it is not possible to obtain a larger power, we return 5.
```

**Example 2:**

```
Input: stations = [4,4,4,4], r = 0, k = 3
Output: 4
Explanation: 
It can be proved that we cannot make the minimum power of a city greater than 4.
```

**Constraints**

- n == stations.length
- 1 <= n <= 105
- 0 <= stations[i] <= 105
- 0 <= r <= n - 1
- 0 <= k <= 109

---

## 题目（中文翻译）

给定一个下标从 **0** 开始、长度为 **n** 的整数数组 `stations`，其中 `stations[i]` 表示第 **i** 座城市拥有的电站数量。  
每座电站可以为固定范围内的所有城市供电。换句话说，若范围记为 `r`，则位于城市 **i** 的电站能够为所有满足 `|i - j| ≤ r` 且 `0 ≤ i, j ≤ n - 1` 的城市 **j** 提供电力。  
城市的 **供电量**（power）指的是为该城市提供电力的电站总数。  

政府批准再建造 **k** 座电站，每座电站可以建在任意城市，且其供电范围与已有电站相同。  
给定整数 `r` 与 `k`，返回在最优建造这些额外电站的情况下，**所有城市中最小供电量的最大可能值**。  
注意，`k` 座电站可以分布在多个城市中建造。

## 示例

### 示例 1

```
Input: stations = [1,2,4,5,0], r = 1, k = 2
Output: 5
Explanation:
一种最优方案是将两座新电站都建在城市 1。
于是 `stations` 变为 [1,4,4,5,0]。
- 城市 0 的供电量为 1 + 4 = 5
- 城市 1 的供电量为 1 + 4 + 4 = 9
- 城市 2 的供电量为 4 + 4 + 5 = 13
- 城市 3 的供电量为 5 + 4 = 9
- 城市 4 的供电量为 0 + 5 = 5
因此所有城市的最小供电量为 5，达到了最大可能值。
```

### 示例 2

```
Input: stations = [4,4,4,4], r = 0, k = 3
Output: 4
Explanation:
可以证明，无论如何建造这 3 座新电站，城市的最小供电量都无法超过 4。
```

## 约束条件

- `n == stations.length`
- `1 ≤ n ≤ 10^5`
- `0 ≤ stations[i] ≤ 10^5`
- `0 ≤ r ≤ n - 1`
- `0 ≤ k ≤ 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一座新电站都放在可以让最弱城市的供电量提升最多的位置**，然后反复遍历整个城市数组，直到把 `k` 块钱用完为止。

- **遍历**：对每一次放置新电站，都遍历所有城市，算出每座城市在当前范围 `r` 内的总电站数（即「城市的供电量」）。这相当于在每个城市「向左看 `r` 格，向右看 `r` 格」把所有电站加起来。
- **选点**：找出当前供电量最小的城市，把新电站建在它的**覆盖范围内**（任意一个能让该城市供电量提升的城市都可以）。
- **重复**：重复 `k` 次。

> **类比**：把每座城市想象成一片土地，需要水（电站）灌溉。每次我们拿到一桶水，就先找最干渴的那块土地，把水倒在能覆盖它的地方。

这个方法之所以**正确**（可以得到一个可行解），是因为我们每一步都在真的把电站放进了数组，且每次都提升了最小城市的供电量。只要把 `k` 块钱全部用完，得到的最小供电量就是一种可能的答案。

不过，这种「每次都全局扫描」的做法非常慢：

- 计算一次所有城市的供电量需要 `O(n·(2r+1))`（每座城市要遍历它的左右 `r` 格）。
- 放置 `k` 块电站需要重复上面的过程 `k` 次。

当 `n` 达到 `10⁵`、`k` 甚至可以是 `10⁹` 时，根本不可行。

#### 代码（Python）

```python
def brute_force(stations, r, k):
    n = len(stations)
    # 辅助函数：返回城市 i 的供电量
    def power(i):
        left = max(0, i - r)
        right = min(n - 1, i + r)
        return sum(stations[left:right + 1])

    for _ in range(k):
        # 计算每座城市的供电量
        powers = [power(i) for i in range(n)]
        # 找到供电量最小的城市
        min_idx = powers.index(min(powers))
        # 在它的覆盖范围内随便选一个位置建电站（这里选最左边）
        build_pos = max(0, min_idx - r)
        stations[build_pos] += 1   # 实际上把电站加到数组里
    # 最后返回最小供电量
    final_powers = [power(i) for i in range(n)]
    return min(final_powers)
```

> 代码仅作思路展示，**在大数据下会超时**。

#### 复杂度

- **时间复杂度**：`O(k * n * r)`（最坏情况下 `r ≈ n`，相当于 `O(k * n²)`）。  
  - 大白话：如果城市有 10 万个，`k` 也是 10 万，执行次数会是 10⁵ × 10⁵ = 10¹⁰ 次，电脑根本跑不完。
- **空间复杂度**：`O(1)`（只用了常数级别的额外变量）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要重新遍历全部城市来统计供电量**，以及**一次只能加 1 块电站**。我们可以把这两个问题分别优化：

1. **快速算出所有城市的初始供电量**  
   - 使用**线段扫描（Line Sweep）**或**前缀和**的技巧，只遍历一次数组就能得到每座城市在范围 `r` 内的累计电站数。  
   - 思路：把每座已有电站的影响范围 `[i‑r, i+r]` 在一个差分数组 `diff` 上做 “+stations[i]” 的标记，最后做一次前缀和得到真实供电量。  
   - 类比：给每座电站发一张「覆盖券」给它能影响的所有城市，所有券收集完后再算总数。

2. **把“放 k 块电站”转化为“检查是否可以让最小供电量 ≥ target”**  
   - 设想我们已经知道答案的下界 `target`（比如 5），我们想验证 **是否能在不超过 k 块电站的情况下，使所有城市的供电量都 ≥ 5**。  
   - 这可以用**贪心 + 滑动窗口**完成：从左到右遍历城市，如果当前城市的供电量 `< target`，说明必须在它的**右侧窗口**（即能覆盖它的最右边位置）里额外建电站来补足。我们把缺口 `need = target - cur_power` 直接加到窗口的最右端（也就是 `i + r`），并在差分数组里记录这次“额外建的电站”。随后继续向右滑动窗口，利用前缀和实时得到每座城市的“当前供电量”。  
   - 关键点是**一次性把缺口全部加在窗口最右端**，因为这样对后面的城市影响最大，最符合贪心思想。

3. **二分搜索答案**  
   - 供电量的最小值显然是 **单调递增** 的：如果可以让最小供电量达到 `x`，那么当然也能达到任何 `y ≤ x`。  
   - 因此我们在 `[low, high]` 区间上二分搜索 `target`，每次用上一步的检查函数 `can_achieve(target)` 判断是否可行。  
   - `low` 可以从 `0` 开始，`high` 可以取 **所有电站加上 `k` 后的最大可能供电量**：  
     ```
     high = max(initial_power) + k   # 因为每块电站最多能让一个城市的供电量再加 1
     ```
   - 二分结束后得到的 `low`（或 `high`）就是答案。

下面把上述思路拆解成代码块并配上中文注释。

#### 代码（Python）

```python
from typing import List

def maxMinPower(stations: List[int], r: int, k: int) -> int:
    n = len(stations)

    # ---------- 1. 预处理：算出每座城市的初始供电量 ----------
    # diff 用来做差分，后面做前缀和得到真实供电量
    diff = [0] * (n + 1)          # 多一个哨兵，防止右边界越界

    for i, cnt in enumerate(stations):
        left = max(0, i - r)      # 影响范围左端
        right = min(n - 1, i + r) # 影响范围右端
        diff[left] += cnt
        diff[right + 1] -= cnt    # right+1 位置减掉，表示区间结束

    # 初始供电量（前缀和）
    init_power = [0] * n
    cur = 0
    for i in range(n):
        cur += diff[i]
        init_power[i] = cur

    # ---------- 2. 检查函数：能否让最小供电量 >= target ----------
    def can_achieve(target: int) -> bool:
        """贪心+滑动窗口，返回是否只用 ≤k 块电站即可让所有城市供电≥target"""
        add = [0] * (n + 1)   # 记录额外建的电站的差分
        used = 0               # 已经使用的电站数
        cur_add = 0            # 当前窗口内累计的额外电站

        for i in range(n):
            cur_add += add[i]                 # 把窗口左端的增量加进来
            # 当前城市的供电量 = 初始 + 窗口内额外的
            cur_power = init_power[i] + cur_add

            if cur_power < target:            # 供电不足，需要补
                need = target - cur_power     # 还差多少
                used += need
                if used > k:                  # 超出预算，直接返回 False
                    return False

                # 把 need 块电站加在能够覆盖 i 的最右端位置
                # 那个位置是 i + r（但不能超过数组右边界）
                pos = min(n - 1, i + r)
                add[pos] += need               # 差分左端加 need
                # 右端的结束位置是 pos + r + 1，但我们不需要再减，因为
                # 后面遍历到 pos+1 时已经不在 i 能覆盖的窗口里了
                # 为了让后面的窗口不再受这批 need 影响，需要在 pos+ r + 1 处减掉
                end = pos + r + 1
                if end <= n:
                    add[end] -= need

                cur_add += need                # 当前窗口立即感受到这批新增
        return True

    # ---------- 3. 二分搜索 ----------
    low, high = 0, max(init_power) + k   # 最高不可能超过这个值
    while low < high:
        mid = (low + high + 1) // 2      # 上取整，防止死循环
        if can_achieve(mid):
            low = mid                    # 可以达到，尝试更大
        else:
            high = mid - 1               # 达不到，缩小区间

    return low
```

**代码要点解释**  

| 行号 | 关键操作 | 类比/解释 |
|------|----------|-----------|
| 4‑12 | 用差分 `diff` 把每座已有电站的覆盖范围标记出来 | 像在地图上画「影响圈」的入口和出口 |
| 15‑20| 前缀和得到 `init_power` | 把所有「入口」累加，得到每座城市真实被多少电站覆盖 |
| 27‑28| `add` 数组记录**额外**建的电站的差分 | 把我们后面「临时增建」的电站也用同样的方式登记 |
| 33‑40| `cur_power = init_power[i] + cur_add` | 当前城市的供电 = 原始 + 已经在窗口里加的 |
| 42‑54| 当供电不足时，把缺口全部加到**最右端** `pos` | 把缺口放在最能帮助后面城市的位置，类似「把水往右推」 |
| 56‑58| `if used > k: return False` | 用光预算就直接认定不行 |
| 68‑77| 二分搜索 `target`，利用 `can_achieve` 判断可行性 | 像在「能否达到」的区间里不断逼近上限 |

#### 复杂度

- **时间复杂度**：`O(n log M)`，其中 `M` 是答案的取值范围（`max(init_power) + k`），`log M ≤ 60`（因为 `k ≤ 10⁹`）。  
  - 大白话：我们只遍历一次数组（`n`），但要把答案范围二分大约 30‑60 次，每次检查都是线性 `O(n)`，所以总体是「一次遍历 × 二分次数」。
- **空间复杂度**：`O(n)`。我们使用了 `diff`、`init_power`、`add` 三个长度为 `n` 的数组。  
  - 大白话：需要额外的几个「记事本」来记录差分和临时增建的电站，大小和原数组成正比。

---

## 心得

- **核心技巧**：**单调二分 + 前缀和（或差分）+ 贪心滑动窗口**。  
  1. 把「最大化最小值」转化为「判断是否能达到某个阈值」的可行性问题。  
  2. 用差分/前缀和一次性算出所有城市的覆盖量，避免 `O(n·r)` 的重复累加。  
  3. 在可行性检查中，贪心地把缺口放在能够覆盖当前城市且对后面影响最大的右端位置，配合滑动窗口实时维护当前累计增量。

- **适用的类似题目**  
  1. *Maximum Number of Darts Inside a Circle*（二分 + 前缀和）  
  2. *Minimum Number of Operations to Make Array Continuous*（二分 + 滑动窗口）  
  3. *Minimum Additions to Make Parentheses Valid*（贪心 + 差分）  

- **一句话总结解题钥匙**  
  > **把“最小值 ≥ X”变成“在预算 k 内用最少的增量把每个缺口填满”，再用二分搜索找最大的 X。**

---

## 反思

- **第一反应**：看到“最大化最小值”立刻想到二分搜索，随后想到需要一个快速判断函数。  
- **最容易踩的坑**  
  1. **边界处理**：差分数组的右端需要 `+1`，否则会导致最后几座城市的覆盖量少算一次。  
  2. **窗口右端的结束位置**：在 `can_achieve` 中必须在 `pos + r + 1` 位置减去 `need`，否则后面的城市会错误地一直受到这批增量的影响。  
  3. **整型溢出**：在 Python 中不怕，但如果换成 C++/Java，需要使用 `long long` 防止 `k`（最高 10⁹）乘以 `n` 时溢出。  
  4. **二分取中**：使用上取整 `(low + high + 1) // 2` 防止死循环。

- **下次遇到同类题**：  
  1. 先判断是否可以把「最大化最小值」转化为「单调可判定」的形式。  
  2. 考虑用前缀和/差分一次性算出所有区间贡献，避免 `O(n·r)` 的重复统计。  
  3. 在判定函数里用**贪心+滑动窗口**把缺口一次性推到最右端，确保每一步都是局部最优且不影响后续的判断。