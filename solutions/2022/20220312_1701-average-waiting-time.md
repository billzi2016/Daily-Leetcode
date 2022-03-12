# #1701. **Average Waiting Time** / Average Waiting Time

> 难度：中等 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/average-waiting-time/)

---

## 题目（英文原版）

**Description**

There is a restaurant with a single chef. You are given an array customers, where customers[i] = [arrivali, timei]:
When a customer arrives, he gives the chef his order, and the chef starts preparing it once he is idle. The customer waits till the chef finishes preparing his order. The chef does not prepare food for more than one customer at a time. The chef prepares food for customers in the order they were given in the input.
Return the average waiting time of all customers. Solutions within 10-5 from the actual answer are considered accepted.

**Examples**

**Example 1:**

```
Input: customers = [[1,2],[2,5],[4,3]]
Output: 5.00000
Explanation:
1) The first customer arrives at time 1, the chef takes his order and starts preparing it immediately at time 1, and finishes at time 3, so the waiting time of the first customer is 3 - 1 = 2.
2) The second customer arrives at time 2, the chef takes his order and starts preparing it at time 3, and finishes at time 8, so the waiting time of the second customer is 8 - 2 = 6.
3) The third customer arrives at time 4, the chef takes his order and starts preparing it at time 8, and finishes at time 11, so the waiting time of the third customer is 11 - 4 = 7.
So the average waiting time = (2 + 6 + 7) / 3 = 5.
```

**Example 2:**

```
Input: customers = [[5,2],[5,4],[10,3],[20,1]]
Output: 3.25000
Explanation:
1) The first customer arrives at time 5, the chef takes his order and starts preparing it immediately at time 5, and finishes at time 7, so the waiting time of the first customer is 7 - 5 = 2.
2) The second customer arrives at time 5, the chef takes his order and starts preparing it at time 7, and finishes at time 11, so the waiting time of the second customer is 11 - 5 = 6.
3) The third customer arrives at time 10, the chef takes his order and starts preparing it at time 11, and finishes at time 14, so the waiting time of the third customer is 14 - 10 = 4.
4) The fourth customer arrives at time 20, the chef takes his order and starts preparing it immediately at time 20, and finishes at time 21, so the waiting time of the fourth customer is 21 - 20 = 1.
So the average waiting time = (2 + 6 + 4 + 1) / 4 = 3.25.
```

**Constraints**

- 1 <= customers.length <= 105
- 1 <= arrivali, timei <= 104
- arrivali <= arrivali+1

---

## 题目（中文翻译）

There is a restaurant with a single chef. You are given an array `customers`, where `customers[i] = [arrivali, timei]`:
- When a customer arrives, he gives the chef his **order** (order), and the chef starts preparing it once he is idle.
- The customer waits until the chef finishes preparing his order.
- The chef does not prepare food for more than one customer at a time.
- The chef prepares food for customers in the order they appear in the input.

Return the average waiting time of all customers. Solutions whose answer is within `10⁻⁵` of the actual value are considered accepted.

---

### 示例

#### 示例 1
**输入**  
``` 
customers = [[1,2],[2,5],[4,3]]
```  
**输出**  
```
5.00000
```  
**解释**  
1. 第一个顾客在时间 `1` 到达，厨师立即接单并在时间 `1` 开始烹饪，`2` 单位时间后完成，于时间 `3` 完成。因此该顾客的等待时间为 `3 - 1 = 2`。  
2. 第二个顾客在时间 `2` 到达，厨师在时间 `3` 才空闲，于是此时开始烹饪，`5` 单位时间后于时间 `8` 完成，等待时间为 `8 - 2 = 6`。  
3. 第三个顾客在时间 `4` 到达，厨师在时间 `8` 才空闲，开始烹饪 `3` 单位时间后于时间 `11` 完成，等待时间为 `11 - 4 = 7`。  
平均等待时间 = `(2 + 6 + 7) / 3 = 5.00000`。

#### 示例 2
**输入**  
``` 
customers = [[5,2],[5,4],[10,3],[20,1]]
```  
**输出**  
```
3.25000
```  
**解释**  
1. 第一个顾客在时间 `5` 到达，厨师立即开始烹饪，`2` 单位时间后于时间 `7` 完成，等待时间为 `7 - 5 = 2`。  
2. 第二个顾客同样在时间 `5` 到达，厨师在时间 `7` 才空闲，开始烹饪 `4` 单位时间后于时间 `11` 完成，等待时间为 `11 - 5 = 6`。  
3. 第三个顾客在时间 `10` 到达，厨师在时间 `11` 开始烹饪，`3` 单位时间后于时间 `14` 完成，等待时间为 `14 - 10 = 4`。  
4. 第四个顾客在时间 `20` 到达，厨师在时间 `20` 空闲，立即烹饪 `1` 单位时间后于时间 `21` 完成，等待时间为 `21 - 20 = 1`。  
平均等待时间 = `(2 + 6 + 4 + 1) / 4 = 3.25000`。

---

### 约束条件
- `1 <= customers.length <= 10⁵`
- `1 <= arrivali, timei <= 10⁴`
- `arrivali ≤ arrivali+1`（即到达时间非递减）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **“逐分钟模拟餐厅的运行”** ：  
1. 维护一个 `clock` 表示当前的时间（秒/分钟都行），从 `0` 开始。  
2. 对每一位顾客 `i`，从 `clock` 开始一步步向前走，直到  
   - `clock` 达到顾客的到达时间 `arrivali`（如果厨师空闲），或者  
   - 厨师已经在做前面的顾客的菜，需要等到前一道菜做好。  
3. 当厨师开始为顾客 `i` 做菜时，`clock` 加上 `timei`（做菜所需时间），  
   此时 `clock - arrivali` 就是这位顾客的 **等待时间**（包括他自己的烹饪时间）。  
4. 把所有等待时间加起来，最后除以顾客数得到平均等待时间。

> **类比**：把 `clock` 想成“厨房的钟表”，每走一步就像厨房里滴答的秒针。  
> 哈希表在这里不需要，用到的唯一数据结构是 **数组**（存放顾客信息）和 **一个整数变量**（`clock`）。

**为什么正确**  
- 我们严格按照题目要求的顺序（输入顺序）处理每位顾客。  
- 每一次把 `clock` 推进到“厨师可以开始新订单的最早时刻”，确保不遗漏任何等待。

**时间/空间复杂度**  
- 这段“逐分钟” 的模拟在最坏情况下会把时间从 `0` 推进到所有顾客离开的最晚时刻。  
- 假设所有顾客的烹饪时间总和为 `S`，则循环的步数大约是 `S`，最坏可达 `10⁹`（超出题目限制），所以 **时间复杂度约为 O(S) ≈ O(∑timei)**，在数据量大时会超时。  
- 只用了常数个额外变量，**空间复杂度 O(1)**。

> 大白话解释：  
> - `O(n²)` 常被描述为“平方级”，如果 `n` 是 10⁵，`n²` 就是 10¹⁰，根本跑不完。  
> - 这里的 `O(S)` 类似于“跟所有做菜的时间总和成正比”，如果每道菜都要 10⁴ 分钟，100 000 道菜就会是 10⁹ 步，显然不行。

#### 代码（Python）

```python
def averageWaitingTime_bruteforce(customers):
    """
    暴力模拟：逐分钟推进厨房的时钟
    :param customers: List[List[int]]  [[arrivali, timei], ...]
    :return: float 平均等待时间
    """
    clock = 0                 # 厨房当前时间
    total_wait = 0            # 所有顾客的累计等待时间

    for arrive, dur in customers:
        # 让时钟跑到顾客到达时（如果厨师此时空闲）
        while clock < arrive:
            clock += 1        # 时钟每走一步相当于一分钟过去

        # 此时 clock >= arrive，厨师可以开始做这道菜
        clock += dur          # 做完这道菜的时间
        total_wait += clock - arrive   # 等待时间 = 完成时刻 - 到达时刻

    return total_wait / len(customers)
```

#### 复杂度

- **时间复杂度**：`O(∑timei)`（在最坏情况下几乎是每分钟都循环一次），相当于“线性于所有烹饪时间的总和”。  
- **空间复杂度**：`O(1)`，只用了常数级别的额外变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正耗时的不是遍历每分钟，而是我们不必真的去“走每一分钟”**。  
只要知道 **“厨师什么时候空闲”**，就能直接算出下一个顾客的开始时间。  

**关键点**：

1. 用一个变量 `chef_free_time` 记录厨师**下次空闲的时间点**。  
2. 对每位顾客 `i`：  
   - 如果 `chef_free_time` ≤ `arrivali`，说明厨师在顾客到达时已经空闲，直接在 `arrivali` 开始做菜，`chef_free_time = arrivali + timei`。  
   - 否则（`chef_free_time` > `arrivali`），顾客必须等到厨师空闲后再开始，`chef_free_time += timei`（在原有空闲时间的基础上再加上这道菜的烹饪时间）。  
3. 无论哪种情况，**顾客的等待时间** 都是 `chef_free_time - arrivali`（因为 `chef_free_time` 已经是这位顾客完成时的时间点）。  
4. 把所有等待时间累加，最后除以顾客数即可。

> **类比**：把 `chef_free_time` 想成“厨师的日程表”，它记录了厨师的下一个空档。每来一个顾客，只要看顾客的到达时间和日程表谁更早，就能立刻决定何时开始，而不需要逐分钟检查。

**为什么更快**  
- 只遍历一次顾客数组，每位顾客的计算都是 **O(1)**，不再跟烹饪时间的长度挂钩。  
- 这正是 **贪心** 思想的体现：每一步都做出对当前最优的决定（让厨师尽早开始下一个订单），从而得到全局最优的平均等待时间。

#### 代码（Python）

```python
def averageWaitingTime(customers):
    """
    最优解：一次遍历，使用 chef_free_time 记录厨师空闲时间点
    :param customers: List[List[int]]  [[arrivali, timei], ...]
    :return: float 平均等待时间
    """
    chef_free_time = 0        # 厨师下一次空闲的时间点
    total_wait = 0.0          # 累计所有顾客的等待时间（使用 float 防止整数除法截断）

    for arrive, dur in customers:
        # 如果厨师在顾客到达时已经空闲，直接在 arrive 开始做菜
        if chef_free_time <= arrive:
            chef_free_time = arrive + dur
        else:                 # 否则顾客需要等到 chef_free_time 再开始
            chef_free_time += dur

        # 等待时间 = 完成时刻 - 到达时刻
        total_wait += chef_free_time - arrive

    # 平均等待时间 = 总等待 / 顾客人数
    return total_wait / len(customers)
```

#### 复杂度

- **时间复杂度**：`O(n)`，只遍历一次顾客列表，`n` 是顾客数量（最多 `10⁵`），这在实际中毫秒级完成。  
  > 与暴力解相比，省掉了“按分钟递增时钟”的循环，真正的瓶颈不再是时间总和，而是顾客数本身。
- **空间复杂度**：`O(1)`，只用了几个整数/浮点数变量，和输入规模无关。

---

## 心得

- **核心技巧**：**贪心 + 维护当前状态**（这里是厨师空闲时间）。  
- **适用场景**：  
  1. 单机调度类问题（如“单线程 CPU 任务调度”）。  
  2. 需要按顺序处理且每个任务都有开始时间限制的情形（如“银行排队”“医院挂号”）。  
  3. “最早完成时间”类的排队模拟（如 LeetCode 1834 *Single-Threaded CPU*）。  
- **一句话总结**：**只要知道下一个可用的时间点，就能 O(1) 直接算出每个顾客的等待时间**。

---

## 反思

- **第一反应**：看到“单厨师、顺序处理”，本能想到“模拟”。最开始会想把时间一步步走，这就是暴力思路。  
- **最容易踩的坑**：  
  - 忘记在 `chef_free_time <= arrivali` 时把 `chef_free_time` 重新设为 `arrivali + timei`，导致后面的顾客等待时间被多算。  
  - 使用整数除法导致平均值被截断，需要显式转换为 `float`（或在 Python3 中直接使用 `/`）。  
  - 边界条件：只有一位顾客或所有顾客到达时间相同，都要确保逻辑仍然成立。  
- **下次遇到同类题**：第一步先 **思考“当前系统的状态（空闲时间、资源占用）该如何用一个变量表达”**，再在遍历中 **更新这个状态**，几乎所有顺序调度类题目都可以用这种方式降到 O(n)。