# #1528. 字符串重排 / Shuffle String

> 难度：简单 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/shuffle-string/)

---

## 题目（英文原版）

**Description**

You are given a string s and an integer array indices of the same length. The string s will be shuffled such that the character at the ith position moves to indices[i] in the shuffled string.
Return the shuffled string.

**Examples**

**Example 1:**

```
Input: s = "codeleet", indices = [4,5,6,7,0,2,1,3]
Output: "leetcode"
Explanation: As shown, "codeleet" becomes "leetcode" after shuffling.
```

**Example 2:**

```
Input: s = "abc", indices = [0,1,2]
Output: "abc"
Explanation: After shuffling, each character remains in its position.
```

**Constraints**

- s.length == indices.length == n
- 1 <= n <= 100
- s consists of only lowercase English letters.
- 0 <= indices[i] < n
- All values of indices are unique.

---

## 题目（中文翻译）

你得到一个字符串 `s` 和一个整数数组 `indices`，二者长度相同。字符串 `s` 将被重新排列，使得原字符在第 `i` 位的字符移动到重新排列后字符串的 `indices[i]` 位置。  
返回重新排列后的字符串。

**示例 1**  

**示例 2**  

**约束条件**  

### 示例

**示例 1**  
```
Input: s = "codeleet", indices = [4,5,6,7,0,2,1,3]
Output: "leetcode"
Explanation: 如图所示，经过重排后 "codeleet" 变成了 "leetcode"。
```

**示例 2**  
```
Input: s = "abc", indices = [0,1,2]
Output: "abc"
Explanation: 重排后，每个字符仍然保持在原来的位置。
```

### 约束条件
- `s.length == indices.length == n`
- `1 <= n <= 100`
- `s` 仅由小写英文字母组成。
- `0 <= indices[i] < n`
- `indices` 中的所有值互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**对每一个字符**，都去遍历 `indices` 找到它应该去的位置，然后把字符放进去。  
可以把 `indices` 想象成一本 **“地址簿”**，每一页（下标）写着对应字符要搬到的目标位置。  
暴力做法就是：  
1. 创建一个长度为 `n`（`n = len(s)`）的空列表 `res`，用 `''` 填充。  
2. 对每个下标 `i`（代表原字符串 `s` 中的第 `i` 个字符），  
   - 再遍历一遍 `indices`，找到 `indices[j] == i`（即原字符 `s[i]` 要搬到的位置是 `j`）。  
   - 把 `s[i]` 放到 `res[j]`。  

这样每个字符都要遍历一次 `indices`，所以会出现 **两层循环**。

> **为什么正确？**  
> 因为题目保证 `indices` 中的每个值都是唯一且在 `[0, n-1]` 范围内，遍历一次就一定能找到唯一的目标位置，所有字符按要求放好后，`res` 就是洗牌后的字符串。

#### 代码（Python）
```python
def restoreString_brute(s: str, indices: list[int]) -> str:
    n = len(s)
    # 先准备一个长度为 n、全部是空字符的列表，等会儿会逐个填充
    res = [''] * n

    # 对原字符串的每个字符 i
    for i in range(n):
        # 在 indices 中找出目标位置 j，使得 indices[j] == i
        for j in range(n):
            if indices[j] == i:          # 找到了！j 就是该字符应该去的下标
                res[j] = s[i]            # 把字符放进去
                break                    # 一个字符只会出现一次，找到后立即退出内层循环

    # 列表转成字符串返回
    return ''.join(res)
```

#### 复杂度
- **时间复杂度：O(n²)** — `n` 是字符串长度。外层遍历 `n` 次，内层最坏也要遍历 `n` 次，相当于“做 n × n 次工作”。  
  用生活中的比喻：如果有 10 本书要放到对应的 10 个书架上，暴力方法相当于每放一本书都要把所有书架检查一遍，检查次数是 10×10=100 次。
- **空间复杂度：O(n)** — 需要额外的列表 `res` 来保存结果，长度为 `n`。

---

### 2. 最优解

#### 思路  
从暴力解可以看到，**慢的地方在于内层的遍历**：我们每次都要在 `indices` 中找目标位置。  
其实 `indices` 本身已经告诉我们每个字符的目标下标——`indices[i]` 就是字符 `s[i]` 要搬到的位置。  
所以我们可以 **一次遍历** 完成所有字符的放置：

1. 创建长度为 `n` 的空列表 `res`（同上）。  
2. 直接遍历 `i = 0 … n-1`，把 `s[i]` 放到 `res[indices[i]]`。  

这一步相当于把 “地址簿” 的信息直接读出来，用 **下标直接定位**，不再需要搜索。

> **核心概念——数组的直接下标访问**  
> 在 Python（以及大多数语言）里，列表（数组）可以用下标 O(1) 时间直接读取或写入元素。把 `indices[i]` 看成 **“直接的门牌号”**，我们走到门口就能直接进屋，不用再找。

#### 代码（Python）
```python
def restoreString_optimal(s: str, indices: list[int]) -> str:
    n = len(s)
    # 同样准备一个空的结果列表
    res = [''] * n

    # 只需要一次遍历：把字符直接放到它对应的下标位置
    for i in range(n):
        target = indices[i]   # 目标下标
        res[target] = s[i]    # 直接放进去

    # 合并成字符串返回
    return ''.join(res)
```

#### 复杂度
- **时间复杂度：O(n)** — 只遍历一次 `s`（或 `indices`），每次操作都是 O(1)。相当于把 10 本书一次性直接搬到对应的书架，只需要 10 次搬运，而不是 100 次。
- **空间复杂度：O(n)** — 仍然需要一个同样长度的列表来存放结果。

---

## 心得

- **核心技巧**：利用数组（列表）下标的直接访问特性，省去不必要的搜索。  
- **适用题型**：  
  1. 根据下标重排数组/字符串（如 “按照给定顺序重排数组”）。  
  2. “原地置换” 类题目（如 “根据映射数组恢复原数组”）。  
- **解题钥匙**：**“如果下标已经告诉你目标位置，就直接把元素塞进去”**。

## 反思

- **第一反应**：看到 “indices[i] 表示字符移动到的位置”，本能会想遍历一次把字符放进去——其实这已经是最优解。  
- **最容易踩的坑**：  
  - 忘记初始化结果列表的长度，导致 IndexError。  
  - 直接在原字符串上修改（字符串不可变），必须使用可变的列表来存放中间结果。  
- **下次思考步骤**：  
  1. **确认下标或映射关系** 已经给出？  
  2. **是否可以一次遍历直接写入**（利用 O(1) 的下标访问）？  
  3. 若不能直接写入，考虑是否需要额外的数据结构（哈希表、额外数组）来保存映射。