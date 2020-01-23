# #744. 找到大于目标字符的最小字母 / Find Smallest Letter Greater Than Target

> 难度：简单 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/find-smallest-letter-greater-than-target/)

---

## 题目（英文原版）

**Description**

You are given an array of characters letters that is sorted in non-decreasing order, and a character target. There are at least two different characters in letters.
Return the smallest character in letters that is lexicographically greater than target. If such a character does not exist, return the first character in letters.

**Examples**

**Example 1:**

```
Input: letters = ["c","f","j"], target = "a"
Output: "c"
Explanation: The smallest character that is lexicographically greater than 'a' in letters is 'c'.
```

**Example 2:**

```
Input: letters = ["c","f","j"], target = "c"
Output: "f"
Explanation: The smallest character that is lexicographically greater than 'c' in letters is 'f'.
```

**Example 3:**

```
Input: letters = ["x","x","y","y"], target = "z"
Output: "x"
Explanation: There are no characters in letters that is lexicographically greater than 'z' so we return letters[0].
```

**Constraints**

- 2 <= letters.length <= 104
- letters[i] is a lowercase English letter.
- letters is sorted in non-decreasing order.
- letters contains at least two different characters.
- target is a lowercase English letter.

---

## 题目（中文翻译）

给定一个字符数组 `letters`，该数组按非递减顺序（non‑decreasing order）排序，并且数组中至少包含两个不同的字符。同时给定一个字符 `target`。  
返回 `letters` 中字典序（lexicographically）**大于** `target` 的最小字符。如果不存在这样的字符，则返回 `letters` 中的第一个字符。

## 示例

### 示例 1
**输入**: `letters = ["c","f","j"]`, `target = "a"`  
**输出**: `"c"`  
**解释**: 在 `letters` 中字典序大于 `'a'` 的最小字符是 `'c'`。

### 示例 2
**输入**: `letters = ["c","f","j"]`, `target = "c"`  
**输出**: `"f"`  
**解释**: 在 `letters` 中字典序大于 `'c'` 的最小字符是 `'f'`。

### 示例 3
**输入**: `letters = ["x","x","y","y"]`, `target = "z"`  
**输出**: `"x"`  
**解释**: `letters` 中不存在字典序大于 `'z'` 的字符，因此返回 `letters[0]`。

## 约束条件
- `2 <= letters.length <= 10^4`
- `letters[i]` 为小写英文字母。
- `letters` 按非递减顺序排序。
- `letters` 至少包含两个不同的字符。
- `target` 为小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是把 `letters` 里每个字符都拿出来和 `target` 比较，找出所有**比 target 大**的字符，然后在这些字符中挑最小的那个。  
- **使用的数据结构**：只需要遍历原数组，用一个变量 `candidate` 暂存当前找到的“最小的更大字符”。可以把它想象成在超市里挑商品：我们把每个商品的价格和目标价格比较，只保留比目标贵且最便宜的那件。  
- **为什么正确**：因为我们把所有符合“比 target 大”的字符都检查了一遍，最终留下的就是字典序最靠前的那一个。若遍历完后没有任何字符比 target 大，说明所有字符都不符合条件，此时按照题意返回数组的第一个字符即可。  

#### 代码（Python）

```python
def nextGreatestLetter_brute(letters, target):
    """
    暴力解法：线性扫描
    :param letters: 已排好序的字符列表
    :param target: 目标字符
    :return: 第一个字典序大于 target 的字符，若不存在返回 letters[0]
    """
    candidate = None                     # 用来记录当前找到的最小更大字符
    for ch in letters:                   # 逐个遍历
        if ch > target:                  # 只关注比 target 大的字符
            if candidate is None or ch < candidate:
                candidate = ch          # 更新为更小的更大字符
    # 如果遍历结束仍未找到，则说明所有字符都 ≤ target
    return candidate if candidate is not None else letters[0]
```

#### 复杂度  

- **时间复杂度**：`O(n)`（这里的 `n` 是 `letters` 的长度）。我们要把数组里的每个元素都检查一遍，就像走完整条街才能找到最合适的店铺。  
- **空间复杂度**：`O(1)`，只用了常数个额外变量（`candidate`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

在暴力解里，**瓶颈**是我们必须把所有字符都看一遍。可是题目已经告诉我们 `letters` 是**已排序**的（非递减），这正好可以利用**二分查找**把搜索范围快速缩小。  

二分查找的核心思想是：  
1. 取数组中间位置 `mid` 的字符 `mid_char`。  
2. 如果 `mid_char` **不大于** `target`（即 `mid_char <= target`），说明**左边**的所有字符也不可能是答案，因为它们更小或相等。于是把搜索区间左移到 `mid + 1`。  
3. 否则（`mid_char > target`），说明 `mid_char` 有可能是答案，但我们仍要检查**更左边**是否还有更小的符合条件的字符，于是把右边界收紧到 `mid`。  

循环结束时，左指针 `left` 会指向**第一个**大于 `target` 的位置。如果整个数组都没有比 `target` 大的字符，`left` 会等于数组长度，此时按照题意返回 `letters[0]`（循环的“环形”特性）。  

下面用生活化的类比帮助理解：  
想象你在一本按字母顺序排好的电话簿里找第一个名字比 “Mike” 更靠后的联系人。你不会从头翻到尾，而是先打开中间的页面，根据页面上名字和 “Mike” 的比较决定往前翻还是往后翻，快速锁定目标位置。二分查找就是这种“折半”策略。

#### 代码（Python）

```python
def nextGreatestLetter_binary(letters, target):
    """
    最优解：二分查找
    :param letters: 已排好序的字符列表
    :param target: 目标字符
    :return: 第一个字典序大于 target 的字符，若不存在返回 letters[0]
    """
    left, right = 0, len(letters) - 1   # 初始化搜索区间
    while left <= right:
        mid = (left + right) // 2       # 取中点
        if letters[mid] <= target:      # 中点字符不大于 target
            left = mid + 1              # 目标在右侧，左边界右移
        else:                           # 中点字符大于 target
            right = mid - 1             # 可能还有更左的符合条件，右边界左移

    # 循环结束时，left 指向第一个大于 target 的位置
    # 若 left 超出数组范围，说明不存在更大的字符，返回首字符实现环形
    return letters[left % len(letters)]
```

#### 复杂度  

- **时间复杂度**：`O(log n)`，因为每一次循环都把搜索区间大小**减半**，类似每次把街道长度缩短一半，几步就能定位到答案。相比线性扫描的 `O(n)`，在 `n` 很大时速度提升明显。  
- **空间复杂度**：`O(1)`，只用了几个整数指针 `left、right、mid`，不随输入规模增加。

---

## 心得

- **核心技巧**：利用**数组已排序**的特性，使用**二分查找**在对数时间内定位第一个大于目标的元素。  
- **适用的题型**：  
  1. 在排好序的数组中查找**第一个满足某个条件**的元素（如 “第一个大于/小于目标”）。  
  2. “环形”查找类问题，如 LeetCode 744（Find Smallest Letter Greater Than Target）本身以及 33（Search in Rotated Sorted Array）等。  
- **一句话总结解题钥匙**：**“有序 → 折半 → 第一个满足”**。

## 反思

- **第一反应**：看到“已排序”，立刻想到二分查找；如果忽视了排序，往往会直接写暴力循环。  
- **最容易踩的坑**：  
  - 忘记处理**环形**情况——当所有字符都不大于 `target` 时，需要返回 `letters[0]`。使用 `left % len(letters)` 能简洁地处理。  
  - 边界条件 `left` 可能等于数组长度，需要取模或单独判断。  
- **下次遇到同类题的第一步**：先确认数组是否有序，若有序就立刻在脑中画出**二分查找的搜索区间**，确定“左闭右闭”还是“左闭右开”以及返回值的取模处理。