# #2296. 文本编辑器设计 / Design a Text Editor

> 难度：困难 · 标签：Linked List、String、Stack、Design、Simulation、Doubly-Linked List · [LeetCode 链接](https://leetcode.com/problems/design-a-text-editor/)

---

## 题目（英文原版）

**Description**

Design a text editor with a cursor that can do the following:
When deleting text, only characters to the left of the cursor will be deleted. The cursor will also remain within the actual text and cannot be moved beyond it. More formally, we have that 0 <= cursor.position <= currentText.length always holds.
Implement the TextEditor class:
Follow-up: Could you find a solution with time complexity of O(k) per call?

**Examples**

**Example 1:**

```
Input
["TextEditor", "addText", "deleteText", "addText", "cursorRight", "cursorLeft", "deleteText", "cursorLeft", "cursorRight"]
[[], ["leetcode"], [4], ["practice"], [3], [8], [10], [2], [6]]
Output
[null, null, 4, null, "etpractice", "leet", 4, "", "practi"]

Explanation
TextEditor textEditor = new TextEditor(); // The current text is "|". (The '|' character represents the cursor)
textEditor.addText("leetcode"); // The current text is "leetcode|".
textEditor.deleteText(4); // return 4
                          // The current text is "leet|". 
                          // 4 characters were deleted.
textEditor.addText("practice"); // The current text is "leetpractice|". 
textEditor.cursorRight(3); // return "etpractice"
                           // The current text is "leetpractice|". 
                           // The cursor cannot be moved beyond the actual text and thus did not move.
                           // "etpractice" is the last 10 characters to the left of the cursor.
textEditor.cursorLeft(8); // return "leet"
                          // The current text is "leet|practice".
                          // "leet" is the last min(10, 4) = 4 characters to the left of the cursor.
textEditor.deleteText(10); // return 4
                           // The current text is "|practice".
                           // Only 4 characters were deleted.
textEditor.cursorLeft(2); // return ""
                          // The current text is "|practice".
                          // The cursor cannot be moved beyond the actual text and thus did not move. 
                          // "" is the last min(10, 0) = 0 characters to the left of the cursor.
textEditor.cursorRight(6); // return "practi"
                           // The current text is "practi|ce".
                           // "practi" is the last min(10, 6) = 6 characters to the left of the cursor.
```

**Constraints**

- 1 <= text.length, k <= 40
- text consists of lowercase English letters.
- At most 2 * 104 calls in total will be made to addText, deleteText, cursorLeft and cursorRight.

---

## 题目（中文翻译）

设计一个带有光标（cursor）的文本编辑器，支持以下操作：

- 当删除文本时，只会删除光标左侧的字符。光标始终位于文本内部，且不能移出文本范围。形式化地，始终满足 `0 <= cursor.position <= currentText.length`。
- 实现 `TextEditor` 类，使其能够处理以下方法：
  - `addText(string text)`：在光标所在位置插入 `text`，光标移动至插入文本的末尾。
  - `deleteText(int k)`：删除光标左侧最多 `k` 个字符，返回实际删除的字符数。光标向左移动相同的距离。
  - `cursorLeft(int k)`：将光标左移 `k` 次（最多移动到文本开头），返回光标左侧最多 10 个字符组成的字符串。
  - `cursorRight(int k)`：将光标右移 `k` 次（最多移动到文本结尾），返回光标左侧最多 10 个字符组成的字符串。

**示例 1**

```json
Input
["TextEditor", "addText", "deleteText", "addText", "cursorRight", "cursorLeft", "deleteText", "cursorLeft", "cursorRight"]
[[], ["leetcode"], [4], ["practice"], [3], [8], [10], [2], [6]]
Output
[null, null, 4, null, "etpractice", "leet", 4, "", "practi"]
```

**解释**

```java
TextEditor textEditor = new TextEditor(); // 当前文本为 "|"（'|' 表示光标）
textEditor.addText("leetcode");          // 文本变为 "leetcode|"
textEditor.deleteText(4);                // 删除左侧 4 个字符，返回 4，文本变为 "leet|"
textEditor.addText("practice");          // 文本变为 "leetpractice|"
textEditor.cursorRight(3);               // 光标右移 3 次，返回 "etpractice"
textEditor.cursorLeft(8);                // 光标左移 8 次，返回 "leet"
textEditor.deleteText(10);               // 删除左侧最多 10 个字符，实际删除 4，返回 4，文本变为 "|"
textEditor.cursorLeft(2);                // 已经在最左侧，返回空字符串 ""
textEditor.cursorRight(6);               // 光标右移 6 次，返回 "practi"
```

**约束条件**

- `1 <= text.length, k <= 40`
- `text` 仅由小写英文字母组成。
- 最多会有 `2 * 10^4` 次对 `addText`、`deleteText`、`cursorLeft` 和 `cursorRight` 的调用。

**进阶**

能否实现每次调用的时间复杂度为 `O(k)`？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把整个文本保存成一个普通的 **Python 字符串**，再用一个整数 `cursor` 记录光标所在的位置（光标左边的字符数）。  
- **addText**：把新字符串插入到 `cursor` 位置，等价于 `text = text[:cursor] + s + text[cursor:]`，随后把 `cursor` 向右移动 `len(s)`。  
- **deleteText**：把光标左侧的 `k` 个字符删掉，同样使用切片 `text = text[:max(0, cursor-k)] + text[cursor:]`，并把 `cursor` 往左移动实际删除的字符数。  
- **cursorLeft / cursorRight**：只需要把 `cursor` 往左或往右移动 `k`（注意不能越界），随后返回光标左侧最多 10 个字符 `text[max(0, cursor-10):cursor]`。

> **类比**：把文本想象成一本书的整页内容，光标是书签所在的页码。每次插入或删除都要把整本书重新装订（复制），这在书很厚时会非常慢。

这个办法**一定能得到正确答案**，因为我们每次都完整地维护了文本的真实内容，光标位置始终满足题目要求的 `0 ≤ cursor ≤ len(text)`。

#### 代码（Python）

```python
class TextEditor:
    def __init__(self):
        self.text = ""          # 整个文本，初始为空
        self.cursor = 0         # 光标在文本中的位置，0 表示在最左侧

    # 在光标左侧插入字符串
    def addText(self, s: str) -> None:
        # 把 s 插入到 cursor 位置
        self.text = self.text[:self.cursor] + s + self.text[self.cursor:]
        self.cursor += len(s)   # 光标右移，刚好在新插入字符的后面

    # 删除光标左侧最多 k 个字符，返回实际删除的字符数
    def deleteText(self, k: int) -> int:
        # 实际能删除的字符数
        del_cnt = min(k, self.cursor)
        # 删除后重新拼接字符串
        self.text = self.text[:self.cursor - del_cnt] + self.text[self.cursor:]
        self.cursor -= del_cnt   # 光标左移
        return del_cnt

    # 将光标左移 k 步，返回光标左侧最多 10 个字符
    def cursorLeft(self, k: int) -> str:
        self.cursor = max(0, self.cursor - k)   # 不能越界
        # 取光标左侧最多 10 个字符
        start = max(0, self.cursor - 10)
        return self.text[start:self.cursor]

    # 将光标右移 k 步，返回光标左侧最多 10 个字符
    def cursorRight(self, k: int) -> str:
        self.cursor = min(len(self.text), self.cursor + k)   # 不能越界
        start = max(0, self.cursor - 10)
        return self.text[start:self.cursor]
```

#### 复杂度  

- **时间复杂度**：  
  - `addText`、`deleteText`、`cursorLeft`、`cursorRight` 都要对整个字符串做切片拼接，最坏情况是 O(*n*)，其中 *n* 为当前文本长度。  
  - 用大白话说，就是每次操作都要“搬家”，如果文本有 10 万字符，单次操作可能要搬 10 万次字符。  
- **空间复杂度**：  
  - 需要保存完整的文本，空间是 O(*n*)。  
  - 额外的变量只有 `cursor` 一个整数，算作 O(1)。

---

### 2. 最优解

#### 思路  

在暴力解中，最大的瓶颈是 **对整段字符串的切片与拼接**——这相当于每次都把整个文本搬一遍。  
要实现 **每次操作只和光标左/右侧的少量字符打交道**，我们可以把文本 **在光标处切成两段**：

- **左侧（left）**：光标左边的所有字符，顺序与实际文本相同。  
- **右侧（right）**：光标右边的所有字符，顺序同样与实际文本相同。

如果把这两段分别保存在 **栈（或双端队列 deque）** 中：

- 栈顶对应光标左边的最近字符，栈底对应文本最左端。  
- 右侧栈的栈顶对应光标右边的最近字符，栈底对应文本最右端。

这样，**所有操作只涉及栈顶的 push / pop**，即 O(1) 时间。  
当需要返回光标左侧最多 10 个字符时，只要从左侧栈的栈顶向下取最多 10 个即可（仍然是 O(10) = O(1)）。

> **类比**：想象你在一根绳子上系了两个小盒子，左盒子装的是光标左边的字符，右盒子装的是光标右边的字符。往左移动光标就把左盒子最上面的字符搬到右盒子最上面，往右移动光标则相反。盒子之间的搬运只涉及最上面的几颗珠子，速度极快。

**关键数据结构**  
- `left` : `list` 当作栈使用（`append` / `pop`）  
- `right` : 也是 `list`（同理）  

**每个接口的实现**  

| 操作 | 具体做法 |
|------|----------|
| `addText(s)` | 把 `s` 的每个字符依次 `append` 到 `left`（相当于在光标左侧插入）。 |
| `deleteText(k)` | 重复弹出 `left.pop()` 最多 `k` 次，计数即为实际删除数。 |
| `cursorLeft(k)` | 重复把 `left.pop()` 的字符 `append` 到 `right`，最多 `k` 次（若 `left` 为空则停止）。最后返回 `left` 最后 10 个字符（从栈底到栈顶）。 |
| `cursorRight(k)` | 与 `cursorLeft` 对称：把 `right.pop()` 的字符 `append` 到 `left`，最多 `k` 次。返回同样的 10 字符片段。 |

**为什么 O(k)？**  
每次 `cursorLeft` / `cursorRight` 最多移动 `k` 次字符，`k` 是调用时给出的参数，且每次移动只涉及栈顶的 `pop` / `append`，这两个操作都是 O(1)。所以整体是 O(k)。  

**返回左侧 10 个字符**  
`left` 是栈结构，直接切片 `left[-10:]` 能得到从左侧最近字符向左数的最多 10 个字符（顺序仍然是左到右），再用 `''.join()` 拼成字符串即可。

#### 代码（Python）

```python
class TextEditor:
    def __init__(self):
        # left 保存光标左侧字符，顺序与文本相同（最左端在下标 0）
        self.left = []   # 用 list 当作栈，append / pop 在右端
        # right 保存光标右侧字符，顺序也与文本相同
        self.right = []  # 同上

    # 在光标左侧插入字符串
    def addText(self, s: str) -> None:
        for ch in s:
            self.left.append(ch)      # 直接压到左栈顶，相当于光标左边新增字符

    # 删除光标左侧最多 k 个字符，返回实际删除的字符数
    def deleteText(self, k: int) -> int:
        del_cnt = 0
        while del_cnt < k and self.left:
            self.left.pop()           # 弹出左栈顶字符，即删除
            del_cnt += 1
        return del_cnt

    # 将光标左移 k 步，返回光标左侧最多 10 个字符
    def cursorLeft(self, k: int) -> str:
        move_cnt = 0
        while move_cnt < k and self.left:
            # 把左栈顶字符移到右栈顶
            self.right.append(self.left.pop())
            move_cnt += 1
        return self._left_ten()

    # 将光标右移 k 步，返回光标左侧最多 10 个字符
    def cursorRight(self, k: int) -> str:
        move_cnt = 0
        while move_cnt < k and self.right:
            # 把右栈顶字符移到左栈顶
            self.left.append(self.right.pop())
            move_cnt += 1
        return self._left_ten()

    # 私有工具：取左侧最多 10 个字符并拼成字符串
    def _left_ten(self) -> str:
        # left[-10:] 取最右侧（即光标左侧最近）的最多 10 个字符
        # 再用 ''.join' 把列表转成字符串
        return ''.join(self.left[-10:])
```

#### 复杂度  

- **时间复杂度**  
  - `addText`：遍历待插入字符串，长度记为 *m*，每次 `append` 为 O(1)，整体 O(*m*)。  
  - `deleteText`、`cursorLeft`、`cursorRight`：最多循环 `k` 次，每次都是 O(1)，所以都是 **O(k)**。  
  - 这里的 *k* 是本次调用传入的参数，题目要求的 “每次调用 O(k)” 正好满足。  

- **空间复杂度**  
  - 两个栈共同保存了全部字符，最多占用 O(*n*)，其中 *n* 为当前文本长度。  
  - 额外的临时变量都是常数级别，算作 O(1)。  
  - 与暴力解相比，空间没有增加，只是把一个大字符串拆成了两个小容器，方便局部操作。

---

## 心得

- **核心技巧**：把光标左右的字符分别放在两个栈（或双端队列）中，使得所有编辑操作都只在栈顶进行，从而实现 **局部 O(1) 操作**。  
- **适用的题型**  
  1. 需要在中间位置频繁插入/删除的文本编辑类问题（如 LeetCode 1406. **石子游戏** 的双端队列思路）。  
  2. “左括号/右括号平衡” 类的实时检查（使用栈）。  
  3. “浏览器前进/后退” 功能实现（两个栈模拟历史记录）。  
- **一句话总结**：把光标左右拆成两堆，只在堆顶搬砖，编辑即瞬间完成。

---

## 反思

- **第一反应**：直接用字符串切片实现，想到“最直接的暴力办法”。  
- **最容易踩的坑**  
  - **边界条件**：光标不能越界，移动时需要检查对应栈是否为空。  
  - **返回的 10 个字符顺序**：`left[-10:]` 取的是从左到右的顺序，若误用 `reversed` 会导致输出倒置。  
  - **删除时实际删除数**：当 `k` 大于左侧字符数时，只能删除已有的字符，需要返回实际删除的数量。  
- **下次第一步**：先思考“能否把问题拆成只在两端操作的结构”，如果答案是“能”，就尝试用 **双栈 / 双 deque** 来实现。