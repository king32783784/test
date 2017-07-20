Title: python metaclass(下）
Date:2017-01-15
Author:李鹏
Slug: 编程语言-Python 
Tags:Python
category:编程语言-Python

### 自定义元类

元类的主要目的就是为了当创建类时能够自动地改变类。通常，你会为API做这样的事情，你希望可以创建符合当前上下文的类。假想一个很傻的例子，你决定在你的模块里所有的类的属性都应该是大写形式。有好几种方法可以办到，但其中一种就是通过在模块级别设定__metaclass__。采用这种方法，这个模块中的所有类都会通过这个元类来创建，我们只需要告诉元类把所有的属性都改成大写形式就万事大吉了。

幸运的是，__metaclass__实际上可以被任意调用，它并不需要是一个正式的类（我知道，某些名字里带有‘class’的东西并不需要是一个class，画画图理解下，这很有帮助）。所以，我们这里就先以一个简单的函数作为例子开始。

    # 元类会自动将你通常传给“type"的参数作为自己的参数传入
    def upper_attr(future_class_name, future_class_parents, future_class_attr)
        """返回一个类对象，将属性都转为大写形式”“”
        # 选择所有不以“__"的属性
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
        
    # 将他们转为大写形式
    uppercase_attr = dict((name.upper(), value) for name, value in attrs)
    
    # 通过type来做类对象的创建
    return type(future_class_name, future_class_parents, uppercase_attr)
    
    __metaclass__ = upper_attr # 这会作用到这个模块所有的类
    
    class Foo(object):
        # 我们可以只在这里定义__mataclass__,这样就只会作用于这个类中
        bar = 'bip"
    print hasattr(Foo, 'bar')
    # 输出 False
    print hasattr(Foo, 'BAR')
    # 输出 True
    f = Foo()
    print f.BAR
    # 打印"bip"
    
下面是用一个真正的class作为元类。

    # 记住， ‘type'实际上是一个类， 就像‘str'和’int'一样
    # 所以，可以从type继承
    class UpperAttrMetaClass(type):
        # __new__是在__init__之前被调用的特殊方法
        # __new__是用来创建对象并返回的方法
        # 而__init__只是用来将传入的参数初始化给对象
        # __new__很少用到，除非你希望能够控制对象的创建
        # 这里创建的对象是类，我嫩希望能够自定义它， 所以我们这里改写__new__
        # 如果你希望的话，可以在__init__中做些事情
        # 还有一些高级的用法会涉及到改写__call__特殊方法，但是我们这里不用
        
        def __new__(upperattr_metaclass, future_class_name,
                    future_class_parents, future_class_attr):
            attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
            uppercase_attr = dict((name.upper(), value) for name, value in attrs)
            return type(future_class_name, future_class_parents, uppercase_attr)
            
但是这种方法其实不是oop。我们直接调用了type, 而且我们没有改写父类的__new__方法。 现在我们这样处理：

    class upperattr_metaclass(type):
        def __new__(upperattr_metaclass, future_class_name,
                    future_class_parents, future_class_attr):
            attrs = ((name, value) for name, value in future_class_attr.items() 
                      if not name.startswith('__')
            uppercase_attr = dict((name.upper(), value) for name, value in attrs)
            
            # 复用type.__new__方法
            # 这就是OOP编程
            return type.__new__(upperattr_metaclass, futurn_class_name, 
                                future_class_parents, uppercase_attr)
                                
你可能已经注意到了有个额外的参数upperattr_metaclass, 这并没有什么特别的。类方法的第一个参数总是表示当前的实例， 就像在普通的类方法中的self参数一样。当然，为了清晰起见，
这里的名字我起的比较长。但是就像self一样，所有的参数都有他们的传统的名称。因此在一个真实产品中的一个元类应该像这样：

    class UpperAttrMetaclass(type):
        def __new__(cls, name, bases, dct):
            attrs = ((name, value) for name, value in dct.items() if not name.startswith('__')
            uppercase_attr = dict((name.upper(), value) for name, value in attrs)
            return type.__new__(cls, name, bases, uppercase_attr)
            
如果使用super方法的话，我们还可以使它变得更清晰一些，这会缓解继承（是的，你可以拥有元类，从元类继承，从type继承）

    class UpperAttrMetaclass(type):
        def __new__(cls, name, bases, dct):
            attrs = ((name, value) for name, value in dct.items() if not name.startswith('__')
            uppercase_attr = dict((name.upper(), value) for name, value in attrs)
            return supper(UpperAttrMetaclass, cls).__new__(cls, name, bases, uppercase_attr)
            
就是这样，除此之外，关于元类真的没有别的可说的了。使用到元类的代码比较复杂，这背后的原因并不是因为元类本身，而是因为你通常会使用元类去做一些晦涩的事情，依赖于自身，
控制继承等等。确实，用元类搞些”黑魔法“是特别有用的，因而会搞出复杂的东西来。但就元类本身而言，其实是很简单的：

* 1) 拦截类的创建
* 2) 修改类
* 3) 返回修改之后的类

### 为什么要用metaclass类而不是函数？

由于__metaclass__ 可以接受任何可调用的对象，那为何还要使用类呢，因为很显然使用类会更加复杂啊？原因如下：

* 1) 意图会更加清晰。当你读到UpperAttrMetaclass(type)时，你知道接下来会发生什么
* 2) 可以使用oop编程。元类可以从元类中继承而来，改写父类的方法。元类甚至还可以使用元类
* 3) 可以把代码组织的更好。当你使用元类的时候肯定不会向上面的这种简单场景，通常都是针对比较复杂的问题。将多个方法归并到一个类中会很有帮助。
* 4) 可以使用__new__, __init__已经__call__这样的特殊方法。他们能帮你处理不同的任务。通常你可以把所有的东西都在__new__里处理掉，有些人还是觉得__init__更舒服。
* 5) 哇哦，这东西的名字是metaclass, 肯定非善类，要小心

### 什么地方使用元类？

现在回到主题，究竟为什么会使用这样一种容易出错而且晦涩的特效？一般来说，根本就用不上它：

    “元类就是深度的魔法，99%的用户应该根本不必为此操心。如果你想搞清楚究竟是否需要用到元类，那么你就不需要它。那些实际用到元类的人都非常清楚地知道他们需要做什么，而且根本不需要解释为什么要用元类。”  —— Python界的领袖 Tim Peters
    
元类的主要用途是创建API。一个典型的例子是Django ORM. 它允许你像这样定义：

    class Person(models.Model):
        name = models.CharField(max_length=30)
        age = models.IntegerField()
        
但是如果你像这样做的话：

    guy = Person(name='bob', age='35')
    print guy.age
    
这并不会返回一个IntegerField对象， 而是会返回一个int， 甚至可以直接从数据库中取出数据。这是有可能的，因为models.Model定义了__metaclass__,并且使用了一些魔法能够将你刚刚定义的
简单的Person类转变成对数据库的一个复杂hook。Django框架将这些看起来很复杂的东西通过暴露一个简单的使用元类的API将其化简，通过这个API重新创建代码，在背后完成真正的工作。

### 最后

首先，类其实是能够创建出类实例的对象。当然，类本身也是实例，是元类的实例。

    >>>class Foo(object): pass
    >>>id(Foo)
    38082608
python中的一切都是对象，他们要么是类的实例，要么是元类的实例，除了type.type实际上是它自己的元类，在纯Python环境中不能做到的，需要在实现层面通过一些手段做到的。
其次，元类是很复杂的。 对应非常简单的类，你可能不希望通过元类来对类做修改。你可以通过其他两种技术来修改类：

* 1) Monkey patching
* 2) class decorators

当你需要动态修改类时，最好使用上面的两种技术。当然，绝大部分情况下是不需要动态修改类的。

《完》

上一篇[python metaclass(上)](https://king32783784.github.io/2015/10/03/python/)

<img src="https://d2lm6fxwu08ot6.cloudfront.net/img-thumbs/280h/WBB0EXYSWE.jpg" height="320" width="540">

