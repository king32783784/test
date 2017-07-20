Title: 类常用内置方法
Date:2017-01-23
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

#### __init__()

__init__()方法是最常用的内置方法。它在一个类的对象被创建时，首先运行。这个方法可以用来做一些初始化工作，比如参数传入等。

例如：

    #!/usr/bin/env python
    # Filename: class_init.py
    
    class Person(object):
        def __init__(self, name):
            self.name = name
            
        def sayHi(self):
            print("hi, my name is %s", %self.name)
            
    p = Person('Swaroop')
    p.sayHi()
     
    输出： hi, my name is Swaroop
    
说明： __init__方法定义为传入一个参数name. 在__init__里，我们只是创建一个新的域，也成为name.两个name是两个不同的变量。在类的其他方法可以使用self.name。self.name成了该类的
属性。

#### __new__():

__new__()是在新式类中新出现的方法，它作用在构造方法建造实例之前，Python中存在于类里面的构造方法__init__负责将类实例化，而在__init__启动之前，__new__决定是否使用该__init__方法，因为
__new__()可以调用其他类的构造方法或返回别的对象类作为本类的实例。

如果将类比喻为工厂，那么__init__()方法则是该工厂的生成工人，__init__()方法接受的初始化参数则是生成所需原料，__init__()方法会按照方法中的语句负责将原料进行加工成实例产品。__new__的角色为
生产经理，__new__方法可以决定是否将原料提供给该生产部工人，同时决定着出货产品是否为为该生产部的产品。因为该生产经理(__new__)可以以该工厂的名义出售其他工厂的产品。

* __new__()方法的特性：

    * __new__()方法是在类准备将自身实例化时调用
    * __new__()方法始终是类的静态方法，即使没有被加上静态方法装饰器
    * 类的实例化和它的构造方法通常为：

    * 类定义
    class MyClass(object):
        def __init__(self, *args, **kwargs):
            ...
    
    * 实例化
    myclass = MyClass(*args, **kwargs)
    
正如以上所示，一个类可以有多个位置参数和多个命名参数，而在实例化开始之后，在调用__init__()方法之前，python首先调用__new__()方法：

    def __new__(cls, *args, **kwargs):
        ...
        
第一个参数cls是当前正在实例化的类。

* 如果要得到当前类的实例，应当在当前类中__new__()方法语句中调用当前类的父类的__new__()方法。

例如，如果当前类是直接继承自object, 那当前类的__new__()方法返回的对象应该为：

    def __new__(cls, *args, **kwargs):
        ...
        return object.__new__(cls)
        
**注意**

  事实上如果(新式)类中没有重写__new__()方法，即在定义新式类时没有重新定义__new__()时，python默认是调用该类的直接父类的__new__()方法来构造该类的实例，如果该类的父类也没有重写__new__(),
那么将一直按此规矩追溯至object的__new__()方法，因为object是所有的新式类的基类。

  而如果新式类中重写了__new__()方法，那么你可以自由选择任意一个其他的新式类(必定要是新式类，只有新式类有__new__(),因为新式类都是object的后代，经典类则没有__new__()方法来制造实例，包括这个新式类的所有前代类和后代类，只要他们不会造成递归死循环。具体看以下代码解释：
  
    class Foo(object):
        def __init__(self, *args, **kwargs):
            ...
        
        def __new__(cls, *args, **kwargs):
            return object.__new__(cls, *args, **kwargs)
            
    # 以上return等同于
    # return object.__new__(Foo, *args, **kwargs)
    # return Stranger.__new__(cls, *args, **kwargs)
    # return Child.__new__(cls, *args, **kwargs)
    
    class Child(Foo):
        def __new__(cls, *args, **kwargs):
            return object.__new__(cls, *args, **kwargs)
            
    # 如果child中没有重新定义__new__()方法，那么会自动调用其父类的__new__()方法来制造实例，即Foo.__new__(cls, *args, **kwargs)
    # 在任何新式类的__new__()方法，不能调用自身的__new__()来制造实例，因为这会造成死循环。因此必须避免类似一下的写法：
    # 在Foo中避免：return Foo.__new__(cls, *args, **kwargs)或return cls.__new__(cls, *args, **kwargs). Child同理。
    # 在object或者没有血缘关系的新式类的__new__()是安全的，但是如果是在继承关系的两个类之间，应避免互调造成死循环，例如：（Foo)return Child.__new__(cls), (Child)return Foo.__new__(cls).
    
    class Stranger(object):
       ...
    # 在制造Stranger实例时，会自动调用object.__new__(cls)
    
* 通常来说，新式类开始实例化时， __new__()方法会返回cls(cls指代当前类）的实例，然后该类的__init__()方法作为构造方法会接收这个实例(即self)作为自己的第一个参数，然后依次传入__new__方法中
 接收的位置参数和命名参数。
 
注意： 如果__new__()没有返回cls(即当前类）的实例，那么当前类的__init__()方法是不会被调用的。如果__new__()返回其他类(新式类或经典类均可)的实例，那么只会调用被返回的那个类的构造方法。

    class Foo(object):
        def __init__(self, *args, **kwargs):
            ...
            
        def __new__(cls, *args, **kwargs):
            return object.__new__(Stranger, *args, **kwargs)
            
    class Stranger(object):
       ...
       
    foo = Foo()
    print type(foo)
    
    # 打印结果显示foo其实是Stranger类的实例
    # 因此可以这么描述__new__()和__init__()的区别，在新式类中__new__()方法才是真正的实例化方法，为类提供外壳制作出实例框架，然后调用该框架内的构造方法__init__()使其丰满。
    # 如果以建房子做比喻， __new__方法负责开发地皮，打下地基，并将原料存放在工地。而__init__()方法负责从工地取材料建造出地皮开发招标书中规定的大楼，__init__()负责大楼的详细设计建造，装修使其可交付给客户。
    
    

            


