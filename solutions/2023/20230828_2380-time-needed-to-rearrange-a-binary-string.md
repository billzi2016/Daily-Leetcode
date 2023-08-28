# #2380. **二进制字符串重排所需时间** / Time Needed to Rearrange a Binary String

> 难度：中等 · 标签：String、Dynamic Programming、Simulation · [LeetCode 链接](https://leetcode.com/problems/time-needed-to-rearrange-a-binary-string/)

---

## 题目（英文原版）

**Description**

You are given a binary string s. In one second, all occurrences of "01" are simultaneously replaced with "10". This process repeats until no occurrences of "01" exist.
Return the number of seconds needed to complete this process.
Follow up:
Can you solve this problem in O(n) time complexity?

**Examples**

**Example 1:**

```
Input: s = "0110101"
Output: 4
Explanation: 
After one second, s becomes "1011010".
After another second, s becomes "1101100".
After the third second, s becomes "1110100".
After the fourth second, s becomes "1111000".
No occurrence of "01" exists any longer, and the process needed 4 seconds to complete,
so we return 4.
```

**Example 2:**

```
Input: s = "11100"
Output: 0
Explanation:
No occurrence of "01" exists in s, and the processes needed 0 seconds to complete,
so we return 0.
```

**Constraints**

- 1 <= s.length <= 1000
- s[i] is either '0' or '1'.

---

## 题目（中文翻译）

给定一个二进制字符串 `s`。在一秒钟内，所有出现的 `"01"` 同时被替换为 `"10"`（即一次并行的子串交换）。该过程会一直重复，直到字符串中不再出现 `"01"` 为止。  
返回完成整个过程所需要的秒数。

**示例 1**

```text
Input: s = "0110101"
Output: 4
Explanation: 
- 第 1 秒后，s 变为 "1011010"。
- 第 2 秒后，s 变为 "1101100"。
- 第 3 秒后，s 变为 "1110100"。
- 第 4 秒后，s 变为 "1111000"。
此时字符串中已不存在 `"01"`，整个过程共用了 4 秒，所以返回 4。
```

**示例 2**

```text
Input: s = "11100"
Output: 0
Explanation:
字符串中本就不存在 `"01"`，因此过程不需要任何时间，返回 0。
```

**约束条件**

- `1 <= s.length <= 1000`
- `s[i]` 只能是 `'0'` 或 `'1'`。

**进阶**

能否在 `O(n)` 时间复杂度内完成此题？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **严格按照题目描述** 来模拟每一秒钟的变化：

1. 从左到右扫描字符串，找出所有子串 `"01"` 的起始位置。  
2. 记下这些位置后，**同时** 把这些 `"01"` 替换成 `"10"`（一次性完成，不能把已经改成的 `10` 再继续参与本轮替换）。  
3. 只要在一次扫描中找到了至少一个 `"01"`，就说明还有后续的秒数，继续进入下一轮循环。  

> **类比**：把字符串想象成一条装满小球的传送带，`0` 是蓝球，`1` 是红球。每秒钟所有相邻的蓝‑红组合（蓝在左、红在右）都会一起交换位置，变成红‑蓝。我们只需要一次性把所有需要交换的对记下来，然后统一执行。

只要把上面三步循环执行，就一定会得到最终没有 `"01"` 的状态，循环的次数就是答案。

#### 代码（Python）

```python
def secondsToRemoveOccurrences_bruteforce(s: str) -> int:
    # 将字符串转成列表，列表的修改更方便
    arr = list(s)
    n = len(arr)
    seconds = 0

    while True:
        # 第一步：找出本轮所有 "01" 的左端下标
        pos = []                         # 用来存放需要交换的下标
        i = 0
        while i < n - 1:
            if arr[i] == '0' and arr[i + 1] == '1':
                pos.append(i)            # 记录左端位置
                i += 2                   # 跳过这两个字符，防止重叠计数
            else:
                i += 1

        # 没有找到 "01" 说明已经完成
        if not pos:
            break

        # 第二步：一次性把所有记录的位置做 "01" → "10" 的替换
        for p in pos:
            arr[p], arr[p + 1] = '1', '0'

        seconds += 1                    # 完成一秒

    return seconds
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  每一次循环我们都要遍历整个字符串（`O(n)`），而最坏情况下需要进行 `O(n)` 次循环（比如 `"000...0111...1"`，每次只能把最左边的 `0` 往右推一步），所以总共是 `n × n`，即 `O(n²)`。  
  用大白话说，就是如果字符串长度是 1000，最慢可能要跑 1 000 × 1 000 = 1 000 000 次基本操作。

- **空间复杂度**：`O(n)`  
  需要一个字符列表来存放字符串（`O(n)`），以及临时的 `pos` 列表，最坏也不过是 `O(n)`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**一次只让相邻的 `0` 向右移动一步**，于是需要多轮才能把所有 `0` 推到最右侧。我们需要从宏观上观察每个 `0` 最终要走多远，而不必一步一步地模拟。

**关键观察**：

- 只要左边有 `1`，`0` 就会被“推动”向右。  
- 对于某个 `0`，它需要的时间等于它左边**比它更靠左的所有 `1` 的数量**，但还有一个细节：如果左边已经有其他 `0` 正在向右跑，这些 `0` 会形成“队列”，后面的 `0` 必须等前面的 `0` 把它的 `1` “清空”后才能继续前进。

换句话说，遍历字符串时维护两个状态：

1. `ones`：到当前位置为止出现的 `1` 的总数。它代表了这段左侧已经准备好的“推动力”。  
2. `seconds`：当前已经需要的总秒数（即答案的上界）。当我们遇到一个 `0` 时，如果它左边已经有 `1`（`ones > 0`），这个 `0` 必须至少再等 `seconds + 1` 秒才能完成交换——因为它要排在之前的所有 `0` 之后。

于是我们可以 **一次遍历** 完成计算：

```
遍历字符 c:
    if c == '1':   ones += 1
    else:          # c == '0'
        if ones > 0:               # 左边有 1，需要移动
            # 这颗 0 至少要等 seconds+1 秒才能和左边的所有 1 交换完
            seconds = max(seconds + 1, ones)
```

- `seconds + 1` 表示在已有的时间基础上再多等一步，让这颗 `0` 排在队尾。
- `ones` 表示如果左边的 `1` 比当前累计的 `seconds` 更多，`0` 必须等到所有 `1` 都能向右搬运完，也就是直接取 `ones`。

遍历结束后，`seconds` 就是整个过程所需的秒数。

> **类比**：把所有 `1` 想象成向右跑的“推手”，每个 `0` 是需要被推的“箱子”。箱子只能排队，一个箱子推完后，下一个箱子才能继续推。`seconds` 记录的是队列的最长等待时间。

#### 代码（Python）

```python
def secondsToRemoveOccurrences_opt(s: str) -> int:
    ones = 0        # 左侧已经出现的 '1' 的数量
    seconds = 0     # 迄今为止需要的最大秒数

    for ch in s:
        if ch == '1':
            ones += 1                     # 记录新的推动力
        else:  # ch == '0'
            if ones > 0:                  # 只有左边有 1 时才需要移动
                # 当前 0 必须等比之前更长的时间
                #   1) 前面已有的秒数 + 1（排到队尾）
                #   2) 左侧 1 的总数（如果 1 还很多，需要更久）
                seconds = max(seconds + 1, ones)

    return seconds
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历一次字符串，`n` 为字符串长度。相比暴力的 `O(n²)`，速度提升了一个数量级。  
  用大白话说：如果长度是 1000，只需要大约 1000 次基本操作，就能算出答案。

- **空间复杂度**：`O(1)`  
  只用了几个整数变量，和输入大小无关。

---

## 心得

- 这道题的核心技巧是 **把“同步替换”抽象为“0 向右移动的等待时间”**，利用**计数 + 取最大**的方式一次遍历完成。
- 该技巧适用于类似的“局部交换会产生全局延迟”问题，例如  
  1. **`Minimum Seconds to Make All the Same`**（把不同字符同步变成相同）  
  2. **`Array K-Increments`**（每次同时把相邻的 `a[i] < a[i+1]` 变大）  
  3. **`Moving Stones Until No Consecutive Pair`**（石子向右移动的最小步数）  
- **解题钥匙**：把一次性“所有相邻 01 同时变 10”转化为 **每个 0 需要等多少秒**，用**计数 + 取最大**完成 O(n) 求解。

---

## 反思

- **第一反应**：直接写循环模拟，像暴力解那样一步一步改字符串。  
- **最容易踩的坑**：  
  - 忘记 **同步** 替换的要求，导致在同一轮中把已经换好的 `10` 再次当作 `01` 处理。  
  - 对于最左侧的 `0`，如果左边没有 `1`，不需要计时，容易误把所有 `0` 都加上 `seconds+1`。  
  - 边界情况如全 `1`、全 `0` 或者只有一个字符时，都应该直接返回 `0`。  
- **下次遇到同类题**：第一步先 **思考每个元素需要“排队”等多久**，尝试把整体过程抽象为**计数 + 最大等待时间**，再决定是暴力模拟还是 O(n) 直接求解。