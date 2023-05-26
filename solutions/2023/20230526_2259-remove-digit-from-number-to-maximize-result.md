# #2259. 删除数字以获得最大结果 / Remove Digit From Number to Maximize Result

> 难度：简单 · 标签：String、Greedy、Enumeration · [LeetCode 链接](https://leetcode.com/problems/remove-digit-from-number-to-maximize-result/)

---

## 题目（英文原版）

**Description**

You are given a string number representing a positive integer and a character digit.
Return the resulting string after removing exactly one occurrence of digit from number such that the value of the resulting string in decimal form is maximized. The test cases are generated such that digit occurs at least once in number.

**Examples**

**Example 1:**

```
Input: number = "123", digit = "3"
Output: "12"
Explanation: There is only one '3' in "123". After removing '3', the result is "12".
```

**Example 2:**

```
Input: number = "1231", digit = "1"
Output: "231"
Explanation: We can remove the first '1' to get "231" or remove the second '1' to get "123".
Since 231 > 123, we return "231".
```

**Example 3:**

```
Input: number = "551", digit = "5"
Output: "51"
Explanation: We can remove either the first or second '5' from "551".
Both result in the string "51".
```

**Constraints**

- 2 <= number.length <= 100
- number consists of digits from '1' to '9'.
- digit is a digit from '1' to '9'.
- digit occurs at least once in number.

---

## 题目（中文翻译）

给定一个表示正整数的字符串 `number` 和一个字符 `digit`。请在 `number` 中恰好删除一次出现的 `digit`，使得删除后得到的字符串在十进制下的数值最大。测试用例保证 `digit` 至少在 `number` 中出现一次。

**示例 1**  
**输入**: `number = "123", digit = "3"`  
**输出**: `"12"`  
**解释**: `"123"` 中仅有一个 `'3'`。删除它后得到 `"12"`。

**示例 2**  
**输入**: `number = "1231", digit = "1"`  
**输出**: `"231"`  
**解释**: 可以删除第一个 `'1'` 得到 `"231"`，也可以删除第二个 `'1'` 得到 `"123"`。由于 `231 > 123`，返回 `"231"`。

**示例 3**  
**输入**: `number = "551", digit = "5"`  
**输出**: `"51"`  
**解释**: 可以删除第一个或第二个 `'5'`，两种情况均得到字符串 `"51"`。

**约束条件**  
- `2 <= number.length <= 100`  
- `number` 只包含字符 `'1'` 到 `'9'`。  
- `digit` 是字符 `'1'` 到 `'9'`。  
- `digit` 在 `number` 中至少出现一次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一个出现的 `digit` 都尝试删掉一次**，看删掉后得到的数字有多大，最后挑最大的返回。  

- **用到的数据结构**：只需要 `string`（字符串）和 `list`（可选），不需要额外的复杂结构。可以把字符串想象成一串珠子，每颗珠子上写着一个数字，删掉一颗珠子后把左边和右边的珠子重新串起来，就是一次尝试。  
- **为什么正确**：因为题目要求恰好删除 **一个** `digit`，而我们把所有可能的删除位置都遍历了一遍，必然会找到价值最大的那一种。  
- **时间/空间复杂度**：  
  - 字符串长度记作 `n`（≤100），我们最多遍历 `n` 次，每次拼接两个子串的时间也是 `O(n)`，所以总时间是 `O(n²)`。  
  - `O(n²)` 可以理解为“如果 `n` 是 100，最多会做 10 000 次基本操作”，在本题的规模下仍然很快。  
  - 只用了常数级别的额外空间（保存临时的结果字符串），所以空间是 `O(1)`。

#### 代码（Python）

```python
def removeDigit_bruteforce(number: str, digit: str) -> str:
    # 用来保存目前找到的最大结果
    best = ""

    # 遍历每一个位置 i，如果这里恰好是要删除的 digit，就尝试删掉
    for i, ch in enumerate(number):
        if ch == digit:                         # 只在出现 digit 的位置动手
            # 删除第 i 位：左边 part + 右边 part
            candidate = number[:i] + number[i + 1:]
            # 如果 candidate 更大，就更新 best
            # 这里直接比较字符串，因为长度相同，字典序和数值大小一致
            if candidate > best:
                best = candidate

    return best
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：`n` 次循环，每次拼接两个子串要遍历一次剩余的字符，总共大约 `n * n` 次字符操作。  
- **空间复杂度**：`O(1)`（不计输出字符串本身）  
  - 解释：只用了几个临时变量，额外占用的内存与 `n` 无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都完整拼接一次字符串**。其实我们只需要找到**最左边的、删掉后可以让后面的数字更大的位置**，一次遍历即可得到答案。

观察一下：  
- 当我们把某个 `digit` 删除后，**左边的部分保持不变**，唯一影响结果的是**被删掉的那个位置以及它右边的第一个字符**。  
- 为了让结果最大，**应该让左边尽可能保持不变，而让右边的数尽可能大**。  
- 具体来说，遍历字符串，找到第一个出现的 `digit`，且它右边的字符 **大于** `digit`，此时删除这个 `digit` 能让左边保持原样，右边的更大数字“提前”到前面，从而整体更大。  
- 如果遍历完都没有出现“右边更大”的情况，说明所有 `digit` 后面的数字都不大于它，这时**删除最右边的那个 `digit`**即可（因为左边相同，删得越靠右，保留下来的左侧数字越多，数值也越大）。

**类比**：把数字想成一列排好序的车厢，每节车厢上写着数字。我们只能把一节写有特定数字 `digit` 的车厢摘掉。要让剩下的列车尽可能“长且快”，我们希望把**最左边、后面有更快车厢的那节**摘掉；如果没有更快的车厢，直接把**最右边的那节**摘掉。

实现时只需要一次遍历，记录**第一个满足右边更大的位置**，或者记录**最右边出现的 `digit`**。最后根据记录的下标直接构造结果字符串。

#### 代码（Python）

```python
def removeDigit_optimal(number: str, digit: str) -> str:
    n = len(number)
    # 记录最右边出现 digit 的位置，默认 -1 表示还没出现
    last_pos = -1

    # 遍历每个字符，寻找“右边更大的情况”
    for i in range(n):
        if number[i] == digit:
            last_pos = i                     # 更新最右边出现的位置
            # 判断右边的字符是否更大
            if i + 1 < n and number[i + 1] > digit:
                # 一旦找到，立刻返回删除此位置的结果
                return number[:i] + number[i + 1:]

    # 如果没有提前返回，说明所有 digit 后面的字符都 ≤ digit
    # 此时删除最右边出现的 digit（last_pos 必然 >= 0，因为题目保证出现至少一次）
    return number[:last_pos] + number[last_pos + 1:]
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：只遍历一次字符串，所有操作都是常数时间，`n` 最多是 100，几乎瞬间完成。相比暴力的 `O(n²)`，省了大量不必要的拼接。  
- **空间复杂度**：`O(1)`  
  - 解释：只用了几个整数变量保存索引，额外空间不随 `n` 增长。

---

## 心得

- **核心技巧**：**贪心 + 单次遍历**——在满足特定“局部最优”（右边更大的第一个 `digit`）的点立即做决定，否则保留最右侧的 `digit`。  
- **适用的题型**：  
  1. “删除一个字符使字符串字典序最大”——如 *Remove K Digits*（不同但思路相似）。  
  2. “在只允许一次操作的情况下，使数值最大/最小”——例如 *Maximum Number After K Swaps*。  
- **一句话总结解题钥匙**：**把“左边保持不变、右边尽可能大”作为删除位置的选择标准**。

---

## 反思

- **第一反应**：看到“删除一个字符”，立刻想到**枚举所有可能**，因为规模小，直接暴力就能通过。  
- **最容易踩的坑**：  
  - 忽略了“右边更大的情况”只能在**第一个**出现时就决定，否则可能错过更大的数。  
  - 忘记处理 **最右边的 `digit`**，导致在没有右边更大的情况下返回错误结果。  
  - 对字符串比较的误解：在同等长度下，字符串的字典序恰好等价于数值大小。  
- **下次类似题的第一步**：先**思考是否存在局部贪心规则**（比如“左边不变、右边更大”），如果有，则尝试一次遍历直接定位，否则再回到枚举。