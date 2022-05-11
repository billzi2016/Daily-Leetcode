# #1773. 计数匹配规则的物品 / Count Items Matching a Rule

> 难度：简单 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/count-items-matching-a-rule/)

---

## 题目（英文原版）

**Description**

You are given an array items, where each items[i] = [typei, colori, namei] describes the type, color, and name of the ith item. You are also given a rule represented by two strings, ruleKey and ruleValue.
The ith item is said to match the rule if one of the following is true:
Return the number of items that match the given rule.

**Examples**

**Example 1:**

```
Input: items = [["phone","blue","pixel"],["computer","silver","lenovo"],["phone","gold","iphone"]], ruleKey = "color", ruleValue = "silver"
Output: 1
Explanation: There is only one item matching the given rule, which is ["computer","silver","lenovo"].
```

**Example 2:**

```
Input: items = [["phone","blue","pixel"],["computer","silver","phone"],["phone","gold","iphone"]], ruleKey = "type", ruleValue = "phone"
Output: 2
Explanation: There are only two items matching the given rule, which are ["phone","blue","pixel"] and ["phone","gold","iphone"]. Note that the item ["computer","silver","phone"] does not match.
```

**Constraints**

- 1 <= items.length <= 104
- 1 <= typei.length, colori.length, namei.length, ruleValue.length <= 10
- ruleKey is equal to either "type", "color", or "name".
- All strings consist only of lowercase letters.

---

## 题目（中文翻译）

**题目描述**  
给定一个二维数组 `items`，其中 `items[i] = [type_i, color_i, name_i]` 分别描述第 `i` 件物品的类型（type）、颜色（color）和名称（name）。另给定两个字符串 `ruleKey` 和 `ruleValue` 表示一条规则。

第 `i` 件物品满足该规则，当且仅当以下任意条件成立：

- `ruleKey` 为 `"type"` 且 `type_i` 等于 `ruleValue`；
- `ruleKey` 为 `"color"` 且 `color_i` 等于 `ruleValue`；
- `ruleKey` 为 `"name"` 且 `name_i` 等于 `ruleValue`。

返回满足给定规则的物品数量。

**示例 1**  
```text
Input: items = [["phone","blue","pixel"],["computer","silver","lenovo"],["phone","gold","iphone"]], ruleKey = "color", ruleValue = "silver"
Output: 1
Explanation: 只有一件物品符合规则，即 ["computer","silver","lenovo"]。
```

**示例 2**  
```text
Input: items = [["phone","blue","pixel"],["computer","silver","phone"],["phone","gold","iphone"]], ruleKey = "type", ruleValue = "phone"
Output: 2
Explanation: 符合规则的物品有两件，分别是 ["phone","blue","pixel"] 和 ["phone","gold","iphone"]。注意物品 ["computer","silver","phone"] 不符合规则。
```

**约束条件**  

- `1 <= items.length <= 10^4`
- `1 <= type_i.length, color_i.length, name_i.length, ruleValue.length <= 10`
- `ruleKey` 的取值只能是 `"type"`、`"color"` 或 `"name"`。
- 所有字符串仅由小写字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
题目给出一个二维数组 `items`，每一行包含三个字符串：`type`、`color`、`name`。  
还有两个查询条件：`ruleKey`（可能是 `"type"`、`"color"` 或 `"name"`）以及对应的 `ruleValue`。  
最直接的想法就是 **把每一件商品都检查一遍**，看它的哪一列和 `ruleKey` 对应，如果该列的值恰好等于 `ruleValue`，计数器就加一。

- **用到的数据结构**：  
  - `list`（数组）——存放所有商品信息，就像超市的货架，每个格子里放着三件商品属性。  
  - `dict`（哈希表）——把 `"type"`、`"color"`、`"name"` 映射到它们在子数组中的下标（0、1、2），这一步类似查字典：把关键词（属性名）对应到页面编号（下标），查找速度是 O(1)。  

- **为什么正确**：  
  因为题目要求“统计满足条件的商品数量”，只要遍历所有商品，逐个判断是否满足规则，就一定能得到准确的计数。没有遗漏，也没有多计。

- **时间/空间复杂度**：  
  - 时间复杂度：遍历 `items` 一次，对每件商品做常数次比较（最多两次字符串相等判断），所以是 **O(n)**，其中 `n = len(items)`。这里的 `O(n)` 可以想象成“走过超市的每一排货架一次”。  
  - 空间复杂度：只用了常数级别的额外空间（一个字典和计数器），即 **O(1)**，不随商品数量增长而增长。

#### 代码（Python）  
```python
from typing import List

def countMatches(items: List[List[str]], ruleKey: str, ruleValue: str) -> int:
    # 把属性名映射到对应的下标，类似查字典：type->0, color->1, name->2
    key_to_index = {"type": 0, "color": 1, "name": 2}
    idx = key_to_index[ruleKey]          # 需要比较的列下标
    cnt = 0                              # 计数器

    for item in items:                   # 遍历每一件商品
        # 如果该列的值等于规则值，就计数
        if item[idx] == ruleValue:
            cnt += 1
    return cnt
```

#### 复杂度  
- **时间复杂度**：`O(n)` —— 线性遍历一次所有商品。  
- **空间复杂度**：`O(1)` —— 只用了固定大小的字典和计数器。

---  

### 2. 最优解  

#### 思路  
对这道 **Easy** 题目来说，暴力遍历已经是最优的时间复杂度 `O(n)`，因为我们必须检查每件商品才能确定它是否满足规则。不存在比遍历更快的办法（除非预处理多次查询，但本题只有一次查询）。  
所以最优解的核心就在于：

1. **一次映射**：把 `ruleKey` 转换为对应的下标，避免在每次循环里用 `if-elif-else` 判断属性名。这样可以把每件商品的比较次数固定为一次。  
2. **一次遍历**：直接在遍历过程中计数，不需要额外的数据结构来保存中间结果。  

下面用图示帮助理解：

```
items = [
  ["phone", "blue",  "pixel"],   # 下标 0 1 2
  ["computer","silver","lenovo"],
  ["phone","gold","iphone"]
]

ruleKey = "color"  -> 下标 1
ruleValue = "silver"
```

遍历时只看每行第 `1` 列（颜色），若等于 `"silver"`，计数器 +1。整个过程就像在超市里只挑选“颜色标签”为银色的商品。

#### 代码（Python）  
```python
from typing import List

def countMatches(items: List[List[str]], ruleKey: str, ruleValue: str) -> int:
    # 只做一次映射，避免在循环里多次判断
    key_to_index = {"type": 0, "color": 1, "name": 2}
    target_idx = key_to_index[ruleKey]

    # 使用生成式直接求和，也是一种“一遍遍历”的写法
    return sum(1 for item in items if item[target_idx] == ruleValue)
```

> 关键行解释  
> - `key_to_index[ruleKey]`：把规则的属性名转成对应列的下标。  
> - `sum(1 for item in items if ...)`：遍历 `items`，每遇到符合条件的商品就产生一个 `1`，最后把所有 `1` 加起来得到计数。

#### 复杂度  
- **时间复杂度**：`O(n)` —— 仍然是线性遍历一次所有商品。相比暴力解，只是把判断次数压到最少。  
- **空间复杂度**：`O(1)` —— 只使用了常数级别的额外空间（字典 + 计数器），生成式本身是惰性求值，不会额外占用 O(n) 空间。

---  

## 心得  

- **核心技巧**：把属性名映射到下标，再一次遍历直接比较。  
- **适用的题型**：  
  1. “根据属性过滤计数”类题目，如 *Number of Matching Subarrays*、*Number of Good Pairs*。  
  2. “一次查询的线性扫描”类题目，如 *Find the Duplicate Number*（只需要一次遍历），或 *Maximum Number of Words Found in Sentences*（逐句统计）。  
- **一句话总结**：**把文字属性转成数字索引，线性遍历一次即得答案**。  

## 反思  

- **第一反应**：看到“数组 + 规则”，第一时间想到遍历检查每一行是否满足条件。  
- **最容易踩的坑**：  
  - 把 `ruleKey` 与对应下标写错（比如把 `"color"` 当成 0）。使用字典映射可以避免。  
  - 忽略了字符串比较的大小写或空格——本题全部小写且无空格，故直接 `==`。  
  - 没考虑 `items` 为空的情况（本题约束 `items.length >= 1`，但实际写代码时仍可防御性检查）。  
- **下次遇到同类题的第一步**：先把 **查询键** 转成 **下标或直接的访问方式**，再 **一次遍历** 完成计数或收集。这样既清晰又高效。