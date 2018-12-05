# #193. 有效的电话号码 / Valid Phone Numbers

> 难度：简单 · 标签：Shell · [LeetCode 链接](https://leetcode.com/problems/valid-phone-numbers/)

---

## 题目（英文原版）

**Description**

Given a text file file.txt that contains a list of phone numbers (one per line), write a one-liner bash script to print all valid phone numbers.
You may assume that a valid phone number must appear in one of the following two formats: (xxx) xxx-xxxx or xxx-xxx-xxxx. (x means a digit)
You may also assume each line in the text file must not contain leading or trailing white spaces.
Example:
Assume that file.txt has the following content:
Your script should output the following valid phone numbers:

**Examples**

**Example 1:**

```
987-123-4567
123 456 7890
(123) 456-7890
```

**Example 2:**

```
987-123-4567
(123) 456-7890
```

---

## 题目（中文翻译）

给定一个名为 `file.txt` 的文本文件，其中每行包含一个电话号码 (phone number)（每行一个），请编写一个单行脚本 (one-liner) 的 bash 脚本 (bash script)，输出所有有效的电话号码 (valid phone numbers)。  

你可以假设，一个有效的电话号码必须符合以下两种格式之一：  

- `(xxx) xxx-xxxx`  
- `xxx-xxx-xxxx`  

其中 `x` 表示任意数字。  

另外，假设文件中的每一行都没有前导或尾随的空格。

**示例 1：**  
```
987-123-4567
123 456 7890
(123) 456-7890
```

**示例 2：**  
```
987-123-4567
(123) 456-7890
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是**逐行读取文件**，把每一行的内容和“合法手机号的两种格式”逐个比对，只要匹配成功就把它打印出来。  

- **数据结构**：我们只需要一个 **列表**（list）来暂存所有读取到的行，或者直接在读取的过程中逐行处理。  
- **类比**：把正则表达式想象成 **“字典查词”**——字典的 *key* 是我们要匹配的模式，*value* 是对应的解释（这里不需要返回值，只要能匹配就行）。  
- **为什么正确**：正则表达式 `^\(\d{3}\) \d{3}-\d{4}$` 完全对应第一种格式 `(xxx) xxx-xxxx`，而 `^\d{3}-\d{3}-\d{4}$` 完全对应第二种格式 `xxx-xxx-xxxx`。只要一行匹配其中之一，就说明它符合题目要求。  

#### 代码（Python）

```python
import re

# 两个合法手机号的正则模式（^ 和 $ 表示行首行尾，确保没有多余字符）
PATTERN1 = r'^\(\d{3}\) \d{3}-\d{4}$'   # (123) 456-7890
PATTERN2 = r'^\d{3}-\d{3}-\d{4}$'       # 123-456-7890

def brute_force_print_valid(file_path: str) -> None:
    """
    逐行读取 file_path，若行匹配任意一种合法格式则直接打印。
    """
    with open(file_path, 'r') as f:
        for line in f:
            line = line.rstrip('\n')          # 去掉行末换行符，题目已保证没有前后空格
            if re.match(PATTERN1, line) or re.match(PATTERN2, line):
                print(line)                   # 符合要求，输出

# 示例调用（把 file.txt 换成实际文件名）：
# brute_force_print_valid('file.txt')
```

**关键行解释**  

- `re.match(PATTERN, line)`: 用正则把整行和模式对齐，匹配成功返回对象，否则返回 `None`。  
- `or`：只要满足任意一种格式即为合法。  
- `print(line)`: 直接把合法手机号输出到标准输出，等价于 Bash 中的 `echo`。

#### 复杂度  

- **时间复杂度：`O(n·m)`**  
  - `n` 为文件行数（即手机号数量），`m` 为每行字符数（这里固定为 12~13），因为我们对每行都要跑两次正则匹配。  
  - 大白话：如果文件有 1000 行，就会检查 1000 次，每次检查的工作量是“看这行是不是符合两种格式”。  

- **空间复杂度：`O(1)`**  
  - 只使用了常数级的额外空间（几个正则对象和临时变量），不随行数增长。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈**在于每行都要进行两次正则匹配。虽然正则本身已经很高效，但我们完全可以把两种格式合并成 **一个正则表达式**，一次匹配即可完成判断，这样可以把常数因子减半。  

合并思路：

- 两种格式的共同点是：**全部是数字和特定的分隔符**，只是在是否出现括号以及空格上有区别。  
- 用 `|`（或）把两种模式拼在一起：  
  ```
  ^(\(\d{3}\) \d{3}-\d{4}|\d{3}-\d{3}-\d{4})$
  ```
- 为了让 Python 每次都复用这条模式，**预编译**正则（`re.compile`），这样内部会把模式转换成高效的状态机，只需要一次匹配调用。

#### 代码（Python）

```python
import re

# 合并后的正则，使用非捕获组 (?: ...) 让表达式更简洁
VALID_PHONE_RE = re.compile(r'^(?:\(\d{3}\) \d{3}-\d{4}|\d{3}-\d{3}-\d{4})$')

def optimal_print_valid(file_path: str) -> None:
    """
    使用单个预编译正则一次匹配，打印所有合法手机号。
    """
    with open(file_path, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            # 只需要一次匹配
            if VALID_PHONE_RE.match(line):
                print(line)

# 示例调用：
# optimal_print_valid('file.txt')
```

**关键行解释**  

- `re.compile(...)`: 把正则编译成内部结构，后续 `match` 调用只需要一次解释，速度更快。  
- `(?: ...)`：非捕获组，只是把两种模式括在一起，不产生额外的匹配结果，写法更清晰。  
- `if VALID_PHONE_RE.match(line)`: 单次匹配即可判断合法性。

#### 复杂度  

- **时间复杂度：`O(n·m)`**（与暴力解同阶）  
  - 只是在常数因子上更优：每行只做一次匹配，而不是两次。  
  - 对 1000 行文件来说，匹配次数从 2000 次降到 1000 次，实际运行更快。  

- **空间复杂度：`O(1)`**  
  - 仍然只使用常数级额外空间，只是多了一个预编译的正则对象。  

---

## 心得

- **核心技巧**：**正则表达式的合并与预编译**。把多个相似的模式用 `|` 合并，避免重复匹配。  
- **适用的题型**：  
  1. 多种输入格式的合法性检查（如日期、邮箱、IP 地址）。  
  2. 文本过滤任务（从日志中抽取特定行）。  
  3. 简单的词法分析（把源代码按关键字、标识符分类）。  
- **一句话总结解题钥匙**：**“把所有合法模式写进同一个正则，一次匹配搞定”。**

---

## 反思

- **第一反应**：直接用两条正则分别匹配，写起来最直观。  
- **最容易踩的坑**：  
  - 忘记在正则前后加 `^` 和 `$`，导致子串匹配（如 `123-456-7890abc` 也会被误判为合法）。  
  - 误把空格或换行算进了字符数，导致匹配失败。  
- **下次遇到同类题**：第一步先**列出所有合法模式**，思考它们的相同点与不同点，再**尝试用一个正则把它们合并**，最后**预编译**提升效率。