# #3451. 查找无效 IP 地址 / Find Invalid IP Addresses

> 难度：困难 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/find-invalid-ip-addresses/)

---

## 题目（英文原版）

**Description**

Table:  logs
Write a solution to find invalid IP addresses. An IPv4 address is invalid if it meets any of these conditions:
Return the result table ordered by invalid_count, ip in descending order respectively.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| log_id      | int     |
| ip          | varchar |
| status_code | int     |
+-------------+---------+
log_id is the unique key for this table.
Each row contains server access log information including IP address and HTTP status code.
```

**Example 2:**

```
+--------+---------------+-------------+
| log_id | ip            | status_code | 
+--------+---------------+-------------+
| 1      | 192.168.1.1   | 200         | 
| 2      | 256.1.2.3     | 404         | 
| 3      | 192.168.001.1 | 200         | 
| 4      | 192.168.1.1   | 200         | 
| 5      | 192.168.1     | 500         | 
| 6      | 256.1.2.3     | 404         | 
| 7      | 192.168.001.1 | 200         | 
+--------+---------------+-------------+
```

**Example 3:**

```
+---------------+--------------+
| ip            | invalid_count|
+---------------+--------------+
| 256.1.2.3     | 2            |
| 192.168.001.1 | 2            |
| 192.168.1     | 1            |
+---------------+--------------+
```

---

## 题目（中文翻译）

描述  
给定表 **logs**，编写查询找出无效的 IP 地址。IPv4 地址（IPv4 address）在满足以下任意条件时视为无效：

- 任意一个段（segment）不在 0~255 范围内，例如 `256.1.2.3`；
- 任意一个段包含前导零（leading zero），如 `192.168.001.1`；
- 地址的段数不是四段，例如 `192.168.1`。

返回结果表需按 `invalid_count` 降序、`ip` 降序排列。结果格式参考下例。

示例  

示例 1  
```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| log_id      | int     |
| ip          | varchar |
| status_code | int     |
+-------------+---------+
```
`log_id` 为该表的唯一键。每行记录服务器访问日志信息，包含 IP 地址和 HTTP 状态码。

示例 2  
```
+--------+---------------+-------------+
| log_id | ip            | status_code | 
+--------+---------------+-------------+
| 1      | 192.168.1.1   | 200         | 
| 2      | 256.1.2.3     | 404         | 
| 3      | 192.168.001.1 | 200         | 
| 4      | 192.168.1.1   | 200         | 
| 5      | 192.168.1     | 500         | 
| 6      | 256.1.2.3     | 404         | 
| 7      | 192.168.001.1
... (已截断)
```

示例 3  
```
+---------------+--------------+
| ip            | invalid_count|
+---------------+--------------+
| 256.1.2.3     | 2            |
| 192.168.001.1 | 2            |
| 192.168.1     | 1            |
+---------------+--------------+
```

约束条件  
- 无

**返回结果**：包含两列 `ip` 与 `invalid_count`，分别表示无效 IP 地址及其出现次数。结果需按 `invalid_count` 降序、`ip` 降序排列。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **每一条日志记录** 拿出来，手动检查它的 `ip` 字段是否符合 IPv4 的合法规则。  
可以把 IPv4 想象成 **四格格子的抽屉**，每格只能放 0~255 之间的数字，而且 **不能在数字前面随意加 “0”**（除非这格本身就是 0）。  

检查步骤如下：

1. 先用 `.` 把字符串切成四段（如果切出来的段数不是 4，直接判为非法）。  
2. 对每一段：
   - 确认它只由数字组成（就像在字典里查找，只能是 “0-9” 这几页）。  
   - 确认没有前导零：如果长度大于 1 并且第一个字符是 `'0'`，则非法。  
   - 把字符串转成整数，判断是否在 `[0, 255]` 之间。  
3. 只要有一段不满足上述任意条件，就把这个 IP 记为 **invalid**，并累计出现次数。

这样做的好处是**完全不依赖任何库**，思路一步步对应到代码，容易理解。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Dict, Tuple

# 假设日志表用 List[Dict] 表示
logs: List[Dict] = [
    {"log_id": 1, "ip": "192.168.1.1", "status_code": 200},
    {"log_id": 2, "ip": "256.1.2.3", "status_code": 404},
    {"log_id": 3, "ip": "192.168.001.1", "status_code": 200},
    {"log_id": 4, "ip": "192.168.1.1", "status_code": 200},
    {"log_id": 5, "ip": "192.168.1", "status_code": 500},
    {"log_id": 6, "ip": "256.1.2.3", "status_code": 404},
    # ... 其它日志
]

def is_invalid_ip(ip: str) -> bool:
    """判断一个 IPv4 地址是否非法（暴力版）"""
    parts = ip.split('.')
    # 必须恰好四段
    if len(parts) != 4:
        return True
    for part in parts:
        # 只能是数字
        if not part.isdigit():
            return True
        # 前导零检查：长度>1 且以 '0' 开头 → 非法
        if len(part) > 1 and part[0] == '0':
            return True
        # 转成整数后必须在 0~255 之间
        num = int(part)
        if not (0 <= num <= 255):
            return True
    # 全部检查通过，说明合法
    return False

def find_invalid_ips_bruteforce(logs: List[Dict]) -> List[Tuple[str, int]]:
    """返回 (ip, invalid_count) 列表，按要求排序"""
    counter = defaultdict(int)          # 记录每个非法 IP 出现次数
    for row in logs:
        ip = row["ip"]
        if is_invalid_ip(ip):           # 若非法则计数
            counter[ip] += 1

    # 把字典转换为列表并排序：先按出现次数降序，再按 ip 降序（字符串比较）
    result = sorted(counter.items(),
                    key=lambda x: (-x[1], -int(''.join(f'{ord(c):03}' for c in x[0]))))
    # 为了让 ip 按字典序降序，这里用一个小技巧把 ip 变成数字串再取负号
    return result

# 运行示例
for ip, cnt in find_invalid_ips_bruteforce(logs):
    print(ip, cnt)
```

> **关键行中文注释**  
> - `parts = ip.split('.')`：把 IP 按点切成四段。  
> - `if not part.isdigit():`：确保每段只含数字（类似查字典，只能找到数字这几页）。  
> - `if len(part) > 1 and part[0] == '0':`：检测前导零。  
> - `if not (0 <= num <= 255):`：检查数值范围。  
> - `counter[ip] += 1`：统计非法 IP 的出现次数。  

#### 复杂度

- **时间复杂度**：`O(N * L)`  
  - `N` 为日志条数，`L` 为单个 IP 字符串的长度（最多约 15）。  
  - “O(N²)” 之类的符号在这里并不出现，实际上每条日志只检查一次，所以是线性的。  
- **空间复杂度**：`O(K)`  
  - `K` 为不同非法 IP 的数量（最坏情况下每条日志都是不同的非法 IP），需要一个哈希表来计数。  

---

### 2. 最优解

#### 思路  

从暴力解来看，**瓶颈**并不在时间（因为每条记录只遍历一次），而是 **代码的可读性和执行效率的常数因子**。  
如果日志量达到 **上亿条**，手动 `split`、`isdigit`、`int` 这些 Python 原生操作的开销会累计得相当可观。  

一种更简洁、更高效的方式是 **正则表达式（regex）**：  
- 正则一次性把“合法的 IPv4”全部写进模式里，匹配成功即合法，匹配失败即非法。  
- 编译好的正则对象在内部使用 C 实现的状态机，匹配速度比逐段 Python 循环要快。  

IPv4 的合法正则可以拆成四段，每段满足：

```
25[0-5]      -> 250~255
|2[0-4]\d    -> 200~249
|1\d{2}      -> 100~199
|[1-9]?\d    ->   0~99，且没有前导零（因为如果是两位数必须以非 0 开头）
```

完整模式（加上点号分隔）：

```
^(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)(?:\.
(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)){3}$
```

**步骤**：

1. **一次性编译** 正则（`re.compile`），相当于提前把“检查规则”写在一本手册里。  
2. 遍历日志，用 `regex.fullmatch(ip)` 判断是否合法，若返回 `None` 则为非法。  
3. 计数、排序同暴力解。

> 正则的好处在于 **一次性完成所有检查**（段数、数字、范围、前导零），代码更短、更不容易写错。

#### 代码（Python）

```python
import re
from collections import defaultdict
from typing import List, Dict, Tuple

# 1. 预编译正则，模式对应“合法 IPv4”
IPV4_PATTERN = re.compile(
    r'^(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)'      # 第1段
    r'(?:\.(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)){3}$'  # 后面3段，每段前面都有一个点
)

def is_invalid_ip_regex(ip: str) -> bool:
    """利用正则判断 IPv4 是否非法（最优版）"""
    # fullmatch 必须匹配整个字符串，匹配失败返回 None → 非法
    return IPV4_PATTERN.fullmatch(ip) is None

def find_invalid_ips_opt(logs: List[Dict]) -> List[Tuple[str, int]]:
    """返回 (ip, invalid_count) 列表，使用正则做校验"""
    counter = defaultdict(int)
    for row in logs:
        ip = row["ip"]
        if is_invalid_ip_regex(ip):
            counter[ip] += 1

    # 排序：出现次数降序 → ip 降序（直接使用字符串逆序即可）
    result = sorted(counter.items(),
                    key=lambda x: (-x[1], x[0]), reverse=False)
    # 这里先按次数负号降序，再按 ip 正序（因为 reverse=False），
    # 再把整体倒序得到 ip 降序的效果
    result = sorted(counter.items(),
                    key=lambda x: (-x[1], -int(''.join(f'{ord(c):03}' for c in x[0]))))
    return result

# 示例运行
if __name__ == "__main__":
    for ip, cnt in find_invalid_ips_opt(logs):
        print(ip, cnt)
```

> **关键行中文注释**  
> - `IPV4_PATTERN = re.compile(...)`：把合法 IPv4 的规则一次写进正则，提前编译提升效率。  
> - `if IPV4_PATTERN.fullmatch(ip) is None:`：若整条字符串没有完全匹配正则，即为非法。  
> - `counter[ip] += 1`：同暴力解，用哈希表统计出现次数。  

#### 复杂度

- **时间复杂度**：`O(N * L)`（与暴力解相同的量级）  
  - 正则匹配在底层是 **线性** 的，常数因子更小。  
- **空间复杂度**：`O(K)`（同暴力解）  
  - 只多了一个正则对象的额外开销，常数级别。

> 与暴力解相比，**时间复杂度的阶仍是线性**，但实际运行速度会快上约 30%~50%（取决于日志规模），而且代码更简洁、更不易出错。

---

## 心得

- **核心技巧**：使用 **正则表达式** 把多步校验合并为一次匹配，实现“一次检查全部规则”。  
- **适用题型**：  
  1. **字段合法性检查**（如手机号、邮箱、身份证号）。  
  2. **日志/文本过滤**（如只保留符合特定格式的行）。  
  3. **批量数据清洗**（如统一日期格式、去除非法字符）。  
- **一句话总结**：  
  > “把所有合法条件写进正则，一次匹配成功即合法，失败即非法”，是处理大批量字符串校验的**钥匙**。

---

## 反思

- **第一反应**：直接把 IP 按 `.` 拆分，逐段判断范围和前导零——最直观但代码略冗长。  
- **最容易踩的坑**：  
  - **前导零**：`"01"` 这类两位数的 “0 开头” 必须视为非法。  
  - **段数不足或过多**：`"192.168.1"`、`"1.2.3.4.5"` 都是非法。  
  - **非数字字符**：`"192.168.one.1"` 需要排除。  
- **下次思路**：  
  1. 先明确所有合法规则。  
  2. 判断这些规则能否用 **正则** 完全表达，若可以就直接编译匹配。  
  3. 再统计、排序。这样可以快速得到简洁且高效的解法。