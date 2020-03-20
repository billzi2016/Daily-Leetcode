# #811. 子域名访问计数 / Subdomain Visit Count

> 难度：中等 · 标签：Array、Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/subdomain-visit-count/)

---

## 题目（英文原版）

**Description**

A website domain "discuss.leetcode.com" consists of various subdomains. At the top level, we have "com", at the next level, we have "leetcode.com" and at the lowest level, "discuss.leetcode.com". When we visit a domain like "discuss.leetcode.com", we will also visit the parent domains "leetcode.com" and "com" implicitly.
A count-paired domain is a domain that has one of the two formats "rep d1.d2.d3" or "rep d1.d2" where rep is the number of visits to the domain and d1.d2.d3 is the domain itself.
Given an array of count-paired domains cpdomains, return an array of the count-paired domains of each subdomain in the input. You may return the answer in any order.

**Examples**

**Example 1:**

```
Input: cpdomains = ["9001 discuss.leetcode.com"]
Output: ["9001 leetcode.com","9001 discuss.leetcode.com","9001 com"]
Explanation: We only have one website domain: "discuss.leetcode.com".
As discussed above, the subdomain "leetcode.com" and "com" will also be visited. So they will all be visited 9001 times.
```

**Example 2:**

```
Input: cpdomains = ["900 google.mail.com", "50 yahoo.com", "1 intel.mail.com", "5 wiki.org"]
Output: ["901 mail.com","50 yahoo.com","900 google.mail.com","5 wiki.org","5 org","1 intel.mail.com","951 com"]
Explanation: We will visit "google.mail.com" 900 times, "yahoo.com" 50 times, "intel.mail.com" once and "wiki.org" 5 times.
For the subdomains, we will visit "mail.com" 900 + 1 = 901 times, "com" 900 + 50 + 1 = 951 times, and "org" 5 times.
```

**Constraints**

- 1 <= cpdomain.length <= 100
- 1 <= cpdomain[i].length <= 100
- cpdomain[i] follows either the "repi d1i.d2i.d3i" format or the "repi d1i.d2i" format.
- repi is an integer in the range [1, 104].
- d1i, d2i, and d3i consist of lowercase English letters.

---

## 题目（中文翻译）

**描述**  
一个网站域名 `"discuss.leetcode.com"` 包含多个子域名（subdomain）。在最高层是 `"com"`，下一层是 `"leetcode.com"`，最底层是 `"discuss.leetcode.com"`。当我们访问 `"discuss.leetcode.com"` 时，也会隐式访问其父域名 `"leetcode.com"` 和 `"com"`。

计数配对域名（count-paired domain）是指符合以下两种格式之一的字符串：`"rep d1.d2.d3"` 或 `"rep d1.d2"`，其中 `rep` 表示对该域名的访问次数，`d1.d2.d3` 为域名本身。

给定一个计数配对域名数组 `cpdomains`，返回一个数组，包含输入中每个子域名的计数配对域名。答案的顺序可以任意。

**示例 1**  

**示例 2**  

**约束条件**  

- `1 <= cpdomains.length <= 100`  
- `1 <= cpdomains[i].length <= 100`  
- `cpdomains[i]` 符合 `"repi d1i.d2i.d3i"` 或 `"repi d1i.d2i"` 的格式  
- `repi` 为区间 `[1, 10^4]` 内的整数  
- `d1i、d2i、d3i` 仅由小写英文字母组成  

**示例**  

**示例 1:**  
```
Input: cpdomains = ["9001 discuss.leetcode.com"]
Output: ["9001 leetcode.com","9001 discuss.leetcode.com","9001 com"]
Explanation: 我们只有一个网站域名："discuss.leetcode.com"。如前所述，子域名 "leetcode.com" 和 "com" 也会被访问。因此它们的访问次数都是 9001 次。
```

**示例 2:**  
```
Input: cpdomains = ["900 google.mail.com", "50 yahoo.com", "1 intel.mail.com", "5 wiki.org"]
Output: ["901 mail.com","50 yahoo.com","900 google.mail.com","5 wiki.org","5 org","1 intel.mail.com","951 com"]
Explanation: 我们会分别访问 "google.mail.com" 900 次、"yahoo.com" 50 次、"intel.mail.com" 1 次以及 "wiki.org" 5 次。  
对于子域名，"mail.com" 被访问了 900 + 1 = 901 次，"com" 被访问了 900 + 50 + 1 = 951 次，"org" 被访问了 5 次。
```

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

题目要求把每条记录 `"cnt domain"` 拆成所有可能的子域名，然后把相同子域名的访问次数累加。  
最直接的做法就是：

1. **遍历输入数组**，取出每条记录。  
2. 用空格把记录分成 `cnt`（访问次数） 和 `domain`（完整域名）。  
3. 把完整域名按点 `.` 再次切分得到各层级的子串，例如  
   `"discuss.leetcode.com"` → `["discuss", "leetcode", "com"]`。  
4. 从左到右依次拼接得到所有子域名：  
   - 第 1 步：`"discuss.leetcode.com"`  
   - 第 2 步：`"leetcode.com"`（把最左边的 `"discuss"` 去掉）  
   - 第 3 步：`"com"`（再去掉 `"leetcode"`）。  
5. 用一个 **哈希表**（在 Python 中是 `dict`）记录每个子域名出现的次数。哈希表就像一本**查字典**，我们把子域名当作“词”，对应的访问次数当作“页码”。每次看到同一个词，就把页码加上新的次数。  

这个方法 **一定正确**，因为我们对每条原始记录都完整地列举了它对应的所有子域名，并且把次数全部累加进去。

> **时间/空间复杂度直观解释**  
> - `O(n * m)`：`n` 是输入记录的条数（最多 100），`m` 是每条记录中点的个数（最多 3），所以整体是“记录数 × 每条记录里子域的个数”。如果把 `n` 想象成“一堆苹果”，`m` 想象成“每个苹果切成几块”，总工作量就是“所有苹果切块的总数”。  
> - `O(k)`：`k` 是出现过的不同子域名的数量（最坏情况下每条记录都有 3 个子域名），这相当于我们需要用多少本“小字典”来记这些子域名。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def subdomainVisits(cpdomains: List[str]) -> List[str]:
    # 用 defaultdict 自动把不存在的键初始化为 0
    count = defaultdict(int)          # 哈希表：key = 子域名，value = 访问次数

    for entry in cpdomains:            # 逐条处理输入
        # 1) 用空格分离出次数和完整域名
        cnt_str, domain = entry.split()
        cnt = int(cnt_str)             # 把次数从字符串转成整数

        # 2) 把完整域名按 '.' 切分成各层级的部分
        parts = domain.split('.')      # 例如 ["discuss","leetcode","com"]

        # 3) 从左到右依次拼接得到所有子域名
        #   i 从 0 到 len(parts)-1，表示保留从 i 开始到结尾的部分
        for i in range(len(parts)):
            subdomain = ".".join(parts[i:])   # 拼接成子域名字符串
            count[subdomain] += cnt          # 哈希表中累计次数

    # 4) 把哈希表转换成题目要求的 "cnt domain" 形式
    result = [f"{cnt} {dom}" for dom, cnt in count.items()]
    return result
```

#### 复杂度  

- **时间复杂度**：`O(N * L)`  
  - `N` 为 `cpdomains` 的长度（最多 100），`L` 为每个域名中点的个数（最多 3），所以整体是“记录数 × 每条记录的子域数”。  
  - 大白话：如果有 100 条记录，每条最多产生 3 个子域，那么最多要处理 300 次累计操作。

- **空间复杂度**：`O(K)`  
  - `K` 为不同子域名的数量，最坏情况下每条记录都有 3 个不同子域，`K ≤ 3N`。  
  - 也就是我们需要的哈希表大小与输入规模线性相关。

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈并不在遍历或切分**——数据量本来就很小（`N ≤ 100`，每条最多 3 个子域），即使是最直接的实现也足够快。  
因此这里的“最优”主要指**代码简洁度和可读性**，而不是进一步降低时间复杂度。我们可以：

1. **一次性完成切分和累计**：在遍历每条记录时，直接使用 `rpartition` 或 `split` 把次数和域名分离，然后利用 `rsplit('.', 1)` 逐层向左获取父域名，省去显式的 `for i in range(len(parts))` 循环。  
2. **使用 `defaultdict`**：免去判断键是否已存在的代码，使整体更简洁。  

核心技巧仍然是**哈希表计数**，只是在实现细节上做了微调，使代码更易读、行数更少。

> **类比**：把完整域名看成一条链条，`"discuss.leetcode.com"` → `"leetcode.com"` → `"com"`，我们每次只需要把链条的**尾巴**剪掉一次，就得到下一个子域。这个过程类似“从右往左依次摘掉最左边的叶子”。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def subdomainVisits(cpdomains: List[str]) -> List[str]:
    cnt_map = defaultdict(int)          # 哈希表：子域名 → 访问次数

    for entry in cpdomains:
        # 1) 先把 "cnt domain" 分成两部分
        cnt_str, domain = entry.split()
        cnt = int(cnt_str)

        # 2) 采用循环：每次把最左边的子域去掉，直到只剩顶级域名
        cur = domain                     # 当前处理的子域名
        while True:
            cnt_map[cur] += cnt           # 累计次数
            # rsplit 只从右边切一次，得到 (左侧, '.', 右侧)
            # 如果没有 '.'，说明已经是顶级域名，退出循环
            if '.' not in cur:
                break
            # 把左侧的更短子域名取出来继续计数
            cur = cur.split('.', 1)[1]    # 只保留第一次 '.' 之后的部分

    # 3) 按题目要求输出 "cnt domain" 形式
    return [f"{c} {d}" for d, c in cnt_map.items()]
```

#### 复杂度  

- **时间复杂度**：`O(N * L)`（与暴力解相同）  
  - 每条记录我们仍然遍历它的所有子域，只是实现方式更紧凑。  
  - 对于本题的输入规模，这已经是“最优”了，因为没有多余的遍历或复杂的数据结构。

- **空间复杂度**：`O(K)`（与暴力解相同）  
  - 仍然需要保存所有不同子域的计数，大小随输入线性增长。

---  

## 心得  

- **核心技巧**：利用哈希表（字典）对子域名进行计数。  
- **适用的题型**：  
  1. **字符计数** 类题目，例如 “Ransom Note” 需要统计每个字符出现次数。  
  2. **分组统计**，如 “Group Anagrams” 把相同特征的字符串归类。  
  3. **区间累计**，比如 “Number of Boomerangs” 中对点对出现次数的统计。  
- **一句话总结解题钥匙**：**把每个完整域名拆成所有父子域，然后用字典把相同子域的访问次数累加**。

## 反思  

- **第一反应**：看到 “子域名也会被访问”，立刻想到要把每个域名拆成层级并累计。  
- **最容易踩的坑**：  
  - 忘记把次数从字符串转换成整数，导致字符串拼接错误。  
  - 处理顶级域名时没有正确退出循环，导致无限循环或遗漏计数。  
  - 输出格式必须是 `"cnt domain"`，而不是 `domain: cnt` 之类的。  
- **下次类似题的第一步**：先明确“**需要对哪些子结构进行统计**”，然后决定使用哈希表（字典）来累加计数。