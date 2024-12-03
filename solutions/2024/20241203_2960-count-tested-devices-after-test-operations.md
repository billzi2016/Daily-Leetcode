# #2960. **测试操作后被测试的设备数量** / Count Tested Devices After Test Operations

> 难度：简单 · 标签：Array、Simulation、Counting · [LeetCode 链接](https://leetcode.com/problems/count-tested-devices-after-test-operations/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array batteryPercentages having length n, denoting the battery percentages of n 0-indexed devices.
Your task is to test each device i in order from 0 to n - 1, by performing the following test operations:
Return an integer denoting the number of devices that will be tested after performing the test operations in order.

**Examples**

**Example 1:**

```
Input: batteryPercentages = [1,1,2,1,3]
Output: 3
Explanation: Performing the test operations in order starting from device 0:
At device 0, batteryPercentages[0] > 0, so there is now 1 tested device, and batteryPercentages becomes [1,0,1,0,2].
At device 1, batteryPercentages[1] == 0, so we move to the next device without testing.
At device 2, batteryPercentages[2] > 0, so there are now 2 tested devices, and batteryPercentages becomes [1,0,1,0,1].
At device 3, batteryPercentages[3] == 0, so we move to the next device without testing.
At device 4, batteryPercentages[4] > 0, so there are now 3 tested devices, and batteryPercentages stays the same.
So, the answer is 3.
```

**Example 2:**

```
Input: batteryPercentages = [0,1,2]
Output: 2
Explanation: Performing the test operations in order starting from device 0:
At device 0, batteryPercentages[0] == 0, so we move to the next device without testing.
At device 1, batteryPercentages[1] > 0, so there is now 1 tested device, and batteryPercentages becomes [0,1,1].
At device 2, batteryPercentages[2] > 0, so there are now 2 tested devices, and batteryPercentages stays the same.
So, the answer is 2.
```

**Constraints**

- 1 <= n == batteryPercentages.length <= 100
- 0 <= batteryPercentages[i] <= 100

---

## 题目（中文翻译）

给定一个下标从 **0** 开始、长度为 `n` 的整数数组 `batteryPercentages`，其中 `batteryPercentages[i]` 表示第 `i` 台设备的电池剩余百分比（0 %~100 %）。

你需要按顺序从设备 `0` 到设备 `n‑1` 依次对每台设备执行以下 **测试操作**（test operation）：

1. 若 `batteryPercentages[i] > 0`，则该设备被 **测试**（tested），计数加 1。  
2. 对所有下标大于 `i` 的设备 `j`（即 `j > i`），将 `batteryPercentages[j]` 减 1，若减后小于 0 则保持为 0。

若 `batteryPercentages[i] == 0`，则直接跳过该设备，不进行任何操作。

在按照上述规则遍历完所有设备后，返回 **被测试的设备数量**。

---

### 示例

**示例 1**  
```text
Input: batteryPercentages = [1,1,2,1,3]
Output: 3
Explanation:
从设备 0 开始依次执行测试操作：
- 设备 0：batteryPercentages[0] > 0，计数变为 1；随后把下标 >0 的所有元素减 1，数组变为 [1,0,1,0,2]。
- 设备 1：batteryPercentages[1] == 0，跳过。
- 设备 2：batteryPercentages[2] > 0，计数变为 2；下标 >2 的元素减 1，数组变为 [1,0,1,0,1]。
- 设备 3：batteryPercentages[3] == 0，跳过。
- 设备 4：batteryPercentages[4] > 0，计数变为 3。

最终返回 3。
```

**示例 2**  
```text
Input: batteryPercentages = [0,1,2]
Output: 2
Explanation:
- 设备 0：batteryPercentages[0] == 0，跳过。
- 设备 1：batteryPercentages[1] > 0，计数变为 1；下标 >1 的元素减 1，数组变为 [0,1,1]。
- 设备 2：batteryPercentages[2] > 0，计数变为 2。

最终返回 2。
```

---

### 约束

- `1 <= n == batteryPercentages.length <= 100`
- `0 <= batteryPercentages[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直观的做法是**把题目描述的每一步都照搬**下来：

1. 从左到右遍历设备 `i = 0 … n-1`。  
2. 看到第 `i` 台设备时，先检查它当前的电量 `batteryPercentages[i]` 是否大于 `0`。  
   - 如果大于 `0`，说明这台设备可以被测试，计数器 `tested` 加 `1`。  
   - **关键点**：测试完以后，所有**后面的**设备（下标 `j > i`）的电量都会减 `1`，因为测试过程会消耗它们的电量。  
3. 继续检查下一个设备。

> **类比**：把 `batteryPercentages` 想象成一排排的水杯，杯子里装的是“电量”。每次我们把左边的杯子端走（测试），右边所有杯子里都要倒掉一点水（电量减 1）。如果某个杯子已经空了（电量 ≤ 0），我们就直接跳过去，不端它。

只要严格按照上面的规则模拟，就一定能得到正确的答案，因为我们没有遗漏任何一步。

#### 代码（Python）

```python
def countTestedDevices_bruteforce(batteryPercentages):
    # 把输入复制一份，防止修改原数组
    batteries = batteryPercentages[:]
    tested = 0                     # 已经成功测试的设备数量

    n = len(batteries)
    for i in range(n):
        # 第 i 台设备当前电量
        if batteries[i] > 0:       # 能测试
            tested += 1
            # 所有后面的设备电量都减 1
            for j in range(i + 1, n):
                batteries[j] -= 1
                # 电量不会出现负数（题目没有要求，但为了安全可以限制）
                if batteries[j] < 0:
                    batteries[j] = 0
        # 否则直接跳过，不做任何修改
    return tested
```

> 关键行解释  
> - `batteries = batteryPercentages[:]` 复制列表，避免把原数据改了。  
> - `if batteries[i] > 0:` 判断当前设备是否还有电。  
> - `for j in range(i + 1, n): batteries[j] -= 1` 模拟“后面的设备电量都减 1”。  

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：外层循环遍历 `n` 次，内层（给后面的设备减 1）在最坏情况下也要遍历近 `n` 次，所以总操作数约为 `n × n`，即 `n²`。把 `n²` 想象成“把一张 100×100 的棋盘每格都走一遍”，当 `n` 很大时会很慢。

- **空间复杂度**：`O(n)`  
  解释：我们额外复制了一份长度为 `n` 的数组 `batteries`，占用的空间和输入规模成线性关系。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**真正消耗时间的地方是每次测试后对所有后续元素的遍历**。如果我们能够**直接算出**第 `i` 台设备在被检查时的电量，而不去真的“减 1”，就可以把 `O(n²)` 降到 `O(n)`。

观察：

- 第 `i` 台设备的原始电量是 `batteryPercentages[i]`。  
- 每一次成功的测试（即一次 “测试操作”）都会让**所有**后面的设备电量减 `1`。  
- 因此，在检查第 `i` 台设备时，它已经被 **之前已经成功测试的设备**（记作 `tested`）减了 `tested` 次电量。  
- 实际电量 = `batteryPercentages[i] - tested`。  
- 只要实际电量 **大于 0**，就可以测试这台设备。等价地：`batteryPercentages[i] > tested`。

于是我们只需要一次遍历：

1. 维护一个计数器 `tested`，表示**已经成功测试的设备数量**。  
2. 从左到右检查每台设备：  
   - 若 `batteryPercentages[i] > tested`，说明它还有电，能够被测试。  
   - 此时 `tested += 1`（因为我们多测试了一台）。  
   - 否则直接跳过。  

> **类比**：把每一次成功测试看成“发射一枚子弹”。每发一枚子弹，后面的所有设备的电量都被“子弹击中”一次。我们不必真的去把每个设备的电量减 1，只要记住已经发射了多少子弹（`tested`），就能直接算出第 `i` 台设备还剩多少电。

#### 代码（Python）

```python
def countTestedDevices_optimal(batteryPercentages):
    """
    只需要一次遍历 O(n) 即可得到答案。
    """
    tested = 0  # 已经成功测试的设备数

    for i, battery in enumerate(batteryPercentages):
        # 实际电量 = 原始电量 - 已经进行的测试次数
        # 只要实际电量大于 0，就能测试
        if battery > tested:
            tested += 1          # 这台设备成功测试
            # 这里不需要真的去修改后面的电量，因为
            # "已测试次数" 已经隐含了对后续设备的所有减 1 操作
    return tested
```

> 关键行解释  
> - `if battery > tested:` 判断**原始电量**是否大于已经进行的测试次数。  
> - `tested += 1` 成功测试后，计数器加一，等价于“所有后面的设备都被减了 1”。  

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历一次数组，操作次数随 `n` 成线性关系。相比暴力的 `n²`，这就像把“在 100×100 的棋盘上走一遍”变成“只走一条直线”，快得多。

- **空间复杂度**：`O(1)`  
  只用了几个整数变量（`tested`），不随输入规模增长。

---

## 心得

- **核心技巧**：**把“每一次操作对后续元素的影响”抽象为一个累计计数**（这里是已经测试的设备数），从而避免显式的循环更新。  
- **适用的题型**：  
  1. “每次操作都会让后面的元素减/加固定值” 的模拟题（如 **“减法游戏”**、**“递增数组”**）。  
  2. 需要判断 “当前值是否大于已发生的次数” 的问题（如 **“按顺序删除数组元素”**）。  
  3. 任何可以用**前缀计数**或**前缀和**简化的线性扫描题目。  
- **一句话总结解题钥匙**：**把重复的“对后面所有元素做同样修改”压缩成一个全局计数，直接比较即可**。

---

## 反思

- **第一反应**：看到“每次测试后，后面的电量都要减 1”，我立刻想到**直接模拟**，于是写出了 `O(n²)` 的暴力代码。  
- **最容易踩的坑**：  
  - 忘记在模拟时把电量减到负数后仍然继续比较，导致计数错误。  
  - 在优化思路里误把条件写成 `battery >= tested`（会多算一次），实际应为 `>`（必须还有正电量）。  
- **下次类似题的第一步**：先问自己“每一次操作对后面的元素到底产生了怎样的统一影响？能否用一个累计变量来代替遍历更新？”这样往往能快速从 `O(n²)` 跳到 `O(n)`。