# #3484. 设计电子表格 / Design Spreadsheet

> 难度：中等 · 标签：Array、Hash Table、String、Design、Matrix · [LeetCode 链接](https://leetcode.com/problems/design-spreadsheet/)

---

## 题目（英文原版）

**Description**

A spreadsheet is a grid with 26 columns (labeled from 'A' to 'Z') and a given number of rows. Each cell in the spreadsheet can hold an integer value between 0 and 105.
Implement the Spreadsheet class:
Note: If getValue references a cell that has not been explicitly set using setCell, its value is considered 0.

**Examples**

**Example 1:**

```
Input: ["Spreadsheet", "getValue", "setCell", "getValue", "setCell", "getValue", "resetCell", "getValue"] [[3], ["=5+7"], ["A1", 10], ["=A1+6"], ["B2", 15], ["=A1+B2"], ["A1"], ["=A1+B2"]]
Output: [null, 12, null, 16, null, 25, null, 15]
Explanation
```

**Constraints**

- 1 <= rows <= 103
- 0 <= value <= 105
- The formula is always in the format "=X+Y", where X and Y are either valid cell references or non-negative integers with values less than or equal to 105.
- Each cell reference consists of a capital letter from 'A' to 'Z' followed by a row number between 1 and rows.
- At most 104 calls will be made in total to setCell, resetCell, and getValue.

---

## 题目（中文翻译）

**描述**  
电子表格（Spreadsheet）是一个网格，包含 26 列（标签为 `'A'` 到 `'Z'`）和给定数量的行。电子表格中的每个单元格（cell）可以存放 0 到 10^5 之间的整数值。实现 `Spreadsheet` 类：

> **注意**：如果 `getValue` 引用了一个未通过 `setCell` 显式设置过的单元格，则该单元格的值视为 0。

**示例 1**

```text
Input: ["Spreadsheet", "getValue", "setCell", "getValue", "setCell", "getValue", "resetCell", "getValue"]
       [[3], ["=5+7"], ["A1", 10], ["=A1+6"], ["B2", 15], ["=A1+B2"], ["A1"], ["=A1+B2"]]
Output: [null, 12, null, 16, null, 25, null, 15]
Explanation
- 创建一个有 3 行的电子表格。
- `getValue("=5+7")` 计算公式，返回 12。
- `setCell("A1", 10)` 将单元格 A1 的值设为 10。
- `getValue("=A1+6")` 读取 A1 的值并加 6，返回 16。
- `setCell("B2", 15)` 将单元格 B2 的值设为 15。
- `getValue("=A1+B2")` 读取 A1 与 B2 的值相加，返回 25。
- `resetCell("A1")` 将 A1 重置为未设置状态（值视为 0）。
- `getValue("=A1+B2")` 此时 A1 为 0，B2 为 15，返回 15。
```

**约束条件**  

- `1 <= rows <= 10^3`
- `0 <= value <= 10^5`
- 公式（formula）始终遵循 `"=X+Y"` 的格式，其中 `X` 与 `Y` 要么是有效的单元格引用（cell reference），要么是不超过 10^5 的非负整数。
- 每个单元格引用由大写字母 `'A'` 到 `'Z'` 加上行号组成，行号在 `1` 到 `rows` 之间。
- `setCell`、`resetCell` 与 `getValue` 的调用总次数不超过 `10^4`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把整个电子表格都建成一个 **二维数组**（`rows × 26`），每个格子里存放整数。  
- **setCell**：把对应坐标的值改成给定的数。  
- **resetCell**：把对应坐标的值改成 `0`。  
- **getValue**：先把公式字符串 `=X+Y` 拆成左、右两个 **操作数**。如果操作数是 **单纯的数字**，直接转成整数；如果是 **单元格引用**（比如 `A1`），就把列字母转成 `0~25` 的索引、行号转成 `0~rows-1` 的索引，然后在二维数组里取值。最后把两个数相加返回。

> **类比**：二维数组就像一张 **坐标纸**，每个格子都有固定的行号和列号。查找格子就像在坐标纸上找交叉点一样直接。

**为什么正确**  
- 所有单元格的值都保存在数组里，随时可以 O(1) 读取或修改。  
- 公式只涉及加法且两侧都是 **常数** 或 **单元格**，只要把两侧的值算出来相加即可。

**时间/空间复杂度**  
- **时间**：  
  - `setCell` / `resetCell` / `getValue` 每一步都只做 **常数次** 的数组下标访问和字符串拆分，**O(1)**。  
  - 但如果我们在 `getValue` 时 **遍历整个数组** 去找对应的单元格（比如把单元格名当作键去线性搜索），则会是 **O(rows·26)**，这就是“暴力”做法的瓶颈。  
- **空间**：  
  - 需要存储 `rows × 26` 个整数，**O(rows·26)**，即 **O(rows)**（因为 26 是常数）。

#### 代码（Python）

```python
class Spreadsheet:
    def __init__(self, rows: int):
        """
        用一个二维列表模拟整个表格。
        行数为 rows，列数固定为 26（A~Z）。
        初始全部为 0。
        """
        self.rows = rows
        self.cols = 26
        self.grid = [[0] * self.cols for _ in range(rows)]

    def _parse_cell(self, ref: str):
        """
        把类似 "B3" 的引用转成 (row_idx, col_idx)。
        col_idx = ord('B') - ord('A') -> 1
        row_idx = int('3') - 1 -> 2
        """
        col = ord(ref[0]) - ord('A')
        row = int(ref[1:]) - 1
        return row, col

    def setCell(self, cell: str, value: int) -> None:
        """把指定单元格的值改成 value"""
        r, c = self._parse_cell(cell)
        self.grid[r][c] = value

    def resetCell(self, cell: str) -> None:
        """把指定单元格的值恢复为 0"""
        r, c = self._parse_cell(cell)
        self.grid[r][c] = 0

    def getValue(self, formula: str) -> int:
        """
        公式形如 "=X+Y"（X、Y 可以是数字或单元格引用）。
        先去掉开头的 '=', 再把左右两侧用 '+' 分开。
        """
        # 去掉等号
        expr = formula[1:]                 # 例如 "A1+6"
        left, right = expr.split('+')      # 分成 "A1" 和 "6"

        def eval_operand(op: str) -> int:
            """把操作数转成整数，若是引用则去表格取值"""
            if op[0].isalpha():           # 以字母开头说明是单元格引用
                r, c = self._parse_cell(op)
                return self.grid[r][c]
            else:                         # 纯数字
                return int(op)

        return eval_operand(left) + eval_operand(right)
```

#### 复杂度

- **时间复杂度**：`O(1)` —— 每次操作只做常数次的下标访问和字符串切分，不随 `rows` 增长。  
  - 这里的 `O(1)` 可以理解为“**不管表格有多大，花的时间都差不多**”。  
- **空间复杂度**：`O(rows·26)` —— 需要一整个二维数组来存所有格子的值。因为列数固定为 26，实际是 **O(rows)**。

---

### 2. 最优解

#### 思路  

从上面的暴力实现可以看到，**真正需要的并不是把所有格子都装进内存**，因为大多数格子在使用前都是默认的 `0`。我们可以只保存**被显式设置过的格子**，其余格子视作 `0`。这正好对应 **哈希表（字典）** 的使用场景。

**瓶颈**  
- 暴力解占用了 `rows × 26` 的空间，`rows` 最多可达 `10³`，虽然不算大，但在更大的约束下会浪费很多内存。  
- 读取或写入时仍然需要先把引用解析成坐标，这一步本身已经是最优的 O(1)。所以我们只需要把“存储结构”换成更省空间的方式。

**核心技巧**：  
- **哈希表**（`dict`）就像一本 **查字典**，`key` 是单元格名称（例如 `"A1"`），`value` 是该格子的整数值。没有出现过的 `key`，我们默认返回 `0`。  
- 公式解析仍然保持不变，只是把 **二维数组查询** 替换成 **字典查询**。

**一步步推导**  
1. **只保存被写过的格子**：`setCell` 时把 `cell` → `value` 放进字典；`resetCell` 时把对应的键删掉（或设为 `0`）。  
2. **读取时默认 0**：在 `getValue` 里，若操作数是单元格引用，先在字典里查找；如果找不到，说明从未被设置过，直接返回 `0`。  
3. 由于题目保证公式永远是 `"=X+Y"`，不需要考虑更复杂的表达式或循环依赖，直接求两侧的值相加即可。

**类比**：  
- 想象你有一本 **电话簿**，只记录已经有人联系过的电话号码。要找某个人的号码，先看电话簿里有没有；没有的话，就认为他不在名单里，返回 “空号”。这里的 “电话簿” 就是字典， “空号” 对应默认的 `0`。

#### 代码（Python）

```python
class Spreadsheet:
    def __init__(self, rows: int):
        """
        只记录被显式赋值的单元格，未出现的视作 0。
        使用 dict，key 为单元格名称（如 "A1"），value 为整数。
        rows 参数仅用于合法性检查（本实现不做额外验证）。
        """
        self.rows = rows
        self.cells = {}          # 哈希表：cell_name -> value

    def setCell(self, cell: str, value: int) -> None:
        """把 cell 的值设为 value，直接写入哈希表"""
        self.cells[cell] = value

    def resetCell(self, cell: str) -> None:
        """恢复 cell 为默认值 0，等价于把它从哈希表中删掉"""
        self.cells.pop(cell, None)   # 若不存在也不报错

    def _value_of(self, token: str) -> int:
        """
        解析单个操作数：
        - 如果是数字，直接转成 int。
        - 如果是单元格引用，去哈希表找，找不到返回 0。
        """
        if token[0].isalpha():           # 单元格引用，如 "B2"
            return self.cells.get(token, 0)
        else:                            # 纯数字
            return int(token)

    def getValue(self, formula: str) -> int:
        """
        公式始终形如 "=X+Y"。先去掉等号，再分割左右两侧，
        分别解析得到整数后相加返回。
        """
        expr = formula[1:]                # 去掉开头的 '='
        left, right = expr.split('+')     # 例如 "A1" 和 "6"
        return self._value_of(left) + self._value_of(right)
```

#### 复杂度

- **时间复杂度**：`O(1)` ——  
  - `setCell`、`resetCell`、`getValue` 都只做一次哈希表的 **插入 / 删除 / 查找**，在均摊意义下是常数时间。  
  - 与暴力解相比，**没有遍历整个表格**，所以更快（尤其在行数很大时）。

- **空间复杂度**：`O(k)` ——  
  - `k` 为实际被设置过的格子数量（最多 `10⁴` 次调用），而不是 `rows·26`。  
  - 这可以理解为“只占用**实际用到的**空间”，如果只改动很少的格子，内存占用几乎为零。

---

## 心得

- **核心技巧**：用哈希表只保存“非默认”值，默认值通过 `dict.get(key, 0)` 轻松返回。  
- **适用场景**：  
  1. **稀疏矩阵**（大部分元素为 0，只需要记录非零元素）。  
  2. **缓存系统**（只缓存被请求过的结果）。  
  3. **文本编辑器的撤销/恢复**（只记录被改动的字符位置）。  
- **解题钥匙**：**“只记录变化的东西，默认值直接返回”**。

## 反思

- **第一反应**：把整个表格全部建出来，像平铺的纸一样遍历。  
- **最容易踩的坑**：  
  - 忽略公式中出现的 **数字** 与 **单元格** 的区别，导致把数字当成键去查字典。  
  - 没有对 `resetCell` 做 “删除键” 的处理，导致默认值仍然是旧值。  
  - 没有考虑行号超过 `rows` 的非法引用（本题保证合法，可在实际项目中加入检查）。  
- **下次思路**：遇到“默认值很多、只会改动少量”的矩阵/表格类问题，第一步就想到 **哈希表（稀疏存储）**，而不是完整的二维数组。