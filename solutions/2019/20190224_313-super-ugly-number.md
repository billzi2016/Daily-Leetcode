# #313. 超级丑数 / Super Ugly Number

> 难度：中等 · 标签：Array、Math、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/super-ugly-number/)

---

## 题目（英文原版）

**Description**

A super ugly number is a positive integer whose prime factors are in the array primes.
Given an integer n and an array of integers primes, return the nth super ugly number.
The nth super ugly number is guaranteed to fit in a 32-bit signed integer.

**Examples**

**Example 1:**

```
Input: n = 12, primes = [2,7,13,19]
Output: 32
Explanation: [1,2,4,7,8,13,14,16,19,26,28,32] is the sequence of the first 12 super ugly numbers given primes = [2,7,13,19].
```

**Example 2:**

```
Input: n = 1, primes = [2,3,5]
Output: 1
Explanation: 1 has no prime factors, therefore all of its prime factors are in the array primes = [2,3,5].
```

**Constraints**

- 1 <= n <= 105
- 1 <= primes.length <= 100
- 2 <= primes[i] <= 1000
- primes[i] is guaranteed to be a prime number.
- All the values of primes are unique and sorted in ascending order.

---

## 题目（中文翻译）

超级丑数（super ugly number）是指其所有质因数（prime factors）均在数组 primes 中的正整数（positive integer）。给定整数 n 和整数数组 primes，返回第 n 个超级丑数。第 n 个超级丑数保证能够放入 32 位有符号整数（32-bit signed integer）中。

示例 1:  
示例 2:  
约束条件:

示例：
### 示例 1
**Input:** `n = 12, primes = [2,7,13,19]`  
**Output:** `32`  
**Explanation:** `[1,2,4,7,8,13,14,16,19,26,28,32]` 是在 `primes = [2,7,13,19]` 时前 12 个超级丑数的序列。

### 示例 2
**Input:** `n = 1, primes = [2,3,5]`  
**Output:** `1`  
**Explanation:** `1` 没有质因数，因此它的所有质因数都在数组 `primes = [2,3,5]` 中。

**约束条件**
- `1 <= n <= 10^5`
- `1 <= primes.length <= 100`
- `2 <= primes[i] <= 1000`
- `primes[i]` 保证是质数（prime number）。
- 所有 `primes` 的值互不相同，且已按升序排序。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**从 1 开始枚举正整数**，把每个数的所有质因数都拆出来，判断这些质因数是否全部在 `primes` 数组里。如果是，就把它加入「丑数」序列；当序列长度达到 `n` 时，返回最后一个数。  

- **数据结构**：我们需要一个集合（`set`）来快速判断一个因子是否在 `primes` 中。集合就像一本**词典**，给定单词（因子）可以在 O(1) 时间内查到对应的页码（是否在词典里）。  
- **正确性**：因为我们把所有正整数都检查了一遍，只要它的所有质因数在 `primes` 中，就一定会被加入序列；序列的顺序自然是从小到大，所以第 `n` 个加入的就是第 `n` 个超级丑数。  

**为什么会超时？**  
- 对每个整数我们都要做一次**分解质因数**的操作，最坏情况下要除到 sqrt(num) 才能确定是否有其他因子，这本身已经是 O(√num)。  
- 还要对每个因子检查是否在 `primes` 中（集合查找是 O(1)），但因为我们要枚举很多数字，整体时间会非常大。  

#### 代码（Python）  

```python
from typing import List

def nthSuperUglyNumber_bruteforce(n: int, primes: List[int]) -> int:
    prime_set = set(primes)                 # 把 primes 放进集合，像查字典一样 O(1) 判断
    ugly = []                               # 用来存放已经找到的超级丑数
    num = 1                                 # 从 1 开始枚举

    # 辅助函数：判断 x 的所有质因数是否都在 prime_set 里
    def is_super_ugly(x: int) -> bool:
        if x == 1:                          # 约定 1 是超级丑数
            return True
        tmp = x
        for p in prime_set:                # 只需要除以 primes 中的质数
            while tmp % p == 0:            # 能被整除就除掉
                tmp //= p
        return tmp == 1                    # 除完后如果是 1，说明没有其他因子

    while len(ugly) < n:                    # 直到找到第 n 个
        if is_super_ugly(num):
            ugly.append(num)                # 加入序列
        num += 1                             # 检查下一个整数

    return ugly[-1]                         # 第 n 个超级丑数
```

> 代码可直接运行，但在 `n` 较大（如 10⁵）时会 **卡死**，因为每个数都要完整分解质因数。

#### 复杂度  

- **时间复杂度**：大约是 `O(N * √M)`（`N` 为要找的丑数个数，`M` 为当前检查的数字大小）。这里的 `√M` 来自因数分解的最坏情况。直观上可以理解为「我们要检查很多很多数字，每检查一个都要除以很多次」。  
- **空间复杂度**：`O(1)`（只用了几个常数大小的变量和一个集合来存 `primes`，不随 `n` 增长）。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到**瓶颈在于重复的因数乘法**：我们每次都要重新去算 `prime * previous_ugly`，而其实这些乘积在之前已经出现过，只是我们没有记住。  

**核心思路**：用**多指针 + 动态规划**的方式，像「合并 k 条有序链表」一样一次性生成所有超级丑数。  

1. **维护一个数组 `ugly`**，`ugly[i]` 保存第 `i+1` 个超级丑数（下标从 0 开始）。`ugly[0] = 1` 是约定的第一个。  
2. 对于每个质数 `primes[j]`，我们维护一个指针 `idx[j]`，它指向 `ugly` 中的某个位置。`primes[j] * ugly[idx[j]]` 就是「下一个可能的超级丑数」候选值。  
3. 每一步取所有候选值的**最小值** `next_val`，把它放进 `ugly`。这一步相当于「从 k 条有序序列里挑出最小的那个」——正好对应「合并 k 条有序链表」的思想。  
4. 为了避免重复（不同质数可能产生相同的 `next_val`），**所有等于 `next_val` 的指针都要向前移动一位**。这样下次再计算时就会产生更大的数。  

> **为什么正确？**  
> - `ugly` 中的数始终是按照从小到大的顺序生成的，因为每次都选最小的候选值。  
> - 每个指针只会向前走，且每走一步都对应把 `primes[j] * ugly[idx[j]]` 加入候选集合，保证**所有**可能的超级丑数都会在某个时刻被考虑到。  
> - 当我们取到第 `n` 个数时，恰好就是第 `n` 小的超级丑数。  

#### 代码（Python）  

```python
from typing import List

def nthSuperUglyNumber(n: int, primes: List[int]) -> int:
    k = len(primes)                 # 质数的个数
    ugly = [1] * n                  # 存放前 n 个超级丑数，先全部填 1
    idx = [0] * k                   # 每个质数对应的指针，初始都指向 ugly[0] (=1)
    next_mul = primes[:]           # 当前每个指针对应的乘积，先是 primes * ugly[0]

    for i in range(1, n):           # 已经有 ugly[0]=1，下面生成 ugly[1] .. ugly[n-1]
        next_val = min(next_mul)    # 选出所有候选乘积中的最小值
        ugly[i] = next_val

        # 所有产生相同最小值的指针都要前进，防止重复
        for j in range(k):
            if next_mul[j] == next_val:
                idx[j] += 1                         # 指针向前走一步
                next_mul[j] = primes[j] * ugly[idx[j]]  # 重新计算该指针的候选乘积

    return ugly[-1]                 # 第 n 个超级丑数
```

> 代码中关键行都有中文注释，直接复制运行即可得到答案。

#### 复杂度  

- **时间复杂度**：`O(n * k)`，其中 `k = len(primes)`。每生成一个超级丑数，需要遍历 `k` 个指针找最小值并更新指针。对初学者可以把它想成「我们要做 n 次循环，每次循环里检查 k 条小路，找最短的那条」——这正是 `n × k` 次操作。  
- **空间复杂度**：`O(n + k)`。`ugly` 数组需要存 `n` 个数，指针数组和乘积数组各占 `k` 个空间。相较于暴力解的 `O(1)`，这里用了更多的额外空间，但仍然在可接受范围（`n ≤ 10⁵`，`k ≤ 100`）。

---

## 心得  

- **核心技巧**：**多指针 + 动态规划**（也叫“最小堆模拟”或“合并 k 条有序序列”）。  
- **适用的题型**：  
  1. **Ugly Number / Super Ugly Number**（本题）。  
  2. **合并 k 条有序链表**（LeetCode 23），思路相同，只是用堆实现。  
  3. **Kth Smallest Number in Multiplication Table**（LeetCode 378），也是利用有序乘积的特性。  
- **一句话总结解题钥匙**：*“把每个质数看成一条只会往前走的有序队列，始终取所有队首的最小值，即可顺序生成第 n 小的超级丑数”。*

---

## 反思  

- **第一反应**：直接遍历所有正整数并判断质因数——这是一种自然的、但效率低下的思路。  
- **最容易踩的坑**：  
  - **重复值**：不同质数的乘积可能相同（例如 `2*3 = 3*2`），如果不把所有产生相同最小值的指针都向前移动，会导致序列出现重复，从而错过后面的数。  
  - **溢出**：虽然题目保证结果在 32 位有符号整数范围，但在乘法时仍要使用 Python 的大整数特性防止意外 overflow（Python 本身不会 overflow）。  
  - **边界条件**：`n = 1` 时直接返回 1，指针的初始化必须对应 `ugly[0] = 1`。  
- **下次遇到同类题**：第一步先思考「有没有办法把所有可能的候选值保持有序」——如果能把它们看成几条有序序列的合并，就可以使用多指针或最小堆来一次性生成答案。