# #1452. 人员的喜欢公司列表不是其他列表的子集 / People Whose List of Favorite Companies Is Not a Subset of Another List

> 难度：中等 · 标签：Array、Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/people-whose-list-of-favorite-companies-is-not-a-subset-of-another-list/)

---

## 题目（英文原版）

**Description**

Given the array favoriteCompanies where favoriteCompanies[i] is the list of favorites companies for the ith person (indexed from 0).
Return the indices of people whose list of favorite companies is not a subset of any other list of favorites companies. You must return the indices in increasing order.

**Examples**

**Example 1:**

```
Input: favoriteCompanies = [["leetcode","google","facebook"],["google","microsoft"],["google","facebook"],["google"],["amazon"]]
Output: [0,1,4] 
Explanation: 
Person with index=2 has favoriteCompanies[2]=["google","facebook"] which is a subset of favoriteCompanies[0]=["leetcode","google","facebook"] corresponding to the person with index 0. 
Person with index=3 has favoriteCompanies[3]=["google"] which is a subset of favoriteCompanies[0]=["leetcode","google","facebook"] and favoriteCompanies[1]=["google","microsoft"]. 
Other lists of favorite companies are not a subset of another list, therefore, the answer is [0,1,4].
```

**Example 2:**

```
Input: favoriteCompanies = [["leetcode","google","facebook"],["leetcode","amazon"],["facebook","google"]]
Output: [0,1] 
Explanation: In this case favoriteCompanies[2]=["facebook","google"] is a subset of favoriteCompanies[0]=["leetcode","google","facebook"], therefore, the answer is [0,1].
```

**Example 3:**

```
Input: favoriteCompanies = [["leetcode"],["google"],["facebook"],["amazon"]]
Output: [0,1,2,3]
```

**Constraints**

- 1 <= favoriteCompanies.length <= 100
- 1 <= favoriteCompanies[i].length <= 500
- 1 <= favoriteCompanies[i][j].length <= 20
- All strings in favoriteCompanies[i] are distinct.
- All lists of favorite companies are distinct, that is, If we sort alphabetically each list then favoriteCompanies[i] != favoriteCompanies[j].
- All strings consist of lowercase English letters only.

---

## 题目（中文翻译）

给定数组 `favoriteCompanies`，其中 `favoriteCompanies[i]` 是第 `i` 个人（下标从 `0` 开始）的喜欢公司列表（list）。  
返回那些 **其喜欢公司列表不是任何其他列表的子集（subset）** 的人的下标。返回的下标需按升序排列。

## 示例

### 示例 1
```text
Input: favoriteCompanies = [["leetcode","google","facebook"],["google","microsoft"],["google","facebook"],["google"],["amazon"]]
Output: [0,1,4] 
```
**解释**：  
下标为 `2` 的人其 `favoriteCompanies[2] = ["google","facebook"]` 是下标为 `0` 的人 `favoriteCompanies[0] = ["leetcode","google","facebook"]` 的子集（subset）。  
下标为 `3` 的人其 `favoriteCompanies[3] = ["google"]` 同样是 `favoriteCompanies[0]` 的子集（subset），因此它们不在答案中。

### 示例 2
```text
Input: favoriteCompanies = [["leetcode","google","facebook"],["leetcode","amazon"],["facebook","google"]]
Output: [0,1] 
```
**解释**：此例中 `favoriteCompanies[2] = ["facebook","google"]` 是 `favoriteCompanies[0] = ["leetcode","google","facebook"]` 的子集（subset），所以答案为 `[0,1]`。

### 示例 3
```text
Input: favoriteCompanies = [["leetcode"],["google"],["facebook"],["amazon"]]
Output: [0,1,2,3]
```
**解释**：每个人的列表互不包含对方的子集（subset），因此全部下标都在答案中。

## 约束条件

- `1 <= favoriteCompanies.length <= 100`
- `1 <= favoriteCompanies[i].length <= 500`
- `1 <= favoriteCompanies[i][j].length <= 20`
- `favoriteCompanies[i]` 中的所有字符串互不相同。
- 所有喜欢公司列表互不相同，即对每个列表按字母序排序后，`favoriteCompanies[i] != favoriteCompanies[j]`（`i != j`）。
- 所有字符串仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **两两比较**：  

1. 把每个人的喜欢公司列表转换成 `set`（集合）。  
   - 集合就像“字典”，把公司名放进去后可以**快速判断**某个公司是否在列表里，时间几乎是 O(1)。  
2. 对于每个下标 `i`，遍历所有其它下标 `j`（`j != i`），检查 `set_i` 是否是 `set_j` 的子集。  
   - 子集的定义是：`set_i` 的每一个元素都能在 `set_j` 中找到。  
3. 只要找到一个 `j` 使得 `set_i ⊆ set_j`，就说明第 `i` 个人不满足题目要求，可以直接把 `i` 排除。  
4. 最后把所有没有被排除的下标按升序返回。

> **为什么正确**  
> 如果 `set_i` 不是任何其他集合的子集，那么它一定满足题目 “不是其他人列表的子集”。反之，只要它是某个集合的子集，就不符合要求。两两比较恰好覆盖了所有可能的 “是否为子集” 的判断。

> **复杂度大白话**  
> - `n` 是人数（即列表的个数），最多 100。  
> - `m` 是单个列表里公司的最多数量，最多 500。  
> - 对每一对 `(i, j)`（一共有 `n·(n‑1)` ≈ `n²` 对）我们要检查最多 `m` 个公司是否全部在另一个集合里。  
>   所以总的时间是 **O(n²·m)**。  
> - 每个人的集合本身需要存储所有公司名，空间是 **O(n·m)**。

#### 代码（Python）

```python
from typing import List

def peopleIndexes(favoriteCompanies: List[List[str]]) -> List[int]:
    n = len(favoriteCompanies)

    # 把每个人的公司列表装进集合，方便 O(1) 判断元素是否存在
    sets = [set(companies) for companies in favoriteCompanies]

    # 记录哪些下标需要保留，初始都保留
    keep = [True] * n

    # 两两比较
    for i in range(n):
        if not keep[i]:          # 已经确定被排除，就不必再比较
            continue
        for j in range(n):
            if i == j:
                continue
            # 如果 i 的集合是 j 的子集，则 i 需要被排除
            if sets[i].issubset(sets[j]):
                keep[i] = False
                break               # 找到一个即可，直接结束内层循环

    # 收集所有仍然为 True 的下标，返回升序列表
    return [idx for idx, ok in enumerate(keep) if ok]
```

#### 复杂度  

- **时间复杂度**：`O(n²·m)`  
  - `n²` 表示两两比较的次数，`m` 表示每次子集检查最多遍历的元素数。  
  - 对于本题的最大规模（`n=100, m=500`），约为 `100·100·500 = 5,000,000` 次基本操作，仍在可接受范围。  

- **空间复杂度**：`O(n·m)`  
  - 用 `set` 保存每个人的公司列表，需要存储所有公司字符串（或其哈希值）共 `n·m` 个。  

---

### 2. 最优解  

#### 思路  

暴力解已经能 AC，但我们可以把 **“字符串比较”** 的成本降下来，使程序跑得更快。  
主要的优化点有两处：

1. **把公司名字映射成整数**  
   - 字符串比较要逐字符比，对比成本较高。我们先遍历所有公司名字，给每个不同的名字分配一个唯一的整数 ID（类似字典查词典的过程），后面的所有比较都在整数之间完成。  
   - 这一步只需要一次遍历，时间是 `O(total number of names)`，空间是 `O(distinct names)`。

2. **对每个列表进行排序 + 双指针检查子集**  
   - 把每个人的公司 ID 列表排序后，子集判断可以用 **双指针**（两根指针）线性完成：  
     - 指针 `i` 遍历较小的列表，指针 `j` 遍历较大的列表。  
     - 当 `small[i] == large[j]` 时，说明找到了对应的公司，两个指针都右移；  
     - 当 `small[i] > large[j]` 时，说明大列表的当前公司比小列表的目标小，只有 `j` 右移；  
     - 当 `small[i] < large[j]` 时，说明小列表里有公司根本不在大列表里，直接判定 **不是子集**。  
   - 由于每个列表最多遍历一次，这一步的复杂度是 `O(m)`，而不是集合的 `O(m)`（集合内部仍有哈希开销）。  

综合起来，整体时间仍是 `O(n²·m)`，但常数更小，尤其在公司名字较长时优势明显。

> **为什么正确**  
> - 将公司名映射为唯一整数后，两个列表的相等关系不变，子集关系也不变。  
> - 排序后，双指针的过程恰好实现了 “逐个匹配” 的子集检查，若所有小列表的元素都能在大列表中找到，则说明它是子集；否则就不是。  

#### 代码（Python）

```python
from typing import List

def peopleIndexes(favoriteCompanies: List[List[str]]) -> List[int]:
    # ---------- 第一步：把所有公司名字映射成整数 ----------
    # 所有出现过的公司名放进一个集合，随后统一编号
    all_names = set(name for lst in favoriteCompanies for name in lst)
    name_to_id = {name: idx for idx, name in enumerate(all_names)}   # O(total names)

    # ---------- 第二步：把每个人的列表转成整数并排序 ----------
    # 这里每个子列表都是一个已排序的整数数组
    int_lists = []
    for lst in favoriteCompanies:
        ids = [name_to_id[name] for name in lst]   # 把名字换成整数
        ids.sort()                                 # 为双指针做准备
        int_lists.append(ids)

    n = len(int_lists)
    keep = [True] * n

    # ---------- 第三步：两两比较，使用双指针判断子集 ----------
    for i in range(n):
        if not keep[i]:
            continue
        for j in range(n):
            if i == j:
                continue
            # 只在 i 列表长度 <= j 列表长度时才有可能是子集
            if len(int_lists[i]) > len(int_lists[j]):
                continue

            # 双指针检查 int_lists[i] 是否是 int_lists[j] 的子集
            a, b = int_lists[i], int_lists[j]
            p = q = 0
            while p < len(a) and q < len(b):
                if a[p] == b[q]:
                    p += 1
                    q += 1
                elif a[p] > b[q]:
                    q += 1               # 大列表指针前进，寻找匹配
                else:                    # a[p] < b[q]，说明小列表里有不在大列表的元素
                    break
            # 若 p 走完了，说明所有元素都匹配成功，即为子集
            if p == len(a):
                keep[i] = False
                break   # 已经确认 i 不是答案，直接结束内层循环

    # ---------- 第四步：收集答案 ----------
    return [idx for idx, ok in enumerate(keep) if ok]
```

#### 复杂度  

- **时间复杂度**：`O(n²·m)`（与暴力解同阶）  
  - 主要耗时仍然是两两比较，每次子集检查最多遍历两列表的长度之和 ≤ `2·m`。  
  - 由于我们把字符串比较换成整数比较、并且使用双指针避免了集合的哈希开销，实际运行时间会更快。  

- **空间复杂度**：`O(n·m + D)`  
  - `n·m` 用于保存所有整数列表（相当于原始数据的整数版）。  
  - `D` 是不同公司名字的数量，用于 `name_to_id` 哈希表。  

---

## 心得  

- **核心技巧**：  
  1. **哈希映射**（把字符串转成整数）降低比较成本。  
  2. **双指针**（两根指针线性遍历已排序数组）高效判断子集关系。  

- **适用的题型**（可以套用相同思路）：  
  - “检查数组 A 是否是数组 B 的子集” 类似问题。  
  - “两个集合的交集/并集大小” 需要先排序再双指针。  
  - “找出所有不被其他集合覆盖的集合” （本题的变体）。  

- **一句话总结解题钥匙**：  
  > 把“比较字符串”转成“比较整数”，再用 **排序 + 双指针** 把子集判定降到线性时间。

---

## 反思  

- **第一反应**：直接把每个列表转成 `set`，用 `issubset` 两两比较。  
- **最容易踩的坑**：  
  - 忘记先判断长度，若 `list_i` 更长，肯定不可能是子集，直接跳过可以省不少时间。  
  - 边界条件：当两个人的列表完全相同时（题目保证不会出现），也会被误判为子集，需要注意题目约束。  
- **下次遇到同类题**：第一步先 **把元素映射为整数并排序**，然后 **用双指针做子集/交集判断**，这样既省时又省空间。