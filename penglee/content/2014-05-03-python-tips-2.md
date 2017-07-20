Title: Python-Tips(二）
Date:2014-05-03
Author:李鹏
Slug:python 
Tags:Python-Tips
category:编程语言-Python

**Tips11**

* 字典是无序的键值对, {};dict["键"]="值",反之不成立

* 字典中可以任意扩展，但键是唯一的；对字典中的键重新赋值，新值会替代旧值；

* 字典的值可以为任何数据类型。

* 类似列表、集合，len()将返回字典中键的数量

* in 判断指定的键是否在字典中

* 空字典为假，非空为真；None是一个特殊常量，是一个空值。None不等同于0; None为假，not None为真

**Tips12**

* 遍历一个序列时，使用enumerate()函数可以同时得到索引和对应的值。

* 同时遍历两个或更多的序列，使用zip()函数可以成对读取元素.

* 要反向遍历一个序列，首先正向生成这个序列，然后调用 reversed() 函数。 for i in reversed(xrange(1,10,2))

* 要按排序顺序循环一个序列，请使用sorted()函数，返回一个新的排序的列表，同时保留源不变。

    >>> basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
    >>> for f in sorted(set(basket)):
    ...     print f

* 遍历字典时，使用iteritems()方法可以同时得到键和对应的值

**Tips13**

* OS模块包含非常多的函数用于操作系统的api

* os.getcwd()函数获取当前目录。os.chdir()改变当前工作目录　

* os.path模块包含了操作文件名和目录名的函数

* os.path.join()可以用于构造路径，os.path.join("/home", "isoft_lp")；os.path.expanduser()
用来将包含~符号（表示当前用户Home目录）的路径扩展为完整的路径　os.path.expanduser('~')

* split函数分割一个完整路径并返回目录和文件名，os.path.splitext()函数分割一个文件名，返回文件名和扩展名，os.path.splitext("hello.py"),返回"hello"和".py"

* glob模块是获得目录内容的一个模块，可以使用shell风格的通配符；glob模块接收一个通配符并返回匹配的文件和路径。如glob.glob("*.py")

* os.stat()函数返回一个包含多种文件元信息的对象，包括以下信息（posix.stat_result(st_mode=33261, st_ino=2952447, st_dev=2061, st_nlink=1, st_uid=0, st_gid=0, st_size=1911, st_atime=1488354105, st_mtime=1484125146, st_ctime=1484125146)

* time是时间相关的模块，time.localtime()可以将纪元时间转为通用格式时间。

* os.path.realpath()函数可以获得文件的绝对路径

* 列表解析可以过滤列表，生成比原列表短的结果列表如过滤当前目录容量大于1000的文件

    [f for f in glob.glob('*.py') if os.stat(f).st_size > 1000]
    
* 字典解析和列表解析类似，生成字典。例如：

    metadata_dict = {f:os.stat(f) for f in glob.glob('*.py')}
    
* 交换字典的键和值：

    {value:key for key, value in a_dict.items()}
    
* 集合的解析方法和字典类似，不同的地方是结合只有值，没有键值对，例如
　　a = {0,1,2}
　　{x ** 2 for x in a}，集合元素求平方
　　{x for x in a if x % 2 == 0}

**Tips14** 

* unicode编码使用4字节的数字来表达每个字母、符号或文字。

* python３支持把值格式化成字符串。

* splitlines()方法以多行字符串作为输入，返回一个字符串组成的列表，列表的元素即为原来的单行字符串。

* lower（）方法把大写转为小写，upper()小写转换为大写

* count()方法对字符串找那个指定的子串进行计数；split()方法使用一个参数，即指定的分隔符，然后根据分隔符将字符串分割为字符串列表。

* 字符串分片跟列表的分片原理是一样的，可以指定索引值进行分片。

* 字节即字节；字符是一种抽象。一个不可变的unicode编码的字符序列叫做string. 一串０到255之间的数字组成的序列叫bytes对象。

* python2中.py文件默认的编码方式为ASCII, Python3编码默认为utf-8;一般字符编码的重载声明:# -*- coding: utf-8 -*-
    







