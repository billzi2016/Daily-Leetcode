# #2582. 传递枕头 / Pass the Pillow

> 难度：简单 · 标签：Math、Simulation · [LeetCode 链接](https://leetcode.com/problems/pass-the-pillow/)

---

## 题目（英文原版）

**Description**

There are n people standing in a line labeled from 1 to n. The first person in the line is holding a pillow initially. Every second, the person holding the pillow passes it to the next person standing in the line. Once the pillow reaches the end of the line, the direction changes, and people continue passing the pillow in the opposite direction.
Given the two positive integers n and time, return the index of the person holding the pillow after time seconds.
Note: This question is the same as  3178: Find the Child Who Has the Ball After K Seconds.

**Examples**

**Example 1:**

```
Input: n = 4, time = 5
Output: 2
Explanation: People pass the pillow in the following way: 1 -> 2 -> 3 -> 4 -> 3 -> 2.
After five seconds, the 2nd person is holding the pillow.
```

**Example 2:**

```
Input: n = 3, time = 2
Output: 3
Explanation: People pass the pillow in the following way: 1 -> 2 -> 3.
After two seconds, the 3rd person is holding the pillow.
```

**Constraints**

- 2 <= n <= 1000
- 1 <= time <= 1000

---

## 题目（中文翻译）

有 `n` 个人站成一排，编号从 `1` 到 `n`。最初枕头（pillow）由排在最前面的第 `1` 个人持有。每秒钟，持有枕头的人会将枕头传递给排在 **下一个**（next）位置的人。当枕头传到排尾的第 `n` 个人时，传递方向会改变，随后大家按相反方向继续传递枕头。

给定正整数 `n` 和 `time`，返回 `time` 秒后持有枕头的人的编号。

**示例 1**  
**示例 2**  

**约束条件**  
- 该题目与 LeetCode 3178: *Find the Child Who Has the Ball After K Seconds* 完全相同。

---

### 示例

#### 示例 1
**输入**: `n = 4, time = 5`  
**输出**: `2`  
**解释**: 枕头的传递顺序为: `1 -> 2 -> 3 -> 4 -> 3 -> 2`。  
经过五秒后，第 `2` 个人持有枕头。

#### 示例 2
**输入**: `n = 3, time = 2`  
**输出**: `3`  
**解释**: 枕头的传递顺序为: `1 -> 2 -> 3`。  
经过两秒后，第 `3` 个人持有枕头。

---

### 约束条件
- `2 <= n <= 1000`
- `1 <= time <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是 **一步一步模拟** Pillow 的传递过程：

1. 用一个整数 `pos` 表示当前 Pillow 所在的人的编号（下标），初始为 `1`（第一个人）。  
2. 用另一个整数 `dir` 表示传递的方向，`+1` 表示向右（编号增大），`-1` 表示向左（编号减小）。一开始方向是向右，所以 `dir = 1`。  
3. 每经过一秒，`pos += dir`，然后检查是否已经到达队伍的两端：  
   - 如果 `pos == n`（最右边），说明下次应该反向，于是把 `dir` 乘 `-1`。  
   - 同理如果 `pos == 1`（最左边），也要把 `dir` 乘 `-1`。  
4. 重复上述步骤 `time` 次，最后的 `pos` 就是答案。

> **类比**：`dir` 像是手电筒的指向，`pos` 像是手电筒照到的那个人。每走一步，手电筒往前照；碰到墙（队伍两端）就调头。

这个方法一定能得到正确答案，因为我们严格按照题目描述的「每秒传递一次」去执行。

#### 代码（Python）

```python
def pass_the_pillow_brute(n: int, time: int) -> int:
    # 当前 Pillow 所在的位置，初始在第 1 个人
    pos = 1
    # 方向，+1 表示向右（编号增大），-1 表示向左
    direction = 1

    # 模拟每一秒的传递
    for _ in range(time):
        # 先移动到下一个人
        pos += direction

        # 到达两端后需要调头
        if pos == n:          # 到最右边，下一步要往左走
            direction = -1
        elif pos == 1:        # 到最左边，下一步要往右走
            direction = 1

    return pos
```

#### 复杂度  

- **时间复杂度**：`O(time)`  
  这里的 `O(time)` 只是一种“次数”的说法，意思是**随时间线性增长**。如果 `time = 1000`，我们最多循环 1000 次。  
- **空间复杂度**：`O(1)`  
  只用了常数个整数变量（`pos`、`direction`），不随输入规模增大而增加。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**每一次传递只和当前方向有关**，而且**运动轨迹是有规律的**：

```
1 → 2 → 3 → … → n-1 → n → n-1 → … → 2 → 1 → 2 → …
```

从 `1` 出发到达 `n` 再回到 `1`，形成一个**来回往返**的循环。  
- 往右走 `n-1` 步到达 `n`，  
- 再往左走 `n-1` 步回到 `1`。  

所以完整的往返周期长度为 `2 * (n - 1)`，记作 `cycle`。  
只要知道 `time` 在这个周期里走了多少步，就可以直接算出位置，而不必真的遍历每一秒。

**步骤**：

1. 计算周期长度 `cycle = 2 * (n - 1)`。  
2. 取模 `t = time % cycle`，得到在当前周期内实际要走的步数（因为完整的周期会把 Pillow 带回到起点，等价于“0 步”。）  
3. 根据 `t` 判断 Pillow 现在在往右还是往左：
   - 如果 `t <= n - 1`（还没有到达最右端），则只是在**向右**走，第 `1 + t` 个人持有 Pillow。  
   - 否则已经走过了右端，需要往左走。此时已经在右端停留了一次，剩余步数 `t - (n - 1)` 表示往左走的步数，位置是 `n - (t - (n - 1))`。  

这样只用了常数时间即可得到答案。

> **类比**：把队伍想成一条跑道，跑者从左端跑到右端再折返。跑道长度是 `n-1`，来回一次是 `2*(n-1)`。我们只关心“跑者在第 `time` 秒跑到哪”，不必真的跑每一步。

#### 代码（Python）

```python
def pass_the_pillow_optimal(n: int, time: int) -> int:
    # 1. 计算往返一个周期的长度
    cycle = 2 * (n - 1)          # 例：n=4 -> cycle=6（1→2→3→4→3→2）

    # 2. 只保留本周期内的步数
    t = time % cycle             # 若恰好是完整周期，t 为 0，表示仍在起点 1

    # 3. 根据 t 判断是向右还是向左
    if t <= n - 1:               # 仍在向右的阶段
        return 1 + t            # 1 -> 2 -> … -> 1+t
    else:                        # 已经到达最右端，开始往左走
        # 已经走了 (n-1) 步到达 n，还剩 (t - (n-1)) 步往左走
        return n - (t - (n - 1))
```

#### 复杂度  

- **时间复杂度**：`O(1)`  
  只做了几次算术运算和一次条件判断，**不随 `time` 的大小增长**。相比暴力的 `O(time)`，这里的“常数时间”就像“一瞬间”算出来。  
- **空间复杂度**：`O(1)`  
  同样只用了几个整数变量。

---

## 心得  

- **核心技巧**：**把往返运动抽象为周期**，利用取模（`%`）把“大时间”压缩到一个小区间，再用简单的数学式子直接定位。  
- **适用场景**：  
  1. “在环形/往返结构中移动 K 步”类题目（如 LeetCode 1019 *Next Greater Node In Linked List* 的循环遍历）。  
  2. “球/灯/指针在两端来回传递”系列（如 3178 *Find the Child Who Has the Ball After K Seconds*、或“灯泡在走廊两端来回点亮”）。  
- **一句话总结解题钥匙**：**找出运动的周期，用取模把时间压缩，再写出周期内的定位公式**。

---

## 反思  

- **第一反应**：直接把每秒的传递写成循环，像模拟游戏一样一步步走。  
- **最容易踩的坑**：  
  - **边界条件**：当 `time` 正好是周期的整数倍时，`t = 0`，答案应该是第 `1` 个人，而不是 `0`。  
  - **方向切换**：忘记在到达两端后立即调头，会导致在最右端或最左端停留两次。  
- **下次类似题的第一步**：先问自己“这段运动有没有重复的模式？”如果有，**先求出周期**，再把大 `K`（或 `time`）映射到周期内部，再做定位。