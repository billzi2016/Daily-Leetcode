# #402. 移除 K 位数字 / Remove K Digits

> 难度：中等 · 标签：String、Stack、Greedy、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/remove-k-digits/)

---

## 题目（英文原版）

**Description**

Given string num representing a non-negative integer num, and an integer k, return the smallest possible integer after removing k digits from num.

**Examples**

**Example 1:**

```
Input: num = "1432219", k = 3
Output: "1219"
Explanation: Remove the three digits 4, 3, and 2 to form the new number 1219 which is the smallest.
```

**Example 2:**

```
Input: num = "10200", k = 1
Output: "200"
Explanation: Remove the leading 1 and the number is 200. Note that the output must not contain leading zeroes.
```

**Example 3:**

```
Input: num = "10", k = 2
Output: "0"
Explanation: Remove all the digits from the number and it is left with nothing which is 0.
```

**Constraints**

- 1 <= k <= num.length <= 105
- num consists of only digits.
- num does not have any leading zeros except for the zero itself.

---

## 题目（中文翻译）

给定字符串（string）`num` 表示一个非负整数（non‑negative integer），以及整数（integer）`k`，返回从 `num` 中删除 `k` 位数字后可能得到的最小整数。

**示例 1：**  
**输入:** `num = "1432219", k = 3`  
**输出:** `"1219"`  
**解释:** 删除数字 `4、3、2`，得到的新数字是 `1219`，这是最小的可能结果。

**示例 2：**  
**输入:** `num = "10200", k = 1`  
**输出:** `"200"`  
**解释:** 删除前导的 `1`，剩下的数字是 `200`。注意输出不能包含前导零。

**示例 3：**  
**输入:** `num = "10", k = 2`  
**输出:** `"0"`  
**解释:** 删除所有数字后，剩下的就是 `0`。

**约束条件：**  
- `1 <= k <= num.length <= 10^5`  
- `num` 只包含数字字符。  
- 除了数字 `0` 本身外，`num` 不含前导零。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把所有可能的删法枚举一遍，选出最小的结果**。  
- 给定长度为 `n` 的字符串 `num`，我们需要删掉恰好 `k` 位。  
- 可以把这 `k` 位的下标看成从 `0 … n‑1` 中挑 `k` 个位置的组合。  
- 对每一种组合，把对应的字符删除，得到一个新的字符串，再把它转成整数（或直接比较字符串），记录最小值。  

**用到的数据结构**  
- **列表 / 数组**：保存当前组合的下标。  
- **遍历组合的工具**（如 `itertools.combinations`），相当于“查字典”，只不过字典的键是下标组合，值是对应的删后数字。  

**为什么正确**  
因为我们把**所有**合法的删法都尝试了一遍，最小的自然就是答案。只要遍历不遗漏，就一定能得到最优解。

**时间/空间复杂度**  
- 组合的数量是 `C(n, k)`（从 `n` 个位置里挑 `k` 个），这在最坏情况下接近 `n^k / k!`，当 `n` 为 100 000、`k` 也可能很大时，根本不可行。  
- 对每一种组合我们都要遍历一遍字符串生成新数，时间是 `O(n)`。  
- 所以总体时间是 **指数级**的 `O(C(n, k) * n)`，这在实际中会“卡死”。  
- 空间只需要保存当前组合和临时字符串，**O(n)**（主要是新字符串的存储）。

> 大白话：如果你把每一种删法想象成一次“选人”，总共要选 `C(n, k)` 种组合，人数越多，组合数就像天文数字一样，根本不可能一次遍历完。

#### 代码（Python）

```python
import itertools

def removeKdigits_bruteforce(num: str, k: int) -> str:
    n = len(num)
    # 如果要删掉全部，直接返回 "0"
    if k >= n:
        return "0"

    best = None  # 用来保存当前找到的最小结果

    # 遍历所有要删除的下标组合
    for del_idx in itertools.combinations(range(n), k):
        # 把要删除的下标放进集合，查询更快
        del_set = set(del_idx)

        # 生成删除后的新字符串
        cur = []
        for i, ch in enumerate(num):
            if i not in del_set:          # 只保留没被删的字符
                cur.append(ch)

        # 去掉前导零，空串视作 "0"
        cur_str = ''.join(cur).lstrip('0') or '0'

        # 更新最小值
        if best is None or len(cur_str) < len(best) or (len(cur_str) == len(best) and cur_str < best):
            best = cur_str

    return best
```

> 关键行中文注释已写在代码里，直接复制运行即可（不过仅适合 `n` 很小的测试）。

#### 复杂度  

- **时间复杂度**：`O(C(n, k) * n)` → 组合数是指数级的，实际不可接受。  
- **空间复杂度**：`O(n)` → 主要用于保存临时生成的字符串。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**枚举所有删除方式**。  
我们需要一种**一次遍历**就能决定哪些数字应该被删除的策略。  

观察题目：我们希望得到**最小的数**，这意味着**左侧的高位尽可能小**。  
如果在某个位置 `i`，当前数字 `num[i]` 比左边的数字大，而左边的数字可以被删除（还有删除配额），把左边的大数字删掉会让整体变小。  

这正是**单调递增栈（Monotonic Stack）**的核心思想：  
- 栈顶保存已经确定的、从左到右**递增**的数字。  
- 当遇到一个更小的数字时，**弹出**（删除）栈顶比它大的数字，直到栈顶不再比当前数字大或已经没有删除次数 `k`。  

步骤如下：

1. 创建一个空栈 `stack`（用列表实现）。  
2. 遍历字符串 `num` 中的每个字符 `c`：  
   - 当 `k > 0` 并且栈不为空且栈顶 `> c` 时，弹出栈顶（相当于删除一个数字），`k -= 1`。  
   - 将 `c` 推入栈。  
3. 循环结束后，若还有剩余的删除次数（`k > 0`），说明数字已经是单调递增的了，只能从**右侧**删除——直接把栈的后 `k` 位截掉。  
4. 把栈里的字符拼成字符串，去掉前导零（`lstrip('0')`），如果结果为空返回 `"0"`。

**为什么正确**  
- **贪心证明**：在遍历过程中，每当我们发现左侧的数字比右侧的大且还有删位机会时，删除左侧的大数字一定不会使最终结果变大，因为左侧的高位被更小的数字取代，整体数值必然减小。  
- 只要我们在**每一次**都做出“当前最优”（把能删的左侧大数删掉），后面的选择不受之前的影响，整个过程得到的就是全局最小。  
- 若遍历结束后仍有剩余删除次数，说明整个序列已经是递增的，此时只能删掉最右侧的数字——这也是让数值最小的唯一方式。

**类比**：想象你在排队买票，队伍里有人比后面的人年龄更大（数字更大），而你手里有“可以请人离开队伍”的卡（删除次数）。只要卡还没用完，你就让年龄更大的人先走（删除），这样队伍里留下的都是年龄最小的，最终排成的队列（数字序列）自然是最小的。

#### 代码（Python）

```python
def removeKdigits(num: str, k: int) -> str:
    """
    使用单调递增栈的贪心算法，时间 O(n)，空间 O(n)
    """
    stack = []                     # 用列表当栈，保存已经遍历过且未被删除的数字
    remain = k                     # 还能删除的次数

    for c in num:                  # 从左到右扫描每个字符
        # 当栈不为空、栈顶数字大于当前数字、并且还有删除次数时，弹出栈顶
        while remain > 0 and stack and stack[-1] > c:
            stack.pop()            # 删除栈顶，等价于把这个数字从原串中去掉
            remain -= 1            # 删除次数减一
        stack.append(c)            # 把当前数字压入栈，保持相对顺序

    # 如果遍历完仍有剩余的删除次数，只能从右侧截掉
    if remain:
        stack = stack[:-remain]    # 删除最后 remain 个字符

    # 把栈中的字符拼成字符串，并去掉前导零
    result = ''.join(stack).lstrip('0')

    # 若结果为空（全被删掉或全是零），返回 "0"
    return result if result else "0"
```

#### 复杂度  

- **时间复杂度**：`O(n)`，只遍历一次字符串，栈的每个元素最多被压入一次、弹出一次。  
  - 与暴力解相比，原来的指数级下降到线性，几乎可以处理 `10^5` 长度的输入。  
- **空间复杂度**：`O(n)`，最坏情况下栈会保存全部字符（比如已经是递增的），需要额外 `n` 的空间。

---

## 心得  

- **核心技巧**：**单调递增栈 + 贪心**——在需要“保持某种单调性”且要“删除若干元素”时非常有用。  
- **适用的类似题型**：  
  1. **LeetCode 402. Remove K Digits**（本题）。  
  2. **LeetCode 84. Largest Rectangle in Histogram**（利用单调栈求最大矩形）。  
  3. **LeetCode 228. Summary Ranges**（虽然不涉及删除，但单调栈常用于处理区间的边界）。  
- **一句话总结**：**把能删的左侧“大数”赶紧踢走，剩下的自然最小**。

---

## 反思  

- **第一反应**：想到“枚举所有删法”，因为直觉上要比较所有可能才放心。  
- **最容易踩的坑**：  
  - **前导零**：删除后可能出现 `000...`，需要手动去掉，否则输出会不符合要求。  
  - **全部删除**：`k` 等于字符串长度时应直接返回 `"0"`，否则 `stack[:-0]` 会出错。  
  - **剩余删除次数**：遍历结束后仍有 `k` 时忘记从右侧截断。  
- **下次遇到同类题**：第一步先问自己“是否可以通过一次遍历把不需要的元素剔除？”——如果答案是“可以”，就尝试**单调栈或双指针的贪心**思路。