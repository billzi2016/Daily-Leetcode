# #771. 珠宝与石头 / Jewels and Stones

> 难度：简单 · 标签：Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/jewels-and-stones/)

---

## 题目（英文原版）

**Description**

You're given strings jewels representing the types of stones that are jewels, and stones representing the stones you have. Each character in stones is a type of stone you have. You want to know how many of the stones you have are also jewels.
Letters are case sensitive, so "a" is considered a different type of stone from "A".

**Examples**

**Example 1:**

```
Input: jewels = "aA", stones = "aAAbbbb"
Output: 3
```

**Example 2:**

```
Input: jewels = "z", stones = "ZZ"
Output: 0
```

**Constraints**

- 1 <= jewels.length, stones.length <= 50
- jewels and stones consist of only English letters.
- All the characters of jewels are unique.

---

## 题目（中文翻译）

给定字符串 **jewels（jewels）**，表示珠宝的类型；以及字符串 **stones（stones）**，表示你拥有的石头。`stones` 中的每个字符代表一种你拥有的石头类型。请统计你拥有的石头中有多少是珠宝。

字母区分大小写（case sensitive），因此 `'a'` 与 `'A'` 被视为不同的石头类型。

**示例 1：**  
**示例 2：**  

**约束条件：**
- `1 <= jewels.length, stones.length <= 50`
- `jewels` 和 `stones` 仅由英文字母组成。
- `jewels` 中的所有字符均唯一。

**示例：**  
示例 1:  
Input: jewels = "aA", stones = "aAAbbbb"  
Output: 3  

示例 2:  
Input: jewels = "z", stones = "ZZ"  
Output: 0

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**把每一颗石头都和珠宝表里的每一种珠宝比较一次**。  
- **使用的数据结构**：这里我们只需要两个普通的字符串。字符串本质上是字符的数组，就像一本书的每一页上都有若干个字母。  
- **生活化类比**：想象你手里有一堆石头（stones），你想知道有多少是珠宝（jewels）。最笨的办法就是把每颗石头拿出来，和珠宝清单上的每一种珠宝逐个比对，看看是否相同。  
- **正确性**：只要遍历到了所有石头，并且对每颗石头都检查了所有珠宝种类，肯定不会漏掉任何一次匹配，所以计数一定是准确的。  

#### 代码（Python）  
```python
def numJewelsInStones_bruteforce(jewels: str, stones: str) -> int:
    count = 0                     # 记录是珠宝的石头数量
    for stone in stones:          # 逐颗遍历手里的石头
        for jewel in jewels:      # 与珠宝表里的每一种珠宝比较
            if stone == jewel:    # 发现相同，说明这颗是珠宝
                count += 1
                break            # 找到后就可以停止内部循环，免得重复计数
    return count
```

#### 复杂度  
- **时间复杂度**：`O(m * n)`，其中 `m = len(jewels)`，`n = len(stones)`。  
  - 大白话：如果珠宝种类有 5 种，石头有 10 颗，就要比较 5 × 10 = 50 次。  
- **空间复杂度**：`O(1)`，只用了常数个额外变量（`count`、循环变量），不随输入规模增长。

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈在于每颗石头都要遍历一次珠宝表**，导致时间是两者长度的乘积。  
我们可以把**“珠宝表”变成一种“查字典”的数据结构**——**哈希表**（在 Python 中直接用 `set` 或 `dict`）。  

- **哈希表的类比**：想象一本字典，左边是单词（这里是珠宝字符），右边是对应的页码（这里只需要记“有”这件事）。查找一个单词只需要一次快速定位，而不需要遍历整本书。  
- **优化步骤**  
  1. 把 `jewels` 中的每个字符放进 `set`，相当于建立一个“珠宝查找表”。  
  2. 再遍历 `stones`，每看到一个石头字符，就在 `set` 里 **一次 O(1) 的查找** 看它是否是珠宝。  
  3. 如果是，就把计数器加一。  

这样就把 **每颗石头的检查时间从 O(m) 降到了 O(1)**，整体时间降为 `O(m + n)`。

#### 代码（Python）  
```python
def numJewelsInStones_optimal(jewels: str, stones: str) -> int:
    # 1. 把所有珠宝字符放进集合（哈希表），相当于做了一次“建表”
    jewel_set = set(jewels)          # O(m) 的时间，m = len(jewels)

    count = 0                         # 记录是珠宝的石头数量
    # 2. 逐颗检查石头，利用集合的 O(1) 查找特性
    for stone in stones:              # O(n) 的时间，n = len(stones)
        if stone in jewel_set:        # O(1) 的成员判定
            count += 1                # 累计
    return count
```

#### 复杂度  
- **时间复杂度**：`O(m + n)`。  
  - 大白话：先把珠宝表里最多 50 个字符放进集合（最多 50 次操作），再检查最多 50 颗石头（最多 50 次操作），总共不超过 100 次，远比 2500 次的暴力法快。  
- **空间复杂度**：`O(m)`。  
  - 需要额外的集合来存珠宝字符，最多存 50 个字符，属于线性空间（随珠宝种类数增长而增长）。

---  

## 心得  

- **核心技巧**：利用哈希表（`set`）实现**常数时间的成员判定**。  
- **适用的题型**  
  1. “两个数组交集” 类似的，需要快速判断元素是否在另一个集合中。  
  2. “判断字符串中是否包含指定字符” 如 “字符串中的第一个唯一字符”。  
  3. “字母异位词分组” 等需要把元素映射到唯一标识的场景。  
- **一句话总结**：**把“遍历比较”改成“哈希查表”，一次 O(1) 就能判断是否匹配**。  

## 反思  

- **第一反应**：直接想到两层循环逐个比较，最容易实现但效率低。  
- **最容易踩的坑**  
  - 忘记把 `jewels` 中的字符放进集合，导致每次判断仍然是线性搜索。  
  - 忽略字符大小写敏感，`'a'` 与 `'A'` 必须被视作不同。  
  - 输入为空字符串的极端情况（虽然题目保证长度 ≥ 1），代码仍应稳健。  
- **下次遇到同类题**：第一步先思考“是否可以把一个集合转成哈希表”，如果可以，就直接用 O(1) 的成员查询来避免嵌套循环。