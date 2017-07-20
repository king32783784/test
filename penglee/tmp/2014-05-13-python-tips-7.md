Title: Python-Tips(七）
Date:2014-05-1３
Author:李鹏
Slug:python 
Tags:Python-Tips
category:编程语言-Python

### Tips 22

**文件操作**

读取文件之前，需要打开，打开文件比较简单：

 a_file = open('roman2.py', encoding='utf-8')

"roman2.py"打开文件的文件名＋路径名　encoding 指定编码规则，如果想查看当前编码信息，可以导入local模块通过locale.getpreferredencoding()查看
open函数返回一个流对象(stream　object)支持下面的方法：

    >>> a_file.name
    'roman2.py'
    >>> a_file.encoding
    'utf-8'
    >>> a_file.mode
    'r'
    >>> a_file.read() # 返回的结果是文件的一个字符串表示
    >>> a_file.read() # 再次读取不会返回一个异常，但返回为空
    ''
    >>> a_file.read() # 依旧在文末所以为空
    ''
    >>> a_file.seek(0) # seek()方法定位到文件中特定字节
    0
    >>> a_file.read(16) #read()方法支持字符个数的参数
    '#*-*coding=utf-8'
    >>> a_file.read(1)
    '*'
    >>> a_file.read(1)
    '-'
    >>> a_file.tell()　# 当前在18字符处　
    18
read()和seek()方法是以字节的方式记数。

    >>> a_file.close()
    >>> a_fiel.read() # 试图读取关闭的文件会引发IOError异常
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    NameError: name 'a_fiel' is not defined
    >>> a_file.close()
    >>> a_file.closed　# closed用来确认文件是否关闭
    True

**自动关闭文件**

try..finally可以，但with更好。

    with open('roman2.py', encoding='utf-8') as a_file:
        a_file.seek(17)
        a_character = a_file.read(1)
        print(a_character)

这里没有使用cloase()方法，但with块结束时，会自动调用a_file.close(),即时程序突然中止，也会保证文件被关闭。
从实现上说，with语句创建了一个运行时环境(runtime context)。在几个样例中，流对象的行为就是一个上下文管理器。当with结束时，python告诉流对象正在退出这个运行时环境，然后环境对象就会调用它的close()方法。

with语句不是针对文件而言的，它是用来创建运行时环境的通用框架，告诉对象它们正在进入和离开一个运行时环境。如果该对象是流对象，那么它就会做一些类似文件对象一样有用的动作。但是那个行为是被流对象自身定义的，不是with决定的。还有很多跟文件无关的使用上线文管理器的方法。

**一次读取一行数据**

    line_number = 0
    with open('roman2.py') as a_file:  # 使用for循环一次读取一行(a_line),流对象也是一个迭代器
        for a_line in a_file:
            line_number += 1
            print('{:>4} {}'.format(line_number, a_line.rstrip())) # 使用字符串的format方法，可以打印出行号和行内容，{:>4}"使用最多４个空格使之右对齐,字符串方法rstrip()可以去掉尾随的空白符


**写入文本文件**

使用open()函数，指定写入模式，存在两种模式用于写入：

* "写"模式会重写文件, mode='w'
* “追加”模式会在文件末尾追写数据，mode='a'

如果打开文件不存在，两种模式都会自动创建文件。
完成写入后应该马上关闭文件，释放文件句柄，并且保证数据被完整的写入到了磁盘。跟读文件类似，可以调用close(),或则使用with块。
    >>> with open('test.log', mode='w', encoding='utf-8') as a_file: # 覆盖写，之前的数据没有了
    ...     a_file.write('test successed')
    ... 
    14
    >>> with open('test.log', encoding='utf-8') as a_file:
    ...     print(a_file.read())
    ... 
    test successed
    >>> with open('test.log', mode='a', encoding='utf-8') as a_file: # 追加写
    ...     a_file.write('and again')
    ... 
    9
    >>> with open('test.log', encoding='utf-8') as a_file:
    ...     print(a_file.read())
    ... 
    test successedand again

**字符编码**
打开写入时加了encoding参数，这个参数非常重要，文件中并不存在字符串，他们都是字节，当年你指定编码方式时，从文件读取字符串才可能。
不是所有的文件都包含文本内容，还可以存放二进制。打开二进制时需要加入参数'b'，二进制流对象没有encoding属性。

**非文件来源的流对象**
使用read()方法即可从虚拟文件读取数据。
比如一个库，其中一个库函数从文件读取数据，它使用文件名为参数，以只读的方式打开文件，读取数据，关闭文件，返回。

    >>> a_string = 'PapayaWhip is the new black.' # 字符串
    >>> import io
    >>> a_file = io.StringIO(a_string)　# io模块定义了StringIO类，可以把内存中字符串作为文件处理
    >>> a_file.read()
    'PapayaWhip is the new black.'
    >>> a_file.read()
    ''
    >>> a_file.seek(0)
    0
    >>> a_file.seek(10)
    10
    >>> a_file.seek(0)
    0
    >>> a_file.read(10)
    'PapayaWhip'
    >>> a_file.tell()
    10
    >>> a_file.seek(18)
    18
    >>> a_file.read()
    'new black.'
io.StringIO可以将一个字符串作为文件处理，io.ByteIO可以把字节数组当成二进制文件处理。

**压缩文件**

python标准库中包含支持读写压缩文件的模块，其中gzip和bzip2是非windows下最流行的压缩方式。
gzip模块允许你创建用来读写gzip压缩文件的流对象，该流对象支持read()方法或则write()方法。也就是可以用普通文件的方式来操作gzip压缩文件，它同样支持with语句。

    >>> import gzip
    >>> with gzip.open('out.log.gz', mode='wb') as z_file: # mode参数里面有b
    ...     z_file.write('A nine mile walk is no joke, especially in the rain.'.encode('utf-8'))
    ... 
    52
    >>> exit()
退出之后，通过ls，可以看到压缩文件。

**标准输入、输出和错误**

sys.stdin, sys.stdout, sys.stderr

数据流应用时，多次提到。标准输出和标准错误输出，是类UNIX系统中的两个管道(pipe)。当你调用print()的时候，需要打印的内容被发送的stdout管道，当程序出错并需要打印跟踪信息时，被发送到sys.stderr管道。默认情况下，两个管道都链接到终端。
sys.stdout和sys.stderr都是流对象，但他们都只支持写入，试图调用read()会引发IOError。

**标准输出重定向**

sys.stdout和sys.stderr是变量不是常量，可以利用其他任意流对象进行重定向他们的输出。

    import sys
     
    class RedirectStdoutTo:
        def __init__(self, out_new):
            self.out_new = out_new # 传入一个参数(上下文环境的生命周期内用作标准输出的流对象
     
        def __enter__(self): # 进入上下文环境时会调用该方法（即with开始时)
            self.out_old = sys.stdout # 把当前的sys.stdout值保存到self.out_old
            sys.stdout = self.out_new　# 通过self.out_new赋给sys.stdout来重定向标准输出
        # 先保存当前的标准输出，然后将标准输出定向到为传入的流对象(out.log)  
   
        def __exit__(self, *args): # 离开上下文是调用（with语句末尾)
            sys.stdout = self.out_old # 把保存的self.out_old的值赋给sys.stdout恢复标准输出
        # 恢复标准输出为标准输出（终端输出）
     
    print('A')　# 输出到终端
    with open('out.log', mode='w', encoding='utf-8') as a_file: # 打开一个文件out.log
        with RedirectStdoutTo(a_file): #  怎么没有as,就像调用函数忽略返回值，with语句的上下文环境同样可以忽略
            print('B')　# 这个print()函数在with语句上下文环境执行，不会输出，会写入文件
    print('C')

with语句块结束了，python告诉每一个上下文管理器完成他们应该离开上下文环境时该做的事。这些上下文环境形成一个后进先出的栈。当一个上下文环境离开时，第二个上下文环境将sys.stdout的值恢复到原来的状态，然后第一个上下文环境关闭out.log文件。由于标准输出已经被恢复，所以再调用print()函数会输出到终端上。
　
 RedirectsStdoutTo上下文环境的side effect,该类是用户自定义的上下文管理器。任何类只要定义了__enter__()和__exit__()就可以变成上下文管理器。





