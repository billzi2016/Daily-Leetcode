# #2347. 最佳扑克手牌 / Best Poker Hand

> 难度：简单 · 标签：Array、Hash Table、Counting · [LeetCode 链接](https://leetcode.com/problems/best-poker-hand/)

---

## 题目（英文原版）

**Description**

You are given an integer array ranks and a character array suits. You have 5 cards where the ith card has a rank of ranks[i] and a suit of suits[i].
The following are the types of poker hands you can make from best to worst:
Return a string representing the best type of poker hand you can make with the given cards.
Note that the return values are case-sensitive.

**Examples**

**Example 1:**

```
Input: ranks = [13,2,3,1,9], suits = ["a","a","a","a","a"]
Output: "Flush"
Explanation: The hand with all the cards consists of 5 cards with the same suit, so we have a "Flush".
```

**Example 2:**

```
Input: ranks = [4,4,2,4,4], suits = ["d","a","a","b","c"]
Output: "Three of a Kind"
Explanation: The hand with the first, second, and fourth card consists of 3 cards with the same rank, so we have a "Three of a Kind".
Note that we could also make a "Pair" hand but "Three of a Kind" is a better hand.
Also note that other cards could be used to make the "Three of a Kind" hand.
```

**Example 3:**

```
Input: ranks = [10,10,2,12,9], suits = ["a","b","c","a","d"]
Output: "Pair"
Explanation: The hand with the first and second card consists of 2 cards with the same rank, so we have a "Pair".
Note that we cannot make a "Flush" or a "Three of a Kind".
```

**Constraints**

- ranks.length == suits.length == 5
- 1 <= ranks[i] <= 13
- 'a' <= suits[i] <= 'd'
- No two cards have the same rank and suit.

---

## 题目（中文翻译）

你得到一个整数数组 `ranks` 和一个字符数组 `suits`。共有 5 张牌，其中第 `i` 张牌的点数为 `ranks[i]`，花色为 `suits[i]`。  

从最好到最差，扑克手牌的类型如下（按从高到低的顺序列出）：

- **Royal Flush**  
- **Straight Flush**  
- **Four of a Kind**  
- **Full House**  
- **Flush**  
- **Straight**  
- **Three of a Kind**  
- **Two Pair**  
- **Pair**  
- **High Card**

返回一个字符串，表示使用给定的 5 张牌能够组成的最佳手牌类型。返回值区分大小写。

---

### 示例

#### 示例 1
**输入**: `ranks = [13,2,3,1,9]`, `suits = ["a","a","a","a","a"]`  
**输出**: `"Flush"`  
**解释**: 所有 5 张牌的花色相同，因此构成了 **Flush**（同花）。

#### 示例 2
**输入**: `ranks = [4,4,2,4,4]`, `suits = ["d","a","a","b","c"]`  
**输出**: `"Three of a Kind"`  
**解释**: 第 1、2、4 张牌的点数相同，构成 **Three of a Kind**（三条）。虽然也可以组成 **Pair**（一对），但 **Three of a Kind** 更好。其他牌也可以用于组成这手 **Three of a Kind**。

#### 示例 3
**输入**: `ranks = [10,10,2,12,9]`, `suits = ["a","b","c","a","d"]`  
**输出**: `"Pair"`  
**解释**: 第 1、2 张牌的点数相同，构成 **Pair**（一对）。无法组成 **Flush**（同花）或 **Three of a Kind**（三条）。

---

### 约束条件
- `ranks.length == suits.length == 5`
- `1 <= ranks[i] <= 13`
- `'a' <= suits[i] <= 'd'`
- 任意两张牌的点数和花色的组合均不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有的“判断”都用两层循环手动去验证：

1. **是否同花（Flush）**  
   - 把每一张牌的花色（`suits[i]`）和第一张牌的花色比较，全部相同才算同花。  
   - 这相当于我们在“查字典”，把每张牌的花色当成“单词”，把第一张的花色当成“答案”，逐个比对。

2. **是否三条（Three of a Kind）**  
   - 对每一种牌面（`ranks[i]`），在剩下的四张牌里找是否还有两张同样的牌面。  
   - 想象我们在一堆相同颜色的球里找相同颜色的三个球，最笨的办法就是一球一球去比较。

3. **是否对子（Pair）**  
   - 同理，只要找到任意两张牌的牌面相同即可。  

4. **否则返回 “High Card”**（题目里没有要求，但为了完整性我们加上）。

> **为什么正确？**  
> 只要我们把所有可能的“同花、三条、对子”检查一遍，必然能找出最高等级的牌型。因为这几类牌型之间是严格的层级关系：同花 > 三条 > 对子 > 高牌。

> **复杂度分析（大白话）**  
> - 我们用了两层循环，每层最多遍历 5 张牌，所以最多比较 5×5=25 次。  
> - 在算法分析里，用 **O(n²)** 来表示“随输入规模 n 的平方增长”。这里 n=5，实际比较次数只有 25 次，几乎可以忽略不计，但在概念上我们仍然把它称为 **O(n²)**。  
> - 额外的存储几乎为零，只用了几个计数变量，记作 **O(1)**（常数空间）。

#### 代码（Python）

```python
def bestHand(ranks, suits):
    # 1️⃣ 检查 Flush：所有花色相同吗？
    same_suit = True                 # 假设全部相同
    first_suit = suits[0]
    for s in suits:                  # 逐个比对
        if s != first_suit:          # 只要有一张不同，就不是 Flush
            same_suit = False
            break
    if same_suit:
        return "Flush"

    # 2️⃣ 检查 Three of a Kind：有没有出现 3 次以上的牌面？
    for i in range(5):
        cnt = 0                      # 统计当前牌面出现了几次
        for j in range(5):
            if ranks[i] == ranks[j]:
                cnt += 1
        if cnt >= 3:                 # 找到 >=3 次，说明是三条
            return "Three of a Kind"

    # 3️⃣ 检查 Pair：有没有出现 2 次的牌面？
    for i in range(5):
        cnt = 0
        for j in range(5):
            if ranks[i] == ranks[j]:
                cnt += 1
        if cnt >= 2:                 # 找到 >=2 次，说明是对子
            return "Pair"

    # 4️⃣ 什么都没有，就返回 High Card（题目未要求，可选）
    return "High Card"
```

#### 复杂度

- **时间复杂度：O(n²)** — 这里的 *n* 是牌的数量（5），两层循环导致比较次数随 *n* 的平方增长。  
- **空间复杂度：O(1)** — 只用了常数个变量，不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于我们反复遍历同一批牌去计数（比如两层循环）。其实，只要一次遍历就能把每张牌的花色和牌面出现次数统计出来，后面只需要看统计结果即可。这正好可以用 **哈希表（字典）** 来实现：

1. **统计花色出现次数**  
   - 用一个字典 `suit_cnt`，键是花色，值是出现次数。  
   - 如果字典里唯一的键只有一个，说明所有牌的花色相同 → **Flush**。

2. **统计牌面出现次数**  
   - 用另一个字典 `rank_cnt`，键是牌面，值是出现次数。  
   - 只要字典里出现次数 ≥3 的键，就是 **Three of a Kind**。  
   - 否则，只要出现次数 ≥2 的键，就是 **Pair**。

3. **若都不满足，返回 “High Card”**（同上）。

> **为什么更快？**  
> - 只遍历一次数组（5 次），在遍历过程中把信息“顺手”记录进字典。  
> - 之后的判断只看字典的统计结果，**不再需要额外的循环**。  
> - 这把时间复杂度从 **O(n²)** 降到了 **O(n)**，在理论上对大规模数据会快很多（虽然这里 n 固定为 5，提升不明显，但思路是通用的）。

> **核心数据结构——哈希表**  
> - 想象哈希表像一本“查字典”，我们把每张牌的花色（或牌面）当作“单词”，把它出现的次数当作“页码”。查一次就能得到出现次数，时间几乎是 **O(1)**，所以整体是线性时间。

#### 代码（Python）

```python
def bestHand(ranks, suits):
    # 1️⃣ 统计每种花色出现的次数（相当于查字典）
    suit_cnt = {}
    for s in suits:
        suit_cnt[s] = suit_cnt.get(s, 0) + 1   # get() 若不存在返回 0

    # 若唯一的花色出现了 5 次，说明全是同一种花色 → Flush
    if len(suit_cnt) == 1:                     # 字典只有一个键
        return "Flush"

    # 2️⃣ 统计每种牌面出现的次数
    rank_cnt = {}
    for r in ranks:
        rank_cnt[r] = rank_cnt.get(r, 0) + 1

    # 检查是否有出现 ≥3 次的牌面 → Three of a Kind
    if any(cnt >= 3 for cnt in rank_cnt.values()):
        return "Three of a Kind"

    # 检查是否有出现 ≥2 次的牌面 → Pair
    if any(cnt >= 2 for cnt in rank_cnt.values()):
        return "Pair"

    # 没有任何组合，返回 High Card（可选）
    return "High Card"
```

#### 复杂度

- **时间复杂度：O(n)** — 只遍历一次 `ranks` 与 `suits`（共 5 次），每次操作都是常数时间。  
  与暴力解的 **O(n²)** 相比，提升了一个数量级，理论上在数据更大时会快很多。  
- **空间复杂度：O(1)** — 虽然用了两个字典，但键的种类最多只有 4 种花色和 13 种牌面，都是常数级别的空间。

---

## 心得

- **核心技巧**：利用哈希表一次遍历完成计数，然后根据计数结果直接判断牌型。  
- **适用的题型**  
  1. “统计出现次数”类题目，如 **“Number of Good Pairs”**、**“Find the Difference of Two Arrays”**。  
  2. “判断是否全相同/是否出现一定次数”类，如 **“Valid Sudoku”**（检查行/列/宫是否出现重复数字）。  
  3. “基于频率的分组”类，如 **“Group Anagrams”**。  
- **一句话总结**：**把所有信息一次性收进哈希表，后面只看计数**，是处理“出现次数”问题的万能钥匙。

## 反思

- **第一反应**：看到只有 5 张牌，直接想用两层循环逐个比较，觉得最直观。  
- **最容易踩的坑**  
  - 忘记先检查 **Flush**，导致在出现同花且有对子时错误返回 “Three of a Kind”。  
  - 统计时把 **“出现 ≥3 次”** 与 **“出现 ≥2 次”** 的顺序写反，导致把三条误判为对子。  
- **下次思路**：一看到“出现次数”或“是否全部相同”这类关键词，就立刻想到 **哈希表计数**，先把计数做好，再按优先级顺序检查即可。