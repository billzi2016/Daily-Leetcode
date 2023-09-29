# #2418. 人员排序 / Sort the People

> 难度：简单 · 标签：Array、Hash Table、String、Sorting · [LeetCode 链接](https://leetcode.com/problems/sort-the-people/)

---

## 题目（英文原版）

**Description**

You are given an array of strings names, and an array heights that consists of distinct positive integers. Both arrays are of length n.
For each index i, names[i] and heights[i] denote the name and height of the ith person.
Return names sorted in descending order by the people's heights.

**Examples**

**Example 1:**

```
Input: names = ["Mary","John","Emma"], heights = [180,165,170]
Output: ["Mary","Emma","John"]
Explanation: Mary is the tallest, followed by Emma and John.
```

**Example 2:**

```
Input: names = ["Alice","Bob","Bob"], heights = [155,185,150]
Output: ["Bob","Alice","Bob"]
Explanation: The first Bob is the tallest, followed by Alice and the second Bob.
```

**Constraints**

- n == names.length == heights.length
- 1 <= n <= 103
- 1 <= names[i].length <= 20
- 1 <= heights[i] <= 105
- names[i] consists of lower and upper case English letters.
- All the values of heights are distinct.

---

## 题目（中文翻译）

给定一个字符串数组 `names` 和一个整数数组 `heights`，其中 `heights` 由互不相同的正整数构成。两个数组的长度均为 `n`。  
对于每个下标 `i`，`names[i]` 与 `heights[i]` 分别表示第 `i` 个人的姓名和身高。  
返回按身高 **降序** 排列后的 `names`。

**示例 1**  
**输入**: `names = ["Mary","John","Emma"], heights = [180,165,170]`  
**输出**: `["Mary","Emma","John"]`  
**解释**: Mary 最高，其次是 Emma，最后是 John。

**示例 2**  
**输入**: `names = ["Alice","Bob","Bob"], heights = [155,185,150]`  
**输出**: `["Bob","Alice","Bob"]`  
**解释**: 第一个 Bob 最高，其次是 Alice，最后是第二个 Bob。

**约束条件**  
- `n == names.length == heights.length`  
- `1 <= n <= 10^3`  
- `1 <= names[i].length <= 20`  
- `1 <= heights[i] <= 10^5`  
- `names[i]` 仅由大小写英文字母组成。  
- 所有 `heights` 的取值互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一次一次挑最高的**，把它放到结果的前面；然后在剩下的人里再挑最高的，放到第二位……  
这和我们在超市挑最贵商品的过程很像：先找最贵的，记下来；再在剩下的商品里找次贵的，依次类推。

实现时可以把 `names` 和 `heights` 看成两条平行的“记录”。  
我们遍历 `heights`，每一次都记录当前未处理区间的最大值所在的下标 `max_idx`，然后把 `max_idx` 对应的 `name` 与 `height` 与当前下标 `i` 交换。  
交换后，第 `i` 位已经确定是第 `i` 高的人，接下来只需要在 `[i+1, n)` 区间继续寻找。

> **为什么正确**  
> 每一次循环都把未排序区间的最高身高放到最前面，等所有循环结束后，所有人已经按照身高从高到低排好序。  
> 这正是**选择排序**（Selection Sort）的核心思想，虽然不是最快的，但非常直观。

#### 代码（Python）

```python
def sortPeople(names, heights):
    # 把 names 和 heights 看成两条平行的记录
    n = len(names)
    # 将两个列表都转成可变的 list（如果本来就是 list 也没关系）
    names = list(names)
    heights = list(heights)

    # 选择排序：每轮找出未排序区间的最大值
    for i in range(n):
        max_idx = i                     # 假设当前 i 位置就是最大值所在
        for j in range(i + 1, n):       # 在 i 之后的区间里找更大的
            if heights[j] > heights[max_idx]:
                max_idx = j

        # 把最大值换到当前位置 i
        heights[i], heights[max_idx] = heights[max_idx], heights[i]
        names[i],   names[max_idx]   = names[max_idx],   names[i]

    return names
```

#### 复杂度

- **时间复杂度：**`O(n²)`  
  这里的 `n` 是人数。外层循环 `n` 次，内层寻找最大值平均要比较 `n/2` 次，整体大约是 `n × n/2 ≈ n²`。  
  用大白话说，就是“人数翻倍，工作量会增加四倍”，所以当 `n` 很大时会变得很慢。

- **空间复杂度：**`O(1)`（原地交换）  
  我们只用了几个额外的变量 `i、j、max_idx`，不随输入规模增长而增加内存。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要遍历未排序区间寻找最大值**，导致 `O(n²)`。  
如果我们一次性把每个人的「名字」和「身高」配对起来，然后利用 **排序算法**（Python 内置的 Timsort）直接把配对好的列表按身高降序排好序，就能把工作交给已经非常高效的库函数完成。

关键点在于：

1. **配对（zip）**  
   把两个列表对应位置的元素组合成元组 `(height, name)`。  
   这一步像是把「身高」这张卡片和「名字」这张卡片贴在一起，方便一起搬运。

2. **排序（sorted）**  
   `sorted` 默认是升序，我们只需要把排序键设为身高并指定 `reverse=True`（降序），就能一次得到从高到低的顺序。  
   Python 的排序使用的是 **Timsort**，在最坏情况下是 `O(n log n)`，在实际数据中往往更快。

3. **提取名字**  
   排好序后，只需要把每个元组的名字取出来，组成最终的答案。

> **为什么正确**  
> 排序算法保证所有元素按照指定的键（这里是身高）从大到小排列。因为身高是 **互不相同**（题目已说明），排序结果唯一，对应的名字顺序就是我们要求的答案。

#### 代码（Python）

```python
def sortPeople(names, heights):
    """
    将名字和身高配对后按身高降序排序，返回排序后的名字列表。
    """
    # 1. 配对：[(180, "Mary"), (165, "John"), (170, "Emma")]
    paired = list(zip(heights, names))

    # 2. 排序：按照第 0 位（height）降序
    #    sorted 返回新列表，不会修改原来的 paired
    paired.sort(key=lambda x: x[0], reverse=True)   # O(n log n)

    # 3. 提取名字：["Mary", "Emma", "John"]
    sorted_names = [name for _, name in paired]

    return sorted_names
```

#### 复杂度

- **时间复杂度：**`O(n log n)`  
  这里的 `log n` 是对数，意味着当人数翻倍，工作量只会增加大约 `log₂(2) = 1` 倍左右（实际上是稍微多一点），远比 `O(n²)` 要快。  
  与暴力解相比，**效率提升了数量级**。

- **空间复杂度：**`O(n)`  
  我们额外创建了一个 `paired` 列表，里面存了 `n` 个元组，每个元组包含一个整数和一个字符串引用。  
  因为需要把配对信息保存下来，空间随输入规模线性增长。

---

## 心得

- **核心技巧**：把多个相关属性配对（`zip`），然后使用**自定义键的排序**一次性完成排序任务。  
- **适用的题型**  
  1. 根据分数、年龄、价格等数值对对象进行排序（如 “按成绩从高到低输出学生名单”）。  
  2. 多属性排序，需要先把属性组合起来再排序（如 “先按年龄升序、年龄相同再按名字字典序”）。  
- **解题钥匙**：**配对 + 排序**，把“要一起移动的东西”先粘在一起，再交给高效的排序算法。

---

## 反思

- **第一反应**：先想到“找最高的、换位置”，也就是选择排序的思路。  
- **最容易踩的坑**  
  - 忘记 **同步交换** 两个列表，导致名字和身高对应错位。  
  - 对 `heights` 进行排序后忘记把对应的 `names` 也一起搬运。  
  - 忽略了身高是**互不相同**的，若有相同身高时需要考虑稳定性。  
- **下次遇到同类题**，第一步应该想到：**把所有属性配对（或打包）成一个整体**，再利用 **排序** 或 **堆** 等数据结构一次性解决。这样既简洁又高效。