# #2839. 检查字符串是否可以通过操作 I 变得相等 / Check if Strings Can be Made Equal With Operations I

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/check-if-strings-can-be-made-equal-with-operations-i/)

---

## 题目（英文原版）

**Description**

You are given two strings s1 and s2, both of length 4, consisting of lowercase English letters.
You can apply the following operation on any of the two strings any number of times:
Return true if you can make the strings s1 and s2 equal, and false otherwise.

**Examples**

**Example 1:**

```
Input: s1 = "abcd", s2 = "cdab"
Output: true
Explanation: We can do the following operations on s1:
- Choose the indices i = 0, j = 2. The resulting string is s1 = "cbad".
- Choose the indices i = 1, j = 3. The resulting string is s1 = "cdab" = s2.
```

**Example 2:**

```
Input: s1 = "abcd", s2 = "dacb"
Output: false
Explanation: It is not possible to make the two strings equal.
```

**Constraints**

- s1.length == s2.length == 4
- s1 and s2 consist only of lowercase English letters.

---

## 题目（中文翻译）

你得到两个长度均为 4 的字符串 `s1` 和 `s2`，均只包含小写英文字母。  
你可以对任意一个字符串无限次执行以下操作：

- 选择两个下标 `i`、`j`（`0 <= i < j < 4`），交换这两个位置的字符。

如果能够通过若干次上述操作使得 `s1` 与 `s2` 相等，则返回 `true`，否则返回 `false`。

---

### 示例

**示例 1**  
输入: `s1 = "abcd"`, `s2 = "cdab"`  
输出: `true`  
解释: 我们可以对 `s1` 依次执行以下操作:  
- 选择下标 `i = 0`, `j = 2`，得到 `s1 = "cbad"`。  
- 再选择下标 `i = 1`, `j = 3`，得到 `s1 = "cdab"`，此时 `s1 == s2`。

**示例 2**  
输入: `s1 = "abcd"`, `s2 = "dacb"`  
输出: `false`  
解释: 无法通过上述操作使两个字符串相等。

---

### 约束条件

- `s1.length == s2.length == 4`
- `s1` 和 `s2` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

- 题目说只能在同一字符串上任选 **一对下标** 进行交换，且下标必须满足 `i % 2 == j % 2`（即只能在奇数位之间或偶数位之间互换）。  
- 对长度为 4 的字符串来说，满足该条件的下标对只有两组：

| 位置 | 下标 | 说明 |
|------|------|------|
| 偶数位 | (0, 2) | 把第 0 位和第 2 位的字符换位置 |
| 奇数位 | (1, 3) | 把第 1 位和第 3 位的字符换位置 |

- 因为每组下标只各有两个位置，**每组最多只能做一次交换或不做**。  
  所以整个字符串一共只有 `2 × 2 = 4` 种可能的结果（每组要么交换，要么不交换）。  

**暴力做法**：枚举这 4 种可能，把每一种得到的字符串和 `s2` 比较，只要有相等的就返回 `True`，否则返回 `False`。  

- 这相当于把 “所有可以通过合法交换得到的字符串” 列举出来，然后看目标字符串是否在其中。  

#### 代码（Python）

```python
def can_be_equal_bruteforce(s1: str, s2: str) -> bool:
    # 直接把 s1 拷贝出来，防止修改原字符串
    from itertools import product

    # 0 表示“不交换”，1 表示“交换”
    # product 会产生 (swap_even, swap_odd) 两个二元组的所有组合
    for swap_even, swap_odd in product([0, 1], repeat=2):
        lst = list(s1)                 # 把字符串转成列表，方便原地交换
        if swap_even:                  # 偶数位 (0,2) 交换
            lst[0], lst[2] = lst[2], lst[0]
        if swap_odd:                   # 奇数位 (1,3) 交换
            lst[1], lst[3] = lst[3], lst[1]
        if ''.join(lst) == s2:        # 生成的新字符串和 s2 相等就成功
            return True
    return False
```

> **关键点注释**  
> - `product([0,1], repeat=2)` 类似“把两枚硬币抛两次”，会得到 `[(0,0),(0,1),(1,0),(1,1)]` 四种组合。  
> - `lst[0], lst[2] = lst[2], lst[0]` 就像把两个盒子里的东西互换位置，Python 能一行搞定。

#### 复杂度

- **时间复杂度：** `O(1)`  
  只枚举了常数 4 种情况，每种情况的操作都是 O(1)。这里的 `O(1)` 表示**不随输入规模增长**（因为长度固定为 4），即使把常数写成 `4` 也可以理解为 “常数时间”。  
- **空间复杂度：** `O(1)`  
  只用了几个长度为 4 的临时列表，空间使用不随输入大小变化。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，真正的“瓶颈”并不是枚举，而是 **我们不必真的去做每一次交换**。  
只要 **每个位置的字符集合** 在可以交换的范围内保持不变，最终一定能把两字符串对齐。

观察一下：

- 偶数位只能在偶数位之间互换，所以 **偶数位出现的字符 multiset 必须相同**。  
- 同理，奇数位只能在奇数位之间互换，**奇数位出现的字符 multiset 也必须相同**。

只要这两个多集合相等，就一定可以通过若干次合法交换把 `s1` 变成 `s2`（把偶数位的字符排成和 `s2` 的偶数位一样，奇数位同理）。  
这一步不需要真的去执行交换，只要比较两个子集合即可。

实现上，最直观的做法是：

1. 把 `s1`、`s2` 按下标奇偶分成两组字符。  
2. 对每组字符进行排序（或计数），得到统一的“顺序”。  
3. 比较两组排序后的结果是否相同。

如果两组都相同，返回 `True`；否则返回 `False`。

> **类比**：把偶数位想象成“左手的口袋”，奇数位想象成“右手的口袋”。左手只能在左手口袋里换东西，右手只能在右手口袋里换东西。只要左手口袋里装的东西种类和右手口袋里装的东西种类分别相同，最终两个人的手里装的东西就能完全一样。

#### 代码（Python）

```python
def can_be_equal_optimal(s1: str, s2: str) -> bool:
    # 把偶数位和奇数位分别提取出来
    even1 = [s1[i] for i in range(0, 4, 2)]   # i = 0,2
    odd1  = [s1[i] for i in range(1, 4, 2)]   # i = 1,3
    even2 = [s2[i] for i in range(0, 4, 2)]
    odd2  = [s2[i] for i in range(1, 4, 2)]

    # 排序后比较，排序相当于把“口袋里的东西”按字典顺序排好，方便直接比较
    even1.sort()
    even2.sort()
    odd1.sort()
    odd2.sort()

    return even1 == even2 and odd1 == odd2
```

> **关键点注释**  
> - `range(0, 4, 2)` 表示「从 0 开始每隔 2 步取一次」——正好是所有偶数下标。  
> - `list.sort()` 会原地把列表从小到大排好，就像把口袋里的字母按字母表顺序排成一行，比较时只要看两行是否一模一样即可。

#### 复杂度

- **时间复杂度：** `O(1)`  
  实际上只处理了长度为 4 的固定字符，排序的代价是常数（最多排序 2 个长度为 2 的列表）。如果把长度记作 `n`（这里 `n=4`），复杂度可写成 `O(n log n)`，但对本题来说仍是常数时间。  
- **空间复杂度：** `O(1)`  
  只用了几段长度为 2 的临时列表，空间不随 `n` 增长。

---

## 心得

- **核心技巧**：把只能在同类下标之间交换的约束转化为“奇偶位字符集合必须相同”。  
- **适用场景**：  
  1. **字符分组交换**（如 “只能在偶数位之间或奇数位之间交换”）  
  2. **数组分块置换**（只能在同一块内部调换元素）  
  3. **棋盘染色问题**（只在同颜色格子上移动）  
- **一句话总结**：只要检查每个 **可交换子集** 内的字符 multiset 是否相同，就能判断能否相等。

---

## 反思

- **第一反应**：看到只有 4 位、且只能在同 parity 位交换，立刻想到「枚举所有可能的交换组合」。  
- **最容易踩的坑**：  
  - 忘记下标的 **奇偶性** 必须保持一致，误把任意两位都能交换会导致错误答案（例如把 `abcd` 与 `dacb` 判为相等）。  
  - 边界条件：虽然本题长度固定为 4，但若改成更长的字符串，需要用循环而不是硬编码下标。  
- **下次思路**：先抽象出“可交换的子集合”，比较每个子集合的字符计数或排序；若子集合相等，答案必为 `True`，否则 `False`。这样可以直接跳到最优解，省去枚举的步骤。