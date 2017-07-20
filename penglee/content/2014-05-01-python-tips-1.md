Title: Python-Tips(一）
Date:2014-05-01
Author:李鹏
Slug:python 
Tags:Python-Tips
category:编程语言-Python

**Tips01**

* 通过使用sys.path.insert(0,new_path)，你可以插入一个新的目录到sys.path列表的第一项，从而使其出现在Python搜索路径的开头。

**Tips02**

* Python中一切皆对象，字符串、列表、函数、类、类的实例、模块等都是对象。

**Tips03**

* Python使用try...except块来处理异常

    try:
         import hello
    except ImportError:
         print("hello")

**Tips04**

* Python 中所有东西都是区分大小写

**Tips05**

* Python 重要的内置数据类型包括布尔型、数值型、字符型、字节、列表、元组、集合、字典；模块、函数、类、方法、文件
* 可以用type查看类型
* isinstance() 判断是否为给定类型，如isinstance(1, int)

**Tips06**

* /运算符执行浮点除法（python3中）
* // 运算符执行古怪的整数除法,用之前最好先判断

**Tips07**

* Python 支持大部分数学运算，但需要导入对应模块

**Tips08**

* 列表是以类的形式实现的，列表支持多种方法进行操作，如append(),extend(), insert()

* append()的参数可以是任何类型的数据，追加到原列表，extend()，参数必须是列表，类似于两个列表的拼接

* count返回列表中元素出现次数， index()返回列表元素的索引（同样元素多个的情况下，只返回第一个元素）

* 列表中不会存在空隙。del用于进行索引删除，remove用于元素删除（多个同样删除第一个）

* pop()删除列表中最后的元素，并返回所删除的值，pop[弹出]删除并返回指定位置的值

* 空列表为假，非空为真

* enumerate()函数可以同时得到索引和对应的值

**Tips09**

* 元组不可变的列表；元素用()闭合，列表为[]

* 元组切片和列表一样，切片可以得到新的元组

* 不可变更的特点，元组不支持append、insert、remove、pop等方法

* 元组比列表快；可以对数据进行“写保护”，元组可以作为字典键（不可变）

* 元组可以转换为列表-list()，列表也可以转换成元组-tuple() 转换：生成对应的元组或列表

* 空元组为加，非空为真；单元素元组，单元数后加","，如a=(1) a为int型；a=(1,) a为tuple

* 元组可以一次赋多个值，如a=(1,2,3) x,y,z = a x=1,y=2,z=3 内建的range()函数构造了一个整数序列,如x,y,x = range(3) 

**Tips10**

* 集合可以包含任何元素的数据，{}

* 使用set函数，将列表创建为集合，集合是无序的;用set()可以创建空集合，a=set(),因为{}是一个字典

* add()方法可以扩展集合，接收任何参数（但集合是唯一值的，相同值只能有一份）

* update()方法效果是合并两个集合

* discard()删除集合的元素（接受一个单值作为参数）；remove（）类似，但remove删除元素不存在时会触发KeyError

* pop()方法从集合删除元素，并返回对应值，集合是无序的，所以只能随机弹出;空集合弹出会触发KeyError

* clear()方法可以将集合清空

* in:判断是否集合是否存在该元素；　union()合并两个集合；　intersection()返回两个集合的交集；difference()返回两个集合的补集（a出现，b没有）；　symmetric_difference()返回只在其中一个集合出现的元素; 

* issubset()判断是否为子集，issuperset()判断是否为超集

* 和列表、元组一样，空集合为假，非空为真






