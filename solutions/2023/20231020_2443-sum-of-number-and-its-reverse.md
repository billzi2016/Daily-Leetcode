# #2443. 数字与其反转之和 / Sum of Number and Its Reverse

> 难度：中等 · 标签：Math、Enumeration · [LeetCode 链接](https://leetcode.com/problems/sum-of-number-and-its-reverse/)

---

## 题目（英文原版）

**Description**

Given a non-negative integer num, return true if num can be expressed as the sum of any non-negative integer and its reverse, or false otherwise.

**Examples**

**Example 1:**

```
Input: num = 443
Output: true
Explanation: 172 + 271 = 443 so we return true.
```

**Example 2:**

```
Input: num = 63
Output: false
Explanation: 63 cannot be expressed as the sum of a non-negative integer and its reverse so we return false.
```

**Example 3:**

```
Input: num = 181
Output: true
Explanation: 140 + 041 = 181 so we return true. Note that when a number is reversed, there may be leading zeros.
```

**Constraints**

- 0 <= num <= 105

---

## 题目（中文翻译）

**描述**  
给定一个非负整数 `num`，如果 `num` 可以表示为某个非负整数与其反转（reverse）之和，则返回 `true`；否则返回 `false`。

**示例**  

**示例 1**  
```
Input: num = 443
Output: true
Explanation: 172 + 271 = 443，所以返回 true。
```

**示例 2**  
```
Input: num = 63
Output: false
Explanation: 63 不能表示为某个非负整数与其反转之和，故返回 false。
```

**示例 3**  
```
Input: num = 181
Output: true
Explanation: 140 + 041 = 181，所以返回 true。注意，当数字被反转时，可能会出现前导零。
```

**约束条件**  
- `0 <= num <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把**所有可能的非负整数**都枚举一遍，看看它们和自己的翻转相加后是否恰好等于 `num`。  

- **数据结构**：只需要一个普通的整数变量来保存当前枚举的数 `x`，以及它的翻转 `rev(x)`。  
  - **翻转**可以想象成把数字写在纸上，然后把纸翻过去读出来——这正好和把字符串倒序后再转回整数的过程一样。  
- **正确性**：因为题目要求“存在任意非负整数 `x`，满足 `x + rev(x) = num`”。只要我们把 **所有** `x`（从 `0` 到 `num`）都尝试一次，就一定能找到答案（如果有的话），或者在全部尝试完后确认不存在。  

#### 代码（Python）

```python
def reverse_number(x: int) -> int:
    """
    把整数 x 翻转，例如 172 -> 271，041 -> 41
    实现思路：先转成字符串，再倒序，最后转回整数
    """
    return int(str(x)[::-1])          # 字符串切片 [::-1] 表示倒序

def sum_of_num_and_reverse_bruteforce(num: int) -> bool:
    """
    暴力枚举所有可能的 x，判断是否满足 x + rev(x) == num
    """
    # x 只能取到不大于 num，因为 rev(x) >= 0
    for x in range(num + 1):          # 包含 num 本身
        rev = reverse_number(x)      # 计算 x 的翻转
        if x + rev == num:           # 找到匹配
            return True
    return False                     # 没有任何匹配
```

#### 复杂度  

- **时间复杂度**：`O(num)`  
  - “`O(num)`”的含义是：如果 `num` 是 10 万，那么最多要检查 10 万次，每一次的操作（翻转和加法）都是常数时间，所以整体耗时大约与 `num` 成正比。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，和 `num` 的大小无关，所占内存是常数级的。

---

### 2. 最优解

#### 思路  

虽然上面的暴力已经能在本题的约束（`0 ≤ num ≤ 10⁵`）下跑得很快，但我们仍可以把 **不必要的循环次数** 再削减一点，使思路更加严谨。

1. **观察**：  
   - `x + rev(x) = num`，两边都是非负数。  
   - `rev(x)` 至少是 `0`，所以 `x ≤ num`（已经在暴力里用了）。  
   - 同时，`rev(x)` 也不可能大于 `num`，因为如果 `rev(x) > num`，左边必然 > `num`，不成立。于是 `rev(x) ≤ num`，这进一步说明 `x` 的 **位数** 不会超过 `num` 的位数。  

2. **进一步削减搜索范围**：  
   - 对于每一位的数字，翻转后仍然是同样的数字，只是位置变了。  
   - 当 `x` 很大（接近 `num`）时，`rev(x)` 通常也比较大，导致 `x + rev(x)` 超过 `num`。  
   - 实际上，只需要枚举 `x` 到 `num // 2` 左右的范围即可（因为如果 `x > num // 2`，则 `rev(x) ≥ 0`，`x + rev(x) > num // 2`，仍可能等于 `num`，但此时 `rev(x)` 必须非常小，这只能在 `x` 的末尾有大量 `0` 时出现；为了不遗漏，这里仍保守地遍历到 `num`，但在实现时直接使用整数翻转，避免字符串带来的额外开销）。  

3. **核心技巧 – 整数翻转**：  
   - 用 **数学方式** 翻转整数，而不是字符串。  
   - 思路类似 “把数字一位一位弹出来，放到新数字的末尾”。这相当于把数字装进一个盒子里，然后把盒子倒过来。  

4. **完整流程**：  
   - 从 `0` 到 `num`（或更紧的 `num // 2`）逐个尝试 `x`。  
   - 用数学方法快速得到 `rev(x)`。  
   - 检查 `x + rev(x) == num`，若成立立刻返回 `True`。  
   - 循环结束仍未找到，则返回 `False`。  

#### 代码（Python）

```python
def reverse_int(x: int) -> int:
    """
    纯数学实现整数翻转，避免使用字符串。
    过程类似：
        123 -> 321
    """
    rev = 0
    while x > 0:
        rev = rev * 10 + x % 10   # 取最低位加入 rev 的末尾
        x //= 10                  # 去掉已经取出的最低位
    return rev

def sum_of_num_and_reverse(num: int) -> bool:
    """
    最优实现：遍历 0~num，使用整数翻转检查是否存在满足条件的 x。
    """
    for x in range(num + 1):          # 包含 num 本身
        if x + reverse_int(x) == num:
            return True
    return False
```

#### 复杂度  

- **时间复杂度**：`O(num * d)`，其中 `d` 是 `num` 的位数（最多 6 位，因为 `num ≤ 10⁵`）。  
  - 实际上 `d` 是常数（≤6），所以整体仍可视为 `O(num)`，比纯字符串实现稍快。  
- **空间复杂度**：`O(1)`，只使用了几个整数变量。

与暴力解的对比：  
- **时间**上，两者都是线性遍历，但最优解省掉了字符串转化的额外开销，常数因子更小。  
- **空间**上，两者均为常数级。

---

## 心得

- **核心技巧**：枚举 + 整数翻转。  
- **适用题型**：  
  1. “判断一个数能否表示为 **两个数的和**，其中一个数是另一个数的**翻转**”。  
  2. “求所有满足 `x + rev(x) = target` 的 `x`（比如找所有可能的 `x`）”。  
  3. “利用数字翻转进行特殊数列的构造或判定（如回文数、反转加数）”。  
- **解题钥匙**：**“把所有可能的候选数枚举出来，再用快速翻转检查”**。

---

## 反思

- **第一反应**：直接想到遍历所有 `x`，因为约束很小，暴力就能通过。  
- **最容易踩的坑**：  
  - 忽视 **前导零** 的存在。翻转 `140` 得到 `041`，数值上等于 `41`，但在实现时只要把整数翻转即可，前导零自然被去掉。  
  - 对 `num = 0` 的特殊处理：`0 + rev(0) = 0`，应该返回 `True`。  
- **下次思路**：看到 “数 + 其翻转” 这种结构，第一步就想到 **枚举 + 翻转**，随后检查是否能进一步剪枝（比如只遍历到 `num // 2`），或者使用 **数学翻转** 以降低常数时间。