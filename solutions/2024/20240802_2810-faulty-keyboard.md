# #2810. **故障键盘** / Faulty Keyboard

> 难度：简单 · 标签：String、Simulation · [LeetCode 链接](https://leetcode.com/problems/faulty-keyboard/)

---

## 题目（英文原版）

**Description**

Your laptop keyboard is faulty, and whenever you type a character 'i' on it, it reverses the string that you have written. Typing other characters works as expected.
You are given a 0-indexed string s, and you type each character of s using your faulty keyboard.
Return the final string that will be present on your laptop screen.

**Examples**

**Example 1:**

```
Input: s = "string"
Output: "rtsng"
Explanation: 
After typing first character, the text on the screen is "s".
After the second character, the text is "st". 
After the third character, the text is "str".
Since the fourth character is an 'i', the text gets reversed and becomes "rts".
After the fifth character, the text is "rtsn". 
After the sixth character, the text is "rtsng". 
Therefore, we return "rtsng".
```

**Example 2:**

```
Input: s = "poiinter"
Output: "ponter"
Explanation: 
After the first character, the text on the screen is "p".
After the second character, the text is "po". 
Since the third character you type is an 'i', the text gets reversed and becomes "op". 
Since the fourth character you type is an 'i', the text gets reversed and becomes "po".
After the fifth character, the text is "pon".
After the sixth character, the text is "pont". 
After the seventh character, the text is "ponte". 
After the eighth character, the text is "ponter". 
Therefore, we return "ponter".
```

**Constraints**

- 1 <= s.length <= 100
- s consists of lowercase English letters.
- s[0] != 'i'

---

## 题目（中文翻译）

Your laptop keyboard is faulty, and whenever you type a character `'i'` on it, it reverses the string that you have written. Typing other characters works as expected.  
You are given a 0-indexed string `s`, and you type each character of `s` using your faulty keyboard.  
Return the final string that will be present on your laptop screen.

**示例 1**

```
Input: s = "string"
Output: "rtsng"
```

**解释**  
- 输入第一个字符后，屏幕上的文字为 `"s"`。  
- 输入第二个字符后，文字为 `"st"`。  
- 输入第三个字符后，文字为 `"str"`。  
- 第四个字符是 `'i'`，此时文字整体反转，变为 `"rts"`。  
- 输入第五个字符后，文字为 `"rtsn"`。  
- 输入第六个字符后，文字为 `"rtsng"`。  
因此返回 `"rtsng"`。

**示例 2**

```
Input: s = "poiinter"
Output: "ponter"
```

**解释**  
- 输入第一个字符后，屏幕上的文字为 `"p"`。  
- 输入第二个字符后，文字为 `"po"`。  
- 第三个字符是 `'i'`，文字反转为 `"op"`。  
- 第四个字符又是 `'i'`，文字再次反转回 `"po"`。  
- 输入第五个字符后，文字为 `"pon"`。  
- 继续输入后得到最终结果 `"ponter"`。  

**约束条件**

- `1 <= s.length <= 100`
- `s` 仅由小写英文字母组成。
- `s[0] != 'i'`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把键盘的每一次按键都 **真实地模拟** 一遍：

1. 从左到右遍历输入字符串 `s` 的每个字符。  
2. 维护一个普通的 Python `list`（或 `str`），把它当作“屏幕上的文字”。  
3. 遇到普通字符（除 `'i'` 之外），直接把它 **追加** 到文字的末尾。  
4. 遇到字符 `'i'`，按照题意把当前文字 **整体翻转**（相当于把 `list[::-1]`）。  

> 类比：`list` 就像一本笔记本，往里写字相当于 `append`，把整本笔记本翻面相当于 `reverse`。  

这种做法一定能得到正确答案，因为我们一步步复制了题目描述的“每敲一个字符，键盘就会做对应的处理”。

#### 代码（Python）

```python
def finalString_bruteforce(s: str) -> str:
    # 用 list 来存储当前屏幕上的字符，list 拼接和翻转都很方便
    screen = []                       # 初始屏幕为空

    for ch in s:                      # 逐个遍历输入的字符
        if ch == 'i':                 # 如果是 'i'，把已有字符全部翻转
            screen.reverse()         # list.reverse() 就地翻转，类似把笔记本翻面
        else:                         # 普通字符直接写到屏幕末尾
            screen.append(ch)        # 相当于在笔记本的最后一页写字

    return ''.join(screen)            # 把列表合并成字符串返回
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 每次遇到 `'i'` 都要把已有的字符全部翻转。最坏情况下，`'i'` 可能出现 `O(n)` 次，每次翻转的长度平均是 `O(n/2)`，于是总操作数约为 `n * n/2 = O(n²)`。  
  - 用“大白话”说，就是当字符串很长且 `'i'` 很多时，程序会不停地把已经写好的文字倒过来，工作量会呈平方增长。

- **空间复杂度**：`O(n)`  
  - 需要额外的列表来保存最终的字符，最多保存 `n` 个字符。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次 `'i'` 都要完整翻转**，这导致重复的工作。  
我们可以把“翻转”这件事 **延迟**，只记录当前文字的 **阅读方向**：

1. 维护一个 **双端队列**（`collections.deque`），它支持在两端 **高效地** 插入字符。  
2. 用一个布尔变量 `rev` 表示当前的阅读方向  
   - `rev = False`：正常顺序，从左到右写入（`append` 到右端）。  
   - `rev = True`：文字被翻转了，此时新字符实际上应该写在 **左端**（`appendleft`）。  
3. 遍历字符串 `s`  
   - 若字符是 `'i'`，只需要把 `rev` 取反（`rev = not rev`），不必真的翻转整个队列。  
   - 否则，根据 `rev` 的值决定是 `append` 还是 `appendleft`。  
4. 遍历结束后，如果 `rev` 为 `True`，说明整体仍然是“倒着”的，需要再把队列整体翻转一次（这一步只做一次，`O(n)`）。  

> 类比：想象我们有一根可伸缩的绳子，两端都有可以写字的笔。  
> 正常情况下我们从右端写字（`append`），一旦键盘说“翻转”，我们把绳子翻过去，接下来就改用左端写字（`appendleft`），而不必把已经写好的字倒回去。

#### 代码（Python）

```python
from collections import deque

def finalString_optimal(s: str) -> str:
    dq = deque()          # 双端队列，支持两端高效插入
    rev = False           # 记录当前文字是否被翻转

    for ch in s:
        if ch == 'i':
            rev = not rev            # 碰到 'i'，只改变方向标记
        else:
            if rev:
                # 已经翻转，新的字符应写在左侧（相当于倒序）
                dq.appendleft(ch)
            else:
                # 正常方向，写在右侧
                dq.append(ch)

    # 如果最终仍是倒置状态，需要把队列整体翻转一次
    if rev:
        dq.reverse()                 # deque.reverse() 是 O(n) 的一次性翻转

    # 把 deque 中的字符拼成字符串返回
    return ''.join(dq)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个字符只做 **一次** 插入操作（`append` 或 `appendleft`），都是 `O(1)`。  
  - 最多只在最后一次整体翻转时遍历一次队列，仍然是线性 `O(n)`。  
  - 与暴力解相比，去掉了大量重复翻转的开销。

- **空间复杂度**：`O(n)`  
  - 仍需要存放全部字符的队列，大小随输入长度线性增长。

---

## 心得

- 这道题的核心技巧是 **“懒翻转 + 双端队列”**，即把**翻转操作延迟**，只用一个方向标记来决定插入位置。  
- 该技巧常用于需要频繁“反转”或“切换顺序”的字符串/数组模拟题，例如  
  1. **LeetCode 2814. Minimum Possible Integer After at Most K Swaps**（使用双端队列模拟前后插入）  
  2. **LeetCode 2037. Minimum Number of Moves to Seat Everyone**（方向标记 + 双指针）  
- **解题钥匙**：遇到“每次出现某个字符就要整体翻转”，先想 **“只记录方向，不真的翻转”**。

---

## 反思

- **第一反应**：直接把每次 `'i'` 都翻转，写出最直观的模拟代码。  
- **最容易踩的坑**：  
  - 忘记题目保证 `s[0] != 'i'`，但仍要防止首字符是 `'i'` 时的特殊处理。  
  - 在最优解中，忘记在遍历结束后根据 `rev` 再做一次整体翻转，导致输出顺序错误。  
- **下次类似题的第一步**：先判断“是否可以把昂贵的操作（如翻转、排序）延迟或用标记代替”，再决定是否需要使用 **双端队列、栈、或方向指针** 来实现 O(1) 的局部操作。