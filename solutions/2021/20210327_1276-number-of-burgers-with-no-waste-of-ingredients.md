# #1276. 无剩余食材的汉堡数量 / Number of Burgers with No Waste of Ingredients

> 难度：中等 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/number-of-burgers-with-no-waste-of-ingredients/)

---

## 题目（英文原版）

**Description**

Given two integers tomatoSlices and cheeseSlices. The ingredients of different burgers are as follows:
Return [total_jumbo, total_small] so that the number of remaining tomatoSlices equal to 0 and the number of remaining cheeseSlices equal to 0. If it is not possible to make the remaining tomatoSlices and cheeseSlices equal to 0 return [].

**Examples**

**Example 1:**

```
Input: tomatoSlices = 16, cheeseSlices = 7
Output: [1,6]
Explantion: To make one jumbo burger and 6 small burgers we need 4*1 + 2*6 = 16 tomato and 1 + 6 = 7 cheese.
There will be no remaining ingredients.
```

**Example 2:**

```
Input: tomatoSlices = 17, cheeseSlices = 4
Output: []
Explantion: There will be no way to use all ingredients to make small and jumbo burgers.
```

**Example 3:**

```
Input: tomatoSlices = 4, cheeseSlices = 17
Output: []
Explantion: Making 1 jumbo burger there will be 16 cheese remaining and making 2 small burgers there will be 15 cheese remaining.
```

**Constraints**

- 0 <= tomatoSlices, cheeseSlices <= 107

---

## 题目（中文翻译）

给定两个整数 `tomatoSlices` 和 `cheeseSlices`。不同类型的汉堡所需的配料如下：

- **巨无霸汉堡（jumbo burger）**：需要 4 片番茄（tomatoSlices）和 1 片奶酪（cheeseSlices）  
- **小汉堡（small burger）**：需要 2 片番茄（tomatoSlices）和 1 片奶酪（cheeseSlices）

返回一个长度为 2 的数组 `[total_jumbo, total_small]`，使得使用完所有配料后剩余的番茄片数和奶酪片数均为 0。如果不存在这样的一组汉堡数量，则返回空数组 `[]`。

---

### 示例

**示例 1**  
```text
Input: tomatoSlices = 16, cheeseSlices = 7
Output: [1,6]
Explanation: 制作 1 个巨无霸汉堡和 6 个小汉堡需要
4*1 + 2*6 = 16 片番茄，且 1 + 6 = 7 片奶酪，恰好用完所有配料。
```

**示例 2**  
```text
Input: tomatoSlices = 17, cheeseSlices = 4
Output: []
Explanation: 无法用全部配料恰好组合出小汉堡和巨无霸汉堡。
```

**示例 3**  
```text
Input: tomatoSlices = 4, cheeseSlices = 17
Output: []
Explanation: 做 1 个巨无霸汉堡后会剩余 16 片奶酪，做 2 个小汉堡后会剩余 15 片奶酪，均无法全部使用。
```

---

### 约束条件

- `0 <= tomatoSlices, cheeseSlices <= 10^7`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
我们先把题目抽象成数学方程：

* 设 **大汉堡**（jumbo） 的数量为 `x`，**小汉堡**（small） 的数量为 `y`。  
* 每个大汉堡需要 4 片番茄 + 1 片奶酪。  
* 每个小汉堡需要 2 片番茄 + 1 片奶酪。  

于是得到两条约束：

```
4·x + 2·y = tomatoSlices          (番茄总数)
x + y = cheeseSlices               (奶酪总数)
```

最直接的办法是把 `x` 从 `0` 枚举到 `cheeseSlices`（因为不可能超过奶酪片数），
每一次算出对应的 `y = cheeseSlices - x`，再检查 `4·x + 2·y` 是否恰好等于 `tomatoSlices`。  

这就像在超市里 **“一边挑汉堡，一边数番茄和奶酪”**，逐个尝试所有可能的组合，看到满足条件的才停下来。

**为什么正确？**  
只要遍历了所有合法的 `x`（即所有可能的大汉堡数量），对应的 `y` 也唯一确定，
因此一定能找到所有满足两个方程的解；若遍历完都找不到，说明根本不存在解。

#### 代码（Python）

```python
def numOfBurgers_bruteforce(tomatoSlices: int, cheeseSlices: int):
    # 枚举大汉堡的可能数量 x
    for x in range(cheeseSlices + 1):                 # x 不能超过奶酪片数
        y = cheeseSlices - x                          # 小汉堡的数量唯一确定
        # 检查番茄是否恰好用完
        if 4 * x + 2 * y == tomatoSlices:
            return [x, y]                             # 找到答案，直接返回
    # 循环结束仍未找到，说明无解
    return []
```

> **关键行中文注释**  
> - `for x in range(cheeseSlices + 1)`: 从 0 到奶酪片数逐个尝试大汉堡数量。  
> - `y = cheeseSlices - x`: 因为每个汉堡都恰好用掉 1 片奶酪，剩下的奶酪全给小汉堡。  
> - `if 4 * x + 2 * y == tomatoSlices`: 判断番茄片数是否恰好匹配。  

#### 复杂度  

- **时间复杂度：** `O(cheeseSlices)`  
  - 用大白话解释就是：如果奶酪有 10 000 片，我们最多要检查 10 001 种组合，时间随奶酪数量线性增长。  
- **空间复杂度：** `O(1)`  
  - 只用了几个整数变量，所占内存几乎不变。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于“逐个尝试”。  
其实我们已经有了两个线性方程，完全可以用代数方法一次性求解，而不必遍历。

把第二个方程 `x + y = cheeseSlices` 变形得到 `y = cheeseSlices - x`，  
代入第一个方程：

```
4·x + 2·(cheeseSlices - x) = tomatoSlices
=> 4x + 2·cheeseSlices - 2x = tomatoSlices
=> 2x = tomatoSlices - 2·cheeseSlices
=> x = (tomatoSlices - 2·cheeseSlices) / 2
```

再把 `x` 代回 `y = cheeseSlices - x`：

```
y = cheeseSlices - (tomatoSlices - 2·cheeseSlices) / 2
  = (2·cheeseSlices - tomatoSlices/2)
```

**关键点**：

1. **整数要求**：`x` 与 `y` 必须是整数。观察公式可知，`tomatoSlices` 必须是 **偶数**（否则除以 2 会出现小数）。  
2. **非负要求**：汉堡的数量不能为负数，必须满足 `x ≥ 0` 且 `y ≥ 0`。  
3. **唯一性**：一旦满足上述条件，解只有这一组（因为两个线性方程组的解唯一），不必担心出现多个答案。

所以算法步骤如下：

1. 若 `tomatoSlices` 为奇数 → 直接返回 `[]`（不可能配齐）。  
2. 计算 `x = tomatoSlices // 2 - cheeseSlices`（这里把 `tomatoSlices/2` 改写为整数除法）。  
3. 计算 `y = cheeseSlices - x`（或者 `y = 2*cheeseSlices - tomatoSlices//2`）。  
4. 检查 `x ≥ 0` 且 `y ≥ 0`，若成立返回 `[x, y]`，否则返回 `[]`。

这一步相当于 **“先算出应该有多少大汉堡，再算出剩下的全是小汉堡”**，一次算完，时间几乎为常数。

#### 代码（Python）

```python
def numOfBurgers(tomatoSlices: int, cheeseSlices: int):
    # 1. 番茄片必须是偶数，否则不可能配成 4x+2y 的形式
    if tomatoSlices % 2 == 1:
        return []

    # 2. 直接用代数推导得到的大汉堡数量
    #    tomatoSlices // 2 其实是 (tomatoSlices / 2) 的整数部分
    x = tomatoSlices // 2 - cheeseSlices   # 大汉堡的个数

    # 3. 小汉堡的个数 = 总奶酪数 - 大汉堡数
    y = cheeseSlices - x

    # 4. 检查是否出现负数（不合法）
    if x < 0 or y < 0:
        return []

    return [x, y]
```

> **关键行中文注释**  
> - `if tomatoSlices % 2 == 1:`：如果番茄片数是奇数，直接返回空列表。  
> - `x = tomatoSlices // 2 - cheeseSlices`：利用公式一次算出大汉堡数量。  
> - `y = cheeseSlices - x`：剩余的奶酪全部给小汉堡。  
> - `if x < 0 or y < 0:`：若出现负数说明配不出合法组合。  

#### 复杂度  

- **时间复杂度：** `O(1)`  
  - 只做了几次算术运算，和输入规模毫无关系。  
- **空间复杂度：** `O(1)`  
  - 只使用了常数个整数变量。

---

## 心得  

- **核心技巧**：把两个线性方程化为代数求解，利用整数约束与非负约束快速判定可行性。  
- **适用的题型**：  
  1. “两种配方恰好用完原料” 类似题（如 **LeetCode 1659** 计数鸡的数量）。  
  2. 只涉及两种物品、两条线性约束的**整数线性方程组**问题。  
- **一句话总结**：**“先把奶酪分配完（x+y=cheese），再检查番茄是否正好匹配”**。

---

## 反思  

- **第一反应**：看到两个方程就想“枚举”，因为直观上好像只能逐个尝试。  
- **最容易踩的坑**：  
  - 忽略了番茄片数必须为偶数（4 与 2 的组合只能产生偶数）。  
  - 没有检查 `x`、`y` 是否为负数，导致返回非法解。  
  - 直接使用浮点除法导致精度问题或类型错误。  
- **下次遇到同类题**：第一步先写出 **线性方程组**，尝试 **代数求解**（消元或代入），再检查整数与非负约束。这样往往可以把 O(N) 的遍历降到 O(1)。