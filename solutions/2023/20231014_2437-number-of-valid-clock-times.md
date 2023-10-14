# #2437. 有效时钟时间的数量 / Number of Valid Clock Times

> 难度：简单 · 标签：String、Enumeration · [LeetCode 链接](https://leetcode.com/problems/number-of-valid-clock-times/)

---

## 题目（英文原版）

**Description**

You are given a string of length 5 called time, representing the current time on a digital clock in the format "hh:mm". The earliest possible time is "00:00" and the latest possible time is "23:59".
In the string time, the digits represented by the ? symbol are unknown, and must be replaced with a digit from 0 to 9.
Return an integer answer, the number of valid clock times that can be created by replacing every ? with a digit from 0 to 9.

**Examples**

**Example 1:**

```
Input: time = "?5:00"
Output: 2
Explanation: We can replace the ? with either a 0 or 1, producing "05:00" or "15:00". Note that we cannot replace it with a 2, since the time "25:00" is invalid. In total, we have two choices.
```

**Example 2:**

```
Input: time = "0?:0?"
Output: 100
Explanation: Each ? can be replaced by any digit from 0 to 9, so we have 100 total choices.
```

**Example 3:**

```
Input: time = "??:??"
Output: 1440
Explanation: There are 24 possible choices for the hours, and 60 possible choices for the minutes. In total, we have 24 * 60 = 1440 choices.
```

**Constraints**

- time is a valid string of length 5 in the format "hh:mm".
- "00" <= hh <= "23"
- "00" <= mm <= "59"
- Some of the digits might be replaced with '?' and need to be replaced with digits from 0 to 9.

---

## 题目（中文翻译）

给定一个长度为 5 的字符串 `time`，它表示数字时钟上当前的时间，格式为 `"hh:mm"`。最早的可能时间是 `"00:00"`，最晚的可能时间是 `"23:59"`。  
在字符串 `time` 中，用 `?` 符号表示未知的数字，需要将每个 `?` 替换为 `0`~`9` 中的某个数字。  

返回一个整数 `answer`，即将所有 `?` 替换后能够得到的 **有效时钟时间**（valid clock times）的数量。

## 示例

### 示例 1  
**输入**: `time = "?5:00"`  
**输出**: `2`  
**解释**: 我们可以把 `?` 替换成 `0` 或 `1`，得到 `"05:00"` 或 `"15:00"`。不能替换成 `2`，因为 `"25:00"` 超出了合法范围。总共有两种可能。

### 示例 2  
**输入**: `time = "0?:0?"`  
**输出**: `100`  
**解释**: 每个 `?` 都可以替换成 `0`~`9` 中的任意数字，所以共有 `10 × 10 = 100` 种组合。

### 示例 3  
**输入**: `time = "??:??"`  
**输出**: `1440`  
**解释**: 小时（`hh`）有 24 种合法取值，分钟（`mm`）有 60 种合法取值，故总共 `24 × 60 = 1440` 种可能。

## 约束

- `time` 是长度为 5、符合 `"hh:mm"` 格式的合法字符串。  
- `"00"` ≤ `hh` ≤ `"23"`  
- `"00"` ≤ `mm` ≤ `"59"`  
- 部分数字可能被 `'?'` 替代，需要用 `0`~`9` 的数字进行填补。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是把 `?` 全部枚举成 `0~9` 的所有可能，然后检查每一种组合是否是合法的时刻。  
- **枚举**：把时间的每一位（共 4 位数字）都从 `0` 到 `9` 依次尝试。  
- **合法性检查**：把得到的 4 位数字拼成 `"hh:mm"`，判断它是否满足 `00 ≤ hh ≤ 23` 且 `00 ≤ mm ≤ 59`。  
- **数据结构类比**：这里用到的“检查合法性”相当于在字典里查词，`hh`、`mm` 就是要查的“词”，合法范围就是“词典”。  

这种方法一定能得到正确答案，因为我们把**所有**可能的组合都试了一遍，只要满足时钟的限制，就算有效。

#### 代码（Python）

```python
def countTime(time: str) -> int:
    # 把字符列表化，方便后面替换
    chars = list(time)

    ans = 0                     # 统计合法时刻的个数
    # 枚举四个位置的数字，若该位置是 ? 则遍历 0~9；否则直接使用原来的数字
    for h1 in range(10) if chars[0] == '?' else [int(chars[0])]:
        for h2 in range(10) if chars[1] == '?' else [int(chars[1])]:
            for m1 in range(10) if chars[3] == '?' else [int(chars[3])]:
                for m2 in range(10) if chars[4] == '?' else [int(chars[4])]:
                    hour   = h1 * 10 + h2          # 组合出小时数
                    minute = m1 * 10 + m2          # 组合出分钟数
                    # 合法性判断：0~23 的小时、0~59 的分钟
                    if 0 <= hour < 24 and 0 <= minute < 60:
                        ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(10⁴) = O(10000)`。  
  解释：最坏情况下四个位置都是 `?`，我们要遍历 `10 × 10 × 10 × 10 = 10000` 种组合。对初学者来说，`10⁴` 就是“一万次”，在电脑里几乎是瞬间完成的。
- **空间复杂度**：`O(1)`。  
  只用了常数个变量来保存计数和临时数字，不会随输入规模增长而增加额外空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**盲目枚举**——即使大多数组合会被直接判为非法，我们仍然要遍历它们。  
观察时钟的取值范围，我们可以**直接计算每一位上合法数字的个数**，再把这些计数相乘得到答案。  

1. **小时的十位 (`h1`)**  
   - 如果 `h1` 为 `?`，合法取值取决于第二位 `h2`（如果已知）或者整体范围。  
   - 当 `h1` 为 `0`、`1` 时，第二位可以是 `0~9`（共 10 种）。  
   - 当 `h1` 为 `2` 时，第二位只能是 `0~3`（共 4 种）。  
   - 当 `h1` 为 `?` 且 `h2` 也是 `?`，合法十位有 `0、1、2`（共 3 种），对应的第二位数目分别是 10、10、4，后面会乘进去。  

2. **小时的个位 (`h2`)**  
   - 已知 `h1` 时，可直接得出合法的个位数目。  
   - 若 `h2` 为 `?`，根据 `h1` 的取值范围确定合法位数（如 `h1 = 2` 时只能是 `0~3`）。  

3. **分钟的十位 (`m1`)**  
   - 只要不是 `?`，合法取值是 `0~5`（共 6 种），因为分钟的十位最大只能是 5。  

4. **分钟的个位 (`m2`)**  
   - 任意数字 `0~9`（共 10 种），只要不是 `?` 就固定为 1 种。  

把每一位的合法选择数相乘，就得到所有可能的合法时刻数。  
这一步只做了常数次的判断和乘法，时间复杂度 **降到 O(1)**。

下面给出一种实现方式：先算出每一位可能的取值集合（用列表），再把它们的长度相乘。

#### 代码（Python）

```python
def countTime(time: str) -> int:
    # 预先把每一位可能的数字集合算出来
    h1, h2, _, m1, m2 = time   # '_' 跳过冒号

    # 小时十位的合法集合
    if h1 == '?':
        if h2 == '?':                     # 两位都是 ?
            h1_choices = ['0', '1', '2']  # 0、1、2 都有可能
        else:
            # h2 已知，只有当 h2 <= '3' 时才可以取 '2'
            h1_choices = ['0', '1']
            if h2 <= '3':
                h1_choices.append('2')
    else:
        h1_choices = [h1]                  # 已确定唯一一种

    # 小时个位的合法集合（先不考虑 h1 的限制，后面统一过滤）
    if h2 == '?':
        h2_choices = [str(d) for d in range(10)]
    else:
        h2_choices = [h2]

    # 过滤掉不满足 hour < 24 的组合
    hour_choices = 0
    for a in h1_choices:
        for b in h2_choices:
            hour = int(a + b)
            if 0 <= hour < 24:
                hour_choices += 1          # 统计合法的 hour 组合数

    # 分钟十位
    if m1 == '?':
        m1_choices = [str(d) for d in range(6)]   # 0~5
    else:
        m1_choices = [m1]

    # 分钟个位
    if m2 == '?':
        m2_choices = [str(d) for d in range(10)]  # 0~9
    else:
        m2_choices = [m2]

    minute_choices = len(m1_choices) * len(m2_choices)

    # 最终答案 = 合法小时组合数 × 合法分钟组合数
    return hour_choices * minute_choices
```

> **代码说明**  
> - 第 1‑3 行把时间字符串拆成单个字符，`_` 用来跳过冒号。  
> - 对每一位分别列出所有可能的字符（`h1_choices`、`h2_choices` 等），再用两层循环过滤掉 **非法的小时**（大于等于 24 的情况）。  
> - 分钟的合法性可以直接用集合大小相乘，因为十位最大 5、个位最大 9，互不影响。  

#### 复杂度

- **时间复杂度**：`O(1)`。  
  只进行常数次的循环（最多 `3 × 10 = 30` 次检查小时合法性），不随输入长度变化。对比暴力的 `10⁴` 次遍历，快了好几个数量级。  
- **空间复杂度**：`O(1)`。  
  使用的列表长度最多 10，都是常数级别的额外空间。

---

## 心得

- **核心技巧**：**枚举合法取值并乘法计数**。先把每一位的合法范围算清楚，再利用乘法原理得到总数。  
- **适用题型**：  
  1. “数字填空” 类题目，如 **`Number of Valid Clock Times`**、**`Valid Time`**（把 `?` 换成合法数字）。  
  2. “组合计数” 类题目，如 **`Number of Unique Good Substrings`**（先算每个字符的合法选择）。  
  3. “区间约束计数” 类题目，如 **`Count Binary Substrings`**（先算每段长度的取值范围）。  
- **一句话总结**：把约束转化为“每位可以有多少种合法选择”，最后用乘法把它们合在一起，就是答案。

---

## 反思

- **第一反应**：看到 `?` 就想“把它们全遍历”，因为最直观的办法是穷举。  
- **最容易踩的坑**：  
  - **小时的上限**不是简单的 `0~2`，而是 **十位为 2 时个位只能到 3**，容易忘记导致计数错误。  
  - **分钟十位**只能到 5，忘记这点会把非法的 `6x`、`7x`… 计进去。  
- **下次第一步**：先**手动列出每一位的合法范围**（考虑相邻位的相互限制），再决定是直接枚举还是用乘法计数。这样可以迅速判断是否需要优化枚举。