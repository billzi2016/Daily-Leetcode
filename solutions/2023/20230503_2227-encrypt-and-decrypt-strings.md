# #2227. 加密与解密字符串 / Encrypt and Decrypt Strings

> 难度：困难 · 标签：Array、Hash Table、String、Design、Trie · [LeetCode 链接](https://leetcode.com/problems/encrypt-and-decrypt-strings/)

---

## 题目（英文原版）

**Description**

You are given a character array keys containing unique characters and a string array values containing strings of length 2. You are also given another string array dictionary that contains all permitted original strings after decryption. You should implement a data structure that can encrypt or decrypt a 0-indexed string.
A string is encrypted with the following process:
Note that in case a character of the string is not present in keys, the encryption process cannot be carried out, and an empty string "" is returned.
A string is decrypted with the following process:
Implement the Encrypter class:

**Examples**

**Example 1:**

```
Input
["Encrypter", "encrypt", "decrypt"]
[[['a', 'b', 'c', 'd'], ["ei", "zf", "ei", "am"], ["abcd", "acbd", "adbc", "badc", "dacb", "cadb", "cbda", "abad"]], ["abcd"], ["eizfeiam"]]
Output
[null, "eizfeiam", 2]

Explanation
Encrypter encrypter = new Encrypter([['a', 'b', 'c', 'd'], ["ei", "zf", "ei", "am"], ["abcd", "acbd", "adbc", "badc", "dacb", "cadb", "cbda", "abad"]);
encrypter.encrypt("abcd"); // return "eizfeiam". 
                           // 'a' maps to "ei", 'b' maps to "zf", 'c' maps to "ei", and 'd' maps to "am".
encrypter.decrypt("eizfeiam"); // return 2. 
                              // "ei" can map to 'a' or 'c', "zf" maps to 'b', and "am" maps to 'd'. 
                              // Thus, the possible strings after decryption are "abad", "cbad", "abcd", and "cbcd". 
                              // 2 of those strings, "abad" and "abcd", appear in dictionary, so the answer is 2.
```

**Constraints**

- 1 <= keys.length == values.length <= 26
- values[i].length == 2
- 1 <= dictionary.length <= 100
- 1 <= dictionary[i].length <= 100
- All keys[i] and dictionary[i] are unique.
- 1 <= word1.length <= 2000
- 2 <= word2.length <= 200
- All word1[i] appear in keys.
- word2.length is even.
- keys, values[i], dictionary[i], word1, and word2 only contain lowercase English letters.
- At most 200 calls will be made to encrypt and decrypt in total.

---

## 题目（中文翻译）

**描述**  
给定一个字符数组 `keys`（character array），其中的字符互不相同；再给定一个字符串数组 `values`（string array），其中每个字符串的长度均为 2。还有一个字符串数组 `dictionary`（dictionary），它包含所有在解密后被允许出现的原始字符串。请实现一个数据结构，能够对 **0 索引** 的字符串进行加密或解密。

**加密过程**  
- 对于待加密的字符串 `word1` 的每个字符 `c`，在 `keys` 中找到对应的下标 `i`（即 `keys[i] == c`），并用 `values[i]` 替换该字符。  
- 将所有得到的长度为 2 的子串依次拼接，得到最终的加密结果并返回。  

> 注意：如果 `word1` 中出现的字符在 `keys` 中不存在，则无法完成加密，返回空串 `""`。

**解密过程**  
- 将待解密的字符串 `word2` 按每两个字符划分为若干子串（长度均为 2）。  
- 对于每个子串 `s`，找出所有满足 `values[i] == s` 的字符 `keys[i]`，这些字符都是 `s` 可能对应的原字符。  
- 统计在 `dictionary` 中，有多少个字符串可以通过对每个子串分别选择上述可能的原字符而组成，返回该计数。

**实现 `Encrypter` 类**  

```cpp
class Encrypter {
public:
    Encrypter(vector<char> keys, vector<string> values, vector<string> dictionary);
    string encrypt(string word1);
    int decrypt(string word2);
};
```

**示例**  

``` 
示例 1:
Input
["Encrypter", "encrypt", "decrypt"]
[[['a', 'b', 'c', 'd'], ["ei", "zf", "ei", "am"], ["abcd", "acbd", "adbc", "badc", "dacb", "cadb", "cbda", "abad"]], ["abcd"], ["eizfeiam"]]
Output
[null, "eizfeiam", 2]

Explanation
Encrypter encrypter = new Encrypter(
    ['a', 'b', 'c', 'd'],
    ["ei", "zf", "ei", "am"],
    ["abcd", "acbd", "adbc", "badc", "dacb", "cadb", "cbda", "abad"]
);
encrypter.encrypt("abcd");   // 返回 "eizfeiam"
encrypter.decrypt("eizfeiam"); // 返回 2，因为在 dictionary 中有两条记录 "abcd" 和 "acbd" 能映射到该密文
```

**约束条件**  

- `1 <= keys.length == values.length <= 26`
- `values[i].length == 2`
- `1 <= dictionary.length <= 100`
- `1 <= dictionary[i].length <= 100`
- 所有 `keys[i]` 与 `dictionary[i]` 中的字符均唯一
- `1 <= word1.length <= 2000`
- `2 <= word2.length <= 200`
- 所有 `word1[i]` 均出现在 `keys` 中
- `word2.length` 为偶数
- `keys、values[i]、dictionary[i]、word1、word2` 仅由小写英文字母组成
- 最多会调用 `encrypt` 与 `decrypt` 共计 200 次

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

- **加密**：把每个字符 `c` 用 `values[i]` 替换，其中 `keys[i] == c`。这相当于把字符当成“单词”，`keys` 像一本**查字典**，`c` 是词，`values[i]` 是对应的页码（长度为 2 的字符串）。只要把原字符串的每个字符在字典里找到了对应的页码，依次拼接起来就是密文。  
- **解密**：最直接的办法是把 **所有可能的原文**（即 `dictionary` 中的单词）逐个加密，然后和给出的密文比较。如果相同，就说明这条原文是合法的。把所有匹配的原文计数，就是 `decrypt` 要返回的答案。

> 这一步是“暴力枚举”。因为题目保证 `dictionary` 的大小最多只有 100，单词长度最多 100，直接遍历一次完全可以接受（虽然不是最优）。

**正确性**  
- 加密时我们严格按照题目给出的映射表进行字符替换，所以得到的密文一定是唯一的。  
- 解密时我们把所有合法原文都加密一遍，只有真正能得到目标密文的原文才会被计数，因而答案一定准确。

**复杂度**  
- 加密：遍历 `word1` 的每个字符一次，时间是 `O(|word1|)`，空间只用一个哈希表 `key → value`，即 `O(|keys|)`（至多 26）。  
- 解密（暴力）：遍历整个 `dictionary`，对每个单词再调用一次加密。设 `D = dictionary.length`，`L` 为单词的平均长度，则时间是 `O(D * L)`，空间仍然是哈希表的大小 `O(|keys|)`。  
  - 用大白话说，假设字典里有 100 条单词，每条单词长 100，最坏要做 10 000 次字符替换，这在机器眼里是“几千步”，还能接受。

#### 代码（Python）

```python
from typing import List

class Encrypter:
    def __init__(self, keys: List[str], values: List[str], dictionary: List[str]):
        # 把 keys 和 values 建成哈希表，类似“查字典”
        self.enc_map = {k: v for k, v in zip(keys, values)}
        # 为了快速判断一个明文是否在 dictionary 中，存成集合
        self.dict_set = set(dictionary)

    # ----------------- 1. 暴力加密 -----------------
    def encrypt(self, word1: str) -> str:
        """把 word1 中每个字符映射成对应的 2 字符串，拼接后返回。"""
        res = []
        for ch in word1:
            if ch not in self.enc_map:          # 找不到映射就直接返回空串
                return ""
            res.append(self.enc_map[ch])        # 把映射的 2 字符串加入结果
        return "".join(res)                     # 合并成最终密文

    # ----------------- 2. 暴力解密 -----------------
    def decrypt(self, word2: str) -> int:
        """
        对 dictionary 中的每个单词进行加密，统计有多少个等于 word2。
        这里直接使用上面的 encrypt 方法。
        """
        cnt = 0
        for w in self.dict_set:                 # 只遍历合法的原文
            if self.encrypt(w) == word2:        # 若加密后等于目标密文，计数
                cnt += 1
        return cnt
```

#### 复杂度

- **时间复杂度**  
  - `encrypt`：`O(|word1|)`，因为只遍历一次字符串。  
  - `decrypt`：`O(D * L)`，其中 `D` 为字典大小（≤100），`L` 为单词平均长度（≤100）。  
- **空间复杂度**  
  - `O(|keys|)`（哈希表），最多 26 条映射，几乎可以忽略不计。

---

### 2. 最优解

#### 思路  

从暴力解出发，慢的地方显而易见：**每次解密都要遍历完整个字典并重新加密**。这相当于每次都在重复做同样的工作。

**关键观察**  
- 加密是一个 **确定性** 的映射：同一个明文总会得到同一个密文。  
- 因此，所有可能的明文在第一次遍历字典时就可以一次性算出它们对应的密文。把这些密文与它们出现的次数记下来，以后只要查询 `word2`，直接返回计数即可，**不需要再遍历字典**。

**实现细节**  

1. **构建映射表** `char → value`（同暴力解）。  
2. **预处理字典**：遍历 `dictionary`，把每个单词加密后得到 `cipher`，在哈希表 `cipher_cnt` 中记录 `cipher` 出现的次数。  
   - 这里的哈希表相当于“逆向查字典”：密文是“词”，出现次数是“页码”。  
3. **加密** 仍然使用步骤 1 中的哈希表，时间不变。  
4. **解密**：只要在 `cipher_cnt` 中查一次表，若不存在返回 0，若存在返回对应的计数。整个过程 **O(1)**。

> 如果你对“哈希表”不熟悉，可以把它想成一个 **大抽屉柜**，每个抽屉都有一个唯一的标签（密文），我们把对应的计数放进去。查找时只需要打开对应的抽屉，时间几乎为常数。

#### 代码（Python）

```python
from typing import List, Dict

class Encrypter:
    def __init__(self, keys: List[str], values: List[str], dictionary: List[str]):
        # 1. 正向映射：字符 -> 两字符密文
        self.enc_map: Dict[str, str] = {k: v for k, v in zip(keys, values)}

        # 2. 逆向映射：密文 -> 出现次数（预处理字典）
        self.cipher_cnt: Dict[str, int] = {}
        for word in dictionary:
            cipher = self._encrypt_word(word)   # 只在这里加密一次
            if cipher:                          # 所有字典单词必定能加密
                self.cipher_cnt[cipher] = self.cipher_cnt.get(cipher, 0) + 1

    # ----------------- 公共的加密子函数 -----------------
    def _encrypt_word(self, word: str) -> str:
        """内部使用的加密实现，返回空串代表字符缺失（本题字典里不会出现）"""
        res = []
        for ch in word:
            if ch not in self.enc_map:          # 安全检查
                return ""
            res.append(self.enc_map[ch])
        return "".join(res)

    # ----------------- 对外的 encrypt -----------------
    def encrypt(self, word1: str) -> str:
        """题目要求的加密接口，直接调用内部实现"""
        return self._encrypt_word(word1)

    # ----------------- 对外的 decrypt -----------------
    def decrypt(self, word2: str) -> int:
        """
        只需要在预处理好的哈希表中查一次表，时间 O(1)。
        若不存在返回 0，存在则返回对应计数。
        """
        return self.cipher_cnt.get(word2, 0)
```

#### 复杂度

- **时间复杂度**  
  - 构造阶段（`__init__`）：遍历 `dictionary` 一次，每个单词加密 `O(L)`，整体 `O(D * L)`（与暴力解相同，只是只做一次）。  
  - `encrypt`：`O(|word1|)`，仍然是线性遍历。  
  - `decrypt`：`O(1)`，只做一次哈希表查找。  
  - 相比暴力解，**解密从 `O(D*L)` 降到 `O(1)`**，在多次调用 `decrypt` 时收益巨大（最多 200 次调用）。

- **空间复杂度**  
  - 正向映射 `O(|keys|)`（≤26）。  
  - 逆向映射 `cipher_cnt` 最多存 `D` 条记录，空间 `O(D)`（≤100），非常小。  
  - 总体仍然是线性额外空间，且常数极小。

---

## 心得

- **核心技巧**：**预处理 + 哈希计数**（或 Trie 剪枝）。把一次性可以算出的信息提前存下来，后续查询就能做到常数时间。  
- **适用场景**  
  1. “**一遍遍历后多次查询**” 的问题，例如 LeetCode 421. Maximum XOR of Two Numbers in an Array（使用 Trie 预处理）。  
  2. “**把映射关系反向存储**” 的场景，如 299. Bulls and Cows（统计出现次数）。  
- **一句话总结**：**把所有可能的密文先算好并记住它们出现的次数，解密时直接查表**。

---

## 反思

- **第一反应**：看到“加密/解密”关键词，立刻想到哈希表映射；随后想到最直接的办法是遍历字典逐个比较。  
- **最容易踩的坑**  
  - **字符缺失**：如果加密时出现不在 `keys` 中的字符，需要立刻返回空串，否则会出现 KeyError。  
  - **重复密文**：不同原文可能映射到同一个密文，计数时必须累计，而不是只记录是否出现。  
  - **字典大小**：虽然本题字典只有 100 条，但如果忘记预处理，`decrypt` 每次都遍历会导致 200 次调用的时间累积到 20 000 次字符替换，仍能 AC，但不符合“最优”。  
- **下次遇到同类题**：第一步先问自己——“这道题是否会多次查询同一批数据？”如果答案是“是”，就考虑 **预处理**（哈希、Trie、前缀和等）把查询成本压到常数。