Title: python metaclass(上）
Date:2016-10-03
Author:李鹏
Slug:编程语言-Python 
Tags:Python
category:编程语言-Python


### 类也是对象

在理解元类之前，需要先掌握python中的类。Python中的类的概念借鉴于Smalltalk, 显得有些奇特。大多数编程语言中，类就是一组用来描述如何生成一个对象的代码段。在Python中这一点仍然成立：

    >>> class ObjectCreator(object):
    ...     pass
    ... 
    >>> my_object = ObjectCreator()
    >>> print my_object
    <__main__.ObjectCreator object at 0x7fcad0b76590>
    >>> 
    
但是python的类还远不止如此。类同样也是一种对象。是的，没错，就是对象。只要使用关键字class,Python解释器在执行的时候就会创建一个对象。下面的代码段：

   >>> class ObjectCreator(object):
   ...     pass
   ...
   
将在内存中创建一个对象，名字就是ObjectCreator. **这个对象（类）自身具有创建对象（类示例）的能力，而这就是为什么它是一个类的原因.** 但是，它的本质仍然是一个对象，于是乎你可以对它做如下的操作：

* 1）可以将它赋值给一个变量
* 2）可以拷贝它
* 3）可以为它增加属性
* 4）可以将它作为函数参数进行传递

下面是示例：

    >>> print ObjectCreator     # 你可以打印一个类，因为它其实也是一个对象
    <class '__main__.ObjectCreator'>
    >>> def echo(o):
    …       print o
    …
    >>> echo(ObjectCreator)                 # 你可以将类做为参数传给函数
    <class '__main__.ObjectCreator'>
    >>> print hasattr(ObjectCreator, 'new_attribute')
    Fasle
    >>> ObjectCreator.new_attribute = 'foo' #  你可以为类增加属性
    >>> print hasattr(ObjectCreator, 'new_attribute')
    True
    >>> print ObjectCreator.new_attribute
    foo
    >>> ObjectCreatorMirror = ObjectCreator # 你可以将类赋值给一个变量
    >>> print ObjectCreatorMirror()
    <__main__.ObjectCreator object at 0x8997b4c>
    
### 动态地创建类

因为类也是对象，可以在运行时动态的创建他们，就像其他任何对象一样。首先，可以在函数中创建类，使用class关键字即可。

    >>> def choose_class(name):
    …       if name == 'foo':
    …           class Foo(object):
    …               pass
    …           return Foo     # 返回的是类，不是类的实例
    …       else:
    …           class Bar(object):
    …               pass
    …           return Bar
    …
    >>> MyClass = choose_class('foo')
    >>> print MyClass              # 函数返回的是类，不是类的实例
    <class '__main__'.Foo>
    >>> print MyClass()            # 你可以通过这个类创建类实例，也就是对象
    <__main__.Foo object at 0x89c6d4c>
    
但这还不够动态，仍然需要自己编写整个类的代码。由于类也是对象，所以它们必须是通过什么东西生成的才对。当你使用class关键字时，Python解释器自动创建这个对象。
但就和Python中大多数事情一样，Python仍然提供给你手动处理的方法。还记得内建函数type吗？这个古老而又强大的函数能够让你知道一个对象的类型是什么，就像这样：

    >>> print type(1)
    <type 'int'>
    >>> print type("1")
    <type 'str'>
    >>> print type(ObjectCreator)
    <type 'type'>
    >>> print type(ObjectCreator())
    <class '__main__.ObjectCreator'>

这里，type有一种完全不同的能力，能动态的创建类。type可以接受一个类的描述作为参数，然后返回一个类。（根据传入参数的不同，同一个函数拥有两种完全不同的用法是一件
很傻的事情，但这在python中是为了保持向后兼容性）

type可以像这样工作：

    type(类名， 父类的元组（针对继承的情况，可以为空）， 包含属性的字典（名称和值））
    
比如下面的代码：

    >>> class MyShinyClass(object):
    ...     pass
    
可以手动这样创建：

    >>>MyShinyClass = type('MyShinyClass', (), {})
    >>>print MyShinyClass
    <class '__main__.MyShinyClass'>
    >>> print MyShinyClass()  #  创建一个该类的实例
    <__main__.MyShinyClass object at 0x8997cec>
    
你会发现我们使用MyShinyClass作为类名，并且也可以把它当做一个变量来作为类的引用。类和变量是不同的，这里没有任何理由把事情搞复杂。

type接受一个字典来为类定义属性， 因此：

    >>> class Foo(object):
    ...     bar = True
    
可以翻译为：

    >>>Foo = type('Foo', (), {'bar':True})

并且可以将Foo当成一个普通的类一样使用：

    >>> print Foo
    <class '__main__.Foo'>
    >>> print Foo.bar
    True
    >>> f = Foo()
    >>> print f
    <__main__.Foo object at 0x8a9b84c>
    >>> print f.bar
    True
    
当然，你可以向这个类继承，所以，如下代码

    >>> class FooChild(Foo):
    ...    pass
    
就可以写成：

    >>> FooChild = type('FooChild', (Foo,), {})
    >>> print FooChild
    <class '__main__.FooChild'>
    >>> print FooChild.bar   # bar属性是由Foo继承而来
    True
    
最终你会希望为你的类增加方法，只需要定义一个有着恰当签名的函数并将其作为属性赋值就可以了。

    >>> def echo_bar(self): 
    …       print self.bar
    …
    >>> FooChild = type('FooChild', (Foo,), {'echo_bar': echo_bar})
    >>> hasattr(Foo, 'echo_bar')
    False
    >>> hasattr(FooChild, 'echo_bar')
    True
    >>> my_foo = FooChild()
    >>> my_foo.echo_bar()
    True
    
你可以看到，python中，类也是对象，可以动态的创建类。这就是当你使用关键字class时python在幕后做的事情，而这就是通过元类来实现的。

### 到底什么是元类？

元类就是用来创建类的“东西”。你创建类就是为了创建类的实例对象，不是吗？但是我们已经了解到python中的类也是对象。元类就是用来创建类（对象）的，元类就是类的类，可以这样理解：

    MyClas = MetaClass()
    MyObject = MyClass()
    
你可以看到了type可以让你像这样做：

    MyClass = type('MyClass', (), {})
    
这就是因为函数type实际上就是一个元类。type就是Python在背后用来创建所有类的元类。str用来创建字符串对象的类，int是用来创建整数对象的类，type就是创建类对象的类。可以通过检查
__class__属性来看到这一点。Python中所有的东西，注意，我是指所有的东西--都是对象。包括整数、字符串、函数以及类。他们全部都是对象，而且他们都是从一个类创建而来。

    >>> age = 35
    >>> age.__class__
    <type 'int'>
    >>> name = 'bob'
    >>> name.__class__
    <type 'str'>
    >>> def foo(): pass
    >>>foo.__class__
    <type 'function'>
    >>> class Bar(object): pass
    >>> b = Bar()
    >>> b.__class__
    <class '__main__.Bar'>
    
现在，对于任何一个__class__的__class__属性又是什么？

    >>> a.__class__.__class__
    <type 'type'>
    >>> age.__class__.__class__
    <type 'type'>
    >>> foo.__class__.__class__
    <type 'type'>
    >>> b.__class__.__class__
    <type 'type'>
    
因此元类就是创建类这种对象的东西，如果你喜欢的话，可以把元类称作“类工厂”（不要和工厂类搞混就好） type就是Python内建元类，当然，你也可以创建自己的元类。

### __metaclass__属性

你可以在写一个类的时候为其添加__metaclass__属性。

    class Foo(object):
        __metaclass__ = something...
    [..]
    
如果这么做了，python就会用元类来创建类Foo. 这里面有些技巧，首先写下class Foo(object),但是类对象Foo还没有在内存中创建。Python会在类的定义中寻找__metaclass__属性，如果找到了，
python就会用它来创建类Foo,如果没有找到，就会用内建的type来创建这个类。把下面的这段话反复读几次，当你写下如下代码时：

    class Foo(Bar):
        pass
        
Python 做了如下操作：

 Foo中有__metaclass__有这个属性吗？ 如果是，Python会在内存中通过__metaclass__创建一个名字为Foo的类对象（我说的是类对象，不是类实例哈）。如果Python没有找到__metaclass__，它会
 在Bar(父类）中寻找__metaclass__属性，并尝试做和前面同样的操作。如果Python在任何父类中都找不到__metaclass__，它就会在模块层次中寻找__metaclass__,并尝试做和前面同样的操作。如果还是找不到__metaclass__, Python就会用内置的type来创建这个类的对象。
 
 现在的问题是，可以在__metaclass__中放置那些代码呢？答案是：可以创建一个类的东西。那什么可以创建一个类呢？type,或则任何使用到type或子类化type的东西都可以。
 
### 自定义元类

元类的主要目的就是为了当创建类时能够自动的改变类。通常，你会为API做这样的事情，你希望可以创建符合当前上下文的类。假想一个很傻的例子，你决定在你的模块里所有的类的属性都应该是大写形式。有好几种方法可以办到，但其中一种就是通过在模块级别设定__metaclass__。采用这种方法，这个模块中的所有类都会通过这个元类来创建，我们只需要告诉元类把所有的属性都改成大写形式即可。

幸运的是，__metaclass__实际上可以被任意调用，它并不是一个正式的类。所以，我们这里先以一个简单的函数作为例子开始。

    # 元类会自动将你通常传给“type"的参数作为自己的参数传入
    def upper_attr(future_class_name, future_class_parents, future__class_attr)
        '''返回一个类对象，将属性都转为大写形式‘’‘
        #  选择所有不以“__”开头的属性
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))

下一篇[python metaclass(下)](https://king32783784.github.io/2017/01/15/python/)

<img src="https://d2lm6fxwu08ot6.cloudfront.net/img-thumbs/280h/WBB0EXYSWE.jpg" height="320" width="540">
