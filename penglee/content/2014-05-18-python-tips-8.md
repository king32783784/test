Title: Python-Tips(七）
Date:2014-05-18
Author:李鹏
Slug:python 
Tags:Python-Tips
category:编程语言-Python

### Tips 23

**XML**

XML是一种描述层次结构话数据的方法。XML文档包含由起始和结束标签分割的一个或多个元素。下面这个就是个简单的XML文件：

    <foo>     # 这是foo元素的起始标签
    </foo>　　# 这是foo元素对应的结束标签
元素可以嵌套到任意层次

    <foo>
      <bar> </bar>  # 可以作为foo元素的子元素
　　</foo>
XML文档中第一个元素叫做根元素，每份XML文档只能有一个根元素。以下就不是一个xml文档。
　　<foo></foo>
    <bar></bar>　# 两个根元素
元素可以有其属性，类似字典的键值对。属性由空格分割列举在元素的起始标签中。一个元素中属性名不恩能够重复，属性值必须用括号包括起来，单引号或双引号都可以。

    <foo lang='en'> # foo元素有一个叫做lang的属性，属性值为'en'
      <bar id='papayawhip' lang="fr"></bar>　# bar元素分别两个属性,id和lang，每个属性都有对应值，每个元素具有独立的属性集
    </foo>
如果元素存在多个属性，书写的顺序不重要。元素的属性都是无序的键值对集，和字典类似。元素的个数是没有限制的。
元素可以有其文本内容
    <foo lang='en'>
    　<bar lang='fr>PapayaWhip</bar>
    </foo>
如果和开头那个啥都没有，较空元素。空元素的简洁表示：<foo/>
和python函数可以在不同模块中声明一样，可以在不同命名空间中声明XML元素。XML文档的命名空间看起来像URL.可以通过xmlns来定义默认命名空间。命名空间声明和元素属性类似，但作用不同。

    <feed xmlns='http://www.w3.org/2005/Atom'> # feed元素处于命名空间"http://www..../Atom' 
      <title>dive into mark</title>  #title元素的命名空间也是，命名空间会作用到子元素
    </feed>
还可以通过xmlns:prefix声明定义一个命名空间并取名为prefix.然后该命名空间的每个元素都必须显式的调用这个前缀。

    <atom:feed xmlns:atom='http://www.w3.org/2005/Atom'> # feed元素属于命名空间http.../Atom
    　　<atom:title> dive into mark </atom:title> # title元素也是
    <atom:feed>

对于XML解析器而言，以上两种方式是一样的。命名空间 + 元素名 = XML标识　前缀是用来引用命名空间的，所以对应解析器来说，这些前缀(atom:）无关紧要。名字空间、元素名、属性、元素的文本内容相同的情况下，xml文档相同。

在根元素之前，加上字符编码信息（无处不在啊）

    <?xml version='1.0' encoding='utf-8'?>

**Atom结构**

每个Atom订阅都共享一个根元素：即在命名空间http://www.w3.org/2005/Atom中的元素feed

    <feed xmlns='http://www.w3.org/2005/Atom'  # 表示命名空间Atom
       xml:lang='en'>    # 用来声明元素及子元素使用的语言 
      <title> dive into mark </title> # 表题
      <subtitle> currently between addictions</subtitle># 子标题
      <id> tag:diveintomark.org,2001-07-29:/</id>　# 全局唯一标识符
      <updated>2009-03-27T21:56:07Z</updated>
      <link rel='alternate' type='text/html' href='http://diveintomark.org/'/>　#link3个属性

    <entry>
      <author> # 作者
        <name>Mark</name>
        <uri>http://diveintomark.org/</uri>
      </author>
      <title>Dive into history, 2009 edition</title>                           # 标题
      <link rel='alternate' type='text/html'                                   # 文章链接 
        href='http://diveintomark.org/archives/2009/03/27/dive-into-history-2009-edition'/>
      <id>tag:diveintomark.org,2009-03-27:/archives/20090327172042</id>        #标识符
      <updated>2009-03-27T21:56:07Z</updated>                                  # 日期
      <published>2009-03-27T17:20:42Z</published>        
      <category scheme='http://diveintomark.org' term='diveintopython'/>       # 类别
      <category scheme='http://diveintomark.org' term='docbook'/>
      <category scheme='http://diveintomark.org' term='html'/>
      <summary type='html'>Putting an entire chapter on one page sounds        # 简介
        bloated, but consider this &amp;mdash; my longest chapter so far
        would be 75 printed pages, and it loads in under 5 seconds&amp;hellip;
        On dialup.</summary>
</entry>                    

 **解析XML**

接下来才是重点，不然啰嗦那么多干嘛

python可以使用几种不同的方式解析XML文档。它包含DOM和SAX解析器。这里讲一下ElementTree和库上边。

    >>> import xml.etree.ElementTree as etree # ElementTree属于Python标准库的一部分，位置为xml.etree.ElementTree
    >>> tree = etree.parse('feed.xml') # parse函数是ElementTree库的主要入口,使用文件名或流对象作为参数,parse()函数会解析完整的文档。如果内存资源紧张，可以增量式解析
    >>> root = tree.getroot() # parse函数会返回一个能代表整篇文档的对象，这不是根元素，获取根元素可以调用getroot()方法
    >>> root 
    <Element '{http://www.w3.org/2005/Atom}feed' at 0x7f61dc975ae8>

 ElementTree使用{namespace}localname来表达XML元素

**元素即列表**

在ElementTree API中，元素的行为就像列表一样。列表中的项即该元素的子元素

    >>> root.tag    # 根元素如下
    '{http://www.w3.org/2005/Atom}feed'
    >>> len(root) # 根元素的长度即为子元素的数量
    8
    >>> for child in root: # 我们可以像使用迭代器（列表）一样遍历其子元素
    ...     print(child)
    ... 
    <Element '{http://www.w3.org/2005/Atom}title' at 0x7fc09da09408>
    <Element '{http://www.w3.org/2005/Atom}subtitle' at 0x7fc09da09458>
    <Element '{http://www.w3.org/2005/Atom}id' at 0x7fc09da09548>
    <Element '{http://www.w3.org/2005/Atom}updated' at 0x7fc09da09598>
    <Element '{http://www.w3.org/2005/Atom}link' at 0x7fc09da09638>
    <Element '{http://www.w3.org/2005/Atom}entry' at 0x7fc09da09688>
    <Element '{http://www.w3.org/2005/Atom}entry' at 0x7fc09da09b38>
    <Element '{http://www.w3.org/2005/Atom}entry' at 0x7fc09da09ef8>
    从输出看到，根元素共8个子元素，所有feed级的元数据(title,subtitle,id,updated,link,entrya)
该列表只包括了直接的子元素，子元素如果有其自身的子元素，是不包含在这，他们包含在各自的子元素的列表中。

**属性即字典**

XML不只是元素的集合；每一个元素还有其属性集。一旦获取某个元素的引用，我们可以像操作字典一样来获取其属性

    >>> root.attrib # attrib是一个代表元素属性的字典，该部分的xml内容： <feed xmlns='http://www.w3.org/2005/Atom' xml:lang='en'>，前缀xml:指示一个内置的名字空间，每个XML不需声明便可使用
    {'{http://www.w3.org/XML/1998/namespace}lang': 'en'}
    >>> root[4] # 第五个子元素即子元素link
    <Element '{http://www.w3.org/2005/Atom}link' at 0x7fc09da09638>
    >>> root[4].attrib # link元素的属性字典
    {'href': 'http://diveintomark.org/', 'type': 'text/html', 'rel': 'alternate'}
    >>> root[3] # 第4个子元素updated
    <Element '{http://www.w3.org/2005/Atom}updated' at 0x7fc09da09598>
    >>> root[3].attrib # updated没有属性，所以是个空字典
    {}
    >>> root[4].attrib['href'] # 和字典操作一样，获取对应的属性值
    'http://diveintomark.org/'

**XML查找结点**

许多情况下，我们需要找到XML中特点的元素。

    >>> root.findall('{http://www.w3.org/2005/Atom}entry') # findall()方法可以查找匹配的子元素
    [<Element '{http://www.w3.org/2005/Atom}entry' at 0x7fc09da09688>, <Element '{http://www.w3.org/2005/Atom}entry' at 0x7fc09da09b38>, <Element '{http://www.w3.org/2005/Atom}entry' at 0x7fc09da09ef8>]
    >>> root.tag
    '{http://www.w3.org/2005/Atom}feed'
    >>> root.findall('{http://www.w3.org/2005/Atom}feed') # 每个元素都有findall()方法，但查询只会搜索其子元素，根元素feed中不存在feed的子元素，所以为空列表
    []
    >>> root.findall('{http://www.w3.org/2005/Atom}author') # author虽然有，但它是entry的子元素
    []
    >>> tree.findall('{http://www.w3.org/2005/Atom}entry') # 对象tree(etree.parse()返回值)中一些方法是根元素方法的镜像，和tree.getroot().findall()返回值一样
    [<Element '{http://www.w3.org/2005/Atom}entry' at 0x7fc09da09688>, <Element '{http://www.w3.org/2005/Atom}entry' at 0x7fc09da09b38>, <Element '{http://www.w3.org/2005/Atom}entry' at 0x7fc09da09ef8>]
    >>> tree.findall('{http://www.w3.org/2005/Atom}author') # 和tree.getroot().findall结果一样
    []
findall()匹配所有元素，find()方法只返回第一个匹配元素

    >>> entries = tree.findall('{http://www.w3.org/2005/Atom}entry')# 查找元素赋给entries
    >>> len(entries)
    3
    >>> title_element = entries[0].find('{http://www.w3.org/2005/Atom}title') # find()方法使用ElementTree作为参数,返回第一个匹配的元素
    >>> title_element.text
    'Dive into history, 2009 edition'
    >>> foo_element = entries[0].find('{http://www.w3.org/2005/Atom}foo')
    >>> foo_element
    >>> type(foo_element) # entries[0]没有foo元素，返回None
    <class 'NoneType'>

ElementTree元素对象如果不包含子元素，其值被认为False(即len(element)为0).if element.find('...')并非在测试是否find()方法找到匹配项，而是在判断元素是否包含子元素。想要判断是否包含要查找的子元素，需要使用if element.find('...') is not None

可以在所以派生元素中搜索，即任意嵌套层次的子元素、孙子元素...

    >>> all_links = tree.findall('.//{http://www.w3.org/2005/Atom}link') # .//指在任意嵌套层次查找
    >>> all_links
    [<Element '{http://www.w3.org/2005/Atom}link' at 0x7fc09da09638>, <Element '{http://www.w3.org/2005/Atom}link' at 0x7fc09da098b8>, <Element '{http://www.w3.org/2005/Atom}link' at 0x7fc09da09d18>, <Element '{http://www.w3.org/2005/Atom}link' at 0x7fc09da0c098>]
    >>> all_links[0].attrib # 直接子元素的link
    {'href': 'http://diveintomark.org/', 'type': 'text/html', 'rel': 'alternate'}
    >>> all_links[1].attrib # 子元素entry子元素link
    {'href': 'http://diveintomark.org/archives/2009/03/27/dive-into-history-2009-edition', 'type': 'text/html', 'rel': 'alternate'}                                                           
    >>> all_links[2].attrib                                                                     
    {'href': 'http://diveintomark.org/archives/2009/03/21/accessibility-is-a-harsh-mistress', 'type': 'text/html', 'rel': 'alternate'}                                                        
    >>> all_links[3].attrib
    {'href': 'http://diveintomark.org/archives/2008/12/18/give-part-1-container-formats', 'type': 'text/html', 'rel': 'alternate'}

ElementTree的findall()方法是其一个非常强大的特性,但它的查询方式有些出乎意料，“有限的XPath支持"  XPath是一种用于查询XML文档的W3C标准。另外一个第三方库对ElementTree的API进行了扩展，提供了对XPath的全面支持。

**LXML**

lxml是一个开源的第三方库，以流行的libxml2解析器为基础开发。它提供了对XPath1.0的全面支持。

    >>> from lxml import etree # 导入lxml，和ElementTree提供相同的API
    >>> tree  = etree.parse('feed.xml') # parse函数和ElementTree
    >>> root = tree.getroot() # 相同
    >>> root.findall('{http://www.w3.org/2005/Atom}entry') # 相同
    [<Element {http://www.w3.org/2005/Atom}entry at 0x7fc09da04b48>, <Element {http://www.w3.org/2005/Atom}entry at 0x7fc09da04a08>, <Element {http://www.w3.org/2005/Atom}entry at 0x7fc09bd92ec8>]

对应大型的xml文件，lxml明显比内置的ElementTree快了许多。如果现在只用到了ElementTree的API，并且想要使用最快的实现，可以尝试导入lxml。

比如
    try:
        from lxml import etree
    except ImportError:
        import xml.etree.ElementTree as etree
这种方法同样适用于其他备选模块的方法

lxml不只是一个更快速的ElementTree,它的findall()方法能够支持更加复杂的表达式。

    >>> import lxml.etree # 直接导入了lxml.etree，强调这些特性只限于lxml
    >>> tree = lxml.etree.parse('feed.xml')
    >>> tree.findall('.//{http://www.w3.org/2005/Atom}*[@href]')# 查找整个文档范围内搜索命名空间Atom中具有href属性的元素 {http://www.w3.org/2005/Atom}指示"搜索范围仅在命名空间Atom中。”*表示“任意本地名的元素”[@href]表示含有href属性“
    [<Element {http://www.w3.org/2005/Atom}link at 0x7fc09bd99088>, <Element {http://www.w3.org/2005/Atom}link at 0x7fc09bd99108>, <Element {http://www.w3.org/2005/Atom}link at 0x7fc09bd990c8>, <Element {http://www.w3.org/2005/Atom}link at 0x7fc09bd92f08>]
    >>> tree.findall(".//{http://www.w3.org/2005/Atom}*[@href='http://diveintomark.org/']") # 查找所有包含href属性并且值为"http://diveintomark.org/"的Atom元素
    [<Element {http://www.w3.org/2005/Atom}link at 0x7fc09bd99088>]
    >>> NS = '{http://www.w3.org/2005/Atom}'
    >>> tree.findall('.//{NS}author[{NS}uri]'.format(NS=NS)) #搜索命名空间Atom中包含uri元素作为子元素的author元素。该语句只返回第一个和第二个entry元素中的author元素，最后的entry元素没有uri 
    [<Element {http://www.w3.org/2005/Atom}author at 0x7fc09bd991c8>, <Element {http://www.w3.org/2005/Atom}author at 0x7fc09bd99048>]

lxml集成了对任意XPath1.0表达式的支持

    >>> import lxml.etree
    >>> tree = lxml.etree.parse('feed.xml')
    >>> NSMAP = { 'atom': 'http://www.w3.org/2005/Atom'} # 要查询命名空间的元素，定义一个命名空间前缀映射。
    >>> entries = tree.xpath(".//atom:category[@term='accessibility']/..", namespaces=NSMAP) #  XPath查询请求。这个XPath表达式目的在于搜索category元素，并且该元素包含值为accessibility的term属性”/.."意思是返回找到的category元素的父元素。这条语句会找到所有包含<category term = 'accessibility'>作为子元素的条目
    >>> entries # xpath()函数返回一个ElementTree对象列表
    [<Element {http://www.w3.org/2005/Atom}entry at 0x7fc09bd99188>] 
    >>> entry = entries[0]
    >>> entry.xpath('./atom:title/text()', namespaces=NSMAP) # XPath表达式并总是返回一个元素列表。一个解析了的xml文档的DOM模型并不包含元素；只包含结点。结点可以是元素，属性，甚至是文本内容。XPath查询的结果是一个结点列表。当前查询返回一个文本结点列表：title元素(atom:title)的文本内容（text()),并且title元素必须是当前元素的子元素(./)

**生成XML**

python同样可以创建xml文档

    >>> import xml.etree.ElementTree as etree 
    >>> new_feed = etree.Element('{http://www.w3.org/2005/Atom}feed', # 实例化Element类创建一个新元素。将元素的名字(命名空间+本地名)作为参数。
    attrib = {'{http://www.w3.org/XML/1998/namespace}lang':'en'}) # 将属性名和值构成的字典传递给attrib参数
    >>> print(etree.tostring(new_feed)) 
    b'<ns0:feed xmlns:ns0="http://www.w3.org/2005/Atom" xml:lang="en" />'
    ['Accessibility is a harsh mistress']

内置的ElementTree库没有提供细粒度地对序列化时命名空间内元素的控制，但是lxml有这样的功能。

    >>> import lxml.etree 
    >>> NSMAP = {None: 'http://www.w3.org/2005/Atom'} # 首先，定义一个用于命名空间映射的字典对象,使用None前缀来定义默认的命名空间
    >>> new_feed = lxml.etree.Element('feed', nsmap=NSMAP) # 我们创建元素的时候，给lxml专有的nsmap参数传值，并且lxml会参照我们定义的命名空间前缀
    >>> print(lxml.etree.tounicode(new_feed))
    <feed xmlns="http://www.w3.org/2005/Atom"/>
    >>> new_feed.set('{http://www.w3.org/XML/1998/namespace}lang', 'en')# 使用set方法随时给元素添加所需属性
    >>> print(lxml.etree.tounicode(new_feed))
    <feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en"/>

    >>> title = lxml.etree.SubElement(new_feed, 'title', attrib={'type':'html'}) # 给已有元素创建子元素，实例化SubElement类，两个参数，父元素(new_feed)和子元素的名字
    >>> print(lxml.etree.tounicode(new_feed))；# 传递属性字典进去
    <feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en"><title type="html"/></feed>
    >>> title.text = 'dive into &hellip;'
    >>> print(lxml.etree.tounicode(new_feed))
    <feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en"><title type="html">dive into &amp;hellip;</title></feed>
    # 新创建title元素在Atom命名空间中，并作为子元素插入到feed元素中。设定元素的文本内容，只需设定其.text属性；当前title元素序列化时就使用了其文本内容，任何包含<或则&符号的内容在序列化时都需要转义
    >>> print(lxml.etree.tounicode(new_feed, pretty_print=True)
    ... )
    <feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en">
      <title type="html">dive into &amp;hellip;</title>
    </feed>
    "pretty_print=True,"会在每个结束的末尾或含义子元素但没有文本内容的末尾添加换行符

**解析损坏的XML**

不再说明了，尽量保证xml格式符合标准吧



