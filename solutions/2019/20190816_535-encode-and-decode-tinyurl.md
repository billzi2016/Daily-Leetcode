# #535. 编码与解码 TinyURL / Encode and Decode TinyURL

> 难度：中等 · 标签：Hash Table、String、Design、Hash Function · [LeetCode 链接](https://leetcode.com/problems/encode-and-decode-tinyurl/)

---

## 题目（英文原版）

**Description**

TinyURL is a URL shortening service where you enter a URL such as https://leetcode.com/problems/design-tinyurl and it returns a short URL such as http://tinyurl.com/4e9iAk. Design a class to encode a URL and decode a tiny URL.
There is no restriction on how your encode/decode algorithm should work. You just need to ensure that a URL can be encoded to a tiny URL and the tiny URL can be decoded to the original URL.
Implement the Solution class:

**Examples**

**Example 1:**

```
Input: url = "https://leetcode.com/problems/design-tinyurl"
Output: "https://leetcode.com/problems/design-tinyurl"

Explanation:
Solution obj = new Solution();
string tiny = obj.encode(url); // returns the encoded tiny url.
string ans = obj.decode(tiny); // returns the original url after decoding it.
```

**Constraints**

- 1 <= url.length <= 104
- url is guranteed to be a valid URL.

---

## 题目（中文翻译）

TinyURL 是一种 URL 缩短服务，你输入一个完整的 URL，例如 `https://leetcode.com/problems/design-tinyurl`，它会返回一个短链接，例如 `http://tinyurl.com/4e9iAk`。请设计一个类，用于 **编码**（encode）一个 URL 并 **解码**（decode）一个 TinyURL。

对你的编码/解码算法没有具体限制，只需保证能够将任意合法 URL 编码为一个短链接，并且能够通过该短链接解码回原始 URL。

实现 `Solution` 类，使其能够完成上述功能。

## 示例 1

**输入**  
`url = "https://leetcode.com/problems/design-tinyurl"`

**输出**  
`"https://leetcode.com/problems/design-tinyurl"`

**解释**  
```java
Solution obj = new Solution();
string tiny = obj.encode(url); // 返回编码后的短链接
string ans = obj.decode(tiny); // 解码后返回原始的 URL
```

## 约束条件

- `1 <= url.length <= 10^4`
- `url` 保证是一个合法的 URL。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**把每一个长 URL 当作字典（哈希表）的 key，随机生成一个短串当作 value**，再把这两者互相保存下来。  

- **哈希表**可以类比为“查字典”。我们把长网址想象成词条，短网址想象成词条对应的页码。只要把词条（长 URL）和页码（短码）放进字典，以后想找回原文，只需要用页码去字典里查一次即可。  
- **生成短码**：可以随意取 6~7 位英文字母+数字的组合（比如 `4e9iAk`），因为 62^6 ≈ 56.8 亿，远大于本题的最大输入量（10⁴ 条），冲突概率极低。若不幸生成了已经被占用的短码，就**重新生成**，直到得到一个未被使用的为止。  
- **正确性**：  
  1. 每次 `encode` 都把长 URL 与生成的短码记在哈希表里。  
  2. `decode` 时，只要把短码当作 key 去哈希表里查找对应的长 URL，即可得到原始地址。  
  只要哈希表没有出错，这对映射就是一一对应的，必然能恢复原始 URL。  

#### 代码（Python）  

```python
import random
import string

class Solution:
    def __init__(self):
        # 长 URL -> 短码
        self.long2short = {}
        # 短码 -> 长 URL
        self.short2long = {}
        # 短 URL 前缀（题目中给的固定部分）
        self.prefix = "http://tinyurl.com/"

    # 生成一个长度为 6 的随机短码，字符集为大小写字母+数字
    def _get_random_code(self) -> str:
        chars = string.ascii_letters + string.digits  # a-zA-Z0-9 共 62 个字符
        return ''.join(random.choice(chars) for _ in range(6))

    def encode(self, longUrl: str) -> str:
        """把长 URL 编码成短 URL"""
        # 已经编码过的直接返回，避免重复生成
        if longUrl in self.long2short:
            return self.prefix + self.long2short[longUrl]

        # 生成不冲突的短码
        code = self._get_random_code()
        while code in self.short2long:          # 若冲突则重新生成
            code = self._get_random_code()

        # 建立双向映射
        self.long2short[longUrl] = code
        self.short2long[code] = longUrl
        return self.prefix + code

    def decode(self, shortUrl: str) -> str:
        """把短 URL 还原成原始的长 URL"""
        code = shortUrl.replace(self.prefix, "")  # 取出短码部分
        return self.short2long.get(code, "")       # 若不存在返回空串
```

#### 复杂度  
- **时间复杂度**：  
  - `encode`：平均 **O(1)**（一次哈希表查询 + 生成随机码）。最坏情况（极少发生）需要多次重新生成随机码，仍然是常数级别的操作。  
  - `decode`：**O(1)**，只做一次哈希表查询。  
  “O(1)” 可以理解为“无论有多少条 URL，查一次表的时间基本不变”。  

- **空间复杂度**：**O(N)**，其中 N 为已编码的 URL 数目。我们需要把每一对长 URL 与短码都保存下来，存储空间随输入线性增长。  

---  

### 2. 最优解  

#### 思路  
暴力解的主要“瓶颈”在于**随机生成短码并检查冲突**。虽然冲突概率极低，但仍然需要循环，且每次生成的短码没有任何规律，可读性差。  

我们可以把“生成短码”的过程改成**可预测且唯一的**：为每一个新 URL 分配一个自增的整数 ID，然后把这个整数用 **62 进制**（即 `0-9 a-z A-Z`）表示成字符串。  

- **为什么 62 进制？**  
  - 字符集大小 62（10 位数字 + 26 小写 + 26 大写），可以用最少的字符表示更大的数。  
  - 例如 ID=125  →  用 62 进制写成 `cb`（只需要两位），比十进制 `125` 更短。  

- **核心步骤**  
  1. **自增 ID**：用一个整数 `counter` 记录已经分配的数量。第一次编码时 `counter = 1`，第二次 `counter = 2` ……  
  2. **整数 → 62 进制**：把 `counter` 按 62 进制拆分，得到字符数组，再拼成短码。  
  3. **双向映射**：仍然需要两个哈希表，一个把长 URL → 短码（防止同一个长 URL 被多次编码得到不同短码），另一个把短码 → 长 URL（解码时使用）。  

- **类比**：想象你在图书馆给每本新书贴上顺序编号（ID），然后把编号写成一种“特殊的字母数字混合码”，这样既保证唯一，又方便快速查找。  

#### 代码（Python）  

```python
class Solution:
    def __init__(self):
        self.prefix = "http://tinyurl.com/"
        self.long2short = {}   # 长 URL -> 短码
        self.short2long = {}   # 短码 -> 长 URL
        self.counter = 1       # 下一个要分配的 ID，起始于 1

        # 62 进制字符表（索引即对应的数值）
        self.chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # 把十进制整数转换为 62 进制字符串
    def _to_base62(self, num: int) -> str:
        if num == 0:
            return self.chars[0]
        res = []
        base = 62
        while num > 0:
            num, rem = divmod(num, base)   # 取余数作为当前位的字符索引
            res.append(self.chars[rem])
        # 由于是从低位到高位依次放入，最后需要逆序
        return ''.join(reversed(res))

    def encode(self, longUrl: str) -> str:
        """把长 URL 编码为固定前缀 + 62 进制短码"""
        # 已经编码过的直接返回，保证同一个长 URL 对应同一个短码
        if longUrl in self.long2short:
            return self.prefix + self.long2short[longUrl]

        # 生成唯一短码
        code = self._to_base62(self.counter)
        self.counter += 1

        # 保存映射关系
        self.long2short[longUrl] = code
        self.short2long[code] = longUrl
        return self.prefix + code

    def decode(self, shortUrl: str) -> str:
        """根据短码查找原始的长 URL"""
        code = shortUrl.replace(self.prefix, "")
        return self.short2long.get(code, "")
```

#### 复杂度  
- **时间复杂度**：  
  - `encode`：**O(1)**（整数转 62 进制的循环次数等于字符数，最多约 `log₆₂(N)`，对 N≤10⁴ 来说最多 3~4 次，仍视作常数）。  
  - `decode`：**O(1)**，一次哈希表查询。  
  与暴力解相比，**不再需要随机生成并检查冲突**，最坏情况更可控。  

- **空间复杂度**：**O(N)**，同样需要保存所有映射，只是额外多了一个整数计数器，常数级别的额外空间。  

---  

## 心得  

- **核心技巧**：使用**自增 ID + 进制转换**（这里是 62 进制）实现唯一且短的编码。  
- **适用场景**：  
  1. 短链接、邀请码、唯一短码生成等需要“短且唯一”的场景。  
  2. 需要把大整数压缩成可读字符串的情形，如 **Base62 编码**、**短 URL**、**文件哈希短码**。  
  3. 任何“把序号映射到自定义字符集”的需求（如自定义进制计数器）。  
- **一句话总结**：**用递增编号再转成62进制，既保证唯一又省空间，是生成短 URL 的钥匙。**  

---  

## 反思  

- **第一反应**：直接想到哈希表 + 随机字符串，这是最直观、最易实现的办法。  
- **最容易踩的坑**：  
  - **冲突处理**：随机生成的短码可能重复，需要循环检查。  
  - **重复编码**：同一个长 URL 多次调用 `encode` 时，应返回相同的短码，否则会浪费空间。  
  - **前缀处理**：`decode` 时要把固定的 `http://tinyurl.com/` 前缀去掉，否则查不到映射。  
- **下次类似题的第一步**：先判断是否可以用“**自增编号 + 进制转换**”直接得到唯一短码；如果不能（比如需要无序、不可预测），再考虑随机哈希或更复杂的哈希函数。