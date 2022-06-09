# #1812. **确定棋盘格子的颜色** / Determine Color of a Chessboard Square

> 难度：简单 · 标签：Math、String · [LeetCode 链接](https://leetcode.com/problems/determine-color-of-a-chessboard-square/)

---

## 题目（英文原版）

**Description**

You are given coordinates, a string that represents the coordinates of a square of the chessboard. Below is a chessboard for your reference.
Return true if the square is white, and false if the square is black.
The coordinate will always represent a valid chessboard square. The coordinate will always have the letter first, and the number second.

**Examples**

**Example 1:**

```
Input: coordinates = "a1"
Output: false
Explanation: From the chessboard above, the square with coordinates "a1" is black, so return false.
```

**Example 2:**

```
Input: coordinates = "h3"
Output: true
Explanation: From the chessboard above, the square with coordinates "h3" is white, so return true.
```

**Example 3:**

```
Input: coordinates = "c7"
Output: false
```

**Constraints**

- coordinates.length == 2
- 'a' <= coordinates[0] <= 'h'
- '1' <= coordinates[1] <= '8'

---

## 题目（中文翻译）

给定一个字符串 `coordinates`，表示国际象棋棋盘上某格的坐标（如 `a1`、`h3`）。下面是一副棋盘示意图供参考。  
如果该格子是白色（white），返回 `true`；如果是黑色（black），返回 `false`。  
坐标一定合法，且始终以字母在前、数字在后。

**示例 1**  
**示例 2**  
**示例 3**

**示例：**

- 示例 1  
  **输入**: `coordinates = "a1"`  
  **输出**: `false`  
  **解释**: 从上图可知，坐标为 `"a1"` 的格子是黑色（black），因此返回 `false`。

- 示例 2  
  **输入**: `coordinates = "h3"`  
  **输出**: `true`  
  **解释**: 从上图可知，坐标为 `"h3"` 的格子是白色（white），因此返回 `true`。

- 示例 3  
  **输入**: `coordinates = "c7"`  
  **输出**: `false`  
  **解释**: 坐标为 `"c7"` 的格子为黑色（black），返回 `false`。

**约束条件**  
- `coordinates.length == 2`  
- `'a' <= coordinates[0] <= 'h'`  
- `'1' <= coordinates[1] <= '8'`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把整个棋盘画出来，记住每个格子的颜色，然后把输入的坐标在棋盘里找一找，直接返回对应的颜色。

- **数据结构**：我们可以用一个二维列表（list of list）来模拟棋盘。  
  - 把 `0` 代表黑格，`1` 代表白格。  
  - 这个二维列表就像一本“查字典”，行号（数字）是字典的页码，列号（字母）是词条，查到的值就是颜色。

- **为什么正确**：棋盘的颜色是固定的，只要把它完整地写进程序里，查询时一定能得到正确答案。

- **时间/空间复杂度**：  
  - **时间**：我们需要遍历整张 8×8 的棋盘一次来把颜色填好，随后再一次遍历找到目标格子。遍历 64 格子，用大白话说就是“做了 64 次相同的操作”，记作 **O(64)**，在渐进记号里写成 **O(1)**（因为 64 是常数）。  
  - **空间**：需要保存整个棋盘的 64 个格子，用 **O(64)** 的额外空间，同样记作 **O(1)**（常数空间）。

> 注：虽然在渐进分析里我们把常数忽略，称为 O(1)，但从“实际执行了多少步”角度看，暴力解确实要走 64 步，比最优解要多。

#### 代码（Python）

```python
def square_is_white_bruteforce(coordinates: str) -> bool:
    """
    暴力解法：先生成完整的 8×8 棋盘，再查表返回颜色。
    返回 True 表示白格，False 表示黑格。
    """
    # 1. 建立 8×8 的棋盘，0 为黑，1 为白
    board = [[0] * 8 for _ in range(8)]      # 先全填成黑格
    for row in range(8):                     # 行号 0~7 对应数字 1~8
        for col in range(8):                 # 列号 0~7 对应字母 a~h
            # 若行号 + 列号 为奇数，则该格为白格
            board[row][col] = (row + col) % 2   # 1 为白，0 为黑

    # 2. 把输入坐标转成数组下标
    col_char, row_char = coordinates[0], coordinates[1]
    col = ord(col_char) - ord('a')   # 'a' -> 0, 'b' -> 1, ...
    row = int(row_char) - 1          # '1' -> 0, '2' -> 1, ...

    # 3. 直接查表返回颜色
    return board[row][col] == 1      # 1 表示白格
```

#### 复杂度

- **时间复杂度**：O(1)（常数时间）——虽然内部遍历了 64 次，但 64 是固定不变的常数。  
- **空间复杂度**：O(1)（常数空间）——额外使用的 8×8 列表大小固定。

---

### 2. 最优解

#### 思路  

从暴力解出发，**慢的地方**其实是我们把整张棋盘都写了一遍，而题目只要我们判断**一个格子**的颜色。  
观察棋盘可以发现：

| 列 (a‑h) | 行 (1‑8) |
|----------|----------|
| a1 为黑 | a2 为白 |
| b1 为白 | b2 为黑 |

颜色呈 **交替** 的规律：相邻格子的颜色总是相反。  
如果把列号转换成数字（a → 1, b → 2, …, h → 8），行号本身已经是数字 1‑8。  
**关键发现**：  
- 当 **列号 + 行号** 为 **偶数** 时，格子是黑色。  
- 当 **列号 + 行号** 为 **奇数** 时，格子是白色。

为什么会这样？可以把棋盘想象成一张黑白相间的格子纸，左上角 (a1) 是黑格，往右或往下走一步就会换颜色。每走一步，行号或列号就加 1，奇偶性（偶/奇）就会翻转一次。于是**行号 + 列号的奇偶性**恰好记录了走了多少次“换颜色”，从而决定了最终颜色。

**实现步骤**：

1. 把字母转成 1‑8 的数字：`col = ord(coordinates[0]) - ord('a') + 1`。  
2. 把字符数字转成整数：`row = int(coordinates[1])`。  
3. 计算 `(col + row) % 2`：  
   - 结果为 `1` → 白格 → 返回 `True`。  
   - 结果为 `0` → 黑格 → 返回 `False`。

整个过程只做了几次算术运算，**不需要任何额外的存储**，因此是最优的。

#### 代码（Python）

```python
def square_is_white(coordinates: str) -> bool:
    """
    最优解：利用行列编号之和的奇偶性判断颜色。
    返回 True 表示白格，False 表示黑格。
    """
    # 1. 把字母列转换成 1~8 的数字（'a'->1, 'b'->2, ...）
    col = ord(coordinates[0]) - ord('a') + 1

    # 2. 把数字字符转换成整数（'1'->1, ...）
    row = int(coordinates[1])

    # 3. 奇偶性决定颜色：奇数 → 白格，偶数 → 黑格
    return (col + row) % 2 == 1
```

#### 复杂度

- **时间复杂度**：O(1) — 只做了常数次的字符转换和加法、取模运算。相比暴力解省去了遍历棋盘的 64 步，真正做到“一次算完”。  
- **空间复杂度**：O(1) — 只使用了几个整数变量，没有额外的数据结构。

---

## 心得

- **核心技巧**：**奇偶性判断**（Parity Check）。在很多棋盘、格子类题目中，颜色或状态往往跟“走了多少步”有关，而走的步数可以用行号 + 列号的奇偶性直接表达。
- **适用的题型**  
  1. 判断棋盘格子颜色（本题）。  
  2. 判断国际象棋马的移动是否在同色格子上。  
  3. 判断二维网格中“棋盘染色”是否冲突（例如 LeetCode 886. Possible Bipartition）。
- **解题钥匙**：**把坐标映射成数字，观察“行+列”的奇偶性**。

---

## 反思

- **第一反应**：把整张棋盘画出来，用查表的方式回答。虽然能得到正确结果，却显得“笨重”。  
- **最容易踩的坑**  
  - 把字母转换成数字时忘记 `+1`，导致 a 对应 0，进而导致奇偶性判断出错。  
  - 坐标字符串长度固定为 2，若不检查直接取 `coordinates[1]`，在非法输入时会报错（但本题保证合法）。  
- **下次遇到同类题**：第一步应该先**思考是否存在一种数学规律**（如奇偶性、模运算），而不是直接构造完整的数据结构。这样往往能直接得到 O(1) 的简洁解法。