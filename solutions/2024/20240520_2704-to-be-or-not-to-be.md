# #2704. 存在还是不存在 / To Be Or Not To Be

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/to-be-or-not-to-be/)

---

## 题目（英文原版）

**Description**

Write a function expect that helps developers test their code. It should take in any value val and return an object with the following two functions.

**Examples**

**Example 1:**

```
Input: func = () => expect(5).toBe(5)
Output: {"value": true}
Explanation: 5 === 5 so this expression returns true.
```

**Example 2:**

```
Input: func = () => expect(5).toBe(null)
Output: {"error": "Not Equal"}
Explanation: 5 !== null so this expression throw the error "Not Equal".
```

**Example 3:**

```
Input: func = () => expect(5).notToBe(null)
Output: {"value": true}
Explanation: 5 !== null so this expression returns true.
```

---

## 题目（中文翻译）

编写一个函数 **expect**，帮助开发者对代码进行断言（assert）。该函数接受任意值 **val**，并返回一个对象，对象中包含以下两个函数：

- `toBe(expected)`：当 **val** 与 **expected** 全等（`===`）时返回 `{ "value": true }`，否则抛出错误对象 `{ "error": "Not Equal" }`。
- `notToBe(unexpected)`：当 **val** 与 **unexpected** 不全等（`!==`）时返回 `{ "value": true }`，否则抛出错误对象 `{ "error": "Equal" }`。

### 示例

**示例 1**  
```javascript
func = () => expect(5).toBe(5)
```
**输出**  
```json
{"value": true}
```
**解释**：`5 === 5` 成立，表达式返回 `true`。

**示例 2**  
```javascript
func = () => expect(5).toBe(null)
```
**输出**  
```json
{"error": "Not Equal"}
```
**解释**：`5 !== null`，表达式抛出错误 `"Not Equal"`。

**示例 3**  
```javascript
func = () => expect(5).notToBe(null)
```
**输出**  
```json
{"value": true}
```
**解释**：`5 !== null` 成立，表达式返回 `true`。

### 约束条件

- 无特殊约束。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的目标是实现一个**简单的断言库**，类似 Jest、Mocha 里常见的 `expect`。  
我们只需要：

1. 接收任意值 `val`。  
2. 返回一个对象，这个对象提供两个方法：  
   - `toBe(expected)`：如果 `val === expected`，返回 `{value: true}`；否则抛出错误，返回 `{error: "Not Equal"}`。  
   - `notToBe(unexpected)`：如果 `val !== unexpected`，返回 `{value: true}`；否则抛出错误，返回 `{error: "Equal"}`（这里可以自行决定错误信息，只要和示例对齐即可）。

> **类比**：`expect` 像一本**词典**，我们把“要比较的值”当成**关键词**，`toBe`/`notToBe` 就是查找这本词典时的**页码**，看是否匹配。

实现思路非常直接：  
- 用 `===`（严格相等）比较两个值。  
- 根据比较结果返回不同的字典（Python 中的 `dict`），或者抛出异常后捕获再返回错误信息。

因为只做一次比较，**正确性**显而易见：如果相等就返回 `true`，不相等就返回错误。

#### 代码（Python）

```python
def expect(val):
    """
    返回一个包含 toBe 与 notToBe 两个方法的对象（这里用 dict 包装成简单的类）。
    """
    class _Expect:
        def __init__(self, actual):
            self.actual = actual   # 保存用户传入的实际值

        def toBe(self, expected):
            """判断 actual 与 expected 是否全等"""
            if self.actual == expected:          # 使用 Python 的 ==（相当于 JS 的 ===）
                return {"value": True}
            # 不相等则抛出错误，外层捕获后返回错误信息
            raise AssertionError("Not Equal")

        def notToBe(self, unexpected):
            """判断 actual 与 unexpected 是否不相等"""
            if self.actual != unexpected:
                return {"value": True}
            raise AssertionError("Equal")

    # 为了让调用者捕获异常并返回统一的 dict，我们在外层做一次 try/except 包装
    try:
        return _Expect(val)          # 直接返回对象，后续调用其方法
    except AssertionError as e:     # 这里其实不会触发，因为对象构造本身不抛异常
        return {"error": str(e)}
```

> 使用方式示例（对应题目示例）  
> ```python
> # 示例 1
> result = expect(5).toBe(5)               # {"value": True}
> 
> # 示例 2
> try:
>     result = expect(5).toBe(None)
> except AssertionError as e:
>     result = {"error": str(e)}          # {"error": "Not Equal"}
> 
> # 示例 3
> result = expect(5).notToBe(None)        # {"value": True}
> ```

#### 复杂度

- **时间复杂度**：`O(1)` — 只做一次常数时间的相等比较，跟输入大小无关。  
- **空间复杂度**：`O(1)` — 只保存了一个实际值和返回的极小对象，所占空间是常数级。

---

### 2. 最优解

#### 思路  

从暴力解看，**唯一的瓶颈**就是每次调用 `toBe` / `notToBe` 都要手动写 `if … raise …`，代码稍显冗余。  
最优解的关键在于：

1. **统一异常处理**：把比较过程放在 `try/except` 中，让两种方法共享同一套错误捕获逻辑，避免重复代码。  
2. **利用闭包**：直接在 `expect` 函数内部定义两个内部函数（`toBe`、`notToBe`），它们可以“记住”外层的 `val`，不需要额外的类包装。这样实现更简洁，且同样是 `O(1)`。

> **类比**：把 `expect` 想成一个装有“钥匙”（`val`）的盒子，盒子里放了两把钥匙（`toBe`、`notToBe`），每次使用钥匙时，只需要把盒子打开一次，钥匙自然能记住盒子里的那把钥匙（值）。

#### 代码（Python）

```python
def expect(val):
    """
    使用闭包实现的轻量级 expect。
    返回一个 dict，内部包含两个可直接调用的函数对象。
    """
    def toBe(expected):
        """如果相等返回 true，否则返回错误 dict"""
        if val == expected:
            return {"value": True}
        # 直接返回错误 dict，而不是抛异常，保持 API 简洁
        return {"error": "Not Equal"}

    def notToBe(unexpected):
        """如果不相等返回 true，否则返回错误 dict"""
        if val != unexpected:
            return {"value": True}
        return {"error": "Equal"}

    # 把两个函数包装进一个对象返回，使用时可以像 expect(5).toBe(5) 那样调用
    return type("Expectation", (), {"toBe": toBe, "notToBe": notToBe})()
```

> 使用方式（与示例保持一致）  
> ```python
> # 示例 1
> result = expect(5).toBe(5)               # {"value": True}
> 
> # 示例 2
> result = expect(5).toBe(None)            # {"error": "Not Equal"}
> 
> # 示例 3
> result = expect(5).notToBe(None)         # {"value": True}
> ```

#### 复杂度

- **时间复杂度**：`O(1)` — 仍然只有一次常数时间的比较，没有额外循环或递归。  
- **空间复杂度**：`O(1)` — 只创建了两个函数对象和一个极小的返回字典，空间使用恒定。

与暴力解相比，最优解在 **代码行数** 与 **可读性** 上更好，时间/空间表现完全相同。

---

## 心得

- **核心技巧**：闭包（closure）与函数对象的组合使用，能够在不创建显式类的情况下保存外层变量。  
- **适用题型**：  
  1. 实现简易的测试/断言框架（如本题）。  
  2. 需要返回多个关联操作的“工厂函数”（Factory Function）场景。  
  3. 需要在函数内部保存状态的高阶函数（如缓存 decorator）。  
- **一句话总结**：`expect` 本质是把值“装进盒子”，盒子里放两把钥匙（`toBe` / `notToBe`），利用闭包即可轻松实现。

---

## 反思

- **第一反应**：直接写一个类，里面实现 `toBe`、`notToBe`，每次比较后抛异常或返回字典。  
- **最容易踩的坑**：  
  - 忘记使用 **严格相等**（在 Python 中使用 `==` 已经足够，因为题目不涉及类型强制转换）。  
  - 返回值格式不统一：示例要求返回 `{"value": true}` 或 `{"error": "..."}，需要确保键名、布尔值的大小写与示例一致。  
- **下次类似题的第一步**：先明确“要返回什么对象”，再决定是用类还是闭包实现；若只需保存一个值并提供少量方法，闭包往往是最简洁的选择。