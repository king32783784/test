Title:  sqlite3 - SQLite数据库DB-API 2.0接口
Date:2016-12-25
Author:李鹏
Slug: python
Tags:Python
category:编程语言-Python

### 简介

SQLite 是一个Ｃ库，它提供了一个轻量级的基于磁盘的数据库，不需要一个单独的服务进程。允许使用非标准的SQL查询语言的变体访问数据库。
一些应用程序可以使用SQLite进行存储内部数据。也可以使用SQLite建立应用原型，随后再将数据或代码移植到大型的数据库，比如PostgreSQL或Ｏracle.

sqlite3模块由Gerhard Haring编写，提供了一个sql接口，该接口和[PEP 249](https://www.python.org/dev/peps/pep-0249/)描述的DB-API 2.0规范兼容。

若要使用该模块，必须首先创建一个表示数据库的连接/connection对象。例如这边的例子，将数据存储到example.db文件：

    import sqlite3
    conn = sqlite3.connect('example.db')
    
还可以使用特殊名称:memory:在RAM(内存）中创建数据库。

一旦有了一个连接／connection,就可以创建cursor/游标对象并调用其execute()方法来执行SQL命令：

    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE stocks
                 (data text, trans text, symbol text, qty real, price real)''')
                 
    # Insert a row of data
    c.execute("INSERT INTO stocks VALUES('2006-01-05', 'BUY', 'RHAT', 100, 35.15)")
    
    # Save(commit) the changes
    conn.commit()
    
    # We can also close the connection if we　are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    
保存过的数据是持久的并在以后的会话中可用：

    import sqlite3
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    
通常的SQL操作需要使用Python变量中的值。不应该使用Python的字符串操作来组装查询，因为这样是不安全的。容易受到SQL注入攻击。

相反，应该使用DB API参数替代。对于你想使用的值，用？作为一个占位符，给游标的execute()方法的第二个参数提供一个值的元组。其他的数据库模块可能使用不同的占位符，如％s或:1。例如：

    # Never do this -- insecure!
    symbol = 'RHAT'
    c.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)
    
    # Do this instead
    t = ('RHAT')
    c.execute("SELECT * FROM stocks WHERE symbol = ?', t)
    print c.fetchone()
    
    # Larger example that inserts many records at a time
    purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                 ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                 ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
                 ]
    c.executemany('INSERT INTO stocks VALUES(?,?,?,?,?)', purchases)
    
为了取回select语句的执行结果，可以把游标cursor当做一个迭代器，通过调用游标的fetchone()方法来获取单行结果；或者通过调用fetchall()方法获取结果集列表。

例如：

    >>> for row in c.execute('SELECT * FROM stocks ORDER BY price'):
            print row
    (u'2006-01-05', u'BUY', u'RHAT', 100, 35.14)
    (u'2006-03-28', u'BUY', u'IBM', 1000, 45.0)
    (u'2006-04-06', u'SELL', u'IBM', 500, 53.0)
    (u'2006-04-05', u'BUY', u'MSFT', 1000, 72.0)

参考资料

[https://github.com/ghaering/pysqlite](https://github.com/ghaering/pysqlite)

The pysqlite web page – sqlite3 is developed externally under the name “pysqlite”.

[http://www.sqlite.org/](http://www.sqlite.org/)
The SQLite web page; the documentation describes the syntax and the available data types for the supported SQL dialect.

[http://www.w3schools.com/sql/](http://www.w3schools.com/sql/)
Tutorial, reference and examples for learning SQL syntax.


### 相关模块函数和常量

**sqlite3.version**

该模块的字符串形式的版本号，不是SQLite库的版本

**sqlite3.version\_info**

该模块的整数元组形式的版本号，不是SQLite库的版本

**sqlite3.sqlite\_version**

SQLite库的版本号，字符串形式

**sqlite3.sqlite\_version_info**

SQLite库的版本号，整数元组形式。

**sqlite3.PARSE\_DECLTYPES**
    
该常量用于connect()函数的detect_typed参数

设置它使得sqlite3模块解析每个返回列的声明的类型。它将解析出声明的类型的第一个单词，比如，　“inter primary key", 它将解析出"integer", 而"number(10)",将解析出”number"。然而对应那列，它将查询转换器字典并对类型使用对应注册的转换器函数。

**sqlite3.PARSE\_COLNAMES**

该常量用于connect()函数的detect_typed参数

设置它使得SQLite接口解析每个返回列的列名。它将查找[mytype]形式的字符串，然后决定'mytype'是列的类型。将会尝试在转换器字典中找到对应于“mytype"的转换器，然后将转换器函数应用于返回的值。Cursor.description中找到的列名只是列名的第一个单词，即，如果SQL中有类似 <t3><t4>'as</t4> <t5>"x</t5> <t6>[datetime]"'</t6></t3>的内容，那么第一个单词将会解析成列名，知道有空格为止，列名只是简单的"x".

**sqlite3.connect(database[,timeout, detect_types, isolation_level,check_same_thread, factory, cached_statements])**

打开到SQLite数据库文件database的连接。可以使用:memory: 打开内存的数据库连接。

当多个连接访问数据库，其中一个进程修改了数据库，SQLite数据库会锁定，直到事务被提交。timeout参数指明为了得到锁，连接最多等待的时间，如果超时会抛出异常。超时参数默认为5s.

对于isolation_level参数，请参阅connection对象的Connection.isolation_level属性。

SQLite原生只支持文本、整数、实数、BLOB和NULL类型。如果想使用其他类型，需要自行添加。detect_types参数和使用由register_converter()函数注册的自定义转换器。

detect_types默认为0（即关闭），可以设置为PARSE_DECLTYPES和PARSE_COLNAMES的任意组合用来打开类型检测。

默认情况下，sqlite3模块使用Connection类以调用connect.然而，可以继承Connection类，通过将子类提供给factory参数，使得connect()使用你的子类

SQLite3模块内部使用语句缓存来避免SQL解析开销。如果想要显示设置连接所缓存的语句的数量，可以设置cached_statements参数。在当前实现中的默认设置是缓存100条语句。

**sqlite3.register_converter(typename, callable)**

  注册可调用对象用来将来自数据库的bytestring转换成为自定义的python类型。对数据库所有有typename类型的值调用该可调用的对象。
  
**sqlite3.register_converter(typename, callable)**

注册可调用对象用来将来自数据库的bytestring转换成为自定义的Python类型。对数据库所有有typename类型的值调用该可调用对象。参见connect()函数的detect_types参数以了解类型检测是如何工作的。请注意typename的大小写和查询中类型的名称必须匹配 ！

**sqlite3.register_adapter(type, callable)**

注册可调用对象用来将自定义的 Python 类型type转换为 SQLite 的支持的类型。可调用对象callable接受一个Python值为参数，返回值的类型必须为如下类型之一：int，long，float，str （UTF-8 编码）， unicode 或缓冲。

**sqlite3.complete_statement(sql)**

如果字符串sql包含一个或多个以分号结束的完整的SQL语句则返回True 。它不验证SQL的语法正确性，只是检查没有未关闭的字符串常量以及语句是以分号结束的。

这可以用于生成一个 sqlite shell，如以下示例所示：

**A minimal SQLite shell for experiments**

    import sqlite3

    con = sqlite3.connect(":memory:")
    con.isolation_level = None
    cur = con.cursor()

    buffer = ""

    print "Enter your SQL commands to execute in sqlite3."
    print "Enter a blank line to exit."

    while True:
        line = raw_input()
        if line == "":
            break
        buffer += line
        if sqlite3.complete_statement(buffer):
            try:
                buffer = buffer.strip()
                cur.execute(buffer)

                if buffer.lstrip().upper().startswith("SELECT"):
                    print cur.fetchall()
            except sqlite3.Error as e:
                print "An error occurred:", e.args[0]
            buffer = ""

    con.close()
    
**sqlite3.enable_callback_tracebacks(flag)**

默认情况下你不会在用户定义的函数、 聚合、 转换器、 授权者回调等地方得到回溯对象（调用栈对象）。如果想要调试它们，将flag设置为True调用此函数。之后可以在sys.stderr通过回调得到回溯。使用False来再次禁用该功能。

<未完待续>    




