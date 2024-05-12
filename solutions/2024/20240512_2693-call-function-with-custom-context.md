# #2693. 调用函数并自定义上下文 / Call Function with Custom Context

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/call-function-with-custom-context/)

---

## 题目（英文原版）

**Description**

Enhance all functions to have the callPolyfill method. The method accepts an object obj as its first parameter and any number of additional arguments. The obj becomes the this context for the function. The additional arguments are passed to the function (that the callPolyfill method belongs on).
For example if you had the function:
Calling this function like tax(10, 0.1) will log "The cost of undefined is 11". This is because the this context was not defined.
However, calling the function like tax.callPolyfill({item: "salad"}, 10, 0.1) will log "The cost of salad is 11". The this context was appropriately set, and the function logged an appropriate output.
Please solve this without using the built-in Function.call method.

**Examples**

**Example 1:**

```
function tax(price, taxRate) {
  const totalCost = price * (1 + taxRate);
  console.log(`The cost of ${this.item} is ${totalCost}`);
}
```

**Example 2:**

```
Input:
fn = function add(b) {
  return this.a + b;
}
args = [{"a": 5}, 7]
Output: 12
Explanation:
fn.callPolyfill({"a": 5}, 7); // 12
callPolyfill sets the "this" context to {"a": 5}. 7 is passed as an argument.
```

**Example 3:**

```
Input: 
fn = function tax(price, taxRate) { 
 return `The cost of the ${this.item} is ${price * taxRate}`; 
}
args = [{"item": "burger"}, 10, 1.1]
Output: "The cost of the burger is 11"
Explanation: callPolyfill sets the "this" context to {"item": "burger"}. 10 and 1.1 are passed as additional arguments.
```

**Constraints**

- typeof args[0] == 'object' and args[0] != null
- 1 <= args.length <= 100
- 2 <= JSON.stringify(args[0]).length <= 105

---

## 题目（中文翻译）

**描述**  
为所有函数增强一个 `callPolyfill` 方法。该方法的第一个参数接受一个对象 `obj`，随后可以接受任意数量的额外参数。`obj` 将作为函数的 `this` 上下文（context）。后续的参数会传递给该函数（即 `callPolyfill` 方法所属的函数）。

例如，给定函数：

```js
function tax(price, taxRate) {
  const totalCost = price * (1 + taxRate);
  console.log(`The cost of ${this.item} is ${totalCost}`);
}
```

直接调用 `tax(10, 0.1)` 会输出  
`The cost of undefined is 11`，因为 `this` 上下文未定义。

而使用 `tax.callPolyfill({item: "salad"}, 10, 0.1)` 调用则会输出  
`The cost of salad is 11`，此时 `this` 已正确指向 `{item: "salad"}`，函数得到正确的输出。

**要求**  
请在实现中 **不使用** 内置的 `Function.call` 方法。

**示例 1**  

```js
function tax(price, taxRate) {
  const totalCost = price * (1 + taxRate);
  console.log(`The cost of ${this.item} is ${totalCost}`);
}
```

**示例 2**  

输入  

```js
fn = function add(b) {
  return this.a + b;
}
args = [{"a": 5}, 7]
```

输出  

```
12
```

解释：  
`fn.callPolyfill({"a": 5}, 7); // 12`  
`callPolyfill` 将 `this` 设置为 `{"a": 5}`，并将 `7` 作为参数传入。

**示例 3**  

输入  

```js
fn = function tax(price, taxRate) { 
  return `The cost of the ${this.item} is ${price * taxRate}`; 
}
args = [{"item": "burger"}, 10, 1.1]
```

输出  

```
"The cost of the burger is 11"
```

解释：`callPolyfill` 将 `this` 设置为 `{"item": "burger"}`，`10` 与 `1.1` 作为额外参数传入。

**约束条件**  

- `typeof args[0] == 'object'` 且 `args[0] != null`
- `1 <= args.length <= 100`
- `2 <= JSON.stringify(args[0]).length <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是直接把 `Function.prototype.call` 方法搬过来：  
```js
fn.call(obj, arg1, arg2, …)
```  
这里的 **call** 相当于把函数 `fn` 放进字典（对象）里，让字典的键对应的值（函数）在执行时自动把字典本身当作 `this`。  

- **数据结构类比**：  
  - **对象** 就像一本词典，`key` 是单词，`value` 是解释。把函数临时挂在对象上，就相当于把解释写进词典里，随后“读”这个解释时自然会知道是哪个词典（即 `this`）。
- **正确性**：  
  - JavaScript 在执行 `obj[key]()` 时，会把 `obj` 作为调用该函数的上下文（`this`），所以只要把函数挂在对象上再调用，就能得到和 `call` 完全一样的效果。
- **时间/空间复杂度**：  
  - 只需要一次把函数挂在对象上、调用一次、再把它删掉，所有操作都是 **常数次**（不随参数个数增长），所以时间复杂度是 **O(1)**，空间也只用了常数级别的临时属性，空间复杂度是 **O(1)**。  
  - 这里的 **O(1)** 可以理解为“无论你传多少参数，程序跑的时间基本不变”。

#### 代码（Python）  

下面先用 Python 写一个「伪实现」来帮助大家理解思路（实际解法在 JavaScript 中实现）：

```python
def call_polyfill(fn, obj, *args):
    """
    把 fn 暂时挂在 obj 上，然后调用，最后删除挂载的属性。
    """
    # 1. 给 obj 加一个唯一的属性名，防止覆盖已有属性
    tmp_key = '__tmp_fn__'
    while tmp_key in obj:          # 防止冲突
        tmp_key = '_' + tmp_key

    # 2. 把函数放进去
    obj[tmp_key] = fn

    # 3. 调用函数，Python 的调用方式会把 obj 当作第一个参数（模拟 this）
    result = obj[tmp_key](*args)

    # 4. 删除临时属性，恢复 obj 原状
    del obj[tmp_key]

    return result
```

> **注意**：Python 本身没有 `this` 概念，这段代码只是帮助大家把「把函数挂在对象上再调用」的思想具体化。真正的实现要写在 JavaScript 中。

#### 复杂度  

- **时间复杂度**：O(1) — 只做了常数次属性的增删和一次函数调用。  
- **空间复杂度**：O(1) — 只临时占用了一个属性的空间。

---

### 2. 最优解

#### 思路  

从上面的暴力思路出发，**慢点** 并不存在——我们已经用了最少的操作。唯一需要注意的是：

1. **不能使用内置的 `Function.call`**（题目限制），所以只能靠「挂在对象上」的方式实现。  
2. 为了避免 **属性冲突**（如果对象本身已经有同名属性），我们使用 **`Symbol`**（唯一且不会被枚举的键）来保存临时函数。  
3. 完成调用后 **一定要删除** 这个临时属性，防止副作用。

整体思路可以用生活中的「借用别人的工具」来类比：  
- 你想用锤子敲钉子，但手边没有锤子。于是你向邻居借了一把锤子（把函数挂到对象上），敲完钉子后立刻归还（删除属性），既不破坏邻居的工具，也完成了工作。

实现步骤：

1. 在 `Function.prototype` 上添加 `callPolyfill` 方法。  
2. 方法内部把 `this`（原函数）挂到传进来的 `obj` 上，键使用 `Symbol()`，保证唯一不冲突。  
3. 用展开运算符 `...args` 把后面的参数直接传给函数调用。  
4. 调用结束后删除临时属性，并把函数返回值返回。

#### 代码（Python）  

这里仍然用 Python 表示思路，实际提交请使用下面的 **JavaScript** 代码块。

```python
def callPolyfill_js_like(fn, obj, *args):
    """
    模拟 JavaScript 中的实现思路（仅供阅读）。
    """
    # 1. 生成唯一键（在 JS 中用 Symbol）
    import uuid
    tmp_key = f'__tmp_{uuid.uuid4().hex}__'

    # 2. 挂载函数
    obj[tmp_key] = fn

    # 3. 调用
    result = obj[tmp_key](*args)

    # 4. 删除临时属性
    del obj[tmp_key]

    return result
```

#### 代码（JavaScript）  

```javascript
// 为所有函数添加 callPolyfill 方法
Function.prototype.callPolyfill = function (obj, ...args) {
  // `this` 就是调用该方法的函数本身
  const fn = this;

  // 使用 Symbol 生成唯一属性名，防止与 obj 现有属性冲突
  const tempKey = Symbol('tempFn');

  // 把函数挂到 obj 上
  obj[tempKey] = fn;

  // 调用挂在 obj 上的函数，`...args` 会展开为普通参数
  // 此时函数内部的 `this` 自动指向 obj
  const result = obj[tempKey](...args);

  // 调用完后立即删除临时属性，保持 obj 原样
  delete obj[tempKey];

  // 把原函数的返回值返回给调用者
  return result;
};
```

> **关键行中文注释**  
> 1. `const fn = this;` // 保存当前函数的引用  
> 2. `const tempKey = Symbol('tempFn');` // 生成唯一键，防止覆盖  
> 3. `obj[tempKey] = fn;` // 把函数临时挂在对象上  
> 4. `const result = obj[tempKey](...args);` // 调用时 `this` 自动指向 `obj`  
> 5. `delete obj[tempKey];` // 清理临时属性，避免副作用  

#### 复杂度  

- **时间复杂度**：O(1) — 只做了常数次属性的增删和一次函数调用。与暴力解相比没有差别，因为我们本来就已经是最简的实现。  
- **空间复杂度**：O(1) — 只临时占用了一个 `Symbol` 键的空间，使用后立即释放。

---

## 心得

- **核心技巧**：利用 **对象属性挂载** + **Symbol 唯一键** 来手动模拟 `call` 的 `this` 绑定。  
- **适用场景**：  
  1. 实现 `apply`、`bind` 等 `this` 绑定相关的 polyfill。  
  2. 在不允许使用原生方法的环境（如面试的白板题）中手动改变函数执行上下文。  
  3. 对象方法的“借用”——把一个函数临时挂到另一个对象上使用。  
- **一句话总结**：把函数临时放进对象，用对象的属性调用方式自然实现 `this` 绑定。

---

## 反思

- **第一反应**：直接想到 `Function.prototype.call`，但题目禁止使用，于是寻找等价的实现手段。  
- **最容易踩的坑**：  
  - **属性冲突**：如果直接用固定键名（如 `tmp`) 挂函数，可能覆盖对象已有属性，导致意外行为。  
  - **忘记删除临时属性**：会产生副作用，影响后续代码。  
  - **`this` 丢失**：在严格模式下直接调用普通函数会把 `this` 设为 `undefined`，必须确保通过对象属性调用才能绑定成功。  
- **下次第一步**：先想“能否把函数放进对象再调用？”——如果可以，用 Symbol 防冲突、调用后清理，即可得到 `call` 的效果。