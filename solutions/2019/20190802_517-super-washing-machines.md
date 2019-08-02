# #517. 超级洗衣机 / Super Washing Machines

> 难度：困难 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/super-washing-machines/)

---

## 题目（英文原版）

**Description**

You have n super washing machines on a line. Initially, each washing machine has some dresses or is empty.
For each move, you could choose any m (1 <= m <= n) washing machines, and pass one dress of each washing machine to one of its adjacent washing machines at the same time.
Given an integer array machines representing the number of dresses in each washing machine from left to right on the line, return the minimum number of moves to make all the washing machines have the same number of dresses. If it is not possible to do it, return -1.

**Examples**

**Example 1:**

```
Input: machines = [1,0,5]
Output: 3
Explanation:
1st move:    1     0 <-- 5    =>    1     1     4
2nd move:    1 <-- 1 <-- 4    =>    2     1     3
3rd move:    2     1 <-- 3    =>    2     2     2
```

**Example 2:**

```
Input: machines = [0,3,0]
Output: 2
Explanation:
1st move:    0 <-- 3     0    =>    1     2     0
2nd move:    1     2 --> 0    =>    1     1     1
```

**Example 3:**

```
Input: machines = [0,2,0]
Output: -1
Explanation:
It's impossible to make all three washing machines have the same number of dresses.
```

**Constraints**

- n == machines.length
- 1 <= n <= 104
- 0 <= machines[i] <= 105

---

## 题目（中文翻译）

**描述**  
你有 n 台排成一行的超级洗衣机（super washing machines）。最初，每台洗衣机中可能有若干件衣物（dresses）或为空。  
每一次操作（move），你可以选择任意 m 台洗衣机（1 ≤ m ≤ n），并让这 m 台洗衣机中的每一台同时把一件衣物传递给它的相邻洗衣机（adjacent washing machines）。  

给定一个整数数组（integer array）`machines`，其中 `machines[i]` 表示第 i 台洗衣机（从左到右）的衣物数量，返回使所有洗衣机拥有相同数量衣物所需的最少操作次数。如果无法实现，返回 -1。

**示例 1**  
```text
Input: machines = [1,0,5]
Output: 3
Explanation:
第 1 次操作:    1     0 <-- 5    =>    1     1     4
第 2 次操作:    1 <-- 1 <-- 4    =>    2     1     3
第 3 次操作:    2     1 <-- 3    =>    2     2     2
```

**示例 2**  
```text
Input: machines = [0,3,0]
Output: 2
Explanation:
第 1 次操作:    0 <-- 3     0    =>    1     2     0
第 2 次操作:    1     2 --> 0    =>    1     1     1
```

**示例 3**  
```text
Input: machines = [0,2,0]
Output: -1
Explanation:
无法使三台洗衣机的衣物数量全部相同。
```

**约束条件**  
- `n == machines.length`  
- `1 <= n <= 10^4`  
- `0 <= machines[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一步步把每台机器的衣服搬到目标值**，就像把水从高的水桶倒到低的水桶一样：

1. 先算出所有机器的衣服总数 `sum`，如果 `sum` 不能被机器数量 `n` 整除，说明根本不可能平均分配，直接返回 `-1`。  
2. 设每台机器最终应该有的衣服数 `avg = sum // n`。  
3. 从左到右遍历机器：  
   - 如果当前机器 `machines[i]` 大于 `avg`，说明它多出 `machines[i] - avg` 件衣服，需要把这些衣服一次一次向右搬。  
   - 如果小于 `avg`，说明它缺少 `avg - machines[i]` 件衣服，需要从左边或右边的机器一次一次搬进来。  
4. 为了模拟“每一步只能把每台机器的 **一件** 衣服搬到相邻机器”，我们在循环里**逐件搬**，每搬一件就记一次移动次数 `steps`，并更新相邻机器的衣服数。  

> **类比**：把每台洗衣机想象成一排水桶，`machines[i]` 是第 `i` 桶里水的体积。我们每次只能把每个桶里 **一滴** 水倒到左或右相邻的桶里。暴力解就是把每一滴水都搬到正确的位置，直到所有桶水量相等。

这种做法虽然能得到正确答案，但每搬一件衣服都要遍历一次数组，最坏情况下会搬 `O(n * max(machines[i]))` 次，时间复杂度大约是 **O(n²)**（因为 `max(machines[i])` 在 `n` 级别的情况下会导致二次遍历），空间只用了常数级别的变量 **O(1)**。

#### 代码（Python）

```python
def findMinMoves_bruteforce(machines):
    n = len(machines)
    total = sum(machines)
    # 1）总数不能整除，直接返回 -1
    if total % n != 0:
        return -1

    avg = total // n          # 每台机器最终应有的衣服数
    steps = 0                 # 记录总的移动次数

    # 2）模拟搬运过程
    # 为了让代码更直观，这里用 while 循环逐件搬
    i = 0
    while i < n:
        # 当前机器多余的衣服
        while machines[i] > avg:
            # 把一件衣服搬到右边（如果已经是最右边，只能往左搬）
            if i + 1 < n:
                machines[i] -= 1
                machines[i + 1] += 1
            else:  # 最右边只能往左搬
                machines[i] -= 1
                machines[i - 1] += 1
            steps += 1
        # 当前机器缺少的衣服
        while machines[i] < avg:
            # 从左边借一件（如果已经是最左边，只能往右借）
            if i - 1 >= 0:
                machines[i] += 1
                machines[i - 1] -= 1
            else:  # 最左边只能向右借
                machines[i] += 1
                machines[i + 1] -= 1
            steps += 1
        i += 1

    return steps
```

> **注意**：这段代码仅用于演示思路，实际运行会非常慢，特别是 `machines` 中的数值很大时。

#### 复杂度

- **时间复杂度**：`O(n²)`（最坏情况下每件衣服都要遍历一次数组）  
  - **大白话**：如果有 100 台机器，每台平均需要搬 100 件衣服，粗略算下来要搬 10 000 次，每次搬都要看一遍 100 台机器，整体操作大约是 1 000 000 步，随机器数量和衣服数的增大呈二次增长。
- **空间复杂度**：`O(1)`（只用了几个整数变量）  

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于**每搬一件衣服都要遍历整个数组**。实际上我们不需要逐件搬，而是可以一次性算出每台机器**在最优情况下**需要多少步才能达到均衡。

关键观察：

1. **总数必须能整除**  
   同暴力解，先判断 `sum(machines) % n != 0`，若不整除直接返回 `-1`。

2. **每台机器的“负担”**  
   - 设目标均值 `avg = total // n`。  
   - 对于第 `i` 台机器，左边所有机器的总衣服数为 `left_sum = sum(machines[:i])`。  
   - 若所有左边机器已经正好均衡，每台应该有 `i * avg` 件衣服。  
   - **左侧缺口**（需要从右边搬进来的衣服） = `i * avg - left_sum`。  
   - 同理，右侧缺口 = `(n - i - 1) * avg - (total - left_sum - machines[i])`。

   这两个缺口分别表示**左边/右边需要多少件衣服才能平衡**。如果缺口是正数，说明该侧需要搬进衣服；如果是负数，说明该侧有剩余可以搬出。

3. **每台机器的最大搬运压力**  
   在一次移动中，一台机器可以**同时向左和向右各搬出一件**（因为题目允许一次选择任意机器并把每台机器的一件衣服送给相邻机器），所以对第 `i` 台机器，**它真正需要的步数**取决于下面两个值的最大值：

   - `abs(left_deficit)` 或 `abs(right_deficit)` 中的较大者 → 说明这台机器一侧的缺口最严重，需要多少步才能把足够的衣服送进/送出。
   - `machines[i] - avg`（即该机器本身多余的衣服） → 即使左右两侧都已经平衡，这台机器本身如果有多余衣服，也需要把这些衣服分散到左右，两边一起搬出，每一步只能搬出一件，所以也会限制步数。

   因此**第 i 台机器的最小步数** = `max( abs(left_deficit), abs(right_deficit), machines[i] - avg )`。

4. **全局答案**  
   所有机器可以并行工作，整体所需的最少步数是**所有机器的局部最大步数的最大值**，即：

   ```
   answer = max_i  max( abs(left_deficit_i), abs(right_deficit_i), machines[i] - avg )
   ```

   只要遍历一次数组，实时维护左侧累计和 `left_sum`，就能在 **O(n)** 时间算出每台机器的三个候选值并取全局最大。

> **类比**：想象每台机器是一个**水库**，左边、右边的水库一起向它“要水”或“给它水”。左侧缺口就是左边水库整体缺多少水，右侧缺口是右边缺多少水。每个水库一次只能放/抽一桶水，所以它需要的时间等于它最紧迫的那条“供水/排水”管道的需求量。全局的时间就是所有水库中需求最大的那条管道的时间。

#### 代码（Python）

```python
def findMinMoves(machines):
    """
    返回使所有洗衣机衣服数量相等的最少移动次数。
    如果不可能返回 -1。
    """
    n = len(machines)
    total = sum(machines)

    # 1）总衣服数必须能被机器数整除
    if total % n != 0:
        return -1

    avg = total // n                # 目标均值
    left_sum = 0                    # 累计左侧衣服数（不包括当前机器）
    answer = 0                      # 记录全局最大步数

    for i, cur in enumerate(machines):
        # 左侧缺口：左侧应有 i * avg 件衣服，实际只有 left_sum 件
        left_deficit = i * avg - left_sum

        # 右侧缺口：右侧应有 (n-i-1) * avg 件衣服，实际为 total - left_sum - cur 件
        right_deficit = (n - i - 1) * avg - (total - left_sum - cur)

        # 该机器本身多余的衣服数（可能为负，表示缺少）
        excess = cur - avg

        # 该机器在最优情况下需要的步数 = 三者的最大值的绝对值
        # left_deficit、right_deficit 可能为负，取绝对值后表示“需要搬多少件”
        need = max(abs(left_deficit), abs(right_deficit), excess)

        # 更新全局答案
        answer = max(answer, need)

        # 累计左侧和，进入下一台机器的计算
        left_sum += cur

    return answer
```

> **代码要点解释**  
> - `left_deficit` 与 `right_deficit` 直接用公式得到，无需额外循环。  
> - `excess`（`cur - avg`）是机器本身的“出货量”，因为机器可以同时向左、向右各出一件，所以只要它本身的多余量大于两侧缺口，就会成为瓶颈。  
> - `need` 取三者的最大值（左、右缺口的绝对值和自身多余量），这一步正是“每台机器最紧迫的搬运任务”。  
> - 最后 `answer` 是所有机器中最紧迫的任务的时间，即整体最少移动次数。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - **大白话**：只需要一次遍历，像数数一样走一遍机器列表，随机器数量线性增长，十万台机器只需要十万步计算，远快于暴力的二次遍历。
- **空间复杂度**：`O(1)`（只用了几个整数变量），不需要额外的数组或哈希表。

---

## 心得

- **核心技巧**：利用**前缀和**一次遍历得到左侧/右侧的“缺口”，并结合**局部最大**与**全局最大**的思想，得到最优步数。  
- **适用的题型**：  
  1. “分配均衡”类问题，如 *Candy Distribution*、*Load Balancing*。  
  2. 需要一次性算出每个位置的**左/右累计差值**的题目，如 *Maximum Subarray Sum with Prefix*。  
  3. 多方向移动且每次只能搬一件的**贪心**问题，如 *Super Washing Machines*（本题）和 *Minimum Number of Moves to Make Array Complementary*（变形）。
- **一句话总结解题钥匙**：**把全局约束（总和可均分）转化为每个位置的左/右缺口，答案就是所有位置缺口的最大值**。

---

## 反思

- **第一反应**：先检查总数能否均分，然后想象把多余的衣服“一件件”搬过去，结果想到暴力模拟。  
- **最容易踩的坑**：  
  - 忽略了**总数不可整除**的情况，导致在实际实现时出现无限循环。  
  - 在计算左/右缺口时忘记取绝对值或误用负数，导致答案出现负数。  
  - 没有考虑**边界机器**只能向单侧搬出/搬入的特殊情况（虽然公式已经天然涵盖）。  
- **下次类似题的第一步**：先把**全局约束（总量、目标均值）**写清楚，再**用前缀和**快速得到每个位置的“需要多少进/出”，最后取**最大**值即为答案。这样可以避免不必要的模拟，直接得到最优解。