# #2231. 奇偶位数字交换后的最大数 / Largest Number After Digit Swaps by Parity

> 难度：简单 · 标签：Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/largest-number-after-digit-swaps-by-parity/)

---

## 题目（英文原版）

**Description**

You are given a positive integer num. You may swap any two digits of num that have the same parity (i.e. both odd digits or both even digits).
Return the largest possible value of num after any number of swaps.

**Examples**

**Example 1:**

```
Input: num = 1234
Output: 3412
Explanation: Swap the digit 3 with the digit 1, this results in the number 3214.
Swap the digit 2 with the digit 4, this results in the number 3412.
Note that there may be other sequences of swaps but it can be shown that 3412 is the largest possible number.
Also note that we may not swap the digit 4 with the digit 1 since they are of different parities.
```

**Example 2:**

```
Input: num = 65875
Output: 87655
Explanation: Swap the digit 8 with the digit 6, this results in the number 85675.
Swap the first digit 5 with the digit 7, this results in the number 87655.
Note that there may be other sequences of swaps but it can be shown that 87655 is the largest possible number.
```

**Constraints**

- 1 <= num <= 109

---

## 题目（中文翻译）

给定一个正整数 `num`。你可以交换 `num` 中任意两个奇偶性相同的数字（即两个都是奇数或两个都是偶数）。  
返回经过任意次数交换后能够得到的最大可能值。

**示例 1**  
**输入**: `num = 1234`  
**输出**: `3412`  
**解释**: 先将数字 `3` 与数字 `1` 交换，得到 `3214`。  
随后将数字 `2` 与数字 `4` 交换，得到 `3412`。  
可以证明，虽然可能存在其他交换序列，但 `3412` 已是能够得到的最大数。  
需要注意的是，数字 `4` 与数字 `1` 不能交换，因为它们的奇偶性不同。

**示例 2**  
**输入**: `num = 65875`  
**输出**: `87655`  
**解释**: 先将数字 `8` 与数字 `6` 交换，得到 `85675`。  
随后将第一个数字 `5` 与数字 `7` 交换，得到 `87655`。  
同样可以证明，虽然可能存在其他交换序列，但 `87655` 已是能够得到的最大数。

**约束条件**  
- `1 <= num <= 10^9`   (即 `num` 至多为十位数的正整数)

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**把所有可以交换的偶数位和奇数位的数字两两尝试一下**，把得到的每一个新数字都和当前的最大值比较，最后留下最大的那个。  

- **使用的数据结构**：  
  - 把整数 `num` 转成字符数组 `digits`（相当于把数字拆成一串“珠子”）。  
  - 两层循环遍历每一对下标 `(i, j)`，如果 `digits[i]` 与 `digits[j]` 同奇偶（都为奇数或都为偶数），就交换它们得到一个新数组。  
  - 把新数组再拼成整数，和当前的最大值 `best` 做比较。  

> **类比**：把数字想成一本词典，查找同奇偶的两个词（数字）并把它们的页码互换，就像把词典里两个相同词性的词调换位置，看看能否得到更“大”的词典序。

- **为什么正确**：只要遍历了**所有**可能的合法交换（包括不交换的情况），就一定会看到最大可达的数字。因为题目只要求“任意次数的合法交换”，只要我们把每一次合法的交换都尝试一次，最终的最大值一定会被捕获。

- **时间/空间复杂度**：  
  - 外层 `n` 次，内层最多 `n` 次（`n` 为数字位数），每次交换后再把数组转成整数，整体是 **O(n²)**。  
    - “O(n²)” 可以想象成：如果有 5 位数字，就要检查 5×5=25 次；位数越多，检查次数呈平方增长。  
  - 只用了原始数组和几个临时变量，**O(1)** 额外空间（不计输入本身）。

#### 代码（Python）

```python
def largestNumber_bruteforce(num: int) -> int:
    # 把整数拆成字符列表，方便交换
    digits = list(str(num))
    n = len(digits)

    # 记录当前找到的最大数字，先设为原始数字
    best = num

    # 两层循环遍历所有下标对 (i, j)
    for i in range(n):
        for j in range(i + 1, n):
            # 判断奇偶是否相同：奇数 % 2 == 1，偶数 % 2 == 0
            if (int(digits[i]) % 2) == (int(digits[j]) % 2):
                # 交换 i、j 位置的字符
                digits[i], digits[j] = digits[j], digits[i]

                # 把交换后的字符列表拼成整数
                candidate = int(''.join(digits))
                # 更新最大值
                if candidate > best:
                    best = candidate

                # 交换回来，恢复原状，继续尝试别的组合
                digits[i], digits[j] = digits[j], digits[i]

    return best
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：如果数字有 9 位（上限），最多要检查 9×9/2≈40 次交换，随着位数增长，检查次数呈二次方增长。  

- **空间复杂度**：`O(1)`（不计输入字符数组）  
  - 只用了常数个临时变量来保存交换后的数字。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于重复地尝试所有可能的交换**。其实我们并不需要枚举每一种交换，而只需要把每一种**奇数位**和**偶数位**的数字按照从大到小的顺序重新安排一次即可。  

**关键观察**  
1. **左边的位贡献更大**：在十进制中，千位比百位对整体数值的影响大 10 倍。于是我们希望把“大的数字”放在尽可能靠左的位置。  
2. **奇偶不能混**：奇数只能和奇数换，偶数只能和偶数换。这相当于把所有奇数分到一个“奇数池”，所有偶数分到一个“偶数池”。  
3. **每个池内部独立排序**：在奇数池里，把最大的奇数放在最左边的奇数位置；在偶数池里，把最大的偶数放在最左边的偶数位置。这样既满足奇偶限制，又让每个位置的数字尽可能大。  

**实现步骤**  

| 步骤 | 说明 |
|------|------|
| 1️⃣ 把 `num` 转成字符列表 `digits` | 方便逐位检查奇偶性 |
| 2️⃣ 收集奇数和偶数到两个列表 `odd`、`even` | 类似把奇数和偶数装进两个抽屉 |
| 3️⃣ 分别对 `odd`、`even` 降序排序 | 把“大数字”排在前面 |
| 4️⃣ 再次遍历原始位置，用已经排好序的列表依次填回 | 先填左边的奇数位，再填左边的偶数位，保证每个位置拿到当前池里最大的剩余数字 |
| 5️⃣ 把最终字符列表拼成整数返回 | 完成 |  

**为什么最优**  
- 排序一次就得到所有奇数/偶数的全局顺序，之后只做一次线性遍历填充，**不需要再尝试任意次数的交换**。  
- 时间主要花在排序上，排序的复杂度是 `O(k log k)`，其中 `k` 为对应池的大小。`k ≤ n`，所以整体是 `O(n log n)`。  
- 只用了几个额外列表保存奇数、偶数，空间是 `O(n)`（存放排好序的数字），已经是最小需要的空间。

#### 代码（Python）

```python
def largestNumber(num: int) -> int:
    # 1. 拆成字符列表，方便逐位处理
    digits = list(str(num))
    n = len(digits)

    # 2. 收集奇数和偶数
    odd = []   # 奇数池
    even = []  # 偶数池
    for ch in digits:
        d = int(ch)
        if d % 2:          # 奇数
            odd.append(ch)
        else:              # 偶数
            even.append(ch)

    # 3. 降序排列（大的在前面），因为字符 '9' > '8' ...，直接排序即可
    odd.sort(reverse=True)
    even.sort(reverse=True)

    # 4. 重新构造答案
    # 使用两个指针分别指向 odd / even 列表的当前位置
    odd_idx, even_idx = 0, 0
    for i in range(n):
        d = int(digits[i])
        if d % 2:                 # 原来是奇数位，需要从 odd 池取最大剩余奇数
            digits[i] = odd[odd_idx]
            odd_idx += 1
        else:                     # 原来是偶数位，从 even 池取最大剩余偶数
            digits[i] = even[even_idx]
            even_idx += 1

    # 5. 把字符列表拼回整数并返回
    return int(''.join(digits))
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - `n` 为数字位数（最多 10 位，因为 `num ≤ 10⁹`）。  
  - 解释：我们对奇数池和偶数池各做一次排序，排序的代价是 `k log k`，`k ≤ n`，所以整体是 `n log n`。相较于暴力的 `n²`，在位数稍大时会快很多。  

- **空间复杂度**：`O(n)`  
  - 需要额外的两个列表保存奇数和偶数，最坏情况下占用与原始数字同等的空间（比如全部都是奇数）。这已经是不可避免的，因为我们必须记住每个奇偶池里剩余的数字。  

---  

## 心得  

- **核心技巧**：**同类（奇数/偶数）内部排序 + 贪心填位**。  
- **适用的题型**：  
  1. “只能在满足某种属性的元素之间交换” 类问题（例如只能在相同颜色的球之间调换位置）。  
  2. “把数字重新排列使结果最大/最小”，但受限于子集的约束（如只能在奇数位或偶数位调换）。  
  3. “分组后各自排序再合并”，如把字母按大小写分组后各自排序。  
- **一句话总结解题钥匙**：**把可以自由调换的元素先收集、排序，然后按原位置的约束贪心填回去**。  

---  

## 反思  

- **第一反应**：看到“只能在相同奇偶的数字之间交换”，立刻想到“把奇数和偶数分别拿出来，分别排个序”。  
- **最容易踩的坑**：  
  - **忘记保持原来奇偶位的顺序**：不能把奇数放到原本是偶数的位置，必须在遍历时检查当前位的奇偶性再决定取哪个池的数字。  
  - **边界情况**：全是奇数或全是偶数时，排序后直接填回即可，代码仍需正常工作。  
  - **字符串与整数的转换**：`int('')` 会报错，确保列表非空后再取元素。  
- **下次遇到同类题**，第一步应该**把所有可以自由调换的元素收集进各自的容器**，随后**对每个容器内部做排序**，最后**按原位置的限制贪心填回**。这样既简洁又高效。