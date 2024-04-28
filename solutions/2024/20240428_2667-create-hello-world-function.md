# #2667. 创建 Hello World 函数 / Create Hello World Function

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/create-hello-world-function/)

---

## 题目（英文原版）

**Description**



**Examples**

**Example 1:**

```
Input: args = []
Output: "Hello World"
Explanation:
const f = createHelloWorld();
f(); // "Hello World"

The function returned by createHelloWorld should always return "Hello World".
```

**Example 2:**

```
Input: args = [{},null,42]
Output: "Hello World"
Explanation:
const f = createHelloWorld();
f({}, null, 42); // "Hello World"

Any arguments could be passed to the function but it should still always return "Hello World".
```

**Constraints**

- 0 <= args.length <= 10

---

## 题目（中文翻译）

**描述**  
实现一个函数 `createHelloWorld`，它返回的函数在被调用时总是返回字符串 `"Hello World"`，无论传入多少参数。

**示例 1**  
```javascript
Input: args = []
Output: "Hello World"
Explanation:
const f = createHelloWorld();
f(); // "Hello World"
```
返回的函数 `f` 应始终返回 `"Hello World"`。

**示例 2**  
```javascript
Input: args = [{}, null, 42]
Output: "Hello World"
Explanation:
const f = createHelloWorld();
f({}, null, 42); // "Hello World"
```
可以向函数传入任意参数，但它仍然必须始终返回 `"Hello World"`。

**约束条件**  
- `0 <= args.length <= 10`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把 “返回 `'Hello World'` ” 这件事写进一个普通函数里，然后把这个函数交给 `createHelloWorld` 再返回。  
- **数据结构**：这里其实不需要任何复杂的数据结构，只要会写函数就行。  
- **为什么正确**：只要返回的函数每次被调用都执行 `return "Hello World"`，不管传进来多少参数，答案就一定是 `"Hello World"`。  
- **时间/空间复杂度**：函数体里只有一条返回语句，执行一次的时间是常数级别，记作 **O(1)**（也就是“只花很少的时间”，不随输入大小变化）。空间上我们只存了一个函数对象，同样是 **O(1)**（占用的内存不会随参数个数增多而增大）。

#### 代码（Python）

```python
def createHelloWorld():
    """
    返回一个函数 f，调用 f 时不管传入什么参数，都返回 "Hello World"
    """
    def f(*args, **kwargs):      # *args 收集位置参数，**kwargs 收集关键字参数
        return "Hello World"     # 永远返回固定字符串
    return f                      # 把内部函数 f 暴露给外部
```

#### 复杂度

- **时间复杂度**：O(1) —— 只做一次函数对象的创建和返回，执行时间不随输入规模变化。  
- **空间复杂度**：O(1) —— 只保存一个函数对象，占用的内存是固定的。

---

### 2. 最优解

#### 思路  
从暴力解可以看到，真正的“慢点”并不存在——整个过程本身就是 **常数时间**、**常数空间**。唯一需要注意的是：  
- 若只写 `def f(): return "Hello World"`，外部调用 `f(1,2)` 时会因为参数不匹配抛异常。  
- 为了让函数 **无论收到多少参数都能正常工作**，必须使用可变参数 `*args`（收集所有位置参数）和 `**kwargs`（收集所有关键字参数）。这就是把“接受任何东西”这件事抽象成“把它们装进一个袋子”，然后我们根本不去看袋子里有什么。

因此，**最优解** 与直觉解在实现上完全相同，只是把“接受任意参数”这一步写得更明确、更具可读性。

#### 代码（Python）

```python
def createHelloWorld():
    """
    生成并返回一个函数 f。
    f 可以接受任意数量和类型的参数，却始终返回同一个字符串 "Hello World"。
    """
    # 使用 *args 和 **kwargs 捕获所有可能的调用方式
    def f(*args, **kwargs):
        # 不管 args、kwargs 长啥样，都不做任何处理，直接返回固定结果
        return "Hello World"

    # 把内部函数对象返回给调用者
    return f
```

#### 复杂度

- **时间复杂度**：O(1) —— 创建函数对象和返回的操作次数都是常数，和传入参数的多少无关。  
- **空间复杂度**：O(1) —— 只占用一个函数对象的内存，同样不随参数个数变化。

---

## 心得

- **核心技巧**：使用可变参数 `*args` 与 `**kwargs` 捕获任意调用方式，使函数对输入“免疫”。  
- **适用的题型**：  
  1. 需要返回一个“占位”函数或回调函数的题目（如创建统一的日志函数）。  
  2. 需要实现 “装饰器” 或 “高阶函数” 并且不关心内部参数的场景。  
  3. 需要对外提供统一接口但内部实现固定的 API（比如统一的错误处理函数）。  
- **一句话总结解题钥匙**：**把所有可能的输入“装进袋子”，然后不管袋子里装的什么，直接给出固定答案。**

---

## 反思

- **第一反应**：看到 “返回一个函数”，立刻想到 **闭包**（函数内部再定义函数并返回）。  
- **最容易踩的坑**：忘记使用 `*args, **kwargs`，导致调用时参数不匹配抛异常。  
- **下次遇到同类题**：先判断返回的函数是否需要 **接受任意参数**，如果是，就立刻在函数定义里加上 `*args, **kwargs`，再实现核心逻辑。