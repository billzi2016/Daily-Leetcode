# #2739. 总行驶距离 / Total Distance Traveled

> 难度：简单 · 标签：Math、Simulation · [LeetCode 链接](https://leetcode.com/problems/total-distance-traveled/)

---

## 题目（英文原版）

**Description**

A truck has two fuel tanks. You are given two integers, mainTank representing the fuel present in the main tank in liters and additionalTank representing the fuel present in the additional tank in liters.
The truck has a mileage of 10 km per liter. Whenever 5 liters of fuel get used up in the main tank, if the additional tank has at least 1 liters of fuel, 1 liters of fuel will be transferred from the additional tank to the main tank.
Return the maximum distance which can be traveled.
Note: Injection from the additional tank is not continuous. It happens suddenly and immediately for every 5 liters consumed.

**Examples**

**Example 1:**

```
Input: mainTank = 5, additionalTank = 10
Output: 60
Explanation: 
After spending 5 litre of fuel, fuel remaining is (5 - 5 + 1) = 1 litre and distance traveled is 50km.
After spending another 1 litre of fuel, no fuel gets injected in the main tank and the main tank becomes empty.
Total distance traveled is 60km.
```

**Example 2:**

```
Input: mainTank = 1, additionalTank = 2
Output: 10
Explanation: 
After spending 1 litre of fuel, the main tank becomes empty.
Total distance traveled is 10km.
```

**Constraints**

- 1 <= mainTank, additionalTank <= 100

---

## 题目（中文翻译）

描述  
一辆卡车有两个燃油箱。给定两个整数 `mainTank` 表示主油箱中剩余的燃油（升），以及 `additionalTank` 表示辅助油箱中剩余的燃油（升）。  
卡车的油耗为 **10 km/升**（mileage）。每当主油箱消耗 **5 升** 燃油后，如果辅助油箱中至少还有 **1 升** 燃油，则会立即从辅助油箱向主油箱转移 **1 升** 燃油。  
返回卡车能够行驶的最大距离（公里）。  

> 注意：辅助油箱的燃油注入不是连续进行的，而是在每消耗满 **5 升** 主油箱燃油时**瞬间**完成一次转移。

示例  

**示例 1**  
```text
Input: mainTank = 5, additionalTank = 10
Output: 60
Explanation: 
在消耗了 5 升燃油后，主油箱剩余燃油为 (5 - 5 + 1) = 1 升，已行驶距离为 50 km。  
随后再消耗 1 升燃油后，未再有燃油注入，主油箱为空。  
总行驶距离为 60 km。
```

**示例 2**  
```text
Input: mainTank = 1, additionalTank = 2
Output: 10
Explanation: 
消耗完 1 升燃油后，主油箱即为空。  
总行驶距离为 10 km。
```

约束条件  
- `1 <= mainTank, additionalTank <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把卡车的行驶过程一步一步地“搬演”出来，直到油箱真的空了为止。  
我们只需要关心两件事：

1. **主油箱里的油** (`mainTank`) 每消耗 5 升，就会检查**副油箱** (`additionalTank`) 是否还有油。如果副油箱还有 ≥1 升，就立刻把 1 升油倒进主油箱。  
2. **行驶的距离**：每消耗 1 升油，卡车能行驶 10 km。

这和生活中的**“倒水罐”**非常相似：  
- 主油箱就像手里装着的水壶，每次喝掉 5 杯（5 升）后，才去厨房的备用壶（副油箱）里倒 1 杯（1 升）补回来。  
- 只要手里还有水，就继续喝；水喝完了，旅程结束。

因为题目限制 `1 ≤ mainTank, additionalTank ≤ 100`，直接模拟最多也只会循环几百次，性能完全够用。

**正确性**：  
- 每一次循环我们都严格遵守题目给出的规则：先消耗主油箱的油，再在恰好消耗了 5 升时尝试一次“加油”。  
- 当主油箱的油量降到 0 时，说明没有更多燃料可以驱动卡车，返回已累计的距离即为答案。

**复杂度**：  
- **时间复杂度**：`O(totalLiters)`，即卡车实际能消耗的油的总升数。最坏情况下 `mainTank = 100, additionalTank = 100`，总共消耗的油不超过 200 升，循环次数 ≤ 200。  
  - 用大白话说，`O(n)` 就是“随着油的多少，循环次数线性增长”。  
- **空间复杂度**：`O(1)`，只用了常数个变量（`main`, `add`, `dist`），不随输入大小增长。

#### 代码（Python）

```python
def totalDistance(mainTank: int, additionalTank: int) -> int:
    # 主油箱和副油箱的剩余油量
    main = mainTank
    add = additionalTank
    # 已经行驶的公里数
    distance = 0

    # 只要主油箱还有油，就可以继续行驶
    while main > 0:
        # 本轮最多消耗 5 升，或者如果油不够就全部消耗完
        consume = min(5, main)

        # 消耗的油对应的行驶距离（每升 10 km）
        distance += consume * 10
        # 主油箱里减去本轮消耗的油
        main -= consume

        # 只有恰好消耗了 5 升且副油箱还有油时，才会进行一次“注油”
        if consume == 5 and add > 0:
            # 从副油箱倒 1 升到主油箱
            main += 1
            add -= 1

    return distance
```

#### 复杂度

- **时间复杂度**：`O(totalLiters)` → 这里最多约 200 次循环，几乎是常数时间。  
- **空间复杂度**：`O(1)` → 只用了几个整数变量。

---

### 2. 最优解

#### 思路  

暴力解已经很快了，但我们可以把“每 5 升换 1 升”的过程抽象成**“换瓶子”**的思路，从而写出更简洁的代码。  

**瓶颈所在**：  
- 暴力解在每一次循环都要检查 `consume == 5`，这一步虽然不慢，但可以把“每 5 升一次注油”直接转化为“只要主油箱还有 5 升，就一定会把副油箱的 1 升倒进来”。  

**优化思路**：  
1. 先用主油箱的油走完整的 `5` 升段：`segments = main // 5`（完整的 5 升段数）。  
2. 每走完一段，就可以从副油箱拿走 1 升，**但**这 1 升本身也可能帮助我们再凑满 5 升，从而产生新的注油机会。  
3. 这正好等价于**“每 5 升的油可以兑换 1 升副油箱的油”**，而这 1 升又会计入后续的总油量。于是我们可以把 **主油箱 + 副油箱** 看成一个“总油量”，再不断用 **5 升换 1 升** 的规则进行“兑换”。  

这与经典的 “把空瓶子换成新饮料瓶” 问题相同：  
- 每喝掉 5 瓶空瓶子可以换 1 瓶新饮料。  
- 最终我们能喝的总瓶数 = 初始饮料瓶数 + 能换到的新瓶数。

**实现**：  
- 把 `total = main + additional` 视为“总的燃料单位”。  
- 只要 `total` 中还有 **5** 个“燃料单位”可以组成一次完整的 5 升段，就可以 **再获得 1** 个燃料单位（来自副油箱的注油）。  
- 于是我们可以用 **循环**（或等价的数学公式）来累计这额外的 1 升，直到不足 5 升为止。  

**伪代码**（思路图）：

```
total = main + additional          # 初始燃料总量（升）
extra = 0                          # 通过“5 换 1”得到的额外升数
while total >= 5:                  # 还能凑满 5 升吗？
    exchange = total // 5          # 能换多少次 1 升
    extra += exchange
    total = total % 5 + exchange   # 剩余的 <5 升 + 换来的新升
return (main + extra) * 10         # 主油箱实际消耗的升数 * 10 km
```

这里 `extra` 正好等价于暴力模拟中从副油箱真正倒进主油箱的升数。

**复杂度**：  
- 循环每次至少把 `total` 减少 4（因为 `total // 5` 至少是 1），所以循环次数 ≤ `log₅(total)`，在本题约为 3~4 次。  
- 因此 **时间复杂度** 为 `O(log total)`，几乎是常数时间。  
- **空间复杂度** 仍为 `O(1)`。

#### 代码（Python）

```python
def totalDistance(mainTank: int, additionalTank: int) -> int:
    # 初始的“燃料单位”，把两箱油加在一起
    total = mainTank + additionalTank
    # 通过“每 5 升换 1 升”得到的额外升数（只会从副油箱转进主油箱）
    extra = 0

    # 只要还能凑满 5 升，就一定会产生一次注油
    while total >= 5:
        # 这一步相当于：用 total // 5 次 5 升 → 产生同等次数的 1 升
        exchange = total // 5
        extra += exchange               # 记录得到的额外升数
        # 剩余的 <5 升 加上新得到的升数，继续循环检查
        total = total % 5 + exchange

    # 实际消耗的升数 = 主油箱最初的油 + 通过注油得到的额外升数
    total_liters_used = mainTank + extra
    # 每升可以跑 10 km
    return total_liters_used * 10
```

#### 复杂度

- **时间复杂度**：`O(log (main + additional))` → 这里的 `log` 基数是 5，意味着循环次数非常少，几乎可以视作常数时间。  
- **空间复杂度**：`O(1)` → 只用了几个整数变量。

---

## 心得

- **核心技巧**：把“每消耗 5 升主油箱就从副油箱取 1 升”抽象成 **“5 换 1” 的兑换过程**，类似“空瓶子换新饮料”或“烟头换新烟”这类贪心/数学模型。  
- **适用题型**：  
  1. **换瓶子类**（如 LeetCode 1518. Water Bottles）  
  2. **兑换类**（如 LeetCode 1368. Minimum Number of Days to Make m Bouquets）  
  3. **资源循环利用**（如 LeetCode 1642. Furthest Building You Can Reach）  
- **一句话总结**：把循环的“每 5 升一次注油”视作一种 **资源兑换**，利用数学公式一次性算出全部可以换到的额外油量。

---

## 反思

- **第一反应**：直接写一个 `while main > 0` 的模拟循环，逐步消耗油并在恰好 5 升时检查副油箱。  
- **最容易踩的坑**：  
  - 只在 **恰好消耗了 5 升** 时才进行注油，不能在消耗不到 5 升时误加油。  
  - 注意 **整数除法**（`//`）和 **取余**（`%`）的区别，防止出现小数导致精度错误。  
- **下次遇到同类题**：第一步先判断是否可以把“每 N 步/单位换 1 步/单位”抽象成 **兑换** 或 **瓶子换瓶子** 的模型，随后用数学或贪心一次性求解。