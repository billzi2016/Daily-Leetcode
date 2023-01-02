# #2075. 解码倾斜密码 / Decode the Slanted Ciphertext

> 难度：中等 · 标签：String、Simulation · [LeetCode 链接](https://leetcode.com/problems/decode-the-slanted-ciphertext/)

---

## 题目（英文原版）

**Description**

A string originalText is encoded using a slanted transposition cipher to a string encodedText with the help of a matrix having a fixed number of rows rows.
originalText is placed first in a top-left to bottom-right manner.
The blue cells are filled first, followed by the red cells, then the yellow cells, and so on, until we reach the end of originalText. The arrow indicates the order in which the cells are filled. All empty cells are filled with ' '. The number of columns is chosen such that the rightmost column will not be empty after filling in originalText.
encodedText is then formed by appending all characters of the matrix in a row-wise fashion.
The characters in the blue cells are appended first to encodedText, then the red cells, and so on, and finally the yellow cells. The arrow indicates the order in which the cells are accessed.
For example, if originalText = "cipher" and rows = 3, then we encode it in the following manner:
The blue arrows depict how originalText is placed in the matrix, and the red arrows denote the order in which encodedText is formed. In the above example, encodedText = "ch ie pr".
Given the encoded string encodedText and number of rows rows, return the original string originalText.
Note: originalText does not have any trailing spaces ' '. The test cases are generated such that there is only one possible originalText.

**Examples**

**Example 1:**

```
Input: encodedText = "ch   ie   pr", rows = 3
Output: "cipher"
Explanation: This is the same example described in the problem description.
```

**Example 2:**

```
Input: encodedText = "iveo    eed   l te   olc", rows = 4
Output: "i love leetcode"
Explanation: The figure above denotes the matrix that was used to encode originalText. 
The blue arrows show how we can find originalText from encodedText.
```

**Example 3:**

```
Input: encodedText = "coding", rows = 1
Output: "coding"
Explanation: Since there is only 1 row, both originalText and encodedText are the same.
```

**Constraints**

- 0 <= encodedText.length <= 106
- encodedText consists of lowercase English letters and ' ' only.
- encodedText is a valid encoding of some originalText that does not have trailing spaces.
- 1 <= rows <= 1000
- The testcases are generated such that there is only one possible originalText.

---

## 题目（中文翻译）

**描述**  
给定一个固定行数 `rows` 的矩阵，原始字符串 `originalText` 通过倾斜置换密码（slanted transposition cipher）被编码为 `encodedText`。  
编码过程如下：

1. 将 `originalText` 按左上角到右下角的斜向顺序依次填入矩阵。  
2. 填充顺序先填蓝色单元格，再填红色单元格，随后是黄色单元格，依此类推，直至 `originalText` 的所有字符都被写入。箭头指示了填充的顺序。所有未被填充的单元格用空格字符 `' '` 填满。列数的选择保证在填完 `originalText` 后最右侧的列不为空。  
3. 形成 `encodedText`：按行顺序遍历矩阵，将矩阵中的字符逐行拼接得到 `encodedText`。读取顺序先读取蓝色单元格，再读取红色单元格，随后是黄色单元格，依此类推，直至所有单元格均被访问。箭头指示了读取的顺序。

示例：`originalText = "cipher"`、`rows = 3` 时的编码过程如下图所示（蓝色箭头表示填充顺序，红色箭头表示读取顺序），得到 `encodedText = "ch ie pr"`。

现在已知 `encodedText` 与行数 `rows`，请返回对应的 `originalText`。  
**注意**：`originalText` 不含任何尾部空格 `' '`，且测试数据保证唯一的合法解。

---

### 示例

**示例 1**  
```
Input: encodedText = "ch   ie   pr", rows = 3
Output: "cipher"
Explanation: 这正是题目描述中的示例。
```

**示例 2**  
```
Input: encodedText = "iveo    eed   l te   olc", rows = 4
Output: "i love leetcode"
Explanation: 上图展示了用于编码 `originalText` 的矩阵。蓝色箭头指示了如何从 `encodedText` 还原出 `originalText`。
```

**示例 3**  
```
Input: encodedText = "coding", rows = 1
Output: "coding"
Explanation: 只有一行时，`originalText` 与 `encodedText` 完全相同。
```

### 约束条件
- `0 <= encodedText.length <= 10^6`
- `encodedText` 只包含小写英文字母和空格字符 `' '`。
- `encodedText` 是某个不含尾部空格的合法 `originalText` 的编码结果。
- `1 <= rows <= 1000`
- 测试用例保证唯一的合法 `originalText`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

我们已经知道 **rows**（行数），但不知道矩阵到底有多少列。  
最直接的想法是 **把所有可能的列数都枚举一遍**，  
对每一种列数：

1. 按照题目描述把 `encodedText` 按行填进矩阵（空格也算字符）。  
2. 再按照“左上 → 右下”的斜线顺序把矩阵里的字符读出来，得到一个候选的 `originalText`。  
3. 把得到的字符串去掉结尾的空格后，检查它 **重新编码** 是否会得到原来的 `encodedText`。  
   - 如果相等，就说明找到了唯一的答案。

> **类比**：把矩阵的列数想象成一把钥匙的齿数。我们不断尝试不同的钥匙，只有一把能打开（匹配）编码的锁。

**为什么能保证正确？**  
因为题目已经说明：  
- `encodedText` 的长度一定是 `rows × cols`（没有多余字符），  
- 并且只会有 **唯一** 一个合法的 `originalText`。  
所以只要遍历所有可能的 `cols`（即 `1 … len(encodedText)`），一定能找到那把唯一的钥匙。

**时间/空间分析**  

- 枚举列数的次数最多是 `len(encodedText)`，记作 `n`。  
- 对每一种列数我们都要 **完整地遍历矩阵一次**（填表 + 斜线读取），时间是 `O(n)`。  
- 所以总时间复杂度是 **`O(n²)`**。  
  - `O(n²)` 可以理解为：如果 `n = 1000`，我们大约要做 1 000 000 次基本操作，随着 `n` 增大，工作量会呈二次方增长，稍微大一点就会变慢。  
- 需要额外的矩阵空间 `rows × cols = n`，空间复杂度是 **`O(n)`**。

> 对于本题的约束（`n ≤ 10⁶`），`O(n²)` 已经会超时，所以需要进一步优化。

#### 代码（Python）

```python
def decode_bruteforce(encodedText: str, rows: int) -> str:
    n = len(encodedText)                # 总字符数
    # 枚举所有可能的列数
    for cols in range(1, n + 1):
        if rows * cols != n:            # 必须恰好填满矩阵
            continue

        # 1️⃣ 按行填入矩阵（包括空格）
        matrix = [list(encodedText[i*cols:(i+1)*cols]) for i in range(rows)]

        # 2️⃣ 按斜线顺序读取，得到 candidate
        cand = []
        # 先从第一行的每一列开始
        for start_c in range(cols):
            r, c = 0, start_c
            while r < rows and c >= 0:
                cand.append(matrix[r][c])
                r += 1
                c -= 1
        # 再从第二行的最右列开始（避免重复第一行的 (0, cols-1)）
        for start_r in range(1, rows):
            r, c = start_r, cols - 1
            while r < rows and c >= 0:
                cand.append(matrix[r][c])
                r += 1
                c -= 1

        # 3️⃣ 去掉末尾的空格，得到可能的 originalText
        original = ''.join(cand).rstrip(' ')

        # 4️⃣ 检查：如果把 original 再次编码会得到原来的 encodedText，说明找到了
        if encode(original, rows) == encodedText:   # encode 为题目给出的编码过程（这里不展开实现）
            return original

    return ""   # 按题目保证不会走到这里
```

> 关键行都有中文注释，帮助初学者快速定位思路。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 这里的 `n` 是 `encodedText` 的长度。遍历所有列数（最多 `n` 次），每次都要遍历整个矩阵（`O(n)`），于是乘起来得到二次方。  
- **空间复杂度**：`O(n)`  
  - 需要存放 `rows × cols = n` 个字符的矩阵。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，真正的瓶颈在 **枚举列数** 这一步。  
实际上，列数根本不需要枚举——我们可以直接算出来！

> **关键观察**  
> 编码过程是：  
> 1. 把原文按斜线（左上 → 右下）填进矩阵。  
> 2. 再把矩阵 **逐行**（左到右、上到下）读出，得到 `encodedText`。  
> 因此，`encodedText` 的长度必然等于 `rows × cols`，而 `cols` 必然是 **整数**。  
> 所以只要把 `len(encodedText)` 除以 `rows`，就能得到唯一的 `cols`：

```
cols = len(encodedText) // rows
```

> 这里的 “//” 表示整数除法，保证得到的是整数列数。  
> 题目已经保证 `encodedText` 的长度一定可以被 `rows` 整除。

有了 `cols`，我们只需要把 `encodedText` **按行** 填回矩阵，然后按照 **斜线顺序** 读取一次即可得到原文。整个过程只遍历一次字符串，时间线性。

**斜线遍历的实现细节**（对初学者友好）：

- 先固定起点在 **第一行**，从左到右依次把每一列当作斜线的起点。  
- 对每个起点 `(0, c)`，沿着左下方向走：`(r+1, c-1)`，直到走出矩阵边界。  
- 接下来把起点移动到 **最后一列**，从第二行开始向下（因为第一行已经处理过），同样沿左下方向走。  

这样可以覆盖矩阵中所有的对角线，且顺序正好是题目中 “左上 → 右下” 的填充顺序。

> **类比**：把矩阵想象成一块棋盘，斜线遍历就像走“象棋的象”，每次从棋盘的最左上角或最右下角的边缘开始，沿着左下方向一步步跳。

#### 代码（Python）

```python
def decodeSlantedCiphertext(encodedText: str, rows: int) -> str:
    """
    把 encodedText 按题目描述解码成原始文字。
    思路：
    1. 计算列数 cols = len(encodedText) // rows。
    2. 按行把 encodedText 填进矩阵（空格也算字符）。
    3. 按斜线（左上 → 右下）顺序读取矩阵，得到原文并去掉末尾空格。
    """
    if rows == 0:                     # 防止除以 0（题目保证 rows ≥ 1）
        return ""

    n = len(encodedText)
    cols = n // rows                  # 直接算出列数

    # 1️⃣ 按行切割得到矩阵，每行是一个列表，便于后续索引
    matrix = [list(encodedText[i*cols:(i+1)*cols]) for i in range(rows)]

    # 2️⃣ 按斜线顺序读取
    original_chars = []

    #   (a) 先从第一行的每一列开始（列号从 0 到 cols-1）
    for start_c in range(cols):
        r, c = 0, start_c
        while r < rows and c >= 0:
            original_chars.append(matrix[r][c])
            r += 1
            c -= 1

    #   (b) 再从第二行的最右列开始（行号从 1 到 rows-1）
    for start_r in range(1, rows):
        r, c = start_r, cols - 1
        while r < rows and c >= 0:
            original_chars.append(matrix[r][c])
            r += 1
            c -= 1

    # 3️⃣ 合并成字符串并去掉尾部的空格（题目保证原文没有尾随空格）
    original = ''.join(original_chars).rstrip(' ')
    return original
```

**关键行解释**（中文注释已写在代码里）：

- `cols = n // rows`：一次算出列数，不需要枚举。  
- `matrix = [...]`：把一维的 `encodedText` 按行切割成二维结构，后面访问更直观。  
- 两个 `while` 循环实现 **斜线遍历**，分别处理“上边界起点”和“右边界起点”。  
- `rstrip(' ')`：去掉原文末尾可能出现的填充空格。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - `n = len(encodedText)`。我们只遍历一次字符串来构造矩阵，随后再遍历一次矩阵的所有格子（总数仍是 `n`），没有额外的嵌套循环。  
  - 与暴力解的 `O(n²)` 相比，**线性** 的增长速度在数据量大时快得多。  
- **空间复杂度**：`O(n)`  
  - 需要保存矩阵本身（`rows × cols = n`），以及最终的字符列表。  
  - 这已经是最小必要的空间，因为题目本身要求我们“看到”每个字符一次。

---

## 心得

- **核心技巧**：**利用行数直接算出列数**，再用**斜线（对角线）遍历**恢复原文。  
- **适用的题型**  
  1. “斜向/对角线”填充或读取的矩阵题（如 LeetCode 1324 – *Print Words Vertically* 的变体）。  
  2. 需要根据已知行数/列数恢复二维结构的题目（如 “Z 字形变换”）。  
- **一句话总结**：**先把一维字符串恢复成矩阵，再按题目指定的斜线顺序读取**，这就是解码的钥匙。

---

## 反思

- **第一反应**：看到 “rows” 与 “encodedText”，本能想 **枚举列数**，因为列数在题面上没有直接给出。  
- **最容易踩的坑**  
  1. **列数计算错误**：忘记 `len(encodedText)` 必须整除 `rows`，直接使用浮点除会导致索引越界。  
  2. **斜线遍历顺序**写反了——先遍历上边界再遍历右边界，否则会漏掉或重复读取某些格子。  
  3. **末尾空格**：原文不应该有尾随空格，需要在最终结果上 `rstrip(' ')`。  
- **下次类似题目**：看到 “把字符串放进矩阵 → 按某种顺序读取” 时，**先把行/列数算出来**（通常是长度除以已知维度），**再用对应的遍历方式**（行、列、对角线、螺旋等）恢复原始顺序。这样可以避免暴力枚举，直接得到线性解法。