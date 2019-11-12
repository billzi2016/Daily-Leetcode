# #657. 机器人返回原点 / Robot Return to Origin

> 难度：简单 · 标签：String、Simulation · [LeetCode 链接](https://leetcode.com/problems/robot-return-to-origin/)

---

## 题目（英文原版）

**Description**

There is a robot starting at the position (0, 0), the origin, on a 2D plane. Given a sequence of its moves, judge if this robot ends up at (0, 0) after it completes its moves.
You are given a string moves that represents the move sequence of the robot where moves[i] represents its ith move. Valid moves are 'R' (right), 'L' (left), 'U' (up), and 'D' (down).
Return true if the robot returns to the origin after it finishes all of its moves, or false otherwise.
Note: The way that the robot is "facing" is irrelevant. 'R' will always make the robot move to the right once, 'L' will always make it move left, etc. Also, assume that the magnitude of the robot's movement is the same for each move.

**Examples**

**Example 1:**

```
Input: moves = "UD"
Output: true
Explanation: The robot moves up once, and then down once. All moves have the same magnitude, so it ended up at the origin where it started. Therefore, we return true.
```

**Example 2:**

```
Input: moves = "LL"
Output: false
Explanation: The robot moves left twice. It ends up two "moves" to the left of the origin. We return false because it is not at the origin at the end of its moves.
```

**Constraints**

- 1 <= moves.length <= 2 * 104
- moves only contains the characters 'U', 'D', 'L' and 'R'.

---

## 题目（中文翻译）

有一个机器人初始位于二维平面（2D plane）上的原点 (0, 0)。给定它的移动序列，判断机器人在完成所有移动后是否回到 (0, 0)。  
你会得到一个字符串 `moves`，其中 `moves[i]` 表示机器人第 i 次移动。合法的移动指令包括：

- `'R'`：向右移动一次  
- `'L'`：向左移动一次  
- `'U'`：向上移动一次  
- `'D'`：向下移动一次  

返回 `true` 表示机器人在完成所有移动后回到了原点，返回 `false` 则表示未回到原点。  
注意：机器人“面向”的方向并不影响移动结果，`'R'` 总是让机器人向右移动一次，`'L'` 总是向左移动一次，依此类推。并且每一步的移动幅度相同。

**示例 1**  
Input: `moves = "UD"`  
Output: `true`  
Explanation: 机器人先向上移动一次，然后向下移动一次。由于每次移动幅度相同，它回到了起始的原点，因此返回 `true`。

**示例 2**  
Input: `moves = "LL"`  
Output: `false`  
Explanation: 机器人向左移动了两次，最终位于原点左侧两个单位的位置。因为结束时不在原点，返回 `false`。

**约束条件**  

- $1 \leq \text{moves.length} \leq 2 \times 10^4$
- `moves` 只包含字符 `'U'`, `'D'`, `'L'` 和 `'R'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是“照搬”机器人的每一步运动：  
1. 先在平面上设定一个坐标 `(x, y)`，初始值都是 `0`（原点）。  
2. 按照字符串 `moves` 中的字符顺序依次更新坐标：  
   - `'R'` → `x += 1`（向右走一步）  
   - `'L'` → `x -= 1`（向左走一步）  
   - `'U'` → `y += 1`（向上走一步）  
   - `'D'` → `y -= 1`（向下走一步）  
3. 遍历完所有字符后，检查 `(x, y)` 是否仍然是 `(0, 0)`。如果是，说明机器人回到了原点，返回 `True`；否则返回 `False`。

> **数据结构类比**：这里的坐标 `(x, y)` 就像一本记事本，记录“机器人当前在第几行第几列”。每次移动就往记事本里写一笔，最后看记事本上写的是否回到了原点。

> **为什么正确**：因为每一步都严格按照题目规定的方向移动，且每一步的距离相同，累计的位移必然等于所有方向的向量和。若最终向量和为 `(0,0)`，则必然回到起点。

> **复杂度直观解释**：  
> - 时间复杂度 `O(n)`：我们要看 `moves` 中每个字符一次，`n` 是字符串长度。想象成排队买票，大家都得轮到一次。  
> - 空间复杂度 `O(1)`：只用到两个整数 `x、y`，不随输入大小增长，像是口袋里只装了一支笔。

#### 代码（Python）

```python
def judgeCircle(moves: str) -> bool:
    # 记录机器人当前位置，初始在原点 (0, 0)
    x, y = 0, 0

    # 逐字符遍历 moves
    for ch in moves:
        if ch == 'R':          # 向右走一步
            x += 1
        elif ch == 'L':        # 向左走一步
            x -= 1
        elif ch == 'U':        # 向上走一步
            y += 1
        elif ch == 'D':        # 向下走一步
            y -= 1
        # 这里不需要 else，因为题目保证字符一定合法

    # 判断是否回到原点
    return x == 0 and y == 0
```

#### 复杂度

- **时间复杂度**：`O(n)` — `n` 为 `moves` 的长度，需要遍历一次。
- **空间复杂度**：`O(1)` — 只使用了常数个整数变量。

---

### 2. 最优解

#### 思路  
暴力解已经是 `O(n)` 的线性遍历，已经是最优的时间复杂度了。  
不过我们可以把 **“每一步都更新坐标”** 换成 **“统计每种方向出现的次数”**，再比较相反方向的计数是否相等：

- 向右的次数要和向左的次数相同，才能在水平方向上回到原点。  
- 向上的次数要和向下的次数相同，才能在垂直方向上回到原点。

实现上有两种常见方式：

1. **计数器（Counter）**：利用 Python 标准库 `collections.Counter` 把字符出现次数统计出来。  
2. **手动计数**：用四个整数分别计数 `R、L、U、D`，代码更直白且不依赖额外库。

这里采用手动计数，思路更容易让初学者抓住“计数平衡”的本质。

> **核心技巧——计数平衡**：把“走路”抽象成“左走几步、右走几步”。只要两边相等，就相当于互相抵消，最终不偏离原点。

> **类比**：想象你在天平上称东西，左边放 `L` 重，右边放 `R` 重；只要两边重量相等，天平就保持平衡；同理，`U` 与 `D` 也是一对平衡砝码。

#### 代码（Python）

```python
def judgeCircle(moves: str) -> bool:
    # 四个计数器，分别统计四个方向出现的次数
    cnt_R = cnt_L = cnt_U = cnt_D = 0

    for ch in moves:
        if ch == 'R':
            cnt_R += 1
        elif ch == 'L':
            cnt_L += 1
        elif ch == 'U':
            cnt_U += 1
        else:               # ch == 'D'，因为题目保证合法，这里直接用 else
            cnt_D += 1

    # 水平相等且垂直相等，即回到原点
    return cnt_R == cnt_L and cnt_U == cnt_D
```

#### 复杂度

- **时间复杂度**：`O(n)` — 仍然只遍历一次字符串，和暴力解一样快。  
- **空间复杂度**：`O(1)` — 只用了四个整数计数器，常数级空间。

> 与暴力解的对比：时间相同，代码更简洁，思路更“数学化”。在实际面试里，这种计数方式更容易让人一眼看出“水平相抵、垂直相抵”的核心判断。

---

## 心得

- **核心技巧**：方向计数平衡（或向量求和）。只要相反方向出现次数相等，机器人必回到原点。  
- **适用的题型**：  
  1. 判断字符串中括号是否配对（计数平衡的思想延伸）。  
  2. 判断数组中正负数是否可以相互抵消（如 “平衡数组”）。  
  3. 判断股票买卖是否盈亏为零（买入次数 = 卖出次数）。  
- **一句话总结**：**“相反的步数抵消，计数相等即回原点”。**

---

## 反思

- **第一反应**：直接把机器人放在坐标系里，模拟每一步的移动。  
- **最容易踩的坑**：  
  - 忽略了字符只能是 `'U','D','L','R'`，导致写了多余的 `else` 检查。  
  - 没考虑空字符串的情况（虽然约束里最短是 1，但写通用代码时要防止空输入）。  
  - 在计数实现时，把 `U` 与 `D`、`L` 与 `R` 搞混，导致比较方向错误。  
- **下次同类题的第一步**：先把“相反操作”配对成一组，思考它们是否可以相互抵消；如果可以，用计数或求和的方式直接判断平衡即可。