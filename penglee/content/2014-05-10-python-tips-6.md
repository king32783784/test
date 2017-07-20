Title: Python-Tips(六）
Date:2014-05-10
Author:李鹏
Slug:python 
Tags:Python-Tips
category:编程语言-Python

### Tips 21

**重构**

前面将了测试驱动开发，但就算尽全力编写的单元测试，仍然会遇到错误。仍然会有考虑不全面的测试用例。
比如前面的实现的转换数字的程序，如果输入空字符，会触发InvalidRomanNumeralError例外。
在出现错误后，应该在修复前写出一个导致该失败情形的测试用例。

    class FromRomanBadInput(unittest.TestCase):
        def testBlank(self):
            '''from_roman should fail with blank string'''
            self.assertRaises(roman2.InvalidRomanNumeralError, roman2.form_roman, '')

执行测试用例会失败，现在可以修复这个bug。

    if not s:
        raise InvalidRomanNumberalError('Input can not be blank')

然后测试成功

正常情况下，罗马数字中任何一个字符在同一行中不得重复出现三次以上，但通过一行4个Ｍ字符来代表4000,这样就可以把数字范围才能够１..3999转为１..4999．先修改测试用例
增加 (4000, 'MMMM'), (4500, 'MMMMD'),(4888, 'MMMMDCCCLXXXVIII), (4999, 'MMMMCMXCIX')
过大值测试由4000转为5000,太多重复数字测试'MMMM'被定为符合要求的罗马数字，所以'MMMM'改为'MMMMM',范围测试的１-3999,改为１-4999
测试失败
因为一些新需求导致失败的测试用例，现在就需要对实现进行修改。
首先判断是否合法的罗马数字的匹配规则要修改
M{0,4}对4000+数字的支持
对数字判断的范围改为(0<n<5000)
到底这样修改，符合要求吗？光说不行啊，还得测试才能确保。测试最终通过，说明我们的修改是有效的

需求变了，实现跟着变了，但改变实现后，影响之前的功能吗？新功能实现成功吗？完整的单元测试的好处就是明确的告诉你修改是否成功，是否对之前的功能有影响。

重构是修改可运行的代码，使其表现更好。更佳可以是性能更好，占用内存更少，占用更少的空间，更加简洁、增加更多功能，代码可读性更高。如果代码存在完整的单元测试的前提下，你才能毫无顾忌的去修改去重构，不然心里没底啊。

原来代码中的正则表达式看起来可读性不高，可以用个查询表替换，但是替换之后功能会不会有影响？别怕，我们已经实现了相应的单元测试。

现在可以大胆去修改实现

    class OutOfRangeError(ValueError): pass
    class NotIntegerError(ValueError): pass
    class InvalidRomanNumeralError(ValueError): pass

    roman_numeral_map = (('M',  1000),
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

    to_roman_table = [ None ]
    from_roman_table = {}
 
    def to_roman(n):
        '''convert integer to Roman numeral'''
        if not (0 < n < 5000):
            raise OutOfRangeError('number out of range (must be 1..4999)')
        if int(n) != n:
            raise NotIntegerError('non-integers can not be converted')
        return to_roman_table[n]

    def from_roman(s):
        '''convert Roman numeral to integer'''
        if not isinstance(s, str):
            raise InvalidRomanNumeralError('Input must be a string')
        if not s:
            raise InvalidRomanNumeralError('Input can not be blank')
        if s not in from_roman_table:
            raise InvalidRomanNumeralError('Invalid Roman numeral: {0}'.format(s))
        return from_roman_table[s]

    def build_lookup_tables():
        def to_roman(n):
            result = ''
            for numeral, integer in roman_numeral_map:
                if n >= integer:
                    result = numeral
                    n -= integer
                    break
            if n > 0:
                result += to_roman_table[n]
            return result

        for integer in range(1, 5000):
            roman_numeral = to_roman(integer)
            to_roman_table.append(roman_numeral) # 1-5000的罗马数字列表
            from_roman_table[roman_numeral] = integer　＃ 1-5000罗马数字和阿拉伯数字的字典

    build_lookup_tables()

修改完成好，再次执行单元测试，测试通过，说明虽然实现变了，但功能依旧能保证。

单元测试是一个威力巨大的概念，如果实施的好，可以降低维护成本，提高项目的灵活性。但编写良好的测试用例非常艰难。很多语言都有自己的单元测试框架，但框架直接的共同点：

* 设计测试用例是具体、自动且独立的工作
* 在编写被测代码之前编写测试用例（测试驱动开发）
* 编写用于检查好输入并验证正确结果的测试
* 编写用于检查坏输入并做出正确失败响应的测试
* 编写并更新测试用例反映新需求
* 重构以提升性能、可扩展性、可读性、可维护性及补充特性

