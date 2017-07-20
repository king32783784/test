#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = '李鹏'
SITENAME = '路漫求索'
SITEURL = 'http://king32783784.github.io'
SITESUBTITLE= '生活不止眼前的苟且，还有诗和远方 <a href="pages/aboutme.html">More...</a>'
TIMEZONE = 'Asia/Shanghai'
PATH = 'content'


DEFAULT_LANG = u'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/atom.xml'
FEED_ALL_RSS = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
# LINKS =  ()


# Share
SHARE = True

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)
SOCIAL = (
        #    ('Twitter', 'https://twitter.com/derwinlu'),
        #    ('Bitbucket', 'https://bitbucket.org/winlu'),
            ('GitHub', 'https://github.com/king32783784'),
        #    ('Google+', 'https://plus.google.com/115771807029208924055'),
             ('RSS', SITEURL + '/' + FEED_ALL_ATOM),
            ('EMAIL', 'mailto:peng.li@i-soft.com.cn'),
          )

#sitelogo
SITELOGO = 'sitelogo.png'
SITELOGO_SIZE = '200'
HIDE_SITENAME = True



#DEFAULT_PAGINATION = 5

#static
STATIC_PATHS = ['images',
                'static',
                'extra/sitelogo.png',
                'extra/favicon.ico',
                'extra/favicon.png',
                'extra/robots.txt',
                'extra/google331456191962689c',
                'extra/CNAME']
EXTRA_PATH_METADATA = {
                        'extra/sitelogo.png': {'path': 'sitelogo.png'},
                        'extra/robots.txt': {'path': 'robots.txt'},
                        'extra/favicon.ico': {'path': 'favicon.ico'},
                        'extra/favicon.png': {'path': 'favicon.png'},
                      }

#theme
#THEME = 'lightweight' #01
#THEME = 'waterspill' #02 
#THEME = 'bootstrap2' #03
#THEME = 'brownstone' #04 *
#THEME = 'pure' #05 *
#THEME = 'plumage' #06 
#THEME = 'pelican-cait' #07 *
THEME = 'pelican-twitchy' #08
#THEME = 'pelican-sober' #09
#THEME = 'voidy-bootstrap' #10
BOOTSTRAP_THEME = 'sandstone'
PYGMENTS_STYLE = 'colorful'



DATE_FORMATS = {
    'zh': '%Y-%m-%d %a'
}
RELATIVE_URLS = True

DISQUS_SITENAME = "king32783784"

#ARTICLE_DIR = 'posts'
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

#DEFAULT_CATEGORY = u'其他'

#PAGE_DIR = 'pages'
#PAGE_URL = 'pages/{slug}.html'
#PAGE_SAVE_AS = 'pages/{slug}.html'
#DISPLAY_PAGES_ON_MENU = True
#DISPLAY_CATEGORIES_ON_MENU = True
#TAGLINE=True

#paths
#PAGE_SAVE_AS = ''
#AUTHOR_SAVE_AS = ''
#AUTHORS_SAVE_AS = ''


DISQUS_SITENAME=False
DUOSHUO_SITENAME=True
DASHANG=True
ALIPAY="https://raw.githubusercontent.com/king32783784/king32783784.github.io/master/tmpfile/wechart.png"

#
DISPLAY_PAGES_ON_MENU = True

#

GITHUB_URL = 'http://github.com/king32783784'
TWITTER_URL = ''
WEIBO_URL = ''
DOUBAN_URL = ''
FACEBOOK_URL = ''
GOOGLEPLUS_URL = ''

PLUGIN_PATHS = 'plugins'
PLUGINS = [
          'bootstrapify',
          'pelican_plugin-render_math',
          'autopages',
          'latex', 
          'tipue_search',
          'gravatar',
          'assets',
          'tag_cloud',
          'sitemap',
          'pelican-toc',
          'category_order',
          'pelican_comment_system',
          'pelican-genealogy',
          'libravatar',
          'pin_to_top',
          'better_code_samples',
          'summary',
          'static_comments',
          'simple_footnotes',
          'pelican-open_graph',
          'headerid',
          'pelican-jinja2content',
          'pelican_javascript',
          'series',
          'bootstrapify',
          "render_math",
           'extract_toc',
          'feed_summary',
          ]
pin_to_top = {
    'pin':True
}
LATEX = 'article'


#sitemap settings
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.6,
        'pages': 0.3
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

DELETE_OUTPUT_DIRECTORY = True      # 编译之前删除output目录，这样保证output下生成的内容是干净的
# test

SURNAME_URL = '{slug}'
SURNAME_SAVE_AS = '/surnames/{slug}.html'
PERSON_URL = '{slug}'
PERSON_SAVE_AS = '/people/{slug}.html'


#menu
DISPLAY_RECENT_POSTS_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_PAGES_ON_MENU = True
#DISPLAY_TAGS_ON_MENU = True
EXPAND_LATEST_ON_INDEX = True

#tag cloud
#TAG_CLOUD_STEPS = 3
#TAG_CLOUD_MAX_ITEMS = 20

#Cookie Consent
COOKIE_CONSENT = True

#license
#CC_LICENSE = "CC-BY-NC-SA"
#CC_ATTR_MARKUP = True

#Markdown
MD_EXTENSIONS = ['codehilite(css_class=highlight)','extra']

#Cache
CACHE_CONTENT = False

#Open Graph
OPEN_GRAPH = True
OPEN_GRAPH_IMAGE = "favicon.png"
                                                   
