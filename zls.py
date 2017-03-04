#! /usr/bin/env python
#coding=utf-8


import urllib2
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

_page = 10 #抓取页数

def get_page_html(page): #读取指定某页源代码
    html_url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?in=160400%3B160000%3B160500%3B160200%3B300100%3B160100%3B160600&jl=%E8%8B%8F%E5%B7%9E&p=1&isadv=0'+str(page)
    html=urllib2.urlopen(html_url).read()
    return html

def get_url(html): #从源代码中解析出url
    pattern_start=re.compile('par="ssidkey=y&amp;ss=201&amp;ff=03" href="') #url开始标记
    pattern_end=re.compile('" target="_blank') #url结束标记
    split1=pattern_start.split(html)
    global url_save #用于存储解析出的url
    url_save=[]
    for link in split1[1:-1]: #跳过第一段split
        url_get=pattern_end.split(link)
        if re.search('http://jobs.zhaopin.com/',url_get[0]):#再次验证结果:
            url_save.append(url_get[0])
    #无须return，因为url_save已经被global
    return 0



def read_url(url,cnt1,cnt2): #读取url内容，写入get_constent.txt
    try:
        constent_all=urllib2.urlopen(url).read() #获取页面源代码
    except:
        constent_all=''
    finally:
        #获取信息流
        pattern_strat=re.compile('<!-- SWSStringCutStart -->')
        pattern_end=re.compile('<!-- SWSStringCutEnd -->')
        constent_get=pattern_strat.split(constent_all)
        constent_get=pattern_end.split(constent_get[-1])
        
        pattern_start=re.compile(' <ul class="terminal-ul clearfix">')
        pattern_end=re.compile('<div class="terminalpage-main clearfix">')
        constent_get2=pattern_start.split(constent_all)
        constent_get2=pattern_end.split(constent_get2[-1])

        
        pattern_start=re.compile('<title>【')
        pattern_end=re.compile('】 - 智联招聘</title>')
        constent_title=pattern_start.split(constent_all)
        constent_title=pattern_end.split(constent_title[-1])

        pattern_start=re.compile('var Str_CompName = "')
        pattern_end=re.compile('var tjUrl =')
        constent_cname=pattern_start.split(constent_all)
        constent_cname=pattern_end.split(constent_cname[-1])

    
        #将信息流转化为独立的句子,并写入文本
        
        fw=open('get_info.txt','a')
        fw2=open('get_job.txt','a')
        fu=open('save_url.txt','a')
        
        if re.search(re.compile('style'),constent_get[0]):
            cnt2 += 1
        else:
            split_pattern=re.compile('<P>|</P>|<p>|</p>|<BR>|<br/>|<br />|<br>')  #格式化获得的信息
            split_pattern2=re.compile('</span>|<strong>|</a></strong></li>|<li><span>|</span><strong>|</ul>|<a target="_blank" href="http://jobs.zhaopin.com/suzhou/sj\d+/">')
            #此命令处理句子间格式
            
            con_0=re.split(split_pattern,constent_get[0])
            con_1=re.split(split_pattern2,constent_get2[0])
            title=re.split('',constent_title[0])
            companyname=re.split('',constent_cname[0])
            fu.write(url+'\n')

            for line in title:
                fw.write('\n'+line+'\n')
            #fw2.write('标题：'+line+'\t')
            for line in companyname:
               write_constentline=line.replace(' ','').replace(';','').replace('"','').replace('\n','\t')
               fw2.write(write_constentline)
               break
            for line in con_0:
                write_constent = line.replace('&nbsp;','').replace('\n','').replace('\r','').replace('\t','').replace(' ','')#处理句内字符
                if len(write_constent):
                    fw.write(write_constent)
            for line in con_1:
                write_constent2 = line.replace('&nbsp;','').replace('\n','').replace('\r','').replace('\t','').replace(' ','').replace('</a>-','').replace('<ahref="http://www.zhaopin.com/gz_suzhou/"target="_blank"title="苏州工资计算器"><imgsrc="http://jobs.zhaopin.com/images/calculator.png"alt="苏州工资计算器"/>','').replace('<atarget="_blank"href="http://www.zhaopin.com/suzhou/">','').replace('<spanid="span4freshdate">','').replace('</strong></li>','\t').replace('/月','/月\t').replace('面议','面议\t').replace('职位月薪：','').replace('工作地点：','').replace('发布日期：','').replace('工作性质：','').replace('工作经验：','').replace('最低学历：','').replace('招聘人数：','').replace('职位类别：','').replace('苏州20','苏州 20')#处理句内字符
                if len(write_constent2):
                    fw2.write(write_constent2)
            cnt1 += 1
            print '正在解析第',cnt1,'条数据'
            fw.write('\n\n\n')
            fw2.write('\n')
        return cnt1,cnt2

#-------------------------主程序开始-------------------------


#读取url_save，解析其中招聘信息，存储在get_constent.txt中

fc=open('get_info.txt','w') #新建get_info.txt,存储得到的信息。
fc.close()
fc2=open('get_job.txt','w')
fc2.close()
fu = open('save_url.txt','w')
fu.close()

global count1 #统计解析数据
global count2 #统计未解析数据
count1 = 0
count2 = 0

for p in range(_page):
    html = get_page_html(p)
    re1 = get_url(html)
    for url in url_save:
        count1,count2 = read_url(url,count1,count2) #解析某一url内容

count_text = '共解析 ' + str(count1) + ' 条数据'
count_text2 = '未解析 ' + str(count2) + ' 条有格式数据'
print count_text.encode('utf-8')
print count_text2.encode('utf-8')
