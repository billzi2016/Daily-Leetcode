# #2513. **最小化两个数组的最大值** / Minimize the Maximum of Two Arrays

> 难度：中等 · 标签：Math、Binary Search、Number Theory · [LeetCode 链接](https://leetcode.com/problems/minimize-the-maximum-of-two-arrays/)

---

## 题目（英文原版）

**Description**

We have two arrays arr1 and arr2 which are initially empty. You need to add positive integers to them such that they satisfy all the following conditions:
Given divisor1, divisor2, uniqueCnt1, and uniqueCnt2, return the minimum possible maximum integer that can be present in either array.

**Examples**

**Example 1:**

```
Input: divisor1 = 2, divisor2 = 7, uniqueCnt1 = 1, uniqueCnt2 = 3
Output: 4
Explanation: 
We can distribute the first 4 natural numbers into arr1 and arr2.
arr1 = [1] and arr2 = [2,3,4].
We can see that both arrays satisfy all the conditions.
Since the maximum value is 4, we return it.
```

**Example 2:**

```
Input: divisor1 = 3, divisor2 = 5, uniqueCnt1 = 2, uniqueCnt2 = 1
Output: 3
Explanation: 
Here arr1 = [1,2], and arr2 = [3] satisfy all conditions.
Since the maximum value is 3, we return it.
```

**Example 3:**

```
Input: divisor1 = 2, divisor2 = 4, uniqueCnt1 = 8, uniqueCnt2 = 2
Output: 15
Explanation: 
Here, the final possible arrays can be arr1 = [1,3,5,7,9,11,13,15], and arr2 = [2,6].
It can be shown that it is not possible to obtain a lower maximum satisfying all conditions.
```

**Constraints**

- 2 <= divisor1, divisor2 <= 105
- 1 <= uniqueCnt1, uniqueCnt2 < 109
- 2 <= uniqueCnt1 + uniqueCnt2 <= 109

---

## 题目（中文翻译）

我们有两个数组 `arr1` 和 `arr2`，它们最初为空。需要向其中添加正整数，使得它们同时满足以下所有条件：

给定 `divisor1`、`divisor2`、`uniqueCnt1` 和 `uniqueCnt2`，返回两数组中可能出现的**最小的最大整数**。

---

**示例 1**  
**输入**: `divisor1 = 2, divisor2 = 7, uniqueCnt1 = 1, uniqueCnt2 = 3`  
**输出**: `4`  
**解释**:  
我们可以把前 4 个自然数分配到 `arr1` 和 `arr2` 中。  
`arr1 = [1]`，`arr2 = [2,3,4]`。  
可以看到两个数组都满足所有条件。  
由于最大值为 4，返回 4。

**示例 2**  
**输入**: `divisor1 = 3, divisor2 = 5, uniqueCnt1 = 2, uniqueCnt2 = 1`  
**输出**: `3`  
**解释**:  
此时 `arr1 = [1,2]`，`arr2 = [3]` 满足所有条件。  
最大值为 3，返回 3。

**示例 3**  
**输入**: `divisor1 = 2, divisor2 = 4, uniqueCnt1 = 8, uniqueCnt2 = 2`  
**输出**: `15`  
**解释**:  
最终可能的数组为 `arr1 = [1,3,5,7,9,11,13,15]`，`arr2 = [2,6]`。  
可以证明不存在满足条件且最大值更小的方案。

---

**约束条件**

- `2 ≤ divisor1, divisor2 ≤ 10^5`
- `1 ≤ uniqueCnt1, uniqueCnt2 < 10^9`
- `2 ≤ uniqueCnt1 + uniqueCnt2 ≤ 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**从 1 开始枚举自然数**，把它们一个一个放进两条数组，直到满足题目给出的四个条件：

1. `arr1` 中恰好有 `uniqueCnt1` 个**不被 `divisor1` 整除**的数。  
2. `arr2` 中恰好有 `unicodeCnt2` 个**不被 `divisor2` 整除**的数。  
3. 任何**能被 `divisor1` 整除的数**都不能放进 `arr1`（它只能放进 `arr2` 或者不放）。  
4. 任何**能被 `divisor2` 整除的数**都不能放进 `arr2`（它只能放进 `arr1` 或者不放）。  

把“不能放进某个数组”想象成**字典查不到对应的词**——如果一个数是 “禁止词”，我们只能把它丢进另一边的“字典”。  

我们不停往两个数组里塞数，直到两边的计数都达标。此时最大的数就是答案。

**为什么能得到正确答案？**  
因为我们把所有可能的正整数都按顺序尝试过了，只要有一种分配方式能满足条件，最先出现的那一次必然是最小的最大值。

**时间/空间分析（大白话）**  

- 时间复杂度：我们可能要遍历到答案本身的大小 `M`。如果答案是 `10^9`，就要循环十亿次，**时间是 O(M)**，在最坏情况下几乎不可接受。  
- 空间复杂度：只需要保存几个计数器和两个数组的大小，**O(1)**（不计数组本身的存储，因为我们只关心最大值）。

> **O(M) 的意义**：把 `M` 想成“一堆糖果”，每吃一颗糖果都要花一次时间，吃 `M` 颗糖果自然要 `M` 次时间。

#### 代码（Python）

```python
def minMaximum(divisor1: int, divisor2: int,
               uniqueCnt1: int, uniqueCnt2: int) -> int:
    # 记录已经放进 arr1 / arr2 的符合条件的数的个数
    cnt1 = cnt2 = 0
    num = 1                     # 从最小的正整数开始尝试

    while True:
        # 这颗糖果能否放进 arr1 ?
        if num % divisor1 != 0:        # 不是 divisor1 的倍数，就可以放进 arr1
            if cnt1 < uniqueCnt1:
                cnt1 += 1
                # 若两边都已经满足，就可以直接返回当前的最大数
                if cnt1 == uniqueCnt1 and cnt2 == uniqueCnt2:
                    return num
        # 这颗糖果能否放进 arr2 ?
        if num % divisor2 != 0:        # 不是 divisor2 的倍数，就可以放进 arr2
            if cnt2 < uniqueCnt2:
                cnt2 += 1
                if cnt1 == uniqueCnt1 and cnt2 == uniqueCnt2:
                    return num
        # 两边都不需要这颗数，或者已经满了，继续往后找
        num += 1
```

> 这段代码可以直接运行，但在数据量大时会超时。

#### 复杂度  

- **时间复杂度**：`O(M)`，其中 `M` 为答案本身的大小。  
- **空间复杂度**：`O(1)`，只用了常数个变量。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**逐个枚举**，当答案很大时会遍历太多数字。  
我们注意到：  

- 对于任意给定的上限 `mid`（假设我们已经决定最大数不超过 `mid`），只要能够在 `[1, mid]` 这段连续的自然数里**挑选出足够的合法数**，就说明答案 ≤ `mid`。  
- 于是可以把“答案是否 ≤ 某个值”转化为**一个判定问题**，随后用**二分搜索**在答案空间里快速定位最小的满足条件的 `mid`。

**如何判定 `[1, mid]` 能否满足条件？**  

1. **不被 `divisor1` 整除的数的个数**  
   `notDiv1 = mid - mid // divisor1`  
   （总数 `mid` 减去被 `divisor1` 整除的数）  
   必须满足 `notDiv1 ≥ uniqueCnt1`。  

2. **不被 `divisor2` 整除的数的个数**  
   `notDiv2 = mid - mid // divisor2`  
   必须满足 `notDiv2 ≥ uniqueCnt2`。  

3. **两边使用的数必须互不冲突**。  
   同时出现于 `arr1` 与 `arr2` 的冲突只会发生在**既能被 `divisor1` 整除又能被 `divisor2` 整除**的数（即 `lcm(divisor1, divisor2)` 的倍数）。这些数既不能放进 `arr1`（被 `divisor1` 整除），也不能放进 `arr2`（被 `divisor2` 整除），只能**舍弃**。  
   因此在 `[1, mid]` 可用的总数是  
   `usable = mid - mid // lcm(divisor1, divisor2)`。  
   必须满足 `uniqueCnt1 + uniqueCnt2 ≤ usable`。

只要以上三个不等式全部成立，就可以在 `mid` 以内完成分配，二分搜索即可收敛到最小的 `mid`。

**核心算法**：二分搜索 + 数学计数（利用整除求数量）。  
**关键数据结构**：只用到整数运算，**不需要额外的数组**，所以空间极小。

**类比**：把 `[1, mid]` 看成一盒糖果，  
- “不能给小朋友 A 的糖果”是被 `divisor1` 整除的；  
- “不能给小朋友 B 的糖果”是被 `divisor2` 整除的；  
- “两个人都不想要的糖果”是同时被两者整除的。  
我们只要检查盒子里够不够满足 A、B 各自的需求以及总量，就能决定是否把盒子再小一点。

#### 代码（Python）

```python
import math

def minMaximum(divisor1: int, divisor2: int,
               uniqueCnt1: int, uniqueCnt2: int) -> int:
    """
    二分搜索最小的最大值，使得可以在 [1, ans] 中分别挑选出
    uniqueCnt1 个不被 divisor1 整除的数 和
    uniqueCnt2 个不被 divisor2 整除的数，且两组数不冲突。
    """
    # 计算最小公倍数（lcm）
    lcm = divisor1 // math.gcd(divisor1, divisor2) * divisor2

    # 判定函数：mid 是否可行
    def ok(mid: int) -> bool:
        # 1) arr1 能得到的合法数
        notDiv1 = mid - mid // divisor1
        if notDiv1 < uniqueCnt1:
            return False

        # 2) arr2 能得到的合法数
        notDiv2 = mid - mid // divisor2
        if notDiv2 < uniqueCnt2:
            return False

        # 3) 总的可用数（剔除同时被两个 divisor 整除的数）
        usable = mid - mid // lcm
        return uniqueCnt1 + uniqueCnt2 <= usable

    # 二分搜索的上下界
    lo, hi = 1, 10**18            # 设一个足够大的上界
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid               # 还能往左走，说明答案不大于 mid
        else:
            lo = mid + 1           # 太小了，需要更大的上限

    return lo
```

**代码要点说明**  

- `math.gcd` 用来求最大公约数，进而算出 `lcm`（最小公倍数），相当于“两个字典的共同页码”。  
- `mid // divisor` 表示 **“mid 以内有多少个 divisor 的倍数”**，这一步把“被除尽的糖果”直接计数出来，省去了遍历。  
- 二分循环 `while lo < hi` 每次都把搜索区间缩小一半，最多进行 `log2(10^18) ≈ 60` 次迭代，几乎是常数时间。

#### 复杂度  

- **时间复杂度**：`O(log answer)`，每次判定是 O(1) 的算术运算，二分至多约 60 次。  
  > 与暴力的 `O(M)` 相比，`log` 级别的增长几乎可以忽略不计。  
- **空间复杂度**：`O(1)`，只用了几个整数变量。

---

## 心得  

- **核心技巧**：把“找最小满足条件的数”转化为“判断某个上限是否可行”，再用 **二分搜索** 快速定位。  
- **适用的题型**  
  1. “在满足若干计数约束的前提下，最小化最大值”——如 *Minimum Size Subarray Sum*、*Find Minimum Number of Days to Make M Bouquets*。  
  2. “给定资源上限，判断是否可以完成任务”——如 *Capacity To Ship Packages Within D Days*、*Koko Eating Bananas*。  
- **一句话总结解题钥匙**：**把枚举转为单调判定 + 二分**。

---

## 反思  

- **第一反应**：直接把 1,2,3,… 一个一个塞进数组，想当然地认为可以跑通。  
- **最容易踩的坑**  
  - **忽略“同时被两个 divisor 整除的数”**：这些数既不能放进 `arr1` 也不能放进 `arr2`，必须在计数时剔除。  
  - **上界选取不当**：若上界太小会导致二分永远找不到可行解，太大则会产生溢出（在 Python 中不怕，但在有整数上限的语言需要注意）。  
  - **边界条件**：`uniqueCnt1`、`uniqueCnt2` 可能接近 `10^9`，一定要用 `int64`（Python 自动）并确保乘法不会 overflow。  
- **下次遇到同类题**：第一步先**判断是否存在单调性**（答案增大时可行性不会变坏），然后**写出判定函数**，最后**二分搜索**。这样思路更清晰，代码也更简洁。