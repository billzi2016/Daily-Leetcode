# #2515. **环形数组中目标字符串的最短距离** / Shortest Distance to Target String in a Circular Array

> 难度：简单 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/shortest-distance-to-target-string-in-a-circular-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed circular string array words and a string target. A circular array means that the array's end connects to the array's beginning.
Starting from startIndex, you can move to either the next word or the previous word with 1 step at a time.
Return the shortest distance needed to reach the string target. If the string target does not exist in words, return -1.

**Examples**

**Example 1:**

```
Input: words = ["hello","i","am","leetcode","hello"], target = "hello", startIndex = 1
Output: 1
Explanation: We start from index 1 and can reach "hello" by
- moving 3 units to the right to reach index 4.
- moving 2 units to the left to reach index 4.
- moving 4 units to the right to reach index 0.
- moving 1 unit to the left to reach index 0.
The shortest distance to reach "hello" is 1.
```

**Example 2:**

```
Input: words = ["a","b","leetcode"], target = "leetcode", startIndex = 0
Output: 1
Explanation: We start from index 0 and can reach "leetcode" by
- moving 2 units to the right to reach index 3.
- moving 1 unit to the left to reach index 3.
The shortest distance to reach "leetcode" is 1.
```

**Example 3:**

```
Input: words = ["i","eat","leetcode"], target = "ate", startIndex = 0
Output: -1
Explanation: Since "ate" does not exist in words, we return -1.
```

**Constraints**

- 1 <= words.length <= 100
- 1 <= words[i].length <= 100
- words[i] and target consist of only lowercase English letters.
- 0 <= startIndex < words.length

---

## 题目（中文翻译）

给定一个下标从 0 开始的环形字符串数组 `words`（circular array）和一个字符串 `target`。环形数组表示数组的末尾与开头相连。

从 `startIndex` 开始，每次可以向左（前一个）或向右（下一个）移动 1 步。返回到达字符串 `target` 所需的最短距离。如果 `target` 不存在于 `words` 中，返回 `-1`。

**示例 1**  
输入: `words = ["hello","i","am","leetcode","hello"]`, `target = "hello"`, `startIndex = 1`  
输出: `1`  
解释: 我们从下标 1 开始，可以通过以下方式到达 `"hello"`：  
- 向右移动 3 步到达下标 4。  
- 向左移动 2 步到达下标 4。  
- 向右移动 4 步到达下标 0。  
- 向左移动 1 步到达下标 0。  
最短的距离是 1。

**示例 2**  
输入: `words = ["a","b","leetcode"]`, `target = "leetcode"`, `startIndex = 0`  
输出: `1`  
解释: 我们从下标 0 开始，可以通过以下方式到达 `"leetcode"`：  
- 向右移动 2 步到达下标 2。  
- 向左移动 1 步到达下标 2。  
最短的距离是 1。

**示例 3**  
输入: `words = ["i","eat","leetcode"]`, `target = "ate"`, `startIndex = 0`  
输出: `-1`  
解释: 由于 `"ate"` 不在 `words` 中，返回 `-1`。

**约束条件**  
- `1 <= words.length <= 100`  
- `1 <= words[i].length <= 100`  
- `words[i]` 和 `target` 仅由小写英文字母组成。  
- `0 <= startIndex < words.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. **遍历整个数组**，找到所有等于 `target` 的下标 `i`。  
2. 对每个 `i` 计算从 `startIndex` 到 `i` 的最短步数。  
   - 直接走的距离是 `abs(i - startIndex)`（左走或右走的直线距离）。  
   - 因为数组是环形的，还可以「绕过去」——即走 `len(words) - abs(i - startIndex)` 步。  
   - 两者取最小值就是从 `startIndex` 到 `i` 的最短距离。  

> **类比**：把环形数组想成一条圆形跑道，跑道上有若干个标记点（下标）。从起点出发，你可以顺时针跑也可以逆时针跑，最短的跑法就是两条路径中更短的一条。

只要把所有目标下标的距离算出来，取最小值即可。如果数组里根本没有 `target`，直接返回 `-1`。

#### 代码（Python）

```python
def shortestDistance(words, target, startIndex):
    n = len(words)                     # 环形数组的长度
    min_dist = float('inf')            # 用来保存最小距离，初始为正无穷

    for i, w in enumerate(words):      # 逐个检查每个单词
        if w == target:                # 只关心等于 target 的位置
            # 直接走的步数
            direct = abs(i - startIndex)
            # 绕环走的步数 = 环的总长 - 直接走的步数
            wrap = n - direct
            # 这两个方向取更小的那个
            cur_dist = min(direct, wrap)
            # 更新全局最小值
            min_dist = min(min_dist, cur_dist)

    # 如果 min_dist 没被更新过，说明数组里没有 target
    return -1 if min_dist == float('inf') else min_dist
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历了一遍数组，`n` 为 `words` 的长度。即使每个元素都要算一次距离，工作量仍然是线性的。  
  > 大白话：如果数组有 1000 个单词，最多检查 1000 次，算起来很快。

- **空间复杂度**：`O(1)`  
  只用了几个额外的变量（`n、min_dist、direct、wrap`），与输入规模无关。

---

### 2. 最优解

#### 思路  

上面的「暴力」解其实已经是最优的 `O(n)` 解法，因为我们必须至少看一遍数组才能确认 `target` 是否存在。  
不过我们可以把代码写得更「直接」一点：

1. **先收集所有 target 出现的下标**（一次遍历）。  
2. **一次遍历这些下标**，用同样的公式 `min(|i - start|, n - |i - start|)` 计算最小距离。  

这种写法把「找下标」和「算距离」分成两步，思路更清晰，也方便以后在需要多次查询同一数组时复用下标列表（比如多次询问不同的 `startIndex`）。

> **类比**：先把所有目标点标记在纸上（下标列表），然后从起点出发，用尺子量最近的那段距离。

#### 代码（Python）

```python
def shortestDistance(words, target, startIndex):
    n = len(words)

    # 第一步：收集所有 target 出现的位置
    target_pos = [i for i, w in enumerate(words) if w == target]

    # 如果列表为空，说明根本没有 target
    if not target_pos:
        return -1

    # 第二步：在这些位置中找最小的环形距离
    min_dist = n   # 最多不会超过环的长度
    for pos in target_pos:
        direct = abs(pos - startIndex)   # 直接走的步数
        wrap = n - direct                # 绕环走的步数
        min_dist = min(min_dist, direct, wrap)

    return min_dist
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  仍然只遍历了一遍数组（收集下标）和一次遍历目标下标列表（最坏情况下列表长度仍然是 `n`），总工作量与 `n` 成线性关系。  
  与暴力解相比，常数因子略有不同，但数量级相同。

- **空间复杂度**：`O(k)`，`k` 为 `target` 在数组中出现的次数。  
  需要额外保存这些下标。如果 `target` 出现很多，最坏会是 `O(n)`；如果只出现一次或根本不出现，则只占很少空间。  
  与暴力解的 `O(1)` 相比，这里用了额外的列表，但在本题约束（`n ≤ 100`）下完全可以接受。

---

## 心得

- **核心技巧**：**环形距离的计算**——`min(|i - j|, n - |i - j|)`。只要把数组看成一个圆环，顺时针和逆时针两条路中取更短的那条即可。  
- **适用题型**：  
  1. 环形数组或环形链表的最近距离问题（如 LeetCode 2059 – Minimum Operations to Make Array Empty）。  
  2. “转盘”类题目，需要在环上寻找最近的目标（如旋转密码锁、环形灯泡等）。  
- **解题钥匙**：**把环形转成“直线 + 绕行”两种情况取最小**。

## 反思

- **第一反应**：看到「环形」二字，马上想到「两头相连」的概念，然后想「顺时针」和「逆时针」两条路。于是就想到了 `abs(i - start)` 与 `len - abs(i - start)`。
- **最容易踩的坑**：  
  - 忘记处理 `target` 不存在的情况，直接返回了错误的最小值。  
  - 计算环形距离时写成 `len - abs(i - start)` 而忘记取 `min`，导致得到的距离不是最短的。  
- **下次第一步**：先判断 `target` 是否在数组里（可以用一次遍历或集合），如果不存在立刻返回 `-1`，再去计算最短环形距离。这样可以避免不必要的计算，也更安全。