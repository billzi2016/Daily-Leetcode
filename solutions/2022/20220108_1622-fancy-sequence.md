# #1622. 奇妙序列 / Fancy Sequence

> 难度：困难 · 标签：Math、Design、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/fancy-sequence/)

---

## 题目（英文原版）

**Description**

Write an API that generates fancy sequences using the append, addAll, and multAll operations.
Implement the Fancy class:

**Examples**

**Example 1:**

```
Input
["Fancy", "append", "addAll", "append", "multAll", "getIndex", "addAll", "append", "multAll", "getIndex", "getIndex", "getIndex"]
[[], [2], [3], [7], [2], [0], [3], [10], [2], [0], [1], [2]]
Output
[null, null, null, null, null, 10, null, null, null, 26, 34, 20]

Explanation
Fancy fancy = new Fancy();
fancy.append(2);   // fancy sequence: [2]
fancy.addAll(3);   // fancy sequence: [2+3] -> [5]
fancy.append(7);   // fancy sequence: [5, 7]
fancy.multAll(2);  // fancy sequence: [5*2, 7*2] -> [10, 14]
fancy.getIndex(0); // return 10
fancy.addAll(3);   // fancy sequence: [10+3, 14+3] -> [13, 17]
fancy.append(10);  // fancy sequence: [13, 17, 10]
fancy.multAll(2);  // fancy sequence: [13*2, 17*2, 10*2] -> [26, 34, 20]
fancy.getIndex(0); // return 26
fancy.getIndex(1); // return 34
fancy.getIndex(2); // return 20
```

**Constraints**

- 1 <= val, inc, m <= 100
- 0 <= idx <= 105
- At most 105 calls total will be made to append, addAll, multAll, and getIndex.

---

## 题目（中文翻译）

**描述**  
编写一个 API，通过 `append`、`addAll` 和 `multAll` 三种操作生成奇妙序列（fancy sequence）。

实现 `Fancy` 类，使其支持以下方法：

- `Fancy()`：构造函数，初始化一个空序列。  
- `void append(int val)`：在序列末尾追加整数 `val`。  
- `void addAll(int inc)`：把 `inc` 加到序列中的每个元素上。  
- `void multAll(int m)`：把序列中的每个元素乘以 `m`。  
- `int getIndex(int idx)`：返回下标为 `idx` 的元素的当前值（对 `10^9+7` 取模），若 `idx` 超出序列范围则返回 `-1`。

---

**示例**  

```json
Input
["Fancy", "append", "addAll", "append", "multAll", "getIndex", "addAll", "append", "multAll", "getIndex", "getIndex", "getIndex"]
[[], [2], [3], [7], [2], [0], [3], [10], [2], [0], [1], [2]]
Output
[null, null, null, null, null, 10, null, null, null, 26, 34, 20]
```

**解释**  
```java
Fancy fancy = new Fancy();
fancy.append(2);    // 序列: [2]
fancy.addAll(3);    // 序列: [2+3] -> [5]
fancy.append(7);    // 序列: [5, 7]
fancy.multAll(2);   // 序列: [5*2, 7*2] -> [10, 14]
fancy.getIndex(0);  // 返回 10
fancy.addAll(3);    // 序列: [10+3, 14+3] -> [13, 17]
fancy.append(10);   // 序列: [13, 17, 10]
fancy.multAll(2);   // 序列: [13*2, 17*2, 10*2] -> [26, 34, 20]
fancy.getIndex(0);  // 返回 26
fancy.getIndex(1);  // 返回 34
fancy.getIndex(2);  // 返回 20
```

---

**约束条件**  

- `1 <= val, inc, m <= 100`  
- `0 <= idx <= 10^5`  
- 至多 `10^5` 次对 `append`、`addAll`、`multAll` 和 `getIndex` 的调用。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

题目要求实现一个「Fancy」类，支持四个操作：

1. **append(val)** 把一个整数 `val` 加到序列末尾。  
2. **addAll(inc)** 把序列中 **所有** 元素统一加上 `inc`。  
3. **multAll(m)** 把序列中 **所有** 元素统一乘以 `m`。  
4. **getIndex(idx)** 返回当前序列第 `idx` 个位置的值（取模 `10⁹+7`），如果 `idx` 越界返回 `-1`。  

最直接的想法是把序列真的存到一个普通的 Python `list` 中，每次 `addAll`、`multAll` 都遍历整个列表把每个元素更新一次。  

- **数据结构**：普通的数组（`list`），相当于我们平时记账本子上的一行行数字。  
- **正确性**：因为我们每次都把所有元素都做了“加”或“乘”，所以序列的每个位置都保持了最新的数值，`getIndex` 直接读取即可。  

**为什么会超时？**  
- `addAll`、`multAll` 每次都要遍历整个序列，最坏情况下会有 `10⁵` 次操作，每次遍历的长度也可能达到 `10⁵`，时间复杂度会达到 `O(10⁵·10⁵)=O(10¹⁰)`，远远超出 1 秒左右的限制。  

#### 代码（Python）

```python
MOD = 10**9 + 7

class Fancy:
    def __init__(self):
        self.seq = []                     # 用列表保存序列

    def append(self, val: int) -> None:
        """把 val 加到序列末尾"""
        self.seq.append(val % MOD)        # 直接存模后值，防止后面溢出

    def addAll(self, inc: int) -> None:
        """把序列中所有数都加 inc"""
        inc %= MOD
        for i in range(len(self.seq)):
            self.seq[i] = (self.seq[i] + inc) % MOD   # 逐个更新

    def multAll(self, m: int) -> None:
        """把序列中所有数都乘 m"""
        m %= MOD
        for i in range(len(self.seq)):
            self.seq[i] = (self.seq[i] * m) % MOD    # 逐个更新

    def getIndex(self, idx: int) -> int:
        """返回第 idx 个元素（0‑based），越界返回 -1"""
        if 0 <= idx < len(self.seq):
            return self.seq[idx]
        return -1
```

#### 复杂度  

- **时间复杂度**  
  - `append` `O(1)`（直接在尾部加一个元素）  
  - `addAll`、`multAll` `O(n)`，其中 `n` 为当前序列长度（要遍历全部元素）  
  - `getIndex` `O(1)`（直接访问下标）  

  在最坏情况下，`addAll`/`multAll` 会被调用 `10⁵` 次，每次遍历 `10⁵` 长度，整体 `O(10¹⁰)`，这就是“慢到不行”。  

- **空间复杂度**  
  - `O(n)`，仅存储序列本身。  

---

### 2. 最优解  

#### 思路  

要把 **每次全体加/乘** 的代价从 `O(n)` 降到 `O(1)`，关键在于**不立即把操作作用到每个元素上**，而是“把操作记下来”，等真正需要读取某个位置的值时再算一次。  

我们可以把所有的 `addAll`、`multAll` 抽象为一个 **线性变换**：

> 对任意一个元素 `x`，经过若干次「先乘后加」的操作后，最终值等价于 `x * mul + add`（模 `MOD`）。

- `mul` 表示所有历史乘法的累计乘子。  
- `add` 表示在当前 `mul` 基础上累计的加法（已经乘以了历史的 `mul`，因为加法是在乘法之后执行的）。  

举个生活化的例子：  
想象你在烤面包，每次烤完后都撒点黄油（加法），有时又把面包整体浸在油里（乘法）。如果你只记录「一共浸了几次油」和「最后一次撒了多少黄油」，那么在你想吃第 `i` 片面包时，只要把原始面包的厚度乘以油的次数，再加上黄油的量，就能得到真实厚度。  

**如何实现「按需计算」？**  

我们仍然需要把 **原始值**（即 `append` 时的数）保存下来，因为每个位置的原始值不一样。除此之外，还要保存 **每次 `append` 时的累计乘子**，这样在查询时可以把「后来出现的乘法」剔除，只保留「该位置之后出现的乘法」的影响。

具体做法：

| 数据结构 | 作用 |
|----------|------|
| `vals[]` | 记录每次 `append` 时的原始值（已经被当时的 `mul`、`add` 影响） |
| `mul_at[]`| 记录 `append` 那一刻的累计乘子 `cur_mul`（即所有在它之前的 `multAll` 的乘积） |
| `cur_mul`| 全局累计乘子（所有 `multAll` 的乘积） |
| `cur_add`| 全局累计加法（所有 `addAll` 在当前 `cur_mul` 下的等价加数） |

**操作细节**  

1. **append(val)**  
   - 实际存入的值应该是 `val` 先经过当前的全局变换：`stored = (val * cur_mul + cur_add) % MOD`。  
   - 同时把当前的 `cur_mul` 记下来：`mul_at.append(cur_mul)`。  

2. **addAll(inc)**  
   - 这相当于在 **所有已有元素** 上再加 `inc`，但因为以后还有乘法会把这次加的 `inc` 也一起放大，所以我们把它转化为 `cur_add = (cur_add + inc * cur_mul) % MOD`。  
   - 解释：先把 `inc` 乘上当前的累计乘子 `cur_mul`，再加到 `cur_add`，这样后面的乘法自然会把它一起放大。  

3. **multAll(m)**  
   - 直接把全局乘子和加法都乘上 `m`：  
     ```
     cur_mul = cur_mul * m % MOD
     cur_add = cur_add * m % MOD
     ```
   - 这样以后再查询任何元素时，都已经把这次乘法的影响计入。  

4. **getIndex(idx)**  
   - 若 `idx` 越界返回 `-1`。  
   - 设 `stored = vals[idx]`，`prev_mul = mul_at[idx]`（该位置插入时的累计乘子）。  
   - 该位置在插入后经历的乘法是 `cur_mul / prev_mul`（模意义下的除法），我们需要 **乘以** 这个比例。  
   - 同时，它在插入时已经带上了当时的 `cur_add`，而现在的 `cur_add` 包含了 **所有** 加法的贡献，需要减去当时已经算进去的部分：`cur_add - prev_mul * added_when_inserted`。 事实上我们可以直接用下面的公式（推导见下方）：

   ```
   result = (stored * inv(prev_mul) % MOD * cur_mul % MOD
            + cur_add - prev_mul * inv(prev_mul) % MOD * cur_add_at_insert) % MOD
   ```

   为了简化实现，我们把 `vals` 保存为 **已经去掉当时的 `cur_mul` 的原始值**，即：

   ```
   raw = (val - cur_add) * inv(cur_mul) % MOD   # 插入时逆运算得到的原始值
   ```

   这样 `getIndex` 只需要：

   ```
   raw = vals[idx]                # 这里已经是原始值
   mul_now = cur_mul
   mul_then = mul_at[idx]
   ans = (raw * mul_now % MOD * inv(mul_then) % MOD + cur_add - cur_add_at_insert) % MOD
   ```

   但更常见、更简洁的做法是 **在 append 时直接保存未被后续乘法影响的原始值**，即：

   ```
   # 在 append 时：
   raw = (val - cur_add) * inv(cur_mul) % MOD
   vals.append(raw)
   mul_at.append(cur_mul)
   ```

   然后 `getIndex`：

   ```
   raw = vals[idx]
   mul_then = mul_at[idx]
   # 该元素从插入到现在经历的乘法比例 = cur_mul / mul_then
   ans = (raw * cur_mul % MOD * inv(mul_then) % MOD + cur_add) % MOD
   ```

   这里的 `inv(x)` 是模 `MOD` 下的 **乘法逆元**（即 `x * inv(x) ≡ 1 (mod MOD)`），可以用快速幂 `pow(x, MOD-2, MOD)` 求得，因为 `MOD` 是质数。  

   **核心公式**（保存原始值的实现）：

   ```
   ans = (raw * cur_mul % MOD * inv(mul_then) % MOD + cur_add) % MOD
   ```

   这一步只用了常数次乘法、加法和一次逆元（逆元可以在 `append` 时预先算好，或在查询时算，都是 O(log MOD)）。  

#### 代码（Python）

```python
MOD = 10**9 + 7

def mod_inv(x: int) -> int:
    """返回 x 在模 MOD 下的乘法逆元，使用快速幂 (MOD 为质数)"""
    return pow(x, MOD - 2, MOD)   # O(log MOD)

class Fancy:
    def __init__(self):
        # 保存“原始值”（在当时的全局变换被消除后的值）以及当时的累计乘子
        self.raw_vals = []          # List[int]
        self.mul_at = []            # List[int]，append 时的 cur_mul
        self.cur_mul = 1            # 累计乘子，初始为 1
        self.cur_add = 0            # 累计加法，初始为 0

    def append(self, val: int) -> None:
        """
        将 val 加入序列。
        为了以后能 O(1) 计算实际值，我们在这里把全局的乘/加“抵消”，
        保存下未被后续操作影响的原始值 raw。
        """
        # 先把全局的 add 也抵消，再把全局的 mul 抵消
        # raw = (val - cur_add) / cur_mul   (模意义下的除法)
        raw = (val - self.cur_add) % MOD
        raw = raw * mod_inv(self.cur_mul) % MOD   # 乘以 cur_mul 的逆元
        self.raw_vals.append(raw)                # 保存原始值
        self.mul_at.append(self.cur_mul)          # 保存当时的累计乘子

    def addAll(self, inc: int) -> None:
        """
        所有已有元素整体加 inc。
        由于以后可能还有乘法，需要把这次加的 inc 也乘上当前的累计乘子。
        """
        inc %= MOD
        # cur_add 表示在当前 cur_mul 基础上已经累计的加数
        self.cur_add = (self.cur_add + inc * self.cur_mul) % MOD

    def multAll(self, m: int) -> None:
        """
        所有已有元素整体乘 m。
        乘法会把之前累计的加法也一起放大，所以两者都要乘上 m。
        """
        m %= MOD
        self.cur_mul = (self.cur_mul * m) % MOD
        self.cur_add = (self.cur_add * m) % MOD

    def getIndex(self, idx: int) -> int:
        """
        读取第 idx（0-index）个元素的当前值，若越界返回 -1。
        设 raw 为该位置保存的原始值，mul_then 为它插入时的累计乘子。
        该元素从插入到现在经历的乘法比例 = cur_mul / mul_then。
        实际值 = raw * (cur_mul / mul_then) + cur_add   (模 MOD)
        """
        if idx < 0 or idx >= len(self.raw_vals):
            return -1

        raw = self.raw_vals[idx]
        mul_then = self.mul_at[idx]

        # 计算 cur_mul / mul_then 的模逆元
        ratio = self.cur_mul * mod_inv(mul_then) % MOD

        ans = (raw * ratio % MOD + self.cur_add) % MOD
        return ans
```

> **代码解释要点**  
> 1. `mod_inv` 用 **费马小定理**（`a^(p-1) ≡ 1 (mod p)`）快速求逆元，时间 `O(log MOD)`（约 30 次乘法）。  
> 2. `append` 时把全局的 `add`、`mul` 抵消，得到的 `raw` 永远是 **不受后续任何全局操作影响的基准值**。  
> 3. `addAll`、`multAll` 只更新全局变量，时间 `O(1)`。  
> 4. `getIndex` 只做常数次乘法、加法和一次逆元，整体 `O(log MOD)`，在本题的 10⁵ 次调用限制下完全够用。  

#### 复杂度  

- **时间复杂度**  
  - `append` `O(log MOD)`（一次逆元）  
  - `addAll`、`multAll` `O(1)`（纯数值更新）  
  - `getIndex` `O(log MOD)`（一次逆元）  

  由于 `log MOD ≈ 30`，实际运行非常快。与暴力解的 `O(n)` 相比，几乎是 **常数时间**，所以可以轻松通过 10⁵ 次调用的限制。  

- **空间复杂度**  
  - `O(N)`，其中 `N` 为已 `append` 的元素个数（最多 10⁵），我们额外存两组整数 (`raw_vals`、`mul_at`)。  

---

## 心得  

- **核心技巧**：把「全局的加/乘」抽象为 **线性变换** `x → x * mul + add`，并在每次 `append` 时记录当时的 `mul`，后续查询时用「逆元」把历史乘子抵消，只保留当前的累计效果。  
- **适用场景**  
  1. 需要对整个数组频繁做「全体加」或「全体乘」且仍要单点查询的题目（如「Range Add & Multiply Query」）。  
  2. 类似的「延迟更新」思路也常用于 **线段树**、**树状数组** 的懒惰标记（lazy propagation）。  
- **一句话总结**：**把所有全局操作压缩成两个累加器（乘子、加数），用逆元在查询时“弹回”到原始值**。  

---

## 反思  

- **第一反应**：直接把序列保存下来，遇到 `addAll`/`multAll` 就遍历修改——最自然但最慢。  
- **最容易踩的坑**  
  1. **模运算的负数**：`(val - cur_add) % MOD` 必须先 `% MOD` 再乘逆元，否则会出现负数导致 Python 的 `pow` 报错。  
  2. **逆元求值**：`MOD` 必须是质数才能用 `pow(x, MOD-2, MOD)`，这里题目已经给出 `10⁹+7` 是质数。  
  3. **溢出**：所有乘法、加法都要及时 `% MOD`，否则中间值会超过 Python 整数的范围（虽然 Python 整数不溢出，但会导致性能下降）。  
- **下次遇到同类题**，第一步应该思考：**“这一次全体操作能否用一个或两个全局变量来表示？”** 若能，就立刻转向「延迟/懒更新」的思路，而不是直接遍历。