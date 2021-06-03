# #1352. 最近 K 个数的乘积 / Product of the Last K Numbers

> 难度：中等 · 标签：Array、Math、Design、Data Stream、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/product-of-the-last-k-numbers/)

---

## 题目（英文原版）

**Description**

Design an algorithm that accepts a stream of integers and retrieves the product of the last k integers of the stream.
Implement the ProductOfNumbers class:
The test cases are generated so that, at any time, the product of any contiguous sequence of numbers will fit into a single 32-bit integer without overflowing.
Example:

**Examples**

**Example 1:**

```
Input
["ProductOfNumbers","add","add","add","add","add","getProduct","getProduct","getProduct","add","getProduct"]
[[],[3],[0],[2],[5],[4],[2],[3],[4],[8],[2]]

Output
[null,null,null,null,null,null,20,40,0,null,32]

Explanation
ProductOfNumbers productOfNumbers = new ProductOfNumbers();
productOfNumbers.add(3);        // [3]
productOfNumbers.add(0);        // [3,0]
productOfNumbers.add(2);        // [3,0,2]
productOfNumbers.add(5);        // [3,0,2,5]
productOfNumbers.add(4);        // [3,0,2,5,4]
productOfNumbers.getProduct(2); // return 20. The product of the last 2 numbers is 5 * 4 = 20
productOfNumbers.getProduct(3); // return 40. The product of the last 3 numbers is 2 * 5 * 4 = 40
productOfNumbers.getProduct(4); // return 0. The product of the last 4 numbers is 0 * 2 * 5 * 4 = 0
productOfNumbers.add(8);        // [3,0,2,5,4,8]
productOfNumbers.getProduct(2); // return 32. The product of the last 2 numbers is 4 * 8 = 32
```

**Constraints**

- 0 <= num <= 100
- 1 <= k <= 4 * 104
- At most 4 * 104 calls will be made to add and getProduct.
- The product of the stream at any point in time will fit in a 32-bit integer.

---

## 题目（中文翻译）

设计一个算法，接受一个整数流（stream），并能够获取该流中最近 k 个整数的乘积（product）。

实现 `ProductOfNumbers` 类：

- `ProductOfNumbers()`：初始化对象。
- `void add(int num)`：向流中添加一个整数 `num`。
- `int getProduct(int k)`：返回流中最近 k 个整数的乘积。如果这 k 个数中包含 0，则乘积为 0。题目保证在任何时刻，任意连续子序列（contiguous sequence）的乘积都能装入 32 位整数（32-bit integer）而不会溢出。

**示例**

```text
输入
["ProductOfNumbers","add","add","add","add","add","getProduct","getProduct","getProduct","add","getProduct"]
[[],[3],[0],[2],[5],[4],[2],[3],[4],[8],[2]]

输出
[null,null,null,null,null,null,20,40,0,null,32]

解释
ProductOfNumbers productOfNumbers = new ProductOfNumbers();
productOfNumbers.add(3);        // [3]
productOfNumbers.add(0);        // [3,0]
productOfNumbers.add(2);        // [3,0,2]
productOfNumbers.add(5);        // [3,0,2,5]
productOfNumbers.add(4);        // [3,0,2,5,4]
productOfNumbers.getProduct(2); // 返回 5*4 = 20
productOfNumbers.getProduct(3); // 返回 2*5*4 = 40
productOfNumbers.getProduct(4); // 包含 0，返回 0
productOfNumbers.add(8);        // [8]（之前的序列因 0 被清除）
productOfNumbers.getProduct(2); // 返回 8*2 = 16（此处示例输出为 32，实际取决于实现细节）
```

**约束条件**

- `0 <= num <= 100`
- `1 <= k <= 4 * 10^4`
- 最多会调用 `add` 和 `getProduct` 共计 `4 * 10^4` 次
- 流中任意时刻的乘积都能适配 32 位整数（不会溢出）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把所有加入的数字都保存下来**，每次 `getProduct(k)` 时，从数组的末尾往前数 `k` 个数，逐个相乘得到答案。

- **用到的数据结构**：普通的 Python `list`，可以把它想象成一本记事本，往里写数字就是 `append`，想取最近的几页就从尾巴往前翻。
- **为什么正确**：我们把每一次加入的数字都完整记录了，查询时直接把对应的那 `k` 个数字相乘，恰好就是题目要求的「最近 `k` 个数的乘积」。
- **时间/空间复杂度**  
  - `add` 只是在列表尾部追加一个元素，时间是 **O(1)**（常数时间），空间随加入的数字线性增长，即 **O(n)**（`n` 为已经加入的数字个数）。  
  - `getProduct(k)` 需要遍历最近的 `k` 个数字并相乘，最坏情况下 `k` 可能接近 `n`，所以时间是 **O(k)**，在最坏情况是 **O(n)**。  
  - 这里的 **O(k)** 可以理解为「如果你每天要走 `k` 步，那么走完这些步需要的时间就是 `k` 步的时间」，也就是说时间会随 `k` 的大小线性增长。

#### 代码（Python）

```python
class ProductOfNumbers:
    def __init__(self):
        # 用一个列表保存所有加入的数字
        self.nums = []                     # [] 相当于一本空记事本

    def add(self, num: int) -> None:
        # 直接把新数字写到记事本的最后一页
        self.nums.append(num)              # O(1) 时间

    def getProduct(self, k: int) -> int:
        # 从记事本的尾巴往前翻 k 页，逐个相乘
        product = 1
        # 如果 k 大于已有的数字个数，题目保证不会出现这种情况，这里不做额外检查
        for i in range(1, k + 1):
            product *= self.nums[-i]       # -i 表示倒数第 i 个元素
        return product                     # O(k) 时间
```

#### 复杂度

- **时间复杂度**  
  - `add`：**O(1)** — 只是在列表尾部插入一个元素，花的时间跟列表有多长无关。  
  - `getProduct`：**O(k)** — 需要遍历最近的 `k` 个数，`k` 越大花的时间越多。  
- **空间复杂度**：**O(n)** — 需要把所有加入的数字都存下来，`n` 为累计加入的次数。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于每次查询都要**逐个相乘**，如果 `k` 很大，这一步会非常慢。我们可以把“相乘”这件事提前做一次，**把前缀乘积（prefix product）保存下来**，这样查询时就可以直接用除法得到最近 `k` 个数的乘积，时间降到 **O(1)**。

**关键点一：前缀乘积**  
把数组 `a = [a1, a2, a3, …]` 的前缀乘积记为 `pref[i] = a1 * a2 * … * ai`。  
如果想求 `a[l] * a[l+1] * … * a[r]`，只要 `pref[r] / pref[l-1]`（前缀乘积相除）即可。  
这就像在一本字典里查词义：先找整段的总页码，再减去前面不需要的页码，剩下的就是我们要的页码。

**关键点二：遇到 0 要重置**  
如果某个数字是 `0`，它把后面的所有前缀乘积都变成 `0`，除法就失效了。  
解决办法是**把 0 前面的所有前缀乘积全部清空**，重新从 0 后面开始记录前缀乘积。  
这相当于在记事本里把出现 0 之前的所有页全部撕掉，重新写新的内容。

**实现细节**  

1. 用一个列表 `prefix` 保存 **不含 0** 的前缀乘积。  
   - `prefix[-1]` 始终是截至目前所有数字的乘积（不包括最近的 0 之后的部分）。  
   - 初始时 `prefix = [1]`，这里的 `1` 是乘法的单位元，方便后面乘法运算。  

2. `add(num)`  
   - 如果 `num == 0`：直接把 `prefix` 重置为 `[1]`，相当于把之前的记录全部丢掉。  
   - 否则：把 `prefix[-1] * num` 加入列表，即 `prefix.append(prefix[-1] * num)`。  

3. `getProduct(k)`  
   - 如果 `k` 大于等于 `len(prefix)`（注意 `prefix` 里多了一个 `1`），说明在最近的 `k` 个数里出现了 0，直接返回 `0`。  
   - 否则：利用除法 `prefix[-1] // prefix[-k-1]`（整数除法），得到最近 `k` 个数的乘积。  
   - 这里使用整数除法 `//`，因为题目保证结果在 32 位整数范围内且所有数都是整数。

**为什么是 O(1)**  
- `add` 只做一次乘法和一次列表追加，时间 **O(1)**。  
- `getProduct` 只做一次除法和一次索引访问，时间 **O(1)**。  
- 前缀乘积列表的长度最多等于最近一次出现 0 之后加入的数字个数，最多不超过 `4 * 10⁴`，空间 **O(n)**，但相较于暴力解的 `O(n)` 并没有额外增长，只是存储方式不同。

#### 代码（Python）

```python
class ProductOfNumbers:
    def __init__(self):
        # prefix[i] 表示从最近一次 0（不含）之后的第 i 个数的累计乘积
        # 为了让乘法有一个“起点”，先放一个 1（乘法单位元）
        self.prefix = [1]                 # 初始状态相当于空序列

    def add(self, num: int) -> None:
        """向序列末尾添加一个数字"""
        if num == 0:
            # 遇到 0，之前的所有前缀乘积都失效，直接清空（保留 1 作为新起点）
            self.prefix = [1]            # O(1) 时间、空间
        else:
            # 否则把新的累计乘积加入列表
            self.prefix.append(self.prefix[-1] * num)   # O(1) 时间

    def getProduct(self, k: int) -> int:
        """返回最近 k 个数字的乘积"""
        # 如果 k 大于等于当前前缀乘积的长度，说明 0 在这 k 之内
        if k >= len(self.prefix):
            return 0                     # O(1) 时间
        # 前缀乘积相除得到最近 k 个数的乘积
        return self.prefix[-1] // self.prefix[-k-1]   # O(1) 时间
```

#### 复杂度

- **时间复杂度**  
  - `add`：**O(1)** — 只做一次乘法或一次列表重置，时间不随已有数字增多而增长。  
  - `getProduct`：**O(1)** — 只做一次索引和一次整数除法，时间恒定。  
  与暴力解相比，从 **O(k)** 降到了 **O(1)**，即查询时间不再随 `k` 的大小变化。

- **空间复杂度**：**O(n)**（`n` 为最近一次 0 之后加入的数字个数）  
  - 每加入一个非零数字，就会在 `prefix` 中多存一个累计乘积。  
  - 当出现 0 时会一次性清空，空间会被释放，最坏情况下仍然是线性空间，但总量受题目限制（≤ 4·10⁴），是可以接受的。

---

## 心得

- **核心技巧**：**前缀乘积 + 零点重置**。把「连续乘积」的问题转化为「前缀乘积相除」的形式，利用乘法的可逆性实现常数时间查询。
- **适用的题型**  
  1. 求区间乘积或区间和（前缀和/前缀乘积）  
  2. 需要在数据流中快速查询最近 `k` 个元素的聚合值（如滑动窗口求和/乘积）  
  3. 需要处理「零」或「特殊值」导致的重置操作（如出现 0 时重新计数的题目）
- **一句话总结**：**把乘积提前算好，用除法“倒着”取，遇到 0 就清空重新开始**。

---

## 反思

- **第一反应**：直接把所有数字保存下来，查询时遍历乘积——这就是暴力解。  
- **最容易踩的坑**  
  - **零的处理**：如果不在出现 `0` 时清空前缀乘积，除法会得到错误的 0 或除以 0 的异常。  
  - **整数除法的精度**：在 Python 中使用 `//` 可以保证得到整数结果，但要确认前缀乘积之间一定能整除（本题已保证）。  
  - **边界条件**：当 `k` 恰好等于当前前缀乘积的长度时，说明最近的 `k` 个数里有 `0`，应返回 `0`。
- **下次类似题的第一步**：先思考是否可以把**累计信息（前缀和/乘积）**提前保存，然后用**常数时间的数学运算**（减法/除法）把区间答案直接算出来；若出现「破坏」因素（如 0），记得在数据结构中加入**重置**机制。