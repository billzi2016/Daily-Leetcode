# #1996. 游戏中弱角色的数量 / The Number of Weak Characters in the Game

> 难度：中等 · 标签：Array、Stack、Greedy、Sorting、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/the-number-of-weak-characters-in-the-game/)

---

## 题目（英文原版）

**Description**

You are playing a game that contains multiple characters, and each of the characters has two main properties: attack and defense. You are given a 2D integer array properties where properties[i] = [attacki, defensei] represents the properties of the ith character in the game.
A character is said to be weak if any other character has both attack and defense levels strictly greater than this character's attack and defense levels. More formally, a character i is said to be weak if there exists another character j where attackj > attacki and defensej > defensei.
Return the number of weak characters.

**Examples**

**Example 1:**

```
Input: properties = [[5,5],[6,3],[3,6]]
Output: 0
Explanation: No character has strictly greater attack and defense than the other.
```

**Example 2:**

```
Input: properties = [[2,2],[3,3]]
Output: 1
Explanation: The first character is weak because the second character has a strictly greater attack and defense.
```

**Example 3:**

```
Input: properties = [[1,5],[10,4],[4,3]]
Output: 1
Explanation: The third character is weak because the second character has a strictly greater attack and defense.
```

**Constraints**

- 2 <= properties.length <= 105
- properties[i].length == 2
- 1 <= attacki, defensei <= 105

---

## 题目（中文翻译）

你正在玩一个包含多个角色的游戏，每个角色都有两个主要属性：攻击（attack）和防御（defense）。给定一个二维整数数组 `properties`，其中 `properties[i] = [attack_i, defense_i]` 表示第 `i` 个角色的属性。

如果存在另一个角色的攻击和防御水平都严格大于该角色的攻击和防御水平，则该角色被称为**弱角色**（weak）。形式化地说，若存在另一个角色 `j` 满足 `attack_j > attack_i` 且 `defense_j > defense_i`，则角色 `i` 为弱角色。

返回弱角色的数量。

## 示例

### 示例 1
**输入:** `properties = [[5,5],[6,3],[3,6]]`  
**输出:** `0`  
**解释:** 没有任何角色的攻击和防御同时严格大于其他角色。

### 示例 2
**输入:** `properties = [[2,2],[3,3]]`  
**输出:** `1`  
**解释:** 第一个角色是弱角色，因为第二个角色的攻击和防御都严格更高。

### 示例 3
**输入:** `properties = [[1,5],[10,4],[4,3]]`  
**输出:** `1`  
**解释:** 第三个角色是弱角色，因为第二个角色的攻击和防御都严格更高。

## 约束条件
- `2 <= properties.length <= 10^5`
- `properties[i].length == 2`
- `1 <= attack_i, defense_i <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把每个角色都和其它所有角色两两比较：

- 对于角色 `i`，遍历所有角色 `j`（`j ≠ i`），检查是否同时满足  
  `attack[j] > attack[i]` **且** `defense[j] > defense[i]`。  
- 只要找到这样一个 `j`，`i` 就算是 **weak**（弱角色），计数加一。

**用到的数据结构**  
- `list`：把 `properties` 按原顺序保存，直接遍历即可。  
- 两层 `for` 循环：相当于把所有角色排成一排，一人一人去“比较”。可以把它想象成在课堂上让每个学生和全班同学依次比较身高和体重，找出被“更高更重”同学压制的学生。

**为什么正确**  
因为我们穷举了**所有可能的配对**，只要存在满足条件的配对，就一定会被检测到，所以计数必然准确。

**时间/空间复杂度**  
- 时间复杂度：两层循环遍历 `n` 个角色，最坏情况要比较 `n·(n‑1)` 次，记作 **O(n²)**。  
  - 大白话：如果有 10 000 个角色，暴力解大约要比较 100 000 000 次，计算量会很快炸掉机器。
- 空间复杂度：只用了原数组和几个计数变量，**O(1)**（不随 `n` 增长）。

#### 代码（Python）

```python
def numberOfWeakCharacters(properties):
    """
    暴力解：两层循环逐一比较
    """
    n = len(properties)
    weak_cnt = 0                     # 记录弱角色数量

    for i in range(n):
        attack_i, defense_i = properties[i]
        # 检查是否存在比 i 更强的角色
        for j in range(n):
            if i == j:
                continue            # 同一个角色不比较
            attack_j, defense_j = properties[j]
            if attack_j > attack_i and defense_j > defense_i:
                weak_cnt += 1        # i 是弱角色
                break                # 找到一个即可，无需再继续比较

    return weak_cnt
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层遍历，每个角色要和所有其他角色比一次。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**大量重复比较**。  
观察题目可以发现：

1. 只要有一个角色的 **攻击值** 更大，且 **防御值** 更大，就能让所有攻击值更小且防御值更低的角色变弱。  
2. 当攻击值相等时，**防御值不影响**（因为攻击必须严格更大），所以同攻击值的角色之间不需要相互比较。

基于这两个观察，我们可以把角色先按照 **攻击值降序** 排序（攻击大的在前），在遍历的过程中维护**已经出现的最大防御值**。  

- 当我们从左到右遍历（攻击值从大到小），如果当前角色的防御值 **小于** 之前出现的最大防御值，那么必定存在一个攻击更大且防御更大的角色，使它成为弱角色。  
- 否则，就更新当前的最大防御值。

**为什么这样可以一次遍历完成？**  
因为排序后，所有在当前角色左侧的角色的攻击值必然 **不小于** 当前角色的攻击值。若左侧已经出现了更大的防御值，那么必然对应的攻击值也更大（因为我们是降序），于是条件 `attackj > attacki && defensej > defensei` 同时满足。

**关键点：处理相同攻击值的情况**  
如果两个角色的攻击值相同，后面的角色不应该被前面的角色“压制”。为避免这种误判，我们在排序时把 **防御值按升序** 放在攻击相同的组内部，这样在遍历时同攻击组的防御值会从小到大出现，保证不会因为同组内的防御更大而错误计数。  

> 类比：想象把所有学生先按照身高从高到低排好队，身高相同的学生再按体重从低到高排。然后从队首往后走，只要遇到体重比之前最高体重小的学生，就说明前面有更高更重的学生把他“压”了。

#### 代码（Python）

```python
def numberOfWeakCharacters(properties):
    """
    最优解：先按 attack 降序、defense 升序排序，
    再一次遍历维护已见最大 defense。
    """
    # 1. 排序：攻击大的在前，攻击相同的按照防御从小到大排
    properties.sort(key=lambda x: (-x[0], x[1]))
    # 示例排序后：[[10,4], [5,5], [5,3], [3,6]] ...

    max_defense_sofar = 0   # 当前遍历到位置左侧出现的最大防御值
    weak_cnt = 0

    for attack, defense in properties:
        # 2. 如果当前防御小于左侧出现的最大防御，说明有更强的角色
        if defense < max_defense_sofar:
            weak_cnt += 1
        else:
            # 否则更新最大防御值
            max_defense_sofar = defense

    return weak_cnt
```

#### 复杂度

- **时间复杂度**：`O(n log n)` —— 主要耗时在排序，`n` 为角色数量。一次线性遍历是 `O(n)`，不影响整体复杂度。  
  - 对比暴力的 `O(n²)`，当 `n` 达到 `10⁵` 时，`n log n`（约 1.7 × 10⁶）可以轻松跑完，而 `n²`（约 10¹⁰）根本不可行。
- **空间复杂度**：`O(1)`（若使用原地排序）或 `O(n)`（Python 的 Timsort 需要额外的临时数组），但不随输入规模指数增长，通常视作常数级别。

---

## 心得

- **核心技巧**：先排序再单次遍历，利用**单调性**（这里是单调递减的攻击 + 单调递增的防御）把二维比较压缩成一维比较。  
- **适用的题型**  
  1. “最大矩形/最大星座”类需要在一个维度排序后维护另一个维度的最值（如 LeetCode 354 – Russian Doll Envelopes）。  
  2. “前缀最大/最小”类问题，常见于区间查询、股票买卖最大利润等。  
  3. “单调栈”或“单调队列”问题，思路相似：维护一个单调序列，快速判断是否存在更优解。  
- **一句话总结解题钥匙**：**先把“大局”排好顺序，再用一次遍历记录“历史最高”，比历史最高小的就是弱角色。**

---

## 反思

- **第一反应**：想到两层循环直接比较，虽然能解出答案，却忽视了数据规模会导致超时。  
- **最容易踩的坑**  
  - **攻击相同的处理**：如果仅按攻击降序排序，攻击相同的角色防御值大的会先出现，导致错误计数。必须在攻击相同的情况下把防御升序排列。  
  - **防御值的更新时机**：只有当当前防御不小于历史最大防御时才更新，否则会把本应弱的角色误当作更强的基准。  
  - **边界条件**：全局只有一种攻击值时，答案必然为 0，需要保证代码在这种极端情况下仍然返回 0。  
- **下次遇到同类题**：第一步先**考虑排序**，把“必须同时更大”的两个维度拆成“一维排序 + 维护最大/最小”。这一步往往能把指数级的暴力搜索降到 `O(n log n)`。