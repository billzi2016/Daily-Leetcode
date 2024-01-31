# #2566. 最大差值（通过重新映射一个数字） / Maximum Difference by Remapping a Digit

> 难度：简单 · 标签：Math、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximum-difference-by-remapping-a-digit/)

---

## 题目（英文原版）

**Description**

You are given an integer num. You know that Bob will sneakily remap one of the 10 possible digits (0 to 9) to another digit.
Return the difference between the maximum and minimum values Bob can make by remapping exactly one digit in num.
Notes:

**Examples**

**Example 1:**

```
Input: num = 11891
Output: 99009
Explanation: 
To achieve the maximum value, Bob can remap the digit 1 to the digit 9 to yield 99899.
To achieve the minimum value, Bob can remap the digit 1 to the digit 0, yielding 890.
The difference between these two numbers is 99009.
```

**Example 2:**

```
Input: num = 90
Output: 99
Explanation:
The maximum value that can be returned by the function is 99 (if 0 is replaced by 9) and the minimum value that can be returned by the function is 0 (if 9 is replaced by 0).
Thus, we return 99.
```

**Constraints**

- 1 <= num <= 108

---

## 题目（中文翻译）

给定一个整数 `num`。已知 Bob 会偷偷地将十个可能的数字（0 到 9）中的 **一个** 数字重新映射为另一个数字。  
返回 Bob 通过在 `num` 中恰好重新映射 **一个** 数字所能得到的 **最大值** 与 **最小值** 之差。

## 示例

### 示例 1
**输入**  
`num = 11891`

**输出**  
`99009`

**解释**  
- 为了得到最大值，Bob 可以将数字 `1` 重新映射为数字 `9`，得到 `99899`。  
- 为了得到最小值，Bob 可以将数字 `1` 重新映射为数字 `0`，得到 `890`。  
这两个数的差为 `99009`。

### 示例 2
**输入**  
`num = 90`

**输出**  
`99`

**解释**  
- 最大值可以通过把 `0` 替换为 `9` 得到 `99`。  
- 最小值可以通过把 `9` 替换为 `0` 得到 `0`。  
因此返回 `99`。

## 约束条件
- `1 <= num <= 10^8`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把「把某个数字全部换成另一个数字」这件事枚举遍历一遍：

1. 把 `num` 转成字符串，方便逐位查看和替换。  
2. 枚举 **原来的数字** `d`（0~9）和 **要换成的数字** `x`（0~9），要求 `d != x`。  
3. 把字符串里所有字符等于 `d` 的位置全部改成 `x`，得到一个新的字符串 `s'`。  
4. 把 `s'` 转回整数（Python 的 `int` 会自动去掉前导零），得到该映射下的数值。  
5. 在所有可能的映射中记录最大的数值 `max_val`，最小的数值 `min_val`，最后返回 `max_val - min_val`。

> **类比**：把哈希表想象成一本词典，`d` 是词，`x` 是对应的页码。我们把所有出现的词统一指向新的页码，就得到新的词典。这里我们只需要遍历所有可能的词（0~9）和页码（0~9），找出最大/最小的结果。

**为什么一定对？**  
题目只要求「恰好一次」的映射，且映射的对象只能是「某个数字」而不是「某个位置」。枚举所有合法的 `(d, x)` 组合就覆盖了所有可能的操作，必然能找到最大和最小的数。

**复杂度分析（大白话）**  
- 枚举 10 个原数字 × 10 个目标数字 = 100 种情况，常数级别。  
- 对每种情况我们要遍历一次字符串，长度至多 9（因为 `num ≤ 10⁸`），所以每次的工作量是 O(长度)。  
- 综合下来，时间复杂度是 **O(10·10·L) ≈ O(L)**，这里的 `L` 代表数字的位数，最多 9 位，几乎可以视为常数。  
- 只用了原字符串和几个整数变量，空间复杂度是 **O(L)**（保存字符串本身），同样很小。

#### 代码（Python）

```python
def maxDiff(num: int) -> int:
    s = str(num)                 # 把整数转成字符串，方便逐位操作
    max_val = -float('inf')      # 用来记录最大的数
    min_val = float('inf')       # 用来记录最小的数

    # 枚举所有可能的「被映射的数字」d 和「映射成的数字」x
    for d in map(str, range(10)):          # d 是字符形式的原数字
        for x in map(str, range(10)):      # x 是字符形式的目标数字
            if d == x:
                continue                  # 必须真的换一个不同的数字
            # 把所有 d 替换成 x，得到新的字符串
            transformed = s.replace(d, x)
            # 转成整数，自动去掉前导零（比如 "001" → 1，"0" → 0）
            val = int(transformed)
            # 更新最大、最小值
            max_val = max(max_val, val)
            min_val = min(min_val, val)

    return max_val - min_val
```

#### 复杂度

- **时间复杂度**：`O(L)`（`L` 为 `num` 的位数，最多 9），因为枚举的组合数是常数 100。
- **空间复杂度**：`O(L)`，主要是存放字符串 `s` 与 `transformed`。

---

### 2. 最优解

#### 思路  

暴力解已经足够快，但我们可以 **用数学观察** 把枚举次数降到 **一次遍历**，这也是面试官常期待的「贪心」思路。

1. **求最大值**  
   - 为了让数字尽可能大，我们希望把 **最高位**（左边第一个）不是 `9` 的数字全部换成 `9`。  
   - 只要把**第一个出现的非 9** 的数字 `d` 映射成 `9`，后面所有相同的 `d` 也会一起变成 `9`，这已经是最大的可能。  
   - 例子 `11891`：左起第一个不是 `9` 的是 `1`，把所有 `1` 换成 `9` → `99899`。  

2. **求最小值**  
   - 为了让数字尽可能小，我们希望把 **最高位**（左边第一个）不是 `0` 的数字全部换成 `0`，**但** 最高位不能变成前导零，否则整数会少一位。  
   - 因此分两种情况：
     - 如果最高位本身不是 `0`，把它换成 `0`（这会导致前导零被自动去掉），得到最小值。  
     - 否则（最高位已经是 `0`，说明原数是 `0` 开头的，这不可能，因为 `num` 是正整数），我们寻找**第一个非 0 且不是最高位的数字** `d`，把它换成 `0`。  
   - 例子 `11891`：最高位是 `1`，把所有 `1` 换成 `0` → `"00890"` → 整数 `890`。  

3. **实现细节**  
   - 将 `num` 转成字符列表 `chars`，遍历一次即可找到两种映射的目标数字 `d_max`、`d_min`。  
   - 再遍历一次（或直接在第一次遍历中完成）生成最大数和最小数的字符串。  
   - 最后把两者转成整数求差。

> **类比**：把数字看成一排小盒子，左边的盒子价值更高。要让总价值最大，只需要把左边第一个「不够好」的盒子里的东西全部升级（换成 9）。要让总价值最小，只需要把左边第一个「还能更差」的盒子里的东西全部降级（换成 0），但降级不能把最左边的盒子直接变成「空盒」——否则盒子会整体向左移动，导致位数变少。

#### 代码（Python）

```python
def maxDiff(num: int) -> int:
    s = str(num)
    chars = list(s)

    # ---------- 求最大值 ----------
    # 找到第一个不是 '9' 的数字 d_max
    d_max = None
    for ch in chars:
        if ch != '9':
            d_max = ch
            break
    # 如果整个数字都是 9，最大值就是它本身
    if d_max is None:
        max_num = num
    else:
        # 把所有 d_max 换成 '9'
        max_str = ''.join('9' if c == d_max else c for c in chars)
        max_num = int(max_str)   # 自动去掉前导零（这里不会出现）

    # ---------- 求最小值 ----------
    # 最高位不能直接换成 0（会产生前导零），所以先判断
    first = chars[0]
    if first != '0':
        # 把最高位所在的数字全部换成 '0'
        d_min = first
        min_str = ''.join('0' if c == d_min else c for c in chars)
    else:
        # 最高位已经是 0（只会在 num = 0 的情况下出现），
        # 实际上题目保证 num >= 1，下面这段是安全兜底
        d_min = None
        min_str = s

    # 若最高位换成 0 导致前导零，需要去掉这些前导零
    min_num = int(min_str)   # int() 会自动去掉所有前导零

    return max_num - min_num
```

#### 复杂度

- **时间复杂度**：`O(L)`，只需要遍历字符串两次（一次找目标数字，一次构造新字符串），`L` 为位数，最多 9。相比暴力的「常数 × L」更直观，也不依赖于枚举 100 种组合。
- **空间复杂度**：`O(L)`，用于保存字符列表和新构造的字符串，同样只和位数有关。

---

## 心得

- **核心技巧**：**贪心 + 位数观察**  
  - 通过「左边的数字价值更高」这一事实，直接定位「第一个不符合极值要求的数字」进行统一替换，就能一次遍历得到最优解。  
- **适用的题型**  
  1. **把数字中的某个字符全部替换**（如 LeetCode 2579 `Maximum Difference by Remapping a Digit`）。  
  2. **把数字中的某位改成 0/9 以得到极值**（如 2236 `Root Equals Sum of Children` 中的类似思路）。  
  3. **把字符串中的某字符统一替换成另一个字符**（如 2265 `Count Nodes Equal to Average of Subtree` 中的字符映射变形）。  
- **一句话总结解题钥匙**：**左起第一位不满足目标（最大要找非 9，最小要找非 0）的数字，就是唯一需要改动的对象**。

---

## 反思

- **第一反应**：直接把所有可能的映射枚举一遍，写代码最快。
- **最容易踩的坑**  
  - **前导零**：把最高位映射成 `0` 时，整数会自动去掉前导零，导致位数缩短，需要用 `int()` 或手动去掉。  
  - **全 9 或全 0 的特殊情况**：如果原数字已经是全部 `9`，最大值不需要再替换；如果最高位是 `0`（只有 `num = 0` 才会出现），最小值也不需要替换。  
- **下次类似题的第一步**：先观察**最高位的影响**，判断「从左到右第一个违背目标的数字」是什么，直接把它统一替换成极端值（0 或 9），即可得到答案。