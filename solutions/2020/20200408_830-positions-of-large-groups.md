# #830. 大组的位置 / Positions of Large Groups

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/positions-of-large-groups/)

---

## 题目（英文原版）

**Description**

In a string s of lowercase letters, these letters form consecutive groups of the same character.
For example, a string like s = "abbxxxxzyy" has the groups "a", "bb", "xxxx", "z", and "yy".
A group is identified by an interval [start, end], where start and end denote the start and end indices (inclusive) of the group. In the above example, "xxxx" has the interval [3,6].
A group is considered large if it has 3 or more characters.
Return the intervals of every large group sorted in increasing order by start index.

**Examples**

**Example 1:**

```
Input: s = "abbxxxxzzy"
Output: [[3,6]]
Explanation: "xxxx" is the only large group with start index 3 and end index 6.
```

**Example 2:**

```
Input: s = "abc"
Output: []
Explanation: We have groups "a", "b", and "c", none of which are large groups.
```

**Example 3:**

```
Input: s = "abcdddeeeeaabbbcd"
Output: [[3,5],[6,9],[12,14]]
Explanation: The large groups are "ddd", "eeee", and "bbb".
```

**Constraints**

- 1 <= s.length <= 1000
- s contains lowercase English letters only.

---

## 题目（中文翻译）

在仅包含小写字母的字符串 `s` 中，连续相同字符会形成一组（group）。
例如，字符串 `s = "abbxxxxzyy"` 的组有 `"a"`、`"bb"`、`"xxxx"`、`"z"` 和 `"yy"`。
每一组可以用区间 `[start, end]` 来标识，其中 `start` 和 `end` 分别表示该组的起始下标和结束下标（均为闭区间）。在上面的例子中，`"xxxx"` 对应的区间是 `[3,6]`。
若一个组的字符数量不少于 3，则称其为**大组**（large group）。
返回所有大组的区间，按 `start` 下标升序排列。

**示例 1**  
**输入**: `s = "abbxxxxzzy"`  
**输出**: `[[3,6]]`  
**解释**: `"xxxx"` 是唯一的大组，起始下标为 3，结束下标为 6。

**示例 2**  
**输入**: `s = "abc"`  
**输出**: `[]`  
**解释**: 我们得到的组有 `"a"`、`"b"`、`"c"`，它们都不是大组。

**示例 3**  
**输入**: `s = "abcdddeeeeaabbbcd"`  
**输出**: `[[3,5],[6,9],[12,14]]`  
**解释**: 大组分别是 `"ddd"`、`"eeee"` 和 `"bbb"`。

**约束条件**  
- `1 <= s.length <= 1000`  
- `s` 仅包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把 **所有可能的子串** 都枚举一遍，检查它们是否满足“同一字符且长度 ≥ 3”。  
- **枚举方式**：用两层循环，外层 `start` 表示子串的左端点，内层 `end` 表示右端点（`end ≥ start`）。  
- **判断子串**：遍历 `s[start…end]`，如果每个字符都和 `s[start]` 相同且 `end‑start+1 ≥ 3`，就把 `[start, end]` 加入答案。  

可以把 “同一字符” 想象成查字典：我们先拿到“词”（第一个字符），然后把后面的每一页都对照这词，看是不是同一个。如果全都匹配，就算找到了一个“大组”。  

这个方法**一定能得到正确答案**，因为我们把所有可能的区间都检查了一遍，漏掉的情况不存在。  

**复杂度分析**（大白话）  
- **时间**：外层 `n` 次，内层最多 `n` 次，每次还要遍历子串检查字符相等，最坏情况是 `O(n³)`，但我们可以在检查时提前退出（只要出现不同字符就停），实际仍然是 **二次** 的量级 `O(n²)`，相当于“把每个人都和每个人握手一次”。  
- **空间**：只用了常数个临时变量，除去返回的结果外，额外空间是 `O(1)`，就像只在桌子上放了几支笔。  

#### 代码（Python）  
```python
def largeGroupPositions_brute(s: str):
    n = len(s)
    res = []                         # 用来存放答案的列表
    for start in range(n):           # 第一个循环：左端点
        for end in range(start, n):  # 第二个循环：右端点
            # 只关心长度至少 3 的区间
            if end - start + 1 < 3:
                continue
            # 检查区间内字符是否全部相同
            same = True
            for k in range(start + 1, end + 1):
                if s[k] != s[start]:  # 一旦发现不同，就不是大组
                    same = False
                    break
            if same:                  # 全部相同且长度≥3，记下来
                res.append([start, end])
    return res
```

#### 复杂度  
- **时间复杂度**：`O(n²)`（最坏情况下两层循环遍历 n² 次，内部检查在发现不相同后会提前退出）。  
  > *直观解释*：如果把字符串想成 1000 个人排成一列，暴力解要把每个人和后面所有人分别比较一次，工作量大约是 1000 × 1000 ≈ 100 万次。  
- **空间复杂度**：`O(1)`（只用了几个计数变量），不随输入规模增长。  

---  

### 2. 最优解  

#### 思路  
暴力解的**瓶颈**在于大量的重复比较：同一个字符会被检查很多次。  
其实我们只需要 **一次遍历**，把相同字符的连续段直接“捆绑”起来，记录下每段的起始下标 `start`，当字符变化或遍历结束时，检查这段的长度是否 ≥ 3。  

这就是 **双指针 / 滑动窗口** 的典型思路：  
1. `start` 保存当前连续相同字符段的起始位置。  
2. 用 `i`（或 `end`）从左到右扫描字符串。  
3. 当 `i` 超出当前段（即 `s[i] != s[start]`）或已经到达字符串末尾时，**结束当前段**。  
4. 计算段长 `i - start`（注意这里 `i` 已经指向了第一个不同的字符或 `n`），如果段长 ≥ 3，就把 `[start, i‑1]` 加入答案。  
5. 把 `start` 移到 `i`，继续下一段的检测。  

类比：把字符串想成一条铁路，火车（相同字符）会连续驶过若干站点。我们只需要在火车离站（字符改变）时，记下这趟火车的起点和终点。如果这趟火车跑了 3 站以上，就算是“大组”。  

#### 代码（Python）  
```python
def largeGroupPositions(s: str):
    """
    返回所有长度不少于 3 的连续相同字符子串的起止下标。
    采用一次遍历的线性时间解法。
    """
    n = len(s)
    res = []
    start = 0                     # 当前大组的起始下标

    for i in range(n):
        # 当遍历到字符串末尾或字符发生变化时，结束当前段
        if i == n - 1 or s[i] != s[i + 1]:
            length = i - start + 1          # 当前段的长度（包含 i）
            if length >= 3:                 # 满足“大组”条件
                res.append([start, i])      # 记录区间
            start = i + 1                   # 下一段从 i+1 开始

    return res
```

> **关键注释解释**  
> - `i == n - 1` 用来处理最后一个字符，因为它后面没有字符可比较，需要在循环结束时也检查一次。  
> - `length = i - start + 1` 计算的是 **闭区间** 长度，`+1` 表示把起始位置也算进去。  

#### 复杂度  
- **时间复杂度**：`O(n)`，只遍历了一遍字符串。  
  > *直观解释*：如果把 1000 个人排成一列，我们只让每个人说一次自己的名字，工作量只有 1000 次，比暴力的 1 000 000 次要省很多。  
- **空间复杂度**：`O(1)`（除答案外，只用了几个整数变量），不随 `n` 增长。  

---  

## 心得  

- **核心技巧**：一次遍历 + 双指针（记录段起点），也叫 **滑动窗口**。  
- **适用题型**：  
  1. “找出所有满足长度条件的连续子串”——如 **1658. 允许键盘输入的最小字符数**（类似的连续计数）。  
  2. “统计连续相同元素的出现次数”——如 **696. 计数二进制子串**（需要统计相邻相同块的长度）。  
  3. “最长连续递增/递减子序列”——也可以用类似的段划分思路。  
- **一句话总结**：一次遍历，遇到字符变化就“关门”，检查当前段是否足够长。  

---  

## 反思  

- **第一反应**：看到“连续相同字符”立刻想到“把相同的字符捆在一起”。  
- **最容易踩的坑**：  
  - 忘记在遍历结束后（字符串最后一个字符）也要检查一次，否则最后一段可能漏掉。  
  - 边界条件写错，如 `i == n - 1` 与 `s[i] != s[i+1]` 的判断顺序会导致索引越界。  
- **下次遇到同类题**：第一步先 **确定划分段的标准**（字符相同、递增、递减等），然后 **用一个指针记录段起点**，在“段结束”时统一处理。这样就能把 O(n²) 的暴力直接压缩到 O(n)。