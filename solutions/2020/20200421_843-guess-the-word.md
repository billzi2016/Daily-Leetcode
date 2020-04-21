# #843. 猜单词 / Guess the Word

> 难度：困难 · 标签：Array、Math、String、Interactive、Game Theory · [LeetCode 链接](https://leetcode.com/problems/guess-the-word/)

---

## 题目（英文原版）

**Description**

You are given an array of unique strings words where words[i] is six letters long. One word of words was chosen as a secret word.
You are also given the helper object Master. You may call Master.guess(word) where word is a six-letter-long string, and it must be from words. Master.guess(word) returns:
There is a parameter allowedGuesses for each test case where allowedGuesses is the maximum number of times you can call Master.guess(word).
For each test case, you should call Master.guess with the secret word without exceeding the maximum number of allowed guesses. You will get:
The test cases are generated such that you can guess the secret word with a reasonable strategy (other than using the bruteforce method).

**Examples**

**Example 1:**

```
Input: secret = "acckzz", words = ["acckzz","ccbazz","eiowzz","abcczz"], allowedGuesses = 10
Output: You guessed the secret word correctly.
Explanation:
master.guess("aaaaaa") returns -1, because "aaaaaa" is not in wordlist.
master.guess("acckzz") returns 6, because "acckzz" is secret and has all 6 matches.
master.guess("ccbazz") returns 3, because "ccbazz" has 3 matches.
master.guess("eiowzz") returns 2, because "eiowzz" has 2 matches.
master.guess("abcczz") returns 4, because "abcczz" has 4 matches.
We made 5 calls to master.guess, and one of them was the secret, so we pass the test case.
```

**Example 2:**

```
Input: secret = "hamada", words = ["hamada","khaled"], allowedGuesses = 10
Output: You guessed the secret word correctly.
Explanation: Since there are two words, you can guess both.
```

**Constraints**

- 1 <= words.length <= 100
- words[i].length == 6
- words[i] consist of lowercase English letters.
- All the strings of wordlist are unique.
- secret exists in words.
- 10 <= allowedGuesses <= 30

---

## 题目（中文翻译）

你得到一个由唯一字符串（unique strings）组成的数组 `words`，其中 `words[i]` 的长度都是 **6**。`words` 中的某个单词被选为 **秘密单词**（secret word）。  

同时你会得到一个帮助对象 `Master`。你可以调用 `Master.guess(word)`，其中 `word` 必须是长度为 **6** 且来自 `words`。`Master.guess(word)` 会返回一个整数，表示 `word` 与秘密单词在相同位置上字符相同的数量。  

每个测试用例都有一个参数 `allowedGuesses`，它表示你最多可以调用 `Master.guess(word)` 的次数。  

对于每个测试用例，你需要在不超过 `allowedGuesses` 次的调用次数内，使用 `Master.guess` 找到并猜出秘密单词。题目保证存在一种合理的策略（不依赖暴力枚举）能够在给定的次数限制内完成猜测。

**示例 1**  

**示例 2**  

**约束条件**  

- `1 <= words.length <= 100`
- `words[i].length == 6`
- `words[i]` 只包含小写英文字母。
- `words` 中的所有字符串互不相同。
- `secret` 必然存在于 `words` 中。
- `10 <= allowedGuesses <= 30`

**示例**

**示例 1**  
```
Input: secret = "acckzz", words = ["acckzz","ccbazz","eiowzz","abcczz"], allowedGuesses = 10
Output: You guessed the secret word correctly.
Explanation:
master.guess("aaaaaa") returns -1, because "aaaaaa" is not in wordlist.
master.guess("acckzz") returns 6, because "acckzz" is secret and has all 6 matches.
master.guess("ccbazz") returns 3, because "ccbazz" has 3 matches.
master.guess("eiowzz") returns 2, because "eiowzz" has 2 matches.
master.guess("abcczz") returns 4, because "abcczz" has 4 matches.
We made 5 calls to master.guess, and one of them was the secret, so we pass the test case.
```

**示例 2**  
```
Input: secret = "hamada", words = ["hamada","khaled"], allowedGuesses = 10
Output: You guessed the secret word correctly.
Explanation: Since there are two words, you can guess both.
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是「一次把所有候选单词都猜一遍，直到猜中为止」。  
- **数据结构**：我们只需要把 `words` 列表原封不动地保存下来，随后在循环里逐个取出。  
- **生活化类比**：把 `words` 想成一本装满了不同密码的「密码本」，我们把每个密码都拿出来试一遍，就像把钥匙孔一个个尝试打开门。  
- **为什么正确**：题目保证 secret 必定在 `words` 中，只要我们把每个单词都递交给 `Master.guess`，终究会遇到 secret，`guess` 会返回 6（全部字符匹配），我们就成功了。  

显然，这种方法**不考虑次数限制**——如果 `words` 长度是 100，而 `allowedGuesses` 只有 10，就会直接超限。它只能作为概念验证或最坏情况的基准。

#### 代码（Python）

```python
def findSecretWord_bruteforce(words, master):
    """
    暴力解：把 wordlist 中的每个单词都尝试一次
    参数
        words  : List[str]，所有候选单词（长度均为 6）
        master : 提供 guess(word) 方法的对象
    """
    for w in words:                     # 逐个遍历 wordlist
        matches = master.guess(w)       # 调用接口，返回匹配字符数
        if matches == 6:                # 6 表示全部字符相同，即猜对了
            return                      # 成功退出
    # 根据题目假设，这里永远不可能走到，因为 secret 必在 words 中
```

#### 复杂度

- **时间复杂度**：`O(n)`（`n = len(words)`），因为我们最多调用 `guess` `n` 次。  
  - 大白话：如果有 100 个单词，就最多要敲 100 次键盘。  
- **空间复杂度**：`O(1)`，只用了常数级别的额外变量（循环计数器、返回值），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈**在于「一次把所有候选都猜」，导致猜的次数与候选数量线性相关。  
我们需要一种**“筛选”**机制：每次猜完后，根据 `guess` 返回的匹配数把候选集合缩小得更快，从而在很少的步骤内锁定 secret。

下面一步步推导出一种被多数人称为 **“Minimax（最小化最大可能）”** 的策略：

1. **一次猜完，得到匹配数**  
   `Master.guess(word)` 会返回 0~6 之间的整数，表示 `word` 与 secret 在相同位置上相同字符的个数。  
   例如，猜 `"acckzz"`，返回 `3`，说明 secret 与它在恰好 3 个位置相同。

2. **利用返回值过滤候选**  
   假设我们这次猜的是 `cand`，返回值为 `k`，那么 **真正的 secret 必须** 与 `cand` 在恰好 `k` 个位置相同。  
   因此我们可以把 `words` 中 **不满足** 这一条件的单词全部剔除，得到新的候选集合 `next_words`。

3. **怎样挑选 `cand` 才能最快把集合砍得小？**  
   - 对每个可能的猜测 `x`（必须在当前候选集合里），我们可以 **模拟** 如果 secret 与 `x` 匹配数为 `k`，会留下多少单词。  
   - 对同一个 `x`，会产生 0~6 共 7 种不同的 `k`，每种 `k` 对应的留下的单词数我们记为 `group_size(k)`。  
   - **最坏情况**：不管 `guess` 返回哪个 `k`，我们最糟糕的情况是留下的单词数是 `max_k group_size(k)`（即最大的那一组）。  
   - 为了让最坏情况尽可能小，我们在所有 `x` 中挑选 **“最大分组最小”** 的那个。换句话说，**选一个能把候选集合均匀分散** 的猜测。

4. **重复上述过程**，每次都挑选“最优猜测”，最多 10 次（实际测试中 ≤ 6 次即可）就能锁定 secret。

> **核心数据结构**：  
> - **哈希表（字典）**：用于统计不同匹配数对应的分组大小。想象成一本「字典」，键是匹配数（0~6），值是有多少单词落在这个键对应的组。  
> - **列表**：保存当前候选单词集合。

#### 关键概念解释  

- **匹配数（match count）**：两个长度相同的字符串，逐位比较相同字符的数量。比如 `"abcde"` 与 `"abzzz"` 匹配数是 2（前两位相同）。  
- **Minimax**：在对手（这里是“未知的 secret”）可能的所有反应中，先考虑最坏的那一种，然后让最坏的情况尽可能好。这里我们把“对手的反应”抽象为 `guess` 返回的匹配数。

#### 代码（Python）

```python
def findSecretWord(words, master):
    """
    最优解：基于 Minimax 思路的迭代筛选
    参数
        words  : List[str]，所有候选单词（长度均为 6）
        master : 提供 guess(word) 方法的对象
    """
    # 计算两个单词的匹配数，O(6) = O(1)
    def match(w1, w2):
        cnt = 0
        for a, b in zip(w1, w2):   # 逐位比较
            if a == b:
                cnt += 1
        return cnt

    candidates = words[:]          # 当前还能成为 secret 的单词集合

    while candidates:
        # ---------- 1. 为每个可能的猜测计算“最坏分组大小” ----------
        # best_word：当前轮次选出的最优猜测
        # best_score：对应的最坏分组大小（越小越好）
        best_word = None
        best_score = float('inf')

        for w in candidates:       # 只在当前候选里挑
            # 统计 w 与候选集合中每个单词的匹配数分布
            groups = [0] * 7       # indices 0~6，对应不同匹配数的出现次数
            for other in candidates:
                groups[match(w, other)] += 1
            # 该猜测的最坏情况是最大的分组
            worst = max(groups)
            # 取最小的 worst，若相同则随便取第一个
            if worst < best_score:
                best_score = worst
                best_word = w

        # ---------- 2. 用选出的最优猜测向 Master 发起询问 ----------
        guess_result = master.guess(best_word)   # 返回 0~6
        if guess_result == 6:                    # 全部匹配，已猜中
            return

        # ---------- 3. 根据返回值过滤候选集合 ----------
        # 只保留那些与 best_word 匹配数恰好等于 guess_result 的单词
        candidates = [w for w in candidates if match(w, best_word) == guess_result]
        # 按题目设定，循环次数 ≤ allowedGuesses（通常 ≤ 10）
```

> **代码要点注释**  
> - `match` 函数是“哈希表的键”，把两个单词映射到它们的匹配数。  
> - `groups` 数组相当于「字典」：`groups[k]` 记录匹配数为 `k` 的单词有多少个。  
> - `worst = max(groups)` 就是「最坏情况」的大小。我们挑 `worst` 最小的那个 `w`，这就是 Minimax 的核心。

#### 复杂度

- **时间复杂度**：  
  - 外层循环最多执行 `allowedGuesses` 次（≤ 10），记作 `g`。  
  - 每次循环内部要对候选集合做两层遍历：  
    1. 对每个候选 `w`（最多 `n`）统计与其它候选的匹配数 → `O(n²)`。  
    2. 过滤候选集合 → `O(n)`。  
  - 因此整体是 `O(g * n²)`，在最坏情况下 `n = 100`、`g = 10`，约 `10 * 10000 = 1e5` 次基本操作，完全可以在毫秒级跑完。  
  - **大白话**：我们每轮都在「对每两本书做一次比较」——最多 10 轮，所以算下来还是很快。

- **空间复杂度**：`O(n)`  
  - 需要保存候选集合（最多 100 条）以及 `groups` 长度为 7 的数组。  
  - 相比于输入规模，这只是线性增长，几乎可以忽略不计。

---

## 心得

- **核心技巧**：**Minimax 选词 + 匹配数过滤**  
  这道题的难点不在于写代码，而在于「怎样用最少的猜测把搜索空间压到最小」——这正是 Minimax 思想的精髓。

- **适用的题型**  
  1. **Mastermind（颜色猜谜）**：每次给出黑白球数，要求在最少步数内找出隐藏代码。  
  2. **猜数字游戏**（如 4 位数，每位不同，返回多少位相同且位置相同）  
  3. **Wordle**（每轮返回绿、黄、灰）——同样需要利用每次反馈筛选候选。

- **一句话总结解题钥匙**：  
  **“每次都挑出能让最坏情况最小的猜测”，把信息收集效率最大化。**

---

## 反思

- **第一反应**：直接把所有单词依次尝试，忽视了 `allowedGuesses` 的限制。  
- **最容易踩的坑**  
  - **忘记检查返回值为 -1**（不在 wordlist）——在正式交互环境下，`guess` 只接受列表里的单词，若传错会直接报错。  
  - **过滤候选时写错条件**：必须用 `match(word, best_word) == guess_result`，否则可能把真正的 secret 误删。  
  - **误以为一次遍历就能得到最优猜测**：必须对每个候选都统计分组情况，否则选出的猜测可能不是最小化最大分组的。

- **下次遇到同类题的第一步**：  
  **先思考“每次猜测后，我能得到哪些信息？如何利用这些信息把候选集合快速缩小？”**  
  然后再考虑如何在所有可能的猜测中挑选最能“削枝”的那一个——这往往就是 Minimax 或信息论（熵）角度的思考。