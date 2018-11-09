# #165. 比较版本号 / Compare Version Numbers

> 难度：中等 · 标签：Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/compare-version-numbers/)

---

## 题目（英文原版）

**Description**

Given two version strings, version1 and version2, compare them. A version string consists of revisions separated by dots '.'. The value of the revision is its integer conversion ignoring leading zeros.
To compare version strings, compare their revision values in left-to-right order. If one of the version strings has fewer revisions, treat the missing revision values as 0.
Return the following:

**Examples**

**Example 1:**

```
Input: version1 = "1.2", version2 = "1.10"
Output: -1
Explanation:
version1's second revision is "2" and version2's second revision is "10": 2 < 10, so version1 < version2.
```

**Example 2:**

```
Input: version1 = "1.01", version2 = "1.001"
Output: 0
Explanation:
Ignoring leading zeroes, both "01" and "001" represent the same integer "1".
```

**Example 3:**

```
Input: version1 = "1.0", version2 = "1.0.0.0"
Output: 0
Explanation:
version1 has less revisions, which means every missing revision are treated as "0".
```

**Constraints**

- 1 <= version1.length, version2.length <= 500
- version1 and version2 only contain digits and '.'.
- version1 and version2 are valid version numbers.
- All the given revisions in version1 and version2 can be stored in a 32-bit integer.

---

## 题目（中文翻译）

给定两个版本字符串（version string），`version1` 和 `version2`，比较它们。  
一个版本字符串由用点 `'.'` 分隔的修订（revision）组成。修订的值是将其转换为整数后得到的结果，忽略前导零。  

比较版本字符串时，需要按从左到右的顺序比较它们的修订值。如果某个版本字符串的修订数量较少，则将缺失的修订值视为 `0`。  

返回如下：

示例 1  
Input: version1 = "1.2", version2 = "1.10"  
Output: -1  
Explanation:  
`version1` 的第二个修订是 `"2"`，`version2` 的第二个修订是 `"10"`：2 < 10，所以 `version1` < `version2`。

示例 2  
Input: version1 = "1.01", version2 = "1.001"  
Output: 0  
Explanation:  
忽略前导零后，`"01"` 和 `"001"` 都表示相同的整数 `1`。

示例 3  
Input: version1 = "1.0", version2 = "1.0.0.0"  
Output: 0  
Explanation:  
`version1` 的修订较少，这意味着所有缺失的修订都视为 `"0"`。

约束条件  
- 1 ≤ `version1`.length, `version2`.length ≤ 500  
- `version1` 和 `version2` 只包含数字和 `'.'`。  
- `version1` 和 `version2` 是有效的版本号。  
- 所有给定的修订在 `version1` 和 `version2` 中都可以存放在 32 位整数中。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把版本号按照 `.` 切成若干段，然后把每段当作整数比较。  
可以把 **切段** 想象成把一本书的章节标题（`1.2.3`）拆成单独的页码，  
再把每个页码（字符串）转成数字（`int`），这一步类似于在字典里查单词对应的页码——把“01”映射成整数 1，前导零自然会被丢掉。  

比较时从左到右逐段进行：
1. 取出对应位置的两个整数  
2. 若不相等，直接返回比较结果  
3. 若相等，继续比较下一段  

如果一个版本的段数比另一个少，缺失的段视为 0（相当于在短的版本后面补了若干个“0.0.0...”）。

**为什么能得到正确答案**  
- 题目要求“忽略前导零”，把每段转成整数天然满足这一点。  
- 按顺序比较每段正好对应题目“左到右比较修订号”的要求。  
- 对缺失的段补 0，等价于题目说的“把缺失的修订号当作 0”。

#### 代码（Python）

```python
def compareVersion(version1: str, version2: str) -> int:
    # 1. 把两个版本号用 '.' 分割成列表
    v1_parts = version1.split('.')
    v2_parts = version2.split('.')
    
    # 2. 取最长的段数，遍历比较
    max_len = max(len(v1_parts), len(v2_parts))
    for i in range(max_len):
        # 取第 i 段的整数，若该段不存在则视为 0
        num1 = int(v1_parts[i]) if i < len(v1_parts) else 0
        num2 = int(v2_parts[i]) if i < len(v2_parts) else 0
        
        # 3. 直接比较
        if num1 < num2:
            return -1
        if num1 > num2:
            return 1
    
    # 所有段都相等
    return 0
```

#### 复杂度  

- **时间复杂度**：`O(n)`，其中 `n` 为两个字符串的总长度。  
  解释：我们只遍历了一遍字符串（`split` 会一次性扫完），每个字符最多被处理一次。  
- **空间复杂度**：`O(n)`，因为 `split` 会把所有段存进列表，相当于额外占用了和输入等长的空间。

---

### 2. 最优解  

#### 思路  

上面的暴力解已经是 **线性时间**，但它使用了额外的列表来存所有段，空间上不是最优的。  
如果我们在比较的过程中 **边走边算**，就不需要把所有段先全部保存下来，只需要常数级的额外空间。  

**瓶颈**  
- 需要两次遍历：一次 `split`（产生列表），一次比较。  
- 列表会占用 `O(n)` 的额外空间。

**优化思路**  
使用 **双指针**（two‑pointers）在两个字符串上同步前进：

1. 设 `i`、`j` 为 `version1`、`version2` 的当前下标，初始为 0。  
2. 从当前位置向右扫描，直到遇到 `'.'` 或字符串结束，期间把字符累加成整数（`num = num * 10 + (ch - '0')`）。这一步相当于“把 `'0012'` 直接算成 12”。  
3. 同时得到 `num1`、`num2` 两个整数后立即比较。  
4. 若不相等直接返回；若相等则继续往后走，指针跳过 `'.'`（如果有的话），进入下一段。  
5. 当两个指针都走到字符串末尾时，说明所有段都相等，返回 0。  

这样我们只用了 **两个指针和两个整数变量**，空间是 `O(1)`。

**关键概念解释**  

- **双指针**：把两个手指分别放在两根绳子上，一起往前走，随时比较各自所在位置的“颜色”。  
- **按位累加整数**：把字符 `'3'`、`'4'` 依次转成 3、34、...，这跟我们平时手算多位数的过程一样。

#### 代码（Python）

```python
def compareVersion(version1: str, version2: str) -> int:
    i, j = 0, 0                # 两个指针分别指向两个版本号的当前位置
    n1, n2 = len(version1), len(version2)

    while i < n1 or j < n2:    # 任意一个还有字符未处理就继续
        # 读取 version1 的当前段，转成整数
        num1 = 0
        while i < n1 and version1[i] != '.':
            # 把字符 '0'~'9' 转成对应的数字并累加
            num1 = num1 * 10 + (ord(version1[i]) - ord('0'))
            i += 1
        # 跳过 '.'（如果有的话）
        if i < n1 and version1[i] == '.':
            i += 1

        # 同理读取 version2 的当前段
        num2 = 0
        while j < n2 and version2[j] != '.':
            num2 = num2 * 10 + (ord(version2[j]) - ord('0'))
            j += 1
        if j < n2 and version2[j] == '.':
            j += 1

        # 立刻比较两段的大小
        if num1 < num2:
            return -1
        if num1 > num2:
            return 1
        # 若相等则继续循环比较下一段

    # 所有段都相等
    return 0
```

#### 复杂度  

- **时间复杂度**：`O(n)`，`n` 为两个字符串的总长度。  
  解释：指针每次只前进一次，整个过程只遍历每个字符一次，没有额外的遍历。  
- **空间复杂度**：`O(1)`，只用了常数个变量（指针、整数），不随输入规模增长。

---

## 心得  

- **核心技巧**：双指针同步遍历字符串、按位累计得到整数、并在同一轮比较后直接返回。  
- **适用题型**：  
  1. “比较 IP 地址” (`"192.168.0.1"` vs `"192.168.0.2"`)。  
  2. “合并两个有序链表的字符串版”——把两个有序的数字段逐段合并。  
  3. “解析 CSV 行”——逐列读取并即时处理。  
- **一句话总结**：**“把每段直接算成整数再比较，指针同步前进，省空间又省事”。**

---

## 反思  

- **第一反应**：把字符串 `split` 成数组，逐段比较——最自然的想法。  
- **最容易踩的坑**：  
  - 前导零会导致字符串直接比较出错，需要转成整数。  
  - 版本号长度不一致时要记得把缺失的段当作 0 处理。  
  - 处理最后一段时如果没有 `'.'`，循环仍要能正常结束。  
- **下次遇到同类题**：第一步先思考 **“是否可以边读边算”**，如果可以，就直接用双指针避免额外的存储。