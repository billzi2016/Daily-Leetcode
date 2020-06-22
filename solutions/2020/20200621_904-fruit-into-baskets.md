# #904. 水果进篮子 / Fruit Into Baskets

> 难度：中等 · 标签：Array、Hash Table、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/fruit-into-baskets/)

---

## 题目（英文原版）

**Description**

You are visiting a farm that has a single row of fruit trees arranged from left to right. The trees are represented by an integer array fruits where fruits[i] is the type of fruit the ith tree produces.
You want to collect as much fruit as possible. However, the owner has some strict rules that you must follow:
Given the integer array fruits, return the maximum number of fruits you can pick.

**Examples**

**Example 1:**

```
Input: fruits = [1,2,1]
Output: 3
Explanation: We can pick from all 3 trees.
```

**Example 2:**

```
Input: fruits = [0,1,2,2]
Output: 3
Explanation: We can pick from trees [1,2,2].
If we had started at the first tree, we would only pick from trees [0,1].
```

**Example 3:**

```
Input: fruits = [1,2,3,2,2]
Output: 4
Explanation: We can pick from trees [2,3,2,2].
If we had started at the first tree, we would only pick from trees [1,2].
```

**Constraints**

- 1 <= fruits.length <= 105
- 0 <= fruits[i] < fruits.length

---

## 题目（中文翻译）

你正在参观一座农场，农场里有一排从左到右排列的水果树。树木用整数数组 **fruits** 表示，其中 `fruits[i]` 是第 `i` 棵树产生的水果种类（type）。  
你希望尽可能多地采集水果，但必须遵守农场主的严格规则。  
给定整数数组 **fruits**，返回你能够采集的水果的最大数量。

**示例 1**  
```text
Input: fruits = [1,2,1]
Output: 3
Explanation: 我们可以从全部 3 棵树上采集水果。
```

**示例 2**  
```text
Input: fruits = [0,1,2,2]
Output: 3
Explanation: 我们可以从树 `[1,2,2]` 上采集水果。  
如果从第一棵树开始，只能采集到树 `[0,1]`。
```

**示例 3**  
```text
Input: fruits = [1,2,3,2,2]
Output: 4
Explanation: 我们可以从树 `[2,3,2,2]` 上采集水果。  
如果从第一棵树开始，只能采集到树 `[1,2]`。
```

**约束条件**  
- `1 <= fruits.length <= 10^5`  
- `0 <= fruits[i] < fruits.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的连续子数组**，检查每个子数组里出现的水果种类是否不超过两种。如果满足条件，就把它的长度（即可以采的水果数量）和当前的最大值比较，取最大。  

- **使用的数据结构**：  
  - `set`（集合）——可以把它想象成“水果种类的清单”，往里面放水果编号，集合会自动去重，就像查字典时只记下出现过的词。  
  - `list`（列表）——用来保存当前检查的子数组，类似于我们手里的一串水果。  

- **为什么正确**：  
  对于每一个起始位置 `i`，我们都尝试把后面的树一个一个加入篮子，只要加入后篮子里水果种类仍 ≤ 2，就说明这段连续的树是合法的。遍历完所有 `i`，就一定会找到最长的合法段落。

- **时间/空间复杂度**：  
  - 外层有 `n`（数组长度）次循环，内层最坏情况下也要遍历 `n` 次（比如所有水果都不相同），于是总的比较次数大约是 `n × n = n²`。  
  - 用大写的 **O(n²)** 表示“随着输入规模 `n` 增大，运行时间会以 n 的平方速度增长”。如果 `n = 10⁴`，运行时间大约是 100 000 000 次比较，明显太慢。  
  - 空间上我们只需要一个 `set`（最多保存 3 个种类）和一些临时变量，和 `n` 无关，记作 **O(1)**（常数空间）。

#### 代码（Python）

```python
from typing import List

def totalFruit_bruteforce(fruits: List[int]) -> int:
    n = len(fruits)
    max_len = 0

    # 枚举子数组的左端点 i
    for i in range(n):
        types = set()          # 当前子数组里出现的水果种类
        # 枚举右端点 j
        for j in range(i, n):
            types.add(fruits[j])   # 把第 j 棵树的水果放进篮子
            if len(types) > 2:     # 种类已经超过两种，不能再继续
                break
            # 此时子数组 [i, j] 合法，更新最大长度
            max_len = max(max_len, j - i + 1)

    return max_len
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环，最坏情况下每一次都要遍历整个数组。  
- **空间复杂度**：`O(1)` —— 只用了几个常数级的变量（集合最多 3 个元素）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都从头重新统计子数组里的水果种类**。其实我们可以**在遍历的过程中维护一个滑动窗口**，窗口左端点和右端点一起向右移动，始终保持窗口内的水果种类不超过两种。

**关键点**：

1. **滑动窗口**：把它想象成一只会“收缩”和“扩张”的篮子。右端点 `right` 每前进一步，就把对应的水果加入篮子；如果加入后篮子里种类超过两种，就要把左端点 `left` 向右移动，直到种类再次 ≤ 2。  
2. **哈希表（字典）**：用 `dict` 记录每种水果在当前窗口出现的次数。它就像一本“水果种类 → 计数”的小账本，查找、增加、减少都在 O(1) 时间内完成。  
3. **窗口长度**：每次窗口合法（种类 ≤ 2）时，用 `right - left + 1` 计算当前可以采的水果数，和历史最大值比较。

**步骤**：

- 初始化 `left = 0`，`max_len = 0`，以及空的计数字典 `cnt = {}`。  
- 遍历 `right` 从 0 到 n‑1：  
  - 把 `fruits[right]` 加入字典，计数加一。  
  - **检查是否违规则**：如果字典的键数（即种类数）大于 2，进入收缩过程。  
    - 循环把 `left` 右移：把 `fruits[left]` 的计数减一，计数为 0 时把对应键删掉（相当于从账本中抹去这种水果），然后 `left += 1`。  
    - 直到字典键数 ≤ 2。  
  - 此时窗口合法，更新 `max_len = max(max_len, right - left + 1)`。  

整个过程只遍历一次数组，左端点和右端点各自最多向右移动 n 步，所以 **时间是线性的**。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def totalFruit(fruits: List[int]) -> int:
    """
    滑动窗口 + 哈希表（字典）统计窗口内每种水果的数量
    """
    left = 0                     # 窗口左边界
    max_len = 0                  # 记录最大合法窗口长度
    cnt = defaultdict(int)      # 计数字典，默认值 0

    # 右边界逐步右移
    for right, fruit in enumerate(fruits):
        cnt[fruit] += 1          # 把右边的新水果放进篮子

        # 若种类超过两种，开始收缩左边界
        while len(cnt) > 2:
            left_fruit = fruits[left]
            cnt[left_fruit] -= 1     # 把左边的水果取走
            if cnt[left_fruit] == 0: # 计数为 0，说明这种水果已不在窗口
                del cnt[left_fruit]  # 从字典中删除键
            left += 1                # 窗口左边界右移

        # 此时窗口合法，更新答案
        max_len = max(max_len, right - left + 1)

    return max_len
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 每个元素最多被右指针加入一次，又最多被左指针移除一次，整体线性增长。相对于暴力的 `O(n²)`，快了很多。  
- **空间复杂度**：`O(1)` —— 字典里最多只会保存 3 种水果的计数（因为一旦出现第 3 种就会立即收缩），所以占用的空间不随 `n` 增长。

---

## 心得

- **核心技巧**：滑动窗口 + 哈希表（或字典）统计窗口内元素的出现次数。  
- **适用的题型**：  
  1. “最长子串/子数组中至多包含 K 种不同字符/数字”——例如 LeetCode 340 *Longest Substring with At Most K Distinct Characters*。  
  2. “子数组之和满足某种约束的最长/最短区间”——如 LeetCode 209 *Minimum Size Subarray Sum*（使用滑动窗口）。  
  3. “最多包含两种字符的最长子串”——类似本题的变体，只是字符换成字母。  
- **一句话总结**：**用滑动窗口把“连续”变成“可动态调整的区间”，再用哈希表快速判断种类是否超限**。

---

## 反思

- **第一反应**：看到“只能挑两种水果”，立刻想到“最多两种不同元素的最长连续子数组”。于是尝试暴力枚举所有子数组。  
- **最容易踩的坑**：  
  - **忘记在左指针收缩时删除计数为 0 的键**，导致字典始终保存旧的种类，使 `len(cnt)` 永远大于 2，窗口无法收缩。  
  - **边界条件**：空数组或只有一种水果的情况也要返回正确长度（这里题目保证长度 ≥ 1）。  
  - **计数溢出**：在 Python 中整数不会溢出，但在其他语言要注意计数变量的类型。  
- **下次遇到同类题的第一步**：先判断**“窗口内需要维护哪些信息”（种类、和、最大值…）**，然后决定使用**滑动窗口**还是**双指针**，并准备好**哈希表/计数数组**来快速更新这些信息。