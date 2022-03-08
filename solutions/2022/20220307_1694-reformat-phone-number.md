# #1694. 重新格式化电话号码 / Reformat Phone Number

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/reformat-phone-number/)

---

## 题目（英文原版）

**Description**

You are given a phone number as a string number. number consists of digits, spaces ' ', and/or dashes '-'.
You would like to reformat the phone number in a certain manner. Firstly, remove all spaces and dashes. Then, group the digits from left to right into blocks of length 3 until there are 4 or fewer digits. The final digits are then grouped as follows:
The blocks are then joined by dashes. Notice that the reformatting process should never produce any blocks of length 1 and produce at most two blocks of length 2.
Return the phone number after formatting.

**Examples**

**Example 1:**

```
Input: number = "1-23-45 6"
Output: "123-456"
Explanation: The digits are "123456".
Step 1: There are more than 4 digits, so group the next 3 digits. The 1st block is "123".
Step 2: There are 3 digits remaining, so put them in a single block of length 3. The 2nd block is "456".
Joining the blocks gives "123-456".
```

**Example 2:**

```
Input: number = "123 4-567"
Output: "123-45-67"
Explanation: The digits are "1234567".
Step 1: There are more than 4 digits, so group the next 3 digits. The 1st block is "123".
Step 2: There are 4 digits left, so split them into two blocks of length 2. The blocks are "45" and "67".
Joining the blocks gives "123-45-67".
```

**Example 3:**

```
Input: number = "123 4-5678"
Output: "123-456-78"
Explanation: The digits are "12345678".
Step 1: The 1st block is "123".
Step 2: The 2nd block is "456".
Step 3: There are 2 digits left, so put them in a single block of length 2. The 3rd block is "78".
Joining the blocks gives "123-456-78".
```

**Constraints**

- 2 <= number.length <= 100
- number consists of digits and the characters '-' and ' '.
- There are at least two digits in number.

---

## 题目（中文翻译）

**题目描述**  
给定一个字符串 `number` 表示电话号码。`number` 只包含数字、空格 `' '` 和连字符 `'-'`。请按照以下规则重新格式化该电话号码：

1. 先移除所有空格和连字符。  
2. 从左到右依次将剩余的数字划分为长度为 3 的块（block），直到剩余的数字不超过 4 位。  
3. 对于最后剩余的数字，按照以下方式分块：  
   - 若恰好 4 位，则划分为两个长度为 2 的块。  
   - 否则直接形成一个长度为 2 或 3 的块。  

4. 最终用连字符 `'-'` 将所有块连接起来。  
   注意，重新格式化的过程中**不会出现长度为 1 的块**，且**至多出现两个长度为 2 的块**。

返回格式化后的电话号码。

**示例**

> 示例 1  
> 输入: `number = "1-23-45 6"`  
> 输出: `"123-456"`  
> 解释:  
> - 去除空格和连字符后得到数字串 `"123456"`。  
> - 步骤 1: 剩余数字超过 4 位，取前 3 位形成块 `"123"`。  
> - 步骤 2: 剩余 3 位，直接形成块 `"456"`。  
> - 用 `'-'` 连接块得到 `"123-456"`。

> 示例 2  
> 输入: `number = "123 4-567"`  
> 输出: `"123-45-67"`  
> 解释:  
> - 去除空格和连字符后得到 `"1234567"`。  
> - 步骤 1: 取前 3 位形成块 `"123"`。  
> - 步骤 2: 剩余 4 位，划分为两个长度为 2 的块 `"45"` 和 `"67"`。  
> - 用 `'-'` 连接块得到 `"123-45-67"`。

> 示例 3  
> 输入: `number = "123 4-5678"`  
> 输出: `"123-456-78"`  
> 解释:  
> - 去除空格和连字符后得到 `"12345678"`。  
> - 步骤 1: 第一个块为 `"123"`。  
> - 步骤 2: 第二个块为 `"456"`。  
> - 步骤 3: 剩余 2 位形成块 `"78"`。  
> - 用 `'-'` 连接块得到 `"123-456-78"`。

**约束条件**
- `2 <= number.length <= 100`
- `number` 只包含数字、字符 `'-'` 和空格 `' '`。
- `number` 中至少包含两位数字。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法可以分成两步：

1. **先把所有无关字符去掉**  
   原字符串里既有数字，又有空格 `' '`，还有短横线 `'-'`。我们只需要留下数字，其他的都像是“脏东西”。把它们全部删掉后，就得到一串纯数字。这个过程可以把字符串想象成一本书，**哈希表**就像查字典一样：我们只关心“数字”这个词，其他词（空格、短横线）直接忽略。

2. **按照题目要求把数字分块**  
   - 当剩余的数字长度 > 4 时，取最左边的 3 位，形成一个块；
   - 当剩余的数字长度 ≤ 4 时，根据下面的规则结束：  
     - 长度为 4 → 分成两个长度为 2 的块；  
     - 长度为 3 → 直接作为一个块；  
     - 长度为 2 → 直接作为一个块。  
   最后把所有块用 `'-'` 连接起来即可。

> **为什么一定对？**  
> 题目规定的“从左到右、每次尽可能取 3 位，除非只剩 4 位或更少”正好对应了上面的分块规则。只要我们严格遵循这个顺序，最终得到的格式必然满足“不出现长度为 1 的块，且最多出现两个长度为 2 的块”。

**复杂度的“大白话”解释**  
- `O(n)` 表示“随着输入长度 n 增大，程序的运行时间大约会线性增长”。比如 n 从 10 增加到 20，时间大约翻倍。  
- `O(1)` 表示“占用的空间是固定的，不随 n 变化”。  

#### 代码（Python）

```python
def reformatNumber(number: str) -> str:
    # 1️⃣ 过滤掉空格和短横线，只保留数字
    digits = []
    for ch in number:
        if ch.isdigit():          # ch.isdigit() 类似“字典查询”，只要是数字就留下
            digits.append(ch)
    # 此时 digits 是一个只包含数字的列表，长度为 n

    # 2️⃣ 按规则分块
    groups = []                   # 用来保存每一个块
    i = 0                         # i 指向当前未处理的数字位置
    n = len(digits)

    while n - i > 4:              # 只要剩余的数字 > 4，就取 3 位
        groups.append(''.join(digits[i:i+3]))
        i += 3

    # 处理剩下的 2~4 位
    remain = n - i
    if remain == 4:               # 4 位要拆成 2+2
        groups.append(''.join(digits[i:i+2]))
        groups.append(''.join(digits[i+2:i+4]))
    else:                         # 2、3 位直接拼成一个块
        groups.append(''.join(digits[i:]))

    # 3️⃣ 用 '-' 连接所有块
    return '-'.join(groups)
```

#### 复杂度

- **时间复杂度：`O(n)`**  
  代码只遍历了原字符串一次（过滤），再遍历了一遍过滤后的数字列表（分块），所以总的操作次数与字符数 n 成正比。

- **空间复杂度：`O(n)`**  
  需要额外的列表 `digits` 保存所有数字，最坏情况下占用和原字符串相同的空间。

---

### 2. 最优解

#### 思路  
暴力解已经是线性时间 `O(n)`，但它用了两次遍历：一次过滤，一次分块。我们可以 **把这两件事合并到一次遍历里**，在读取字符的同时直接决定它属于哪个块。这种“一遍完成” 的技巧在处理大数据时可以显著降低常数因子。

关键点：

1. **一次遍历完成清洗和分块**  
   - 用一个临时字符串 `cur` 收集当前块的数字；
   - 当 `cur` 长度达到 3 且剩余未处理的字符仍然 > 4 时，立即把 `cur` 加入结果列表并清空 `cur`；
   - 当遍历结束后，剩余的 `cur` 长度一定是 2、3 或 4（因为我们在满足 “>4 且已经取了 3 位” 时就已经提前切块），这时只需要再做一次简单的拆分。

2. **只使用一个列表存放最终块**  
   这样可以避免在中间保存完整的 `digits` 列表，节省了额外的空间。

> **类比**：想象你在排队买票，原本先把所有人筛选出符合条件（过滤），再分成若干小组排队（分块）。最优解相当于在筛选的同时直接把符合条件的人安排进小组，省掉了先把全部人放在一边再重新排队的过程。

#### 代码（Python）

```python
def reformatNumber(number: str) -> str:
    res = []          # 最终块列表
    cur = []          # 正在构造的块（最多放 3 位）

    # 一次遍历：过滤 + 分块
    for ch in number:
        if not ch.isdigit():      # 跳过空格和短横线
            continue
        cur.append(ch)            # 把当前数字加入正在构造的块

        # 当块已经满 3 位，并且后面还有 >4 位未处理时，立即收尾
        # 这里用 len(res) 与 cur 的组合来间接判断“后面还有多少未处理的数字”
        # 为了简化实现，仍然在遍历结束后统一处理剩余部分
        if len(cur) == 3:
            # 先把块放进去，后面再根据剩余长度决定是否需要重新拆分
            res.append(''.join(cur))
            cur = []               # 清空当前块，准备收集下一个块

    # 此时 cur 中可能剩余 0~3 位数字，且 res 已经可能包含若干 3 位块
    # 需要根据剩余长度进行最后的整理
    if cur:
        # 如果已经有块且最后的块长度为 1，说明之前的切分不够好，需要把
        # 前一个 3 位块拆成 2+2（因为只能出现至多两个长度为 2 的块）
        if len(cur) == 1 and res and len(res[-1]) == 3:
            # 把倒数第二块的最后一个字符移动到 cur 前面，形成 2+2
            last = list(res.pop())   # 把原来的 3 位块弹出
            res.append(''.join(last[:2]))  # 前两个字符成块
            cur = [last[2]] + cur          # 把剩下的 1 位放到 cur 前面

        # 现在 cur 的长度只能是 2、3 或 4（4 的情况只会在这里出现）
        if len(cur) == 4:
            res.append(''.join(cur[:2]))
            res.append(''.join(cur[2:]))
        else:
            res.append(''.join(cur))

    return '-'.join(res)
```

> **代码说明**  
> - `cur` 类似“正在装箱的货物”，当装满 3 件时就立即封箱（`res.append`）。  
> - 若遍历结束后出现了只剩 1 位的情况，需要把前一个已经封好的 3 位箱子拆开，保证不会出现长度为 1 的块。  
> - 最终用 `'-'.join` 把所有块连起来。

#### 复杂度

- **时间复杂度：`O(n)`**  
  只遍历一次原字符串，所有操作（判断、追加、弹出）都是常数时间。

- **空间复杂度：`O(n)`**  
  需要存放最终的块列表 `res`，其总字符数仍然是原数字的数量 `n`（不计入输出字符串本身）。

> 与暴力解相比，**时间常数更小**（只遍历一次），**空间占用略低**（没有额外的 `digits` 列表），在极端长度（100）下差别不大，但思路更贴近“一次完成”的优化原则。

---

## 心得

- **核心技巧**：一次遍历完成过滤与分块，必要时对已经生成的块进行局部调整（把 3 位块拆成 2+2），避免出现非法的长度 1 块。  
- **适用的题型**：  
  1. 需要先“清洗”输入再“分段”输出的字符串处理题（如 “License Key Formatting”）。  
  2. 需要在遍历中动态决定分割点的分组问题（如 “Group the People Given the Group Size They Belong To”）。  
- **解题钥匙**：**“边读边决定”**——在读取字符的同时即时判断是否可以形成一个合法块，而不是先全部读完再后处理。

---

## 反思

- **第一反应**：把所有非数字字符删掉，再用 `while` 循环按规则切块。  
- **最容易踩的坑**：  
  - 处理剩余 4 位数字时忘记拆成两个 2 位块，导致出现长度为 1 的块。  
  - 当最后只剩 1 位时，没有把前面的 3 位块拆开，违反题目“永不出现长度为 1 的块”。  
- **下次第一步**：**先确定“过滤 + 直接分块”是否能一次完成**，如果不能，再考虑后处理或局部调整。这样可以快速定位是否需要额外的“拆块”步骤。