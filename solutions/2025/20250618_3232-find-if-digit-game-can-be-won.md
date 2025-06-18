# #3232. 判断数字游戏是否能获胜 / Find if Digit Game Can Be Won

> 难度：简单 · 标签：Array、Math · [LeetCode 链接](https://leetcode.com/problems/find-if-digit-game-can-be-won/)

---

## 题目（英文原版）

**Description**

You are given an array of positive integers nums.
Alice and Bob are playing a game. In the game, Alice can choose either all single-digit numbers or all double-digit numbers from nums, and the rest of the numbers are given to Bob. Alice wins if the sum of her numbers is strictly greater than the sum of Bob's numbers.
Return true if Alice can win this game, otherwise, return false.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,10]
Output: false
Explanation:
Alice cannot win by choosing either single-digit or double-digit numbers.
```

**Example 2:**

```
Input: nums = [1,2,3,4,5,14]
Output: true
Explanation:
Alice can win by choosing single-digit numbers which have a sum equal to 15.
```

**Example 3:**

```
Input: nums = [5,5,5,25]
Output: true
Explanation:
Alice can win by choosing double-digit numbers which have a sum equal to 25.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 99

---

## 题目（中文翻译）

给定一个由正整数（positive integers）构成的数组 `nums`。

Alice 和 Bob 正在玩一个游戏。游戏规则如下：

- Alice 可以从 `nums` 中选择 **全部** 的单数字（single-digit numbers）或 **全部** 的双数字（double-digit numbers），其余的数字全部交给 Bob。
- 如果 Alice 所拿数字的和 **严格大于** Bob 所拿数字的和，则 Alice 获胜。

返回 `true` 表示 Alice 能够获胜，否则返回 `false`。

## 示例

### 示例 1
**输入**  
`nums = [1,2,3,4,10]`  

**输出**  
`false`  

**解释**  
无论 Alice 选择全部单数字还是全部双数字，她都无法使自己的总和严格大于 Bob 的总和。

### 示例 2
**输入**  
`nums = [1,2,3,4,5,14]`  

**输出**  
`true`  

**解释**  
Alice 选择全部单数字，得到的和为 `1+2+3+4+5 = 15`，而 Bob 只剩下 `14`，所以 Alice 获胜。

### 示例 3
**输入**  
`nums = [5,5,5,25]`  

**输出**  
`true`  

**解释**  
Alice 选择全部双数字，得到的和为 `25`，而 Bob 只剩下 `5+5+5 = 15`，因此 Alice 获胜。

## 约束条件

- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 99`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目只给了两种合法的选择：

1. **全选所有一位数**（即 0~9 的数字），其余的交给 Bob。  
2. **全选所有两位数**（即 10~99 的数字），其余的交给 Bob。

我们可以**直接把这两种情况都算一遍**，看哪一种能让 Alice 的总和大于 Bob 的总和。

- **数据结构**：只需要遍历一次数组，用两个整数变量分别累计“一位数的和” `single_sum` 和 “两位数的和” `double_sum`。  
  - 这里的“哈希表”类比可以想象成一本字典，`key` 是“数字的位数”，`value` 是“该类数字的总和”。不过我们这里不真的建哈希表，只是用两个变量来“记”这两个键对应的值。

- **为什么正确**：因为题目限制 Alice 只能一次性选 **全部** 的一位数或全部的两位数，没有别的组合可能。只要我们把这两种可能的总和算出来，再和全体数字的总和比较，就能判断是否能获胜。

- **时间/空间复杂度**  
  - 我们会 **分别遍历数组两次**（一次算一位数的和，一次算两位数的和），每次都要看 `num` 的大小。遍历一次是 `O(n)`，遍历两次就是 `2·O(n)`，在大 O 记号里我们只关心数量级，所以写作 **`O(n)`**。  
    - 大白话：如果数组有 1000 个数，程序大概会检查 2000 次数字，这在电脑眼里算是“线性”增长，规模翻倍检查次数也翻倍。
  - 只用了常数个额外变量（`single_sum、double_sum、total_sum`），所以 **`O(1)`**（常数空间）。  
    - 大白话：不管数组有多大，记住几个数字的空间始终不变。

#### 代码（Python）

```python
from typing import List

def canAliceWin_bruteforce(nums: List[int]) -> bool:
    # 1️⃣ 先算出所有数字的总和，后面要用到
    total_sum = sum(nums)                # O(n)

    # 2️⃣ 计算「所有一位数」的和
    single_sum = 0
    for x in nums:                       # 第一次遍历 O(n)
        if x < 10:                        # 一位数的条件
            single_sum += x

    # 3️⃣ 计算「所有两位数」的和
    double_sum = 0
    for x in nums:                       # 第二次遍历 O(n)
        if x >= 10:                       # 两位数的条件
            double_sum += x

    # 4️⃣ 判断 Alice 选哪种能赢
    #   选单数时：Alice = single_sum，Bob = total_sum - single_sum
    #   需要 Alice > Bob，即 2*single_sum > total_sum
    if 2 * single_sum > total_sum:
        return True
    #   选双数时同理
    if 2 * double_sum > total_sum:
        return True

    return False
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 虽然代码里出现了两次遍历，但常数因子（2）在大 O 记号里被忽略。  
  - 实际含义：数组长度每增加一倍，程序检查的次数也大约增加两倍（一次算一位数，一次算两位数）。
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，和数组大小无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**两次遍历是冗余的**：在一次遍历中，我们完全可以同时累计“一位数的和”和“两位数的和”。这样就把“遍历次数”从 2 次降到 1 次，时间常数因子减半。

**瓶颈**：在暴力解里，重复遍历数组导致不必要的 CPU 读取。对长度最多 100 的数组来说影响不大，但养成“一遍搞定”的好习惯对更大规模的数据更重要。

**优化步骤**：

1. 初始化三个累计变量：`total_sum、single_sum、double_sum`。  
2. **一次遍历**整个数组，对每个 `num`：
   - 加入 `total_sum`（所有数字的和）。
   - 根据 `num` 是 <10 还是 ≥10，分别加到 `single_sum` 或 `double_sum`。  
   这一步相当于在同一次“检查”里完成了“查字典”和“更新值”的两件事。
3. 遍历结束后，用同样的比较公式判断：
   - `2 * single_sum > total_sum` 或 `2 * double_sum > total_sum`。

**核心算法/数据结构**：这里没有高级结构，唯一的技巧是**一次遍历（single pass）**，它利用了**线性扫描**的特性，把所有需要的信息一次性收集完。

**类比**：想象你在超市买东西，要统计水果和蔬菜的花费。如果先把所有水果的花费加起来，再去一次超市把蔬菜的花费加起来，你会走两遍超市；而如果你在同一次购物时，把水果和蔬菜的花费分别记下来，就只需要走一次。

#### 代码（Python）

```python
def canAliceWin(nums: List[int]) -> bool:
    total_sum = 0      # 所有数字的总和
    single_sum = 0     # 一位数的总和
    double_sum = 0     # 两位数的总和

    for x in nums:                 # 只遍历一次 O(n)
        total_sum += x
        if x < 10:                 # 一位数
            single_sum += x
        else:                      # 两位数（题目保证不超过 99）
            double_sum += x

    # 判断 Alice 选哪种能赢
    return 2 * single_sum > total_sum or 2 * double_sum > total_sum
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组。  
  - 与暴力解相比，**实际运行的循环次数少了一半**，在大数据量时会更快。
- **空间复杂度**：`O(1)` —— 仍然只用常数个整数变量。

---

## 心得

- **核心技巧**：一次遍历同时累计多类信息（多路统计）。  
- **适用的题型**  
  1. “统计奇数/偶数之和、正数/负数之和”等需要分别求两类或多类累计值的题目。  
  2. “在一次遍历中求最大值、最小值和总和”这类多目标统计。  
  3. “根据属性把元素分组求和”比如分年龄段、分字母等。
- **解题钥匙**：**把所有需要的统计放进同一次循环**，避免重复遍历。

---

## 反思

- **第一反应**：先把一位数和两位数分别求和，分别比较。  
- **最容易踩的坑**  
  - 忽略了“严格大于” (`>` 而不是 `>=`) 的条件。  
  - 没有考虑数组全是同一位数的极端情况（例如全部都是 1 位数），但公式仍然适用。  
  - 把 10 当成“一位数”误判。  
- **下次遇到同类题**：第一步想到 **“一次遍历收集所有类别的累计信息”**，再在遍历结束后统一判断。这样既简洁又高效。