# #1410. HTML 实体解析器 / HTML Entity Parser

> 难度：中等 · 标签：Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/html-entity-parser/)

---

## 题目（英文原版）

**Description**

HTML entity parser is the parser that takes HTML code as input and replace all the entities of the special characters by the characters itself.
The special characters and their entities for HTML are:
Given the input text string to the HTML parser, you have to implement the entity parser.
Return the text after replacing the entities by the special characters.

**Examples**

**Example 1:**

```
Input: text = "&amp; is an HTML entity but &ambassador; is not."
Output: "& is an HTML entity but &ambassador; is not."
Explanation: The parser will replace the &amp; entity by &
```

**Example 2:**

```
Input: text = "and I quote: &quot;...&quot;"
Output: "and I quote: \"...\""
```

**Constraints**

- 1 <= text.length <= 105
- The string may contain any possible characters out of all the 256 ASCII characters.

---

## 题目（中文翻译）

HTML entity parser 是一种解析器，接受 HTML 代码作为输入，并将所有特殊字符的实体（entity）替换为对应的字符本身。HTML 中的特殊字符及其实体如下：

- `&quot;` → 双引号（"）
- `&apos;` → 单引号（'）
- `&amp;`  → 和号（&）
- `&gt;`   → 大于号（>）
- `&lt;`   → 小于号（<）
- `&frasl;` → 斜杠（/）

给定待解析的文本字符串 `text`，请实现实体解析器。返回将所有实体替换为相应特殊字符后的文本。

**示例 1**

```text
Input: text = "&amp; is an HTML entity but &ambassador; is not."
Output: "& is an HTML entity but &ambassador; is not."
```

**解释**：解析器会把 `&amp;` 实体替换为 `&`，而 `&ambassador;` 不是合法实体，保持不变。

**示例 2**

```text
Input: text = "and I quote: &quot;...&quot;"
Output: "and I quote: \"...\""
```

**解释**：`&quot;` 被解析为双引号 `"`。

**约束条件**

- `1 <= text.length <= 10^5`
- 输入字符串可能包含所有 256 个 ASCII 字符中的任意字符。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

1. **从左到右逐字符遍历**  
   - 把字符串看成一串字符的队列，像阅读一本书一样，从第一个字符读到最后一个字符。  
2. **遇到字符 `'&'` 时尝试匹配实体**  
   - HTML 实体都有固定的写法，例如 `&amp;`、`&lt;`、`&gt;`、`&quot;`、`&apos;`。  
   - 把 `'&'` 当成“起点”，往后看最多 6 个字符（最长的实体是 `&quot;`，长度 6），看看这段子串是否正好等于上面任意一个实体。  
   - 如果匹配成功，就把对应的普通字符（`&`、`<`、`>`、`"`、`'`）写入答案；否则把原始的 `'&'` 原样写入。  

> **类比**：  
> - 哈希表就像一本字典，`key` 是单词，`value` 是对应的解释。这里我们把实体当作 `key`，对应的普通字符当作 `value`，用字典来“一键查找”。  

3. **构造结果**  
   - 为了避免频繁的字符串拼接（每次拼接都会产生新字符串，代价大），我们使用一个列表 `res`，把每一步得到的字符 `append` 进去，最后 `''.join(res)` 合成答案。  

**为什么这个方法一定能得到正确答案**  
- 每次只要找到一个合法的实体，就一定把它替换成唯一对应的字符；如果没有找到合法实体，就保持原样。  
- 由于遍历顺序不跳过字符（只会在匹配成功时一次性跳过整个实体），所有字符都会被检查一次，确保没有遗漏。  

**时间/空间分析（大白话）**  
- **时间复杂度**：我们最多遍历一次输入字符串（长度记作 `n`），在每个 `'&'` 处最多检查 6 次子串是否相等（常数时间），所以总体是 `O(n)`。  
- **空间复杂度**：需要额外的列表保存答案，长度同样是 `n`，所以是 `O(n)` 的额外空间。  

#### 代码（Python）  

```python
def entityParser(text: str) -> str:
    # 1. 把所有合法实体和对应的字符放进字典，像查字典一样使用
    entity_map = {
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&quot;": "\"",
        "&apos;": "'",
    }

    n = len(text)
    i = 0                 # 当前扫描到的位置
    res = []              # 用列表收集结果字符，最后一次性合并

    while i < n:
        # 只要看到 '&'，就尝试匹配最长 6 个字符（&quot; 长度是 6）
        if text[i] == '&':
            matched = False
            # 检查所有可能的实体（这里枚举字典的键即可）
            for ent, ch in entity_map.items():
                L = len(ent)
                # 判断从 i 开始的子串是否等于当前实体
                if i + L <= n and text[i:i+L] == ent:
                    res.append(ch)   # 找到匹配，写入对应字符
                    i += L           # 跳过整个实体
                    matched = True
                    break
            if not matched:          # 没有匹配到任何实体，原样输出 '&'
                res.append('&')
                i += 1
        else:
            # 普通字符直接加入结果
            res.append(text[i])
            i += 1

    return ''.join(res)
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次字符串，常数次的子串比较不影响整体量级。  
- **空间复杂度**：`O(n)` —— 需要额外的列表保存转换后的字符。  

---  

### 2. 最优解  

#### 思路  

从暴力解我们已经看到，**瓶颈**并不在时间（已经是线性），而在**实现的简洁度和可读性**。  
我们可以进一步把“遍历所有实体并逐个比较”这一步抽象成一次**哈希表查找**，把实体作为键、对应字符作为值，直接一次 `O(1)` 的查找完成匹配。  

**优化步骤**  

1. **预先建立哈希表**（字典）  
   - `entity_map = {"&amp;": "&", "&lt;": "<", ...}`。  
   - 以后只要拿到一个子串，就能在 `O(1)` 时间内判断它是否是合法实体。  

2. **一次遍历**  
   - 同样从左到右扫描。  
   - 当看到 `'&'` 时，尝试把后面的字符往后取（最多取到下一个 `';'` 为止），形成候选子串 `cand = text[i:j+1]`。  
   - 检查 `cand` 是否在哈希表中：  
     - 若在 → 用哈希表得到的普通字符替换，`i = j + 1`（跳过整个实体）。  
     - 若不在 → 把当前字符 `'&'` 原样写入，`i += 1`。  

3. **为什么只取到 `';'`**  
   - 所有合法实体都以分号 `';'` 结束，且长度不会超过 6。  
   - 如果在 `'&'` 之后找不到 `';'`（或 `';'` 超过了最大长度），一定不是合法实体，直接原样输出 `'&'`。  

**核心概念解释**  

- **哈希表（字典）**：像一本“快捷查找的字典”，把实体（key）映射到普通字符（value），查询只需要一次“看页码”。  
- **前缀扫描**：从左到右一次扫过，每次只决定当前字符应该怎么写，保证不需要回头。  

**时间/空间对比**  

- **时间**：仍是 `O(n)`，但每次匹配只做一次哈希查找，代码更简洁。  
- **空间**：额外的哈希表占 `O(1)`（实体种类固定），答案列表仍是 `O(n)`。  

#### 代码（Python）  

```python
def entityParser(text: str) -> str:
    # 1. 哈希表：实体 -> 对应字符
    entity_map = {
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&quot;": "\"",
        "&apos;": "'",
    }

    n = len(text)
    i = 0
    res = []

    while i < n:
        if text[i] == '&':
            # 2. 尝试在后面找一个 ';'，但最多只往后找 6 个字符
            j = i + 1
            while j < n and j - i <= 6 and text[j] != ';':
                j += 1

            # 如果找到了分号且长度在合法范围内，形成候选实体
            if j < n and text[j] == ';' and (j - i + 1) <= 6:
                cand = text[i:j+1]          # 包含 '&' 和 ';' 的子串
                if cand in entity_map:      # 哈希表 O(1) 判断
                    res.append(entity_map[cand])
                    i = j + 1               # 跳过整个实体
                    continue                # 直接进入下一轮循环
            # 3. 没有匹配成功，按原字符输出 '&'
            res.append('&')
            i += 1
        else:
            # 普通字符直接加入结果
            res.append(text[i])
            i += 1

    return ''.join(res)
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次字符串，查表是常数时间。  
- **空间复杂度**：`O(n)`（答案列表） + `O(1)`（哈希表），总体仍是线性额外空间。  

---  

## 心得  

- **核心技巧**：利用哈希表（字典）把固定的“实体 → 字符”映射起来，配合一次线性扫描完成替换。  
- **适用场景**：  
  1. **字符映射替换**：如 LeetCode “Decode String” 中的字母到数字映射。  
  2. **词法分析**：编译器/解释器里把关键字、符号转换成 token。  
  3. **文本清洗**：把常见的转义序列（如 `\n`、`\t`）转回真实字符。  
- **一句话总结**：**把所有“查找‑替换”规则预先放进字典，遍历一次字符串，遇到起始标记就一次哈希查表即可**。  

## 反思  

- **第一反应**：看到 `&`、`;`，立刻想到“这是一段可能的实体”，于是想到逐个检查。  
- **最容易踩的坑**：  
  - **忘记判断分号是否真的出现**，导致把类似 `&abc`（没有 `;`）误当成实体。  
  - **实体长度不固定**，如果硬写固定长度（如只检查 4 位），会漏掉 `&quot;`。  
  - **字符转义**：在 Python 字符串里写 `"` 必须用 `\"`，不然会报语法错误。  
- **下次遇到同类题**：第一步先**列出所有合法模式**，把它们放进哈希表；第二步**一次线性扫描**，在出现起始标记时**尝试最短/最长匹配**并查表决定是否替换。