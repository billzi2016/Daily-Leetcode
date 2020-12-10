# #1103. 分发糖果 / Distribute Candies to People

> 难度：简单 · 标签：Math、Simulation · [LeetCode 链接](https://leetcode.com/problems/distribute-candies-to-people/)

---

## 题目（英文原版）

**Description**

We distribute some number of candies, to a row of n = num_people people in the following way:
We then give 1 candy to the first person, 2 candies to the second person, and so on until we give n candies to the last person.
Then, we go back to the start of the row, giving n + 1 candies to the first person, n + 2 candies to the second person, and so on until we give 2 * n candies to the last person.
This process repeats (with us giving one more candy each time, and moving to the start of the row after we reach the end) until we run out of candies.  The last person will receive all of our remaining candies (not necessarily one more than the previous gift).
Return an array (of length num_people and sum candies) that represents the final distribution of candies.

**Examples**

**Example 1:**

```
Input: candies = 7, num_people = 4
Output: [1,2,3,1]
Explanation:
On the first turn, ans[0] += 1, and the array is [1,0,0,0].
On the second turn, ans[1] += 2, and the array is [1,2,0,0].
On the third turn, ans[2] += 3, and the array is [1,2,3,0].
On the fourth turn, ans[3] += 1 (because there is only one candy left), and the final array is [1,2,3,1].
```

**Example 2:**

```
Input: candies = 10, num_people = 3
Output: [5,2,3]
Explanation: 
On the first turn, ans[0] += 1, and the array is [1,0,0].
On the second turn, ans[1] += 2, and the array is [1,2,0].
On the third turn, ans[2] += 3, and the array is [1,2,3].
On the fourth turn, ans[0] += 4, and the final array is [5,2,3].
```

**Constraints**

- 1 <= candies <= 10^9
- 1 <= num_people <= 1000

---

## 题目（中文翻译）

我们将一定数量的糖果（candies）分配给排成一行的 `n = num_people` 个人，分配方式如下：

- 第一次从第一个人开始，给第一个人 1 颗糖果，给第二个人 2 颗，依次递增，直到给最后一个人 `n` 颗糖果。  
- 然后回到行首，给第一个人 `n + 1` 颗糖果，给第二个人 `n + 2` 颗，依次递增，直到给最后一个人 `2 * n` 颗糖果。  
- 这个过程不断重复（每轮分配的糖果数量比上一轮多 1，且在到达行尾后回到行首），直到糖果全部发完。**最后一个人会收到剩余的所有糖果**（未必恰好比前一次多 1 颗）。

返回一个长度为 `num_people` 的数组（array），其中第 `i` 项表示第 `i` 个人最终得到的糖果数，且数组中所有元素之和等于 `candies`。

### 示例

#### 示例 1
**输入**: `candies = 7, num_people = 4`  
**输出**: `[1,2,3,1]`  
**解释**:  
- 第一次分配后，`ans[0] += 1`，数组变为 `[1,0,0,0]`。  
- 第二次分配后，`ans[1] += 2`，数组变为 `[1,2,0,0]`。  
- 第三次分配后，`ans[2] += 3`，数组变为 `[1,2,3,0]`。  
- 第四次分配时只剩 1 颗糖果，`ans[3] += 1`，最终数组为 `[1,2,3,1]`。

#### 示例 2
**输入**: `candies = 10, num_people = 3`  
**输出**: `[5,2,3]`  
**解释**:  
- 第一次分配后，`ans[0] += 1`，数组变为 `[1,0,0]`。  
- 第二次分配后，`ans[1] += 2`，数组变为 `[1,2,0]`。  
- 第三次分配后，`ans[2] += 3`，数组变为 `[1,2,3]`。  
- 第四次分配后，`ans[0] += 4`，最终数组为 `[5,2,3]`。

### 约束条件
- `1 <= candies <= 10^9`  
- `1 <= num_people <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **按题目描述一步一步模拟** ：  
1. 设一个长度为 `num_people` 的数组 `ans`，全部初始化为 `0`。  
2. 从 `give = 1` 开始，每次把 `give` 颗糖分给当前轮到的同学（用下标 `i = (give‑1) % num_people`），  
   - 如果剩余糖果 `candies` 大于等于 `give`，就完整地给 `give` 颗；  
   - 否则只剩下 `candies` 颗了，全部给这位同学，结束循环。  
3. 每发完一次糖，`candies` 减去 `give`，`give` 加 `1`，继续下一轮。

> **类比**：把 `ans` 看成一排小盒子（每个人的口袋），`give` 就像手里递增的糖果数，`i` 就是指向当前盒子的指针，指针走到最后会自动回到第一个盒子（取模运算）。

**为什么正确**  
因为我们严格按照题目中「每轮递增、到头回头」的规则把糖分配完，所有糖必然恰好分配完或最后一次把剩余的糖全给了某个人。  

**复杂度分析（大白话）**  
- **时间**：每次循环只发一次糖，循环次数等于发糖的总次数 `give`，而 `give` 近似满足 `1 + 2 + … + give ≈ candies`，即 `give ≈ √(2·candies)`。所以时间复杂度是 **O(√candies)**，在最坏情况下（`candies = 10⁹`）约为 `44721` 次，仍然能跑完。  
- **空间**：只用了一个长度为 `num_people` 的数组，空间复杂度是 **O(num_people)**，最多 `1000`，非常小。

#### 代码（Python）

```python
def distributeCandies_bruteforce(candies: int, num_people: int):
    ans = [0] * num_people          # 每个人最终得到的糖果数
    give = 1                         # 本轮要送的糖果数量
    while candies > 0:               # 只要还有糖就继续
        idx = (give - 1) % num_people # 当前该给谁（循环）
        if candies >= give:          # 糖够，完整发
            ans[idx] += give
            candies -= give
        else:                        # 糖不够，全部给当前人
            ans[idx] += candies
            candies = 0
        give += 1                     # 下一轮糖数递增
    return ans
```

#### 复杂度

- **时间复杂度**：`O(√candies)` —— 这里的 `√candies` 表示发糖的次数大约等于糖的总量的平方根，随着糖的增多，次数只会慢慢增加，而不是线性增长。  
- **空间复杂度**：`O(num_people)` —— 只用了一个长度等于人数的数组来记录结果。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次只发一颗糖**，循环次数随糖的总量 `candies` 增大而增大。我们可以 **一次性算出完整的循环轮数**（即每个人都已经收到了一整轮的糖），然后只剩下不足一轮的糖再单独处理。

**关键观察**  

- 第 `k` 次发糖的数量恰好是 `k`（从 `1` 开始递增）。  
- 若已经发了 `m` 次糖，则已经发出的糖总数是 `1 + 2 + … + m = m·(m+1)/2`（等差数列求和公式）。  
- 当 `m` 正好是 `num_people` 的整数倍时，意味着已经走完了若干 **完整的轮次**（每轮恰好分给每个人一次）。设完整轮数为 `r`，则 `m = r·num_people`。  
- 所以我们要找最大的 `r` 使得  
  \[
  \frac{(r·num\_people)·(r·num\_people+1)}{2} \le candies
  \]  
  这相当于在 **一段连续整数** 中找出最大的前缀和不超过 `candies`。  

**求完整轮数的方式**  

直接用二分查找或数学公式求根。这里用二分查找实现更直观：

1. 设 `left = 0, right = candies`（因为最坏情况每次只发 1 颗，最多发 `candies` 次）。  
2. 中点 `mid` 表示已经发了 `mid` 次糖，计算 `total = mid·(mid+1)//2`。  
3. 若 `total <= candies`，说明可以再发更多，`left = mid`；否则 `right = mid - 1`。  
4. 循环结束后 `left` 即为最大的发糖次数 `m`。  
5. 完整轮数 `r = left // num_people`，剩余的发糖次数 `rem = left % num_people`（这部分已经在 `ans` 中分配好）。  
6. 仍有 `candies - total` 颗糖未分配，按题意全部给下一个人（下标 `rem`）。

**如何直接算每个人在完整轮数 `r` 中得到的糖**  

在 `r` 轮里，第 `i`（0‑based）个人收到的次数恰好是 `r` 次，且每次收到的糖构成等差数列：

- 第一次：`i + 1` 颗  
- 第二次：`i + 1 + num_people` 颗  
- 第三次：`i + 1 + 2·num_people` 颗  
- … 第 `r` 次：`i + 1 + (r‑1)·num_people` 颗  

等差数列求和公式：

\[
\text{sum}_i = r \times \frac{2·(i+1) + (r-1)·num\_people}{2}
\]

把这个值直接写进 `ans[i]`，时间只需 `O(num_people)`。

**整体步骤**  

1. 用二分查找得到最大发糖次数 `m`（满足前 `m` 次糖的总和不超过 `candies`）。  
2. 计算完整轮数 `r = m // num_people`，以及已经用掉的糖 `used = m·(m+1)//2`。  
3. 对每个人 `i`，把 `sum_i` 加入 `ans[i]`（只需要 `r` 轮的等差求和）。  
4. 剩余糖 `left = candies - used`，如果还有 `left > 0`，把它全部加到下标为 `m % num_people` 的人身上。  

> **类比**：想象你在把糖装进一条环形的传送带，每转一圈都比上一圈多装 `num_people` 颗糖。我们先算出完整转了多少圈（`r`），再把最后剩下的糖直接塞进下一个格子里。

#### 代码（Python）

```python
def distributeCandies_optimal(candies: int, num_people: int):
    # ---------- 1. 找到最大的发糖次数 m ----------
    left, right = 0, candies
    while left < right:
        mid = (left + right + 1) // 2          # 上取整防止死循环
        total = mid * (mid + 1) // 2           # 前 mid 次糖的总和
        if total <= candies:
            left = mid
        else:
            right = mid - 1
    m = left                                   # 发了 m 次糖，仍然 <= candies
    used = m * (m + 1) // 2                    # 已经用了这么多糖

    # ---------- 2. 计算完整轮数 ----------
    r = m // num_people                         # 完整的循环轮数
    ans = [0] * num_people

    # ---------- 3. 把完整轮数的糖直接算进每个人 ----------
    for i in range(num_people):
        # 等差数列求和：r 项，首项 = i+1，公差 = num_people
        ans[i] = r * (2 * (i + 1) + (r - 1) * num_people) // 2

    # ---------- 4. 处理剩余的糖 ----------
    remain = candies - used                     # 还剩下的糖
    if remain > 0:
        idx = m % num_people                     # 下一个该给谁
        ans[idx] += remain

    return ans
```

#### 复杂度

- **时间复杂度**：`O(num_people + log candies)`  
  - 二分查找的循环次数是 `log₂(candies)`（约 30 次），远小于 `num_people`（最多 1000），整体线性于人数。  
  - 与暴力解的 `O(√candies)` 相比，`log` 级别要快得多，尤其当 `candies` 达到上限 `10⁹` 时差距明显。  
- **空间复杂度**：`O(num_people)` —— 只用了结果数组，没有额外的递归栈或大表。

---

## 心得

- **核心技巧**：把连续递增的数列求和转化为等差数列求和，再用二分查找快速定位「可以完整发几次」的边界。  
- **适用的题型**  
  1. “把 **连续整数** 加到某个上限” 类似题目（如 LeetCode 441 `Arranging Coins`）。  
  2. “循环分配并且每轮递增” 的模拟题（如 LeetCode 1195 `Fizz Buzz Multithreaded` 中的计数思路）。  
- **一句话总结解题钥匙**：**先算出能完整执行多少轮，再把剩余的糖一次性塞进去**。

## 反思

- **第一反应**：直接写循环模拟，代码好写但可能会超时。  
- **最容易踩的坑**  
  - **整数溢出**：在 Python 中不易出现，但在其他语言要注意 `mid * (mid+1)` 可能超过 32 位整数范围。  
  - **边界条件**：当 `candies` 正好等于前 `m` 次的和时，`remain` 为 0，别忘了不再额外加糖。  
  - **取模位置**：剩余糖要加到 `m % num_people`（而不是 `m-1`），因为 `m` 表示已经发完的次数，下一次的受赠者正是这个下标。  
- **下次类似题的第一步**：**把递增的“发放次数”转化为等差求和，先求出完整的循环次数**，再处理余数。这样既能保证正确性，又能把时间控制在对数或线性级别。