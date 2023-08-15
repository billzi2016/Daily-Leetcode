# #2363. 合并相似物品 / Merge Similar Items

> 难度：简单 · 标签：Array、Hash Table、Sorting、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/merge-similar-items/)

---

## 题目（英文原版）

**Description**

You are given two 2D integer arrays, items1 and items2, representing two sets of items. Each array items has the following properties:
Return a 2D integer array ret where ret[i] = [valuei, weighti], with weighti being the sum of weights of all items with value valuei.
Note: ret should be returned in ascending order by value.

**Examples**

**Example 1:**

```
Input: items1 = [[1,1],[4,5],[3,8]], items2 = [[3,1],[1,5]]
Output: [[1,6],[3,9],[4,5]]
Explanation: 
The item with value = 1 occurs in items1 with weight = 1 and in items2 with weight = 5, total weight = 1 + 5 = 6.
The item with value = 3 occurs in items1 with weight = 8 and in items2 with weight = 1, total weight = 8 + 1 = 9.
The item with value = 4 occurs in items1 with weight = 5, total weight = 5.  
Therefore, we return [[1,6],[3,9],[4,5]].
```

**Example 2:**

```
Input: items1 = [[1,1],[3,2],[2,3]], items2 = [[2,1],[3,2],[1,3]]
Output: [[1,4],[2,4],[3,4]]
Explanation: 
The item with value = 1 occurs in items1 with weight = 1 and in items2 with weight = 3, total weight = 1 + 3 = 4.
The item with value = 2 occurs in items1 with weight = 3 and in items2 with weight = 1, total weight = 3 + 1 = 4.
The item with value = 3 occurs in items1 with weight = 2 and in items2 with weight = 2, total weight = 2 + 2 = 4.
Therefore, we return [[1,4],[2,4],[3,4]].
```

**Example 3:**

```
Input: items1 = [[1,3],[2,2]], items2 = [[7,1],[2,2],[1,4]]
Output: [[1,7],[2,4],[7,1]]
Explanation:
The item with value = 1 occurs in items1 with weight = 3 and in items2 with weight = 4, total weight = 3 + 4 = 7. 
The item with value = 2 occurs in items1 with weight = 2 and in items2 with weight = 2, total weight = 2 + 2 = 4. 
The item with value = 7 occurs in items2 with weight = 1, total weight = 1.
Therefore, we return [[1,7],[2,4],[7,1]].
```

**Constraints**

- 1 <= items1.length, items2.length <= 1000
- items1[i].length == items2[i].length == 2
- 1 <= valuei, weighti <= 1000
- Each valuei in items1 is unique.
- Each valuei in items2 is unique.

---

## 题目（中文翻译）

**题目描述**  
给你两个二维整数数组（2D integer array），`items1` 和 `items2`，分别表示两组物品。每个数组中的每个元素 `items[i] = [value_i, weight_i]` 表示一种物品，其中 `value_i` 为物品的价值，`weight_i` 为物品的重量。  
请你返回一个二维整数数组（2D integer array） `ret`，其中 `ret[i] = [value_i, weight_i]`，`weight_i` 为所有价值为 `value_i` 的物品的重量之和。  
**注意**：`ret` 必须按照价值 `value_i` 的升序（ascending order）返回。

**示例**  

> 示例 1  
> ```text
> Input: items1 = [[1,1],[4,5],[3,8]], items2 = [[3,1],[1,5]]
> Output: [[1,6],[3,9],[4,5]]
> Explanation: 
> - 价值为 1 的物品在 `items1` 中的重量为 1，在 `items2` 中的重量为 5，合计重量为 1 + 5 = 6。  
> - 价值为 3 的物品在 `items1` 中的重量为 8，在 `items2` 中的重量为 1，合计重量为 8 + 1 = 9。  
> - 价值为 4 的物品仅在 `items1` 中出现，重量为 5。  
> ```

> 示例 2  
> ```text
> Input: items1 = [[1,1],[3,2],[2,3]], items2 = [[2,1],[3,2],[1,3]]
> Output: [[1,4],[2,4],[3,4]]
> Explanation: 
> - 价值为 1 的物品在 `items1` 中的重量为 1，在 `items2` 中的重量为 3，合计重量为 1 + 3 = 4。  
> - 价值为 2 的物品在 `items1` 中的重量为 3，在 `items2` 中的重量为 1，合计重量为 3 + 1 = 4。  
> - 价值为 3 的物品在 `items1` 中的重量为 2，在 `items2` 中的重量为 2，合计重量为 2 + 2 = 4。  
> ```

> 示例 3  
> ```text
> Input: items1 = [[1,3],[2,2]], items2 = [[7,1],[2,2],[1,4]]
> Output: [[1,7],[2,4],[7,1]]
> Explanation:
> - 价值为 1 的物品在 `items1` 中的重量为 3，在 `items2` 中的重量为 4，合计重量为 3 + 4 = 7。  
> - 价值为 2 的物品在 `items1` 中的重量为 2，在 `items2` 中的重量为 2，合计重量为 2 + 2 = 4。  
> - 价值为 7 的物品仅在 `items2` 中出现，重量为 1。  
> ```

**约束条件**  
- `1 <= items1.length, items2.length <= 1000`  
- `items1[i].length == items2[i].length == 2`  
- `1 <= value_i, weight_i <= 1000`  
- `items1` 中的每个 `value_i` 均唯一。  
- `items2` 中的每个 `value_i` 均唯一。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：把两张表 `items1`、`items2` 挨个拿出来，**把所有出现的 value 放进一个大列表**，然后对这个列表**逐个检查**，把相同 value 的 weight 加起来。  

- **用到的数据结构**  
  - `list`（列表）相当于我们生活中的“收集箱”，把所有物品先收进去。  
  - `for` 循环遍历相当于“一张张检查”。  

- **为什么正确**  
  - 题目要求把 **相同 value 的 weight 累加**，只要我们把所有出现的 `(value, weight)` 都遍历一遍，并把同 value 的 weight 累加，就一定得到正确的结果。  

- **复杂度分析（大白话）**  
  - 假设 `n = len(items1) + len(items2)`，即总共的物品数。我们把所有物品放进列表需要 **O(n)** 的时间。  
  - 接下来，对每个物品我们都要在已经收集好的列表里 **遍历一次** 去找相同的 value，最坏情况下每次都要遍历整个列表，时间大约是 `1 + 2 + … + n ≈ n²/2`，所以时间复杂度是 **O(n²)**。  
  - 额外的空间只用了一个列表来存放所有物品，大小正好是 `n`，所以空间复杂度是 **O(n)**。  

#### 代码（Python）  

```python
def mergeSimilarItems_bruteforce(items1, items2):
    # 把两张表直接拼在一起，得到所有 (value, weight) 对
    all_items = items1 + items2          # O(n) 的时间

    # 用一个空列表来存放合并后的结果
    merged = []                          # 最终返回的 list

    # 对每个 (value, weight) 逐个检查
    for value, weight in all_items:      # 外层遍历 n 次
        # 看看 merged 里是否已经有相同的 value
        found = False
        for pair in merged:              # 内层最坏遍历到当前已合并的数量
            if pair[0] == value:         # 找到相同的 value
                pair[1] += weight        # 累加 weight
                found = True
                break
        # 如果遍历完都没有找到，说明是新出现的 value，直接加入
        if not found:
            merged.append([value, weight])

    # 最后按照 value 升序排序
    merged.sort(key=lambda x: x[0])      # O(k log k)，k 为不同的 value 数量

    return merged
```

#### 复杂度  

- **时间复杂度**：**O(n²)**  
  - `n` 为两张表中元素总数。外层遍历 `n` 次，内层最坏遍历已合并的元素，形成平方级别。  
- **空间复杂度**：**O(n)**  
  - 需要存放所有原始元素以及合并后的结果，最多和输入等大。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要遍历已有的结果去找相同的 value**。如果我们能**直接定位**到对应的 value，就可以把这一步从线性搜索降到常数时间。  

这正是 **哈希表（字典）** 的强项：  
- 哈希表像一本 **字典**，我们把 **value 当作单词**，**weight 当作页码**。查找一个单词对应的页码，只需要一次 “快速查找”，时间几乎是 **O(1)**。  

实现步骤：  

1. **创建一个空字典 `cnt`**，键是 `value`，值是累计的 `weight`。  
2. **遍历 `items1`，把每个 `(value, weight)` 放进字典**。如果 `value` 已经在字典里，就把 `weight` 加上去；否则新建键值对。  
3. **同样遍历 `items2`，继续往字典里累加**。这样两张表的所有相同 `value` 自动合并。  
4. **把字典的键值对取出来，按键（value）升序排序**，得到最终的二维数组。  

**为什么正确**  
- 每一次遍历都把对应的 `weight` 加到同一个 `value` 的累计值上，等所有元素都处理完后，字典里每个键对应的值正好是题目要求的 **所有相同 value 的 weight 之和**。  

**复杂度解释**  
- **遍历两张表** 各一次，时间是 **O(n)**（`n` 为总元素数）。  
- **字典的增删改查** 在均摊意义下是 **O(1)**，所以总时间仍是 **O(n)**。  
- **排序** 只针对不同的 `value`（记作 `k`），`k ≤ n`，排序时间是 **O(k log k)**。在最坏情况下 `k = n`，整体仍是 **O(n log n)**。  
- **空间** 需要存放字典里最多 `k` 条记录，**O(k)**，即 **O(n)**。  

#### 代码（Python）  

```python
def mergeSimilarItems(items1, items2):
    """
    使用哈希表（字典）把相同 value 的 weight 合并，
    最后按 value 升序返回结果。
    """
    # 1. 建立空字典，key = value, value = 累计的 weight
    cnt = {}                     # O(1) 的空间

    # 2. 处理 items1
    for value, weight in items1:   # 遍历 n1 次
        if value in cnt:           # 如果已经出现过
            cnt[value] += weight   # 累加 weight
        else:
            cnt[value] = weight    # 第一次出现，建立键值对

    # 3. 处理 items2（同上）
    for value, weight in items2:   # 遍历 n2 次
        if value in cnt:
            cnt[value] += weight
        else:
            cnt[value] = weight

    # 4. 把字典转成列表并按 value 升序排序
    #    sorted 会返回一个新的列表，key=lambda x: x[0] 表示按键（value）排序
    result = sorted(cnt.items(), key=lambda x: x[0])   # O(k log k)

    # 5. 将 (value, weight) 的 tuple 转成题目要求的 [value, weight] 形式
    return [[value, weight] for value, weight in result]
```

#### 复杂度  

- **时间复杂度**：**O(n log n)**（其中 `n = len(items1) + len(items2)`）  
  - 两次线性遍历是 **O(n)**，排序是 **O(k log k)**，`k ≤ n`，综合为 **O(n log n)**。相比暴力的 **O(n²)** 快很多。  
- **空间复杂度**：**O(k)**（`k` 为不同的 value 个数，最多 `n`）  
  - 只额外用了一个字典来记录累计的 weight。  

---

## 心得  

- **核心技巧**：使用 **哈希表（字典）** 实现“以 value 为键的快速累加”。  
- **适用的题型**  
  1. 合并两个或多个列表中相同键的数值（如 “Two Sum IV - Input is a BST” 的计数）  
  2. 统计字符出现次数（LeetCode 383 “Ransom Note”）  
  3. 合并相同坐标的点的权重（LeetCode 1825 “Sorting the Students by Their Scores”）  
- **一句话总结解题钥匙**：**把“寻找相同 value”这一步交给字典，让它在 O(1) 时间内帮你定位**。  

---

## 反思  

- **第一反应**：把两张表直接拼在一起，然后手动遍历合并。  
- **最容易踩的坑**  
  - 忘记对结果进行 **升序排序**，导致输出顺序不符合要求。  
  - 没有考虑 **value 只在其中一张表出现** 的情况，直接假设两张表都有对应键会导致 KeyError。  
- **下次遇到同类题**：第一步先想 **“能不能用哈希表把键映射到累计值”**，如果可以，就直接用字典实现；如果键的范围很大且要求有序，后面再考虑使用 **有序容器**（如 `OrderedDict` 或排序）来输出。