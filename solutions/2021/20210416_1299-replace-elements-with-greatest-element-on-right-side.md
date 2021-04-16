# #1299. 将元素替换为右侧最大元素 / Replace Elements with Greatest Element on Right Side

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/replace-elements-with-greatest-element-on-right-side/)

---

## 题目（英文原版）

**Description**

Given an array arr, replace every element in that array with the greatest element among the elements to its right, and replace the last element with -1.
After doing so, return the array.

**Examples**

**Example 1:**

```
Input: arr = [17,18,5,4,6,1]
Output: [18,6,6,6,1,-1]
Explanation: 
- index 0 --> the greatest element to the right of index 0 is index 1 (18).
- index 1 --> the greatest element to the right of index 1 is index 4 (6).
- index 2 --> the greatest element to the right of index 2 is index 4 (6).
- index 3 --> the greatest element to the right of index 3 is index 4 (6).
- index 4 --> the greatest element to the right of index 4 is index 5 (1).
- index 5 --> there are no elements to the right of index 5, so we put -1.
```

**Example 2:**

```
Input: arr = [400]
Output: [-1]
Explanation: There are no elements to the right of index 0.
```

**Constraints**

- 1 <= arr.length <= 104
- 1 <= arr[i] <= 105

---

## 题目（中文翻译）

给定一个数组 `arr`，将数组中的每个元素替换为其右侧所有元素中的最大元素（greatest element），并将最后一个元素替换为 `-1`。完成后返回修改后的数组。

### 示例

#### 示例 1
```text
Input: arr = [17,18,5,4,6,1]
Output: [18,6,6,6,1,-1]
Explanation: 
- 下标 0 → 右侧最大元素位于下标 1，值为 18。
- 下标 1 → 右侧最大元素位于下标 4，值为 6。
- 下标 2 → 右侧最大元素位于下标 4，值为 6。
- 下标 3 → 右侧最大元素位于下标 4，值为 6。
- 下标 4 → 右侧最大元素为下标 5，值为 1。
- 下标 5 → 最后一个元素，替换为 -1。
```

#### 示例 2
```text
Input: arr = [400]
Output: [-1]
Explanation: 下标 0 右侧没有元素，直接替换为 -1。
```

### 约束条件
- `1 <= arr.length <= 10^4`
- `1 <= arr[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**对每一个位置 `i`，把它右边所有元素都找出来，取最大的那个填回去**。  
- 用到的数据结构：只需要原数组本身和一个临时变量 `mx` 来保存右边的最大值。可以把 `mx` 想象成“手里拿的最大数字”，每次遍历右边的元素时把更大的数字换进去。  
- 为什么正确：题目要求把每个位置的值替换成**右侧**的最大元素，而我们正是逐个检查右侧所有元素并取最大，自然满足要求。  
- 时间/空间复杂度分析：  
  - 对每个 `i`（一共 `n` 个），我们都要遍历它右边的所有元素，最坏情况下要遍历 `n‑1 + n‑2 + … + 1 = n·(n‑1)/2` 次。用大 O 表示就是 **O(n²)**，也就是说时间会随数组长度的平方增长。  
  - 只用了常数个额外变量（比如 `mx`），所以空间是 **O(1)**，即不随 `n` 增长。

#### 代码（Python）  

```python
def replaceElements_bruteforce(arr):
    n = len(arr)
    # 创建一个新数组来存放结果，避免在遍历时把原数据改掉影响后面的比较
    res = [-1] * n          # 最后一个位置一定是 -1，先全部填好

    for i in range(n - 1):  # 最后一个元素不需要再找右侧最大值
        mx = arr[i + 1]      # 先把右边第一个元素当作最大值
        # 从 i+2 到数组末尾全部遍历，找最大值
        for j in range(i + 2, n):
            if arr[j] > mx:
                mx = arr[j]  # 发现更大的就更新 mx
        res[i] = mx          # 把找到的最大值写进结果数组

    # res[n-1] 已经是 -1，直接返回
    return res
```

#### 复杂度  

- **时间复杂度：O(n²)** — 想象一下如果数组有 10,000 个元素，暴力解大约要跑 100,000,000 次比较，明显太慢。  
- **空间复杂度：O(1)** — 只用了几个额外变量（`mx`、循环计数器），不随输入规模增大。

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈在于每次都要重新遍历右侧所有元素**。如果我们能**把右侧的最大值记下来**，后面再用时就不必重新扫描。  
- 关键观察：从右往左遍历时，**当前元素右边的最大值** 正好就是**上一次遍历时保存的最大值**。  
- 具体做法：  
  1. 从数组最右端开始，维护一个变量 `max_so_far`，它始终保存**已经遍历过的右侧元素的最大值**。  
  2. 对每个位置 `i`，先把原来的 `arr[i]` 暂存到 `temp`（因为我们马上要把 `arr[i]` 换成 `max_so_far`），再把 `arr[i]` 替换为 `max_so_far`。  
  3. 然后把 `max_so_far` 更新为 `max(max_so_far, temp)`，这样在往左继续时，它仍然是右侧的最大值。  
- 类比：把 `max_so_far` 想成“向左走的灯塔”，它照亮了左边所有位置，让它们直接看到右侧的最高峰，而不必自己去爬山。  

这种方法只需要一次线性遍历，时间大幅提升。

#### 代码（Python）  

```python
def replaceElements(arr):
    """
    从右往左遍历，只用一个变量记录右侧最大值。
    """
    n = len(arr)
    max_so_far = -1          # 最右侧没有元素，默认填 -1

    # 从最后一个元素开始往左遍历
    for i in range(n - 1, -1, -1):
        current = arr[i]     # 暂存当前值，因为接下来要被覆盖
        arr[i] = max_so_far   # 用右侧最大值覆盖当前位
        # 更新右侧最大值：取原来的 max_so_far 和 暂存的 current 两者的较大者
        if current > max_so_far:
            max_so_far = current

    return arr
```

#### 复杂度  

- **时间复杂度：O(n)** — 只遍历了一遍数组，数组长度翻倍只会导致比较次数翻倍，线性增长非常快。  
- **空间复杂度：O(1)** — 只用了常数个额外变量 `max_so_far`、`current`，不随 `n` 变化。

---

## 心得  

- 这道题考察的核心技巧是 **“从右向左维护前缀（后缀）最大值”**，属于 **单调遍历** 的典型。  
- 这种技巧常用于需要**“某个方向的极值”**的题目，例如：  
  1. **LeetCode 228. 汇总统计数组**（前缀和）  
  2. **LeetCode 1145. 二叉树中的最长连续序列**（后序遍历维护最大/最小）  
  3. **LeetCode 284. 峰值元素**（左右最大值比较）  
- **一句话总结解题钥匙**：**把“遍历右侧求最大”改成“遍历时把右侧最大值记下来”。**

---

## 反思  

- **第一反应**：看到“右侧最大”，自然想到双层循环逐个比较。  
- **最容易踩的坑**：  
  - 忘记最后一个元素要直接填 `-1`，导致答案错误。  
  - 在原地修改时直接使用 `arr[i]` 进行比较，会把原来的值覆盖掉，导致后面的 `max_so_far` 计算错误。必须先把原值存到临时变量。  
- **下次遇到同类题**，第一步应该思考**“是否可以从某一端往回遍历，把需要的极值/信息提前保存”**，而不是每次都重新扫描。这样往往能把时间复杂度从平方级降到线性级。