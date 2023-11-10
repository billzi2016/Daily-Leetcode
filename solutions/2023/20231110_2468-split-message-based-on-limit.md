# #2468. 按限制拆分消息 / Split Message Based on Limit

> 难度：困难 · 标签：String、Binary Search、Enumeration · [LeetCode 链接](https://leetcode.com/problems/split-message-based-on-limit/)

---

## 题目（英文原版）

**Description**

You are given a string, message, and a positive integer, limit.
You must split message into one or more parts based on limit. Each resulting part should have the suffix "<a/b>", where "b" is to be replaced with the total number of parts and "a" is to be replaced with the index of the part, starting from 1 and going up to b. Additionally, the length of each resulting part (including its suffix) should be equal to limit, except for the last part whose length can be at most limit.
The resulting parts should be formed such that when their suffixes are removed and they are all concatenated in order, they should be equal to message. Also, the result should contain as few parts as possible.
Return the parts message would be split into as an array of strings. If it is impossible to split message as required, return an empty array.

**Examples**

**Example 1:**

```
Input: message = "this is really a very awesome message", limit = 9
Output: ["thi<1/14>","s i<2/14>","s r<3/14>","eal<4/14>","ly <5/14>","a v<6/14>","ery<7/14>"," aw<8/14>","eso<9/14>","me<10/14>"," m<11/14>","es<12/14>","sa<13/14>","ge<14/14>"]
Explanation:
The first 9 parts take 3 characters each from the beginning of message.
The next 5 parts take 2 characters each to finish splitting message. 
In this example, each part, including the last, has length 9. 
It can be shown it is not possible to split message into less than 14 parts.
```

**Example 2:**

```
Input: message = "short message", limit = 15
Output: ["short mess<1/2>","age<2/2>"]
Explanation:
Under the given constraints, the string can be split into two parts: 
- The first part comprises of the first 10 characters, and has a length 15.
- The next part comprises of the last 3 characters, and has a length 8.
```

**Constraints**

- 1 <= message.length <= 104
- message consists only of lowercase English letters and ' '.
- 1 <= limit <= 104

---

## 题目（中文翻译）

给定一个字符串 `message` 和一个正整数 `limit`。  
你必须根据 `limit` 将 `message` 拆分成一个或多个部分（parts）。每个生成的部分都需要带有后缀 `<a/b>`，其中 `b` 替换为总的部分数，`a` 替换为该部分的序号（从 1 开始，到 `b` 结束）。此外，每个生成的部分（包括后缀）的长度必须等于 `limit`，**最后一部分**的长度可以不超过 `limit`。  

生成的各部分必须满足：去掉后缀后，将它们按顺序连接（concatenated）得到的字符串恰好等于 `message`。同时，拆分得到的部分数应尽可能少。  

返回一个字符串数组（array of strings），其中每个元素是拆分后得到的部分。如果无法按要求拆分，则返回空数组。

## 示例

### 示例 1

**输入**  
```json
message = "this is really a very awesome message"
limit = 9
```

**输出**  
```json
["thi<1/14>","s i<2/14>","s r<3/14>","eal<4/14>","ly <5/14>","a v<6/14>","ery<7/14>"," aw<8/14>","eso<9/14>","me<10/14>"," m<11/14>","es<12/14>","sa<13/14>","ge<14/14>"]
```

**解释**  
前 9 个部分每次从 `message` 的开头取 3 个字符。  
接下来的 5 个部分每次取 2 个字符，完成对 `message` 的拆分。

### 示例 2

**输入**  
```json
message = "short message"
limit = 15
```

**输出**  
```json
["short mess<1/2>","age<2/2>"]
```

**解释**  
在给定的限制下，字符串可以拆分成两部分：  
- 第 1 部分由前 10 个字符组成，长度为 15。  
- 第 2 部分由剩余的 3 个字符组成，长度为 8。

## 约束条件

- `1 <= message.length <= 10^4`
- `message` 仅由小写英文字母和空格 `' '` 构成
- `1 <= limit <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的总段数 `b`（从 1 到 `len(message)`）都枚举一遍**，  
对每一个 `b`：

1. 先算出后缀 `"<a/b>"` 的长度。  
   - `a` 和 `b` 都是整数，写成字符串后再拼接上字符 `<`、`/`、`>`。  
   - 这一步可以类比为 **查字典**：字典里每一页都有页码（`b`），我们要先知道页码有几位数，才能算出整本书的页眉占多大空间。  
2. 用 `limit - suffix_len` 计算出 **每一段能放多少真正的消息字符**。  
3. 把原始 `message` 按照这个字符数依次切分，看看能否恰好用完所有字符且段数正好是 `b`。  

如果可以，就把切好的每段加上对应的后缀返回；如果遍历完都找不到合法的 `b`，说明任务不可能完成，返回空列表 `[]`。

**为什么一定能找到答案（如果存在的话）？**  
因为我们把所有可能的 `b` 都尝试了，只要有一种 `b` 能满足 “每段长度 ≤ limit 且最后一段 ≤ limit” 这个条件，就一定会在枚举过程中被发现。

**时间/空间复杂度**  
- 我们最多枚举 `len(message)` 次（最坏情况下 `message` 长度是 10⁴），每次都要 **遍历一次完整的字符串** 来模拟切分。  
- 所以时间复杂度是 **O(n²)**，这里的 `n` 就是消息的长度。  
  - “O(n²)” 可以理解为：如果 `n = 10⁴`，算法大约要做 10⁴ × 10⁴ = 1 亿次基本操作，已经很慢了。  
- 额外使用的空间只是一小段用于存放临时字符串，**O(1)**（不计输出数组）。

#### 代码（Python）

```python
def splitMessage_bruteforce(message: str, limit: int):
    n = len(message)

    # 枚举所有可能的总段数 b
    for b in range(1, n + 1):
        # 计算后缀的最大长度：a 最多有和 b 同样的位数
        suffix_len = len(str(b)) * 2 + 3          # "<a/b>"
        if suffix_len > limit:                    # 后缀本身已经超出 limit，后面的 b 都不可能
            break

        # 每段实际能放的字符数（会随 a 的位数变化，这里先取最保守的最大后缀长度）
        content_len = limit - suffix_len
        if content_len <= 0:                      # 没有空间放消息字符
            continue

        # 按 content_len 把 message 切成若干段
        parts = []
        pos = 0
        for i in range(1, b + 1):
            # 当前段的后缀（a 的位数可能比 b 少，但这不会让后缀更长）
            suffix = f"<{i}/{b}>"
            cur_len = limit - len(suffix)        # 本段实际能放的字符数
            part = message[pos:pos + cur_len] + suffix
            parts.append(part)
            pos += cur_len

        # 检查是否正好用了完所有字符
        if pos == n:
            return parts

    # 没有任何合法的划分
    return []
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 枚举 `b`（最多 `n` 次）并在每次里遍历整个 `message`（`n` 次）。  
- **空间复杂度**：`O(1)`（不计输出列表）。  
  - 这里的 `O(1)` 表示我们只用了常数级别的临时变量；输出本身当然需要 `O(n)` 空间来保存结果。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **对每一个可能的 `b` 都去完整遍历一次字符串**。  
实际上我们只需要 **判断一个 `b` 是否可行**，不必真的切出每段来验证。  
如果能够用数学公式直接算出需要的段数，就可以把枚举过程变成 **二分查找**，从而把时间从 `O(n²)` 降到 `O(n log n)`。

下面一步步推导出这个快速判定方法：

1. **后缀长度的上界**  
   - 对于任意段 `i`，后缀形式是 `"<i/b>"`。  
   - `i` 的位数 ≤ `b` 的位数（因为 `i ≤ b`），所以后缀最长时的长度是  
     `len(str(b)) + len(str(b)) + 3`（两个数字的位数，加上字符 `<`、`/`、`>`）。  
   - 把它记作 `suffix_len(b)`。  
   - 如果 `suffix_len(b) > limit`，说明 **连后缀都装不下**，更大的 `b` 只会让后缀更长，直接不可能。

2. **每段能放多少真实字符**  
   - 给定 `b`，每段实际可用的字符数是 `limit - suffix_len(b)`（这里用了上界，保守但足够）。  
   - 记作 `content_len(b)`。如果 `content_len(b) ≤ 0`，说明根本没有空间放消息字符，直接不行。

3. **需要的最少段数**  
   - 整条消息长度为 `n = len(message)`。  
   - 用 `content_len(b)` 把它切成若干段，最少需要的段数是  
     ```
     need = ceil(n / content_len(b))
          = (n + content_len(b) - 1) // content_len(b)   # 整数除法写法
     ```
   - 如果 `need ≤ b`，说明 **我们可以在不超过 `b` 段的情况下装完消息**。  
     - 因为我们在二分查找的过程中总是寻找 **最小的**合法 `b`，最终得到的 `b` 正好等于 `need`，这样每段（除了最后一段）恰好填满 `limit`，最后一段 ≤ `limit`。

4. **二分搜索**  
   - `b` 的取值范围是 `[1, n]`（不可能比字符数更多段）。  
   - 使用二分搜索找最左侧满足 `need ≤ b` 的 `b`。  
   - 每一次检查只需要常数时间（算后缀长度、content_len、need），所以整体是 `O(log n)` 次检查。

5. **真正构造答案**  
   - 确定了最小合法的 `b` 后，按照真实的后缀长度（`len(str(i))` 可能小于 `len(str(b))`）逐段取字符并拼接后缀。  
   - 这样得到的每段 **恰好** 长度为 `limit`（除最后一段 ≤ `limit`），并且拼起来等于原始 `message`。

**类比**：  
把整个任务想象成把一本书（`message`）装进若干个统一大小的盒子（`limit`），每个盒子还要贴上标签 `"<i/b>"`。  
我们先估算出 **标签占多大空间**，再算出 **每个盒子还能装多少文字**，最后看 **需要多少盒子**。如果盒子数够用，就可以把书装进去；否则就换更大的盒子数再试。

#### 代码（Python）

```python
import math
from typing import List

def splitMessage(message: str, limit: int) -> List[str]:
    n = len(message)

    # ---------- 1. 判定函数：给定总段数 b，能否完成切分 ----------
    def can_split(b: int) -> bool:
        # 后缀最长可能的长度："<a/b>"，a 的位数最多和 b 一样多
        suffix_len = len(str(b)) * 2 + 3          # 3 个固定字符 < / >
        if suffix_len > limit:                    # 甚至装不下后缀
            return False
        content_len = limit - suffix_len          # 每段最多放多少真实字符
        if content_len <= 0:                      # 没有空间放消息
            return False
        # 需要的最少段数
        need = (n + content_len - 1) // content_len
        return need <= b

    # ---------- 2. 二分搜索最小合法的 b ----------
    lo, hi = 1, n
    answer_b = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if can_split(mid):
            answer_b = mid          # 记下可能的答案，继续往左找更小的
            hi = mid - 1
        else:
            lo = mid + 1

    # 如果根本没有合法的 b，直接返回空列表
    if answer_b == -1:
        return []

    b = answer_b

    # ---------- 3. 真正构造每一段 ----------
    parts = []
    pos = 0
    for i in range(1, b + 1):
        suffix = f"<{i}/{b}>"
        cur_len = limit - len(suffix)          # 本段实际能放的字符数
        # 取出对应的子串（可能为空）
        part_body = message[pos:pos + cur_len]
        parts.append(part_body + suffix)
        pos += cur_len

    # 检查一下是否正好用了完所有字符（理论上一定成立）
    if pos != n:
        # 说明我们的 b 估算有误，返回空列表以防万一
        return []

    return parts
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 二分搜索需要 `log n` 次判定，每次判定只做常数次算术运算。  
  - 构造答案时遍历一次 `message`，是 `O(n)`。  
  - 综合来看主导因素是 `log n` 次检查 + 一次线性遍历 → `O(n log n)`。  
  - 与暴力的 `O(n²)` 相比，**当 `n` 达到 10⁴ 时，运算次数从 1 亿下降到几千，快了好几个数量级**。

- **空间复杂度**：`O(n)`  
  - 需要存放返回的分段列表，长度正好等于原始字符串的字符数（每个字符最终都会出现在某个段里）。  
  - 除了输出本身，额外使用的变量都是常数级别的 `O(1)`。

---

## 心得  

- **核心技巧**：**先估算后缀占用的空间，再用整数除法求最少段数，配合二分搜索找到最小合法的段数**。  
- 这类“**先算出约束，再二分/枚举**”的思路在很多字符串切分、分页、装箱类题目里都很常见。  
  1. **`Split Array Largest Sum`**（把数组切成若干段，使每段和不超过阈值）  
  2. **`Minimum Number of Days to Make m Bouquets`**（二分答案）  
  3. **`Find Minimum Possible Integer After Rearranging Digits`**（同样先算位数约束）  
- **一句话总结**：**把后缀长度视作固定的“盒子空余”，先算出最少盒子数，再二分找最小可行值**。

---

## 反思  

- **第一反应**：看到“每段都要有 `<a/b>` 后缀”，本能想到把后缀的长度算进去，然后把剩余空间平分。  
- **最容易踩的坑**  
  1. **后缀长度会随 `a` 位数变化**：最保守的做法是使用 `b` 的位数来上界，这样可以一次性判断。  
  2. **最后一段可以短于 `limit`，但前面的段必须恰好等于 `limit`**：构造时一定要用实际的后缀长度来决定每段取多少字符。  
  3. **`suffix_len > limit` 的情况**：必须提前返回空数组，否则二分会陷入无限循环。  
- **下次遇到类似题**：第一步先 **“把所有固定的占用（标签、分隔符、页眉等）抽象成长度”，再用 **“总长度 ÷ 可用长度 = 最少块数”** 的公式快速判断可行性，必要时再二分或枚举块数。这样可以把原本的指数级搜索压缩到对数级或常数级。