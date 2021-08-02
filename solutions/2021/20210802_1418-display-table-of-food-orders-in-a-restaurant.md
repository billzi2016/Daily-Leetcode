# #1418. 餐厅食物订单展示表 / Display Table of Food Orders in a Restaurant

> 难度：中等 · 标签：Array、Hash Table、String、Sorting、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/display-table-of-food-orders-in-a-restaurant/)

---

## 题目（英文原版）

**Description**

Given the array orders, which represents the orders that customers have done in a restaurant. More specifically orders[i]=[customerNamei,tableNumberi,foodItemi] where customerNamei is the name of the customer, tableNumberi is the table customer sit at, and foodItemi is the item customer orders.
Return the restaurant's “display table”. The “display table” is a table whose row entries denote how many of each food item each table ordered. The first column is the table number and the remaining columns correspond to each food item in alphabetical order. The first row should be a header whose first column is “Table”, followed by the names of the food items. Note that the customer names are not part of the table. Additionally, the rows should be sorted in numerically increasing order.

**Examples**

**Example 1:**

```
Input: orders = [["David","3","Ceviche"],["Corina","10","Beef Burrito"],["David","3","Fried Chicken"],["Carla","5","Water"],["Carla","5","Ceviche"],["Rous","3","Ceviche"]]
Output: [["Table","Beef Burrito","Ceviche","Fried Chicken","Water"],["3","0","2","1","0"],["5","0","1","0","1"],["10","1","0","0","0"]] 
Explanation:
The displaying table looks like:
Table,Beef Burrito,Ceviche,Fried Chicken,Water
3    ,0           ,2      ,1            ,0
5    ,0           ,1      ,0            ,1
10   ,1           ,0      ,0            ,0
For the table 3: David orders "Ceviche" and "Fried Chicken", and Rous orders "Ceviche".
For the table 5: Carla orders "Water" and "Ceviche".
For the table 10: Corina orders "Beef Burrito".
```

**Example 2:**

```
Input: orders = [["James","12","Fried Chicken"],["Ratesh","12","Fried Chicken"],["Amadeus","12","Fried Chicken"],["Adam","1","Canadian Waffles"],["Brianna","1","Canadian Waffles"]]
Output: [["Table","Canadian Waffles","Fried Chicken"],["1","2","0"],["12","0","3"]] 
Explanation: 
For the table 1: Adam and Brianna order "Canadian Waffles".
For the table 12: James, Ratesh and Amadeus order "Fried Chicken".
```

**Example 3:**

```
Input: orders = [["Laura","2","Bean Burrito"],["Jhon","2","Beef Burrito"],["Melissa","2","Soda"]]
Output: [["Table","Bean Burrito","Beef Burrito","Soda"],["2","1","1","1"]]
```

**Constraints**

- 1 <= orders.length <= 5 * 10^4
- orders[i].length == 3
- 1 <= customerNamei.length, foodItemi.length <= 20
- customerNamei and foodItemi consist of lowercase and uppercase English letters and the space character.
- tableNumberi is a valid integer between 1 and 500.

---

## 题目（中文翻译）

给定一个二维数组 `orders`，其中每个元素 `orders[i] = [customerName_i, tableNumber_i, foodItem_i]` 分别表示顾客姓名、顾客所在的桌号以及顾客点的菜品。  
请返回该餐厅的 **展示表（display table）**。展示表是一张二维表，行（row）记录每张桌子点的各类菜品的数量，列（column）记录每种菜品的名称。  

- 第一列固定为桌号，后续列按照菜品名称的字母顺序排列。  
- 第一行是表头（header），第一列的标题为 `"Table"`，随后是所有菜品名称。  
- 顾客的姓名不出现在表中。  
- 所有行（即各桌号）需要按数值递增的顺序排列。

**示例 1**  
**示例 2**  
**示例 3**

**约束条件**

- `1 <= orders.length <= 5 * 10^4`
- `orders[i].length == 3`
- `1 <= customerName_i.length, foodItem_i.length <= 20`
- `customerName_i` 和 `foodItem_i` 仅由大小写英文字母和空格组成。
- `tableNumber_i` 为 `1` 到 `500` 之间的合法整数。

---

### 示例

#### 示例 1
**输入**  
```json
orders = [["David","3","Ceviche"],["Corina","10","Beef Burrito"],["David","3","Fried Chicken"],["Carla","5","Water"],["Carla","5","Ceviche"],["Rous","3","Ceviche"]]
```
**输出**  
```json
[["Table","Beef Burrito","Ceviche","Fried Chicken","Water"],["3","0","2","1","0"],["5","0","1","0","1"],["10","1","0","0","0"]]
```
**解释**  
展示表如下所示（省略了中间的换行）：

```
Table,Beef Burrito,Ceviche,Fried Chicken,Water
3,0,2,1,0
5,0,1,0,1
10,1,0,0,0
```

#### 示例 2
**输入**  
```json
orders = [["James","12","Fried Chicken"],["Ratesh","12","Fried Chicken"],["Amadeus","12","Fried Chicken"],["Adam","1","Canadian Waffles"],["Brianna","1","Canadian Waffles"]]
```
**输出**  
```json
[["Table","Canadian Waffles","Fried Chicken"],["1","2","0"],["12","0","3"]]
```
**解释**  
- 桌号 1：Adam 和 Brianna 各点了 1 份 `"Canadian Waffles"`，因此该列的计数为 2。  
- 桌号 12：James、Ratesh 和 Amadeus 都点了 `"Fried Chicken"`，计数为 3。  

#### 示例 3
**输入**  
```json
orders = [["Laura","2","Bean Burrito"],["Jhon","2","Beef Burrito"],["Melissa","2","Soda"]]
```
**输出**  
```json
[["Table","Bean Burrito","Beef Burrito","Soda"],["2","1","1","1"]]
```
**解释**  
唯一的桌号 2 点了三种不同的菜品，各自计数为 1。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：  

1. **先把所有菜名收集起来**。把每一次点单的 `foodItem` 放进一个集合（集合就像装所有不同菜名的抽屉，重复的菜名只会出现一次）。  
2. **把所有桌号收集起来**。同理，用集合把出现过的 `tableNumber` 收集好。  
3. **遍历每一张桌子**，对每一种菜都 **重新遍历一遍全部点单**，统计这张桌子点了多少该菜。  
   - 想象你在餐厅里，手里只有这张点单清单。想知道 3 号桌点了几份“Ceviche”，只能从头到尾查一遍所有记录，找到属于 3 号桌且菜名是“Ceviche”的条目并计数。  

这样做一定能得到正确的结果，因为我们把 **每一张桌子 + 每一种菜** 的组合都检查了一遍。  

> **为什么会对？**  
> - 所有出现的菜名都已经列在表头里。  
> - 所有出现的桌号都已经列在行号里。  
> - 对每个 (桌号, 菜名) 组合我们都统计了出现次数，正好对应题目要求的“每张桌子点了多少该菜”。  

#### 代码（Python）  

```python
from typing import List

def displayTable(orders: List[List[str]]) -> List[List[str]]:
    # 1. 收集所有不同的菜名（集合像“字典”，不放重复）
    food_set = set()
    for _, _, food in orders:
        food_set.add(food)               # 把菜名加入集合

    # 2. 收集所有不同的桌号并转成整数，方便后面排序
    table_set = set()
    for _, table, _ in orders:
        table_set.add(int(table))        # 桌号转成 int，后面要数值排序

    # 3. 把菜名和桌号排序，得到表头和行顺序
    foods = sorted(food_set)             # 字典序（字母顺序）
    tables = sorted(table_set)           # 数值升序

    # 4. 暴力统计：对每张桌子、每道菜，都遍历一次 orders
    result = []
    # 表头
    result.append(["Table"] + foods)

    for t in tables:                     # 按顺序遍历每张桌子
        row = [str(t)]                   # 第一列是桌号（字符串形式）
        for f in foods:                  # 按字母顺序遍历每道菜
            cnt = 0
            for name, table, food in orders:   # 重新遍历全部点单
                if int(table) == t and food == f:
                    cnt += 1
            row.append(str(cnt))        # 计数结果转成字符串
        result.append(row)

    return result
```

#### 复杂度  

- **时间复杂度：** `O(T * F * N)`  
  - `T` 为不同桌号的数量，`F` 为不同菜名的数量，`N` 为点单总数。  
  - 想象你在做三层循环：外层遍历桌子，中层遍历菜名，最里层遍历所有点单。  
  - 最坏情况下（比如 500 张桌子、500 种菜、5·10⁴ 条记录），时间会比较大。  
- **空间复杂度：** `O(T + F)`  
  - 只用了两个集合分别存放桌号和菜名，另外输出表格本身也占用同样大小的空间。  

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到 **瓶颈** 在于“每次统计都要遍历完整个 `orders`”。  
如果我们在第一次遍历 `orders` 时，就把 **每个 (桌号, 菜名) 的出现次数记录下来**，后面再查询就可以 **直接拿到**，不需要再遍历。

这正好可以用 **哈希表（字典）** 来实现：  

- 把 **键 (key)** 设计成 `(table, food)` 这对信息。  
  - 想象哈希表是一张“查字典”，**key** 就是词条（这里是桌号+菜名），**value** 是对应的定义（这里是点了几份）。  
- 第一次遍历 `orders` 时，遇到一条记录就把对应的计数 `+1`。  
- 同时把所有出现的 **菜名**、**桌号** 收集进集合，后面只需要排序一次。  

这样，我们只需要 **一次遍历** 就完成计数，后面再按顺序把结果填进表格即可。  

**核心技巧**：  
- **哈希表** 用来统计频次。  
- **集合 + 排序** 用来得到表头和行顺序。  

#### 代码（Python）  

```python
from typing import List
from collections import defaultdict

def displayTable(orders: List[List[str]]) -> List[List[str]]:
    # 哈希表： (table, food) -> 次数
    # 使用 defaultdict(int) 省去手动判断键是否存在的步骤
    cnt = defaultdict(int)

    food_set = set()      # 所有出现的菜名
    table_set = set()     # 所有出现的桌号（整数）

    # 只遍历一次 orders，完成所有统计
    for name, table, food in orders:
        table_num = int(table)          # 转成整数，方便后面数值排序
        cnt[(table_num, food)] += 1     # 对应的 (桌号, 菜名) 计数加一
        food_set.add(food)              # 收集菜名
        table_set.add(table_num)        # 收集桌号

    # 把菜名按字母顺序、桌号按数值升序排列
    foods = sorted(food_set)            # 列标题（除 "Table" 之外）
    tables = sorted(table_set)          # 行顺序

    # 构造结果表格
    result = []
    # 表头
    result.append(["Table"] + foods)

    # 对每一张桌子，直接从哈希表里拿计数，不再遍历 orders
    for t in tables:
        row = [str(t)]                  # 第一列是桌号（字符串）
        for f in foods:
            row.append(str(cnt[(t, f)]))   # 若键不存在，defaultdict 返回 0
        result.append(row)

    return result
```

#### 复杂度  

- **时间复杂度：** `O(N + T·log T + F·log F)`  
  - `N` 为点单总数，只遍历一次 `orders`（一次 O(N)）。  
  - `T·log T` 和 `F·log F` 是对桌号集合和菜名集合各自排序的代价。  
  - 与暴力解相比，去掉了那层 `O(T·F·N)` 的嵌套遍历，速度快很多。  
- **空间复杂度：** `O(N + T + F)`  
  - `cnt` 哈希表最坏会保存每条记录对应的键（即每对 (桌号, 菜名)），数量不超过 `N`。  
  - 另外还有保存所有不同桌号和菜名的集合。  

---

## 心得  

- **核心技巧**：使用哈希表一次遍历完成“出现次数统计”，再配合集合+排序生成有序的表头和行。  
- **适用场景**：  
  1. **统计类题目**：如 “统计每个字符出现次数”“统计每种商品的销量”。  
  2. **分组聚合**：如 “按城市分组统计人口”“按员工部门统计工资总和”。  
  3. **二维计数**：如 “统计棋盘上每种棋子出现的次数”“统计学生每门课程的成绩”。  
- **一句话总结**：**把“计数”放在遍历的第一步，用哈希表直接记下来，后面只需要排个序填表。**  

---

## 反思  

- **第一反应**：看到“每张桌子、每道菜的数量”，本能想把表格的每个格子都单独算一遍——也就是暴力三层循环。  
- **最容易踩的坑**：  
  - 忘记把 **桌号转成整数** 再排序，导致 “10” 会排在 “2” 前面（字符串排序的错误）。  
  - 表格要求所有数值都以 **字符串** 形式返回，直接返回整数会导致答案不匹配。  
  - 没有考虑 **空格或大小写** 对菜名的影响，直接使用原始字符串即可（因为题目保证一致）。  
- **下次思路**：遇到“**每 X 的统计**”时，先问自己 “能不能在一次遍历里把计数弄好？”——如果能，用哈希表；如果涉及排序，再把键收集起来排个序。这样就能从暴力直接跳到最优解。