# #1603. 停车系统设计 / Design Parking System

> 难度：简单 · 标签：Design、Simulation、Counting · [LeetCode 链接](https://leetcode.com/problems/design-parking-system/)

---

## 题目（英文原版）

**Description**

Design a parking system for a parking lot. The parking lot has three kinds of parking spaces: big, medium, and small, with a fixed number of slots for each size.
Implement the ParkingSystem class:

**Examples**

**Example 1:**

```
Input
["ParkingSystem", "addCar", "addCar", "addCar", "addCar"]
[[1, 1, 0], [1], [2], [3], [1]]
Output
[null, true, true, false, false]

Explanation
ParkingSystem parkingSystem = new ParkingSystem(1, 1, 0);
parkingSystem.addCar(1); // return true because there is 1 available slot for a big car
parkingSystem.addCar(2); // return true because there is 1 available slot for a medium car
parkingSystem.addCar(3); // return false because there is no available slot for a small car
parkingSystem.addCar(1); // return false because there is no available slot for a big car. It is already occupied.
```

**Constraints**

- 0 <= big, medium, small <= 1000
- carType is 1, 2, or 3
- At most 1000 calls will be made to addCar

---

## 题目（中文翻译）

设计一个停车场的停车系统。停车场有三种停车位：大车位（big）、中车位（medium）和小车位（small），每种尺寸的车位数量在初始化时固定。

实现 `ParkingSystem` 类，使其能够处理以下操作：

- `ParkingSystem(int big, int medium, int small)`  
  构造函数，分别初始化大车位、中车位和小车位的数量。

- `bool addCar(int carType)`  
  当有相应类型的车位可用时，将车停入并返回 `true`，否则返回 `false`。  
  `carType` 的取值为 1（大车位）、2（中车位）或 3（小车位）。

示例 1：

```text
Input
["ParkingSystem", "addCar", "addCar", "addCar", "addCar"]
[[1, 1, 0], [1], [2], [3], [1]]

Output
[null, true, true, false, false]
```

**解释**  
```java
ParkingSystem parkingSystem = new ParkingSystem(1, 1, 0);
parkingSystem.addCar(1); // 返回 true，因为还有 1 个大车位可用
parkingSystem.addCar(2); // 返回 true，因为还有 1 个中车位可用
parkingSystem.addCar(3); // 返回 false，因为没有小车位
parkingSystem.addCar(1); // 返回 false，因为大车位已满
```
（以上代码仅为示例，实际实现语言可自行选择）

约束条件：

- `0 <= big, medium, small <= 1000`
- `carType` 只能是 1、2 或 3
- 最多会调用 `addCar` 方法 1000 次

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一种车位都“列出来”，比如：

- `big` 车位用一个长度为 `big` 的列表表示，列表里的每个元素代表一个具体的车位，`0` 表示空，`1` 表示已占用。  
- `medium`、`small` 同理。

当一辆车要进来时，根据 `carType`（1 = 大车，2 = 中车，3 = 小车）去对应的列表里 **从头遍历**，找到第一个 `0` 就把它改成 `1`，表示占用了一个车位；如果遍历完整个列表都没有 `0`，说明该种类的车位已经满了，返回 `false`。

> 类比：想象你在图书馆查找一本书的空位，你会从第一排一排排往后找，看到空位就坐下。这种“从前往后找空位”的方式就是暴力解。

这种方法 **一定能得到正确答案**，因为我们真的把每一个车位都检查了一遍，绝不会漏掉任何空位。

#### 代码（Python）

```python
class ParkingSystem:
    def __init__(self, big: int, medium: int, small: int):
        # 用列表模拟每一种车位，0 表示空，1 表示已占用
        self.big_spots = [0] * big
        self.medium_spots = [0] * medium
        self.small_spots = [0] * small

    def addCar(self, carType: int) -> bool:
        """尝试停入一辆车，返回是否成功"""
        if carType == 1:          # 大车
            spots = self.big_spots
        elif carType == 2:        # 中车
            spots = self.medium_spots
        else:                     # 小车（carType == 3）
            spots = self.small_spots

        # 暴力遍历寻找第一个空位
        for i in range(len(spots)):
            if spots[i] == 0:      # 找到空位
                spots[i] = 1       # 占用它
                return True
        # 没有空位了
        return False
```

#### 复杂度

- **时间复杂度**：`O(n)`，其中 `n` 是对应车种的车位总数。因为每次进车都要**线性遍历**一次列表，最坏情况下要检查所有车位。  
  > 大白话：如果有 10 个大车位，需要找空位时最多要看 10 次；如果车位很多，这个过程会变慢。

- **空间复杂度**：`O(n)`，我们用了三个列表来保存每个车位的占用情况，列表长度正好等于车位数。  
  > 大白话：需要的额外记忆和车位数量一样多。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在于遍历整个列表**——我们其实并不需要记住每一个具体的车位，只要知道还有多少空位即可。

- **核心观察**：每种车只会占用同一种车位，车位之间互不干扰。只要保存「剩余空位数」就能判断是否还能停车。
- **数据结构**：用三个整数（或一个长度为 3 的数组）分别记录大车、中车、小车当前还有多少可用车位。整数的查询、加减都是 **O(1)**，不需要遍历。

类比：这就像在图书馆的入口处挂了一个显示牌，实时写着“还有几张空座”。你不必进去每排每排找，只要看牌子上数字够不够就知道能不能坐下。

**实现步骤**：

1. 初始化时把每种车位的数量保存到 `self.spots`（长度为 3 的列表），下标 `0` 对应大车，`1` 对应中车，`2` 对应小车。  
2. `addCar(carType)` 时，把 `carType` 转换为列表下标 `carType-1`，检查对应的剩余数量是否大于 0。  
   - 若大于 0，说明还有空位，减一后返回 `True`。  
   - 否则返回 `False`。

整个过程只涉及 **常数次**的整数比较和加减，时间、空间都达到最优。

#### 代码（Python）

```python
class ParkingSystem:
    def __init__(self, big: int, medium: int, small: int):
        # 使用一个长度为 3 的列表记录剩余车位数
        # 下标 0 → 大车, 1 → 中车, 2 → 小车
        self.spots = [big, medium, small]

    def addCar(self, carType: int) -> bool:
        """
        尝试停入一辆车
        carType: 1（大车）、2（中车）、3（小车）
        返回 True 表示成功停入，False 表示已满
        """
        idx = carType - 1               # 转成 0/1/2 的下标
        if self.spots[idx] > 0:         # 还有空位吗？
            self.spots[idx] -= 1        # 占用一个
            return True
        return False                    # 已经没有空位
```

#### 复杂度

- **时间复杂度**：`O(1)` —— 只做一次整数比较和一次减法，**不随车位数量增长**。  
  > 大白话：不管停车场有 10 还是 10 000 个大车位，检查能否停下只需要看一眼数字，时间固定。

- **空间复杂度**：`O(1)` —— 只用了一个长度为 3 的固定列表，**不随输入规模变化**。  
  > 大白话：额外占用的记忆永远是三个数字，和车位多少毫无关系。

---

## 心得

- **核心技巧**：用计数器（整数）代替具体的集合/列表，省去遍历。  
- **适用题型**  
  1. 资源分配类（如「设计循环队列」的容量计数）。  
  2. 频次限制类（如「实现一个带限流的 API」）。  
  3. 简单模拟类（如「实现一个水池的加水/放水」）。  
- **一句话总结**：只要关心“还有多少”，用整数计数即可，遍历所有元素往往是多余的。

---

## 反思

- **第一反应**：把每个车位都列出来，用数组或列表保存占用情况，然后逐个检查。  
- **最容易踩的坑**  
  - **忘记把 `carType` 转成 0‑based 下标**，导致数组越界。  
  - **边界条件**：初始化时某种车位数为 0，需要直接返回 `False`，计数器方式自然可以处理。  
- **下次类似题的第一步**：先问自己「我到底需要知道每个元素的具体状态吗？」如果答案是「不需要」，立刻考虑用「计数」或「累计和」来压缩信息。