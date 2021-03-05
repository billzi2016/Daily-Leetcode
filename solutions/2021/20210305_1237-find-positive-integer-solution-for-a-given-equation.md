# #1237. 寻找给定方程的正整数解 / Find Positive Integer Solution for a Given Equation

> 难度：中等 · 标签：Math、Two Pointers、Binary Search、Interactive · [LeetCode 链接](https://leetcode.com/problems/find-positive-integer-solution-for-a-given-equation/)

---

## 题目（英文原版）

**Description**

Given a callable function f(x, y) with a hidden formula and a value z, reverse engineer the formula and return all positive integer pairs x and y where f(x,y) == z. You may return the pairs in any order.
While the exact formula is hidden, the function is monotonically increasing, i.e.:
The function interface is defined like this:
We will judge your solution as follows:

**Examples**

**Example 1:**

```
interface CustomFunction {
public:
  // Returns some positive integer f(x, y) for two positive integers x and y based on a formula.
  int f(int x, int y);
};
```

**Example 2:**

```
Input: function_id = 1, z = 5
Output: [[1,4],[2,3],[3,2],[4,1]]
Explanation: The hidden formula for function_id = 1 is f(x, y) = x + y.
The following positive integer values of x and y make f(x, y) equal to 5:
x=1, y=4 -> f(1, 4) = 1 + 4 = 5.
x=2, y=3 -> f(2, 3) = 2 + 3 = 5.
x=3, y=2 -> f(3, 2) = 3 + 2 = 5.
x=4, y=1 -> f(4, 1) = 4 + 1 = 5.
```

**Example 3:**

```
Input: function_id = 2, z = 5
Output: [[1,5],[5,1]]
Explanation: The hidden formula for function_id = 2 is f(x, y) = x * y.
The following positive integer values of x and y make f(x, y) equal to 5:
x=1, y=5 -> f(1, 5) = 1 * 5 = 5.
x=5, y=1 -> f(5, 1) = 5 * 1 = 5.
```

**Constraints**

- 1 <= function_id <= 9
- 1 <= z <= 100
- It is guaranteed that the solutions of f(x, y) == z will be in the range 1 <= x, y <= 1000.
- It is also guaranteed that f(x, y) will fit in 32 bit signed integer if 1 <= x, y <= 1000.

---

## 题目（中文翻译）

给定一个可调用函数 `f(x, y)`（内部实现隐藏）以及一个整数 `z`，请逆向推断该函数的公式，并返回所有满足 `f(x, y) == z` 的正整数对 `(x, y)`。答案的返回顺序可以任意。

虽然具体公式未知，但已知该函数在两个参数上**单调递增**（monotonically increasing），即当 `x1 ≤ x2` 且 `y1 ≤ y2` 时必有 `f(x1, y1) ≤ f(x2, y2)`。

函数接口定义如下：

```cpp
interface CustomFunction {
public:
  // 返回基于某隐藏公式的正整数 f(x, y)，其中 x 和 y 为正整数
  int f(int x, int y);
};
```

我们将按以下方式评判你的解法：

（评判细节在原题中给出，此处略）

### 示例

#### 示例 1

```cpp
interface CustomFunction {
public:
  // Returns some positive integer f(x, y) for two positive integers x and y based on a formula.
  int f(int x, int y);
};
```

#### 示例 2

**输入**：`function_id = 1, z = 5`  
**输出**：`[[1,4],[2,3],[3,2],[4,1]]`  
**解释**：`function_id = 1` 对应的隐藏公式为 `f(x, y) = x + y`。满足 `f(x, y) = 5` 的正整数 `(x, y)` 有：

- `x = 1, y = 4 → f(1, 4) = 1 + 4 = 5`
- `x = 2, y = 3 → f(2, 3) = 2 + 3 = 5`
- `x = 3, y = 2 → f(3, 2) = 3 + 2 = 5`
- `x = 4, y = 1 → f(4, 1) = 4 + 1 = 5`

#### 示例 3

**输入**：`function_id = 2, z = 5`  
**输出**：`[[1,5],[5,1]]`  
**解释**：`function_id = 2` 对应的隐藏公式为 `f(x, y) = x * y`。满足 `f(x, y) = 5` 的正整数 `(x, y)` 有：

- `x = 1, y = 5 → f(1, 5) = 1 * 5 = 5`
- `x = 5, y = 1 → f(5, 1) = 5 * 1 = 5`

### 约束

- `1 <= function_id <= 9`
- `1 <= z <= 100`
- 保证所有满足 `f(x, y) == z` 的解均在 `1 <= x, y <= 1000` 范围内
- 同时保证在 `1 <= x, y <= 1000` 时，`f(x, y)` 的结果能够放入 32 位有符号整数中

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的正整数 `(x, y)` 都枚举一遍，然后把每一对交给已知的 `f(x, y)` 计算，看看是否等于目标 `z`。  

- **使用的数据结构**：只需要两个普通的整数变量 `x`、`y`，以及一个装答案的列表 `res`。这里不需要任何高级结构，甚至不需要哈希表。  
- **生活化类比**：把 `f` 想成一本“黑盒子”计算器，我们只能把数字放进去，看到输出。暴力枚举就像把所有可能的钥匙（`x,y`）都试一遍，看看哪把钥匙能打开（使 `f(x,y)=z`）。  
- **为什么正确**：题目保证解一定落在 `1 ≤ x, y ≤ 1000` 的范围内。只要把这 1000×1000 = 10⁶ 对全部检查一遍，就一定能找到所有满足条件的组合，且不会漏掉。  

#### 代码（Python）

```python
# 假设已经有一个可调用对象 customfunction，提供方法 f(x, y)
# 这里我们用一个占位的类来演示，实际提交时 LeetCode 会直接给出实例。
class CustomFunction:
    def f(self, x: int, y: int) -> int:
        # 这里的实现仅作演示，真实环境下用户不可见
        return x + y   # 示例：function_id = 1 时的公式

def findSolution(customfunction: 'CustomFunction', z: int):
    """
    暴力枚举所有 1~1000 的正整数对，找出 f(x,y) == z 的组合
    """
    res = []                           # 用来存放答案的列表
    for x in range(1, 1001):           # 外层遍历 x
        for y in range(1, 1001):       # 内层遍历 y
            if customfunction.f(x, y) == z:   # 调用黑盒子
                res.append([x, y])   # 找到答案就加入结果
    return res
```

#### 复杂度  

- **时间复杂度**：`O(1000 × 1000) = O(10⁶)`。直观来说，就是要检查一百万次 `f(x,y)`，所以运行时间会随输入规模线性增长。  
- **空间复杂度**：`O(k)`，其中 `k` 为答案的数量。我们只保存满足条件的配对，除此之外几乎不占额外空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**两层循环**，即使 `z` 很小，也要遍历全部 10⁶ 对。观察题目给出的关键性质：

> `f(x, y)` 对 **x** 和 **y** 都是**单调递增**的。  
> 换句话说：当 `x` 增大时 `f(x, y)` 不会变小；同理 `y` 增大时 `f(x, y)` 也不变小。

利用单调性，我们可以把搜索空间压缩到 **O(1000)**，类似“在有序矩阵中查找目标值”的双指针技巧：

1. **从左上角或右上角开始**  
   - 设 `x = 1`（最小），`y = 1000`（最大）。此时 `f(x, y)` 已经是**可能的最大**值（因为 `y` 最大），而 `x` 最小。  
2. **比较 `f(x, y)` 与目标 `z`**  
   - 若 `f(x, y) == z`，说明找到了一个答案，记录后 **左移** `x += 1`（尝试更大的 `x`），因为 `y` 已经是当前行最大的，继续往左走会让 `f` 更小，错过其他解。  
   - 若 `f(x, y) < z`，说明当前 `f` 太小，需要 **增大** `x`（下移），因为增大 `x` 能让 `f` 增大。  
   - 若 `f(x, y) > z`，说明当前 `f` 太大，需要 **减小** `y`（左移），因为减小 `y` 能让 `f` 降低。  
3. **循环终止条件**  
   - 当 `x` 超过 1000 或 `y` 小于 1 时，搜索结束。

因为每一步要么 `x` 加 1，要么 `y` 减 1，最多执行 `1000 + 1000 = 2000` 次循环，远快于暴力的 10⁶ 次。

> **类比**：把 `f` 看成一张高度随坐标递增的山坡图，从右上角向左下角“滑坡”。每次根据当前高度与目标的关系决定往左走还是往下走，最终遍历到所有可能的等高线点。

#### 代码（Python）

```python
def findSolution(customfunction: 'CustomFunction', z: int):
    """
    双指针（Two Pointers）利用单调递增性质，在 O(1000) 时间内找出所有解。
    """
    res = []                       # 用来存放答案
    x, y = 1, 1000                 # 从左下角 (x 最小, y 最大) 开始

    while x <= 1000 and y >= 1:    # 只要坐标仍在合法范围内就继续
        cur = customfunction.f(x, y)   # 计算当前值
        if cur == z:               # 找到一个答案
            res.append([x, y])
            # 为了不重复，继续向右下移动：增大 x，保持 y 不变
            x += 1
        elif cur < z:              # 当前值太小，需要增大 x（下移）让 f 增大
            x += 1
        else:                      # cur > z，当前值太大，需要减小 y（左移）让 f 降低
            y -= 1
    return res
```

#### 复杂度  

- **时间复杂度**：`O(1000 + 1000) = O(2000) ≈ O(1)`（常数级）。因为每次循环只会让 `x` 增 1 或 `y` 减 1，最多执行 2000 次，和 `z` 的大小无关。相比暴力的 `O(10⁶)`，快了好几个数量级。  
- **空间复杂度**：`O(k)`，仍然只存放答案，其中 `k` 为满足条件的配对数。

---

## 心得

- **核心技巧**：利用函数的 **单调递增** 性质，用 **双指针**（也叫“从右上角往左下角扫”的技巧）把搜索空间从二维的 `1000×1000` 压到线性的 `2000`。  
- **适用的题型**：  
  1. “在单调递增矩阵中查找目标值”（LeetCode 240）  
  2. “两数之和的变形”——已知函数单调且只涉及正整数的情况  
  3. “寻找满足不等式的整数对”——如 `a * b <= target`（可用类似的双指针）  
- **一句话总结**：**“单调 + 双指针 = 线性搜索”**，把二维遍历变成一步步逼近目标。

---

## 反思

- **第一反应**：看到“函数单调递增”，本能想到二分搜索或双指针。最直观的做法是暴力枚举，但很快会想到利用单调性优化。  
- **最容易踩的坑**：  
  - 忘记 `x`、`y` 的取值范围是 **正整数**，不能让 `x` 或 `y` 变成 0 或负数。  
  - 在找到 `cur == z` 时，只移动 `x`（或只移动 `y）而不同时移动，可能导致重复计数或漏掉解。  
  - 对于某些隐藏的函数（如 `f(x,y)=x^2 + y^2`），仍然满足单调递增，双指针同样有效，只要保证搜索起点是 `(1, max)` 即可。  
- **下次遇到同类题**：第一步先确认函数或数组是否**单调**（递增/递减），如果是，就立刻考虑 **双指针** 或 **二分搜索** 来把搜索复杂度降到线性或对数级。这样可以避免盲目枚举，写出更高效的代码。