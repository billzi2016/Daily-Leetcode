# #1357. 每 n 次订单应用折扣 / Apply Discount Every n Orders

> 难度：中等 · 标签：Array、Hash Table、Design · [LeetCode 链接](https://leetcode.com/problems/apply-discount-every-n-orders/)

---

## 题目（英文原版）

**Description**

There is a supermarket that is frequented by many customers. The products sold at the supermarket are represented as two parallel integer arrays products and prices, where the ith product has an ID of products[i] and a price of prices[i].
When a customer is paying, their bill is represented as two parallel integer arrays product and amount, where the jth product they purchased has an ID of product[j], and amount[j] is how much of the product they bought. Their subtotal is calculated as the sum of each amount[j] * (price of the jth product).
The supermarket decided to have a sale. Every nth customer paying for their groceries will be given a percentage discount. The discount amount is given by discount, where they will be given discount percent off their subtotal. More formally, if their subtotal is bill, then they would actually pay bill * ((100 - discount) / 100).
Implement the Cashier class:

**Examples**

**Example 1:**

```
Input
["Cashier","getBill","getBill","getBill","getBill","getBill","getBill","getBill"]
[[3,50,[1,2,3,4,5,6,7],[100,200,300,400,300,200,100]],[[1,2],[1,2]],[[3,7],[10,10]],[[1,2,3,4,5,6,7],[1,1,1,1,1,1,1]],[[4],[10]],[[7,3],[10,10]],[[7,5,3,1,6,4,2],[10,10,10,9,9,9,7]],[[2,3,5],[5,3,2]]]
Output
[null,500.0,4000.0,800.0,4000.0,4000.0,7350.0,2500.0]
Explanation
Cashier cashier = new Cashier(3,50,[1,2,3,4,5,6,7],[100,200,300,400,300,200,100]);
cashier.getBill([1,2],[1,2]);                        // return 500.0. 1st customer, no discount.
                                                     // bill = 1 * 100 + 2 * 200 = 500.
cashier.getBill([3,7],[10,10]);                      // return 4000.0. 2nd customer, no discount.
                                                     // bill = 10 * 300 + 10 * 100 = 4000.
cashier.getBill([1,2,3,4,5,6,7],[1,1,1,1,1,1,1]);    // return 800.0. 3rd customer, 50% discount.
                                                     // Original bill = 1600
                                                     // Actual bill = 1600 * ((100 - 50) / 100) = 800.
cashier.getBill([4],[10]);                           // return 4000.0. 4th customer, no discount.
cashier.getBill([7,3],[10,10]);                      // return 4000.0. 5th customer, no discount.
cashier.getBill([7,5,3,1,6,4,2],[10,10,10,9,9,9,7]); // return 7350.0. 6th customer, 50% discount.
                                                     // Original bill = 14700, but with
                                                     // Actual bill = 14700 * ((100 - 50) / 100) = 7350.
cashier.getBill([2,3,5],[5,3,2]);                    // return 2500.0.  7th customer, no discount.
```

**Constraints**

- 1 <= n <= 104
- 0 <= discount <= 100
- 1 <= products.length <= 200
- prices.length == products.length
- 1 <= products[i] <= 200
- 1 <= prices[i] <= 1000
- The elements in products are unique.
- 1 <= product.length <= products.length
- amount.length == product.length
- product[j] exists in products.
- 1 <= amount[j] <= 1000
- The elements of product are unique.
- At most 1000 calls will be made to getBill.
- Answers within 10-5 of the actual value will be accepted.

---

## 题目（中文翻译）

描述  
超市的商品由两个平行整数数组 `products` 和 `prices` 表示，其中第 `i` 件商品的 ID 为 `products[i]`，价格为 `prices[i]`。  
当顾客结账时，他们的账单也由两个平行整数数组 `product` 和 `amount` 表示，其中第 `j` 件购买的商品 ID 为 `product[j]`，`amount[j]` 表示购买的数量。账单的小计（subtotal）计算为所有 `amount[j] * （对应商品的价格）` 的和。  

超市决定开展促销活动：每第 `n` 位结账的顾客可以获得一次折扣。折扣的幅度由 `discount` 给出，表示在小计上直接减去 `discount` 百分比。更正式地说，如果小计为 `bill`，则实际应付金额为 `bill * ((100 - discount) / 100)`。  

请实现 `Cashier` 类（Cashier class）：

```cpp
Cashier(int n, int discount, int[] products, int[] prices);
double getBill(int[] product, int[] amount);
```

- 构造函数 `Cashier` 初始化每 `n` 位顾客可享受 `discount`% 折扣，以及商品 ID 与对应价格的映射。  
- `getBill` 根据当前顾客的购物清单返回实际应付金额，并在计数到第 `n` 位顾客时应用折扣。  

示例  

```text
输入
["Cashier","getBill","getBill","getBill","getBill","getBill","getBill","getBill"]
[[3,50,[1,2,3,4,5,6,7],[100,200,300,400,300,200,100]],
 [[1,2],[1,2]],
 [[3,7],[10,10]],
 [[1,2,3,4,5,6,7],[1,1,1,1,1,1,1]],
 [[4],[10]],
 [[7,3],[10,10]],
 [[7,5,3,1,6,4,2],[10,10,10,9,9,9,7]],
 [[2,3,5],[5,3,2]]]
输出
[null,500.0,4000.0,800.0,4000.0,4000.0,7350.0,2500.0]
解释
Cashier cashier = new Cashier(3, 50, [1,2,3,4,5,6,7], [100,200,300,400,300,200,100]);

第 1 位顾客购买商品 1（1 件）和商品 2（2 件），应付 1*100 + 2*200 = 500.0（未满 3 位，不打折）。

第 2 位顾客购买商品 3（10 件）和商品 7（10 件），应付 10*300 + 10*100 = 4000.0（未满 3 位，不打折）。

第 3 位顾客购买每种商品各 1 件，总计 1+2+3+4+5+6+7 = 800.0，正好是第 3 位顾客，打 50% 折扣后实际应付 800.0 * 0.5 = 400.0（示例中返回 800.0 是因为在此实现里折扣在下一个顾客生效，具体实现细节请参考题意）。

随后第 4、5 位顾客同理计算，直到再次到达第 6 位顾客时再次触发折扣，依此类推，最终得到示例输出的各个金额。

约束条件  
- `1 <= n <= 10^4`  
- `0 <= discount <= 100`  
- `1 <= products.length <= 200`  
- `prices.length == products.length`  
- `1 <= products[i] <= 200`  
- `1 <= prices[i] <= 1000`  
- `products` 中的元素互不相同。  
- `1 <= product.length <= products.length`  
- `amount.length == product.length`  
- `product[j]` 必定在 `products` 中出现。  
- `1 <= amount[j] <= 1000`  
- `product` 中的元素互不相同。  
- 最多会调用 `getBill` 1000 次。  
- 答案相对误差在 `10^-5` 之内均视为正确。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**每次结账都去原始的 `products` 与 `prices` 两个数组里找对应商品的单价**，再把单价乘以购买数量累加得到小计，最后判断这是不是第 `n` 位顾客，若是就套用折扣公式。  

- **用到的数据结构**：仅仅是两个平行数组 `products`（商品编号）和 `prices`（对应的价格）。可以把它想象成一本“商品目录”，要找某本书的价格，就得把目录从头到尾翻一遍，看到对应的编号才算找到——这就是**线性查找**。  
- **为什么正确**：因为题目保证每个购买的商品编号一定在 `products` 中出现，只要我们把对应的价格找出来相乘累加，就得到准确的小计；随后根据 `n` 是否整除当前顾客计数来决定是否打折，公式本身没有歧义。  

#### 代码（Python）  

```python
class Cashier:
    def __init__(self, n: int, discount: int, products: list[int], prices: list[int]):
        """
        n          ：每第 n 位顾客打折
        discount   ：折扣百分比，如 50 表示 5 折
        products   ：商品编号列表
        prices     ：对应的单价列表
        """
        self.n = n
        self.discount = discount
        self.products = products      # 商品编号数组
        self.prices = prices          # 单价数组
        self.cnt = 0                  # 已经为多少位顾客结过账

    def getBill(self, product: list[int], amount: list[int]) -> float:
        """
        product : 本次结账的商品编号列表
        amount  : 对应的购买数量
        返回值  : 实际需要支付的金额（可能已打折）
        """
        self.cnt += 1                # 先把顾客计数加 1
        subtotal = 0                # 小计

        # 暴力查价：对每件商品，在 products 中线性搜索对应的下标，再取价格
        for pid, qty in zip(product, amount):
            # 在 products 中找到 pid 的位置 i
            i = 0
            while self.products[i] != pid:
                i += 1               # 线性遍历，最坏要遍历完整个数组
            price = self.prices[i]   # 取对应的单价
            subtotal += price * qty  # 累加该商品的总价

        # 判断是否需要打折
        if self.cnt % self.n == 0:    # 第 n、2n、3n… 位顾客
            discounted = subtotal * (100 - self.discount) / 100
            return discounted
        else:
            return float(subtotal)
```

#### 复杂度  

- **时间复杂度**：`O(m * k)`  
  - `m = len(product)`（本次结账的商品种类数）  
  - `k = len(products)`（所有商品的总种类数，最多 200）  
  - 对每件购买的商品我们都要在 `products` 中线性搜索一次，最坏要遍历 `k` 次，所以整体是 `m·k`。  
  - 大白话：如果超市有 200 种商品，而一次顾客买了 10 种，那么最多要比较 2000 次。  

- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外变量（计数器、临时的 `subtotal` 等），不随输入规模增长。

---

### 2. 最优解  

#### 思路  

从暴力解可以看出**瓶颈在于每次都要遍历 `products` 来找单价**。这一步的时间是线性的，虽然题目规模不大，但我们完全可以把查询过程改成 **常数时间**。

**核心技巧：哈希表（字典）**  
- 把 `products[i]` 作为 **键（key）**，`prices[i]` 作为 **值（value）**，存进 Python 的 `dict`。  
- 类比：字典就像一本“商品-价格对照手册”，直接翻到对应的页码（key）就能看到价格（value），不需要从头找。  

实现步骤如下：  

1. **构造阶段**（`__init__`）  
   - 用 `dict(zip(products, prices))` 把两数组一次性压缩成哈希表 `price_map`。这一步只做一次，耗时 `O(k)`，空间 `O(k)`。  

2. **结账阶段**（`getBill`）  
   - 计数器 `cnt` 同样自增。  
   - 对本次购买的每件商品，直接用 `price_map[pid]` 取单价，时间 `O(1)`。  
   - 累加得到小计后，再判断是否满足第 `n` 位顾客的条件，若是则套用折扣公式。  

这样每次 `getBill` 的时间从 `O(m·k)` 降到 **`O(m)`**，即只和本次购买的商品种类数成正比。  

#### 代码（Python）  

```python
class Cashier:
    def __init__(self, n: int, discount: int, products: list[int], prices: list[int]):
        """
        初始化 Cashier：
        - n, discount 同题意
        - 使用哈希表把商品编号映射到单价，后续查询 O(1)
        """
        self.n = n
        self.discount = discount
        self.cnt = 0                         # 已经为多少位顾客结过账
        # 哈希表：商品编号 -> 单价
        self.price_map = {pid: price for pid, price in zip(products, prices)}
        # 解释：就像一本“商品-价格字典”，查价像查字典一样快

    def getBill(self, product: list[int], amount: list[int]) -> float:
        """
        计算本次结账应付金额（可能已打折）。
        - 直接在哈希表里 O(1) 拿到单价
        - 累加后判断是否需要打折
        """
        self.cnt += 1                # 第几位顾客
        subtotal = 0

        # 对每件商品，直接通过哈希表获取单价
        for pid, qty in zip(product, amount):
            price = self.price_map[pid]   # O(1) 查表
            subtotal += price * qty

        # 是否第 n 位顾客（第 n、2n、3n…）
        if self.cnt % self.n == 0:
            # 打折：原价乘以 (100 - discount) / 100
            return subtotal * (100 - self.discount) / 100.0
        else:
            return float(subtotal)
```

#### 复杂度  

- **时间复杂度**：`O(m)`  
  - `m = len(product)`，每件商品只做一次哈希表查询（常数时间）。  
  - 与暴力解相比，从 `O(m·k)` 降到了 `O(m)`，当商品种类很多时提升明显。  

- **空间复杂度**：`O(k)`  
  - 需要额外存储一个哈希表，大小等于所有商品的种类数 `k`（最多 200），这在内存上是可以接受的。  
  - 大白话：我们把超市的“商品目录”提前写好，后面查价就像打开字典翻页一样快，只是多占一点纸（内存）。

---

## 心得  

- **核心技巧**：使用哈希表把商品编号映射到单价，实现 **O(1) 查询**。  
- **适用场景**：  
  1. “查询-更新”频繁且键唯一的数据，如 **键值对映射**（电话号码簿、商品价目表）。  
  2. 需要**快速计数**或**频率统计**的题目，如 **Two Sum**、**字母异位词分组**。  
  3. 任何需要**把数组转换为快速查找结构**的场景。  
- **一句话总结**：把“遍历找对应”变成“直接哈希取”，时间从线性搜索降到常数查询，就是这道题的解题钥匙。  

---

## 反思  

- **第一反应**：看到“每 nth 位顾客打折”，先想到要维护一个计数器；随后想到要把商品编号对应的价格存下来，最直观的做法是每次遍历原数组。  
- **最容易踩的坑**：  
  - 忘记在每次 `getBill` 调用后 **自增计数器**，导致折扣永远不生效或一直生效。  
  - 把 `discount` 当成 “打多少折” 而不是 “打几折”，公式应是 `price * (100 - discount) / 100`。  
  - 返回值必须是 `float`（即使没有折扣），因为题目要求答案在 `1e-5` 误差范围内。  
- **下次类似题的第一步**：先判断“是否需要频繁根据键查询对应值”。如果是，立刻把数据装进 **哈希表**，把“遍历找对应”这一步直接省掉。这样往往就能把时间复杂度从 `O(n·m)` 降到 `O(n)`，大幅提升效率。