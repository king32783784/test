Title:  Python-tips01
Date:2016-01-01
Author:李鹏
Slug: effective-python
Tags:python
category:编程语言-Python

### 确认python版本

* 目前两个版本活跃状态，python2和python3
* python有很多流行的运行环境，如cpython jython ironpython以及  pypy
* 运行Python时，确保python是想用的版本
* 以后项目尽量使用python3

### PEP8风格
* 编写python代码时，应该遵循PEP8风格指南
* 采用通用的代码风格，便于多人协作
* 一致的代码风格易于维护

### bytes、str与Unicode的区别

* Python3中，bytes是一种包含8位值的序列，str是一种包含Unicode字符的序列。开发时不能以>或+等操作符来混同操作bytes和str实例。
* Python2中，str是一种包含8位值的序列，Unicode是一种包含Unicode字符的序列。如果 str只包含7位ASCII字符，可以通过想过操作符同时操作str和Unicode。
* 对于输入的数据进行操作之前，使用辅助函数来保证字符序列的类型与开发者的期望相符。
* 从文件中读取二进制数据或向其中写入二进制数据时，总应该以'rb'或'wb'等二进制模式来开启文件。

编写Python程序的时候，一定要把编码和解码操作放在解码最外围做。程序的核心部分分别使用Unicode字符类型（Python3中str，Python2中的unicode),而且不要对字符编码做任何假设。
由于字符类型有别，所以Python代码经常会出现两种常见的使用情景：
* 开发者需要原始8位值，这些8位值表示UTF-8格式来编码字符
* 开发者需要操作没有特定编码形式的Unicode字符。

编写两个helper函数以便在这种情况之间转换，使得转换后的输入数据符合预期。
python3中，需要编写接受str或bytes,并总是返回 str 的方法：

    def to_str(bytes_or_str):
        if isinstance(bytes_or_str, bytes):
            value = bytes_or_str.decode('utf-8')
        else:
            value = bytes_or_str
        retunr value 
另外，需要编写接受str或bytes,总是返回bytes：

    def to_bytes(bytes_or_str):
        if isinstance(bytes_or_str, str):
            value = bytes_or_str.encode('utf-8')
        else:
            value = bytes_or_str
        return value

Python2,需要编写接受str或Unicode，总是返回Unicode的方法：

    #python2
    def to_unicode(unicode_or_str):
        if isinstance(unicode_or_str, str):
            value = unicode_or_str.decode('utf-8')
        else:
            value = unicode_or_str
        return value

编写接受str或Unicode，总是返回str的方法

    def to_str(unicode_or_str):
        if isinstance(unicode_or_str, unicode):
            value = unicode_or_str.encode('unf-8')
        else:
            value = unicode_or_str
        return value

python使用8位值与Unicode字符时，需要注意以下问题：
python2中，如果str只包含7位ASCII，Unicode和str实例成了同一种类型。
可以用+操作符把这种str和Unicode连接
可以用等价与不等价操作符，
格式化字符串中，可以用“%”形式代表Unicode。

Python3中，如果通过内置的open函数获取了文件句柄，该句柄默认会采用UTF-8编码格式操作文件。而Python2中，文件默认编码格式为二进制格式。可能或出现问题。
例如，向文件中写入一些二进制数据。下面这种方法在Python2中可以正常运行，Python3不行

   with open（'/tmp/random.bin', 'w') as f:
       f.write(os.urandom(10))

   >>>TypeError: must be str, not bytes

Python3给open函数添加了名为encoding的新参数，而这个新参数的默认值却是"utf-8"。这样在文件句柄上进行read和write操作时，系统要求开发者必须传入包含Unicode字符的str实例，而不接受包含二进制的bytes实例。
为了解决这个问题，我们必须用二进制写入模式（'wb')来开启操作的文件。以下方式同时适用Python2和Python3:
    
    with open('/tmp/random.bin', 'wb') as f:
        f.write(os.urandom(10))


