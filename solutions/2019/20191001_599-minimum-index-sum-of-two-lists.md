# #599. 两个列表的最小索引和 / Minimum Index Sum of Two Lists

> 难度：简单 · 标签：Array、Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/minimum-index-sum-of-two-lists/)

---

## 题目（英文原版）

**Description**

Given two arrays of strings list1 and list2, find the common strings with the least index sum.
A common string is a string that appeared in both list1 and list2.
A common string with the least index sum is a common string such that if it appeared at list1[i] and list2[j] then i + j should be the minimum value among all the other common strings.
Return all the common strings with the least index sum. Return the answer in any order.

**Examples**

**Example 1:**

```
Input: list1 = ["Shogun","Tapioca Express","Burger King","KFC"], list2 = ["Piatti","The Grill at Torrey Pines","Hungry Hunter Steakhouse","Shogun"]
Output: ["Shogun"]
Explanation: The only common string is "Shogun".
```

**Example 2:**

```
Input: list1 = ["Shogun","Tapioca Express","Burger King","KFC"], list2 = ["KFC","Shogun","Burger King"]
Output: ["Shogun"]
Explanation: The common string with the least index sum is "Shogun" with index sum = (0 + 1) = 1.
```

**Example 3:**

```
Input: list1 = ["happy","sad","good"], list2 = ["sad","happy","good"]
Output: ["sad","happy"]
Explanation: There are three common strings:
"happy" with index sum = (0 + 1) = 1.
"sad" with index sum = (1 + 0) = 1.
"good" with index sum = (2 + 2) = 4.
The strings with the least index sum are "sad" and "happy".
```

**Constraints**

- 1 <= list1.length, list2.length <= 1000
- 1 <= list1[i].length, list2[i].length <= 30
- list1[i] and list2[i] consist of spaces ' ' and English letters.
- All the strings of list1 are unique.
- All the strings of list2 are unique.
- There is at least a common string between list1 and list2.

---

## 题目（中文翻译）

给定两个字符串数组（array of strings）`list1` 和 `list2`，找出索引和（index sum）最小的公共字符串。  
公共字符串指同时出现在 `list1` 和 `list2` 中的字符串。  
索引和最小的公共字符串是指若该字符串在 `list1[i]` 与 `list2[j]` 位置出现，则 `i + j` 在所有公共字符串中为最小值。  
返回所有满足该条件的公共字符串，答案的顺序可以任意。

## 示例

### 示例 1  
**输入**: `list1 = ["Shogun","Tapioca Express","Burger King","KFC"], list2 = ["Piatti","The Grill at Torrey Pines","Hungry Hunter Steakhouse","Shogun"]`  
**输出**: `["Shogun"]`  
**解释**: 唯一的公共字符串是 `"Shogun"`。

### 示例 2  
**输入**: `list1 = ["Shogun","Tapioca Express","Burger King","KFC"], list2 = ["KFC","Shogun","Burger King"]`  
**输出**: `["Shogun"]`  
**解释**: 索引和最小的公共字符串是 `"Shogun"`，其索引和为 `0 + 1 = 1`。

### 示例 3  
**输入**: `list1 = ["happy","sad","good"], list2 = ["sad","happy","good"]`  
**输出**: `["sad","happy"]`  
**解释**: 共有三个公共字符串：  
- `"happy"` 的索引和为 `0 + 1 = 1`。  
- `"sad"` 的索引和为 `1 + 0 = 1`。  
- `"good"` 的索引和为 `2 + 2 = 4`。  
索引和最小的字符串是 `"sad"` 与 `"happy"`。

## 约束条件

- `1 <= list1.length, list2.length <= 1000`
- `1 <= list1[i].length, list2[i].length <= 30`
- `list1[i]` 和 `list2[i]` 仅由空格 `' '` 与英文字母组成
- `list1` 中的所有字符串互不相同
- `list2` 中的所有字符串互不相同
- `list1` 与 `list2` 至少存在一个公共字符串

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把 `list1` 和 `list2` 中的每一对元素都拿出来比较一次，如果相等就算出它们的下标和 `i + j`，把所有满足“出现于两列表”的字符串以及对应的下标和记录下来，最后挑出下标和最小的那几个字符串返回。

- **使用的数据结构**  
  - **两个普通的列表**（list），因为我们只需要顺序遍历它们。  
  - **一个临时的变量** 用来保存当前最小的下标和（`min_sum`），以及一个列表 `ans` 用来收集所有达到最小下标和的字符串。  

- **为什么这个方法正确**  
  - 暴力遍历保证了 **每一种可能的配对**（即每个 `list1[i]` 与每个 `list2[j]`）都会被检查一次。只要出现相同的字符串，就一定会计算出它的下标和并参与比较，所以不会遗漏任何符合条件的答案。

- **复杂度分析（大白话版）**  
  - 假设 `list1` 长度为 `n`，`list2` 长度为 `m`。我们要把 `n` 个元素分别和 `m` 个元素配对，类似于“把两排学生两两握手”。握手的次数是 `n × m`，这就是 **O(n·m)**，也就是所谓的 **二次时间**（在最坏情况下会比较很多次）。  
  - 额外使用的空间只有几个计数器和返回的答案，和输入规模无关，算作 **O(1)**（常数空间）。

#### 代码（Python）  

```python
def findRestaurant(list1, list2):
    # 初始化最小下标和为一个很大的数，后面会逐渐变小
    min_sum = float('inf')
    ans = []                     # 用来保存所有满足最小下标和的字符串

    # 双层循环，遍历每一对下标 (i, j)
    for i, s1 in enumerate(list1):          # enumerate 能一次得到下标 i 和元素 s1
        for j, s2 in enumerate(list2):
            if s1 == s2:                    # 找到相同的字符串
                cur_sum = i + j            # 计算它们的下标和
                if cur_sum < min_sum:      # 出现了更小的下标和
                    min_sum = cur_sum
                    ans = [s1]              # 重新开始收集答案，只保留当前字符串
                elif cur_sum == min_sum:   # 与当前最小下标和相同
                    ans.append(s1)          # 再加入答案列表
    return ans
```

#### 复杂度  

- **时间复杂度：** `O(n·m)`  
  - 这里的 `n`、`m` 分别是两列表的长度。想象两个人分别排成两列，每个人要和另一列的每个人握手一次，握手次数正好是 `n×m`。  

- **空间复杂度：** `O(1)`（不计答案列表）  
  - 只用了几个整数变量和一个用于存放答案的列表，答案列表的大小最多是所有公共字符串的个数，和输入规模无关。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于两层循环**：每次我们都要把 `list2` 扫一遍来找匹配的字符串。其实我们只需要 **快速判断一个字符串是否在另一列表中出现**，并且还能直接得到它的下标。  

**哈希表（字典）** 正好能帮我们做到这一点：把较短的列表（这里任选 `list1`）的每个字符串映射成它的下标，形成 `{"Shogun":0, "Tapioca Express":1, ...}`。查找一个字符串是否在 `list1` 中，只需要一次 “字典查询”，时间是 **O(1)**（常数时间），相当于在字典里直接翻到对应的页码。  

有了这个映射后，只需要一次遍历 `list2`，每遇到一个字符串就：

1. 用字典判断它是否在 `list1` 中出现。  
2. 若出现，则取出 `list1` 中的下标 `i`，再加上当前在 `list2` 中的下标 `j`，得到下标和 `i + j`。  
3. 同暴力解一样，用 `min_sum` 与 `ans` 维护最小下标和的答案。

这样 **只需要一次遍历 `list1` + 一次遍历 `list2`**，时间降到线性 `O(n + m)`，空间上需要存储字典，大小为 `O(n)`（或 `O(m)`，取决于我们把哪一个列表放进哈希表）。

**关键概念解释**  

- **哈希表（Python 中的 dict）**：想象它是一张“词典”，每个单词（这里是字符串）对应一个页码（这里是下标）。查找某个单词，只需要直接看页码，时间非常快，和遍历整个列表相比快了很多。  
- **单次遍历**：只走一遍列表，像在跑步机上走一步，不会来回跑。

#### 代码（Python）  

```python
def findRestaurant(list1, list2):
    # 1. 把 list1 的字符串映射到它们的下标，形成哈希表
    index_map = {s: i for i, s in enumerate(list1)}   # O(n) 的时间，O(n) 的空间

    min_sum = float('inf')
    ans = []

    # 2. 遍历 list2，检查每个字符串是否在哈希表里
    for j, s in enumerate(list2):                     # O(m) 的时间
        if s in index_map:                            # O(1) 的哈希查询
            i = index_map[s]                          # 取出在 list1 中的下标
            cur_sum = i + j
            if cur_sum < min_sum:                     # 发现更小的下标和
                min_sum = cur_sum
                ans = [s]                             # 重新开始收集答案
            elif cur_sum == min_sum:                  # 与当前最小相同
                ans.append(s)                         # 再加入答案列表
    return ans
```

#### 复杂度  

- **时间复杂度：** `O(n + m)`  
  - 第一步把 `list1` 放进字典需要遍历一次，`n` 次操作。第二步遍历 `list2` 也是 `m` 次，每次只做常数时间的哈希查询和算术运算。整体就是两次线性遍历，和列表长度成正比。  
  - 与暴力解的 `n·m` 相比，这里即使列表各有 1000 项，也只需要大约 2000 次操作，快得多。  

- **空间复杂度：** `O(n)`（或 `O(min(n, m))`）  
  - 额外的字典保存了 `list1` 中每个字符串对应的下标，需要占用与 `list1` 长度相同的空间。答案列表本身的空间不算在额外空间里，因为它是必须返回的结果。  

---  

## 心得  

- **核心技巧**：**使用哈希表把一个列表的元素映射为下标，实现 O(1) 查找**。  
- **适用的题型**：  
  1. 两数组的交集并需要额外信息（如下标、出现次数）——如 *Intersection of Two Arrays II*。  
  2. 在两个序列中寻找满足某种“最小/最大”条件的共同元素——如 *Find the Duplicate Number*（利用哈希或集合）。  
- **一句话总结解题钥匙**：**把可以重复查询的“是否在集合中”操作，用哈希表一次搞定，避免双层循环**。  

---  

## 反思  

- **第一反应**：看到“找公共字符串”，自然想到“双层循环遍历”，因为最直接的思路总是检查每一对。  
- **最容易踩的坑**：  
  - 忘记处理 **多个答案**（下标和相同的情况），导致只返回了一个字符串。  
  - 在暴力实现里没有提前退出或记录最小值，导致每次都重新遍历所有已经找到的公共元素，增加不必要的时间。  
  - 忽视 **空列表** 或 **只有一个公共元素** 的边界情况。  
- **下次遇到同类题**，第一步应该问自己：**“是否可以把其中一个列表预处理成哈希表，以实现 O(1) 的快速查询？”** 这一步往往能把时间复杂度从平方级降到线性级。