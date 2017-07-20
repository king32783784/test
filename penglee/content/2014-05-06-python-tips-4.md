Title: Python-Tips(四）
Date:2014-05-06
Author:李鹏
Slug:python 
Tags:Python-Tips
category:编程语言-Python

## Tips19

### 斐波那契生成器      

每个数字都是前两个数字的和

    def fib(max):
        a, b = 0, 1
        while a < max:
            yield a　　　　# a是当前序列的数字，因此对它进行yield，yield命令的意思是这不是一个普通的函数。它是一次生成一个值的特殊类型函数。可以将其视为可恢复函数。调用该函数将返回一个可用于生成连　　续x值的生成器【Generator】　　
            a,b = b, a+b   # b是序列中下一个数字，因此将它赋值给a，但同时计算下一个值(a+b)并将其赋值给b以供稍后使用
    for n in fib(1000):
        print(n, end=' ')
        
    0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987

### 复数规则生成器　　

英文单词复数形式

    import re
    def build_math_and_appll_function(pattern, search, replace):
        def matches_rule(word):
            return re.search(pattern, word)
        def apply_rule(word):
            return re.sub(search, replace, word)
        return (matches_rule, apply_rule)

    def rules(rules_filename):          # rules()是按照需求连续生成匹配和应用函数的生成器
        with open(rules_filename, encoding='utf-8') as pattern_file:
            for line in pattern_file:
                pattern, search, replace = line.split(None, 3)
                yield
            build_math_and_appll_function(pattern, search, replace)
            
    def plural(noun, rules_filename='plural5-rules.txt'):
        for matches_rule, apply_rule in rules(rules_filename):　# rules是生成器，可直接for循环使用
            if matches_rule(noun):
                return apply_rule(noun)
            raise ValueError('no matching rule for {0}'.format(noun))
            
### 斐波那契迭代器

迭代器就是一个定义了__iter__()方法的类。

    class Fib(object):
        def __init__(self, max):
            self.max = max
            
        def __iter__(self): # 调用iter(fib)时，__iter__()就会被调用
            self.a = 0
            self.b = 1
            return self
            
        def __next__(self):　# 当有人在迭代器实例中调用next()方法时，__next__()会自动调用
            fib = self.a
            if fib > self.max:
                raise StopIteration　# 给调用者发送迭代用完的信号
            self.a, self.b = self.b, self.a + self.b
            return fib
            
    for n in Fib(1000):
        print (n, end=' ')
  
for 循环调用iter(fib_inst),它返回迭代器，叫fib_iter.在这，fib_inst== fib_inst,因为__iter__()方法返回self.for 循环调用next(fib_iter),调用fib_iter对象的__next__()方法，产生下一个计算并返回值。当抛出StopIteration时，for循环将接收该异常并退出。

### 复数规则迭代器器

    iter(f) 调用f.__iter__
    next(f) 调用f.__next__

    class LazyRules:
        rules_filename = 'plural6-rules.txt'
        def __init__(self):
            self.pattern_file = open(self.rules_filename, encoding='utf-8') # 实例化LazyRules时，打开文件
            self.cache = []　　　＃　打开文件之后，初始化缓存
        
        def __iter__(self):　　　　# 调用iter(rules)时，__iter__方法会自动调用
            self.cache_index = 0
            return self　　　　　　# 每个__iter__方法都需要返回一个迭代器，返回self
            
        def __next__(self):　　　　# 调用__next__方法，next(rules)会跟着被调用
            self.cache_index += 1
            if len(self.cache) >= self.cache_index:
                return self.cache[self.cache_index - 1]
            if self.pattern_file.closed:
                raise StopIteration
            
            line = self.pattern_file.readline()
            if not line:
                self.pattern_file.close()
                raise StopIteration
                
            pattern, search, replace = line.split(None, 3)
            funcs = build_math_and_appll_function(
                pattern, search, replace)
            self.cache.append(funcs)　　# 在返回匹配和应用功能之前（保存在元组funcs中）
            return funcs
        rules = LazyRules()
        
### 高级迭代器

例如，解决字母算术谜题。

HAWAII+IDAHO+IOWA+OHIO==STATES

510199+98153+9301+3593==621246

H=5 A=1 W=0 I=9 D=8 O=3 S=6 T=2 E=4

示例代码

    import re
    import itertools
 
    def solve(puzzle):
        words = re.findall('[A-Z]+', puzzle.upper()) # 找到字符串，形成字符串列表
        unique_characters = set(''.join(words)) # 通过集合唯一性，找到字母的集合
        assert len(unique_characters) <= 10, 'Too many letters' # 判断字母的种类是否大于10
        first_letters = {word[0] for word in words} # 获取每个字符串的首字母　
        n = len(first_letters) # 字符串数量
        sorted_characters = ''.join(first_letters) + ''.join(unique_characters - first_letters) #首字符在前的，有序字符串
        characters = tuple(ord(c) for c in sorted_characters) # 获取字母的对应的字节值列表
        digits = tuple(ord(c) for c in '0123456789') # 计算0-9数字的字节值生成元组
        zero = digits[0]  # 0的字节值
        for guess in itertools.permutations(digits, len(characters)): # 通过迭代器取出指定数目的>有序组合
            if zero not in guess[:n]:  # 判断是否存在０
                equation = puzzle.translate(dict(zip(characters, guess)))# 先将characters和guess>元素对构造出作为转换表的字典，然后通过translate,将字符串中的每个字母转换为相应的数字）
                if eval(equation): # 判断equation是否成立
                    return equation
 
    if __name__ == '__main__':
        import sys
        for puzzle in sys.argv[1:]:
            solution = solve(puzzle)
            if solution:
                print(solution)

运行结果
    
    [root@isoft_lp 0306]# python3 alphametics.py "HAWAII + IDAHO + IOWA + OHIO == STATES"

    HAWAII + IDAHO + IOWA + OHIO == STATES                                                                                                               
    510199 + 98153 + 9301 + 3593 == 621246 
    
解决这个问题，首先要找到谜题中所有的[A-Z]字母

    re.findall('[0-9]+', '16 2-by-4s in rows of 8')  # 找到字符串中的数字

    re.findall('[A-Z]+', 'SEND + MORE == MONEY')　　# 找到字符串中的字母

    re.findall(' s.*? s', "The sixth sick sheikh's is sixth sheep's sick.") # 先匹配一个空格，后跟s 然后任意字符然后空格s;重叠的匹配只返回前一个
  
**在序列中需找不同的元素**

集合使得在序列中查找不同的元素变得容易。

    > a_list = ['The', 'sixth', 'sick', "sheik's", 'sixth', "sheep's", 'sick']
    > set(a_list)
    {"sheik's", 'sick', 'The', "sheep's", 'sixth'}　# set()函数将字符串列表转为集合（去掉重复，且无序）
    > a_string = 'EAST IS EAST'
    > set(a_string)
    {'E', ' ', 'I', 'S', 'T', 'A'}　　　　# set()函数可以将字符串转为集合
    > words = ['SEND', 'MORE', 'MONEY']
    > ''.join(words)
    'SENDMOREMONEY'　　# ''.join(words)将字符串列表拼接成一个字符串
    > set(''.join(words))
    {'D', 'E', 'M', 'Y', 'S', 'R', 'O', 'N'} # 先拼接字符串，先后转为集合（去掉重复的字母）
    > unique_characters = set(''.join(words)) # 找到了题目提供不同字符的集合

**断言**

python中assert语句用作断言。例如

    assert 1 + 1 == 2  # True
    assert 1 + 1 == 3  # AssertionError
    assert len(unique_characters) <= 10, 'Too many letters' # 出现AssertionError，打印"Too many letters"因为数字只有０－９ 10个数字，如果字母大于10,肯定是无解的

**生成器表达式**

    > unique_characters = { 'E', 'D', 'M', 'O', 'N', 'S', 'R', 'Y'}
    > gen = (ord(c) for c in unique_characters)  # 生成器表达式类似一个yield值的匿名函数
    > gen　　# 生成器表达式返回迭代器
    <generator object <genexpr> at 0x7f74c9f02938>　
    > next(gen)       # 调用next(gen)返回迭代器的下一个值
    68
    > next(gen)    
    69
    > tuple(ord(c) for c in unique_characters) # 将生成器表达式ord(c) for c in unique_characters传递给tiple()，生成一个元组
    (68, 69, 77, 89, 82, 83, 79, 78)

**使用生成器表达式取代列表解析可以同时节省cpu和内存，如果构造一个列表的目的仅仅是传递给别的函数（比如传递给tuple或set()),推荐使用生成器表达式替代**

**生成器函数**

    def ord_map(a_string):
        for c in a_string:
            yield ord(c)
    gen = ord_map(unique_characters)

生成器表达式功能相同，但更紧凑

### 计算排列

    > import itertools　　
    > perms = itertools.permutations([1,2,3], 2)　# permutations()函数接受一个序列(3个元素的列表，和排列的元素的数目）函数返回一个迭代器，可以在for循环使用它
    > next(perms)　　# [1,2,3]取２个的第一个排列是（１，2)
    (1, 2)
    > next(perms)
    (1, 3)
    > next(perms)
    (2, 1)           # 排列是有序的
    > next(perms)
    (2, 3)
    > next(perms)
    (3, 1)
    > next(perms)
    (3, 2)
    > next(perms)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    StopIteration

permutaitons()函数可以接受任何序列，甚至是字符串。

    >perms = itertools.permutations('ABC', 3)　# 字符串'ABC'和列表['A','B','C']是等价的
    > for string in perms:
    ...     print(string)
    ... 

    ('A', 'B', 'C')
    ('A', 'C', 'B')
    ('B', 'A', 'C')
    ('B', 'C', 'A')
    ('C', 'A', 'B')
    ('C', 'B', 'A')
    > list(itertools.permutations('ABC', 3))　# permutaitons()函数总是返回迭代器，将这个迭代器传给内建list()函数接收排列
    [('A', 'B', 'C'), ('A', 'C', 'B'), ('B', 'A', 'C'), ('B', 'C', 'A'), ('C', 'A', 'B'), ('C', 'B', 'A')]

### itertools模块中其他有意思的方法

    > list(itertools.product('ABC', '123'))　# itertools.product()函数返回包含两个序列的笛卡尔乘积的迭代器
    [('A', '1'), ('A', '2'), ('A', '3'), ('B', '1'), ('B', '2'), ('B', '3'), ('C', '1'), ('C', '2'), ('C', '3')]
    > list(itertools.combinations('ABC', 2)) # itertools.combinations()函数返回包含给定序列的给定长度的所有组合的迭代器
    [('A', 'B'), ('A', 'C'), ('B', 'C')]
    > names = list(open('favorite-people.text', encoding='utf-8'))　# 这个表达式将文本内容以一行一行组成的列表返回
    > names
    ['Dora\n', 'Ethan\n', 'Wesley\n', 'John\n', 'Anne\n', 'Mike\n', 'Chris\n', 'Sarah\n', 'Alex\n', 'Lizzie\n']
    > names = [name.rstrip() for name in names]　# 通过rstrip字符串方法移除每行的空白
    > names
    ['Dora', 'Ethan', 'Wesley', 'John', 'Anne', 'Mike', 'Chris', 'Sarah', 'Alex', 'Lizzie']
    > names=sorted(names)　# 进行排列
    > names
    ['Alex', 'Anne', 'Chris', 'Dora', 'Ethan', 'John', 'Lizzie', 'Mike', 'Sarah', 'Wesley']
    > names = sorted(names, key=len)　# 通过key参数定义排序规则
    > names
    ['Alex', 'Anne', 'Dora', 'John', 'Mike', 'Chris', 'Ethan', 'Sarah', 'Lizzie', 'Wesley']
    > groups = itertools.groupby(names, len)　# 接收一个序列和一个key函数，返回一个生成二元组的迭代器，每个二元组包含key_functoion(each item)的结果和另一个包含着所有共享key结果的元素的迭代器
    > groups
    <itertools.groupby object at 0x7f6788c8da48>
    > list(groups)
    [(4, <itertools._grouper object at 0x7f6788c86da0>), (5, <itertools._grouper object at 0x7f6788c86dd8>), (6, <itertools._grouper object at 0x7f6788c86e10>)]　# 调用list()函数会耗尽这个迭代器，将迭代器中所以元素生成了list。迭代器一但使用，就无法重新开始
    > groups = itertools.groupby(names, len)　# 重新生成迭代器,会分别生成４个字母的迭代器，５个字母的迭代器，６个字母的迭代器
    > for name_length, name_iter in groups:　
    ...     print('Names with {0:d} letters:'.format(name_length))
    ...     for name in name_iter:
    ...         print(name)
    ... 　# 
    Names with 4 letters:
    Alex
    Anne
    Dora
    John
    Mike
    Names with 5 letters:
    Chris
    Ethan
    Sarah
    Names with 6 letters:
    Lizzie
    Wesley

itertools.groupby()只有当输入序列已经按分组函数排过序才能正常工作。

    > list(range(0,3))
    [0, 1, 2]
    > list(range(10,13))
    [10, 11, 12]
    > list(itertools.chain(range(0,3), range(10,13)))　# itertools.chain()函数接受两个迭代器，返回一个迭代器，它接受任何数目的迭代器，并把他们按传入顺序串在一起
    [0, 1, 2, 10, 11, 12]
    > list(zip(range(0,3), range(10,13)))　# zip函数：接收任何数目的序列，然后返回一个迭代器，其第一个元素是每个序列的第一个元素组成的数组，以此类推
    [(0, 10), (1, 11), (2, 12)]
    > list(zip(range(0,3), range(10,14)))　# zip在到达最短序列结尾的时候停止。
    [(0, 10), (1, 11), (2, 12)]
    > list(itertools.zip_longest(range(0,3), range(10,14)))# itertools.zip_longest()函数到达最长的序列的结尾时停止，空的填入None
    [(0, 10), (1, 11), (2, 12), (None, 13)]
    > characters = ('S', 'M', 'E', 'D', 'O', 'N', 'R', 'Y')
    > guess = ('1', '2', '0', '3', '4', '5', '6', '7')
    > tuple(zip(characters, guess)) #  zip将字母列表，数字列表对应生成一组组字母数字对
    (('S', '1'), ('M', '2'), ('E', '0'), ('D', '3'), ('O', '4'), ('N', '5'), ('R', '6'), ('Y', '7'))
    > dict(zip(characters, guess))　# 将字母列表、数字列表生成对应键值对的字典
    {'S': '1', 'E': '0', 'N': '5', 'D': '3', 'O': '4', 'Y': '7', 'R': '6', 'M': '2'}

算术谜题解决方法使用这个方法对每一个可能的解法创建一个将谜题中字母映射到解法中的数字的字典

    characters = tuple(ord(c) for c in sorted_characters)
    digits = tuple(ord(c) for c in '0123456789')
    ...
    for guess in iteratools.permutations(digits, len*characters)):
        ...
        equation = puzzle.translate(dict(zip(characters, guess)))

### translate方法

python字符串方法有很多。

    > translation_table = {ord('A'): ord('O')}　# 字符串翻译从一个转换表开始，转换表是将一个字符映射到另一个字符的字典(一个字节映射到另一个）
    > translation_table　# python3字节是整型数，ord()函数返回字符的ASCII码。
    {65: 79}
    > 'MARK'.translate(translation_table)# 一个字符串的translate()方法接收一个转换表，并用它来转换该字符串。
    'MORK'
    > characters = tuple(ord(c) for c in 'SMEDONRY')# 使用生成器表达式，可以快速的计算字符串每个字符的字节值
    > characters
    (83, 77, 69, 68, 79, 78, 82, 89)
    > guess = tuple(ord(c) for c in '91570682')# 使用另一个生成器表达式，快速的计算出字符串中每个数字的字节值，计算结果guess，正好是alphametics.solve()函数中iteratools.permutations()函数返回值的格式
    > guess
    (57, 49, 53, 55, 48, 54, 56, 50)
    > translation_table = dict(zip(characters, guess))#通过characters和guesszipping出来的元素对序列构造出的字典作为转换表，正是alphametics.solve()在for循环里面干的事情
    > translation_table
    {82: 56, 83: 57, 68: 55, 69: 53, 89: 50, 77: 49, 78: 54, 79: 48}
    > 'SEND + MORE == MONEY'.translate(translation_table)# 最后我们将转换表传递给原始字符串的translate（）方法。将字符串中的每个字母转换为相应的数字（基于characters中字母和guess中的数字）
    '9567 + 1085 == 10652'
    > eval('9567 + 1085 == 10652')
    True
    > eval('"A" + "B"')
    'AB'
    > eval('"MARK".translate({65:79})')
    'MORK'
    > eval('"AAAAA".count("A")')
    5
    > eval('["*"] * 5')
    ['*', '*', '*', '*', '*']
    > x=5
    > eval("x * 5")
    25
    > eval("pow(x,2)")
    25
    > import math
    > eval("math.sqrt(x)")
    2.23606797749979

eval()接受的表达式可以引用evel()之外定义的全局变量，以及函数、模块

    > import subprocess
    > eval("subprocess.getoutput('ls ~')")
    'abc.xml\nAndroidStudioProjects\navocado\ncpu.cfs_quota_us~\nDesktop\nDocuments\ninstall.txt\nLinux-version-test-result-201701181301.tar.gz\nrpmbuild\ntest_brain\ntest.brain\ntest.log\n下载'

subprocess模块允许执行任何shell命令并以字符串形式获得输出

总的来说，这个程序通过暴力解决字母数字算术谜题，通过穷举所有可能。

１通过re.findall()函数找到谜题中所有的字母

2.使用集合和set()函数找到谜题出现的所有不同的字母

3.使用assert语句检查是否有超过１０个不同的字母，超过则无解

4.通过一个生成器对象将字符转换成对应的ascii码值

5.使用itertools.permutations()函数计算所有可能的解法

6.使用translate()字符串方法将所有可能的解转换成python表达式

7.使用eval()函数通过求值python表达式来检验解法

8.返回第一个求值结果为True的解法
