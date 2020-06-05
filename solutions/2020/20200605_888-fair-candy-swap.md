# #888. **公平糖果交换** / Fair Candy Swap

> 难度：简单 · 标签：Array、Hash Table、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/fair-candy-swap/)

---

## 题目（英文原版）

**Description**

Alice and Bob have a different total number of candies. You are given two integer arrays aliceSizes and bobSizes where aliceSizes[i] is the number of candies of the ith box of candy that Alice has and bobSizes[j] is the number of candies of the jth box of candy that Bob has.
Since they are friends, they would like to exchange one candy box each so that after the exchange, they both have the same total amount of candy. The total amount of candy a person has is the sum of the number of candies in each box they have.
Return an integer array answer where answer[0] is the number of candies in the box that Alice must exchange, and answer[1] is the number of candies in the box that Bob must exchange. If there are multiple answers, you may return any one of them. It is guaranteed that at least one answer exists.

**Examples**

**Example 1:**

```
Input: aliceSizes = [1,1], bobSizes = [2,2]
Output: [1,2]
```

**Example 2:**

```
Input: aliceSizes = [1,2], bobSizes = [2,3]
Output: [1,2]
```

**Example 3:**

```
Input: aliceSizes = [2], bobSizes = [1,3]
Output: [2,3]
```

**Constraints**

- 1 <= aliceSizes.length, bobSizes.length <= 104
- 1 <= aliceSizes[i], bobSizes[j] <= 105
- Alice and Bob have a different total number of candies.
- There will be at least one valid answer for the given input.

---

## 题目（中文翻译）

Alice 和 Bob 各自拥有的糖果总数不同。给定两个整数数组（integer arrays）`aliceSizes` 和 `bobSizes`，其中 `aliceSizes[i]` 表示 Alice 第 `i` 盒糖果中的糖果数量，`bobSizes[j]` 表示 Bob 第 `j` 盒糖果中的糖果数量。

由于是好朋友，他们希望各交换一盒糖果，使得交换后两人的糖果总数相等。一个人的糖果总数等于他拥有的所有糖果盒中糖果数量的和。

返回一个长度为 2 的整数数组 `answer`，其中 `answer[0]` 为 Alice 需要交换的糖果盒中的糖果数量，`answer[1]` 为 Bob 需要交换的糖果盒中的糖果数量。如果存在多个答案，返回任意一个即可。题目保证至少存在一个可行答案。

---

### 示例

**示例 1**  
输入: `aliceSizes = [1,1]`, `bobSizes = [2,2]`  
输出: `[1,2]`

**示例 2**  
输入: `aliceSizes = [1,2]`, `bobSizes = [2,3]`  
输出: `[1,2]`

**示例 3**  
输入: `aliceSizes = [2]`, `bobSizes = [1,3]`  
输出: `[2,3]`

---

### 约束条件

- `1 <= aliceSizes.length, bobSizes.length <= 10^4`
- `1 <= aliceSizes[i], bobSizes[j] <= 10^5`
- Alice 和 Bob 的糖果总数不同。
- 对于给定的输入，至少存在一个有效答案。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法就是把 **所有可能的交换** 都枚举一遍，看看哪一对能够让两个人的糖果总数相等。  
- **数据结构**：只需要两个普通的列表（`aliceSizes`、`bobSizes`），不需要额外的结构。可以把列表想象成装糖果盒子的箱子。  
- **为什么正确**：如果我们把每一种可能的 `(Alice 的盒子 a , Bob 的盒子 b)` 都尝试一次，必然能找到题目保证存在的那一对。  
- **复杂度大白话**：  
  - `O(m·n)` 里的 `m` 是 Alice 的盒子数量，`n` 是 Bob 的盒子数量。就像把两个人的盒子排成两行，然后让每个 Alice 的盒子去和每个 Bob 的盒子“握手”。如果两行各有 1000 个盒子，总共要握手 1,000,000 次。  
  - 空间只用了常数级的变量（比如几个累计和），记作 `O(1)`，意思是占用的内存几乎不随输入规模增长。  

#### 代码（Python）  

```python
from typing import List

def fairCandySwap_brute(aliceSizes: List[int], bobSizes: List[int]) -> List[int]:
    # 计算两个人最初的糖果总数
    sum_alice = sum(aliceSizes)          # Alice 的总糖果数
    sum_bob = sum(bobSizes)              # Bob   的总糖果数

    # 枚举所有可能的交换组合
    for a in aliceSizes:                 # 遍历 Alice 的每个盒子
        for b in bobSizes:               # 与 Bob 的每个盒子配对
            # 交换后两人的总数分别是：
            #   sum_alice - a + b   与   sum_bob - b + a
            if sum_alice - a + b == sum_bob - b + a:
                return [a, b]            # 找到答案，直接返回
    # 题目保证一定有解，理论上不会走到这里
    return []
```

#### 复杂度  
- **时间复杂度**：`O(m·n)` —— 需要检查每一对盒子，最坏情况下是所有组合都要尝试一次。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，和输入规模无关。  

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到 **瓶颈** 在于「双重循环」——每次都要把 Alice 的每个盒子和 Bob 的每个盒子配对，次数太多。  
我们可以利用等式化简，把查找过程变成 **一次遍历 + 哈希查找**，把时间从 `O(m·n)` 降到 `O(m+n)`。

1. **等式推导**  
   交换前后两人的总数相等：  
   \[
   \text{sumA} - a + b = \text{sumB} - b + a
   \]  
   把式子整理得到：  
   \[
   a - b = \frac{\text{sumA} - \text{sumB}}{2}
   \]  
   左边是「Alice 送出的盒子数」减「Bob 收到的盒子数」，右边是一个常数（记作 `diff`），只要我们知道 `diff`，就只需要在 Bob 的盒子里找一个满足 `b = a - diff` 的盒子即可。

2. **核心数据结构：集合（Set）**  
   - **类比**：集合就像一本「糖果盒子号码表」，我们可以在 O(1) 时间内检查某个号码是否存在（相当于查字典的页码）。  
   - 把 Bob 的所有盒子大小放进一个 `set`，这样判断 `b` 是否存在只需要常数时间。

3. **算法步骤**  
   - 计算 `sumA`、`sumB`，得到 `diff = (sumA - sumB) // 2`（一定是整数，因为题目保证有解）。  
   - 把 `bobSizes` 放进集合 `bob_set`。  
   - 遍历 `aliceSizes`，对每个 `a` 计算 `b = a - diff`，如果 `b` 在 `bob_set` 中，就找到了答案。  

4. **为什么正确**  
   - 只要找到满足 `a - b = diff` 的一对 `(a, b)`，根据推导的等式必然能让两人的总数相等。  
   - 由于题目保证至少有一个答案，上面的遍历必然会命中。

#### 代码（Python）  

```python
from typing import List

def fairCandySwap(aliceSizes: List[int], bobSizes: List[int]) -> List[int]:
    # 1. 计算两个人的糖果总数
    sum_alice = sum(aliceSizes)
    sum_bob = sum(bobSizes)

    # 2. 目标差值：a - b = diff
    diff = (sum_alice - sum_bob) // 2   # // 是整数除法，保证是整数

    # 3. 把 Bob 的盒子大小放进集合，方便 O(1) 查找
    bob_set = set(bobSizes)            # 类似“糖果盒子号码表”

    # 4. 遍历 Alice 的每个盒子，寻找匹配的 Bob 盒子
    for a in aliceSizes:
        b = a - diff                    # 根据等式计算应该找的 Bob 盒子大小
        if b in bob_set:                # O(1) 检查是否存在
            return [a, b]               # 找到答案，直接返回
    # 题目保证一定有解，代码不会走到这里
    return []
```

#### 复杂度  
- **时间复杂度**：`O(m + n)` ——  
  - 计算两次求和各是 `O(m)`、`O(n)`；  
  - 构造集合 `bob_set` 为 `O(n)`；  
  - 遍历 Alice 的列表为 `O(m)`。  
  总体线性增长，远快于暴力的 `O(m·n)`。  
- **空间复杂度**：`O(n)` —— 需要存放 Bob 的所有盒子大小的集合，大小随 Bob 的盒子数量线性增长。  

---  

## 心得  

- **核心技巧**：把「交换后总数相等」的约束转化为一个 **差值等式**，然后用 **哈希集合** 实现常数时间查找。  
- **适用的题型**：  
  1. 两数组的“配对”问题，需要满足某种线性关系（如 `a + b = target`）。  
  2. “找出两个数组中满足特定差值的元素”——如 LeetCode 167（Two Sum II – Input array is sorted）可以用二分或哈希实现。  
  3. “数组交换后满足某种平衡条件”——如 1656（Design an Ordered Stream）中的顺序匹配。  
- **一句话总结解题钥匙**：**把等式化简成常数差值，再用哈希表快速定位匹配元素**。  

---  

## 反思  

- **第一反应**：看到「交换」和「总数相等」会立刻想到列等式并求差值，或者直接想遍历所有配对（暴力）。  
- **最容易踩的坑**：  
  - 忘记除以 2（因为每交换一次会影响两个人的总数），导致 `diff` 计算错误。  
  - 使用普通列表查找 `b`，时间会退化到 `O(m·n)`，失去优化的意义。  
  - 忽略整数除法的细节，在 Python 2 中 `/` 会产生浮点数，需要使用 `//`。  
- **下次遇到同类题**：第一步先**写出数学等式**，看能否把问题转化为「在一个数组中找满足某个固定值的元素」，随后考虑使用 **哈希表/集合** 或 **二分查找** 进行快速定位。