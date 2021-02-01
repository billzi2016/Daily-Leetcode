# #1186. 最多一次删除的最大子数组和 / Maximum Subarray Sum with One Deletion

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/maximum-subarray-sum-with-one-deletion/)

---

## 题目（英文原版）

**Description**

Given an array of integers, return the maximum sum for a non-empty subarray (contiguous elements) with at most one element deletion. In other words, you want to choose a subarray and optionally delete one element from it so that there is still at least one element left and the sum of the remaining elements is maximum possible.
Note that the subarray needs to be non-empty after deleting one element.

**Examples**

**Example 1:**

```
Input: arr = [1,-2,0,3]
Output: 4
Explanation: Because we can choose [1, -2, 0, 3] and drop -2, thus the subarray [1, 0, 3] becomes the maximum value.
```

**Example 2:**

```
Input: arr = [1,-2,-2,3]
Output: 3
Explanation: We just choose [3] and it's the maximum sum.
```

**Example 3:**

```
Input: arr = [-1,-1,-1,-1]
Output: -1
Explanation: The final subarray needs to be non-empty. You can't choose [-1] and delete -1 from it, then get an empty subarray to make the sum equals to 0.
```

**Constraints**

- 1 <= arr.length <= 105
- -104 <= arr[i] <= 104

---

## 题目（中文翻译）

给定一个整数数组，返回一个非空子数组（subarray）（连续元素）的最大和，且该子数组至多可以删除 **一个** 元素。换句话说，你需要选取一个子数组，并可以选择性地删除其中的一个元素，使得删除后仍保留至少一个元素，并且剩余元素的和尽可能大。  
注意：删除元素后，子数组仍必须是非空的。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  

- $1 \leq \text{arr.length} \leq 10^5$  
- $-10^4 \leq \text{arr}[i] \leq 10^4$

---

### 示例

**示例 1**  
```
Input: arr = [1,-2,0,3]
Output: 4
Explanation: 可以选择子数组 [1, -2, 0, 3] 并删除 -2，得到子数组 [1, 0, 3]，其和为最大值 4。
```

**示例 2**  
```
Input: arr = [1,-2,-2,3]
Output: 3
Explanation: 直接选择子数组 [3] 即可得到最大和。
```

**示例 3**  
```
Input: arr = [-1,-1,-1,-1]
Output: -1
Explanation: 子数组必须非空。不能先选择 [-1] 再删除其中的 -1 得到空子数组来使和为 0。
```

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**枚举所有可能的子数组**，并且在每个子数组内部再枚举一次是否删除其中的一个元素。  

- **子数组**：数组中连续的一段，就像一根绳子只剪掉两头，留下的中间部分。  
- **删除元素**：相当于在这根绳子上挑出一个结点把它剪掉，剩下的仍然是一根连续的绳子（只要删后还有结点）。  

我们可以用两层循环 `i, j` 表示子数组的左端点和右端点（`i ≤ j`），再用第三层循环 `k`（`i ≤ k ≤ j`）表示要删掉的元素位置。对每一种 `(i, j, k)` 组合，计算剩余元素的和，取最大值。  

为什么这种方法一定能得到答案？因为我们把**所有合法的子数组和所有合法的删除位置**都遍历了一遍，最大值自然会被找到。  

但是，这种做法会非常慢。  
- 外层两个循环遍历所有子数组，数量是 `n*(n+1)/2 ≈ O(n²)`。  
- 再加上第三层遍历删除位置，最坏情况是每个子数组长度为 `n`，于是总时间是 `O(n³)`。  

#### 代码（Python）  

```python
def maximumSum_bruteforce(arr):
    n = len(arr)
    best = -10**9                      # 记录最大和，初始设为一个很小的数
    for i in range(n):                # 子数组左端点
        for j in range(i, n):          # 子数组右端点
            # 1）不删元素的情况（直接求子数组和）
            cur_sum = sum(arr[i:j+1])
            best = max(best, cur_sum)

            # 2）删掉子数组中任意一个元素的情况
            for k in range(i, j+1):    # 要删掉的下标
                # 删除后剩下的和 = 子数组和 - 被删掉的那个数
                cur_sum_del = cur_sum - arr[k]
                best = max(best, cur_sum_del)
    return best
```

> **注意**：  
> - `sum(arr[i:j+1])` 在每次循环里都会重新遍历一次子数组，实际时间更高。  
> - 这里的实现仅为说明思路，**不建议在正式提交中使用**。

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - “立方”意味着如果数组长度是 1000，程序要做大约 10⁹ 次运算，几乎不可能在 1 秒内跑完。  
- **空间复杂度**：`O(1)`  
  - 只用了常数级的额外变量（`best、cur_sum` 等），不随输入规模增长。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到**瓶颈**在于我们反复计算子数组的和。  
如果我们能**一次性得到每个位置左侧（含自己）的最大子数组和**，以及**右侧（含自己）的最大子数组和**，那么只需要常数时间就能算出“删除某个元素后，两边最大和之和”。  

这正是 **Kadane 算法**（求不删元素时的最大子数组和） 的思想：  
- `forward[i]` = 以 `i` 为结尾的子数组的最大和。  
- `backward[i]` = 以 `i` 为起点的子数组的最大和。  

计算方法（从左到右）：

```
forward[i] = max(arr[i], forward[i-1] + arr[i])
```

解释：要么从前面延伸过来（`forward[i-1] + arr[i]`），要么自己单独成一个子数组（`arr[i]`）。这一步就像在走路时决定是继续往前走还是在这里重新出发。

同理，**从右往左**计算 `backward[i]`：

```
backward[i] = max(arr[i], backward[i+1] + arr[i])
```

得到这两个数组后，我们可以枚举**被删除的下标 `k`**，把左边最大子数组（结尾在 `k-1`）和右边最大子数组（起点在 `k+1`）相加：

```
candidate = forward[k-1] + backward[k+1]
```

此外，**不删任何元素**的情况仍然是合法的，只需要取 `forward[i]`（或 `backward[i]`）的最大值即可。  

整个过程只遍历了几遍数组，时间 `O(n)`，空间 `O(n)`（可以进一步压缩到 `O(1)`，但对初学者保持可读性更重要）。

#### 代码（Python）  

```python
def maximumSum(arr):
    n = len(arr)
    # forward[i] : 以 i 为结尾的最大子数组和
    forward = [0] * n
    forward[0] = arr[0]
    for i in range(1, n):
        # 要么从前面延伸，要么自己单独开始
        forward[i] = max(arr[i], forward[i-1] + arr[i])

    # backward[i] : 以 i 为起点的最大子数组和
    backward = [0] * n
    backward[-1] = arr[-1]
    for i in range(n-2, -1, -1):
        backward[i] = max(arr[i], backward[i+1] + arr[i])

    # 初始答案可以是「不删任何元素」的最大子数组和
    ans = max(forward)   # 或者 max(backward)，两者相等

    # 枚举删除位置 k（必须保证左、右两侧都有元素）
    for k in range(1, n-1):          # 两端不删，因为删后会空
        cand = forward[k-1] + backward[k+1]
        ans = max(ans, cand)

    return ans
```

> **关键行中文注释**  
> - `forward[i] = max(arr[i], forward[i-1] + arr[i])` # 决定是继续还是重新开始  
> - `backward[i] = max(arr[i], backward[i+1] + arr[i])` # 同理，只是从右往左  
> - `ans = max(forward)` # 不删元素的最佳情况  
> - `cand = forward[k-1] + backward[k+1]` # 删除 k 后，左侧最大 + 右侧最大  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历了三遍数组（一次正向，一次逆向，一次枚举删除点），即使 `n = 10⁵` 也能在毫秒级完成。  
- **空间复杂度**：`O(n)`  
  - 需要两个额外数组 `forward`、`backward`，每个长度为 `n`，即占用线性空间。  
  - 对于更进阶的优化，可把 `backward` 的值在枚举时即时计算，从而把空间降到 `O(1)`，但这里为了思路清晰保留 `O(n)`。

---

## 心得  

- **核心技巧**：利用 Kadane 算法分别求“左侧最大子数组和”和“右侧最大子数组和”，再在 O(1) 时间内合并得到“删除某个元素后的最大和”。  
- **适用的题型**  
  1. **带限制的最大子数组**（如最多删除 k 个元素、最多翻转一次等）。  
  2. **分割数组求最大和**（比如把数组分成两段，各自求最大子数组和再相加）。  
  3. **环形数组的最大子数组**（可以把环拆成前后两段，类似思路）。  
- **一句话总结解题钥匙**：**先把每个位置左/右的最佳子数组预先算好，删掉某个元素时只需把两侧的最佳结果拼在一起**。

---

## 反思  

- **第一反应**：想到枚举所有子数组并尝试删除元素，直接写出三层循环的暴力实现。  
- **最容易踩的坑**  
  - **边界条件**：删除数组第一个或最后一个元素会导致子数组为空，需要排除或单独处理。  
  - **全负数情况**：不能把答案默认为 0，必须保证子数组非空，答案可能是最大的负数。  
  - **整数溢出**（在 Python 不会出现，但在某些语言需要注意）。  
- **下次遇到同类题**：第一步先思考“如果不删元素，最大子数组和怎么求？”（Kadane），再在此基础上考虑“删除一个元素相当于把左侧最大子数组和和右侧最大子数组和拼起来”。这样可以快速定位到前缀/后缀 DP 的思路。