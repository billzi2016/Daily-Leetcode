# #1710. 最大单元数的卡车装载 / Maximum Units on a Truck

> 难度：简单 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-units-on-a-truck/)

---

## 题目（英文原版）

**Description**

You are assigned to put some amount of boxes onto one truck. You are given a 2D array boxTypes, where boxTypes[i] = [numberOfBoxesi, numberOfUnitsPerBoxi]:
You are also given an integer truckSize, which is the maximum number of boxes that can be put on the truck. You can choose any boxes to put on the truck as long as the number of boxes does not exceed truckSize.
Return the maximum total number of units that can be put on the truck.

**Examples**

**Example 1:**

```
Input: boxTypes = [[1,3],[2,2],[3,1]], truckSize = 4
Output: 8
Explanation: There are:
- 1 box of the first type that contains 3 units.
- 2 boxes of the second type that contain 2 units each.
- 3 boxes of the third type that contain 1 unit each.
You can take all the boxes of the first and second types, and one box of the third type.
The total number of units will be = (1 * 3) + (2 * 2) + (1 * 1) = 8.
```

**Example 2:**

```
Input: boxTypes = [[5,10],[2,5],[4,7],[3,9]], truckSize = 10
Output: 91
```

**Constraints**

- 1 <= boxTypes.length <= 1000
- 1 <= numberOfBoxesi, numberOfUnitsPerBoxi <= 1000
- 1 <= truckSize <= 106

---

## 题目（中文翻译）

你需要将若干箱子装上卡车。给定一个 **2D 数组（二维数组）** `boxTypes`，其中 `boxTypes[i] = [numberOfBoxesi, numberOfUnitsPerBoxi]` 表示第 `i` 种箱子的数量 `numberOfBoxesi` 以及每个箱子包含的单元数 `numberOfUnitsPerBoxi`。  
同时给定一个整数 `truckSize`，它是卡车能够容纳的**最大箱子数量**。只要装上的箱子总数不超过 `truckSize`，你可以自由选择任意箱子装上卡车。  

返回卡车上能够装载的**最大总单元数**。

## 示例

### 示例 1
**输入**  
`boxTypes = [[1,3],[2,2],[3,1]], truckSize = 4`  
**输出**  
`8`  
**解释**  
- 第一种箱子有 1 箱，每箱 3 单元。  
- 第二种箱子有 2 箱，每箱 2 单元。  
- 第三种箱子有 3 箱，每箱 1 单元。  

可以把所有第一种和第二种的箱子全部装上，再装一箱第三种的箱子。  
总单元数 = `(1 * 3) + (2 * 2) + (1 * 1) = 8`。

### 示例 2
**输入**  
`boxTypes = [[5,10],[2,5],[4,7],[3,9]], truckSize = 10`  
**输出**  
`91`

## 约束条件
- `1 <= boxTypes.length <= 1000`
- `1 <= numberOfBoxesi, numberOfUnitsPerBoxi <= 1000`
- `1 <= truckSize <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的装箱方案枚举一遍，找出单位数最多的那一种**。  
可以把每一种箱子看成一种“商品”，每种商品有 `numberOfBoxes` 件，每件商品的价值是 `numberOfUnitsPerBox`。  
我们的卡车相当于一个只能装 `truckSize` 件商品的**背包**，只要装的商品总件数不超过 `truckSize`，价值越大越好。

实现上可以：

1. 递归（或回溯）遍历每一种箱子取 0~`numberOfBoxes` 件的所有可能。
2. 累计已经装的箱子数量和得到的单位数。
3. 当装的箱子数量已经达到 `truckSize`，或者遍历完所有箱子类型时，更新全局最大单位数。

> **生活化类比**：把箱子想象成超市的货架，货架上每种商品都有若干件，每件商品上贴着“单件价值”。我们要在有限的购物车（只能装 `truckSize` 件）里挑选商品，使得购物车里商品的总价值最高。暴力解相当于把所有可能的挑选方式都写在纸上，逐一比较。

**为什么这个方法正确**  
因为我们遍历了**所有**合法的装箱组合，必然能找到价值最大的那一种。

**时间/空间复杂度**  
- 时间复杂度：  
  对于第 `i` 种箱子，需要尝试 `0~numberOfBoxes_i` 种取法。最坏情况下每种箱子都有 `k` 件（`k ≤ 1000`），而箱子种类数为 `n`（`n ≤ 1000`），于是总的尝试次数是 `O(k^n)`，指数级爆炸。用大白话说，就是**“随箱子种类的增加，时间会像滚雪球一样飞速增长”**，根本不可接受。
- 空间复杂度：  
  递归栈的深度等于箱子种类数 `n`，所以是 `O(n)`，在最坏情况下最多 1000 层。

#### 代码（Python）

```python
from typing import List

def maximumUnits_bruteforce(boxTypes: List[List[int]], truckSize: int) -> int:
    """
    暴力递归遍历所有可能的装箱方式
    """
    n = len(boxTypes)
    best = 0                     # 记录目前找到的最大单位数

    def dfs(idx: int, used: int, units: int):
        """
        idx   : 当前正在考虑的箱子种类下标
        used  : 已经装进卡车的箱子数量
        units : 已经获得的单位总数
        """
        nonlocal best
        # 如果卡车已满或所有种类都已考虑完，更新答案
        if used == truckSize or idx == n:
            best = max(best, units)
            return

        cnt, val = boxTypes[idx]               # 该种箱子的数量和每箱的单位数
        # 取 0 到 min(cnt, 剩余空间) 件
        max_take = min(cnt, truckSize - used)
        for take in range(max_take + 1):
            # 递归到下一种箱子
            dfs(idx + 1, used + take, units + take * val)

    dfs(0, 0, 0)
    return best
```

> 关键行注释已经写在代码里，直接运行即可看到结果（但对大数据会超时）。

#### 复杂度

- **时间复杂度**：`O(k^n)`（指数级），这里的 `k` 是每种箱子的最大件数，`n` 是箱子种类数。直观上就是“所有可能的组合数”。
- **空间复杂度**：`O(n)`，递归栈深度等于箱子种类数。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于枚举所有组合**。我们其实不需要尝试所有可能，只要**每次都把最有价值的箱子装上**，就能保证最终的单位数最大。原因如下：

1. **贪心原理**：只要还有空位，装 **单位数最高** 的箱子永远不会让后面还能装的箱子更好。因为后面的箱子单位数必然不超过当前箱子，换句话说，把一个低价值箱子换成一个高价值箱子，单位数必增或不变。
2. 因此，只要把箱子类型按照 **每箱单位数从大到小** 排序，然后依次取箱子，**尽可能多取**（受 `truckSize` 限制），即可得到最优解。

> **生活化类比**：想象你在超市里买零食，手里只有固定数量的购物袋（卡车容量），每种零食的“每袋价值”不同。要让购物袋里的价值最大，你应该先把最贵的零食装进去，装满后再考虑次贵的，如此往复。这样不需要尝试所有可能的装袋组合，只要一次遍历就能得到最佳。

**关键步骤**：

1. **排序**：`boxTypes.sort(key=lambda x: x[1], reverse=True)`，把每箱单位数从高到低排好。这里的 `lambda x: x[1]` 把第二个元素（单位数）当作排序依据，`reverse=True` 表示降序。
2. **遍历取箱**：遍历排好序的列表，对于每种箱子：
   - 计算还能装多少箱：`take = min(numberOfBoxes, remainingTruckSize)`。
   - 累加单位数：`totalUnits += take * numberOfUnitsPerBox`。
   - 更新剩余空间：`remainingTruckSize -= take`。
   - 若卡车已装满（`remainingTruckSize == 0`），提前结束循环。

#### 代码（Python）

```python
from typing import List

def maximumUnits(boxTypes: List[List[int]], truckSize: int) -> int:
    """
    贪心：先装单位数最多的箱子，直至卡车装满
    """
    # 1. 按每箱单位数降序排列
    boxTypes.sort(key=lambda x: x[1], reverse=True)   # 类比：把价值最高的商品排在最前面

    total_units = 0          # 累计得到的单位总数
    remaining = truckSize    # 卡车还能装的箱子数量

    for number, unit in boxTypes:   # 遍历每种箱子 (数量, 每箱单位数)
        if remaining == 0:           # 卡车已满，直接退出
            break

        # 这一次我们最多可以装多少箱？受两方面限制：箱子本身的数量 与 卡车剩余空间
        take = min(number, remaining)

        # 累加价值：取了 take 箱，每箱 unit 单位
        total_units += take * unit

        # 更新剩余空间
        remaining -= take

    return total_units
```

> 代码已加入中文注释，直接运行即可得到答案。

#### 复杂度

- **时间复杂度**：`O(n log n)`，其中 `n = len(boxTypes)`。主要花费在排序上（`log n` 是排序的比较次数），遍历本身是线性 `O(n)`。相较于暴力的指数级，**这已经是“几乎瞬间”**的速度。  
  - 大白话：如果有 1000 种箱子，排序大约只需要几千次比较，几乎可以在眨眼之间完成。
- **空间复杂度**：`O(1)`（不计输入本身的存储），只用了常数个额外变量。即使排序在某些语言内部需要额外的临时空间，Python 的原地排序 `list.sort` 也只使用了 `O(log n)` 的栈空间，仍然可以视作常数级。

---

## 心得

- **核心技巧**：**贪心 + 排序**。在“要在容量限制下最大化价值”这类问题中，**先选价值最高的** 往往是最直接、最有效的策略。
- **适用的题型**  
  1. *分配资源类*：如 “分配糖果”、 “最大化利润的股票买卖（一次交易）” 等，需要在有限资源下取最高收益。  
  2. *背包的特殊形式*：当每件物品的价值和重量呈单调比例（如每箱单位数相同，重量为箱子数量），可以用贪心代替完整背包 DP。  
  3. *任务调度*：如 “任务调度的最短完成时间”，常用 “按时长/收益比率排序” 的思路。

- **一句话总结**：**“把价值最高的装进去，装不下再换下一个”——贪心排序是解这类容量约束最大化问题的钥匙**。

---

## 反思

- **第一反应**：看到“最大化单位数”和“卡车容量”，自然想到背包问题。随后想到如果把价值最高的箱子先装，可能会更快。
- **最容易踩的坑**  
  1. **忘记提前退出**：遍历完所有箱子后仍继续循环会导致不必要的计算。  
  2. **边界条件**：`truckSize` 可能大于所有箱子总数，这时应返回所有箱子的总单位数；如果 `truckSize` 为 0，答案应是 0。  
  3. **排序方向写错**：如果把单位数升序排列，贪心思路就会失效，得到的结果会是最小而不是最大。
- **下次类似题的第一步**：先判断**“价值是否可以直接排序”**——如果每件物品的价值/重量比是单调的（或者题目已经暗示“取价值最高的”），就立刻采用**贪心 + 排序**，而不是直接考虑动态规划或暴力搜索。