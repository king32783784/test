Title:  python数据存储
Date:2016-12-24
Author:李鹏
Slug: python
Tags:Python
category:编程语言-Python

### 存储方式

Python的数据存储主要是以下六类：普通文件、DBM文件、Pickled对象存储、shelve对象存储、对象数据库存储、关系数据库存储。

#### DBM文件

普通文件不解释了，DBM就是把字符串的键值对存储在文件里：

Python代码

    >>> import anydbm                             
    >>> file = anydbm.open('movie', 'c')        # make a DBM file called 'movie' 
    >>> file['Batman'] = 'Pow!'                 # store a string under key 'Batman' 
    >>> file.keys( )                                 # get the file's key directory  

    ['Batman']  

    >>> file['Batman']                          # fetch value for key 'Batman' 

    'Pow!'

#### Pickled对象存储

Pickled就是把对象序列化到文件，可以存储复杂类型：

    >>> table = {'a': [1, 2, 3],  
             'b': ['spam', 'eggs'],  
             'c': {'name':'bob'}}  
    >>>  
    >>> import pickle  
    >>> mydb  = open('dbase', 'w')  
    >>> pickle.dump(table, mydb)
    
下面是反序列化：

    >>> import pickle  
    >>> mydb  = open('dbase', 'r')  
    >>> table = pickle.load(mydb)  
    >>> table  

    {'b': ['spam', 'eggs'], 'a': [1, 2, 3], 'c': {'name': 'bob'}}

#### shelve存储

shelve存储差不多就是DBM和Pickled方式的结合，以键值对的形式把对象序列化到文件：

数据存储：

    >>> import shelve  
    >>> dbase = shelve.open("mydbase")  
    >>> object1 = ['The', 'bright', ('side', 'of'), ['life']]  
    >>> object2 = {'name': 'Brian', 'age': 33, 'motto': object1}  
    >>> dbase['brian']  = object2  
    >>> dbase['knight'] = {'name': 'Knight', 'motto': 'Ni!'}  
    >>> dbase.close( )

取数据：

    >>> import shelve  
    >>> dbase = shelve.open("mydbase")  
    >>> len(dbase)                             # entries  
        2 
 
    >>> dbase.keys( )                          # index  
        ['knight', 'brian']  
 
    >>> dbase['knight']                        # fetch  
        {'motto': 'Ni!', 'name': 'Knight'}
        
对象数据库的存储没怎么了解，因为不习惯用它存储数据。感觉应该和shelve差不多吧，只是把数据保存到了数据库里（其实还是一个文件嘛），然后增加了些事务之类的高级功能。

Python中关系数据库的存储是重点，操作关系数据库最“简单”的就是直接用DB-API，就像Java里的JDBC；当然，数据结构复杂了、设计要求高了，就得找些ORM框架偷懒了，主要有独立的SQLAlchemy，Django的自带ORM等。

 <img src="https://d2lm6fxwu08ot6.cloudfront.net/img-thumbs/280h/8N5QJCOLP7.jpg" height="280" width="420">

### 简单比较Python的数据操作

Python中操作关系数据库最直接的就是用DB-API了，流程一般是：连接、执行SQL语句、提交、断开。以MySQL为例，下面是各步骤的代码示例：

首先是连接：

    >>> import MySQLdb  
    >>> conn = MySQLdb.connect(host='localhost', user='root', passwd='python')

接着便可以执行语句了，但在执行SQL语句前要先获取指针：

    >>> curs = conn.cursor( )  
    >>> curs.execute('create database peopledb')  
    1L  
    >>> curs.execute('use peopledb')  
    0L  
    >>> tblcmd = 'create table people (name char(30), job char(10), pay int(4))' 
    >>> curs.execute(tblcmd)  
    0L
    
添加数据：

    >>> curs.execute('insert people values (%s, %s, %s)', ('Bob', 'dev', 5000))  
    1L  
    >>> curs.executemany('insert people values (%s, %s, %s)',  
    ...          [ ('Sue', 'mus', '70000'),  
    ...            ('Ann', 'mus', '60000')])  
    2L  
    >>> conn.commit( )
    
执行查询：

    >>> curs.execute('select * from people')  
    6L  
    >>> curs.fetchall( )  
    (('Bob', 'dev', 5000L), ('Sue', 'mus', 70000L), ('Ann', 'mus', 60000L), ('Tom',  
    'mgr', 100000L))

执行完数据库操作记得断开连接：

    conn.close( )        # close, _ _del_ _ call rollback if changes not committed yet

如果数据结构不是很复杂，配合Python强大的列表解析能力，不用ORM框架也是很方便的；或者自己封装对象映射也不是很难。

如果使用了Django框架，可以使用它自带的ORM工具来操作数据库。首先当然是编写实体类（或者叫模型）了：

    from django.db import models  
 
    class Musician(models.Model):  
        first_name = models.CharField(max_length=50)  
        last_name = models.CharField(max_length=50)  
        instrument = models.CharField(max_length=100)  
 
    class Album(models.Model):  
        artist = models.ForeignKey(Musician)  
        name = models.CharField(max_length=100)  
        release_date = models.DateField()  
        num_stars = models.IntegerField()

Python的代码已经很清楚了，类对应表，成员变量对应表的列，列属性由models.XXXField(…)定义。如果实体类没有显式定义主键，Django会默认加上一句：

    id = models.AutoField(primary_key=True)

Django里可以这样定义枚举型数据：

    class Person(models.Model):  
        GENDER_CHOICES = (  
            (u'M', u'Male'),  
            (u'F', u'Female'),  
        )  
        name = models.CharField(max_length=60)  
        gender = models.CharField(max_length=2, choices=GENDER_CHOICES)

对于关联关系，在做列的映射定义时可以这么写：

    poll = models.ForeignKey(Poll)  
    sites = models.ManyToManyField(Site)  
    place = models.OneToOneField(Place")

在Django里定义关联关系还有更多功能，后面的文件再介绍。

Django的Model基类中已经定义了基本的数据库操作，因为所有的实体类都是继承自Model类，所以也就有了这些操作。例如新建并保存一个person只需要这么做：

    >>> p = Person(name="Fred Flinstone", gender="M")  
    >>> p.save()

Django会通过查询对象的主键是否存在来决定该UPDATE还是INSERT，当然你也可以强制框架执行某种操作。如果你不满意框架自带的方法，可以重写它：

    class Blog(models.Model):  
        name = models.CharField(max_length=100)  
        tagline = models.TextField()  
 
        def save(self, *args, **kwargs):  
            do_something()  
            super(Blog, self).save(*args, **kwargs) # Call the "real" save() method.  
            do_something_else()

发现没，Django里存取数据不需要那种session，最讨厌Hibernate里的session了，总是报“Session Closed”错误……

Python还有一个独立的ORM框架——SQLAlchemy。功能更强大，支持的数据库也比Django自带的ORM工具要多。它有两种建立实体类的方法。

一种是分开定义，再将表定义和类定义映射起来。首先是建立表的定义：

    >>> from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey  
    >>> metadata = MetaData()  
    >>> users_table = Table('users', metadata,  
    ...     Column('id', Integer, Sequence('user_id_seq'), primary_key=True),  
    ...     Column('name', String(50)),  
    ...     Column('fullname', String(50)),  
    ...     Column('password', String(12))  
    ... )
    
接着定义实体类：

    >>> class User(object):  
    ...     def __init__(self, name, fullname, password):  
    ...         self.name = name  
    ...         self.fullname = fullname  
    ...         self.password = password

这还没完，还要把他们映射起来：

    >>> from sqlalchemy.orm import mapper  
    >>> mapper(User, users_table)

这样的过程有点像Hibernate里将XML的Map文件和实体类的映射。Hibernate中还可以方便的直接用注释在实体类中完成与表的映射，当然SQLAlchemy也有直接的方法：


    >>> from sqlalchemy.ext.declarative import declarative_base  
 
    >>> Base = declarative_base()  
    >>> class User(Base):  
    ...     __tablename__ = 'users' 
    ...  
    ...     id = Column(Integer, primary_key=True)  
    ...     name = Column(String)  
    ...     fullname = Column(String)  
    ...     password = Column(String)

作为一个独立的ORM框架，实体类的存取当然就不会像Django那样集成的那么完美了，SQLAlchemy里存取数据也是要Session的：

    >>> from sqlalchemy.orm import sessionmaker  
    >>> Session = sessionmaker(bind=engine)
    
这里的engine对象需要这样建立：

    >>> from sqlalchemy import create_engine  
    >>> engine = create_engine('<span style="font-family: monospace; white-space: normal; color: #333333; line-height: 20px;">dialect+driver://user:password@host/dbname[?key=value..]</span>', echo=True)

对于存取操作，如果是保存就这么写：

    >>> ed_user = User('ed', 'Ed Jones', 'edspassword')  
    >>> session.add(ed_user)

如果要查询，就是类似的这种形式：

    >>> our_user = session.query(User).filter_by(name='ed').first()
    执行完一些数据操作，必要的时候要提交或是回滚：
    >>> session.rollback()  
    或者  
    >>> session.commit()

SQLAlchemy框架还有一个衍生产品——Elixir，在SQLAlchemy的基础上对其映射方式做了些封装，使得实体类的定义有点类似Django中的定义方式。

话说Django的ORM与它的其他模块结合的很紧密，不好单独使用；SQLAlchemy虽然强大，但风格不太喜欢，所以下一步打算深入两个ORM框架的代码，看看他们是怎么实现的。一方面好抉择用哪一个，另外也可以看看在自己的应用中能否自己做一个简单的ORM。
