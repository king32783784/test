Title: Python-Tips(五）
Date:2014-05-07
Author:李鹏
Slug:python 
Tags:Python-Tips
category:编程语言-Python

### Tips 20

**TDD／单元测试**

例子要求
1.只有一种正确的途径用阿拉伯数字表示罗马数字。
2.反过来一样，一个字符串类型的有效的罗马数字也仅可以表示一个阿拉伯数字（即，这种转换方式也是只有一种）。
3.只有有限范围的阿拉伯数字可以以罗马数字表示，那就是1‐3999。而罗马数字表示大数字却有几种方式。例如，为了表示一个数字连续出现时正确的值则需要乘以1000。限定罗马数字在1到3999之间。
4.无法用罗马数字来表示0。
5.无法用罗马数字来表示负数。
6.无法用罗马数字来表示分数或非整数

１．to_roman()方法应该返回代表1-3999的罗马数字

    import roman1
    import unittest
    
    class KonwnValues(unittest.TestCase): # 测试用例类应该继承unittest的TestCase子类
        known_values = ((1,'I'),　　# 需要测试所有明显边界值
                        (2, 'II'),
                        (3, 'III'),
                        (4, 'IV'),
                        (5, 'V'),
                        (6, 'VI'),
                        (7, 'VII'),
                        (8, 'VIII'),
                        (9, 'IX'),
                        (10, 'X'),
                        (50, 'L'),
                        (100,'C'),
                        (500, 'D'),
                        (1000, 'M'),
                        (31, 'XXXI'),
                        (148, 'CXLVIII'),
                        (294, 'CCXCIV'),
                        (312, 'CCCXII'),
                        (421, 'CDXXI'),
                        (528, 'DXXVIII'),
                        (621, 'DCXXI'),
                        (782, 'DCCLXXXII'),
                        (870, 'DCCCLXX'),
                        (941, 'CMXLI'),
                        (1043, 'MXLIII'),
                        (1110, 'MCX'),
                        (1226, 'MCCXXVI'),
                        (1301, 'MCCCI'),
                        (1485, 'MCDLXXXV'),
                        (1509, 'MDIX'),
                        (1607, 'MDCVII'),
                        (1754, 'MDCCLIV'),
                        (1832, 'MDCCCXXXII'),
                        (1993, 'MCMXCIII'),
                        (2074, 'MMLXXIV'),
                        (2152, 'MMCLII'),
                        (2212, 'MMCCXII'),
                        (2343, 'MMCCCXLIII'),
                        (2499, 'MMCDXCIX'),
                        (2574, 'MMDLXXIV'),
                        (2646, 'MMDCXLVI'),
                        (2723, 'MMDCCXXIII'),
                        (2892, 'MMDCCCXCII'),
                        (2975, 'MMCMLXXV'),
                        (3051, 'MMMLI'),
                        (3185, 'MMMCLXXXV'),
                        (3250, 'MMMCCL'),
                        (3313, 'MMMCCCXIII'),
                        (3408, 'MMMCDVIII'),
                        (3501, 'MMMDI'),
                        (3610, 'MMMDCX'),
                        (3743, 'MMMDCCXLIII'),
                        (3844, 'MMMDCCCXLIV'),
                        (3888, 'MMMDCCCLXXXVIII'),
                        (3940, 'MMMCMXL'),
                        (3999, 'MMMCMXCIX'))           
                        
        def test_to_roman_konwn_values(self):　# 每个独立的测试都有自己的不含参数及没有返回值的方法，如果不跑异常则测试通过
            '''to_roman should give known result with know input'''
            for interger, numeral in self.konwn_values:
                result = roman1.to_roman(integer)　# 这里调用了roman1中的to_roman()方法，这里roman1仍未编写，但此处已定义了其接口
                self.assertEqual(numeral, result)　# 假设to_roman()方法已经正确定义，正确调用，成功实现并返回了一个值，这里判断返回值是否正确，TestCase类提供assertEqual方法检查两个值是否相对。如果返回值与预期值相同，则会正常退出，也就通过了测试
                
    if __name__ == '__main__':
        unittest.main()

roman1.py

    def to_roman(n):
        '''整型转罗马数字'''
        pass  # 什么都不做
        
现在执行测试用例，结果如你所料，肯定会失败。-v　参数会有更详细的输出
输出：
    [root@isoft_lp 0306]# python romantest1.py  -v
    test_to_roman_known_values (__main__.KnownValues) #运行脚本就会执行unittest.main(),该方法执行每一个测试用例，每条用例都是romantest.py中的类方法，这些类没有必要的组织要求；它们每一个都包含一个独立的测试方法，可以编写一个含有多个方法的类。但每个类都必须继承unittest.TestCase
    to_roman should give known result with known input ... FAIL # 每个测试用例，unitest模块都会打印测试方法的docstring

    ======================================================================
    FAIL: test_to_roman_known_values (__main__.KnownValues)　　　#每个失败的用例，unittest模块会打印出详细的跟踪信息
    to_roman should give known result with known input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    File "romantest1.py", line 66, in test_to_roman_known_values
        self.assertEqual(numeral, result)　　# assertEqual() 的调用抛出了一个AssertionError异常，因为to_roman(1)应该返回"I",但时间没有
    AssertionError: 'I' != None

    ----------------------------------------------------------------------
    Ran 1 test in 0.000s　# 说明每个用例执行情况后，打印执行了多少用例，用了多少时间

    FAILED (failures=1)　# 如果测试用例没有通过的话，unittest可以区别用例执行失败跟程序错误的。像assertXYX, assertRaise这样的assertEqual方法的失败是因为被声明的条件不是为真，或则预期的异常没有抛出。
    
现在可以实现to_roman

    roman_numeral_map = (('M', 1000),
                     ('CM', 900),
                     ('D',  500),
                     ('CD', 400),
                     ('C',  100),
                     ('XC', 90),
                     ('L',  50),
                     ('XL', 40),
                     ('X',  10),
                     ('IX', 9),
                     ('V',  5),
                     ('IV', 4),
                     ('I',  1))
                              # 组成罗马数字基本的元素
    def to_roman(n):
    '''整型转罗马数字'''
        result = ''
        for numeral, integer in roman_numeral_map:
            while n >= integer:
                result += numeral
                n -= integer
        return result
        
这样就可以通过测试了

如果输入非法值会怎么样呢？
比如输入4000,程序返回了MMMM,和预期不符，而且不是一个正确的罗马数
当to_roman()应该抛出一个OutOfRangeError异常

测试代码如下：

    class ToRomanBadInput(unittest.TestCase):
        def test_too_large(self):
            '''to_roman should fail with large input'''
            self.assertRaise(roman2.OutOfRangeErr, roman2.to_roman, 4000)
        该测试方法需要以下：期望的异常，要测试的方法及传入给方法的参数
最后一行，这里没有直接调用to_roman()，也不需要手动检查它抛出的异常类型（通过一个try...except块包装），　这些assertRaises方法都完成了。
我们要做的事情只有，告诉assertRaise所期望的异常类型(roman2.OutOfRangeErr),被测方法(to_roman()),以及方法的参数(4000).assertEqual方法负责调用to_roman()和检查方法抛出roman2.OutOfRangeError异常。这里只是把to_roman方法以参数传递，没有调用被测方法，也不是被测方法作为一个字符串名字传递进去。

执行
    [root@isoft_lp 0306]# python romantest2.py  -v
    test_to_roman_known_values (__main__.KnownValues)
    to_roman should give known result with known input ... ok
    test_too_large (__main__.ToRomanBadInput)
    to_roman should fail with large input ... ERROR

    ======================================================================
    ERROR: test_too_large (__main__.ToRomanBadInput)
    to_roman should fail with large input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "romantest2.py", line 71, in test_too_large
        self.assertRaises(roman2.OutOfRangeError, roman2.to_roman, 4000)
    AttributeError: 'module' object has no attribute 'OutOfRangeError'

    ----------------------------------------------------------------------
    Ran 2 tests in 0.000s

    FAILED (errors=1)

测试本身是失败，但这里是报错了，提示没有OutOfRangeError
在测试模块添加

    class OutOfRangeError(ValueError):
        pass
        
异常也是类，越界是值错误的一种，因此继承ValueError

再次执行，仍然失败，但没有出错，意味者用例执行成功了。
现在修改代码，使其通过

    def to_roman(n):
        '''convert interger to Roman'''
        if n > 3999：
            raise OutOfRangeError('number out of range (must be less than 4000)')
        result = ''
        for numeral, interger in roman_numeral_map:
            whiel n >= integer:
                result += numeral
                n -= interger
        return result
        
最终两个测试都通过了

    [root@isoft_lp 0306]# python romantest2.py  -v
    test_to_roman_known_values (__main__.KnownValues)
    to_roman should give known result with known input ... ok
    test_too_large (__main__.ToRomanBadInput)
    to_roman should fail with large input ... ok

    ----------------------------------------------------------------------
    Ran 2 tests in 0.000s

    OK

我们的需求还提到无法转换０和负数，因此要增加用例来进行测试。

    def test_zero(self):
        '''to_roman　should fail with 0 input'''
        self.assertRaises(roman3.OutOfRangeError, roman3.to_roman,0) # 如果输入０触发错误
        
    def test_negative(self):
        ''' to_roman should fail with negative input'''
        self.assertRaises(roman3.OutOfRangeError, roman3.to_roman, -1) # 如果输入-1触发错误
        
执行测试，不出所料的失败，因为roman3中没有实现对应处理，接下来要考虑如何修改roman3让测试通过
修改如下：

    def to_roman(n):
        '''整型转罗马数字'''
        if not (0< n < 4000):
            raise OutOfRangeError('number out of range (must be less than 4000)')
        result = ''
        for numeral, integer in roman_numeral_map:
            while n >= integer:
                result += numeral
                n -= integer
        return result

如果是非整型数据呢？需要再添加对应的测试用例:

    def test_non_interger(self):
        '''to_roman should fail with non-integer'''
        self.assertRaises(roman2.NotIntegerError, roman2.to_roman, 0.5)

执行测试，缺少NotIntegerError,需要在roman2模块中进行定义，和前面一样

    class NotINtergerError(ValueError):pass
    
再次执行测试，不出所料，提示未触发异常，因为roman2没有进行判断，实现该判断：

    if not isinstance(n, int):
        raise NotIntegerError('no-integers can not be converted')
再次执行测试：

    test_to_roman_known_values (__main__.KnownValues)
    to_roman should give known result with known input ... ok
    test_negative (__main__.ToRomanBadInput)
    to_roman should fail with negative input ... ok
    test_non_interger (__main__.ToRomanBadInput)
    to_roman should fail with non-integer ... ok
    test_too_large (__main__.ToRomanBadInput)
    to_roman should fail with large input ... ok
    test_zero (__main__.ToRomanBadInput)
    to_roman should fail with 0 input ... ok----------------------------------------------------------------------
    Ran 5 tests in 0.001s
    OK

开头提出的需求是相互转换，所以还要实现罗马数字转阿拉伯数字的功能，不过测试先行。

    
    def test_from_roman_know_values(self):
        '''from_roman should give know result with konwn input'''
        for integer, numeral in self.known_values:
            result = roman2.from_roman(numeral)
            self.assertEqual(integer, result)

看起来好像和前面的测试阿拉伯转罗马数字一样，确实，调用的测试数据是一样的，只不过输入输出颠倒了。理论上把数字传递给to_roman()方法，得到一个罗马字符串，然后把字符串传入from_roman(),然后又返回一个数字，这个数字和最初传给to_roman()应该是一样的。

    n = from_roman(to_roman(n)) for all values of n

那么，from_roman的边界取值测试就可以利用这个方法，进行测试，也就是输入的还是数字，先调用to_roman()转成罗马数字，然后to_roman的输出作为from_roman的输入，进行from_roman的测试
    class RoundtripCheck(unittest.TestCase):
 
        def test_roundtrip(self):
            '''from_roman(to_roman(n))==n for all n'''
            for integer in range(1, 4000):
                numeral = roman2.to_roman(integer)
                result = roman2.from_roman(numeral)
                self.assertEqual(integer, result)

如果现在测试，肯定是提示error,因为我们还没有实现from_roman

下面开始实现from_roman:

    def from_roman(s):
        '''罗马数字转整型'''
        result = 0
        index = 0
        for numeral, integer in roman_numeral_map:
            while s[index:index+len(numeral)] == numeral: # 沿着roman_numeral_map从上往下匹配，匹配一个转换一个再相加
                result += integer
                index += len(numeral)
            return result

现在开始执行测试，Ran 7 tests in 0.030s  OK

现在１-3999的合法输入的罗马数字都可以转换为正确的数字，但是如果不是合法的罗马数字呢？这就需要一个方法检查输入的字符是不是有效的罗马数字。
罗马数字的规则不再描述:

    def test_too_many_repeated_numerals(self):
        '''from_roman should fail with too many repeated'''
        for s in ('MMMM', 'DD', 'CCCC', 'LL', 'XXXX', 'VV', 'IIII'): # 一种情况，比如4是IV而不是IIII,首先测试这类情况
            self.assertRaises(roman2.InvalidRomanNumeralError,
                              roman2.from_roman, s)

    def test_repeated_pairs(self):
        '''from_roman should fail with repeated pairs of numerals'''
        for s in ('CMCM', 'CDCD', 'XCXC', 'XLXL', 'IXIX', 'IVIV'): # 检查某些不允许的重复，如IX为９，但IXIX不合法
            self.assertRaises(roman2.InvalidRomanNumeraError,
                              roman2.from_roman,s)
 
    def test_malformed_antecedents(self):
        '''from_roman shoud fail with malformed antecedents'''
        for s in ('IIMXCC', 'VX', 'DCM', 'CMM', 'IXIV', 'MCMC', 'XCX', 'IVI',　# 检测数字是否正确顺序出现，比如CL150,但LC不合法
                  'LM', 'LD', 'LC'):
            self.assertRaises(roman2.InvalidRomanNumeraError,
                              roman2.from_roman, s)


现在要做的是修改from_roman实现对输入罗马数字的检测：
    
    roman_numeral_pattern = re.compile('''
        ^        # 字符的开头
        M{0,3}   # 千位,可以是0-3个M
        (CM|CD|D?C{0,3})  # 百位,900(CM), 400(CD), 500(D) 0-300（0-3个C)
        (XC|XL|L?X{0,3})  # 十位,90(XC),40(XL),0-30(0-3个X),50(L)
        (IX|IV|V?I{0,3})  # 个位,9(IX), 4(IV), 5(V), 0-3(I,II,III)
        $                 # 字符结束
        ''', re.VERBOSE)
        if not roman_numeral_pattern.search(s):
            raise InvalidRomanNumberalError('Invalid Roman numeral: {0}'.format(s))
最终：
    ..........
    ----------------------------------------------------------------------
    Ran 10 tests in 0.038s
    OK

测试驱动开发(TDD)方法的好处不言而喻。所以会测试的开发才是好开发。


 

