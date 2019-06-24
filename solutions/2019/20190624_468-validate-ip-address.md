# #468. 验证 IP 地址 / Validate IP Address

> 难度：中等 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/validate-ip-address/)

---

## 题目（英文原版）

**Description**

Given a string queryIP, return "IPv4" if IP is a valid IPv4 address, "IPv6" if IP is a valid IPv6 address or "Neither" if IP is not a correct IP of any type.
A valid IPv4 address is an IP in the form "x1.x2.x3.x4" where 0 <= xi <= 255 and xi cannot contain leading zeros. For example, "192.168.1.1" and "192.168.1.0" are valid IPv4 addresses while "192.168.01.1", "192.168.1.00", and "192.168@1.1" are invalid IPv4 addresses.
A valid IPv6 address is an IP in the form "x1:x2:x3:x4:x5:x6:x7:x8" where:
For example, "2001:0db8:85a3:0000:0000:8a2e:0370:7334" and "2001:db8:85a3:0:0:8A2E:0370:7334" are valid IPv6 addresses, while "2001:0db8:85a3::8A2E:037j:7334" and "02001:0db8:85a3:0000:0000:8a2e:0370:7334" are invalid IPv6 addresses.

**Examples**

**Example 1:**

```
Input: queryIP = "172.16.254.1"
Output: "IPv4"
Explanation: This is a valid IPv4 address, return "IPv4".
```

**Example 2:**

```
Input: queryIP = "2001:0db8:85a3:0:0:8A2E:0370:7334"
Output: "IPv6"
Explanation: This is a valid IPv6 address, return "IPv6".
```

**Example 3:**

```
Input: queryIP = "256.256.256.256"
Output: "Neither"
Explanation: This is neither a IPv4 address nor a IPv6 address.
```

**Constraints**

- queryIP consists only of English letters, digits and the characters '.' and ':'.

---

## 题目（中文翻译）

给定一个字符串 `queryIP`，如果它是合法的 IPv4 地址则返回 `"IPv4"`，如果是合法的 IPv6 地址则返回 `"IPv6"`，否则返回 `"Neither"`。  

合法的 **IPv4** 地址（IPv4 address）形如 `"x1.x2.x3.x4"`，其中每个 `xi` 满足 `0 <= xi <= 255`，且 `xi` 不能出现前导零。例如 `"192.168.1.1"` 和 `"192.168.1.0"` 是合法的 IPv4 地址，而 `"192.168.01.1"`、`"192.168.1.00"`、`"192.168@1.1"` 均非法。  

合法的 **IPv6** 地址（IPv6 address）形如 `"x1:x2:x3:x4:x5:x6:x7:x8"`，其中每个 `xi` 是 **1 到 4 位** 的十六进制数（可以包含大写字母 `A-F`），并且不能出现前导零（除非该块本身就是 `"0"`）。例如 `"2001:0db8:85a3:0000:0000:8a2e:0370:7334"` 与 `"2001:db8:85a3:0:0:8A2E:0370:7334"` 均为合法的 IPv6 地址，而 `"2001:0db8:85a3::8A2E:037j:7334"`（出现了双冒号 `::`）以及 `"02001:0db8:85a3:0000:0000:8a2e:0370:7334"`（块前有多余的零）均非法。  

## 示例  

### 示例 1  
**输入**: `queryIP = "172.16.254.1"`  
**输出**: `"IPv4"`  
**解释**: 这是一个合法的 IPv4 地址，返回 `"IPv4"`。  

### 示例 2  
**输入**: `queryIP = "2001:0db8:85a3:0:0:8A2E:0370:7334"`  
**输出**: `"IPv6"`  
**解释**: 这是一个合法的 IPv6 地址，返回 `"IPv6"`。  

### 示例 3  
**输入**: `queryIP = "256.256.256.256"`  
**输出**: `"Neither"`  
**解释**: 既不是合法的 IPv4 地址，也不是合法的 IPv6 地址。  

## 约束条件  

- `queryIP` 仅由英文字母、数字以及字符 `'.'` 和 `':'` 构成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把字符串按 `.` 或 `:` 分割，然后逐段检查每段是否符合对应的规则。

- **数据结构**：  
  - `list`（列表）相当于把一串水果（字符）切成若干小盒子（子串），每个盒子里装的就是一个段。  
  - 判断段是否合法需要用到 **整数**（把字符串转成数字）和 **字符集合**（判断是否只包含十六进制字符）。  
- **为什么正确**：  
  - IPv4 必须恰好有 4 段、每段都是 0~255 的十进制整数，且不能有前导零。  
  - IPv6 必须恰好有 8 段、每段是 1~4 位的十六进制数（0‑9、a‑f、A‑F），不能有空段。  
  - 只要逐段满足这些条件，整体就一定是合法的 IP。
- **复杂度分析**：  
  - 我们只遍历一次原字符串（长度记作 *n*），每个字符最多被检查一次，所以时间是 **O(n)**。  
  - 只用了常数个额外变量（几个列表、计数器），空间是 **O(1)**（不计输入本身的存储）。  
  - 大白话：如果字符串有 20 个字符，算法大约做 20 次“检查”，不管是 20 还是 2000，都是线性增长。

#### 代码（Python）

```python
class Solution:
    def validIPAddress(self, queryIP: str) -> str:
        # ---------- 判断是否是 IPv4 ----------
        if queryIP.count('.') == 3:                     # 必须恰好有 3 个点
            parts = queryIP.split('.')                  # 把字符串切成 4 段
            if len(parts) == 4 and all(self.is_ipv4_part(p) for p in parts):
                return "IPv4"

        # ---------- 判断是否是 IPv6 ----------
        if queryIP.count(':') == 7:                     # 必须恰好有 7 个冒号
            parts = queryIP.split(':')                  # 切成 8 段
            if len(parts) == 8 and all(self.is_ipv6_part(p) for p in parts):
                return "IPv6"

        # 两种格式都不匹配
        return "Neither"

    # ----- IPv4 子段检查 -----
    def is_ipv4_part(self, s: str) -> bool:
        # 空串、前导零（除非就是 "0"）直接失败
        if not s or (s[0] == '0' and len(s) > 1):
            return False
        # 必须全是数字
        if not s.isdigit():
            return False
        # 转成整数检查范围 0~255
        val = int(s)
        return 0 <= val <= 255

    # ----- IPv6 子段检查 -----
    def is_ipv6_part(self, s: str) -> bool:
        # 长度必须在 1~4 之间
        if not (1 <= len(s) <= 4):
            return False
        # 每个字符必须是十六进制字符（0-9 a-f A-F）
        for ch in s:
            if ch not in "0123456789abcdefABCDEF":
                return False
        return True
```

**关键行中文注释已标注**，代码可以直接运行。

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次输入字符串，`n` 为字符数。  
- **空间复杂度**：`O(1)` — 除了保存切分后的列表（最多 8 段）外，只使用常数级别的额外空间。

---

### 2. 最优解

#### 思路  

暴力解已经是线性时间、常数空间的最优复杂度。这里把“暴力”进一步精炼：

1. **一次遍历决定类型**  
   - 在遍历字符串的同时统计 `.` 和 `:` 的个数。  
   - 如果两者同时出现，立刻返回 `"Neither"`，因为合法 IP 只能用一种分隔符。  
2. **边界检查**  
   - 在遍历过程中直接检查每段的合法性，而不是先切分再检查。这样可以提前发现错误，省去后面的切分和额外遍历。  
3. **不使用额外的列表**  
   - 用两个指针 `start`、`i` 标记当前段的起始位置，遍历结束或遇到分隔符时直接验证该段。  

核心技巧是 **双指针 + 在线验证**，类似于在字符串里“找单词”时不复制子串，而是直接用索引检查。

> **类比**：想象你在一本书里找每一页的页码，直接用手指指向当前页的起始位置，而不是把每页的内容抄下来再检查。

#### 代码（Python）

```python
class Solution:
    def validIPAddress(self, queryIP: str) -> str:
        dot_cnt = queryIP.count('.')
        colon_cnt = queryIP.count(':')

        # 同时出现 . 与 :，直接不是合法 IP
        if dot_cnt and colon_cnt:
            return "Neither"

        # ---------- IPv4 ----------
        if dot_cnt == 3:                     # 必须恰好有 3 个点
            if self.is_ipv4(queryIP):
                return "IPv4"
            return "Neither"

        # ---------- IPv6 ----------
        if colon_cnt == 7:                   # 必须恰好有 7 个冒号
            if self.is_ipv6(queryIP):
                return "IPv6"
            return "Neither"

        return "Neither"

    # 在线验证 IPv4（不切分列表）
    def is_ipv4(self, s: str) -> bool:
        n = len(s)
        i = 0
        for part in range(4):               # 必须恰好四段
            if i >= n:                      # 提前结束
                return False
            start = i
            # 找到下一个点或字符串末尾
            while i < n and s[i] != '.':
                if not s[i].isdigit():      # 只能是数字
                    return False
                i += 1
            segment = s[start:i]            # 当前段子串
            # 不能为空，且不能有前导零（除非就是 "0"）
            if not segment or (segment[0] == '0' and len(segment) > 1):
                return False
            # 整数范围检查
            if int(segment) > 255:
                return False
            i += 1                           # 跳过点，进入下一段
        # 循环结束后 i 应该恰好等于 n（没有多余字符）
        return i == n + 1  # 因为最后一次循环会多加一次 i+=1

    # 在线验证 IPv6（不切分列表）
    def is_ipv6(self, s: str) -> bool:
        n = len(s)
        i = 0
        for part in range(8):               # 必须恰好八段
            if i >= n:
                return False
            start = i
            while i < n and s[i] != ':':
                ch = s[i]
                # 十六进制字符检查
                if not (ch.isdigit() or 'a' <= ch.lower() <= 'f'):
                    return False
                i += 1
            segment = s[start:i]
            # 长度必须 1~4
            if not (1 <= len(segment) <= 4):
                return False
            i += 1                           # 跳过冒号
        return i == n + 1  # 同上，最后一次 i+=1 会指向 n+1
```

> **注意**：这里的 `i == n + 1` 是因为循环体里统一在段结束后 `i += 1`，所以在成功遍历完所有段后 `i` 会比实际长度多 1。若感觉不直观，也可以在循环结束后 `i -= 1` 再比较。

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次字符串，所有检查都在同一次遍历中完成。  
- **空间复杂度**：`O(1)` — 只使用几个整数指针和常量级别的临时变量。

相比于先 `split` 再遍历的写法，**这里省去了创建子列表的开销**，在极端长字符串（如 10⁶ 字符）时会更省内存。

---

## 心得

- **核心技巧**：双指针（或称“滑动窗口”）在字符串中**在线**验证子段是否合法。  
- **适用题型**：  
  1. 判别合法的日期/时间字符串（如 `YYYY-MM-DD`）。  
  2. 检查电话号码或邮箱格式。  
  3. 解析自定义协议头（例如 `key=value;key2=value2`）。  
- **一句话总结**：**“一次遍历、分段即时校验”** 是处理固定分隔符格式的钥匙。

---

## 反思

- **第一反应**：看到 `.` 与 `:` 两种分隔符，就想到先 `split` 再检查每段。  
- **最容易踩的坑**：  
  - 前导零的处理（`0` 合法，`01` 不合法）。  
  - IPv6 中不能出现空段（连续 `::` 只在压缩写法里才合法，但本题不允许）。  
  - 结尾多余的分隔符或缺失分隔符导致段数不对。  
- **下次遇到同类题**：第一步先**统计分隔符出现次数**，确定是哪种格式，再**用指针逐段校验**，而不是直接 `split`。这样可以更早发现错误，也更节约空间。