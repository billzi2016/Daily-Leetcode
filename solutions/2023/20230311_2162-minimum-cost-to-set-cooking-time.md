# #2162. 设置烹饪时间的最小成本 / Minimum Cost to Set Cooking Time

> 难度：中等 · 标签：Math、Enumeration · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-set-cooking-time/)

---

## 题目（英文原版）

**Description**

A generic microwave supports cooking times for:
To set the cooking time, you push at most four digits. The microwave normalizes what you push as four digits by prepending zeroes. It interprets the first two digits as the minutes and the last two digits as the seconds. It then adds them up as the cooking time. For example,
You are given integers startAt, moveCost, pushCost, and targetSeconds. Initially, your finger is on the digit startAt. Moving the finger above any specific digit costs moveCost units of fatigue. Pushing the digit below the finger once costs pushCost units of fatigue.
There can be multiple ways to set the microwave to cook for targetSeconds seconds but you are interested in the way with the minimum cost.
Return the minimum cost to set targetSeconds seconds of cooking time.
Remember that one minute consists of 60 seconds.

**Examples**

**Example 1:**

```
Input: startAt = 1, moveCost = 2, pushCost = 1, targetSeconds = 600
Output: 6
Explanation: The following are the possible ways to set the cooking time.
- 1 0 0 0, interpreted as 10 minutes and 0 seconds.
  The finger is already on digit 1, pushes 1 (with cost 1), moves to 0 (with cost 2), pushes 0 (with cost 1), pushes 0 (with cost 1), and pushes 0 (with cost 1).
  The cost is: 1 + 2 + 1 + 1 + 1 = 6. This is the minimum cost.
- 0 9 6 0, interpreted as 9 minutes and 60 seconds. That is also 600 seconds.
  The finger moves to 0 (with cost 2), pushes 0 (with cost 1), moves to 9 (with cost 2), pushes 9 (with cost 1), moves to 6 (with cost 2), pushes 6 (with cost 1), moves to 0 (with cost 2), and pushes 0 (with cost 1).
  The cost is: 2 + 1 + 2 + 1 + 2 + 1 + 2 + 1 = 12.
- 9 6 0, normalized as 0960 and interpreted as 9 minutes and 60 seconds.
  The finger moves to 9 (with cost 2), pushes 9 (with cost 1), moves to 6 (with cost 2), pushes 6 (with cost 1), moves to 0 (with cost 2), and pushes 0 (with cost 1).
  The cost is: 2 + 1 + 2 + 1 + 2 + 1 = 9.
```

**Example 2:**

```
Input: startAt = 0, moveCost = 1, pushCost = 2, targetSeconds = 76
Output: 6
Explanation: The optimal way is to push two digits: 7 6, interpreted as 76 seconds.
The finger moves to 7 (with cost 1), pushes 7 (with cost 2), moves to 6 (with cost 1), and pushes 6 (with cost 2). The total cost is: 1 + 2 + 1 + 2 = 6
Note other possible ways are 0076, 076, 0116, and 116, but none of them produces the minimum cost.
```

**Constraints**

- 0 <= startAt <= 9
- 1 <= moveCost, pushCost <= 105
- 1 <= targetSeconds <= 6039

---

## 题目（中文翻译）

要设置烹饪时间，你最多可以按四个数字。微波炉会在你按的数字前面补零，使其成为四位数字。它将前两位解释为 **分钟（minutes）**，后两位解释为 **秒（seconds）**，然后将它们相加得到烹饪时间。例如，`1 2 3 4` 被解释为 12 分钟 34 秒，即 12 × 60 + 34 = 754 秒。  

给定整数 `startAt`、`moveCost`、`pushCost` 和 `targetSeconds`。最初你的手指位于数字 `startAt` 上。将手指移动到任意特定数字需要消耗 `moveCost` 单位的疲劳值。把手指下的数字按一次需要消耗 `pushCost` 单位的疲劳值。  

可能存在多种方式让微波炉的烹饪时间恰好为 `targetSeconds` 秒，但你只关心费用最小的那种方式。返回设置 `targetSeconds` 秒烹饪时间的最小费用。请记住，**1 分钟 = 60 秒**。  

---

### 示例

#### 示例 1
```
Input: startAt = 1, moveCost = 2, pushCost = 1, targetSeconds = 600
Output: 6
```
**解释**：下面是几种可能的设置方式。  
- `1 0 0 0`，解释为 10 分钟 0 秒（即 600 秒）。  
  手指已经在数字 1 上，按 1（费用 1），移动到 0（费用 2），按 0（费用 1），再按两次 0（各费用 1）。  
  总费用为：`1 + 2 + 1 + 1 + 1 = 6`。  

（其他方式如 `0600`、`600` 等要么费用更高，要么无法得到恰好 600 秒的烹饪时间。）

#### 示例 2
```
Input: startAt = 0, moveCost = 1, pushCost = 2, targetSeconds = 76
Output: 6
```
**解释**：最优的做法是只按两个数字 `7 6`，解释为 76 秒。  
手指先移动到 7（费用 1），按 7（费用 2），再移动到 6（费用 1），按 6（费用 2）。  
总费用为：`1 + 2 + 1 + 2 = 6`。  

其他可能的方式包括 `0076`、`076`、`0116`、`116`，但它们的费用都不比 6 小，且有的不能得到恰好 76 秒的烹饪时间。

---

### 约束条件
- `0 <= startAt <= 9`
- `1 <= moveCost, pushCost <= 10^5`
- `1 <= targetSeconds <= 6039`   （因为最大可表示的时间为 99 分 99 秒 = 6039 秒）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的本质是**在所有可以表示目标秒数的 4 位数字组合中，找出操作费用最小的一种**。  
我们可以把问题拆成两层：

1. **先枚举所有合法的时间表示**  
   - 微波炉把输入的 4 位数字解释为「前两位是分钟、后两位是秒」，于是实际烹饪时间 = `minutes * 60 + seconds`。  
   - 题目限制 `0 ≤ minutes, seconds ≤ 99`，因此只需要遍历 `minutes = 0 … 99`，计算对应的 `seconds = targetSeconds - minutes * 60`。  
   - 当 `seconds` 落在 `[0, 99]` 区间时，这对 `(minutes, seconds)` 就是一个**合法的**表示。

2. **再在每个合法的 `(minutes, seconds)` 上求最小按键费用**  
   - 把 `(minutes, seconds)` 用 2 位十进制补零的方式写成 4 位字符串，例如 `minutes = 7, seconds = 6` → `"0706"`。  
   - 题目说**最多按四个数字**，并且**会在左侧自动补零**。这意味着我们可以**把左侧的零删掉**（只要删掉的都是最左边的零），得到 1~4 位的实际按键序列。  
   - 对于 `"0706"`，合法的按键序列有  
     - `"0706"`（不删）  
     - `"706"`（删掉最左边的 `0`）  
     - `"06"`（再删一个左边的 `0`）  
     - `"6"`（再删一个左边的 `0`）  
   - 对每一种序列，模拟指尖的移动和按压即可算出费用。  
   - 取这些费用的最小值，就是当前 `(minutes, seconds)` 的最佳费用。

> **生活化类比**：  
> - **哈希表**就像一本字典，`key` 是单词，`value` 是页码。这里我们不需要哈希表，只用**遍历**（相当于一本本翻开看）所有可能的分钟数。  
> - **指尖移动**好比在键盘上从一个键跳到另一个键，移动一次要付“搬家费”，按一次要付“使用费”。我们只要记录每一步是否需要搬家，就能算出总费用。

**为什么这个方法一定能得到答案？**  
因为我们把 **所有** 可能的时间表示（最多 100 种）都枚举出来，并且对每种表示尝试 **所有** 合法的按键长度（最多 4 种），再把每一种实际操作的费用算出来，取最小值。没有遗漏的情况，自然能得到全局最优。

#### 代码（Python）

```python
def minCostSetTime(startAt: int, moveCost: int, pushCost: int, targetSeconds: int) -> int:
    # -------------------------------------------------
    # 计算一次完整按键序列的费用
    # seq: 只包含我们实际要按的数字（字符串形式），如 "706"
    # -------------------------------------------------
    def cost_of_seq(seq: str) -> int:
        finger = startAt          # 指尖一开始指在 startAt 上
        total = 0
        for ch in seq:
            d = int(ch)           # 当前要按的数字
            if finger != d:       # 需要搬家
                total += moveCost
                finger = d
            total += pushCost     # 按一次键的费用
        return total

    best = float('inf')           # 记录全局最小费用

    # -------------------------------------------------
    # 1) 枚举 minutes ∈ [0, 99]
    # -------------------------------------------------
    for minutes in range(100):
        seconds = targetSeconds - minutes * 60
        # seconds 必须落在合法区间 [0, 99]
        if 0 <= seconds <= 99:
            # 把 (minutes, seconds) 写成 4 位字符串，例如 07:06 → "0706"
            full = f"{minutes:02d}{seconds:02d}"   # 长度必为 4
            # -------------------------------------------------
            # 2) 删除左侧的 0，得到 1~4 位的真实按键序列
            #    只要删除的都是最左边的零才合法
            # -------------------------------------------------
            for cut in range(4):   # cut 表示删掉前面多少位
                seq = full[cut:]    # 剩余的字符串
                if not seq:         # 不能全删光
                    continue
                # 计算这条序列的费用，取最小
                best = min(best, cost_of_seq(seq))

    return best
```

#### 复杂度

- **时间复杂度：** `O(100 * 4 * L)`，其中 `L ≤ 4` 是每条按键序列的长度。实质上只遍历了最多 400 条极短的序列，算作 **O(1)** 常数时间。  
  - 大白话：我们只检查「0 到 99」这 100 种分钟数，每种最多检查 4 种不同的按键方式，每种方式最多按 4 次键。整个过程非常快，基本可以认为是“常数时间”。

- **空间复杂度：** `O(1)`。只用了几个整数和长度不超过 4 的临时字符串，没有随输入规模增长的额外存储。

---

### 2. 最优解

#### 思路  

虽然上面的暴力解已经是 **最优的**（因为搜索空间本身很小），但我们可以把它写得更**结构化**，帮助读者从“枚举”到“利用约束”逐步提升思路：

1. **定位瓶颈**  
   - 暴力解的唯一循环是 `minutes` 从 0 到 99，时间复杂度已经是 O(100)。在本题里这已经是最小可能的遍历次数，无法再进一步“加速”。  
   - 真正需要关注的是**如何快速、准确地算出每种表示的费用**，以及**如何避免非法的 `seconds`**。

2. **利用约束**  
   - `minutes` 只可能是 0~99，**枚举**是最直接且最安全的做法。  
   - 对每个 `minutes`，`seconds = targetSeconds - minutes*60` 必须满足 `0 ≤ seconds ≤ 99`，这一步过滤掉了大多数无效组合。

3. **统一费用计算**  
   - 把“指尖移动 + 按键费用”抽象成一个 **函数** `calc(seq)`，这样代码结构更清晰，也便于以后复用。  
   - 该函数只需要知道当前指尖所在的数字 `startAt`、搬家费 `moveCost`、按键费 `pushCost`，以及待按的数字序列 `seq`。

4. **处理前导零**  
   - 微波炉会把我们实际按的数字左侧补零到 4 位。因此，只要把完整的 4 位字符串 `mmss` 的左侧**连续零**全部删掉（最多删 3 位），剩下的就是我们真的要按的序列。  
   - 对每个合法的 `(mm, ss)`，只需要尝试 `cut = 0,1,2,3` 四种删除方式，取费用最小者。

5. **整体流程**  

   ```
   best = +∞
   for minutes in 0..99:
       seconds = target - minutes*60
       if 0 <= seconds <= 99:
           full = 4位字符串 mmss
           for cut in 0..3:
               seq = full[cut:]
               if seq 非空:
                   best = min(best, calc(seq))
   return best
   ```

   这段伪代码已经把**枚举+约束+费用计算**完整展示出来。

#### 代码（Python）

```python
def minCostSetTime(startAt: int, moveCost: int, pushCost: int, targetSeconds: int) -> int:
    """
    返回把微波炉调到 targetSeconds 所需的最小疲劳值。
    思路：枚举 minutes∈[0,99]，计算对应的 seconds，合法则枚举
          四种可能的实际按键序列，取费用最小。
    """

    # ---------- 费用计算函数 ----------
    def calc(seq: str) -> int:
        """给定实际要按的数字序列，返回从 startAt 开始的总费用。"""
        finger = startAt
        total = 0
        for ch in seq:
            d = int(ch)
            if finger != d:          # 需要搬家
                total += moveCost
                finger = d
            total += pushCost        # 按一次键的费用
        return total

    ans = float('inf')               # 初始为正无穷

    # ---------- 枚举 minutes ----------
    for mm in range(100):            # 0 … 99
        ss = targetSeconds - mm * 60
        if 0 <= ss <= 99:            # seconds 必须合法
            # 完整的 4 位表示，例如 07:06 → "0706"
            full = f"{mm:02d}{ss:02d}"
            # 删除左侧的 0，得到 1~4 位的真实按键序列
            for cut in range(4):
                seq = full[cut:]      # 切掉前面 cut 位
                if not seq:           # 切光了就不合法
                    continue
                ans = min(ans, calc(seq))

    return ans
```

#### 复杂度

- **时间复杂度：** `O(100 * 4 * L)`，`L ≤ 4`。等价于常数时间 `O(1)`，因为循环次数与题目给定的上界（99）固定不变。  
  - 与暴力解的区别仅在于代码结构更清晰，**没有任何额外的时间开销**。

- **空间复杂度：** `O(1)`。只使用了若干局部变量和最多 4 位的字符串，不随输入规模增长。

---

## 心得

- **核心技巧**：**枚举有限范围 + 前导零裁剪 + 费用模拟**。  
  这是一种“穷举+剪枝”的思路：先把搜索空间压到极小（这里是 0~99），再对每个候选做细致的费用评估。

- **适用的题型**  
  1. **有限枚举 + 费用计算**：如 LeetCode 1680 “Concatenation of Consecutive Binary Numbers”。  
  2. **需要处理前导零或左侧补齐的键盘/遥控器类题目**：如 2170 “Minimum Number of Operations to Make Array Empty”。  
  3. **时间/金额等单位转换后再枚举**：如 1799 “Maximum Score of a Good Subarray”。

- **一句话总结解题钥匙**：  
  **“把所有合法的表示列出来，然后用同一套费用函数把每种表示的代价算出来，取最小”。**

---

## 反思

- **拿到题目第一反应**：先把时间转成「分钟+秒」的两位数形式，想到要枚举分钟数，随后计算对应的秒数是否在合法区间。

- **最容易踩的坑**  
  1. **秒数超出 0~99**：忘记过滤 `seconds` 不合法的情况，会导致错误的 `mm:ss` 被计入。  
  2. **前导零的处理**：必须考虑 **删掉左侧连续零** 的所有可能，不能随意删掉中间的零。  
  3. **指尖起始位置**：第一位如果正好等于 `startAt`，就不需要搬家费用；代码里一定要先判断再加 `moveCost`。

- **下次遇到同类题，第一步该想到**：  
  **“先把搜索空间限定到极小的范围（枚举分钟/小时/金额的上限），再用统一的代价函数对每个候选做评估”。** 只要搜索空间是常数级，暴力枚举往往已经是最优解。