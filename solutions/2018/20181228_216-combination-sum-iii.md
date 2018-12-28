# #216. 组合总和 III / Combination Sum III

> 难度：中等 · 标签：Array、Backtracking · [LeetCode 链接](https://leetcode.com/problems/combination-sum-iii/)

---

## 题目（英文原版）

**Description**

Find all valid combinations of k numbers that sum up to n such that the following conditions are true:
Return a list of all possible valid combinations. The list must not contain the same combination twice, and the combinations may be returned in any order.

**Examples**

**Example 1:**

```
Input: k = 3, n = 7
Output: [[1,2,4]]
Explanation:
1 + 2 + 4 = 7
There are no other valid combinations.
```

**Example 2:**

```
Input: k = 3, n = 9
Output: [[1,2,6],[1,3,5],[2,3,4]]
Explanation:
1 + 2 + 6 = 9
1 + 3 + 5 = 9
2 + 3 + 4 = 9
There are no other valid combinations.
```

**Example 3:**

```
Input: k = 4, n = 1
Output: []
Explanation: There are no valid combinations.
Using 4 different numbers in the range [1,9], the smallest sum we can get is 1+2+3+4 = 10 and since 10 > 1, there are no valid combination.
```

**Constraints**

- 2 <= k <= 9
- 1 <= n <= 60

---

## 题目（中文翻译）

找出所有由 **k** 个不同数字组成且和为 **n** 的合法组合（combination），满足以下条件：

- 返回所有可能的合法组合列表（list）。  
- 列表中不能出现重复的组合，组合的返回顺序可以任意（order）。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  
- 2 ≤ k ≤ 9  
- 1 ≤ n ≤ 60  

---

### 示例

**示例 1**  
Input: k = 3, n = 7  
Output: [[1,2,4]]  
**解释**：  
1 + 2 + 4 = 7  
没有其他合法组合。

**示例 2**  
Input: k = 3, n = 9  
Output: [[1,2,6],[1,3,5],[2,3,4]]  
**解释**：  
1 + 2 + 6 = 9  
1 + 3 + 5 = 9  
2 + 3 + 4 = 9  
没有其他合法组合。

**示例 3**  
Input: k = 4, n = 1  
Output: []  
**解释**：  
使用范围在 [1,9] 内的 4 个不同数字，最小可能的和为 1+2+3+4 = 10，且 10 > 1，故不存在合法组合。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **1~9** 这 9 个数字全部列出来，尝试所有可能的取法，找出恰好有 **k** 个数且和等于 **n** 的组合。

- **数据结构**：我们可以把 1~9 放进一个普通的列表 `nums = [1,2,...,9]`。  
  类比：把数字想成超市里 9 种商品的货架，挑选商品就相当于从列表里挑元素。

- **遍历方式**：对每个数字都有「选」或「不选」两种可能，这相当于 **二进制的 0/1 选择**，所有可能的子集总数是 `2^9 = 512`。我们只需要把每个子集的长度和求和检查一下，满足 `len==k && sum==n` 的就放进答案。

- **为什么正确**：因为我们枚举了 **所有** 可能的子集，凡是满足题目要求的组合必然会在枚举过程中被发现。

- **复杂度大白话**：  
  - **时间复杂度** `O(2^9 * 9)`：每个子集最多要遍历 9 次来算长度和，`2^9=512` 是一个常数，但如果把范围改成 `m`（这里是 9），时间就是 `O(2^m * m)`，随 `m` 指数增长。  
  - **空间复杂度** `O(1)`（不计返回结果）：只用几个临时变量，和输入规模无关。

#### 代码（Python）

```python
from itertools import combinations
def combinationSum3_brute(k: int, n: int):
    ans = []
    # 1~9 所有数字的组合，长度固定为 k
    for combo in combinations(range(1, 10), k):   # itertools 自动生成不重复的组合
        if sum(combo) == n:                       # 检查和是否等于 n
            ans.append(list(combo))               # 把元组转成列表再加入答案
    return ans

# 示例
print(combinationSum3_brute(3, 7))   # [[1, 2, 4]]
print(combinationSum3_brute(3, 9))   # [[1, 2, 6], [1, 3, 5], [2, 3, 4]]
```

#### 复杂度

- **时间复杂度**：`O(C(9, k) * k)`，其中 `C(9, k)` 表示从 9 个数里挑 `k` 个的组合数。  
  - 大白话：组合数本身最大不超过 9!/(4!5!) = 126，乘以每次求和的 `k`（最多 9），整体仍是一个很小的常数。  
- **空间复杂度**：`O(1)`（不计返回的答案列表）。只用了几个循环变量。

---

### 2. 最优解

#### 思路  

暴力解已经可以 AC（因为搜索空间只有 512），但如果把数字范围扩大到 `m`，枚举所有子集就会爆炸。**回溯（Backtracking）** 能在搜索过程中**提前剪枝**，只遍历真正有可能得到答案的分支。

从暴力解的瓶颈来看：

- **瓶颈 1**：我们一次性把所有组合生成出来，然后再筛选。  
- **瓶颈 2**：即使当前已经选的数字之和已经大于 `n`，仍会继续往下递归。

**优化思路**：

1. **递归+深度优先搜索**：从小到大依次尝试数字 `start … 9`，每选一个就进入下一层递归。  
2. **剪枝条件**  
   - **和超限**：`current_sum > n` 时直接返回，因为后面再加任何正数只会更大。  
   - **剩余数字不够**：如果已经选了 `len(path)` 个数，剩下还能选的最大数量是 `9 - start + 1`。如果 `len(path) + (9 - start + 1) < k`，说明即使把后面的所有数字都选上也达不到 `k`，直接剪枝。  
   - **最小可能和 > n**：当前已经选了 `len(path)` 个数，最小还能选的 `k - len(path)` 个数分别是 `start, start+1, …`。如果这些最小和加上 `current_sum` 已经大于 `n`，也可以提前返回。  
3. **终止条件**：当选到恰好 `k` 个数且 `current_sum == n` 时，把当前路径复制一份加入答案。

> **核心数据结构**：`path`（当前递归路径）是一个 **列表**，类似装满糖果的盒子，里面的糖果顺序就是我们选的数字顺序。  
> **回溯** 的过程就像在盒子里放糖果，放进去后发现不对，就把最后一个糖果拿出来（`pop`），再尝试别的糖果。

#### 代码（Python）

```python
def combinationSum3(k: int, n: int):
    """
    使用回溯（深度优先搜索）找出所有恰好 k 个数、和为 n 的组合。
    数字只能用 1~9，且每个数字只能使用一次。
    """
    ans = []                     # 用来收集所有合法组合

    def dfs(start: int, path: list, cur_sum: int):
        """
        参数说明：
        - start: 下一次尝试的数字下标（因为组合要递增，防止重复）
        - path: 当前已经选好的数字序列
        - cur_sum: path 中数字的累计和
        """
        # 1. 已经选够 k 个数字
        if len(path) == k:
            if cur_sum == n:                 # 和正好等于 n，找到一组答案
                ans.append(path.copy())      # 复制一份防止后面修改影响结果
            return                            # 无论是否相等，都不再继续往下选

        # 2. 剪枝：如果当前和已经大于 n，后面再加只会更大
        if cur_sum > n:
            return

        # 3. 剪枝：剩余可选数字的最大数量不足以凑满 k 个
        #    还有 (9 - start + 1) 个数可以选
        if len(path) + (9 - start + 1) < k:
            return

        # 4. 从 start 开始枚举可能的下一个数字
        for num in range(start, 10):          # 10 是开区间，上限为 9
            # 剪枝：如果把当前最小的几个数字都加上已经超过 n，直接结束循环
            #   这里用 (k - len(path) - 1) 表示选了 num 以后还需要的数字个数
            min_possible = cur_sum + num + sum(range(num + 1, num + 1 + (k - len(path) - 1)))
            if min_possible > n:
                break   # 之后的 num 更大，只会让和更大

            path.append(num)                  # 选这个数字
            dfs(num + 1, path, cur_sum + num) # 递归搜索下一个位置
            path.pop()                        # 撤销选择，回到上层

    dfs(1, [], 0)    # 从数字 1 开始搜索
    return ans

# 示例
print(combinationSum3(3, 7))   # [[1, 2, 4]]
print(combinationSum3(3, 9))   # [[1, 2, 6], [1, 3, 5], [2, 3, 4]]
print(combinationSum3(4, 1))   # []
```

#### 复杂度

- **时间复杂度**：`O(C(9, k))`（实际遍历的组合数），因为回溯在每层最多只遍历一次每个数字，并且通过剪枝大幅削减无效分支。  
  - 大白话：最坏情况下仍然是把所有合法的 `k` 组合都枚举一遍，最多 `C(9,4)=126` 种，远远小于暴力的 `2^9=512`。  
- **空间复杂度**：`O(k)`，递归栈的深度最多是 `k`（最多 9），再加上保存当前路径的列表。返回结果的空间不计入额外复杂度。

---

## 心得

- **核心技巧**：**回溯（DFS） + 剪枝**，在搜索组合问题时，先把搜索空间限定在“递增且不重复”，再用当前和、剩余可选数等信息提前退出不可能的分支。  
- **适用的题型**  
  1. `Combination Sum` / `Combination Sum II`（求和组合）  
  2. `Subset II`（去重子集）  
  3. `Palindrome Partitioning`（划分回文子串）  
- **一句话总结解题钥匙**：**“把大树砍成小枝，先判断这根枝还能长到目标吗，不行就直接剪掉。”**

---

## 反思

- **第一反应**：看到 “1~9 的 k 个数”，立刻想到 **枚举所有子集** 或 **组合**，因为数字范围极小，直接暴力就能过。  
- **最容易踩的坑**  
  - 忘记 **每个数字只能使用一次**，导致出现 `[1,1,5]` 之类的非法组合。  
  - 没有提前剪枝，递归层数虽然不深，但会产生不必要的计算。  
  - 边界情况 `k > 9` 或 `n` 超出最小/最大可能和时直接返回空列表。  
- **下次遇到同类题**：第一步先判断 **搜索空间大小**（如数字范围、组合长度），如果仍然在可接受范围内可以先写 **暴力**，随后思考 **怎样在递归/迭代过程中用已知信息提前剪枝**。这样既能快速验证思路，又能在规模扩大时直接切换到高效的回溯实现。