# #3274. 检查两个棋盘格是否颜色相同 / Check if Two Chessboard Squares Have the Same Color

> 难度：简单 · 标签：Math、String · [LeetCode 链接](https://leetcode.com/problems/check-if-two-chessboard-squares-have-the-same-color/)

---

## 题目（英文原版）

**Description**

You are given two strings, coordinate1 and coordinate2, representing the coordinates of a square on an 8 x 8 chessboard.
Below is the chessboard for reference.
Return true if these two squares have the same color and false otherwise.
The coordinate will always represent a valid chessboard square. The coordinate will always have the letter first (indicating its column), and the number second (indicating its row).

**Examples**

**Example 1:**

```
Input: coordinate1 = "a1", coordinate2 = "c3"
Output: true
Explanation:
Both squares are black.
```

**Example 2:**

```
Input: coordinate1 = "a1", coordinate2 = "h3"
Output: false
Explanation:
Square "a1" is black and "h3" is white.
```

**Constraints**

- coordinate1.length == coordinate2.length == 2
- 'a' <= coordinate1[0], coordinate2[0] <= 'h'
- '1' <= coordinate1[1], coordinate2[1] <= '8'

---

## 题目（中文翻译）

**题目描述**  
给定两个字符串 `coordinate1` 和 `coordinate2`，它们分别表示 8×8 国际象棋棋盘上某个格子的坐标。坐标的格式始终为字母在前（表示列），数字在后（表示行），且必定是合法的棋盘格子。  
返回 `true` 当且仅当这两个格子颜色相同，否则返回 `false`。  

**示例**  

示例 1  
```
Input: coordinate1 = "a1", coordinate2 = "c3"
Output: true
Explanation:
Both squares are black.
```
解释：两个格子都是黑色的。  

示例 2  
```
Input: coordinate1 = "a1", coordinate2 = "h3"
Output: false
Explanation:
Square "a1" is black and "h3" is white.
```
解释：格子 `"a1"` 为黑色，而 `"h3"` 为白色。  

**约束条件**  

- `coordinate1.length == coordinate2.length == 2`
- `'a' <= coordinate1[0], coordinate2[0] <= 'h'`
- `'1' <= coordinate1[1], coordinate2[1] <= '8'`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是先把整张 8×8 的棋盘“画”出来，记住每个格子的颜色，然后把输入的坐标直接在这张表里查。  
- **数据结构**：我们可以用一个二维列表（list of list）来存放棋盘。二维列表就像一本**表格**，行号是下标，列号也是下标。  
- **颜色规则**：左下角 `a1` 是黑色，随后每相邻格子颜色交替。于是我们可以用 **奇偶交替** 来填充整张表：如果行号 + 列号是偶数，就是黑色；否则是白色。  
- **查找**：把坐标的字母（`a`~`h`）转成列号（0~7），把数字（`1`~`8`）转成行号（0~7），直接在表里取颜色比较即可。  

这种方法**一定能得到正确答案**，因为我们把每一个格子的颜色都显式地写了出来，查表自然不会错。  

#### 代码（Python）  
```python
def squares_are_same_color_bruteforce(coordinate1: str, coordinate2: str) -> bool:
    # 1️⃣ 先构造一张 8×8 的棋盘，True 表示黑色，False 表示白色
    board = [[False] * 8 for _ in range(8)]          # 创建 8 行 8 列的空表
    for r in range(8):                               # r 表示行（0~7）
        for c in range(8):                           # c 表示列（0~7）
            # 行号 + 列号 为偶数的格子为黑色（True），奇数为白色（False）
            board[r][c] = (r + c) % 2 == 0

    # 2️⃣ 把坐标转成数组下标
    def to_index(coord: str) -> (int, int):
        col = ord(coord[0]) - ord('a')   # 'a'→0, 'b'→1, …, 'h'→7
        row = int(coord[1]) - 1          # '1'→0, '2'→1, …, '8'→7
        return row, col

    r1, c1 = to_index(coordinate1)
    r2, c2 = to_index(coordinate2)

    # 3️⃣ 直接比较两格的颜色
    return board[r1][c1] == board[r2][c2]
```

#### 复杂度  
- **时间复杂度**：`O(8·8) = O(1)`  
  虽然我们遍历了整张棋盘（64 次），但 64 是一个固定常数，和输入大小无关，所以算作 **常数时间**。可以把它想象成“只需要几秒钟就能把整块棋盘检查完”。  
- **空间复杂度**：`O(8·8) = O(1)`  
  我们额外开了一个 8×8 的表，大小固定，不会随输入增大而增长。  

---

### 2. 最优解  

#### 思路  
从暴力解可以看到，真正决定格子颜色的只有 **行号 + 列号 的奇偶性**，我们根本不需要把整张棋盘都写出来。  
- **瓶颈**：暴力解的“遍历整个棋盘”这一步是多余的。  
- **优化**：直接把坐标转换成数字后，计算 `row + col` 的奇偶性即可得到颜色。  
- **核心技巧**：**奇偶性判断**（Parity Check）。  
  - 奇数+奇数 = 偶数 → 同色（都是黑）  
  - 偶数+偶数 = 偶数 → 同色（都是黑）  
  - 奇数+偶数 = 奇数 → 不同色（一个黑一个白）  
  把“颜色是黑色当且仅当 `row + col` 为偶数”这条规则直接写进代码，就不需要任何额外空间。  

**类比**：把棋盘看成一条黑白相间的条纹地毯，只要知道你站在第几格（行+列），就能立刻判断是黑还是白，不需要把整块地毯铺开来检查。  

#### 代码（Python）  
```python
def squares_are_same_color(coordinate1: str, coordinate2: str) -> bool:
    """
    只用 O(1) 的时间和空间判断两格是否同色。
    """

    def color(coord: str) -> int:
        """
        返回格子的颜色：0 表示白色，1 表示黑色。
        计算方式：行号 + 列号 的奇偶性（奇数 → 1，偶数 → 0）。
        """
        col = ord(coord[0]) - ord('a')   # 列号 0~7
        row = int(coord[1]) - 1          # 行号 0~7
        # (row + col) % 2 为 0 表示白色，为 1 表示黑色
        return (row + col) % 2

    return color(coordinate1) == color(coordinate2)
```

#### 复杂度  
- **时间复杂度**：`O(1)`  
  只做了几次算术运算和字符转数字，和输入大小无关。可以理解为“瞬间就能算出答案”。  
- **空间复杂度**：`O(1)`  
  只用了几个整数变量，额外占用的内存是常数级的。  

---

## 心得  

- **核心技巧**：利用**行列坐标之和的奇偶性**直接判断颜色。  
- **适用题型**：  
  1. 判断棋盘或格子颜色的题目（如 “Determine if a cell is white/black”）。  
  2. 判断网格中“交替”属性的题目（如 “Pattern of a checkerboard”）。  
  3. 需要根据坐标的奇偶性分类的题目（如 “Maximum size of a chessboard submatrix with same parity”）。  
- **一句话总结解题钥匙**：**把空间映射到数字，奇偶性就是颜色**。  

---

## 反思  

- **第一反应**：先把棋盘画出来，查表验证。  
- **最容易踩的坑**：  
  - 把字母 `'a'~'h'` 当作数字直接相加，而忘记先转成 0~7 的索引。  
  - 把行号当作字符 `'1'~'8'` 直接相加，导致得到的不是数值。  
  - 忘记 `a1` 是黑色（即奇偶性为偶），容易把黑白判反。  
- **下次思路**：看到“棋盘”“格子颜色”这类描述，第一步就想到“行+列的奇偶性”。只要把坐标转成数字，奇偶性判断即可。