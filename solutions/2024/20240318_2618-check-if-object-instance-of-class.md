# #2618. 检查对象是否为类的实例 / Check if Object Instance of Class

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/check-if-object-instance-of-class/)

---

## 题目（英文原版）

**Description**

Write a function that checks if a given value is an instance of a given class or superclass. For this problem, an object is considered an instance of a given class if that object has access to that class's methods.
There are no constraints on the data types that can be passed to the function. For example, the value or the class could be undefined.

**Examples**

**Example 1:**

```
Input: func = () => checkIfInstanceOf(new Date(), Date)
Output: true
Explanation: The object returned by the Date constructor is, by definition, an instance of Date.
```

**Example 2:**

```
Input: func = () => { class Animal {}; class Dog extends Animal {}; return checkIfInstanceOf(new Dog(), Animal); }
Output: true
Explanation:
class Animal {};
class Dog extends Animal {};
checkIfInstanceOf(new Dog(), Animal); // true

Dog is a subclass of Animal. Therefore, a Dog object is an instance of both Dog and Animal.
```

**Example 3:**

```
Input: func = () => checkIfInstanceOf(Date, Date)
Output: false
Explanation: A date constructor cannot logically be an instance of itself.
```

**Example 4:**

```
Input: func = () => checkIfInstanceOf(5, Number)
Output: true
Explanation: 5 is a Number. Note that the "instanceof" keyword would return false. However, it is still considered an instance of Number because it accesses the Number methods. For example "toFixed()".
```

---

## 题目（中文翻译）

编写一个函数，用于检查给定的值 **value** 是否是指定类 **class** 或其超类（superclass）的实例（instance）。在本题中，如果对象（object）能够访问该类的成员方法（method），则认为它是该类的实例。

对传入函数的数据类型没有任何限制。例如，**value** 或 **class** 本身可能为 `undefined`。

**示例 1**  
```javascript
func = () => checkIfInstanceOf(new Date(), Date)
```
**输出**: `true`  
**解释**: 由 `Date` 构造函数返回的对象，按照定义，是 `Date` 的实例（instance）。

**示例 2**  
```javascript
func = () => {
    class Animal {};
    class Dog extends Animal {};
    return checkIfInstanceOf(new Dog(), Animal);
}
```
**输出**: `true`  
**解释**:  
```javascript
class Animal {};
class Dog extends Animal {};
checkIfInstanceOf(new Dog(), Animal); // true
```  
`Dog` 是 `Animal` 的子类（subclass）。因此，`Dog` 的实例既是 `Dog` 的实例，也是 `Animal` 的实例。

**示例 3**  
```javascript
func = () => checkIfInstanceOf(Date, Date)
```
**输出**: `false`  
**解释**: `Date` 构造函数本身不可能是它自己的实例（instance）。

**示例 4**  
```javascript
func = () => checkIfInstanceOf(5, Number)
```
**输出**: `true`  
**解释**: `5` 是一个 `Number`。注意，使用 `instanceof` 运算符会返回 `false`，但它仍被视为 `Number` 的实例，因为它可以访问 `Number` 的方法（method），例如 `toFixed()`。

**约束条件**  
无任何约束。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把对象的所有父类（包括它自己的类）全部列出来，看看目标类是否在这条“继承链”上**。  
在 JavaScript 中，这条链叫 *prototype chain*，我们可以把它想象成“一本字典的目录”。  
每个类就像目录里的一个章节，章节之间按顺序相连（子类 → 父类 → 父父类 …）。  
要判断一个对象能否使用某个类的方法，只要在这本目录里找得到对应章节，就说明它“拥有”那个类的所有方法。

在 Python 中，类的继承信息保存在 `__mro__`（Method Resolution Order）属性里，实际上就是一个从子类到最顶层父类的列表。  
我们可以一步一步地遍历这个列表，和目标类做比较：

1. **取对象的实际类型**：`type(obj)`（如果 `obj` 本身就是类，则直接使用它）。
2. **取该类型的 `__mro__`**，得到完整的继承链。
3. **逐个比对**：如果链上出现了目标类 `cls`，返回 `True`；遍历完仍未找到，返回 `False`。

> 为什么这样可以判断“是否可以访问该类的方法”？  
> 因为只要对象的继承链上有 `cls`，Python（和 JavaScript）在属性查找时就会沿着这条链往上找，一定能找到 `cls` 上的方法。

**时间/空间复杂度**  
- 时间复杂度是 `O(h)`，`h` 为对象的继承层数。就像在一本目录里从前往后找，最坏要翻完全部章节。  
- 空间复杂度是 `O(1)`，我们只用常数个额外变量（不需要额外的数组或哈希表）。

> 大白话解释：如果一棵树有 10 层，我们最多检查 10 次；如果只有 2 层，只检查 2 次。这个检查次数跟树的高度成正比。

#### 代码（Python）

```python
def check_if_instance_of(value, cls):
    """
    判断 value 是否是 cls（或其子类）的实例。
    这里的“实例”指的是 value 能访问到 cls 定义的方法。
    """

    # 1. 先排除不合法的 cls（比如 None、数字等），它们根本不是类
    if not isinstance(cls, type):
        # 在 Python 中，合法的类一定是 type 的实例
        return False

    # 2. 取 value 的真实类型
    #    - 如果 value 本身是类（比如把类当作参数传进来），type(value) 会是 type，
    #      这时我们直接把它当作实例去检查（与 JavaScript 的构造函数不同）。
    #    - 对普通对象，type(value) 就是它的类。
    value_type = type(value)

    # 3. 通过 __mro__（方法解析顺序）遍历完整的继承链
    for base in value_type.__mro__:          # __mro__ 是一个元组，顺序是: 子类 → 父类 → … → object
        if base is cls:                     # 找到目标类，说明可以访问它的方法
            return True

    # 4. 遍历完都没找到，返回 False
    return False
```

#### 复杂度

- **时间复杂度：**`O(h)`，`h` 为对象的继承层数。  
  > 想象成在一条链子上逐个检查，最坏情况要检查到最顶层 `object`。

- **空间复杂度：**`O(1)`，只用了常数级别的额外变量（`value_type`、循环计数器等）。

---

### 2. 最优解

#### 思路  

从暴力解我们已经看到，真正的“慢点”在于**逐层遍历继承链**。  
不过这已经是最直接、最省空间的做法——我们只需要检查 `h` 次，而 `h` 本身是对象结构决定的，无法再进一步压缩。  
在 Python（以及大多数面向对象语言）里，判断实例关系的标准操作就是 `isinstance`，它内部也是基于 `__mro__` 的线性查找，且实现用 C 写得非常快。

因此，**最优解**只需要把我们手写的遍历交给 Python 内置的 `isinstance`，并在 `cls` 不是合法类时做一次防护。这样既保持 **O(1)** 的常数时间（因为底层实现已经做了最优化），又省掉我们自己写循环的代码。

> 这里的“最优”指的不是更低的时间复杂度，而是**利用语言自带的高效实现**，代码更简洁、可读性更好。

#### 代码（Python）

```python
def check_if_instance_of(value, cls):
    """
    最简洁的实现：直接使用 Python 的 isinstance。
    只要 cls 是合法的类（type 的实例），isinstance 能正确判断
    包括子类、内置类型等情况。
    """
    # 先确保 cls 真的是一个类对象；如果不是，直接返回 False
    if not isinstance(cls, type):
        return False

    # isinstance 已经帮我们遍历了完整的继承链
    return isinstance(value, cls)
```

#### 复杂度

- **时间复杂度：**`O(1)`（在语义层面是常数时间）。  
  > 实际上 `isinstance` 仍然会遍历 `__mro__`，但它的实现是用 C 写的，几乎可以视作常数时间，对比我们自己用 Python 循环的 `O(h)`，速度快很多。

- **空间复杂度：**`O(1)`，只使用了极少的临时变量。

---

## 心得

- **核心技巧**：利用 **继承链（prototype chain / MRO）** 判断对象是否能访问某个类的方法。  
- **适用的题型**  
  1. 判断对象是否实现某个接口或抽象基类（如 LeetCode “Valid Parentheses” 的 OOP 变体）。  
  2. 需要在运行时根据对象类型决定分支逻辑的题目（如 “Design Parking System”）。  
  3. 实现自定义的 `instanceof` / `isinstance` 功能（本题）。  

> **解题钥匙**：把“对象能否使用某个类的方法”翻译成“目标类是否在对象的继承链上”。

---

## 反思

- **第一反应**：看到“instanceof”关键字，我马上想到要遍历原型链（在 Python 中就是遍历 `__mro__`）。
- **最容易踩的坑**  
  - **cls 不是类**：直接传入 `None`、数字或函数会导致 `isinstance` 抛异常，需要先判断 `isinstance(cls, type)`。  
  - **原始数据类型**：在 JavaScript 中 `5` 仍被视为 `Number` 的实例，Python 中对应的是 `int`、`float`，所以要确保把这些基本类型当作合法类来比较。  
  - **类本身的检查**：`check_if_instance_of(Date, Date)` 应返回 `False`（类不是它自己的实例），这在 Python 中自然满足，因为 `type(Date)` 是 `type`，而 `Date` 不是 `type` 的子类。

- **下次遇到同类题**：第一步先**判断参数是否合法**（尤其是目标类），然后**直接使用语言自带的实例判断函数**（如 `isinstance`），只有在语言没有提供时才手动遍历继承链。这样既安全又高效。