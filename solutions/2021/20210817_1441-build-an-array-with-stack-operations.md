# #1441. **构建数组的栈操作** / Build an Array With Stack Operations

> 难度：中等 · 标签：Array、Stack、Simulation · [LeetCode 链接](https://leetcode.com/problems/build-an-array-with-stack-operations/)

---

## 题目（英文原版）

**Description**

You are given an integer array target and an integer n.
You have an empty stack with the two following operations:
You also have a stream of the integers in the range [1, n].
Use the two stack operations to make the numbers in the stack (from the bottom to the top) equal to target. You should follow the following rules:
Return the stack operations needed to build target following the mentioned rules. If there are multiple valid answers, return any of them.

**Examples**

**Example 1:**

```
Input: target = [1,3], n = 3
Output: ["Push","Push","Pop","Push"]
Explanation: Initially the stack s is empty. The last element is the top of the stack.
Read 1 from the stream and push it to the stack. s = [1].
Read 2 from the stream and push it to the stack. s = [1,2].
Pop the integer on the top of the stack. s = [1].
Read 3 from the stream and push it to the stack. s = [1,3].
```

**Example 2:**

```
Input: target = [1,2,3], n = 3
Output: ["Push","Push","Push"]
Explanation: Initially the stack s is empty. The last element is the top of the stack.
Read 1 from the stream and push it to the stack. s = [1].
Read 2 from the stream and push it to the stack. s = [1,2].
Read 3 from the stream and push it to the stack. s = [1,2,3].
```

**Example 3:**

```
Input: target = [1,2], n = 4
Output: ["Push","Push"]
Explanation: Initially the stack s is empty. The last element is the top of the stack.
Read 1 from the stream and push it to the stack. s = [1].
Read 2 from the stream and push it to the stack. s = [1,2].
Since the stack (from the bottom to the top) is equal to target, we stop the stack operations.
The answers that read integer 3 from the stream are not accepted.
```

**Constraints**

- 1 <= target.length <= 100
- 1 <= n <= 100
- 1 <= target[i] <= n
- target is strictly increasing.

---

## 题目（中文翻译）

你得到一个整数数组 `target` 和一个整数 `n`。  
你有一个空栈，并且只能使用以下两种栈操作（stack operations）：

* `Push`：将当前读取的整数压入栈中。  
* `Pop`：弹出栈顶的整数。

同时，你还有一个整数流，包含区间 `[1, n]` 内的所有整数，按照递增顺序依次出现。  
利用这两种栈操作，使得栈中从底部到顶部的元素序列恰好等于 `target`。需要遵循以下规则：

* 按照整数流的顺序读取数字，决定是 `Push` 还是 `Pop`。  
* 当栈的内容（从底部到顶部）已经与 `target` 完全相同，即可停止操作。  

返回构造 `target` 所需的操作序列。如果存在多个合法答案，返回任意一个即可。

---

**示例 1**  
**输入**: `target = [1,3]`, `n = 3`  
**输出**: `["Push","Push","Pop","Push"]`  
**解释**: 初始时栈 `s` 为空，栈顶为最后一个元素。  
1. 从流中读取 `1` 并 `Push` 到栈中。`s = [1]`。  
2. 从流中读取 `2` 并 `Push` 到栈中。`s = [1,2]`。  
3. `Pop` 栈顶元素。`s = [1]`。  
4. 从流中读取 `3` 并 `Push` 到栈中。`s = [1,3]`。

**示例 2**  
**输入**: `target = [1,2,3]`, `n = 3`  
**输出**: `["Push","Push","Push"]`  
**解释**: 初始时栈 `s` 为空，栈顶为最后一个元素。  
1. 读取 `1` 并 `Push`。`s = [1]`。  
2. 读取 `2` 并 `Push`。`s = [1,2]`。  
3. 读取 `3` 并 `Push`。`s = [1,2,3]`。

**示例 3**  
**输入**: `target = [1,2]`, `n = 4`  
**输出**: `["Push","Push"]`  
**解释**: 初始时栈 `s` 为空，栈顶为最后一个元素。  
1. 读取 `1` 并 `Push`。`s = [1]`。  
2. 读取 `2` 并 `Push`。`s = [1,2]`。  
此时栈（从底部到顶部）的内容已经等于 `target`，停止操作。

---

**约束条件**

- `1 <= target.length <= 100`  
- `1 <= n <= 100`  
- `1 <= target[i] <= n`  
- `target` 严格递增。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

我们先把题目想象成**“把流水线上的数字一个一个拿出来，用栈把想要留下的数字保存下来”**。  
- **栈**：就像一叠盘子，最上面的盘子最先被取走（后进先出）。  
- **Push**：把当前数字放到栈顶。  
- **Pop**：把栈顶的盘子拿走（相当于“丢弃”这个数字）。  

最直接的做法是：  
1. 对目标数组 `target` 的每一个元素 `t`，从上一次已经处理过的数字 `prev+1` 开始，依次读取流水线的数字 `i`。  
2. 每读到一个 `i`，先 **Push** 到栈。  
3. 如果 `i` 正好等于 `t`，说明这个数字要保留下来，直接进入下一个目标元素的处理。  
4. 如果 `i` 小于 `t`，说明它不是目标，需要 **Pop** 把它弹出。  

这样把 **每个目标元素** 都单独循环一次，最坏情况下会出现两层循环（外层遍历 `target`，内层遍历 `i`），时间复杂度是 `O(n * m)`，其中 `n = len(target)`，`m = n`（因为 `i` 最多跑到 `n`），于是最坏是 `O(n²)`。  

**为什么正确？**  
- 我们严格按照数字顺序（从 1 到 n）读取，因为题目要求只能按这个顺序从流中取数。  
- 对每个读取的数字我们都执行了 **Push**，确保栈里始终记录了我们已经看到的所有数字。  
- 对于不在目标里的数字立即 **Pop**，所以最终栈中留下的恰好是目标数组的元素，且顺序和题目要求一致（从栈底到栈顶即目标数组本身）。  

#### 代码（Python）  

```python
def buildArray_brute(target, n):
    """
    暴力实现：对每个目标元素都单独遍历一次
    返回所有操作的列表，如 ["Push","Push","Pop","Push"]
    """
    ops = []            # 用来保存所有操作指令
    prev = 0            # 已经处理到的最大数字，初始为 0

    for t in target:                # 逐个目标数字
        # 从 prev+1 开始，一直读取到 t
        for i in range(prev + 1, t + 1):
            ops.append("Push")      # 先把 i 放进栈
            if i != t:              # 不是目标数字，需要丢掉
                ops.append("Pop")
        prev = t                    # 更新已处理的最大数字
    return ops
```

#### 复杂度  

- **时间复杂度：** `O(n²)`（最坏情况下 `target` 长度接近 `n`，内层循环会遍历 `1…n`）  
  - 这里的 `O(n²)` 并不是说真的要跑几亿次，而是说 **“两层循环”**，对初学者来说可以理解为“会比线性快慢很多”。  
- **空间复杂度：** `O(1)`（除去返回的操作列表，算法本身只用常数级的额外变量）。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**慢的地方在于每次都要从 `prev+1` 再遍历到目标数字 `t`**。其实我们不需要每次重新循环，只要一次遍历 **所有可能的数字**（`1 … n`），在遍历的过程中判断当前数字是否应该保留即可。  

**关键观察**：  
- `target` 是严格递增的（题目保证），所以我们可以用一个指针 `i` 指向 `target` 的当前位置。  
- 当遍历到的数字 `num` 正好等于 `target[i]` 时，说明它是目标，需要 **Push** 并把指针向后移动（`i += 1`）。  
- 当 `num` 小于 `target[i]` 时，说明它不在目标里，只需要 **Push** 再 **Pop**（相当于 “读取但丢弃”）。  
- 当指针已经走到 `target` 末尾时，说明目标已经全部构造完，直接停止遍历即可（不必继续读取后面的数字）。  

这样只需要 **一次线性遍历**，时间复杂度降到 `O(n)`，空间仍然是 `O(1)`（除了返回列表）。  

**类比**：想象你在超市排队买东西，**目标清单**是 `target`，而超市的商品是从 1 到 n 按顺序摆放的货架。你一次走过货架，遇到清单里需要的商品就买（Push），不需要的就直接放回原位（Push+Pop），走完清单后就可以离开。  

#### 代码（Python）  

```python
def buildArray(target, n):
    """
    最优实现：一次遍历 1..n，使用指针指向 target 中当前要匹配的元素。
    返回操作序列。
    """
    ops = []                # 记录操作指令
    idx = 0                 # target 的指针，指向下一个待匹配的数字

    # 遍历可能出现的每个数字
    for num in range(1, n + 1):
        if idx == len(target):          # 已经全部匹配完目标，直接结束
            break

        if num == target[idx]:          # 正好是目标数字，保留下来
            ops.append("Push")
            idx += 1                    # 移动到下一个目标数字
        else:                           # 不是目标，需要读进来再丢掉
            ops.append("Push")
            ops.append("Pop")
    return ops
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 只遍历一次 `1…n`（最多 100 次），每次只做常数时间的判断和记录操作。  
  - 与暴力解的 `O(n²)` 相比，**快了一个量级**，在大数据下差距会非常明显。  

- **空间复杂度：** `O(1)`（不计返回的操作列表，仅使用几个指针变量）。  

---  

## 心得  

- **核心技巧**：**一次遍历 + 双指针**（一个遍历数字流，一个遍历目标数组）。  
- **适用的题型**：  
  1. 需要按顺序处理两个已排序序列的题目（如合并两个有序数组）。  
  2. “模拟”类题目，需要按照给定顺序产生操作序列（如 “用栈模拟队列”）。  
- **解题钥匙**：**“把两个序列同步走，一步一步决定是保留还是丢弃”。**  

## 反思  

- **第一反应**：看到“栈”和“Push/Pop”，第一时间会想到每读一个数都要 **Push**，然后判断要不要 **Pop**。  
- **最容易踩的坑**：  
  - 忘记在目标全部匹配后提前停止遍历，会继续产生无意义的操作。  
  - 没考虑 `target` 长度可能小于 `n`，导致不必要的循环。  
  - 对指针的移动顺序写反，导致出现多余的 `Pop`。  
- **下次类似题的第一步**：先画出 **“读取流 → 决策保留/丢弃”** 的流程图，明确每一步只需要一次遍历，然后再写代码。