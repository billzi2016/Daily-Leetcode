# #1472. 设计浏览器历史 / Design Browser History

> 难度：中等 · 标签：Array、Linked List、Stack、Design、Doubly-Linked List、Data Stream · [LeetCode 链接](https://leetcode.com/problems/design-browser-history/)

---

## 题目（英文原版）

**Description**

You have a browser of one tab where you start on the homepage and you can visit another url, get back in the history number of steps or move forward in the history number of steps.
Implement the BrowserHistory class:
Example:

**Examples**

**Example 1:**

```
Input:
["BrowserHistory","visit","visit","visit","back","back","forward","visit","forward","back","back"]
[["leetcode.com"],["google.com"],["facebook.com"],["youtube.com"],[1],[1],[1],["linkedin.com"],[2],[2],[7]]
Output:
[null,null,null,null,"facebook.com","google.com","facebook.com",null,"linkedin.com","google.com","leetcode.com"]

Explanation:
BrowserHistory browserHistory = new BrowserHistory("leetcode.com");
browserHistory.visit("google.com");       // You are in "leetcode.com". Visit "google.com"
browserHistory.visit("facebook.com");     // You are in "google.com". Visit "facebook.com"
browserHistory.visit("youtube.com");      // You are in "facebook.com". Visit "youtube.com"
browserHistory.back(1);                   // You are in "youtube.com", move back to "facebook.com" return "facebook.com"
browserHistory.back(1);                   // You are in "facebook.com", move back to "google.com" return "google.com"
browserHistory.forward(1);                // You are in "google.com", move forward to "facebook.com" return "facebook.com"
browserHistory.visit("linkedin.com");     // You are in "facebook.com". Visit "linkedin.com"
browserHistory.forward(2);                // You are in "linkedin.com", you cannot move forward any steps.
browserHistory.back(2);                   // You are in "linkedin.com", move back two steps to "facebook.com" then to "google.com". return "google.com"
browserHistory.back(7);                   // You are in "google.com", you can move back only one step to "leetcode.com". return "leetcode.com"
```

**Constraints**

- 1 <= homepage.length <= 20
- 1 <= url.length <= 20
- 1 <= steps <= 100
- homepage and url consist of  '.' or lower case English letters.
- At most 5000 calls will be made to visit, back, and forward.

---

## 题目（中文翻译）

**描述**  
你有一个只有一个标签页的浏览器，最初打开 `homepage`（首页），随后可以执行以下操作：

- `visit(url)`：访问一个新的 `url`（网址），此时会把当前页面之后的所有前进历史全部删除。
- `back(steps)`：在浏览历史中后退 `steps` 步，返回后退后所在的页面 URL。如果已经到达最早的页面，则停在最早的页面。
- `forward(steps)`：在浏览历史中前进 `steps` 步，返回前进后所在的页面 URL。如果已经到达最新的页面，则停在最新的页面。

请实现 `BrowserHistory` 类：

```java
class BrowserHistory {
    public BrowserHistory(String homepage) { ... }   // 初始化对象，当前页面为 homepage
    public void visit(String url) { ... }           // 访问 url
    public String back(int steps) { ... }           // 后退 steps 步，返回当前页面 URL
    public String forward(int steps) { ... }        // 前进 steps 步，返回当前页面 URL
}
```

**示例**  

```text
输入:
["BrowserHistory","visit","visit","visit","back","back","forward","visit","forward","back","back"]
[["leetcode.com"],["google.com"],["facebook.com"],["youtube.com"],[1],[1],[1],["linkedin.com"],[2],[2],[7]]
输出:
[null,null,null,null,"facebook.com","google.com","facebook.com",null,"linkedin.com","google.com","leetcode.com"]
```

**解释**  

```java
BrowserHistory browserHistory = new BrowserHistory("leetcode.com"); // 你在 "leetcode.com" 页面
browserHistory.visit("google.com");       // 访问 "google.com"
browserHistory.visit("facebook.com");     // 访问 "facebook.com"
browserHistory.visit("youtube.com");      // 访问 "youtube.com"
browserHistory.back(1);                   // 后退 1 步，返回 "facebook.com"
browserHistory.back(1);                   // 后退 1 步，返回 "google.com"
browserHistory.forward(1);                // 前进 1 步，返回 "facebook.com"
browserHistory.visit("linkedin.com");     // 访问 "linkedin.com"
browserHistory.forward(2);                // 前进 2 步，无法前进，仍停在 "linkedin.com"
browserHistory.back(2);                   // 后退 2 步，返回 "google.com"
browserHistory.back(7);                   // 后退 7 步，最多只能后退到 "leetcode.com"
```

**约束条件**  

- `1 <= homepage.length <= 20`
- `1 <= url.length <= 20`
- `1 <= steps <= 100`
- `homepage` 和 `url` 只包含 `'.'` 或小写英文字母。
- 最多会调用 `visit`、`back`、`forward` 共计 `5000` 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把浏览器的历史记录全部存到一个 **列表**（`list`）里。  
- 每次 `visit(url)` 时，把当前页面后面的所有记录都删掉（因为访问新页面会把“前进”历史清空），再把新 `url` 加到列表尾部。  
- `back(steps)` 时，只要把指针往左移动 `steps` 步（如果已经到最左边就停在最左），返回指针所在位置的页面。  
- `forward(steps)` 同理，指针往右移动。

这里的 **指针** 可以理解为「手指」指向列表中的某个位置，手指左边是“后退”历史，右边是“前进”历史。

> **为什么正确**  
> 浏览器的历史本质上就是一个线性序列，只要保证 `visit` 时把指针后面的内容全部抹掉，`back/forward` 只在指针所在的范围内移动，就能完整模拟浏览器的行为。

> **时间/空间复杂度大白话**  
> - 删除列表后面的元素在 Python 中是 **O(k)**（k 为被删元素的个数），最坏会是 **O(n)**，相当于把一本书的后半页全部撕掉。  
> - `back/forward` 只改动指针，是 **O(1)**，像是把手指向左或向右挪动一格，几乎不花时间。  
> - 整体空间是把所有访问过的页面都存下来，最多 **O(n)**，就像把每一页都放进抽屉里。

#### 代码（Python）

```python
class BrowserHistory:
    def __init__(self, homepage: str):
        # 用一个列表保存所有访问过的页面
        self.history = [homepage]      # 第 0 位是首页
        self.curr = 0                  # 指针指向当前页面（下标）

    def visit(self, url: str) -> None:
        # 访问新页面时，先把指针后面的历史全部删掉
        #   这里的切片操作会生成一个新列表，时间随被删元素数量线性增长
        self.history = self.history[:self.curr + 1]
        self.history.append(url)      # 把新页面加到末尾
        self.curr += 1                # 指针移到新页面

    def back(self, steps: int) -> str:
        # 往左走 steps 步，走不到头就停在最左边（下标 0）
        self.curr = max(0, self.curr - steps)
        return self.history[self.curr]

    def forward(self, steps: int) -> str:
        # 往右走 steps 步，走不到头就停在最右边（列表最后一个元素）
        self.curr = min(len(self.history) - 1, self.curr + steps)
        return self.history[self.curr]
```

#### 复杂度

- **时间复杂度**  
  - `visit`：最坏 **O(n)**（需要截断列表），因为要把指针后面的所有元素都删掉。  
  - `back` / `forward`：**O(1)**，只改动一个整数。  
- **空间复杂度**：**O(n)**，需要存储所有访问过的 URL。

---

### 2. 最优解

#### 思路  

从上面的暴力实现可以看到，**瓶颈**在于 `visit` 时要把后面的元素全部删除，这一步会产生 **O(n)** 的拷贝。  
实际上，我们并不需要真的把后面的元素从内存中移除，只要“忽略”它们即可。  

**核心思路**：使用 **双向链表**（或等价的数组+指针）来维护历史，每个节点保存一个 URL，并且有 `prev`、`next` 两个指针。  
- `visit(url)`：在当前节点后面新建一个节点，指向它；把原来的 `next` 链全部丢弃（不必遍历删除，只需要把指针置为 `None`）。  
- `back(steps)`：沿 `prev` 指针走 `steps` 步，走不到头就停在最左边。  
- `forward(steps)`：沿 `next` 指针走 `steps` 步，走不到头就停在最右边。

因为每次操作只涉及指针的重新指向或移动，**时间都是 O(1)**（不管历史有多长），空间只会随访问的页面数线性增长 **O(n)**。

如果不想自己实现链表，**数组 + 当前索引** 也可以达到同样的 O(1) 效果，只要在 `visit` 时把 `curr` 右侧的内容视为“无效”。这相当于在数组上做“懒删”。下面给出基于数组的实现，思路更易懂，且在 Python 中运行更快。

> **类比**：想象一本笔记本，指针是笔尖所在的页码。  
> - `visit` 就像在当前页后面撕掉后面的所有页，然后在新页上继续写。我们不必真的把后面的纸撕掉，只要把笔尖移动到新页并把“后面的页数”记为 0 即可。  
> - `back` / `forward` 就是把笔尖往左或往右翻页，翻几页都只需要一次动作。

#### 代码（Python）

```python
class BrowserHistory:
    def __init__(self, homepage: str):
        # 使用一个固定大小的列表保存所有访问过的页面（最多 5000 次操作）
        self.history = [homepage]      # 第 0 位保存首页
        self.curr = 0                  # 当前所在的下标
        self.last = 0                  # 已经真正存在的最右边下标（有效历史的右边界）

    def visit(self, url: str) -> None:
        """
        访问新页面时，把指针后面的所有历史“抹掉”，
        然后把新页面写到下一个位置。
        """
        self.curr += 1                # 指针向右移动一格
        if self.curr < len(self.history):
            # 位置已经被占用，直接覆盖（懒删）
            self.history[self.curr] = url
        else:
            # 还没有到达列表末尾，直接追加
            self.history.append(url)
        # 访问新页面后，所有“前进”记录失效，右边界跟随指针
        self.last = self.curr

    def back(self, steps: int) -> str:
        """
        往左走 steps 步，不能超过最左边（下标 0）。
        """
        self.curr = max(0, self.curr - steps)
        return self.history[self.curr]

    def forward(self, steps: int) -> str:
        """
        往右走 steps 步，不能超过已经存在的最右边界 self.last。
        """
        self.curr = min(self.last, self.curr + steps)
        return self.history[self.curr]
```

#### 复杂度

- **时间复杂度**  
  - `visit`、`back`、`forward` 均为 **O(1)**，因为只做指针的加减或一次赋值。相比暴力解的 `visit` O(n)，提升明显。  
- **空间复杂度**：**O(n)**，需要存储每一次真正访问的 URL。这里的 `n` 最多是 5000（题目限制），完全在可接受范围。

---

## 心得

- **核心技巧**：**指针+懒删**（或双向链表）。把“历史”看成一条线，操作只在指针两端移动或重新指向。
- **适用的题型**  
  1. **设计类**的题目，如「实现文本编辑器的撤销/重做」  
  2. 「前进/后退」类的浏览记录、音乐播放列表等  
  3. 「滑动窗口」需要在固定序列上维护左、右边界的情形
- **一句话总结**：**只动指针，不动数据**——把“删除”变成“忽略”，即可实现 O(1) 的操作。

## 反思

- **第一反应**：直接用列表保存所有页面，然后在 `visit` 时 `pop` 掉后面的元素。这样写起来直观，却会导致每次 `visit` 产生线性时间开销。  
- **最容易踩的坑**  
  - 忘记在 `visit` 后更新右边界（`last`），导致 `forward` 仍然可以访问已经失效的页面。  
  - `back` / `forward` 的步数可能超过边界，需要用 `max`/`min` 做保护。  
  - 题目限制最多 5000 次操作，若用极端的 O(n²) 方案会超时。  
- **下次类似题的第一步**：先把“状态”抽象成 **指针 + 数据容器**，判断哪些操作只需要移动指针，哪些需要真正修改容器。这样往往能直接得到 O(1) 的实现思路。