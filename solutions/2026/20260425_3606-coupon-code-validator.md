# #3606. 优惠码验证器 / Coupon Code Validator

> 难度：简单 · 标签：Array、Hash Table、String、Sorting · [LeetCode 链接](https://leetcode.com/problems/coupon-code-validator/)

---

## 题目（英文原版）

**Description**

You are given three arrays of length n that describe the properties of n coupons: code, businessLine, and isActive. The ith coupon has:
A coupon is considered valid if all of the following conditions hold:
Return an array of the codes of all valid coupons, sorted first by their businessLine in the order: "electronics", "grocery", "pharmacy", "restaurant", and then by code in lexicographical (ascending) order within each category.

**Examples**

**Example 1:**

```
Input: code = ["SAVE20","","PHARMA5","SAVE@20"], businessLine = ["restaurant","grocery","pharmacy","restaurant"], isActive = [true,true,true,true]
Output: ["PHARMA5","SAVE20"]
Explanation:
```

**Example 2:**

```
Input: code = ["GROCERY15","ELECTRONICS_50","DISCOUNT10"], businessLine = ["grocery","electronics","invalid"], isActive = [false,true,true]
Output: ["ELECTRONICS_50"]
Explanation:
```

**Constraints**

- n == code.length == businessLine.length == isActive.length
- 1 <= n <= 100
- 0 <= code[i].length, businessLine[i].length <= 100
- code[i] and businessLine[i] consist of printable ASCII characters.
- isActive[i] is either true or false.

---

## 题目（中文翻译）

**描述**  
给定三个长度为 `n` 的数组，分别描述 `n` 张优惠券的属性：`code`、`businessLine` 和 `isActive`。第 `i` 张优惠券拥有：

- **code[i]**：优惠码  
- **businessLine[i]**：业务线（business line）  
- **isActive[i]**：是否激活（boolean）

一张优惠券在满足以下所有条件时被视为有效：

（此处应列出题目原文中省略的具体条件）

返回所有有效优惠券的 **code**，按 **businessLine** 的顺序排序，顺序为 `"electronics"`、`"grocery"`、`"pharmacy"`、`"restaurant"`；在同一业务线内，再按 **code** 的字典序（升序）排序。

**示例 1**  
**输入**  
```json
code = ["SAVE20","","PHARMA5","SAVE@20"]
businessLine = ["restaurant","grocery","pharmacy","restaurant"]
isActive = [true,true,true,true]
```
**输出**  
```json
["PHARMA5","SAVE20"]
```
**解释**：

**示例 2**  
**输入**  
```json
code = ["GROCERY15","ELECTRONICS_50","DISCOUNT10"]
businessLine = ["grocery","electronics","invalid"]
isActive = [false,true,true]
```
**输出**  
```json
["ELECTRONICS_50"]
```
**解释**：

**约束条件**  

- `n == code.length == businessLine.length == isActive.length`
- `1 <= n <= 100`
- `0 <= code[i].length, businessLine[i].length <= 100`
- `code[i]` 和 `businessLine[i]` 由可打印的 ASCII 字符组成
- `isActive[i]` 为 `true` 或 `false`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有优惠券** 挨个检查一遍，只有满足所有限制条件的才留下来，最后再按照题目要求的顺序排序。  

- **检查条件**  
  1. `isActive[i]` 必须为 `True`（相当于只挑“开着的灯”。）  
  2. `code[i]` 不能为空且只能出现字母、数字或下划线。这里可以把 `code` 看成一本字典，字典里只能有合法的单词，非法字符就像不在字典里的词，需要剔除。  
  3. `businessLine[i]` 必须是四个合法业务线之一：`"electronics"、"grocery"、"pharmacy"、"restaurant"`，相当于只接受四种颜色的球，其他颜色直接丢掉。  

- **保存合法的券**  
  把每张合法券记成 `(businessLine, code)` 这对数据，后面排序只需要看这两个字段。  

- **排序**  
  先按照业务线的固定顺序排列，再在同一业务线内部按照 `code` 的字典序（即“字母表顺序”）排列。  
  为了让电脑“懂”业务线的顺序，我们可以建一个 **优先级映射**（哈希表），比如 `{"electronics":0, "grocery":1, "pharmacy":2, "restaurant":3}`，把业务线映射成数字，数字小的排在前面。哈希表就像一本查字典，`key` 是业务线，`value` 是它的排位。

- **返回结果**  
  排序好后，只取出 `code` 部分组成结果数组返回。

这个思路之所以 **正确**，是因为我们逐条检查每一个约束，只有全部满足时才保留；排序时严格遵守了题目给出的两层次顺序。

#### 代码（Python）

```python
import re
from typing import List

def validateCoupons(code: List[str],
                    businessLine: List[str],
                    isActive: List[bool]) -> List[str]:
    """
    暴力实现：逐个过滤，然后排序返回合法的 coupon code
    """
    # 1. 合法业务线集合（像一个“白名单”）
    allowed_lines = {"electronics", "grocery", "pharmacy", "restaurant"}

    # 2. 正则表达式：只允许字母、数字、下划线
    pattern = re.compile(r'^[A-Za-z0-9_]+$')

    # 3. 收集所有合法的 (businessLine, code) 对
    valid_pairs = []                     # 用来存放 (业务线, 优惠码) 的列表
    for c, b, act in zip(code, businessLine, isActive):
        # 条件1：必须是激活状态
        if not act:
            continue
        # 条件2：code 不能为空且只能由字母/数字/下划线组成
        if not c or not pattern.fullmatch(c):
            continue
        # 条件3：业务线必须在白名单里
        if b not in allowed_lines:
            continue
        # 所有条件都满足，加入列表
        valid_pairs.append((b, c))

    # 4. 为业务线建立优先级映射（哈希表）
    priority = {"electronics": 0,
                "grocery": 1,
                "pharmacy": 2,
                "restaurant": 3}

    # 5. 按 (业务线优先级, code 字典序) 排序
    valid_pairs.sort(key=lambda x: (priority[x[0]], x[1]))

    # 6. 只返回代码部分
    return [c for _, c in valid_pairs]
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 遍历数组一次是 `O(n)`（`n` 为优惠券数量），  
  - 排序需要 `O(m log m)`，其中 `m` 是合法券的数量，最坏情况下 `m = n`，于是整体为 `O(n log n)`。  
  - 用大白话说，就是“先检查一遍，每张券花常数时间；再把合格的券排个序，排一次要花点时间，和券的数量的对数成正比”。

- **空间复杂度**：`O(m)`  
  - 需要额外存放合法券的 `(businessLine, code)` 对，最坏 `O(n)`。  
  - 其它辅助结构（哈希表、正则对象）都是常数级别。

---

### 2. 最优解

#### 思路  

暴力解已经是 **线性遍历 + 排序**，其中最大的耗时在排序环节。因为题目要求 **返回所有合法券且必须排序**，我们无法省掉排序这一步（除非使用计数排序等特殊技巧，但业务线种类只有 4 种，代码本身是字符串，无法用计数排序直接处理）。  

因此，**最优解** 与暴力解的核心思路相同，只是在实现细节上做一点点“微调”，让代码更简洁、更易读：

1. **一次遍历** 完成过滤与收集（与暴力解相同）。  
2. 使用 **`defaultdict(list)`** 按业务线分桶，先把合法券按照业务线分别放进 4 个列表。这样可以避免在排序时每次都去查哈希表的优先级，直接对每个业务线内部排序即可。  
3. 按业务线的固定顺序依次取出已排序好的子列表，拼接得到最终结果。  

这种 **分桶 + 局部排序** 的思路，仍然是 `O(n log n)`（因为每个子列表内部仍然要排序），但在常数因子上会略有提升，而且逻辑更直观：先把同类的券放在一起，再各自排好序。

#### 代码（Python）

```python
import re
from collections import defaultdict
from typing import List

def validateCoupons_opt(code: List[str],
                        businessLine: List[str],
                        isActive: List[bool]) -> List[str]:
    """
    最优实现：分桶后局部排序，保持整体 O(n log n)。
    """
    # 1. 白名单、正则
    allowed = {"electronics", "grocery", "pharmacy", "restaurant"}
    pattern = re.compile(r'^[A-Za-z0-9_]+$')

    # 2. 用 dict 按业务线分桶，value 是该业务线下所有合法的 code 列表
    buckets = defaultdict(list)   # 例如 {"grocery": ["SAVE20", ...], ...}

    for c, b, act in zip(code, businessLine, isActive):
        if act and c and pattern.fullmatch(c) and b in allowed:
            buckets[b].append(c)   # 合法则放入对应业务线的桶

    # 3. 按业务线固定顺序遍历，每个桶内部再按字典序排序
    order = ["electronics", "grocery", "pharmacy", "restaurant"]
    result = []
    for line in order:
        if line in buckets:
            # 对该业务线的优惠码进行字典序排序
            buckets[line].sort()
            result.extend(buckets[line])   # 按顺序加入最终答案

    return result
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 遍历一次 `O(n)`。  
  - 每个业务线内部排序，总体等价于对所有合法券排序，仍是 `O(m log m)`，最坏 `O(n log n)`。  
  - 与暴力解相比，常数因子更小（因为每次比较只涉及同一业务线的字符串，而不是先比较业务线再比较字符串）。

- **空间复杂度**：`O(m)`  
  - 需要额外的分桶容器存放合法券，同样是 `O(n)` 最坏情况。

---

## 心得

- **核心技巧**：**过滤 + 哈希表（或分桶） + 排序**。  
  - 过滤阶段把“不合规”的数据一次性剔除，避免后续处理浪费时间。  
  - 哈希表（字典）用来快速判断业务线是否合法、以及给业务线分配固定的优先级或桶。  
  - 排序时利用 **多键排序**（先业务线后代码），或分桶后局部排序，确保输出满足题目顺序要求。

- **适用的题型**  
  1. “按多重条件筛选并排序” 的集合类题目（如《学生成绩排序》）。  
  2. “白名单过滤 + 分组统计” 类型（如《统计不同城市的用户数量》）。  
  3. “合法性检查 + 排序输出” 的字符串处理题（如《合法用户名列表》）。

- **一句话总结**：**先把非法的先踢出去，再用哈希表给合法的分层，最后按层级顺序排好序。**  

---

## 反思

- **第一反应**：看到三个等长数组，立刻想到 `for i in range(n)` 同时遍历三者，逐条判断合法性，然后收集。  
- **最容易踩的坑**  
  - **正则写错**：忘记加 `^`、`$` 导致只匹配子串，导致 `"A#B"` 误判为合法。  
  - **业务线大小写**：题目给的是全小写，需要严格匹配，不要把 `"Electronics"` 当作合法。  
  - **空字符串**：`code[i]` 可能是 `""`，必须显式检查空值。  
  - **返回顺序**：先业务线后代码的双层排序容易写成相反顺序，导致答案不对。  

- **下次遇到同类题**：**先把过滤条件全部列出来，用集合或正则把合法范围固定，然后决定是一次排序还是分桶排序**，这样思路会更清晰。