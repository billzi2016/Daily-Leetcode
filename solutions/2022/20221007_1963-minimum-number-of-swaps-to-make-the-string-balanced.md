# #1963. 使字符串平衡的最少交换次数 / Minimum Number of Swaps to Make the String Balanced

> 难度：中等 · 标签：Two Pointers、String、Stack、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-swaps-to-make-the-string-balanced/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string s of even length n. The string consists of exactly n / 2 opening brackets '[' and n / 2 closing brackets ']'.
A string is called balanced if and only if:
You may swap the brackets at any two indices any number of times.
Return the minimum number of swaps to make s balanced.

**Examples**

**Example 1:**

```
Input: s = "][]["
Output: 1
Explanation: You can make the string balanced by swapping index 0 with index 3.
The resulting string is "[[]]".
```

**Example 2:**

```
Input: s = "]]][[["
Output: 2
Explanation: You can do the following to make the string balanced:
- Swap index 0 with index 4. s = "[]][][".
- Swap index 1 with index 5. s = "[[][]]".
The resulting string is "[[][]]".
```

**Example 3:**

```
Input: s = "[]"
Output: 0
Explanation: The string is already balanced.
```

**Constraints**

- n == s.length
- 2 <= n <= 106
- n is even.
- s[i] is either '[' or ']'.
- The number of opening brackets '[' equals n / 2, and the number of closing brackets ']' equals n / 2.

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的字符串 `s`，其长度为偶数 `n`。字符串恰好包含 `n / 2` 个左方括号 `'['` 和 `n / 2` 个右方括号 `']'`。

当且仅当以下条件成立时，字符串被称为 **平衡（balanced）**：

- 对于字符串的任意前缀，左方括号 `'['` 的数量不小于右方括号 `']'` 的数量；
- 整个字符串中左方括号和右方括号的数量相等（题目已保证）。

你可以任意次数地交换任意两个下标处的括号。返回使 `s` **平衡（balanced）** 所需的最小交换次数。

## 示例

### 示例 1
**输入**  
` s = "][][" `  

**输出**  
`1`  

**解释**  
将下标 `0` 与下标 `3` 交换后，得到平衡字符串 `"[[]]"`。

### 示例 2
**输入**  
` s = "]]][[[" `  

**输出**  
`2`  

**解释**  
可以按如下步骤得到平衡字符串：

1. 交换下标 `0` 与下标 `4`，得到 `s = "[]][]["`。  
2. 交换下标 `1` 与下标 `5`，得到 `s = "[[][]]"`。  

最终得到的字符串 `"[[][]]"` 是平衡的。

### 示例 3
**输入**  
` s = "[]" `  

**输出**  
`0`  

**解释**  
该字符串已经是平衡的，无需交换。

## 约束条件

- `n == s.length`
- `2 <= n <= 10^6`
- `n` 为偶数
- `s[i]` 为 `'['` 或 `']'`
- 左方括号 `'['` 的数量恰好为 `n / 2`，右方括号 `']'` 的数量也恰好为 `n / 2`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**把每一次不平衡的 `]` 当成“需要换位”的信号**，然后把它和后面最近的 `[` 交换。  
可以把字符串想象成一排座位，`[` 像是“左手”，`]` 像是“右手”。我们希望从左到右遍历时，左手的数量永远不比右手少，否则就出现“右手多于左手”，这时就需要把后面某个左手（`[`）提前到这里去“平衡”。  

暴力实现的步骤：

1. 从左到右遍历字符串，用 `balance` 记录当前左手(`[` )减去右手(`]`)的差值。  
   - `balance += 1` 表示遇到 `[`，左手多了一个。  
   - `balance -= 1` 表示遇到 `]`，右手多了一个。  
2. 当 `balance` 变成负数时，说明已经出现了“右手多于左手”。这时我们在**后面**找最近的 `[`（即左手）并把它和当前的 `]` 交换。  
3. 交换一次后，`balance` 会恢复到 `+1`（因为我们把一个左手提前了），继续遍历。  

> **为什么正确？**  
> 每一次出现 `balance < 0`，必然意味着当前前缀里 `]` 的数量大于 `[`，这在任何平衡字符串里都是不允许的。把最近的左手提前到这里是最省“步数”的做法，因为左手越靠后，越可能在后面的其它位置再次被需要。一次交换立刻把当前前缀恢复为合法（`balance` 变为正），所以最终得到的字符串一定是平衡的。

#### 代码（Python）

```python
def minSwaps_bruteforce(s: str) -> int:
    # 把字符串转成列表，方便原地交换
    arr = list(s)
    n = len(arr)
    balance = 0          # 左手数 - 右手数
    swaps = 0

    for i in range(n):
        if arr[i] == '[':
            balance += 1
        else:  # arr[i] == ']'
            balance -= 1

        # 一旦出现右手多于左手，必须进行一次交换
        if balance < 0:
            # 在后面找最近的 '['
            j = i + 1
            while j < n and arr[j] != '[':
                j += 1
            # 必然能找到，因为题目保证左手、右手数量相等
            arr[i], arr[j] = arr[j], arr[i]   # 交换
            swaps += 1
            balance = 1   # 交换后当前位变成 '['，所以平衡值恢复为 +1

    return swaps
```

#### 复杂度

- **时间复杂度：** `O(n²)`  
  最坏情况下每次 `balance < 0` 都要在后面遍历一次找 `[`，这相当于两层循环。  
  用生活化的说法：想象每次都要去仓库的最远端找工具，工具越多，找的次数越多，整体工作量呈平方增长。

- **空间复杂度：** `O(n)`  
  需要把字符串转成列表（`list(s)`）来支持原地交换，额外占用与输入等长的空间。  

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**每次不平衡都要线性搜索后面的 `[`**。我们可以用**双指针**一次遍历把这一步省掉。

核心观察：

1. 只要遍历过程中 `balance` 从非负变为负，就说明在当前前缀里 `]` 多了。  
2. 为了让 `balance` 恢复为非负，只需要把**最右侧的 `[`**（也就是后面未使用的左手）提前到这里。  
3. 记录所有 `[` 的下标（或者直接用指针指向下一个可用的 `[`），每次出现 `balance < 0` 时，直接取这个下标进行一次“假想的交换”。实际不必真的改动字符串，只要计数即可，因为交换后 `balance` 恰好加 2（`-1` 变成 `+1`）。

实现细节：

- 用一个指针 `left` 从左往右扫描，记录已经看到的 `[` 的下标列表 `open_pos`（可以是栈）。  
- 用另一个指针 `right` 指向 `open_pos` 中**最右侧还未使用**的下标。  
- 当 `balance < 0` 时，`right` 指向的 `[` 与当前 `]` 交换，`swaps += 1`，`balance += 2`（因为原本 `]` 贡献 -1，交换后变成 `[` 贡献 +1）。  
- 交换后，把 `right` 向左移动一位，表示这个 `[` 已经被用掉。

其实更简洁的写法是不保存全部下标，只保存**最近的未使用的 `[`**的下标。因为我们只会在 `balance < 0` 时使用它，而且使用后它再也不可能被再次使用。

下面给出最常见的 **贪心 + 双指针** 实现：

#### 代码（Python）

```python
def minSwaps(s: str) -> int:
    """
    贪心 + 双指针，只遍历一次 O(n)。
    """
    n = len(s)
    balance = 0          # 左手数 - 右手数
    swaps = 0
    # left_ptr 用来找下一个可以交换的 '['，从左往右扫描
    left_ptr = 0

    # 预处理：找第一个 '[' 的位置，后面会用 left_ptr 向后移动
    while left_ptr < n and s[left_ptr] != '[':
        left_ptr += 1

    for i, ch in enumerate(s):
        if ch == '[':
            balance += 1
        else:               # ch == ']'
            balance -= 1

        # 当 balance 变负，说明当前前缀不平衡，需要一次交换
        if balance < 0:
            # left_ptr 必然指向一个未使用的 '['，因为 '[' 与 ']' 数相等
            swaps += 1
            balance += 2   # 交换后相当于把当前的 ']' 换成 '['，所以 +2

            # 把 left_ptr 向后移动，找下一个可用的 '['
            left_ptr += 1
            while left_ptr < n and s[left_ptr] != '[':
                left_ptr += 1

    return swaps
```

> **代码解释**  
> - `balance`：记录遍历到当前位置时左手比右手多多少。  
> - `swaps`：累计需要的交换次数。  
> - `left_ptr`：指向下一个可以提供的左手（`[`），相当于“仓库里最近的工具”。每当需要交换时，直接使用它，不必再遍历整个后半段。  
> - 当 `balance < 0` 时，说明右手多了 1 个。把一个左手提前进来后，右手少了 1 个、左手多了 1 个，整体 `balance` 增加 2，正好恢复非负。  

#### 复杂度

- **时间复杂度：** `O(n)`  
  只进行一次线性遍历，`left_ptr` 也只向右移动最多 `n` 步。  
  用大白话说：我们只走了一遍字符串，就把所有“不平衡”都修好，工作量随字符数量线性增长。

- **空间复杂度：** `O(1)`  
  只用了几个整数变量，不随输入规模增长额外占用空间。  

---

## 心得

- **核心技巧**：**贪心 + 双指针**。遇到不平衡时，立刻用最近的未使用左括号进行一次“假想交换”。  
- **适用的题型**  
  1. “最小交换次数使字符串平衡”系列（如 `Minimum Swaps to Make Balanced Parentheses`）。  
  2. “最小翻转次数使二进制数组全为 1” 类似的前缀不平衡问题。  
  3. “最小交换次数使所有 0 移到左侧，1 移到右侧” 的贪心解法。  
- **一句话总结**：**只要在遍历时记录前缀差值，负值出现时立即用最近的可用正值补齐，交换次数即为负值出现的次数**。

---

## 反思

- **第一反应**：看到 `[` 与 `]` 数量相等，立刻想到“前缀平衡”概念，检查遍历时的差值。  
- **最容易踩的坑**  
  1. **忘记把 `balance` 恢复为正**：交换后应 `+= 2`，否则后续判断会出错。  
  2. **没有正确维护 `left_ptr`**：需要保证它指向的 `[` 尚未被使用，否则会重复计数。  
  3. **边界条件**：字符串全是 `[` 或 `]`（在本题不会出现）会导致找不到可用的 `[`，实现时要确保 `left_ptr` 不越界。  
- **下次类似题的第一步**：先用一个计数器（如 `balance`）遍历一次，定位“前缀不合法”出现的位置，再思考如何用最近的合法元素一次性修复。这样往往能直接导出 O(n) 的贪心解。