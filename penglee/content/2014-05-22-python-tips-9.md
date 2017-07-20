Title: Python-Tips(八)
Date:2014-05-22
Author:李鹏
Slug:python 
Tags:Python-Tips
category:编程语言-Python

### Tips 24

**序列化对象**

#### pickle

序列化的概念很简单，内存里面的数据，想保存下来。下次使用时，又能容易恢复，而且不想使用大型的数据库。这种情况下，pickle模块是理想的，它是python标准库的一部分，所以总是可用的。它的大部分和python解释器本身一样是用C编写的，可用存储任意复杂的python数据结构。

* python支持的原生类型:布尔，整数，浮点数，复数，字符串，字符数组，None
* 列表，元组，字典和集合
* 列表，元组，字典和集合嵌套列表，元组，字典和集合（直到python支持最大的递归层数）
* 函数，类，和类的实例

**保存数据到文件**

    >>> entry
    {'article_link': 'http://diveintomark.org/archives/2009/03/27/dive-into-history-2009-edition', 'published': True, 'published_date': time.struct_time(tm_year=2009, tm_mon=3, tm_mday=27, tm_hour=22, tm_min=20, tm_sec=42, tm_wday=4, tm_yday=86, tm_isdst=-1), 'internal_id': b'\xde\xd5\xb4\xf8', 'tags': ('diveintopython', 'docbook', 'html'), 'comments_link': None, 'title': 'Dive into history, 2009 edition'}

定义了一个包含多个数据格式的字典

保存数据

    >>> import pickle
    >>> with open('entry.pickle', 'wb') as f: # open打开一个文件，文件模式'wb'
    ...     pickle.dump(entry, f)  # pickle模块的dump()函数接收一个可序列化的python数据结构。使用pickle协议将其序列化为二进制，保存到entry.pickle 
pickle协议是python特定的。该协议也在修改变化，最新的协议是二进制格式的，所以使用时注意其版本变化

读取数据

    >>> with open('entry.pickle', 'rb') as f: # with语句，二进制模式打开entry.pickle文件
    ...     entrya = pickle.load(f)   # pickle.load()函数接收一个流对象，从文件读取序列化后的数据，创建一个新的python对象
    ... 
    >>> entrya # 和前面的entry内容一样
    {'published_date': time.struct_time(tm_year=2009, tm_mon=3, tm_mday=27, tm_hour=22, tm_min=20, tm_sec=42, tm_wday=4, tm_yday=86, tm_isdst=-1), 'comments_link': None, 'title': 'Dive into history, 2009 edition', 'article_link': 'http://diveintomark.org/archives/2009/03/27/dive-into-history-2009-edition', 'internal_id': b'\xde\xd5\xb4\xf8', 'published': True, 'tags': ('diveintopython', 'docbook', 'html')}

pickle.dump()/pickle.load()循环的结果是一个和原始数据结构等同的新的数据结构

    >>> with open('entry.pickle', 'rb') as f:
    ...     entryb = pickle.load(f)
    ... 
    >>> entryb == entry # 另外读取的entryb和之前的entry相等
    True 
    >>> entryb is entry # 虽然相等，但不是一个
    False

**保存到内存**

    >>> b = pickle.dumps(entry) # 这里是dumps
    >>> type(b)   # 保存的是二进制数据格式
    <class 'bytes'>
    >>> entry3 = pickle.loads(b) # 接收包含序列化后的数据bytes对象
    >>> entry3 == entry
    True

**pickle**文件调试

    >>> import pickletools
    >>> with open('entry.pickle', 'rb') as f:
    ...     pickletools.dis(f)
    ... 
        0: \x80 PROTO      3
    ...
    highest protocol among opcodes = 3  # 显示了pickle协议的版本号

#### JSON

pickle序列化数据是python特定的，但json是可以跨语言使用的。

json是基于文本的，不是二进制。json值是大小写敏感的。由于是文本格式的，存在空白的问题。json允许在值之间有任意数目的空白（空格，跳格，回车，换行）。空白是无关紧要的，可以根据需要添加任意的空白。python的josn模块在编码时支持pretty-printing选项
json同样要注意编码格式

**保存数据**

json看起来想在javascript手工定义的数据结构。支持js中eval()函数来解码json序列化的数据。

    >>> basic_entry
    {'tags': ('diveintopython', 'docbook', 'html'), 'id': 256, 'comments_link': None, 'published': True, 'title': 'Dive into history, 2009 edition'}
    >>> import json
    >>> with open('basic.json', mode='w', encoding='utf-8') as f: # json是文本格式，所以w打开即可
    ...     json.dump(basic_entry, f) # 同pickle一样，json定义了dump()函数，接收一个流对象和一个可写的流对象。然后写入
    ...

json是文本格式，所以可是用cat查看一下其内容

    >>> with open('basic-pretty.json', mode='w', encoding='utf-8') as f:
    ...     json.dump(basic_entry, f, indent=2) # indent参数指定空格数量进行缩进嵌套保存数据

**读取数据**

类似pickle模块，json模块有一个load()函数接受一个流对象，从中读取JSON编码过的数据，并且创建该JSON数据结构的python对象的镜像

    >>> with open('basic.json', 'r', encoding='utf-8') as f:
    ...     entry = json.load(f)
    ... 
    >>> entry
    {'tags': ['diveintopython', 'docbook', 'html'], 'id': 256, 'comments_link': None, 'published': True, 'title': 'Dive into history, 2009 edition'}
    
Python中还有其他一些序列化对象的如dbm、shelve等等


