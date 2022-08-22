# #1904. 你玩过的完整轮次 / The Number of Full Rounds You Have Played

> 难度：中等 · 标签：Math、String · [LeetCode 链接](https://leetcode.com/problems/the-number-of-full-rounds-you-have-played/)

---

## 题目（英文原版）

**Description**

You are participating in an online chess tournament. There is a chess round that starts every 15 minutes. The first round of the day starts at 00:00, and after every 15 minutes, a new round starts.
You are given two strings loginTime and logoutTime where:
If logoutTime is earlier than loginTime, this means you have played from loginTime to midnight and from midnight to logoutTime.
Return the number of full chess rounds you have played in the tournament.
Note: All the given times follow the 24-hour clock. That means the first round of the day starts at 00:00 and the last round of the day starts at 23:45.

**Examples**

**Example 1:**

```
Input: loginTime = "09:31", logoutTime = "10:14"
Output: 1
Explanation: You played one full round from 09:45 to 10:00.
You did not play the full round from 09:30 to 09:45 because you logged in at 09:31 after it began.
You did not play the full round from 10:00 to 10:15 because you logged out at 10:14 before it ended.
```

**Example 2:**

```
Input: loginTime = "21:30", logoutTime = "03:00"
Output: 22
Explanation: You played 10 full rounds from 21:30 to 00:00 and 12 full rounds from 00:00 to 03:00.
10 + 12 = 22.
```

**Constraints**

- loginTime and logoutTime are in the format hh:mm.
- 00 <= hh <= 23
- 00 <= mm <= 59
- loginTime and logoutTime are not equal.

---

## 题目（中文翻译）

你正在参加一场线上国际象棋锦标赛。每 **15 分钟** 会开始一轮新的对局（round）。当天的第一轮在 **00:00** 开始，之后每隔 **15 分钟** 就会有新的一轮开始。

给定两个字符串 `loginTime` 和 `logoutTime`，其中：

- 如果 `logoutTime` 早于 `loginTime`，则表示你从 `loginTime` 持续到午夜，然后从午夜继续到 `logoutTime`。

返回你在本次锦标赛中完整参与的对局（round）的数量。

> 注意：所有给出的时间均采用 24 小时制。这意味着当天的第一轮在 **00:00** 开始，最后一轮在 **23:45** 开始。

## 示例

### 示例 1

**输入**  
`loginTime = "09:31", logoutTime = "10:14"`

**输出**  
`1`

**解释**  
- 你完整参与了一轮，从 **09:45** 到 **10:00**。  
- 你没有完整参与 **09:30** 到 **09:45** 的这一轮，因为你在 **09:31** 才登录，错过了该轮的起始。  
- 你也没有完整参与 **10:00** 到 **10:15** 的这一轮，因为你在 **10:14** 就已退出，未能看到该轮结束。

### 示例 2

**输入**  
`loginTime = "21:30", logoutTime = "03:00"`

**输出**  
`22`

**解释**  
- 从 **21:30** 到 **00:00**，你完整参与了 **10** 轮。  
- 从 **00:00** 到 **03:00**，你完整参与了 **12** 轮。  
- 总计 `10 + 12 = 22` 轮。

## 约束条件

- `loginTime` 和 `logoutTime` 的格式为 `hh:mm`。  
- `00 <= hh <= 23`  
- `00 <= mm <= 59`  
- `loginTime` 与 `logoutTime` 不相等。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

我们先把一天划分成若干**完整的棋局**（每局 15 分钟）。  
- 00:00~00:15 为第一局，00:15~00:30 为第二局……一直到 23:45~24:00 为最后一局。  
- 这样一天一共有 `24 * 60 / 15 = 96` 局。

现在已知登录时间 `loginTime` 和登出时间 `logoutTime`（格式都是 `"hh:mm"`），如果登出时间在登录时间之前，说明跨过了午夜，需要把后半段算到第二天的时间线上。

**暴力做法**：  
1. 把 `loginTime`、`logoutTime` 都转成“从 00:00 开始的分钟数”。  
2. 如果 `logout < login`，则把 `logout` 加上 24 小时的分钟数（`1440`），相当于把时间线拉长到 48 小时。  
3. 逐个检查 96 局，每局的 **开始** 与 **结束** 是否都完全落在 `[login, logout]` 区间内。  
   - 只要局的开始时间 `>= login` **且** 结束时间 `<= logout`，这局就是完整的。  

> **类比**：把每局棋想成一本书的章节，登录时间是你打开书的时间，登出时间是合上的时间。只有章节的“起始页”和“结束页”都在你打开的时间段里，这章节才算完整阅读。

这种方法直接、容易理解，适合作为第一步。

#### 代码（Python）

```python
def time_to_min(t: str) -> int:
    """把 \"hh:mm\" 转成当天的分钟数，例如 \"09:31\" -> 9*60+31"""
    h, m = map(int, t.split(':'))
    return h * 60 + m


def fullRounds_bruteforce(loginTime: str, logoutTime: str) -> int:
    login = time_to_min(loginTime)
    logout = time_to_min(logoutTime)

    # 跨午夜的话，把 logout 往后推一天（1440 分钟）
    if logout < login:
        logout += 24 * 60

    full = 0
    # 00:00~24:00 之间每 15 分钟一局，共 96 局
    for start in range(0, 24 * 60, 15):          # 局的开始时间（分钟）
        end = start + 15                         # 局的结束时间（分钟）
        # 如果这局完全在登录区间内，就算一局完整的棋局
        if start >= login and end <= logout:
            full += 1
    return full
```

#### 复杂度  

- **时间复杂度**：`O(96)` → 实际上是常数时间，因为一天下 96 局，遍历一次即可。可以把它理解为“最多检查 100 次”，和输入大小无关。  
- **空间复杂度**：`O(1)` → 只用了几个整数变量，和输入规模不相关。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**逐局检查**，虽然本题常数很小，但我们仍可以把它压缩到 **一次算完**。  
关键在于找出：

1. **从登录时间开始的第一个完整局的起始时间**（向上取整到最近的 15 的倍数）。  
2. **在登出时间之前的最后一个完整局的结束时间**（向下取整到最近的 15 的倍数）。

只要这两个时间点之间的局数就能直接算出来：

```
局数 = (最后局结束时间 - 第一个局开始时间) / 15 + 1
```

如果第一个局的开始时间已经超过了最后局的结束时间，说明根本没有完整局，返回 0。

**如何取整**  
- 向上取整（ceil）：`ceil(x / 15) * 15` → 把 `x` 往后推到最近的 15 的倍数。  
- 向下取整（floor）：`floor(x / 15) * 15` → 把 `x` 往前拉到最近的 15 的倍数。  

因为登录时间和登出时间都是分钟数，直接使用整数除法即可。

跨午夜的情况同样用 “把登出时间加上一天” 来处理，这样所有比较都可以在同一条直线（0~2880 分钟）上完成。

> **类比**：把一天想成一条直尺，上面标记了每 15 分钟的刻度。你从 `login` 开始往右走，找到第一个刻度（完整局的起点），再找到最后一个刻度（完整局的终点），两者之间的刻度数就是完整局的数量。

#### 代码（Python）

```python
def time_to_min(t: str) -> int:
    """把 \"hh:mm\" 转成当天的分钟数"""
    h, m = map(int, t.split(':'))
    return h * 60 + m


def fullRounds_optimal(loginTime: str, logoutTime: str) -> int:
    login = time_to_min(loginTime)
    logout = time_to_min(logoutTime)

    # 跨午夜则把 logout 往后推一天（1440 分钟）
    if logout < login:
        logout += 24 * 60

    # 第一个完整局的开始时间：向上取整到最近的 15 的倍数
    #   (login + 14) // 15 先把 login 往上“凑满”15 再整除
    first_start = ((login + 14) // 15) * 15

    # 最后一个完整局的结束时间：向下取整到最近的 15 的倍数
    last_end = (logout // 15) * 15

    # 如果第一个局已经在最后一个局之后，说明没有完整局
    if first_start > last_end:
        return 0

    # 两者之间相差多少分钟，除以 15 再加 1 就是局数
    return (last_end - first_start) // 15 + 1
```

#### 复杂度  

- **时间复杂度**：`O(1)` → 只做了几次算术运算和比较，和输入长度完全无关。相比暴力的 `O(96)`，更快更省资源。  
- **空间复杂度**：`O(1)` → 只用了固定个数的整数变量。

---

## 心得  

- **核心技巧**：**向上/向下取整**（ceil & floor）配合 **时间线统一化**（跨午夜时把时间加上 24 小时）。  
- 这种技巧在所有**周期性事件**（每隔固定时间出现一次）的计数题里都很常用，例如：  
  1. 统计一天内多少个完整的 **工作时段**（比如每 30 分钟一次的会议）。  
  2. 计算 **闹钟** 或 **计时器** 在给定时间段内响了多少次。  
- **解题钥匙**：把“每隔固定长度的区间”看成**等差数列的刻度**，只要找到第一个合法刻度和最后一个合法刻度，数量就能直接算出来。

## 反思  

- **第一反应**：先把时间转成分钟，然后“逐局遍历”。这是一种直观且安全的做法。  
- **最容易踩的坑**：  
  - **跨午夜**：忘记把登出时间往后推一天，会导致计数错误。  
  - **取整细节**：登录时间恰好在局的开始时刻（例如 09:30）应该算作完整局的起点，需要使用向上取整的技巧 `+14 // 15`，否则会少算一局。  
  - **边界条件**：登录时间与登出时间相差不足 15 分钟时应该返回 0。  
- **下次类似题的第一步**：先把所有时间映射到 **统一的数轴**（分钟或秒），并用 **向上/向下取整** 把区间对齐到固定周期的刻度上。这样就可以在 O(1) 时间内得到答案。