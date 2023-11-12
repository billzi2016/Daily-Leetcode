# #2469. 温度转换 / Convert the Temperature

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/convert-the-temperature/)

---

## 题目（英文原版）

**Description**

You are given a non-negative floating point number rounded to two decimal places celsius, that denotes the temperature in Celsius.
You should convert Celsius into Kelvin and Fahrenheit and return it as an array ans = [kelvin, fahrenheit].
Return the array ans. Answers within 10-5 of the actual answer will be accepted.
Note that:

**Examples**

**Example 1:**

```
Input: celsius = 36.50
Output: [309.65000,97.70000]
Explanation: Temperature at 36.50 Celsius converted in Kelvin is 309.65 and converted in Fahrenheit is 97.70.
```

**Example 2:**

```
Input: celsius = 122.11
Output: [395.26000,251.79800]
Explanation: Temperature at 122.11 Celsius converted in Kelvin is 395.26 and converted in Fahrenheit is 251.798.
```

**Constraints**

- 0 <= celsius <= 1000

---

## 题目（中文翻译）

**描述**  
给定一个四舍五入到小数点后两位的非负浮点数 `celsius`，表示摄氏温度。  
你需要将摄氏温度转换为开尔文（Kelvin）和华氏温度（Fahrenheit），并以数组 `ans = [kelvin, fahrenheit]` 的形式返回。  
只要答案在实际值的 `10⁻⁵` 以内均视为正确。

**示例 1**  
Input: celsius = 36.50  
Output: [309.65000,97.70000]  
解释：36.50 摄氏度转换为开尔文是 309.65，转换为华氏度是 97.70。

**示例 2**  
Input: celsius = 122.11  
Output: [395.26000,251.79800]  
解释：122.11 摄氏度转换为开尔文是 395.26，转换为华氏度是 251.798。

**约束条件**  
- `0 <= celsius <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题唯一的要求是把摄氏温度 `celsius` 按照已知的公式分别换算成 **开尔文** 和 **华氏度**，然后把两个结果放进数组返回。

- **开尔文** 的换算公式：  
  \[
  K = C + 273.15
  \]
  把摄氏度直接加上 273.15 就得到开尔文。可以把它想象成在“温度表”上往右平移 273.15 格子。

- **华氏度** 的换算公式：  
  \[
  F = C \times \frac{9}{5} + 32
  \]
  先把摄氏度乘以 9/5（相当于把每一格拉长 1.8 倍），再加上 32（相当于把零点向上平移 32 度）。

> 这里没有需要遍历、搜索或递归的过程，所谓“暴力”其实就是直接套公式，算一次就完事。

#### 代码（Python）

```python
def convertTemperature(celsius: float):
    """
    将摄氏温度转换为开尔文和华氏度
    :param celsius: 摄氏温度，非负且保留两位小数
    :return: [kelvin, fahrenheit]，保留 5 位小数（LeetCode 会自动容忍误差 1e-5）
    """
    # 开尔文 = 摄氏度 + 273.15
    kelvin = celsius + 273.15          # + 就像在字典里查到对应的“页码”，直接相加得到新值

    # 华氏度 = 摄氏度 * 9/5 + 32
    fahrenheit = celsius * 9 / 5 + 32 # 先把温度拉伸 1.8 倍，再平移 32 度

    # 按题目要求返回一个列表
    return [kelvin, fahrenheit]
```

#### 复杂度  

- **时间复杂度**：`O(1)` — 只做了几次加减乘除，和输入大小无关。  
  *大白话*：不管你给多少温度，程序跑的时间都是一样的，几乎是瞬间完成。

- **空间复杂度**：`O(1)` — 只用了常量级的变量存放结果，不会随输入规模增长而占用更多内存。  

---

### 2. 最优解

#### 思路  

对这类“直接套公式” 的题目，**暴力解** 与 **最优解** 在本质上是一样的：唯一的瓶颈是**没有瓶颈**。我们唯一能优化的地方就是：

1. **避免不必要的精度损失**：在 Python 中使用浮点数运算时，直接使用 `float` 足够；若想更严格控制误差，可以在返回前使用 `round(..., 5)`，但 LeetCode 已经容忍 `1e-5` 的误差，直接返回即可。
2. **代码可读性**：把公式抽成变量，写清楚每一步的意义，让阅读者一眼就能看出是哪个公式。

因此，**最优解** 仍然是一次性套公式，只是把实现写得更清晰、注释更详细。

#### 代码（Python）

```python
def convertTemperature(celsius: float):
    """
    最优实现：一步完成摄氏 → 开尔文、华氏的转换
    """
    # 1. 计算开尔文
    #   开尔文 = 摄氏度 + 273.15
    kelvin = celsius + 273.15

    # 2. 计算华氏度
    #   华氏度 = 摄氏度 * 9/5 + 32
    fahrenheit = celsius * 9 / 5 + 32

    # 3. 返回结果列表（LeetCode 自动容忍 1e-5 的误差）
    return [kelvin, fahrenheit]
```

#### 复杂度  

- **时间复杂度**：`O(1)` — 只做常数次算术运算。与暴力解相同，只是实现更简洁。
- **空间复杂度**：`O(1)` — 只用常量空间存放两个结果。

---

## 心得

- **核心技巧**：熟记并正确使用温度换算公式（加法、乘除、常数平移）。
- **适用场景**：  
  1. 任何需要单位转换的数学题（如公里↔英里、秒↔分钟等）。  
  2. 直接使用已知公式求值的 “实现题” （如求圆的面积、体积等）。
- **一句话总结**：**公式即答案，直接套上去即可**。

## 反思

- **第一反应**：看到“把摄氏度转成开尔文和华氏度”，立刻想起学校学的两个换算公式，直接写出即可。
- **最容易踩的坑**：  
  - 忘记加上 273.15（导致开尔文偏小）。  
  - 华氏度的系数写成 `9/4` 或 `5/9`（会产生错误的比例）。  
  - 对于极端输入（如 `0` 或 `1000`），仍需保证公式不溢出——但浮点数范围足够大，这里不会出现问题。
- **下次类似题的第一步**：先在纸上写出 **“输入 → 目标公式 → 输出”** 的映射关系，确认公式无误后再落代码。