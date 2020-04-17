# #838. **推倒多米诺骨牌** / Push Dominoes

> 难度：中等 · 标签：Two Pointers、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/push-dominoes/)

---

## 题目（英文原版）

**Description**

There are n dominoes in a line, and we place each domino vertically upright. In the beginning, we simultaneously push some of the dominoes either to the left or to the right.
After each second, each domino that is falling to the left pushes the adjacent domino on the left. Similarly, the dominoes falling to the right push their adjacent dominoes standing on the right.
When a vertical domino has dominoes falling on it from both sides, it stays still due to the balance of the forces.
For the purposes of this question, we will consider that a falling domino expends no additional force to a falling or already fallen domino.
You are given a string dominoes representing the initial state where:
Return a string representing the final state.

**Examples**

**Example 1:**

```
Input: dominoes = "RR.L"
Output: "RR.L"
Explanation: The first domino expends no additional force on the second domino.
```

**Example 2:**

```
Input: dominoes = ".L.R...LR..L.."
Output: "LL.RR.LLRRLL.."
```

**Constraints**

- n == dominoes.length
- 1 <= n <= 105
- dominoes[i] is either 'L', 'R', or '.'.

---

## 题目（中文翻译）

有 n 个多米诺骨牌排成一条直线，最初每个骨牌都是竖直立着的。我们会同时将其中若干骨牌向左或向右推倒。  

每秒钟，向左倒下的骨牌会把左侧相邻的骨牌也向左推倒；同理，向右倒下的骨牌会把右侧相邻的骨牌向右推倒。  
当一块竖直的骨牌同时受到左右两侧骨牌的推力时，由于受力平衡，它保持不动。  

在本题中，已经倒下的骨牌对已经倒下或正在倒下的骨牌 **不再产生额外的推力**（即不叠加力）。  

给定一个字符串 `dominoes` 表示初始状态，其中 `dominoes[i]` 为 `'L'`（向左倒）、`'R'`（向右倒）或 `'.'`（竖直未受力），请返回表示最终状态的字符串。

### 示例

**示例 1**  
```
Input: dominoes = "RR.L"
Output: "RR.L"
Explanation: 第一个向右倒的骨牌对第二个骨牌不产生额外的推力。
```

**示例 2**  
```
Input: dominoes = ".L.R...LR..L.."
Output: "LL.RR.LLRRLL.."
```

### 约束条件

- `n == dominoes.length`
- `1 <= n <= 10^5`
- `dominoes[i]` 只能是 `'L'`、`'R'` 或 `'.'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **一步步模拟时间的流逝**：  

1. 把输入的字符串看成一排多米诺骨牌，每个字符可能是  
   * `'L'` – 已经向左倒下的骨牌  
   * `'R'` – 已经向右倒下的骨牌  
   * `'.'` – 仍然竖立的骨牌  
2. 每一次“秒”同时检查所有竖立的骨牌（`'.'`），看它左边是否有正在向右倒的骨牌，右边是否有正在向左倒的骨牌。  
   * 只受到左侧 `R` 的推力 → 本秒它会倒向右，记为 `'R'`。  
   * 只受到右侧 `L` 的推力 → 本秒它会倒向左，记为 `'L'`。  
   * 同时受到两侧推力 → 两股力相互抵消，它保持竖立（仍是 `'.'`）。  
3. 把所有在本秒产生变化的骨牌一次性更新后，进入下一秒。  
4. 当一整轮遍历后 **没有任何骨牌再发生变化**，说明已经达到最终稳定状态，返回当前字符串。

> **类比**：这跟在街道上观察行人相互推挤的过程很像。我们每秒钟“拍一张照”，记录谁被哪边的行人推倒，然后把结果写进下一张照里，直到再也没有人被推倒为止。

这个方法之所以一定能得到正确答案，是因为题目本身就是让我们“每秒钟所有倒下的骨牌同时推动相邻竖立骨牌”。只要严格按照“同步更新”来模拟，就不会错过任何一次可能的倒塌。

#### 代码（Python）

```python
def pushDominoes_bruteforce(dominoes: str) -> str:
    # 把字符串转成列表，方便原地修改
    arr = list(dominoes)
    n = len(arr)

    while True:                     # 不断循环直到没有变化
        changed = False             # 本轮是否有骨牌倒下
        # 记录本轮每个位置受到的力量：-1 表示左推，+1 表示右推，0 表示不受力
        force = [0] * n

        # 先遍历一次，统计每个竖立骨牌左右两侧的力量来源
        for i, ch in enumerate(arr):
            if ch == 'L':           # 向左倒的骨牌会向左推它左边的竖立骨牌
                if i > 0 and arr[i - 1] == '.':
                    force[i - 1] -= 1
            elif ch == 'R':         # 向右倒的骨牌会向右推它右边的竖立骨牌
                if i + 1 < n and arr[i + 1] == '.':
                    force[i + 1] += 1

        # 根据统计的力量一次性更新
        for i in range(n):
            if arr[i] == '.' and force[i] != 0:
                if force[i] > 0:    # 只受到右侧推力
                    arr[i] = 'R'
                elif force[i] < 0:  # 只受到左侧推力
                    arr[i] = 'L'
                # 同时受到左右推力时 force[i] == 0，保持不变
                changed = True

        if not changed:            # 本轮没有任何变化，结束循环
            break

    return ''.join(arr)
```

> **关键点**：  
> - **同步更新**：先把本秒所有受力记录在 `force` 数组里，等全部统计完再统一改写 `arr`，避免“一边改写一边读取”导致错误。  
> - `changed` 用来判断是否进入下一秒；若一次循环后没有任何骨牌倒下，说明已经稳定。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 最坏情况下（比如全部是 `'.'`，中间只有一个 `'R'`），每秒只能让最左侧的一个 `'.'` 倒下，需进行 `n` 次循环；每次循环遍历全部 `n` 个位置 → `n × n`。  
  - 用大白话说，就是“每次只能前进一步，最终要走 `n` 步，每步都要检查 `n` 次”。  
- **空间复杂度**：`O(n)`  
  - 需要额外的 `force` 数组和字符列表 `arr`，长度均为 `n`。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每秒只让极少数骨牌改变**，导致要重复遍历整条字符串很多次。  
要把时间压到 `O(n)`，我们必须 **一次遍历就把每个位置的最终受力算出来**。  

下面给出两种等价的 “一次遍历” 思路，任选其一都能得到 `O(n)`：

1. **力的衰减模型（前缀力 + 后缀力）**  
   - 把每个向右倒的 `'R'` 看成在它左侧产生的正向力量 `+N`（`N` 足够大），每往右移动一步，力量减 `1`（因为距离远了，推力弱了）。  
   - 同理，向左倒的 `'L'` 在它右侧产生负向力量 `-N`，往左移动时力量增 `1`（负数的绝对值变小）。  
   - 第一次从左到右遍历，累加所有右推力得到 **左→右的力数组 `forces`**。  
   - 第二次从右到左遍历，累加所有左推力并 **直接加到 `forces` 上**（因为左推力是负的）。  
   - 最终，`forces[i] > 0` → 最终向右倒 `'R'`；`forces[i] < 0` → 向左倒 `'L'`；`forces[i] == 0` → 仍竖立 `'.'`。  

2. **双指针分段处理**（更直观的“区间”思路）  
   - 把字符串视作若干段，每段的左右端点一定是 `'L'`、`'R'` 或虚拟的边界 `'#'`（相当于无穷远的 `'L'` 或 `'R'`）。  
   - 对每两个相邻非 `'.'` 的字符之间的 `'.'` 区间进行分析：  
     * `R ... R` → 全部变成 `'R'`（右推力一直向右）。  
     * `L ... L` → 全部变成 `'L'`。  
     * `R ... L` → 中间向右的骨牌向右倒，向左的骨牌向左倒，距离中心点相等的骨牌保持 `'.'`（因为两股力相抵）。  
     * `L ... R` → 两股力相背离，区间保持不变（所有 `'.'` 仍是 `'.'`）。  
   - 只需一次遍历收集所有非 `'.'` 的位置，用指针把相邻两者之间的区间按上述规则填充。

下面我们实现 **力的衰减模型**，因为它只需要两次线性遍历，代码更简洁，且易于解释“力的正负”。

#### 代码（Python）

```python
def pushDominoes(dominoes: str) -> str:
    n = len(dominoes)
    forces = [0] * n          # 正数表示向右的合力，负数表示向左的合力

    # ---------- 第一次遍历：从左到右累加右推力 ----------
    # 初始力量取一个足够大的正数（> n），确保左侧的 'R' 能覆盖全部右侧
    force = 0
    for i in range(n):
        if dominoes[i] == 'R':
            force = n          # 重新注入一个强大的右推力
        elif dominoes[i] == 'L':
            force = 0          # 左推力会抵消右推力，右侧不再受右推力影响
        else:                   # dominoes[i] == '.'
            force = max(force - 1, 0)   # 力量随距离衰减，最小不能为负
        forces[i] += force      # 把当前右推力累加到 forces

    # ---------- 第二次遍历：从右到左累加左推力 ----------
    force = 0
    for i in range(n - 1, -1, -1):
        if dominoes[i] == 'L':
            force = n          # 注入一个强大的左推力（记为负数）
        elif dominoes[i] == 'R':
            force = 0          # 右推力会抵消左推力，左侧不再受左推力影响
        else:                   # '.'
            force = max(force - 1, 0)   # 同样随距离衰减
        forces[i] -= force      # 左推力是负的，用减法累加

    # ---------- 根据合力决定最终状态 ----------
    result = []
    for f in forces:
        if f > 0:
            result.append('R')
        elif f < 0:
            result.append('L')
        else:
            result.append('.')
    return ''.join(result)
```

**代码要点解释**  

| 行号 | 关键行 | 中文注释 |
|------|--------|----------|
| 7‑12 | `for i in range(n): …` | 从左往右遍历，遇到 `'R'` 时把 **强大的右推力** 设为 `n`（大于最长可能距离），随后每往右走一步，推力衰减 `1`，衰减到 `0` 为止。 |
| 13‑14| `forces[i] += force` | 把当前右推力累加到 `forces[i]`，后面会再加上左推力的影响。 |
| 18‑23| `for i in range(n-1, -1, -1): …` | 从右往左遍历，逻辑与左→右相同，只是把 **左推力** 记为正数后在 `forces[i]` 上 **减去**，实现负方向的合力。 |
| 27‑34| `if f > 0 … elif f < 0 … else …` | 合力大于零 → 右倒，大于零的绝对值越大说明右侧推力更强；小于零 → 左倒；等于零 → 两股力相抵或本来就没有推力，保持竖立。 |

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只进行两次线性遍历（左→右、右→左）以及一次遍历生成结果。相比暴力解的 `O(n²)`，我们“一次走完所有路”。  
- **空间复杂度**：`O(n)`  
  - 需要额外的 `forces` 数组存放每个位置的合力，长度为 `n`。如果把原字符串转成列表再原地写回，也仍然是 `O(n)`（因为字符串本身已经占用 `n` 空间）。

---

## 心得

- **核心技巧**：把“每秒的推动”抽象为 **力的叠加**（正负数），利用 **线性衰减** 的思想一次性算出每个位置的最终合力。  
- **适用的题型**  
  1. **Push Dominoes**（本题）——力的正负叠加。  
  2. **Asteroid Collision**（LeetCode 735）——使用栈模拟相向运动的“碰撞”。  
  3. **Shortest Distance to a Character**（LeetCode 821）——双向遍历求最小距离，同样是左→右、右→左的“力”合并。  
- **一句话总结**：**把动态过程转化为一次性“力”累计，就能把模拟的时间压到线性**。

---

## 反思

- **第一反应**：看到“每秒同时推动”，立刻想到 **逐秒模拟**，于是写出了暴力解。  
- **最容易踩的坑**  
  1. **同步更新**：在模拟时必须先记录所有受力，再统一修改，否则会出现“本秒的变化影响同秒的其他骨牌”，导致错误。  
  2. **边界处理**：字符串最左/右端没有左/右邻居，需要在力衰减时防止越界。  
  3. **力的大小取值**：在最优解里把初始力量设为 `n`（或更大），确保它能覆盖最远的距离；如果设得太小，可能会提前衰减成 `0`，导致结果错误。  
- **下次类似题的第一步**：先问自己 **“这是不是可以用一次遍历把所有影响累计？”**，如果答案是“可以”，就尝试 **把局部的递推关系（如力衰减、距离递增）写成线性扫描**；否则再考虑使用栈或双指针等更复杂的结构。