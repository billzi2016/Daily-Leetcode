# #2525. 根据标准对盒子进行分类 / Categorize Box According to Criteria

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/categorize-box-according-to-criteria/)

---

## 题目（英文原版）

**Description**

Given four integers length, width, height, and mass, representing the dimensions and mass of a box, respectively, return a string representing the category of the box.
Note that the volume of the box is the product of its length, width and height.

**Examples**

**Example 1:**

```
Input: length = 1000, width = 35, height = 700, mass = 300
Output: "Heavy"
Explanation: 
None of the dimensions of the box is greater or equal to 104. 
Its volume = 24500000 <= 109. So it cannot be categorized as "Bulky".
However mass >= 100, so the box is "Heavy".
Since the box is not "Bulky" but "Heavy", we return "Heavy".
```

**Example 2:**

```
Input: length = 200, width = 50, height = 800, mass = 50
Output: "Neither"
Explanation: 
None of the dimensions of the box is greater or equal to 104.
Its volume = 8 * 106 <= 109. So it cannot be categorized as "Bulky".
Its mass is also less than 100, so it cannot be categorized as "Heavy" either. 
Since its neither of the two above categories, we return "Neither".
```

**Constraints**

- 1 <= length, width, height <= 105
- 1 <= mass <= 103

---

## 题目（中文翻译）

给定四个整数 `length`、`width`、`height` 和 `mass`，分别表示盒子的长度、宽度、高度和质量，返回一个字符串，表示该盒子的类别。  
注意，盒子的体积（volume）等于长度、宽度和高度的乘积。

### 示例

#### 示例 1
**输入**: `length = 1000, width = 35, height = 700, mass = 300`  
**输出**: `"Heavy"`  
**解释**:  
- 没有任意一个维度大于或等于 `10^4`。  
- 其体积 = `24500000 ≤ 10^9`，因此不能归为 `"Bulky"`。  
- 但是质量 `mass ≥ 100`，所以盒子属于 `"Heavy"`。  
- 由于盒子既不是 `"Bulky"` 也不是 `"Heavy"`，我们返回 `"Heavy"`。

#### 示例 2
**输入**: `length = 200, width = 50, height = 800, mass = 50`  
**输出**: `"Neither"`  
**解释**:  
- 没有任意一个维度大于或等于 `10^4`。  
- 其体积 = `8 * 10^6 ≤ 10^9`，因此不能归为 `"Bulky"`。  
- 质量也小于 `100`，因此也不能归为 `"Heavy"`。  
- 由于既不属于上述两类，我们返回 `"Neither"`。

### 约束条件
- `1 <= length, width, height <= 10^5`  
- `1 <= mass <= 10^3`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题只需要判断 **四个整数** 是否满足几条固定的条件，然后返回对应的文字描述。  
最直接的想法就是：

1. **计算体积**：`volume = length * width * height`（体积就是长宽高的乘积）。
2. **判断 “Bulky”**  
   - 任意一个维度 `≥ 10⁴`，**或者** 体积 `≥ 10⁹` → 箱子算 “Bulky”。  
   - 这里的 “≥” 就像在查字典，看到一个词（维度）已经够大，就直接返回“是”。
3. **判断 “Heavy”**  
   - 质量 `mass ≥ 100` → 箱子算 “Heavy”。  
4. **组合结果**  
   - 两个标记都为真 → 返回 `"Both"`  
   - 只满足 “Bulky” → 返回 `"Bulky"`  
   - 只满足 “Heavy” → 返回 `"Heavy"`  
   - 两个都不满足 → 返回 `"Neither"`  

这套流程是“暴力”的，因为我们不做任何提前的剪枝或数学变形，直接把所有条件全部检查一遍。  

> **为什么正确**  
> 条件本身就是题目给出的分类规则，逐条检查自然能得到唯一的答案。没有遗漏，也没有冲突。

#### 代码（Python）

```python
def categorizeBox(length: int, width: int, height: int, mass: int) -> str:
    """
    根据题目给出的规则返回箱子的类别。
    """
    # 1. 计算体积
    volume = length * width * height          # 长 × 宽 × 高

    # 2. 判断是否满足 "Bulky"
    #   - 任意一边 >= 10^4
    #   - 或者体积 >= 10^9
    bulky = (length >= 10**4 or
             width  >= 10**4 or
             height >= 10**4 or
             volume >= 10**9)

    # 3. 判断是否满足 "Heavy"
    heavy = mass >= 100

    # 4. 根据两个布尔值返回对应的文字
    if bulky and heavy:
        return "Both"
    if bulky:
        return "Bulky"
    if heavy:
        return "Heavy"
    return "Neither"
```

#### 复杂度  

- **时间复杂度：O(1)** — 只做了几次算术运算和比较，跟输入的大小无关。  
  > “O(1)” 可以理解为“不管箱子有多大，程序只需要固定步数就能算出答案”。  
- **空间复杂度：O(1)** — 只用了常数个变量 (`volume`, `bulky`, `heavy`) 保存中间结果。  

---

### 2. 最优解

#### 思路  

从暴力解来看，**所有操作本身已经是常数时间**，已经达到了理论上的最优。  
所谓“最优”，这里指的是 **代码的简洁度和可读性**，以及 **避免不必要的乘法**：

- 体积的乘法只有在所有维度都小于 `10⁴` 时才会影响 “Bulky” 判定。  
- 若已经发现某个维度 `≥ 10⁴`，我们可以直接把 `bulky` 设为 `True`，**不必再计算体积**，省去一次乘法（在极端情况下可以略微提升速度）。  

实现思路：

1. 先检查四个维度是否有 `≥ 10⁴`，若有直接 `bulky = True`。  
2. 若四个维度都小于 `10⁴`，再计算体积并与 `10⁹` 比较。  
3. 质量判定保持不变。  

这样做的好处是 **把乘法的次数最小化**，虽然在 Python 中乘法本身已经很快，但对初学者来说，**先筛选再计算** 的思路更容易迁移到需要大量乘法的题目（比如矩阵乘法、快速幂等）。

#### 代码（Python）

```python
def categorizeBox(length: int, width: int, height: int, mass: int) -> str:
    """
    通过先筛选维度，再在必要时计算体积，得到最简洁的 O(1) 解法。
    """
    # 1. 先判断是否有任意一边已经够大
    bulky = (length >= 10**4 or
             width  >= 10**4 or
             height >= 10**4)

    # 2. 若上一步没有确认 "Bulky"，再检查体积
    if not bulky:
        volume = length * width * height
        bulky = volume >= 10**9

    # 3. 判断是否 "Heavy"
    heavy = mass >= 100

    # 4. 返回对应的类别
    if bulky and heavy:
        return "Both"
    if bulky:
        return "Bulky"
    if heavy:
        return "Heavy"
    return "Neither"
```

#### 复杂度  

- **时间复杂度：O(1)** — 仍然是常数时间，只是最多进行一次乘法。  
- **空间复杂度：O(1)** — 使用的变量数量未增加。

---

## 心得

- **核心技巧**：**多条件判定 + 布尔逻辑组合**。  
- **适用的题型**  
  1. “判定是否满足多个阈值条件”——如 LeetCode 1662 *Check If Two String Arrays are Equivalent*（只要每个字符满足条件即可）。  
  2. “分类问题”——如 1742 *Maximum Number of Balls in a Box*（根据容量划分箱子）。  
  3. “阈值过滤”——如 1669 *Merge In Between Linked Lists*（判断链表节点是否在区间内）。  
- **一句话总结**：**把每条规则写成独立的布尔表达式，再用逻辑运算组合即可快速得到答案**。

---

## 反思

- **第一反应**：看到“体积”和“质量”两个概念，立刻想到要分别判断体积阈值和质量阈值，然后把结果组合。  
- **最容易踩的坑**  
  1. **整数溢出**：在某些语言（如 C/C++）里 `length * width * height` 可能超过 32 位整数，需要使用 64 位或大数类型。Python 天然支持大整数，故不必担心。  
  2. **忘记“或”关系**：判断 “Bulky” 时是 “任意维度 ≥ 10⁴ **或** 体积 ≥ 10⁹”，容易误写成 “且”。  
  3. **返回值拼写**：题目要求的返回字符串必须完全匹配（大小写、空格），写错会直接 WA。  
- **下次遇到同类题**：**第一步先把每条判定条件抽离成单独的布尔变量**，再根据这些变量的组合决定最终答案，这样思路清晰且不易遗漏。