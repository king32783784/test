Title: 类常用内置方法(二）
Date:2017-02-13
Author:李鹏
Slug: python
Tags:Python
category:编程语言-Python

python的类中包含很多内置的方法。

### 内置方法列表

以下是一些基本的内置方法，后面还会列举一些其他的方法。

| 内置方法             |                说明
| --------------------| ---------------------------------------
| __init__(self,...)  | 初始化对象，在创建新对象时调用
| __del__(self)       | 释放对象，在对被删除之前调用
| __new__(cls, *args, **kwd) | 实例的生成操作
| __str__(self)       | 在使用print语句时被调用
| __getitem__(self, key) | 获取序列的索引key对应的值，等价于seq[key]
| __len__(self)        | 在调用内联函数len()时被调用
| __cmp__(stc, dst)    | 比较两个对象src和dst
| __getattr__(s, name) | 获取属性的值
| __setattr__(s, name,value) | 设置属性的值
| __delattr__(s, name) | 删除name属性
| __getattribute__() | 功能与__getattr__()类似
| __gt__(self, other) | 判断self对象是否大于other对象
| __lt__(self, other) | 判断self对象是否小于other对象
| __ge__(self, other) | 判断self对象是否大于或则等于other对象
| __le__(self, other) | 判断self对象是否小于或等于other对象
| __eq__(self, other) | 判断self对象是否等于other对象
| __call__(self,*args) |  把实例对象作为函数调用 

#### __del__()

  在实例即将销毁时调用。它也被称作析构器。如果一个基类具有一个__del__()方法，继承类的__del__()方法，如果存在，必须显式的调用它以确保实例的基类部分的正确删除。注意__del__()方法可以（虽然不推荐）通过创建该实例的一个新的引用以推迟它的销毁。它可以在以后该新的引用被删除时调用。不能保证在解释器退出时仍然存在的对象的__del__()被调用。

#### __getattr__()、__setattr__()和__getattribute__():

  当读取对象的某个属性时，python会自动调用__getattr__()方法。例如,fruit.clor将转换为fuit.__getattr__(color). 当使用赋值语句对属性进行设置时，python会自动调用__getattr__
__setattr__()方法。__getattribute__()的功能与__getattr__()类似，用于获取属性的值。但是__getattribute__()能提供更好的控制，代码更健壮。注意，python中并不存在
__setattribute__()方法

例子

    #!/usr/bin/python
    # -*-coding:UTF-8-*-*
    
    class Fruit(object):
        def __init__(self, color = "red", price = 0):
            self.__color = color
            self.__price = price
            
        def __getattribute__(self, name): # 获取属性的方法
            return object.__getattribute__(self, name)
            
        def __setattr__(self, name, value):
            self.__dict__[name] = value
            
    if __name__ == '__main__":
        fruit = Fruit("blue", 10)
        print fruit.__dict__.get("_Fruit_color") # 获取color属性
        fruit.__dict__["_Fruit__price"] = 5
        print fruit.__dict__.get("_Fruit__price") # 获取price属性
        
#### __getitem__():

如果类把某个属性定义为序列， 可以使用__getitem__()输出序列属性中某个元素。假设水果店中销售多种水果，可以通过__getitem__()方法获取水果店中的每种水果

实例：

    #!/usr/bin/python
    # -*- coding: UTF-8 -*-
    class FruitShop:
        def __getitem__(self, i):  # 获取水果店的水果
            return self.fruits[i]
            
    if __name__ == "__main__":
        shop = FruitShop()
        shop.fruits = ["apple", "banana"]
        print shop[1]
        for item in shop:  # 输出水果店的水果
            print item

#### __str__():

__str__()用于表示对象代表的含义，返回一个字符串。实现了__str__()方法后，可以直接使用print语句输出对象，也可以通过函数str()触发__str__()的执行。这样
就把对象和字符串关联起来，便于某些程序的实现，可以用这个字符串来表示某个类

示例：

    #!/usr/bin/python
    # -*-coding: UTF-8 -*-
    class Fruit:
        '''Fruit类'''  # 为Fruit类
        def __str__(self):  # 定义对象的字符串表示
            return self.__doc__
        
    if __name__ == '__main__":
        fruit = Fruit()
        print str(fruit)   # 调用内置函数str()出发__str__()方法， 输出结果为：Fruit类
        print fruit        # 直接输出对象fruit, 返回__str__()方法的值， 输出结果为：Fruit类
        
#### __call__():

在类中实现__call__()方法，可以在对象创建时直接返回__call__()的内容。使用该方法可以模拟静态方法。

示例：

    #!/usr/bin/python
    # -*- coding: UTF-8 -*-
    
    class Fruit:

        class Growth:    # 内部类
            def __call__(self):
                print "grow..."
                
        grow = Growth()  # 调用Growth(), 此时将类Growth作为函数返回，即为外部类Fruit定义方法 grow(),grow()将执行__call__()内的代码
        
    if __name__ == "__main__":
        fruit = Fruit()
        fruit.grow()  # 输出结果： grow...
        Fruit.grow()  # 输出结果： grow...
        



