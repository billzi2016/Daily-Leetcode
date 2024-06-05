# #2722. 按 ID 合并两个数组 / Join Two Arrays by ID

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/join-two-arrays-by-id/)

---

## 题目（英文原版）

**Description**

Given two arrays arr1 and arr2, return a new array joinedArray. All the objects in each of the two inputs arrays will contain an id field that has an integer value.
joinedArray is an array formed by merging arr1 and arr2 based on their id key. The length of joinedArray should be the length of unique values of id. The returned array should be sorted in ascending order based on the id key.
If a given id exists in one array but not the other, the single object with that id should be included in the result array without modification.
If two objects share an id, their properties should be merged into a single object:

**Examples**

**Example 1:**

```
Input: 
arr1 = [
    {"id": 1, "x": 1},
    {"id": 2, "x": 9}
], 
arr2 = [
    {"id": 3, "x": 5}
]
Output: 
[
    {"id": 1, "x": 1},
    {"id": 2, "x": 9},
    {"id": 3, "x": 5}
]
Explanation: There are no duplicate ids so arr1 is simply concatenated with arr2.
```

**Example 2:**

```
Input: 
arr1 = [
    {"id": 1, "x": 2, "y": 3},
    {"id": 2, "x": 3, "y": 6}
], 
arr2 = [
    {"id": 2, "x": 10, "y": 20},
    {"id": 3, "x": 0, "y": 0}
]
Output: 
[
    {"id": 1, "x": 2, "y": 3},
    {"id": 2, "x": 10, "y": 20},
    {"id": 3, "x": 0, "y": 0}
]
Explanation: The two objects with id=1 and id=3 are included in the result array without modifiction. The two objects with id=2 are merged together. The keys from arr2 override the values in arr1.
```

**Example 3:**

```
Input: 
arr1 = [
    {"id": 1, "b": {"b": 94},"v": [4, 3], "y": 48}
]
arr2 = [
    {"id": 1, "b": {"c": 84}, "v": [1, 3]}
]
Output: [
    {"id": 1, "b": {"c": 84}, "v": [1, 3], "y": 48}
]
Explanation: The two objects with id=1 are merged together. For the keys "b" and "v" the values from arr2 are used. Since the key "y" only exists in arr1, that value is taken form arr1.
```

**Constraints**

- arr1 and arr2 are valid JSON arrays
- Each object in arr1 and arr2 has a unique integer id key
- 2 <= JSON.stringify(arr1).length <= 106
- 2 <= JSON.stringify(arr2).length <= 106

---

## 题目（中文翻译）

**描述**  
给定两个数组 `arr1` 和 `arr2`，返回一个新数组 `joinedArray`。两个输入数组中的所有对象都包含一个整数类型的 `id` 字段。  
`joinedArray` 通过 **合并（merge）** `arr1` 和 `arr2` 中的对象，按照它们的 `id` 键进行合并得到。`joinedArray` 的长度应等于所有唯一 `id` 值的个数。返回的数组需要 **按升序（ascending order）** 根据 `id` 键进行排序。  

- 如果某个 `id` 只在其中一个数组出现，则直接把该对象（不作修改）加入结果数组。  
- 如果两个对象拥有相同的 `id`，则需要将它们的属性合并为单个对象：

  - 对于同名属性，使用 **后出现的数组**（即 `arr2`）中的值覆盖前面的值。  
  - 对于只在其中一个对象中出现的属性，直接保留该属性及其对应的值。

**示例 1**  
```json
Input: 
arr1 = [
  {"id": 1, "x": 1},
  {"id": 2, "x": 9}
], 
arr2 = [
  {"id": 3, "x": 5}
]
Output: 
[
  {"id": 1, "x": 1},
  {"id": 2, "x": 9},
  {"id": 3, "x": 5}
]
```
**解释**：没有重复的 `id`，因此直接把 `arr1` 与 `arr2` 连接即可。

**示例 2**  
```json
Input: 
arr1 = [
  {"id": 1, "x": 2, "y": 3},
  {"id": 2, "x": 3, "y": 6}
], 
arr2 = [
  {"id": 2, "x": 10, "y": 20},
  {"id": 3, "x": 0, "y": 0}
]
Output: 
[
  {"id": 1, "x": 2, "y": 3},
  {"id": 2, "x": 10, "y": 20},
  {"id": 3, "x": 0, "y": 0}
]
```
**解释**：`id=1` 和 `id=3` 的对象只出现一次，直接保留。`id=2` 的对象在两个数组中都出现，属性被合并后使用 `arr2` 中的值覆盖 `arr1` 中的对应值。

**示例 3**  
```json
Input: 
arr1 = [
  {"id": 1, "b": {"b": 94}, "v": [4, 3], "y": 48}
]
arr2 = [
  {"id": 1, "b": {"c": 84}, "v": [1, 3]}
]
Output: [
  {"id": 1, "b": {"c": 84}, "v": [1, 3], "y": 48}
]
```
**解释**：`id=1` 的对象被合并。键 `"b"` 和 `"v"` 的值取自 `arr2`，而键 `"y"` 只在 `arr1` 中出现，故保留 `arr1` 中的值。

**约束条件**  
- `arr1` 和 `arr2` 为合法的 JSON 数组。  
- 每个对象的 `id` 键是唯一的整数。  
- `2 <= JSON.stringify(arr1).length <= 10^6`  
- `2 <= JSON.stringify(arr2).length <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把 `arr1` 和 `arr2` 先全部拼在一起，得到一个大数组 `merged`。  
然后对这个大数组 **逐个检查**，看每个对象的 `id` 是否已经出现过：

1. 取出第一个对象，记下它的 `id`。  
2. 再遍历后面的所有对象，寻找相同的 `id`。  
3. 如果找到了相同 `id`，就把两个对象的属性合并（把后面的属性直接覆盖前面的）。  
4. 把合并好的对象放进结果数组 `joinedArray`，并把已经处理过的对象标记为“已用”。  

> **数据结构类比**：  
> - **数组** 就像一排排的信封，每个信封里装着一张卡片（对象）。  
> - **遍历** 就是把手伸进每个信封里，逐个查看卡片内容。  
> - **标记已用** 可以想象在信封上贴一张小贴纸，表示这封已经处理完了。

这种做法一定能得到正确答案，因为我们把每一对可能同 `id` 的对象都找到了并合并了，最后把所有对象都放进了结果里。

#### 代码（Python）

```python
def join_arrays_brute(arr1, arr2):
    # 把两个数组直接拼在一起
    merged = arr1 + arr2                     # O(n+m)

    n = len(merged)
    used = [False] * n                       # 标记每个元素是否已经加入结果
    result = []

    for i in range(n):
        if used[i]:                          # 已经被合并进别的对象，跳过
            continue

        cur = merged[i].copy()               # 复制一份，防止改动原数据
        used[i] = True

        # 在后面的元素里寻找相同的 id
        for j in range(i + 1, n):
            if not used[j] and merged[j]["id"] == cur["id"]:
                # 合并属性：后面的属性直接覆盖前面的属性
                cur.update(merged[j])        # dict.update 会把相同的键值替换
                used[j] = True               # 这条记录已经被合并，标记为已用

        result.append(cur)

    # 按 id 升序排序
    result.sort(key=lambda obj: obj["id"])   # O(k log k)，k 为不同 id 的数量
    return result
```

**关键行中文注释**  
- `merged = arr1 + arr2` 把两个数组拼在一起。  
- `used = [False] * n` 用布尔列表记录每个元素是否已经被合并。  
- `cur.update(merged[j])` 把后面的对象属性覆盖到前面对象上（实现“合并”）。  
- `result.sort(key=lambda obj: obj["id"])` 按照 `id` 从小到大排序。

#### 复杂度

- **时间复杂度**：`O((n+m)²)`  
  - 外层遍历 `n+m` 次，内层最坏情况下也要遍历 `n+m` 次（每次都要找相同的 `id`），所以是平方级别。  
  - 用大白话说，就是如果数组有 1000 条记录，程序大约要跑 1000 × 1000 = 1,000,000 次比较，效率不高。

- **空间复杂度**：`O(n+m)`  
  - 需要额外的 `merged`（复制两个数组）和 `used`（布尔标记），以及最终的 `result`。这些都和输入规模线性相关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于每次都要遍历后面的所有元素去找相同的 `id`，这导致了二次循环。  
如果我们能 **一次就定位到对应的对象**，就可以把时间从平方级降到线性级。

**关键点**：  
- `id` 是唯一的整数，完全可以把它当作 **哈希表（字典）的键**。  
- Python 的 `dict` 就像一本“电话簿”：通过键（这里是 `id`）可以 **O(1) 时间**（常数时间）直接找到对应的值（对象）。

**优化步骤**：

1. 建立一个空字典 `lookup = {}`，键是 `id`，值是已经合并好的对象。  
2. 先遍历 `arr1`：把每个对象直接放进 `lookup`（`lookup[id] = obj.copy()`），这里不需要合并，因为还没有冲突。  
3. 再遍历 `arr2`：  
   - 如果 `id` 已经在 `lookup` 中，说明出现了冲突，直接用 `obj.update(lookup[id])` 或者相反的顺序把属性合并。题目要求 **以 arr2 的属性覆盖 arr1**，所以我们用 `lookup[id].update(obj)`（先保留 arr1，再用 arr2 覆盖）。  
   - 如果 `id` 不在 `lookup` 中，直接把对象加入字典。  
4. 把字典的所有值取出来，得到一个列表。  
5. 最后 **按 `id` 排序**（因为字典本身不保证顺序），得到最终的 `joinedArray`。

> **数据结构类比**：  
> - **哈希表（dict）** 就像一本“身份证登记册”，每个人的身份证号（`id`）对应唯一的一页记录（对象）。要找某个人，只要翻到对应的页码，**不需要从头到尾查**。

#### 代码（Python）

```python
def join_arrays_opt(arr1, arr2):
    """
    用哈希表一次遍历完成合并，时间 O(n + m) + 排序 O(k log k)。
    """
    lookup = {}                     # id -> 合并后的对象

    # 先放入 arr1 的数据
    for obj in arr1:
        # 复制一份，防止后面被原地修改
        lookup[obj["id"]] = obj.copy()

    # 再处理 arr2，遇到相同 id 时用 arr2 的值覆盖
    for obj in arr2:
        if obj["id"] in lookup:
            # 已存在，使用 arr2 的属性覆盖 arr1（题目要求）
            lookup[obj["id"]].update(obj)   # update 会把相同键的值替换
        else:
            # 之前没有出现过，直接放进去
            lookup[obj["id"]] = obj.copy()

    # 取出所有合并好的对象，按 id 升序排列
    result = list(lookup.values())
    result.sort(key=lambda o: o["id"])   # O(k log k)，k 为不同 id 的数量

    return result
```

**关键行中文注释**  
- `lookup = {}` 创建空字典，准备把 `id` 当键。  
- `lookup[obj["id"]] = obj.copy()` 把对象复制后存进字典。  
- `lookup[obj["id"]].update(obj)` 如果已经有相同 `id`，用 `arr2` 的属性覆盖（`update` 会把键相同的值改为新的）。  
- `result.sort(key=lambda o: o["id"])` 最终按照 `id` 从小到大排序。

#### 复杂度

- **时间复杂度**：`O(n + m + k log k)`  
  - `n` 为 `arr1` 长度，`m` 为 `arr2` 长度。遍历两遍数组各一次，都是线性时间。  
  - 最后一步排序需要 `k log k`（`k` 是不同 `id` 的数量），这一步是必不可少的，因为题目要求返回的数组必须按 `id` 升序。  
  - 与暴力解相比，**遍历阶段从平方级降到了线性级**，只剩下排序的对数因素。

- **空间复杂度**：`O(k)`  
  - 需要一个字典保存所有不同 `id` 的对象，大小正好等于结果数组的长度 `k`。  
  - 额外的临时列表 `result` 也占 `O(k)` 空间。

---

## 心得

- **核心技巧**：使用哈希表（Python 的 `dict`）实现 **键值映射**，在 O(1) 时间内完成 “根据 id 找对象” 的操作。  
- **适用的题型**  
  1. 两个列表/数组按照唯一键合并（如合并用户信息、订单记录）。  
  2. “去重并保留最新信息” 场景（例如日志去重、最新状态覆盖）。  
  3. “交叉查找” 类问题（如两个表的外键关联）。  
- **一句话总结解题钥匙**：**把唯一标识 `id` 当作字典的键，利用 O(1) 查找实现一次遍历合并**。

---

## 反思

- **第一反应**：直接把两个数组拼在一起，用两层循环去找相同的 `id`，因为这样最容易想到，代码也很直观。  
- **最容易踩的坑**  
  - **覆盖顺序**：题目要求 “`arr2` 的属性覆盖 `arr1`”，如果写成 `obj.update(lookup[id])` 会把 `arr2` 的值被 `arr1` 覆盖，结果出错。  
  - **深拷贝 vs 浅拷贝**：如果对象里还有嵌套的字典或列表，直接 `copy()` 只会复制引用。这里题目只要求浅层覆盖，所以 `copy()` 足够，但在实际项目中可能需要 `deepcopy`。  
  - **排序**：忘记最后的 `id` 排序会导致输出顺序不符合要求，测试会直接报错。  
- **下次遇到同类题**：第一步先判断是否有 **唯一键**（如 `id`），如果有，立刻想到使用 **哈希表** 把键映射到对象，以实现 “一次遍历合并”。这样可以把时间复杂度从 `O(n²)` 降到 `O(n log n)`（排序除外）。