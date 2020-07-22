<!--
 * @Author: jokerkeny
 * @Date: 2020-07-21 04:24:26
 * @LastEditors: jokerkeny
 * @LastEditTime: 2020-07-22 02:11:57
 * @Description: file content
--> 
合租一个月租6000元的三室公寓，谁住主卧谁住次卧谁住客房？每人该付多少钱？  
一份价格100元的寿司套餐里，有一个金枪鱼海胆手卷和一个蟹棒手卷，两人各选一个该如何分？  
double date住酒店，都想住标间，但酒店只剩一套\$200的标间和一套\$600豪华双人间，这两对情侣都不愿意住这么贵的豪华双人间，但愿意给标间多付点钱，能否协商入住呢？  
……  
这些问题经过抽象变成下文的模型，还可以泛化，比如竞拍者可以是两个国家，形成基于比较优势的贸易模式，报价可以是生产率，也可以是负的生产时间。  
可以用负的报价表示损失，比如在任务分配问题中，负数报价可以是时间消耗，也可以是要求分得的奖金。

若是对理论不感兴趣，可以直接跳到文末[一个简单的在线实现方法](#一个简单的在线实现方法)

# 多物品拍卖（最优分配算法）
该算法的目的是把总价为<img src="svgs/c0e79c1903ae281461a9393c4c3b3021.svg?invert_in_darkmode" align=middle width=16.62673319999999pt height=24.7161288pt/>的n个物品更有效的分配给n个人，实现效用最大化以及相对公平的分价。
## 理论步骤
### 封闭报价
n个竞拍者封闭报价，给出自己对n个物品的报价，反映n个物品对**自己**的效用（并不是“认为他人应为该物品付多少钱”，而是**自己**愿意为单独购买此物品所付的价格，与他人无关），形成报价矩阵<img src="svgs/dab9b7f48541e38f88b599bc81639aba.svg?invert_in_darkmode" align=middle width=20.83533374999999pt height=22.465723500000017pt/>
<p align="center"><img src="svgs/6b2f69a9ddacca88e5b113dd89964b20.svg?invert_in_darkmode" align=middle width=171.4652313pt height=88.76800184999999pt/></p>

其中第1行<img src="svgs/0e7d734ea7ea05e0e8d92a9c56a2269f.svg?invert_in_darkmode" align=middle width=135.78563624999998pt height=22.465723500000017pt/>即第1个人对n个物品的报价。  
...以此类推

因此每行之和，即每个人的对所有物品的报价和，都等于原始n个物品的总价<img src="svgs/c0e79c1903ae281461a9393c4c3b3021.svg?invert_in_darkmode" align=middle width=16.62673319999999pt height=24.7161288pt/>

### 物品分配
(虚拟)卖家将挑选出最优报价组合<img src="svgs/207d572cd221ca87e47f5f117f2213a6.svg?invert_in_darkmode" align=middle width=137.18360864999997pt height=24.65753399999998pt/>，使报价组合的总价格<img src="svgs/350efd48f7f10d8b1453a434c935fec1.svg?invert_in_darkmode" align=middle width=196.68660659999998pt height=22.465723500000017pt/>最高  
其中<img src="svgs/3bf666e5de563cb17e8c51e17ac9d52a.svg?invert_in_darkmode" align=middle width=75.48094289999999pt height=21.68300969999999pt/>代表矩阵中互不相同的n行，即n个不一样的人  
物品1将分配给第<img src="svgs/47052b496001b26f18651237c317563f.svg?invert_in_darkmode" align=middle width=12.21577334999999pt height=21.68300969999999pt/>个人  
物品2将分配给第<img src="svgs/d1d06b56596ac0b076c455596b357d7d.svg?invert_in_darkmode" align=middle width=12.21577334999999pt height=21.68300969999999pt/>个人  
......以此类推  

### 实际支出
n个物品原本的总价是固定的<img src="svgs/c0e79c1903ae281461a9393c4c3b3021.svg?invert_in_darkmode" align=middle width=16.62673319999999pt height=24.7161288pt/>（比方说一个包含可乐、鸡翅、薯条、汉堡的套餐总价为30元）  
显然，拍卖后卖家挑选的最优报价组合的总价格 <img src="svgs/b3868eb61a1bb775c0ac6fdbfb3e7981.svg?invert_in_darkmode" align=middle width=51.38113694999999pt height=24.7161288pt/>（仅在所有人报价完全一致时取等）

由于本方案的目的是更好的分配物品，拍卖的卖家是虚拟的，无须盈利。所以我们要**调整实际支出**，使得所有人的实际支出和等于物品的原始总价。

此处给出两种方法，第一种熟悉的**Normalize正则化**基于效用的比例差异，第二种**均匀返现**基于效用的绝对值差异，绝对值差异在数学上会更严谨。但严谨程度都取决于竞拍人在报价反映自身效用时的想法。

#### Normalize正则化
已知<img src="svgs/df5a289587a2f0247a5b97c1e8ac58ca.svg?invert_in_darkmode" align=middle width=12.83677559999999pt height=22.465723500000017pt/>为最优报价组合的总价格，<img src="svgs/c0e79c1903ae281461a9393c4c3b3021.svg?invert_in_darkmode" align=middle width=16.62673319999999pt height=24.7161288pt/>为n个物品原始价格总额。则设正则项
<p align="center"><img src="svgs/6848a6244a704b6b1a4310b7ed828c82.svg?invert_in_darkmode" align=middle width=74.60374019999999pt height=33.62942055pt/></p>

设第i个人在最优组合中被分配到了物品j，
则每个人调整后的实际支出为
<p align="center"><img src="svgs/d82e2a87f17bc708c8b3d6e7ad7107a8.svg?invert_in_darkmode" align=middle width=143.78094225pt height=38.864210549999996pt/></p>


#### 均匀返现
虚拟卖家把超额利润<img src="svgs/b9867cda17caabfbfa0bb09e34ca4bae.svg?invert_in_darkmode" align=middle width=49.55469749999998pt height=24.7161288pt/>均分给所有n个竞拍者，即
<p align="center"><img src="svgs/4188dc9149b6a2a03be57b9330f8f15a.svg?invert_in_darkmode" align=middle width=137.67243765pt height=34.75462155pt/></p>

### 最终效果
显然，每个人的实际支出<img src="svgs/9df9cc8c13822e8722019b07dff39ebc.svg?invert_in_darkmode" align=middle width=14.81734484999999pt height=24.7161288pt/>都将小于他对该物品的原报价<img src="svgs/e257acd1ccbe7fcb654708f1a866bfe9.svg?invert_in_darkmode" align=middle width=11.027402099999989pt height=22.465723500000017pt/>。因此，经过组合团购&拍卖交易后，每个人获得的效用增加了。
## 数学证明
假设效用可以用货币来衡量。
设第j个物品给第i个人带来的效用（Utility）为<img src="svgs/91d79fc058413bff469d160f74946464.svg?invert_in_darkmode" align=middle width=21.979146749999988pt height=22.465723500000017pt/>，报价为<img src="svgs/dab9b7f48541e38f88b599bc81639aba.svg?invert_in_darkmode" align=middle width=20.83533374999999pt height=22.465723500000017pt/>，那么假如报价即为此人购买该物品的支出，则购买物品j给第i个人带来的收益为
<p align="center"><img src="svgs/d91195d5c17a330500c1871393a93329.svg?invert_in_darkmode" align=middle width=197.45404634999997pt height=17.031940199999998pt/></p>

假设任何一个竞拍者，对所有物品的报价都真实反映了该物品对自己的效用，则所有物品给该竞拍者带来的收益都相等。即
<p align="center"><img src="svgs/a9182560b2ceccddad6845f937e66266.svg?invert_in_darkmode" align=middle width=258.34341059999997pt height=14.611878599999999pt/></p>

记为<img src="svgs/2dad7b36055f507dc73d7967cbebba34.svg?invert_in_darkmode" align=middle width=50.17920929999999pt height=22.831056599999986pt/>。

因竞拍者对n个物品报价之和为原本的总价<img src="svgs/c0e79c1903ae281461a9393c4c3b3021.svg?invert_in_darkmode" align=middle width=16.62673319999999pt height=24.7161288pt/>是固定的，易得
<p align="center"><img src="svgs/e4a697f57fee854080c9ec330f098226.svg?invert_in_darkmode" align=middle width=378.8674263pt height=38.07505515pt/></p>
又由式(1)可得
<p align="center"><img src="svgs/2a63a1ee59f529839317890b162dd8b7.svg?invert_in_darkmode" align=middle width=191.34956115pt height=17.031940199999998pt/></p>
此式说明，由于<img src="svgs/2dad7b36055f507dc73d7967cbebba34.svg?invert_in_darkmode" align=middle width=50.17920929999999pt height=22.831056599999986pt/>对第i个人是固定的常数，那么他对不同物品的**报价**的**绝对值差异**，和不同物品给他带来的**效用**的**绝对值差异**，是相等的。
### 总效用最大化
以下给出两种思路，证明该分配方案能使所有人得到的总效用最大化。（自然也是帕累托最优）

#### 证明1：

已知报价组合的总价格为
<p align="center"><img src="svgs/bad5a0937f37cb32538384d2f41b7b89.svg?invert_in_darkmode" align=middle width=272.88659475pt height=47.1348339pt/></p>

其中<img src="svgs/2c0c126fa01c5e5dfc5b1faa7b319032.svg?invert_in_darkmode" align=middle width=89.08829159999999pt height=24.65753399999998pt/>是1到n的一个排列，表示第<img src="svgs/36b5afebdba34564d884d347484ac0c7.svg?invert_in_darkmode" align=middle width=7.710416999999989pt height=21.68300969999999pt/>个物品分配给<img src="svgs/b60fd85f5e6f4ba2e90e7a46b0e8d2d9.svg?invert_in_darkmode" align=middle width=11.767735649999992pt height=21.68300969999999pt/>。

又由式(2)可得
<p align="center"><img src="svgs/faed57ff824d13fea413b095070fae65.svg?invert_in_darkmode" align=middle width=351.55793639999996pt height=47.1348339pt/></p>

又由式(3)可知，<img src="svgs/2dad7b36055f507dc73d7967cbebba34.svg?invert_in_darkmode" align=middle width=50.17920929999999pt height=22.831056599999986pt/>在分配前已经是固定的了，<img src="svgs/84f188adbf31f077676f85971953e424.svg?invert_in_darkmode" align=middle width=92.38722734999999pt height=26.438629799999987pt/>是一个常数，而<img src="svgs/adbe2b0427e1bbadee00a9673927e1d9.svg?invert_in_darkmode" align=middle width=71.78190194999999pt height=26.438629799999987pt/>就是所有物品分配后给所有人带来的总效用。所以<img src="svgs/ee3a85572cf014a7dec77da2ca6b9d0c.svg?invert_in_darkmode" align=middle width=47.53983629999998pt height=22.465723500000017pt/>。

因此最优报价组合在最大化报价组合的总额<img src="svgs/df5a289587a2f0247a5b97c1e8ac58ca.svg?invert_in_darkmode" align=middle width=12.83677559999999pt height=22.465723500000017pt/>的同时，也使得总效用最大化。

#### 证明2：

还有另外一种证明思路，总共有<img src="svgs/50c0357224674ab662b8ea5e5ca3eb8a.svg?invert_in_darkmode" align=middle width=14.433101099999991pt height=22.831056599999986pt/>个**可行报价组合**<img src="svgs/207d572cd221ca87e47f5f117f2213a6.svg?invert_in_darkmode" align=middle width=137.18360864999997pt height=24.65753399999998pt/>，倘若每个人的支出和报价一致，那么无论怎样组合，第i个人获得的收益始终是<img src="svgs/165e81a9941eb4296492a4c565e095d9.svg?invert_in_darkmode" align=middle width=50.17920929999999pt height=22.831056599999986pt/>。  
但**最优报价组合**能使报价之和<img src="svgs/df5a289587a2f0247a5b97c1e8ac58ca.svg?invert_in_darkmode" align=middle width=12.83677559999999pt height=22.465723500000017pt/>最大，则虚拟卖家获得的“超额收益”<img src="svgs/b9867cda17caabfbfa0bb09e34ca4bae.svg?invert_in_darkmode" align=middle width=49.55469749999998pt height=24.7161288pt/>能达到最大，虚拟卖家的这部分收益是会全额返还给竞拍者的。  
假如把超额收益**均匀返现**，则第i个人最终获得的实际收益为<img src="svgs/aa23508f2161c4b51b588d2e28b0230d.svg?invert_in_darkmode" align=middle width=108.06267119999998pt height=31.99855889999998pt/>。所有物品原始价格<img src="svgs/c0e79c1903ae281461a9393c4c3b3021.svg?invert_in_darkmode" align=middle width=16.62673319999999pt height=24.7161288pt/>不变，则报价组合的总额<img src="svgs/df5a289587a2f0247a5b97c1e8ac58ca.svg?invert_in_darkmode" align=middle width=12.83677559999999pt height=22.465723500000017pt/>越大，每个人得到的收益越大。


*其实除了效用最大化，还有两点需要证明，一是竞拍者为什么会严格根据物品带来的效用差异来报价，即从博弈论的角度证明这是竞拍者的最优策略。二是如何调整实际支出，即怎样把“超额收益”返还给竞拍者最合理（我个人是觉得normalize在物品价差较大时更合理）。*

# Reference
起初就如引子里所提，由于存在物品分配/分价上的不一致，我基于对拍卖的一些初浅认识，尝试琢磨出这么一套方案，随后意外发现可以数学上证明它能使效用最大化。

不过在我试图提交到github时，搜了搜现有的repo，发现该问题经过假设抽象后，就成了[Assignment Problem](https://en.wikipedia.org/wiki/Assignment_problem)，并有成熟的算法如[Hungarian algorithm](https://en.wikipedia.org/wiki/Hungarian_algorithm)以<img src="svgs/90846c243bb784093adbb6d2d0b2b9d0.svg?invert_in_darkmode" align=middle width=43.02219404999999pt height=26.76175259999998pt/>来求解该模型的最优化问题。

# 一个简单的在线实现方法
step 1:每个人准备好自己的报价写进自己私人的google sheet

step 2:过3分钟，大家一起公开自己的报价sheet的只读sharelink。（由于google sheet的修改记录是可见的，可验证3分钟内不存在报价变动。）

step 3:在colab里打开程序，输入报价并运行。当然也可以直接下载auction.py或auction.ipynb在本地运行。

其中step1 & 2是用于可靠的封闭报价的，sharelink得一起公开，否则存在事先准备好多个googlesheet的作弊漏洞。  
如果没法使用google服务，可用加密的excel代替，随后公开密码。
如果在现实中当面报价，Step 1 & 2可直接用纸笔封闭报价代替。  

> Written with [StackEdit](https://stackedit.io/).  
> Convert to github markdown by [readme2tex](https://github.com/leegao/readme2tex)