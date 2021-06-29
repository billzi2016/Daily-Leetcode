# #1381. **设计一个支持递增操作的栈** / Design a Stack With Increment Operation

> 难度：中等 · 标签：Array、Stack、Design · [LeetCode 链接](https://leetcode.com/problems/design-a-stack-with-increment-operation/)

---

## 题目（英文原版）

**Description**

Design a stack that supports increment operations on its elements.
Implement the CustomStack class:

**Examples**

**Example 1:**

```
Input
["CustomStack","push","push","pop","push","push","push","increment","increment","pop","pop","pop","pop"]
[[3],[1],[2],[],[2],[3],[4],[5,100],[2,100],[],[],[],[]]
Output
[null,null,null,2,null,null,null,null,null,103,202,201,-1]
Explanation
CustomStack stk = new CustomStack(3); // Stack is Empty []
stk.push(1);                          // stack becomes [1]
stk.push(2);                          // stack becomes [1, 2]
stk.pop();                            // return 2 --> Return top of the stack 2, stack becomes [1]
stk.push(2);                          // stack becomes [1, 2]
stk.push(3);                          // stack becomes [1, 2, 3]
stk.push(4);                          // stack still [1, 2, 3], Do not add another elements as size is 4
stk.increment(5, 100);                // stack becomes [101, 102, 103]
stk.increment(2, 100);                // stack becomes [201, 202, 103]
stk.pop();                            // return 103 --> Return top of the stack 103, stack becomes [201, 202]
stk.pop();                            // return 202 --> Return top of the stack 202, stack becomes [201]
stk.pop();                            // return 201 --> Return top of the stack 201, stack becomes []
stk.pop();                            // return -1 --> Stack is empty return -1.
```

**Constraints**

- 1 <= maxSize, x, k <= 1000
- 0 <= val <= 100
- At most 1000 calls will be made to each method of increment, push and pop each separately.

---

## 题目（中文翻译）

Design a stack that supports increment operations on its elements.

实现 `CustomStack` 类，使其具备以下功能：

- `CustomStack(int maxSize)`  
  初始化对象，`maxSize` 为栈的最大容量。

- `void push(int x)`  
  当栈未满时，将 `x` 压入栈顶。

- `int pop()`  
  弹出并返回栈顶元素。如果栈为空，返回 `-1`。

- `void inc(int k, int val)`  
  将栈底的 `k` 个元素（若元素不足 `k`，则全部元素）都增加 `val`。

---

### 示例 1

**输入**

```json
["CustomStack","push","push","pop","push","push","push","inc","inc","pop","pop","pop","pop"]
[[3],[1],[2],[],[2],[3],[4],[5,100],[2,100],[],[],[],[]]
```

**输出**

```json
[null,null,null,2,null,null,null,null,null,103,202,201,-1]
```

**解释**

```java
CustomStack stk = new CustomStack(3); // 栈为空 []
stk.push(1);                          // 栈变为 [1]
stk.push(2);                          // 栈变为 [1,2]
stk.pop();                            // 返回 2，栈变为 [1]
stk.push(2);                          // 栈变为 [1,2]
stk.push(3);                          // 栈变为 [1,2,3]
stk.push(4);                          // 栈仍为 [1,2,3]（已达到容量上限）
stk.inc(5, 100);                      // 栈变为 [101,102,103]
stk.inc(2, 100);                      // 栈变为 [201,202,103]
stk.pop();                            // 返回 103，栈变为 [201,202]
stk.pop();                            // 返回 202，栈变为 [201]
stk.pop();                            // 返回 201，栈变为 []
stk.pop();                            // 返回 -1，栈为空
```

---

### 约束条件

- `1 <= maxSize, x, k <= 1000`
- `0 <= val <= 100`
- 每个方法（`inc`、`push`、`pop`）至多被调用 `1000` 次。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

我们先把 **栈** 看成一根 **数组**（list），栈顶对应数组的最后一个位置，栈底对应数组的第一个位置。  
三种操作的最直接实现方式如下：

| 操作 | 直观做法 | 类比 |
|------|----------|------|
| `push(x)` | 把 `x` 加到数组的末尾（`append`） | 把一本新书放到书架最上面 |
| `pop()`   | 删除数组的最后一个元素并返回它（`pop`） | 把最上面的那本书拿下来 |
| `increment(k, val)` | 把数组前 `k`（或全部）个元素都加上 `val` | 给书架最底下的 `k` 本书都涂上颜色 |

> **为什么暴力法是对的？**  
> - `push` / `pop` 本身就是栈的基本定义，直接使用数组的 `append` / `pop` 完全符合。  
> - `increment` 只要把指定范围的每个元素都加上 `val`，就实现了“把栈底的 k 个元素都增加 val”。没有别的隐藏条件。

#### 代码（Python）

```python
class CustomStack:
    def __init__(self, maxSize: int):
        # 用一个列表模拟栈，最大容量 maxSize
        self.stack = []
        self.maxSize = maxSize

    def push(self, x: int) -> None:
        # 栈满了就不再加入
        if len(self.stack) < self.maxSize:
            self.stack.append(x)          # 把元素放到栈顶
        # 否则什么都不做（题目要求返回 None）

    def pop(self) -> int:
        if not self.stack:                # 栈为空返回 -1
            return -1
        return self.stack.pop()           # 删除并返回栈顶元素

    def increment(self, k: int, val: int) -> None:
        # 只对实际存在的前 k 个元素做加法
        limit = min(k, len(self.stack))
        for i in range(limit):            # 依次遍历栈底到第 k 个位置
            self.stack[i] += val          # 每个元素加上 val
```

#### 复杂度  

- **时间复杂度**  
  - `push` / `pop`：`O(1)`（只在列表末尾操作）  
  - `increment`：`O(k)`，因为要遍历前 `k` 个元素。若 `k` 接近栈大小 `n`，最坏是 `O(n)`。  
    > **大白话**：如果栈里有 1000 本书，`increment(1000, 5)` 要把每本书都抹 5 次颜色，工作量跟书的数量成正比。  

- **空间复杂度**  
  - 只用了一个列表保存栈内元素，最多 `maxSize` 个整数，`O(maxSize)`。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 `increment`：每次都要遍历 `k` 个元素，最坏情况会导致 **每次调用都是线性时间**。  
我们需要把这段遍历“搬到以后再做”，让 `increment` 本身变成 **常数时间**。  

**关键想法——延迟增量（lazy increment）**  

- 为每个可能的栈位置准备一个额外数组 `inc[]`，长度同 `maxSize`。  
- `inc[i]` 表示 **在第 `i` 个位置（从栈底算起）之上的所有元素** 需要额外加的值。  
- 当调用 `increment(k, val)` 时，只在 `inc[k-1]` 上加 `val`（如果 `k` 超出当前栈大小，就在栈顶对应的位置加）。这一步是 `O(1)`。  
- 真正把增量加到元素上，**在弹出元素 (`pop`) 时** 完成：  
  1. 取出栈顶元素 `x`。  
  2. 把 `inc[top]`（对应栈顶的累计增量）加到 `x` 上。  
  3. 把 `inc[top]` 的值 **向下传递** 给 `inc[top-1]`（因为底层的增量仍然对剩下的元素有效）。  

这样，所有的 `increment` 操作只在 `inc` 中记一笔，真正的加法在 `pop` 时一次性完成。  

**类比**：想象有一条传送带，想给前面几件商品统一加价。我们不把每件商品都立刻改价，而是把“这批商品整体加价多少”记录在一个标签上。等到商品离开传送带（`pop`）时，再把标签上的加价算进去。

#### 代码（Python）

```python
class CustomStack:
    def __init__(self, maxSize: int):
        # 栈本体，保存真实的数值（未加上延迟增量）
        self.stack = []
        # inc[i] 表示「截至当前栈顶，位于 i 位置的元素」需要额外加的值
        self.inc = [0] * maxSize
        self.maxSize = maxSize

    def push(self, x: int) -> None:
        if len(self.stack) < self.maxSize:      # 栈未满才可以压入
            self.stack.append(x)                # 只存原始值，增量留在 inc 中

    def pop(self) -> int:
        if not self.stack:                      # 空栈返回 -1
            return -1

        idx = len(self.stack) - 1               # 栈顶在数组中的下标
        inc_val = self.inc[idx]                 # 取出累计的延迟增量
        if idx > 0:
            # 把这份增量向下传递给下一个元素（因为它仍然对剩余元素有效）
            self.inc[idx - 1] += inc_val
        # 清除当前位的增量记录
        self.inc[idx] = 0

        # 真正的返回值 = 原始值 + 累计增量
        return self.stack.pop() + inc_val

    def increment(self, k: int, val: int) -> None:
        # 只对实际存在的前 k 个位置做标记
        limit = min(k, len(self.stack)) - 1    # 最后受影响的位置下标
        if limit >= 0:                         # 若栈非空
            self.inc[limit] += val             # 在该位置记录一次增量
```

#### 复杂度  

- **时间复杂度**  
  - `push`：`O(1)`（直接 `append`）  
  - `pop`：`O(1)`（只做常数次加法和下标运算）  
  - `increment`：`O(1)`（只在 `inc` 的一个位置加 `val`）  
  > 与暴力解相比，**所有操作都变成常数时间**，即使 `increment` 的 `k` 很大也不会导致遍历。  

- **空间复杂度**  
  - 额外使用了一个长度为 `maxSize` 的 `inc` 数组，整体仍是 `O(maxSize)`。  
  - 与暴力解相比，只多了一个同等规模的整数数组，空间开销是线性的、可接受的。  

---

## 心得  

- **核心技巧**：**延迟增量（lazy increment） + 额外的辅助数组**。  
- **适用场景**：  
  1. 需要对「前缀」或「后缀」批量修改但希望每次操作保持 `O(1)`（如 “设计一个支持 `addToPrefix` 的数组”）。  
  2. 需要在栈/队列上做累计操作但只在弹出时真正计算（如 “设计一个支持 `inc` 的队列”）。  
- **一句话总结**：把“批量加”记在一个单独的标记里，等元素出栈时再统一算上去。  

---

## 反思  

- **第一反应**：直接遍历前 `k` 个元素，像平常的数组操作一样写 `for` 循环。  
- **最容易踩的坑**：  
  - `increment` 时忘记 `k` 可能大于当前栈大小，需要取 `min(k, size)`。  
  - 在 `pop` 时忘记把累计的增量向下传递，导致后面的元素少加了值。  
  - `inc` 数组需要与最大容量等长，不能随栈大小缩小，否则下标越界。  
- **下次类似题**：第一步先思考“有没有办法把耗时的遍历推迟到必须返回结果的时刻”，如果可以，用 **标记+懒计算** 的思路。