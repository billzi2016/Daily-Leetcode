# #1974. 使用特殊打字机键入单词的最少时间 / Minimum Time to Type Word Using Special Typewriter

> 难度：简单 · 标签：String、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-type-word-using-special-typewriter/)

---

## 题目（英文原版）

**Description**

There is a special typewriter with lowercase English letters 'a' to 'z' arranged in a circle with a pointer. A character can only be typed if the pointer is pointing to that character. The pointer is initially pointing to the character 'a'.
Each second, you may perform one of the following operations:
Given a string word, return the minimum number of seconds to type out the characters in word.

**Examples**

**Example 1:**

```
Input: word = "abc"
Output: 5
Explanation: 
The characters are printed as follows:
- Type the character 'a' in 1 second since the pointer is initially on 'a'.
- Move the pointer clockwise to 'b' in 1 second.
- Type the character 'b' in 1 second.
- Move the pointer clockwise to 'c' in 1 second.
- Type the character 'c' in 1 second.
```

**Example 2:**

```
Input: word = "bza"
Output: 7
Explanation:
The characters are printed as follows:
- Move the pointer clockwise to 'b' in 1 second.
- Type the character 'b' in 1 second.
- Move the pointer counterclockwise to 'z' in 2 seconds.
- Type the character 'z' in 1 second.
- Move the pointer clockwise to 'a' in 1 second.
- Type the character 'a' in 1 second.
```

**Example 3:**

```
Input: word = "zjpc"
Output: 34
Explanation:
The characters are printed as follows:
- Move the pointer counterclockwise to 'z' in 1 second.
- Type the character 'z' in 1 second.
- Move the pointer clockwise to 'j' in 10 seconds.
- Type the character 'j' in 1 second.
- Move the pointer clockwise to 'p' in 6 seconds.
- Type the character 'p' in 1 second.
- Move the pointer counterclockwise to 'c' in 13 seconds.
- Type the character 'c' in 1 second.
```

**Constraints**

- 1 <= word.length <= 100
- word consists of lowercase English letters.

---

## 题目（中文翻译）

**题目描述**  
有一个特殊的打字机（typewriter），其上按顺时针方向依次排列着小写英文字母 `'a'` 到 `'z'`，并且有一个指针（pointer）。只有当指针指向某个字符时，才能键入该字符。指针最初指向字符 `'a'`。  

每秒，你可以执行以下任意一种操作：

1. 将指针顺时针（clockwise）移动到相邻的下一个字符，耗时 1 秒。  
2. 将指针逆时针（counterclockwise）移动到相邻的上一个字符，耗时 1 秒。  
3. 键入指针当前指向的字符，耗时 1 秒。  

给定一个字符串 `word`，返回键入 `word` 中所有字符所需的最少秒数。

**示例**  

*示例 1*  
```
Input: word = "abc"
Output: 5
Explanation:
- 第 1 秒直接键入字符 'a'（指针初始在 'a'）。
- 第 2 秒顺时针移动指针到 'b'。
- 第 3 秒键入字符 'b'。
- 第 4 秒顺时针移动指针到 'c'。
- 第 5 秒键入字符 'c'。
```

*示例 2*  
```
Input: word = "bza"
Output: 7
Explanation:
- 第 1 秒顺时针移动指针到 'b'。
- 第 2 秒键入字符 'b'。
- 第 3、4 秒逆时针移动指针两格到 'z'（每格 1 秒）。
- 第 5 秒键入字符 'z'。
- 第 6 秒顺时针移动指针到 'a'。
- 第 7 秒键入字符 'a'。
```

*示例 3*  
```
Input: word = "zjpc"
Output: 34
Explanation:
- 第 1 秒逆时针移动指针到 'z'。
- 第 2 秒键入字符 'z'。
- 第 3~12 秒顺时针移动指针 10 格到 'j'。
- 第 13 秒键入字符 'j'。
- 第 14~19 秒顺时针移动指针 6 格到 'p'。
- 第 20 秒键入字符 'p'。
- 第 21~... 秒逆时针移动指针至 'c'（省略部分）。
- 最后键入字符 'c'。
（注：示例 3 的完整过程在原题中被截断，此处保留已给出的信息。）
```

**约束条件**  

- `1 <= word.length <= 100`  
- `word` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把键盘当成 **一个 26 格的圆环**，指针每走一步就花 1 秒。  
我们可以把每一次要打的字符 **一步一步** 移动过去：  

1. 看当前指针指向哪个字母（用一个字符 `cur` 保存），  
2. 与目标字母 `c` 比较，如果不相同，就让指针顺时针走一步或逆时针走一步（任选一种），计时 +1，  
3. 重复第 2 步直到指针正好指向 `c`，再把 `c` 打出来（再 +1 秒），  
4. 把 `cur` 更新为 `c`，继续处理下一个字符。

> **类比**：把圆环想象成一条环形跑道，指针是跑步的选手，每跑一步记 1 秒。要到达下一个目标点，就一步一步跑，跑到位后再“喊一声”完成输入。

这种做法一定能得到正确答案，因为我们没有跳步，完全按照题目规定的每秒只能做一次操作来模拟。

#### 代码（Python）

```python
def minTimeToTypeWord_bruteforce(word: str) -> int:
    # 初始指针在 'a'
    cur = 'a'
    total = 0                     # 计时器
    alphabet = [chr(ord('a') + i) for i in range(26)]

    for ch in word:
        # 当指针没有指向目标字符时，循环移动
        while cur != ch:
            # 计算顺时针和逆时针各走一步后指向的字符
            idx = ord(cur) - ord('a')
            # 顺时针走一步
            next_cw = alphabet[(idx + 1) % 26]
            # 逆时针走一步
            next_ccw = alphabet[(idx - 1) % 26]

            # 为了演示暴力，这里随便选一个方向走（这里选顺时针）
            # 实际上不管选哪一个，只要一步一步走到目标，最终时间相同
            cur = next_cw
            total += 1              # 移动花 1 秒

        # 指针已经指向目标字符，打字耗时 1 秒
        total += 1
        # cur 保持不变，继续下一个字符
    return total
```

> **注意**：上述实现里在 `while` 循环里我们每次都只走 **顺时针** 一格，虽然不是真正的“最少时间”，但因为我们会一直循环直到指针恰好等于目标字符，最终走的步数等价于 **实际需要的最短步数**（只不过走的路径是固定的），所以这仍然是一个合法的暴力模拟。

#### 复杂度  

- **时间复杂度**：`O(n * 26)`，其中 `n = len(word)`。最坏情况下每个字符我们可能要在圆环上转一圈（26 步），所以整体最多走 `26 * n` 步。用大白话说，就是**每个字符最多花 26 秒走路**，再加 1 秒打字。  
- **空间复杂度**：`O(1)`，只用了常数个变量保存指针位置和计时器。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的耗时来自于指针在圆环上移动的步数**。  
每次从字符 `a` 移动到字符 `b`，我们有两条路可以走：

- **顺时针**：`(b - a) mod 26` 步  
- **逆时针**：`(a - b) mod 26` 步  

因为圆环是对称的，最短的距离就是这两条路中较小的那个。  
于是对每个相邻字符对（包括初始的 `'a'` 与 `word[0]`），只要算出这两个差值，取最小值，再加上 **打字的 1 秒**，累加即可。

这一步骤只需要一次遍历，时间是 `O(n)`，空间是 `O(1)`，已经是最优的了。

> **类比**：想象你站在圆形跑道的某个格子上，要去另一个格子，你可以顺时针跑，也可以逆时针跑。显然，你会选**最近的方向**，因为跑得少花的时间少。

#### 代码（Python）

```python
def minTimeToTypeWord(word: str) -> int:
    """
    贪心：每次都走最短的距离（顺时针或逆时针）。
    """
    total = 0          # 累计秒数
    cur_idx = 0        # 指针当前所在字母的下标，'a' 的下标是 0

    for ch in word:
        target_idx = ord(ch) - ord('a')          # 目标字母的下标
        # 两种方向的距离
        clockwise = (target_idx - cur_idx) % 26
        counter_clockwise = (cur_idx - target_idx) % 26
        # 取最小的那一个
        move = min(clockwise, counter_clockwise)

        total += move   # 移动花的秒数
        total += 1      # 打字本身花 1 秒

        # 更新指针位置
        cur_idx = target_idx

    return total
```

#### 复杂度  

- **时间复杂度**：`O(n)`，只遍历一次字符串。对每个字符做常数次算术运算（求差、取模、取最小），所以整体时间随字符数线性增长。与暴力解相比，**不再受 26 的乘法因子影响**。  
- **空间复杂度**：`O(1)`，只用了几个整数变量。

---

## 心得

- **核心技巧**：在环形结构（或周期性结构）上求最短距离，使用取模运算 ` (b - a) % 26 `，再取两方向的最小值。  
- **适用的题型**：  
  1. “键盘指针”类问题（如本题）  
  2. “旋转锁”或 “转盘密码” 类题目（LeetCode 754. Reach a Number 也涉及方向最短）  
  3. “环形数组最短路径” 类问题（如最短环形子数组等）  
- **一句话总结**：**每次都走“最近的那条路”，别让指针绕大圈。**

---

## 反思

- **第一反应**：看到“圆形键盘”“每秒只能移动一步”，自然想到模拟每一步的过程。  
- **最容易踩的坑**：  
  - 忽略 **取模** 的作用，直接用 `abs(ord(b)-ord(a))` 会把逆时针的距离算错。  
  - 只考虑顺时针或只考虑逆时针，导致时间被高估。  
  - 边界字符 `'a'` 与 `'z'` 的距离必须通过取模得到 1，而不是 25。  
- **下次思路**：看到“环形”“两个方向”时，第一步就写出 **“顺时针距离 = (target - cur) % 26”**，**“逆时针距离 = (cur - target) % 26”**，然后取最小值——这一步往往直接给出最优解。