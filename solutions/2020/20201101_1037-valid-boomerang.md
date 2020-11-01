# #1037. 有效的回旋镖 / Valid Boomerang

> 难度：简单 · 标签：Array、Math、Geometry · [LeetCode 链接](https://leetcode.com/problems/valid-boomerang/)

---

## 题目（英文原版）

**Description**

Given an array points where points[i] = [xi, yi] represents a point on the X-Y plane, return true if these points are a boomerang.
A boomerang is a set of three points that are all distinct and not in a straight line.

**Examples**

**Example 1:**

```
Input: points = [[1,1],[2,3],[3,2]]
Output: true
```

**Example 2:**

```
Input: points = [[1,1],[2,2],[3,3]]
Output: false
```

**Constraints**

- points.length == 3
- points[i].length == 2
- 0 <= xi, yi <= 100

---

## 题目（中文翻译）

给定一个数组 `points`，其中 `points[i] = [xi, yi]` 表示平面直角坐标系（X‑Y plane）上的一个点，返回 `true` 当且仅当这三个点能够构成回旋镖（boomerang）。  
回旋镖是指由 **三个** **互不相同** 的点且这三点 **不在同一直线** 上组成的集合。

**示例 1**  
Input: points = [[1,1],[2,3],[3,2]]  
Output: true  

**示例 2**  
Input: points = [[1,1],[2,2],[3,3]]  
Output: false  

**约束条件**  
- `points.length == 3`  
- `points[i].length == 2`  
- `0 <= xi, yi <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
我们要判断 **三点是否在同一直线上**。  
最直观的办法是把两两之间的斜率算出来，然后比较斜率是否相等。  

- **斜率** = (y₂‑y₁) / (x₂‑x₁)  
- 如果 `points[0]‑points[1]` 的斜率和 `points[0]‑points[2]` 的斜率相同，说明三点共线，**不是** boomerang。  
- 否则三点不共线，就是 boomerang。  

> 类比：斜率就像字典里“词→解释”的映射。我们把每一对点看成一个“词”，对应的斜率是“解释”。如果两个词的解释相同（斜率相同），说明它们指向同一个方向——也就是共线。  

**正确性**：  
- 对于两条不平行的直线，它们的斜率一定不相等。  
- 当三点不共线时，任意选取的两条连线必不平行，斜率必不同。  

**复杂度分析**：  
- 只需要算两次斜率，时间是 **O(1)**（常数时间），因为点的数量固定为 3。  
- 只用到常数级的额外变量，空间是 **O(1)**。  
> 这里的 O(1) 可以理解为“无论输入多大，花的时间和空间都几乎不变”。  

#### 代码（Python）  

```python
from typing import List

def isBoomerang(points: List[List[int]]) -> bool:
    # 取出三个点的坐标，便于阅读
    x1, y1 = points[0]
    x2, y2 = points[1]
    x3, y3 = points[2]

    # 计算两条向量的斜率，分子分母都放在一起，避免除零错误
    # (y2 - y1) / (x2 - x1) 与 (y3 - y1) / (x3 - x1) 相等 ⇔ 两向量共线
    # 为避免浮点数误差，用交叉相乘的方式比较
    # 交叉相乘后： (y2 - y1)*(x3 - x1) == (y3 - y1)*(x2 - x1) 说明共线
    return (y2 - y1) * (x3 - x1) != (y3 - y1) * (x2 - x1)
```

#### 复杂度  

- **时间复杂度**：`O(1)` — 只做了几次加减乘除，跟输入规模无关。  
- **空间复杂度**：`O(1)` — 只用了几个临时变量，额外空间不随输入增长。  

---  

### 2. 最优解  

#### 思路  
虽然上面的暴力解已经是 **O(1)**，但我们可以把它用更几何化的语言表述：**三点组成的三角形面积是否为零**。  

- 两条向量的 **叉积（cross product）** 的绝对值正好等于它们构成的平行四边形面积。  
- 三角形面积是叉积的一半。  
- 只要叉积不为零，三角形面积就非零，说明三点不共线，即为 boomerang。  

**为什么叉积能判断共线**：  
- 在平面上，向量 `AB = (x2‑x1, y2‑y1)`、`AC = (x3‑x1, y3‑y1)`。  
- 叉积公式：`AB × AC = (x2‑x1)*(y3‑y1) - (y2‑y1)*(x3‑x1)`。  
- 如果结果为 0，说明两向量平行（共线），面积为 0。  

**优化点**：  
- 直接使用叉积避免了除法（斜率除零问题），更稳健。  
- 代码只写一次判断，逻辑更清晰。  

#### 代码（Python）  

```python
from typing import List

def isBoomerang(points: List[List[int]]) -> bool:
    # 解包三个点
    x1, y1 = points[0]
    x2, y2 = points[1]
    x3, y3 = points[2]

    # 计算向量 AB 和 AC 的叉积
    cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

    # 叉积不为 0 表示面积非零，即不是共线
    return cross != 0
```

#### 复杂度  

- **时间复杂度**：`O(1)` — 只做了常数次加减乘，仍然是最快的。  
- **空间复杂度**：`O(1)` – 只用了几个整数变量。  
> 与暴力解相比，时间和空间都没有变化，但代码可读性更好，且避免了除法可能带来的精度或除零问题。  

---  

## 心得  

- 这道题的核心是 **判断三点是否共线**，本质上是求**面积是否为零**。  
- 适用的技巧：  
  1. **斜率比较**（适用于任意两点的共线判断）。  
  2. **叉积（向量叉乘）**（几何中判断平行、面积、方向的常用工具）。  
  3. **面积公式**（如 Shoelace formula 用于多边形面积）。  
- **一句话总结解题钥匙**：`用叉积判断是否共线，非零即为 boomerang`。  

---  

## 反思  

- **第一反应**：想到用斜率或面积公式来判断三点是否在一条直线上。  
- **最容易踩的坑**：  
  - 斜率除以零的情况（两点 x 相同）。  
  - 浮点数精度误差（如果使用除法）。  
  - 忘记把三点全部都要 **不同**（题目要求“distinct”，但输入已保证）。  
- **下次遇到类似题**，第一步应该想到 **“用向量叉积判断共线或面积是否为零”**，因为它既避免除零又不产生浮点误差。