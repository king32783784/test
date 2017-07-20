Title: python实现awk域简单例子
Date:2017-02-20
Author:李鹏
Slug: python
Tags:Python
category:编程语言-Python

### 问题

ltp功能验证测试的结果的文本（截取片段）格式为：

    Test Start Time: Tue Feb 14 15:47:55 2017
    -----------------------------------------
    Testcase                       Result     Exit Value
    --------                       ------     ----------
    abort01                        PASS       0
    accept01                       PASS       0
    accept4_01                     PASS       0
    acct01                         PASS       0
    add_key01                      PASS       0
    add_key02                      PASS       0
    adjtimex01                     PASS       0
    bind01                         PASS       0
    capset02                       PASS       0
    cacheflush01                   CONF       32
    chdir01                        PASS       0
    chdir01A                       PASS       0
    fork10                         PASS       0
    fork11                         PASS       0
    fork13                         FAIL       2
    dio28                          CONF       32
    aio01                          PASS       0
    aio02                          PASS       0
    memcg-stress                   FAIL       1
    -----------------------------------------------
    Total Tests: 1884
    Total Skipped Tests: 157
    Total Failures: 28
    Kernel Version: 4.9.0-10
    Machine Architecture: x86_64
    Hostname: test

我们在处理测试结果时，一般想得到的数据包括”Fail case的数量、CONF case的数量， PASS case的数量，测试case的总数， Fail case的列表， Conf case的列表，
Pass case的列表。虽然测试log最后会给出部分数据，但不准确，需要进行处理。下面分别用shell、python实现获取这些数据。

#### Shell版本

示例代码：

    #!/usr/bin/bash

    FILE='runalltest.log'
    # CASE 数量
    FAILNUM=$(grep FAIL $FILE | wc -l)
    PASSNUM=$(grep PASS $FILE | wc -l)
    CONFNUM=$(grep CONF $FILE | wc -l)
    TOTAL=$(echo "$FAILNUM + $PASSNUM + $CONFNUM" | bc)

    # CASE 列表
    FAILLIST=$(grep FAIL runalltest.log | awk '{print $1}') # awk打印第一列
    CONFLIST=$(grep CONF runalltest.log | awk '{print $1}')
    PASSLIST=$(grep PASS runalltest.log | awk '{print $1}')

    echo "Fail case num is $FAILNUM"
    echo "Pass case num is $PASSNUM"
    echo "Conf case num is $CONFNUM"
    echo "Total case num is $TOTAL"
    echo "Fail case list is $FAILLIST"
    echo "Conf case list is $CONFLIST"
    echo "Pass case list is $PASSLIST"
    
执行结果：

    Fail case num is 2
    Pass case num is 15
    Conf case num is 2
    Total case num is 19
    Fail case list is fork13
    memcg-stress
    Conf case list is cacheflush01
    dio28
    Pass case list is abort01
    accept01
    accept4_01
    acct01
    add_key01
    add_key02
    adjtimex01
    bind01
    capset02
    chdir01
    chdir01A
    fork10
    fork11
    aio01
    aio02
    
#### Python版本

示例代码：

    #!/usr/bin/env python
    # *-*coding=utf-8*-*
    import re

    def data_process():
        PASSNUM=0  # PASS case 数量
        FAILNUM=0  # FAIL case 数量
        CONFNUM=0  # CONF case 数量
        PASSLIST=[] # PASS case 列表
        FAILLIST=[] # FAIL case 列表
        CONFLIST=[] # CONF case 列表
        f = open("/opt/ltp/results/runalltest.log")
        while True:
            lines = f.readlines(10000)
            if not lines:
                break
            for line in lines:
                linelist = re.split('\W+', line) # 通过正则表达式将字符串分离
                if "PASS" in linelist:           # 拆分后，PASS字段可能不在第二列，判断改行是否存在PASS
                    PASSNUM += 1
                    if linelist.index("PASS") == 1:
                        PASSLIST.append(linelist[0])
                    else:
                        index = linelist.index("PASS")
                        PASSLIST.append('-'.join(linelist[:index]))  # 将本行PASS所在列前面的字符串拼接
                if "FAIL" in linelist:
                    FAILNUM +=1
                    if linelist.index("FAIL") == 1:
                        FAILLIST.append(linelist[0])
                    else:
                        index = linelist.index("FAIL")
                        FAILLIST.append("-".join(linelist[:index]))
                if "CONF" in linelist:
                    CONFNUM += 1
                    if linelist.index("CONF") == 1:
                        CONFLIST.append(linelist[0])
                    else:
                        index = linelist.index("CONF")
                        CONFLIST.append("-".join(linelist[:index]))
        TOTALNUM = int(FAILNUM) + int(PASSNUM) + int(CONFNUM)
        print("Fali case num is %s" % FAILNUM)
        print("Pass case num is %s" % PASSNUM)
        print("Conf case num is %s" % CONFNUM)
        print("Total case num is %s" % TOTALNUM)
        print("Fail case list is %s" % FAILLIST)
        print("Conf case list is %s" % CONFLIST)
        print("Pass case list is %s" % PASSLIST)

    if __name__ == "__main__":
        data_process()

执行结果：

    Fali case num is 2
    Pass case num is 15
    Conf case num is 2
    Total case num is 19
    Fail case list is ['fork13', 'memcg-stress']
    Conf case list is ['cacheflush01', 'dio28']
    Pass case list is ['abort01', 'accept01', 'accept4_01', 'acct01', 'add_key01', 'add_key02', 'adjtimex01', 'bind01', 'capset02', 'chdir01', 'chdir01A', 'fork10', 'fork11', 'aio01', 'aio02']

两则执行的效率差不多，python版本稍快。

