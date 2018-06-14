# #11. 盛最多水的容器 / Container With Most Water

> 难度：中等 · 标签：Array、Two Pointers、Greedy · [LeetCode 链接](https://leetcode.com/problems/container-with-most-water/)

---

## 题目（英文原版）

**Description**

You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).
Find two lines that together with the x-axis form a container, such that the container contains the most water.
Return the maximum amount of water a container can store.
Notice that you may not slant the container.

**Examples**

**Example 1:**

```
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.
```

**Example 2:**

```
Input: height = [1,1]
Output: 1
```

**Constraints**

- n == height.length
- 2 <= n <= 105
- 0 <= height[i] <= 104

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `height`。在坐标系中绘制 `n` 条竖直线，第 `i` 条线的两个端点为 `(i, 0)` 和 `(i, height[i])`。  
找出两条线，使它们与 x 轴共同形成的容器能够容纳最多的水。返回该容器可以存储的最大水量。  
注意，容器不能倾斜。

**示例 1**  
```
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: 上图中的竖直线对应数组 [1,8,6,2,5,4,8,3,7]。在这种情况下，容器能够盛装的最大水面积（蓝色部分）为 49。
```

**示例 2**  
```
Input: height = [1,1]
Output: 1
Explanation: 只有两条等高的线，能够形成的容器面积为 1。
```

**约束条件**  
- `n == height.length`  
- `2 <= n <= 10^5`  
- `0 <= height[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举**所有可能的两根竖线，算出它们能装多少水，最后取最大值。  
- **枚举**两根线相当于在数组 `height` 中挑选两个下标 `i` 和 `j (i < j)`，这跟在一排小树苗里挑两棵树很像。  
- 两根线之间的宽度是 `j - i`（相邻下标之间的距离），高度取决于两根线的**较矮**那根，因为水只能装到最短的那根的高度。  
- 所以面积 = `min(height[i], height[j]) * (j - i)`。  

**为什么正确**：  
对每一对下标我们都计算了它们能够形成的容器面积，最大值必然是答案。没有遗漏，也没有多算。

**时间/空间复杂度**：  
- 我们要遍历所有的 `(i, j)` 组合。第一个指针 `i` 可以有 `n` 种取法，第二个指针 `j` 在 `i` 之后还有至多 `n-1` 种取法，总共大约是 `n·(n-1)/2` 次计算。用大写的 **O(n²)** 来表示，意思是**随着数组长度 n 的增长，运算次数会呈二次方增长**（比如 n 从 10 增到 100，运算次数会从 100 左右升到 10,000 左右）。
- 只用了常数级别的额外空间（几个整数），所以是 **O(1)**。

#### 代码（Python）

```python
def maxArea_brute(height):
    """
    暴力枚举所有两根线，返回最大装水面积
    """
    n = len(height)
    max_water = 0                     # 记录目前找到的最大面积
    for i in range(n):                # 第一个指针 i 从左到右
        for j in range(i + 1, n):     # 第二个指针 j 必须在 i 的右边
            # 容器的高度取两根线的较小值
            h = min(height[i], height[j])
            # 容器的宽度是两根线的横坐标差
            w = j - i
            area = h * w               # 当前这对线能装的水量
            if area > max_water:       # 更新最大值
                max_water = area
    return max_water
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 需要遍历所有两两组合，运算次数随 `n` 的平方增长。  
- **空间复杂度**：`O(1)` —— 只用了几个临时变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**宽度**随指针之间的距离变大而变小，**高度**取决于两根线的较矮者。  
暴力解的瓶颈在于**重复计算**了很多不可能成为最优解的组合。我们可以用**双指针**一次遍历把这些无效的组合直接跳过。

**关键观察**：

1. **面积公式**：`area = min(height[l], height[r]) * (r - l)`  
   - `r - l` 是宽度，随指针向内收敛而 **只会变小**。  
   - `min(height[l], height[r])` 是高度，只有当我们把 **较矮的那根线** 移动到更高的线时，面积才有可能变大。

2. **为什么总是移动较矮的一侧**：  
   - 假设左侧 `height[l]` 更矮。当前面积受左侧高度限制，即 `area = height[l] * (r - l)`。  
   - 如果我们把右指针左移（即 `r--`），宽度会变小，而左侧高度不变，面积只能等于或更小，**不可能比当前更好**。  
   - 只有把左指针右移，才有机会找到更高的左线，提升 `min(height[l], height[r])`，从而抵消宽度的缩小，甚至得到更大的面积。  
   - 同理，如果右侧更矮，就移动右指针。

**算法步骤**：

1. 左指针 `l` 放在最左端，右指针 `r` 放在最右端。  
2. 计算当前面积，更新答案。  
3. 比较 `height[l]` 与 `height[r]`：  
   - 若 `height[l] < height[r]`，左指针右移 `l += 1`；  
   - 否则右指针左移 `r -= 1`。  
4. 重复步骤 2~3，直到 `l == r` 为止。

整个过程只遍历数组一次，**时间是线性的 O(n)**，空间仍是常数。

#### 代码（Python）

```python
def maxArea(height):
    """
    双指针贪心解法：一次遍历得到最大装水面积
    """
    l, r = 0, len(height) - 1          # 左右指针分别指向数组两端
    max_water = 0                       # 记录目前找到的最大面积

    while l < r:                        # 当两指针未相遇时继续
        # 当前容器的高度取左右较矮的那根
        h = min(height[l], height[r])
        # 宽度是指针之间的横坐标差
        w = r - l
        area = h * w                     # 计算面积
        if area > max_water:             # 更新最大值
            max_water = area

        # 移动较矮的一侧指针，尝试寻找更高的线
        if height[l] < height[r]:
            l += 1                        # 左指针右移
        else:
            r -= 1                        # 右指针左移

    return max_water
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只进行一次线性遍历，`n` 为数组长度。相比暴力的 `O(n²)`，运算次数从“平方级”降到了“线性级”，即 `n` 从 10 增到 100，运算次数只从 10 增到 100，而不是 10,000。  
- **空间复杂度**：`O(1)` —— 只使用了几个指针和临时变量，和输入规模无关。

---

## 心得

- **核心技巧**：**双指针 + 贪心**——在满足“宽度单调递减、只能提升较矮高度”这一约束下，始终移动较矮的一侧，保证不会错过最优解。  
- **适用的题型**：  
  1. `Trapping Rain Water`（接雨水）——同样涉及高度和宽度的关系。  
  2. `Valid Palindrome`（验证回文）——使用双指针从两端向中间比较。  
  3. `Three Sum Closest`（最接近的三数之和）——在排序后利用双指针寻找目标。  
- **一句话总结解题钥匙**：**“宽度只能变小，想让面积变大只能提升较矮那根的高度——所以每次把较矮的指针往里走”。**

---

## 反思

- **第一反应**：看到“找两根线形成最大面积”，本能想到**枚举所有组合**，因为最安全、最直接。  
- **最容易踩的坑**：  
  - 忘记在计算面积时使用 `min(height[l], height[r])`（取较矮的高度）。  
  - 误以为可以随意移动任意一侧指针，导致漏掉可能更大的解。  
  - 边界条件：数组长度恰好为 2 时，指针只移动一次，仍能得到正确答案。  
- **下次遇到同类题**：第一步先**思考“哪个量是单调的（只会增/只会减）”，然后**利用双指针把搜索空间一步步压缩**。这样往往能从 O(n²) 降到 O(n)。