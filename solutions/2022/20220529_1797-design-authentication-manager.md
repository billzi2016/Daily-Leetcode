# #1797. **设计认证管理器** / Design Authentication Manager

> 难度：中等 · 标签：Hash Table、Linked List、Design、Doubly-Linked List · [LeetCode 链接](https://leetcode.com/problems/design-authentication-manager/)

---

## 题目（英文原版）

**Description**

There is an authentication system that works with authentication tokens. For each session, the user will receive a new authentication token that will expire timeToLive seconds after the currentTime. If the token is renewed, the expiry time will be extended to expire timeToLive seconds after the (potentially different) currentTime.
Implement the AuthenticationManager class:
Note that if a token expires at time t, and another action happens on time t (renew or countUnexpiredTokens), the expiration takes place before the other actions.

**Examples**

**Example 1:**

```
Input
["AuthenticationManager", "renew", "generate", "countUnexpiredTokens", "generate", "renew", "renew", "countUnexpiredTokens"]
[[5], ["aaa", 1], ["aaa", 2], [6], ["bbb", 7], ["aaa", 8], ["bbb", 10], [15]]
Output
[null, null, null, 1, null, null, null, 0]

Explanation
AuthenticationManager authenticationManager = new AuthenticationManager(5); // Constructs the AuthenticationManager with timeToLive = 5 seconds.
authenticationManager.renew("aaa", 1); // No token exists with tokenId "aaa" at time 1, so nothing happens.
authenticationManager.generate("aaa", 2); // Generates a new token with tokenId "aaa" at time 2.
authenticationManager.countUnexpiredTokens(6); // The token with tokenId "aaa" is the only unexpired one at time 6, so return 1.
authenticationManager.generate("bbb", 7); // Generates a new token with tokenId "bbb" at time 7.
authenticationManager.renew("aaa", 8); // The token with tokenId "aaa" expired at time 7, and 8 >= 7, so at time 8 the renew request is ignored, and nothing happens.
authenticationManager.renew("bbb", 10); // The token with tokenId "bbb" is unexpired at time 10, so the renew request is fulfilled and now the token will expire at time 15.
authenticationManager.countUnexpiredTokens(15); // The token with tokenId "bbb" expires at time 15, and the token with tokenId "aaa" expired at time 7, so currently no token is unexpired, so return 0.
```

**Constraints**

- 1 <= timeToLive <= 108
- 1 <= currentTime <= 108
- 1 <= tokenId.length <= 5
- tokenId consists only of lowercase letters.
- All calls to generate will contain unique values of tokenId.
- The values of currentTime across all the function calls will be strictly increasing.
- At most 2000 calls will be made to all functions combined.

---

## 题目（中文翻译）

有一个基于认证令牌（authentication token）的认证系统。每次会话开始时，用户会获得一个新的认证令牌，该令牌将在 **timeToLive** 秒后（相对于当前时间 `currentTime`）过期。如果对令牌执行续期（renew）操作，则其过期时间会被延长至 **timeToLive** 秒后（相对于此时的 `currentTime`，该时间可能与之前不同）。

实现 `AuthenticationManager` 类，需要支持以下接口：

- `AuthenticationManager(int timeToLive)`  
  构造函数，初始化令牌的存活时间为 `timeToLive` 秒。

- `void generate(string tokenId, int currentTime)`  
  在时间 `currentTime` 生成一个新的令牌 `tokenId`。该令牌的过期时间设为 `currentTime + timeToLive`。题目保证所有 `generate` 调用的 `tokenId` 均不重复。

- `void renew(string tokenId, int currentTime)`  
  若令牌 `tokenId` **未过期**，则将其过期时间更新为 `currentTime + timeToLive`。若令牌已过期或不存在，则该操作不做任何修改。

- `int countUnexpiredTokens(int currentTime)`  
  返回截至时间 `currentTime` 时，仍未过期的令牌数量。

> **注意**：如果令牌在时间点 `t` 失效，而在同一时间点 `t` 又有续期（`renew`）或计数（`countUnexpiredTokens`）操作，则先执行失效处理，再执行后续操作。

---

### 示例

```text
输入
["AuthenticationManager", "renew", "generate", "countUnexpiredTokens", "generate", "renew", "renew", "countUnexpiredTokens"]
[[5], ["aaa", 1], ["aaa", 2], [6], ["bbb", 7], ["aaa", 8], ["bbb", 10], [15]]
输出
[null, null, null, 1, null, null, null, 0]
```

**解释**

```java
AuthenticationManager authenticationManager = new AuthenticationManager(5); // timeToLive = 5 秒
authenticationManager.renew("aaa", 1);          // "aaa" 不存在或已过期，什么也不做
authenticationManager.generate("aaa", 2);      // 生成令牌 "aaa"，过期时间为 2 + 5 = 7
authenticationManager.countUnexpiredTokens(6); // 只有 "aaa" 未过期，返回 1
authenticationManager.generate("bbb", 7);      // 生成令牌 "bbb"，过期时间为 7 + 5 = 12
authenticationManager.renew("aaa", 8);          // "aaa" 已在时间 7 失效，续期无效
authenticationManager.renew("bbb", 10);         // "bbb" 未失效，更新过期时间为 10 + 5 = 15
authenticationManager.countUnexpiredTokens(15); // 时间 15 时 "bbb" 已失效，返回 0
```

---

### 约束条件

- `1 <= timeToLive <= 10^8`
- `1 <= currentTime <= 10^8`
- `1 <= tokenId.length <= 5`
- `tokenId` 仅由小写英文字母组成
- 所有 `generate` 调用的 `tokenId` 均唯一
- 所有函数调用中的 `currentTime` 值严格递增
- 所有函数的调用总次数不超过 `2000` 次

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有 token 的过期时间都存到一个哈希表**（Python 中的 `dict`）里。  
- **哈希表**可以类比成一本“查字典”：词（`tokenId`）对应页码（过期时间 `expireTime`），查找、插入、修改都只需要一步，就像在字典里翻页一样快。  
- `generate(tokenId, currentTime)` → 把 `tokenId` → `currentTime + timeToLive` 放进字典。  
- `renew(tokenId, currentTime)` → 先检查字典里是否有这个 `tokenId`，再判断它的过期时间是否已经小于等于 `currentTime`（已经失效），如果仍然有效就把它的过期时间更新为 `currentTime + timeToLive`。  
- `countUnexpiredTokens(currentTime)` → 把字典里所有的过期时间都遍历一遍，统计出 **大于** `currentTime` 的数量。

**为什么这种方法一定能得到正确答案**  
因为我们把每一次操作的所有信息都完整记录下来：每个 token 的最新过期时间。只要在查询时把已经失效的 token 过滤掉，剩下的就是“未过期”的 token，计数自然正确。

**时间/空间复杂度的大白话解释**  
- `generate`、`renew` 只涉及一次哈希表的写入或读取，**相当于把一本字典翻到某一页并写上新内容**，时间几乎不随数据量变化，用 `O(1)` 表示。  
- `countUnexpiredTokens` 必须把字典里 **所有** 的条目都检查一遍，就像把整本字典从头到尾快速浏览一遍，最坏情况下要看 `n` 条记录（`n` 为当前已生成的 token 数），所以是 `O(n)`。  
- 空间上我们要保存每个 token 的 ID 和它的过期时间，**和 token 的数量成正比**，即 `O(n)`。

#### 代码（Python）

```python
class AuthenticationManager:
    def __init__(self, timeToLive: int):
        """
        :param timeToLive: token 的存活时间（秒）
        """
        self.time_to_live = timeToLive               # 保存 ttl
        self.expire = {}                               # 哈希表：tokenId -> 失效时间

    def generate(self, tokenId: str, currentTime: int) -> None:
        """生成一个新的 token"""
        self.expire[tokenId] = currentTime + self.time_to_live   # 直接写入字典

    def renew(self, tokenId: str, currentTime: int) -> None:
        """如果 token 仍然有效，则延长其失效时间"""
        # 先判断 token 是否存在且未过期
        if tokenId in self.expire and self.expire[tokenId] > currentTime:
            self.expire[tokenId] = currentTime + self.time_to_live   # 更新失效时间

    def countUnexpiredTokens(self, currentTime: int) -> int:
        """统计所有未过期的 token 数量"""
        cnt = 0
        for expire_time in self.expire.values():     # 遍历所有失效时间
            if expire_time > currentTime:            # 只计数仍然有效的
                cnt += 1
        return cnt
```

#### 复杂度

- **时间复杂度**  
  - `generate`：`O(1)`（一次哈希写入）  
  - `renew`：`O(1)`（一次哈希查询 + 写入）  
  - `countUnexpiredTokens`：`O(n)`，其中 `n` 为当前已生成的 token 数。相当于“把所有记录都检查一遍”。  

- **空间复杂度**  
  - `O(n)`，因为要保存每个 token 的 ID 与对应的失效时间。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在 `countUnexpiredTokens`**：每次都要遍历全部 token，导致 `O(n)`。  
如果我们能够 **把已经失效的 token 及时从数据结构中移除**，那么计数时只需要看剩下的“活着的” token 数量即可，时间就会降到 `O(1)`（或与未过期 token 数量成正比，但不会随已失效的 token 增长）。

**关键观察**  
- 所有 token 的失效时间都是 **递增** 的（因为 `currentTime` 在所有调用中严格递增），所以如果我们把 token 按失效时间的顺序排成一条链（或队列），**最早失效的 token 永远在链头**。  
- 当需要统计未过期 token 时，只要**从链头一直删掉已经失效的节点**，剩下的节点就是全部未过期的 token。  

**采用的数据结构**  

| 数据结构 | 作用 | 类比 |
|----------|------|------|
| **哈希表 `token -> Node`** | 让我们可以**O(1)** 找到任意 token 对应的链节点，便于更新或删除 | 像一本“查字典”，词（token）对应页码（链节点） |
| **双向链表（Doubly Linked List）** | 按失效时间从早到晚维护所有 token，头部是最早失效的 | 想象一列排队的乘客，最先上车的站在最前面，后面的人排得更晚 |

**操作细节**  

1. **生成 token**  
   - 计算 `expire = currentTime + timeToLive`。  
   - 在链表尾部（最新的失效时间）插入一个新节点 `Node(tokenId, expire)`。  
   - 在哈希表中记录 `tokenId -> 该节点`。  

2. **续期 token**  
   - 先通过哈希表找到对应的节点。  
   - 判断节点的 `expire` 是否已经 ≤ `currentTime`（已经失效），如果是则直接忽略。  
   - 否则：**删除旧节点**（因为失效时间要改动），在链表尾部重新插入一个 **新的节点**，并在哈希表中更新指向。  

3. **计数未过期 token**  
   - **从链表头部一直向后**，只要头节点的 `expire ≤ currentTime`，就把它弹出（同时在哈希表中删掉对应的键）。这一步称为“懒惰删除”。  
   - 当链表头部的 `expire` 已经大于 `currentTime` 时，说明剩下的全部都是未过期的。直接返回链表长度即可（我们可以维护一个计数器 `size`，每插入一次 `+1`，每删除一次 `-1`）。  

这样，**每一次 `countUnexpiredTokens` 只需要把已经过期的、且** **在最前面的****节点逐个弹出**，而已过期但不在最前面的节点已经在之前的 `renew` 或 `count` 中被清理掉了。整体时间复杂度趋近于 **摊销 O(1)**。

#### 代码（Python）

```python
class Node:
    """双向链表的节点，保存 tokenId 与对应的失效时间"""
    __slots__ = ('token', 'expire', 'prev', 'next')
    def __init__(self, token: str, expire: int):
        self.token = token
        self.expire = expire
        self.prev = None
        self.next = None


class AuthenticationManager:
    def __init__(self, timeToLive: int):
        self.ttl = timeToLive                 # token 的存活时长
        self.map = {}                          # tokenId -> Node（哈希表）
        # 初始化一个哨兵节点，方便插入/删除操作（头尾同一个哨兵）
        self.head = Node('', -1)               # 虚拟头节点
        self.tail = Node('', -1)               # 虚拟尾节点
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0                          # 当前未过期 token 的数量

    # ----- 链表基础操作 -----
    def _add_to_tail(self, node: Node) -> None:
        """把节点接到链表尾部（最新的失效时间）"""
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node
        self.size += 1

    def _remove(self, node: Node) -> None:
        """把节点从链表中摘除"""
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def _purge(self, currentTime: int) -> None:
        """
        删除所有已经失效且位于链表最前面的节点。
        这一步在每次查询前执行，保证链表里只剩未过期的 token。
        """
        while self.head.next != self.tail and self.head.next.expire <= currentTime:
            expired_node = self.head.next
            self._remove(expired_node)
            # 同时把哈希表中的映射删掉
            del self.map[expired_node.token]

    # ----- 对外接口 -----
    def generate(self, tokenId: str, currentTime: int) -> None:
        """生成新 token，直接放在链表尾部"""
        expire = currentTime + self.ttl
        node = Node(tokenId, expire)
        self._add_to_tail(node)
        self.map[tokenId] = node

    def renew(self, tokenId: str, currentTime: int) -> None:
        """如果 token 仍然有效，则把它的失效时间延后"""
        node = self.map.get(tokenId)
        if not node:
            return                     # token 不存在，直接返回
        if node.expire <= currentTime:
            # 已经过期，不做任何操作
            return
        # 先把旧节点摘除，然后重新插入一个新的节点（新的失效时间）
        self._remove(node)
        new_expire = currentTime + self.ttl
        new_node = Node(tokenId, new_expire)
        self._add_to_tail(new_node)
        self.map[tokenId] = new_node   # 哈希表指向最新的节点

    def countUnexpiredTokens(self, currentTime: int) -> int:
        """返回未过期 token 的数量"""
        self._purge(currentTime)       # 先清理掉已经失效的
        return self.size
```

#### 复杂度

- **时间复杂度**  
  - `generate`：`O(1)`（在链表尾部插入、哈希表写入）  
  - `renew`：`O(1)`（哈希表定位 → 链表删除 → 链表尾部插入）  
  - `countUnexpiredTokens`：摊销 `O(1)`。虽然在一次调用中可能会遍历并删除多个已经失效的节点，但每个节点只会被删除一次，累计下来仍是线性 `O(totalCalls)`，相当于每次操作的均摊代价是常数。  

- **空间复杂度**  
  - `O(n)`，其中 `n` 为当前未过期 token 的数量（因为已经过期的节点会在 `countUnexpiredTokens` 中被及时清除）。  

与暴力解相比，**最主要的提升是把计数从遍历所有 token（`O(n)`）降到了只看未过期 token 的数量（`O(1)`）**，而且额外的链表操作只占常数时间。

---

## 心得

- **核心技巧**：利用**哈希表 + 双向链表**（或队列）实现 **“按失效时间有序的集合”**，并在查询前进行**懒惰删除**。  
- **适用的题型**  
  1. **缓存淘汰**（LRU Cache）——同样需要哈希表快速定位 + 链表维护使用顺序。  
  2. **有时间窗口的计数**（比如滑动窗口最大值、计数器）——需要按时间顺序快速剔除过期元素。  
  3. **设计类题目**（如设计限流器、验证码系统）——常常涉及“在一定时间内只保留最近的记录”。  
- **一句话总结解题钥匙**：**“把最早失效的元素放在最前面，随时把它们弹出”，这样计数永远是 O(1)。**

---

## 反思

- **第一反应**：看到 “countUnexpiredTokens” 需要遍历所有 token，立刻想到直接用 `dict` 存储，然后每次遍历计数——这就是暴力思路。  
- **最容易踩的坑**  
  1. **时间顺序的细节**：题目说明 “如果在时间 t 有失效和 renew/ count 同时发生，失效先执行”。在实现时必须在 `renew`、`countUnexpiredTokens` 里先判断 `expire <= currentTime` 再进行后续操作。  
  2. **边界条件**：`generate` 的 `tokenId` 保证唯一，但 `renew` 可能收到已经失效或根本不存在的 token，需要安全地直接返回。  
  3. **内存泄漏**：如果只在 `renew` 时删除旧节点，却不在 `countUnexpiredTokens` 中清理已经过期的节点，链表会无限增长。  
- **下次类似题的第一步**：先问自己 **“是否可以把过期的元素按照时间排成一列，并在需要时一次性清理掉最前面的元素？”** 如果答案是肯定的，往往就可以用 **哈希表 + 有序容器（链表/队列/堆）** 来把操作摊销到 O(1)。