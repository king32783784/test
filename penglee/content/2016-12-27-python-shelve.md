Title: python shelve
Date:2016-12-27
Author:李鹏
Slug:编程语言-Python 
Tags:Python
category:编程语言-Python


本文对shelve模块进行说明。

shelve模块实现了对任意可被pickle的python对象进行持久存储，并提供了类字典的API使用。

 <img src="https://d2lm6fxwu08ot6.cloudfront.net/img-thumbs/280h/4C0XUNHJ7C.jpg" height="280" width="420">

### 简介

当使用关系数据库太重时，shelve模块可以为python对象提供了一个简单的持久的存储选择。它就像字典一样，通过关键字访问shelf对象，其值经过pickle,写入anydbm创建和管理的数据库。在使用时，可以自己定义一些存储结构使其存储较复杂的数据。

### 创建shelf对象

最简单的使用shelve模块的方式是通过DbfilenameShelf类。使用函数shelve.open()(使用的是anydbm）来存储数据。可以使用类或简单的调用：

    import shelve
    
    s = shelve.open('test_shelf.db')  # 创建test_shelf.db文件进行存储
    try:
        s['key1'] = {'int':10, 'float':9.5, 'string': 'Sample Data'}　#　写入key1，值可以是python支持的对象，看起来和字典的用法一样
    finally:
        s.close()
        
访问已存储的数据，打开shelf,可以像字典一样进行使用。

    s = shelve.open('test_shelf.db')  # 打开已存在的数据文件
    try:
        existing = s['key1'] # 获取之前存储的key1
    finally:
        s.close()
    
    print(existing)  # 打印s['key1'],会得到刚才存储的数据
    
执行结果：

    $ python shelve_create.py
    $ python shelve_existing.py
    {'int': 10, 'float': 9.5, 'string': 'Sample data'}
    
dbm模块不支持多个应用同时写入同一数据库，如果客户端或程序不会修改shelf,请指定shelve以只读方式打开数据库。

    s = shelve.open('test_shelf.db', flag='r')   # 打开时指定flag＝‘r'，只读模式打开
    try:
        existing =  s['key1']
    finally:
        s.close()
        
    print existing
    
当数据库以只读模式打开，但又试图更改数据库时，会引起一个访问出错异常。这一异常类型依赖于在创建数据库时被anydbm选择的数据库模块。

### 写回

默认情况下，Shelves不去追踪可变对象的修改。意思就是，如果你改变了已存储在shelf中的一个项目的内容，就必须重新存储该项目来更新shelf.

    s = shelve.open('test_shelf.db')
    try:
        print s['key1']
        s['key']['new_value'] = 'this is not here before'
    finally:
        s.close()

    s = shelve.open('test_shelf.db', writeback = True) # 设置写回或同步
    try:
       print s['key1']
    finally:
        s.close()
        
在这个例子中，没有对字典的关键字key1的内容进行存储，虽然打开时设置了writeback,因此重新打开shelf时，key1内容没有改变。

    $ python shelve_create.py
    $ python shelve_withoutwriteback.py
    {'int': 10, 'float': 9.5, 'string': 'Sample data'}
    {'int': 10, 'float': 9.5, 'string': 'Sample data'}

为了自动捕捉存储在shelf中的可变对象所发生的改变，需改变前设置writeback可用.writeback标志导致shelf使用一缓存来记住从数据库中调出的所有对象。当shelf关闭的时候，每一个缓存中的对象也重新写回数据库。

    s = shelve.open('test_shelf.db', writeback=True)
    try:
        print(s['key1'])
        s['key1']['new_value'] = 'this was not here before'
        print(s['key1'])
    finally;
        s.close()
        
    s = shelve.open('test_shelf.db', writeback=True)
    try:
        print(s['key1'])
    finally:
        s.close()
        
执行结果：

    $ python shelve_create.py
    $ python shelve_writeback.py
    {'int': 10, 'float': 9.5, 'string': 'Sample data'}
    {'int': 10, 'new_value': 'this was not here before', 'float': 9.5, 'string': 'Sample data'}
    {'int': 10, 'new_value': 'this was not here before', 'float': 9.5, 'string': 'Sample data'}
    
虽然使用writeback模式可用减少出错几率，也能更加透明化对象的持久性。但是，不是每种情况都要使用writeback模式。原因看到前面的示例，应该能猜到。当shelf打开时，缓存就要占用额外的内存。
并且，当shelf关闭时，同样会对缓存中的对象再次写回数据库，增加了开销。即使没有进行改变，仍然会进行数据写回。比较好的方式是，确认需要写入数据时，再设置writeback,读数据时设置只读或默认即可。

### 指定shelf类型

上面的例子全部使用默认的shelf实现。使用shelve.open()直接代替一种shelf实现，是常见用法, 尤其是在不关心用哪种数据库存储数据的时候. 然而, 有时常会关心它. 如果是在这种情况下, 通常就会直接使用DbfilenameShelf或者BsdDbShelf, 更或者是通过Shelf的子类来解决问题.
