# #2666. 只允许调用一次的函数 / Allow One Function Call

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/allow-one-function-call/)

---

## 题目（英文原版）

**Description**

Given a function fn, return a new function that is identical to the original function except that it ensures fn is called at most once.

**Examples**

**Example 1:**

```
Input: fn = (a,b,c) => (a + b + c), calls = [[1,2,3],[2,3,6]]
Output: [{"calls":1,"value":6}]
Explanation:
const onceFn = once(fn);
onceFn(1, 2, 3); // 6
onceFn(2, 3, 6); // undefined, fn was not called
```

**Example 2:**

```
Input: fn = (a,b,c) => (a * b * c), calls = [[5,7,4],[2,3,6],[4,6,8]]
Output: [{"calls":1,"value":140}]
Explanation:
const onceFn = once(fn);
onceFn(5, 7, 4); // 140
onceFn(2, 3, 6); // undefined, fn was not called
onceFn(4, 6, 8); // undefined, fn was not called
```

**Constraints**

- calls is a valid JSON array
- 1 <= calls.length <= 10
- 1 <= calls[i].length <= 100
- 2 <= JSON.stringify(calls).length <= 1000

---

## 题目（中文翻译）

**描述**  
给定一个函数 `fn`，返回一个新函数，该函数与原函数完全相同，唯一的区别是它确保 `fn` 最多只会被调用一次。

**示例 1**  
**示例 2**  
**约束条件**  

- `calls` 是一个合法的 JSON 数组  
- `1 <= calls.length <= 10`  
- `1 <= calls[i].length <= 100`  
- `2 <= JSON.stringify(calls).length <= 1000`

**示例**

**示例 1:**  
```json
Input: fn = (a,b,c) => (a + b + c), calls = [[1,2,3],[2,3,6]]
Output: [{"calls":1,"value":6}]
```
**解释:**  
```js
const onceFn = once(fn);
onceFn(1, 2, 3); // 6
onceFn(2, 3, 6); // undefined, fn 未被调用
```

**示例 2:**  
```json
Input: fn = (a,b,c) => (a * b * c), calls = [[5,7,4],[2,3,6],[4,6,8]]
Output: [{"calls":1,"value":140}]
```
**解释:**  
```js
const onceFn = once(fn);
onceFn(5, 7, 4); // 140
onceFn(2, 3, 6); // undefined, fn 未被调用
onceFn(4, 6, 8); // undefined, fn 未被调用
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：每次调用返回的函数时，都把「这次是否已经调用过」的信息记录下来，然后在后面的调用里去**遍历**这些记录，看函数是否已经被调用过。  
- **数据结构**：我们可以用一个列表 `called` 来保存每一次的调用标记（`True` 表示已经调用）。列表就像一本笔记本，往里写一行行记录。  
- **为什么正确**：只要在每次调用前检查列表里是否已经有 `True`，如果有就直接返回 `None`（相当于 `undefined`），否则就执行原函数并把 `True` 加进去。这样就保证了原函数最多只会执行一次。  
- **时间/空间复杂度**：  
  - 每一次调用都要遍历整个列表来判断是否已经调用过，最坏情况需要查看 `k` 次（`k` 为已经调用的次数），所以时间复杂度是 **O(k)**。如果总共调用 `n` 次，整体时间是 **O(n²)**（因为 1+2+…+n≈n²/2）。  
  - 列表里会保存每一次的调用标记，最多保存 `n` 个布尔值，空间复杂度是 **O(n)**。  
> **大白话**：把每一次的「是否已经调用」都写在纸上，查时要把纸一页页翻过去，纸越多查得越慢，纸越多占的空间也越大。

#### 代码（Python）

```python
def once_bruteforce(fn):
    """
    暴力实现：用列表记录每一次是否已经调用过。
    """
    # 用一个列表保存调用记录，类似“笔记本”
    called_records = []          # 每一次调用后会往里放一个 True

    def wrapper(*args, **kwargs):
        # 逐个检查列表里是否已经有 True（即已经调用过）
        for flag in called_records:
            if flag:              # 找到一次已经调用的记录
                return None       # 直接返回 None，等价于 JavaScript 的 undefined

        # 这里说明还没有调用过，执行原函数
        result = fn(*args, **kwargs)

        # 记录本次调用，后面的调用会看到这个 True
        called_records.append(True)

        return result

    return wrapper
```

#### 复杂度

- **时间复杂度**：O(n²)（每一次调用都要遍历已有的调用记录，累计会形成二次方增长）  
  > *含义解释*：如果你总共调用 10 次，最坏情况下要检查 1+2+…+10=55 次，比直接一次检查要慢很多。  
- **空间复杂度**：O(n)（需要保存每一次的调用标记）  
  > *含义解释*：调用越多，记的纸就越多，最多要保存和调用次数一样多的布尔值。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈在于每次都要遍历整个记录列表**。其实我们只需要知道“是否已经调用过一次”，这是一种**二元状态**（未调用 / 已调用），不必保存所有历史。  

**优化步骤**：

1. **把列表换成一个布尔变量** `has_been_called`，它只有 `True`（已经调用）或 `False`（未调用）两种状态。  
2. 每次调用时，先检查这个变量：  
   - 为 `False` 时，说明是第一次调用，执行原函数并把变量设为 `True`。  
   - 为 `True` 时，直接返回 `None`（不再调用原函数）。  
3. 这样每一次检查只需要 **一次判断**，时间是 **O(1)**，空间只需要保存一个布尔值，也是 **O(1)**。  

**类比**：这就像在厨房的门口贴一张纸条 “已经开锅”。第一次开锅时把纸条贴上，后面再想开锅时只要看纸条有没有就行，根本不需要回顾过去的每一次操作。

#### 代码（Python）

```python
def once(fn):
    """
    最优实现：只用一个布尔变量记录是否已经调用过。
    """
    # 初始状态为未调用
    has_been_called = False      # 相当于“门口的纸条”，False 表示还没有贴

    def wrapper(*args, **kwargs):
        nonlocal has_been_called   # 声明要修改外层变量

        if has_been_called:        # 已经调用过一次了
            return None            # 直接返回 None（相当于 undefined）

        # 第一次调用，执行原函数
        result = fn(*args, **kwargs)

        # 标记已经调用
        has_been_called = True

        return result

    return wrapper
```

#### 复杂度

- **时间复杂度**：O(1) — 每一次调用只做一次布尔判断，时间固定不变。  
  > *含义解释*：不管你调用多少次，检查“是否已经调用”只需要一步，就像只看一张纸条，不需要翻阅任何记录。  
- **空间复杂度**：O(1) — 只保存一个布尔变量 `has_been_called`，占用的内存固定。  
  > *含义解释*：不管调用多少次，都只需要一张纸条，空间不会随调用次数增长。

---

## 心得

- **核心技巧**：使用**闭包**（在函数内部保存状态）配合**布尔标记**实现“一次性”调用。  
- **适用的题型**：  
  1. “只执行一次”类的高阶函数（如 `once`、`memoize` 的第一次调用）。  
  2. 需要记录**全局状态**的装饰器（如只能执行一次的日志记录器）。  
  3. 防抖/节流（debounce / throttle）实现的状态判断。  
- **一句话总结解题钥匙**：**只需要一个“是否已经执行过”的布尔标记**，把它放进闭包里即可。

---

## 反思

- **第一反应**：看到 “确保函数最多调用一次”，自然想到“记录已经调用的次数”，于是想到用列表或计数器来保存历史。  
- **最容易踩的坑**：  
  - 忘记在内部函数里使用 `nonlocal` 声明，否则对外层布尔变量的修改只会影响局部副本，导致仍然可以多次调用。  
  - 返回值要和题目保持一致：第一次调用返回原函数的返回值，之后返回 `None`（对应 JavaScript 的 `undefined`）。  
- **下次遇到同类题**：第一步先思考“状态到底只有几种”，如果是 **两种**（未调用 / 已调用），就直接用 **布尔变量**，不必维护更复杂的数据结构。