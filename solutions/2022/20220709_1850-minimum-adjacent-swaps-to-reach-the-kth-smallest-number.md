# #1850. 最少相邻交换次数以获得第 K 小的奇妙整数 / Minimum Adjacent Swaps to Reach the Kth Smallest Number

> 难度：中等 · 标签：Two Pointers、String、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-adjacent-swaps-to-reach-the-kth-smallest-number/)

---

## 题目（英文原版）

**Description**

You are given a string num, representing a large integer, and an integer k.
We call some integer wonderful if it is a permutation of the digits in num and is greater in value than num. There can be many wonderful integers. However, we only care about the smallest-valued ones.
Return the minimum number of adjacent digit swaps that needs to be applied to num to reach the kth smallest wonderful integer.
The tests are generated in such a way that kth smallest wonderful integer exists.

**Examples**

**Example 1:**

```
Input: num = "5489355142", k = 4
Output: 2
Explanation: The 4th smallest wonderful number is "5489355421". To get this number:
- Swap index 7 with index 8: "5489355142" -> "5489355412"
- Swap index 8 with index 9: "5489355412" -> "5489355421"
```

**Example 2:**

```
Input: num = "11112", k = 4
Output: 4
Explanation: The 4th smallest wonderful number is "21111". To get this number:
- Swap index 3 with index 4: "11112" -> "11121"
- Swap index 2 with index 3: "11121" -> "11211"
- Swap index 1 with index 2: "11211" -> "12111"
- Swap index 0 with index 1: "12111" -> "21111"
```

**Example 3:**

```
Input: num = "00123", k = 1
Output: 1
Explanation: The 1st smallest wonderful number is "00132". To get this number:
- Swap index 3 with index 4: "00123" -> "00132"
```

**Constraints**

- 2 <= num.length <= 1000
- 1 <= k <= 1000
- num only consists of digits.

---

## 题目（中文翻译）

给定一个字符串 `num`，表示一个大整数，以及一个整数 `k`。  
我们称某个整数为 **奇妙整数（wonderful integer）**，如果它是 `num` 中数字的一个全排列，并且数值大于 `num`。可能存在许多奇妙整数，但我们只关心数值最小的那些。  

返回将 `num` 通过相邻数字交换得到第 `k` 小的奇妙整数所需的最少交换次数。  
测试数据保证第 `k` 小的奇妙整数一定存在。

**示例 1**  

**示例 2**  

**示例 3**  

**约束条件**

- `2 <= num.length <= 1000`
- `1 <= k <= 1000`
- `num` 仅由数字组成  

---

### 示例

#### 示例 1
```text
Input: num = "5489355142", k = 4
Output: 2
Explanation: 第 4 小的奇妙整数是 "5489355421"。得到该整数的过程如下：
- 交换下标 7 与下标 8： "5489355142" → "5489355412"
- 交换下标 8 与下标 9： "5489355412" → "5489355421"
```

#### 示例 2
```text
Input: num = "11112", k = 4
Output: 4
Explanation: 第 4 小的奇妙整数是 "21111"。得到该整数的过程如下：
- 交换下标 3 与下标 4： "11112" → "11121"
- 交换下标 2 与下标 3： "11121" → "11211"
- 交换下标 1 与下标 2： "11211" → "12111"
- 交换下标 0 与下标 1： "12111" → "21111"
```

#### 示例 3
```text
Input: num = "00123", k = 1
Output: 1
Explanation: 第 1 小的奇妙整数是 "00132"。得到该整数的过程如下：
- 交换下标 3 与下标 4： "00123" → "00132"
```

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

1️⃣ **求第 k 个「更大的」排列**  
把 `num` 看成一串数字。  
「比 `num` 大的最小排列」恰好就是 **字典序的下一个排列**（next permutation）。  
所以「第 k 个更大的排列」= 「对 `num` 连续调用 `next_permutation` k 次」的结果。  

> **类比**：想象一本字典，`num` 就是一本单词。要找比它大的下一个单词，只要把后面的字母往前调一点点，就是「下一个排列」；再调一次、再调一次… 连调 k 次就得到第 k 个更大的单词。

2️⃣ **计算最少相邻交换次数**  
得到目标字符串 `target` 后，需要把原始字符串 `num` 通过 **相邻交换**（一次只能把相邻的两个字符位置互换）变成 `target`。  
最直接的办法是 **模拟**：从左到右逐位比较：

- 第 `i` 位如果已经相同，直接继续。
- 否则，在 `num` 的后面（`i+1 … n-1`）找第一个等于 `target[i]` 的字符，记它的位置为 `j`。
- 把这个字符一步一步左移到位置 `i`，每左移一次就相当于一次相邻交换，交换次数累加 `j-i`。

> **类比**：把一排排好队的学生重新排成另一种顺序，只能让相邻的两个学生互换位置。我们从左边开始，让正确的学生一步步走到该站的位置，走几格就要换几次。

**为什么这样一定得到最少交换次数？**  
因为相邻交换的代价只和「一个字符要向左走多少格」有关，而不影响其它已经排好的位置。我们每次都把最左侧不匹配的字符尽可能左移到它该去的地方，已经排好的左侧部分永远不被打乱，所以这就是最优的。

#### 代码（Python）

```python
def next_permutation(s: list) -> None:
    """
    原地把列表 s 变成字典序的下一个排列。
    思路：从右往左找到第一次下降的地方 i，
          再在 i 右侧找到比 s[i] 大且最小的元素 j，交换后把 i 右侧逆序。
    """
    n = len(s)
    # 1. 找到下降点 i
    i = n - 2
    while i >= 0 and s[i] >= s[i + 1]:
        i -= 1
    if i < 0:                     # 已经是最大排列，直接逆序得到最小排列
        s.reverse()
        return

    # 2. 在 i 右侧找第一个比 s[i] 大的元素 j（从右往左找第一个即可）
    j = n - 1
    while s[j] <= s[i]:
        j -= 1
    # 3. 交换
    s[i], s[j] = s[j], s[i]
    # 4. 把 i 右侧逆序（因为原来是降序，逆序后变成升序）
    s[i + 1:] = reversed(s[i + 1:])


def get_kth_wonderful(num: str, k: int) -> str:
    """返回第 k 个更大的排列（即第 k 小的 wonderful number）"""
    s = list(num)
    for _ in range(k):
        next_permutation(s)
    return ''.join(s)


def min_adjacent_swaps(num: str, target: str) -> int:
    """计算把 num 变成 target 所需的最少相邻交换次数"""
    a = list(num)          # 工作副本，边模拟边计数
    n = len(a)
    swaps = 0

    for i in range(n):
        if a[i] == target[i]:
            continue                     # 已经匹配，无需操作
        # 在 i 右侧寻找第一个等于 target[i] 的位置 j
        j = i + 1
        while j < n and a[j] != target[i]:
            j += 1
        # 把 a[j] 左移到 i 位置，每左移一步计一次交换
        while j > i:
            a[j], a[j - 1] = a[j - 1], a[j]   # 交换相邻两个字符
            swaps += 1
            j -= 1
    return swaps


def get_min_swaps(num: str, k: int) -> int:
    """主函数：返回答案"""
    target = get_kth_wonderful(num, k)
    return min_adjacent_swaps(num, target)
```

#### 复杂度  

- **时间复杂度**  
  - 求第 k 个排列：每次 `next_permutation` 只遍历一次数组 → `O(n)`，共 `k` 次 → `O(k·n)`。  
  - 计算相邻交换次数：外层遍历 `n` 次，内层最坏要找 `j` 并左移 `j-i` 步，整体最多 `O(n²)`（因为每个字符最多被移动 `n` 次）。  
  - **总计** `O(k·n + n²)`。在本题约束（`n ≤ 1000, k ≤ 1000`）下完全可接受。  

- **空间复杂度**  
  - 只用了几个长度为 `n` 的列表副本 → `O(n)`。  

---

### 2. 最优解  

在本题的约束下，上面的「暴力」实现已经足够快，但我们仍可以把 **交换计数** 部分再提速到 `O(n log n)`，把整体时间降到 `O(k·n + n log n)`。核心思路是 **使用树状数组（Fenwick Tree）** 维护已经「移动」过的字符位置。

#### 思路  

1️⃣ **第 k 个排列**仍然使用 `next_permutation` 连续 k 次得到 `target`，这一步已经是最直接且最优的 `O(k·n)`。

2️⃣ **相邻交换次数的计数**  
   - 当我们把字符从位置 `j` 移到位置 `i`（`j > i`）时，实际交换的次数等于 **在原数组中从 i 到 j 之间还剩多少未被「固定」的字符**。  
   - 想象每个位置上有一个「标记」：未被固定的为 1，已经固定（已经移动到左边并不再参与后续移动）的为 0。  
   - 把 `j` 往左移动到 `i` 时，需要跨过的「1」的数量正好是我们要的交换次数。  

   这正好可以用 **树状数组**（Fenwick Tree）来维护前缀和：  
   - 初始化时，所有位置的值都是 1（代表「未固定」）。  
   - 当我们把某个字符固定在左边时，把它所在的下标对应的值设为 0（`add(idx, -1)`）。  
   - 对于一次移动，交换次数 = `query(j) - query(i)`（即区间 `[i, j]` 内的 1 的个数），随后把 `j` 位置设为 0（因为该字符已经被搬走），`i` 位置仍保持 1（后面还会继续使用）。  

3️⃣ **实现细节**  
   - 仍然需要把 `num` 按左到右的顺序与 `target` 对齐。我们遍历 `i = 0 … n-1`：  
        * 在 `num` 中找到与 `target[i]` 对应的最左侧未使用位置 `j`（可以用字典 `pos[digit]` 保存每个数字出现的下标队列）。  
        * 用树状数组求出 `j` 前面还有多少未被固定的字符，即 `swaps += fenwick.sum(j) - fenwick.sum(i)`。  
        * 把 `j` 标记为「已使用」：`fenwick.add(j, -1)`。  

   - 这样每次只做 `O(log n)` 的查询/更新，整体 `O(n log n)`。

> **类比**：想象有一排座位，座位上坐着人（1 表示有人，0 表示座位空）。我们每次把某个人从座位 `j` 拉到 `i`，需要跨过多少人就等于我们要换的次数。树状数组就像一个「快速统计」工具，能在瞬间告诉我们任意区间里还有多少人。

#### 代码（Python）

```python
class Fenwick:
    """树状数组（Binary Indexed Tree）实现前缀和"""
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)          # 1-indexed

    def add(self, idx: int, delta: int) -> None:
        """把 idx 位置的值加 delta（idx 为 0-indexed）"""
        i = idx + 1
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def sum(self, idx: int) -> int:
        """返回前缀和 sum[0..idx]（idx 为 0-indexed，若 idx<0 返回 0）"""
        if idx < 0:
            return 0
        i = idx + 1
        res = 0
        while i:
            res += self.bit[i]
            i -= i & -i
        return res


def get_kth_wonderful(num: str, k: int) -> str:
    """同上，只保留最简实现"""
    s = list(num)
    for _ in range(k):
        # ---- next_permutation ----
        i = len(s) - 2
        while i >= 0 and s[i] >= s[i + 1]:
            i -= 1
        if i >= 0:
            j = len(s) - 1
            while s[j] <= s[i]:
                j -= 1
            s[i], s[j] = s[j], s[i]
            s[i + 1:] = reversed(s[i + 1:])
        else:                 # 已经是最大排列，直接逆序得到最小排列
            s.reverse()
    return ''.join(s)


def min_swaps_fenwick(num: str, target: str) -> int:
    """利用 Fenwick 树在 O(n log n) 计算最少相邻交换次数"""
    n = len(num)
    # 为每个数字维护出现位置的队列（从左到右）
    from collections import deque, defaultdict
    pos = defaultdict(deque)
    for idx, ch in enumerate(num):
        pos[ch].append(idx)

    fenwick = Fenwick(n)
    for i in range(n):
        fenwick.add(i, 1)          # 初始全部为 1（未固定）

    swaps = 0
    for i in range(n):
        need = target[i]           # 目标位置 i 需要的字符
        j = pos[need].popleft()    # 该字符在原串中最左侧未使用的下标
        # 计算 j 前面还有多少未被固定的字符，即需要跨过的交换次数
        swaps += fenwick.sum(j) - fenwick.sum(i - 1)
        # 把 j 位置标记为已使用
        fenwick.add(j, -1)
    return swaps


def get_min_swaps(num: str, k: int) -> int:
    target = get_kth_wonderful(num, k)
    return min_swaps_fenwick(num, target)
```

#### 复杂度  

- **时间复杂度**  
  - 求第 k 个排列：`O(k·n)`（与暴力相同）。  
  - 计数交换次数：每个字符一次 `O(log n)` 的查询/更新 → `O(n log n)`。  
  - **总计** `O(k·n + n log n)`，在最坏情况下比 `O(k·n + n²)` 快很多，尤其当 `n` 接近 1000 时更明显。

- **空间复杂度**  
  - `pos`、Fenwick 树、若干临时列表共 `O(n)`。  

---

## 心得  

- **核心技巧**：  
  1. **next permutation**：一次遍历即可得到字典序的下一个排列。  
  2. **相邻交换计数**：从左到右模拟移动，或使用 **Fenwick 树** 把「跨过多少未固定字符」的查询降到 `O(log n)`。  

- **适用的题型**（可以套用同样思路）：  
  - 「求第 k 个更大的排列」类问题（如 LeetCode 31、556）。  
  - 「最少相邻交换将一个序列变成另一序列」的计数问题（如「Minimum Swaps to Make Strings Equal」）。  
  - 需要「从一个排列到另一个排列的距离」的场景，常用 **逆序对**（BIT）或 **线段树** 求解。  

- **一句话总结解题钥匙**：  
  *先用「字典序下一个排列」快速定位目标，再用「左移+前缀和」或「树状数组」精确统计跨越的相邻交换次数。*  

---

## 反思  

- **第一反应**：看到「第 k 个更大的数字」立刻想到「next permutation」；看到「相邻交换」想到「模拟左移」或「逆序对」。  
- **最容易踩的坑**  
  - `next_permutation` 实现错误（忘记把后缀逆序）。  
  - 当原串已经是最大排列时，需要先整体逆序得到最小排列再继续。  
  - 计数时忘记把已经使用的字符从「未固定」集合中剔除，导致重复计数。  
  - 处理前导零：题目允许出现前导零，直接按字符比较即可，不需要额外去掉。  

- **下次遇到同类题的第一步**：  
  *先明确「目标排列」怎么得到（next permutation / kth permutation），再决定「如何计数」——是直接模拟 O(n²) 还是用 BIT/线段树把计数降到 O(n log n)。*