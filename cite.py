#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:05:13 2020

@author: cx
"""

from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import numpy as np
from bs4 import BeautifulSoup 

'''
manage papers and dig papers ref network
'''

class Cite():
    def __init__(self):
        chrome_options=Options()
        chrome_options.add_argument('--headless')
        #self.browser = webdriver.Chrome(options=chrome_options)
        chrome_path = 'D:/迅雷下载/chromedriver_win32/chromedriver.exe'
        self.browser = webdriver.Chrome(chrome_path)

    
    '''
    search papertitle on semanticscholar, return paper_ref_format and paper_bibtex(latex format)
    
    ##############################################################################################
    cite = Cite()
    title = “Adversarial Manipulation of Deep Representations.”
    ref, bibtex = get_cite(title)
    
    return 
            ref:Sabour, Sara et al. “Adversarial Manipulation of Deep Representations.” CoRR abs/1511.05122 (2016): n. pag.
            bibtex:@article{Sabour2016AdversarialMO,
                  title={Adversarial Manipulation of Deep Representations},
                  author={Sara Sabour and Yanshuai Cao and Fartash Faghri and David J. Fleet},
                  journal={CoRR},
                  year={2016},
                  volume={abs/1511.05122}
                }
    ##############################################################################################

    '''
    
    # def get_cite(self, title):
    #     #browser = webdriver.Chrome()
    #     self.browser.get('https://www.semanticscholar.org')
    #     input_ = self.browser.find_element_by_xpath('//*[@id="search-form"]/div/div/input')
    #     input_.send_keys(title)#传送入关键词
    #     button1 = self.browser.find_element_by_xpath('//*[@id="search-form"]/div/div/button/div/span')
    #     button1.click()
    #     time.sleep(5)
    #     button2 = self.browser.find_element_by_xpath("//span[text()='Cite']")
    #     button2.click()
    #     bibtex = self.browser.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/div[1]/div[2]/cite')
    #     bibtex = bibtex.text
    #     button3 = self.browser.find_element_by_xpath('//*[@id="app"]/div[1]/div/div/div[1]/div[1]/ul/li[2]/button')
    #     button3.click()
    #     p_s = self.browser.find_element_by_xpath('//*[@id="app"]/div[1]/div/div/div[1]/div[2]/cite')
    #     ref =  p_s.text
    #     return ref, bibtex
    
    def clean_bibtex(self, bibtex):
        mood = ['{', '}', '\n']
        for i in mood:
            bibtex = bibtex.replace(i, '')
        return bibtex
    
    def search_cite_one_time(self, title):
        input_box = self.browser.find_element_by_xpath('//*[@id="search-form"]/div/div/input')
        input_box.send_keys(Keys.CONTROL, 'a')
        input_box.send_keys(title)
        self.browser.find_element_by_xpath('//*[@id="search-form"]/div/div/button/div/span').click()
        time.sleep(5)
        button2 = self.browser.find_element_by_xpath("//span[text()='Cite']")
        button2.click()
        bibtex = self.browser.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/div[1]/div[2]/cite')
        bibtex = bibtex.text
        button3 = self.browser.find_element_by_xpath('//*[@id="app"]/div[1]/div/div/div[1]/div[1]/ul/li[2]/button')
        button3.click()
        p_s = self.browser.find_element_by_xpath('//*[@id="app"]/div[1]/div/div/div[1]/div[2]/cite')
        ref =  p_s.text
        self.browser.find_element_by_xpath('//*[@id="app"]/div[1]/div/div/div[2]/button/span').click()
        return ref, bibtex
        
        
        
    '''
    phrase bibtex to convert dict format, and make use through panda.DataFrame
    
    input:
          article{Sabour2016AdversarialMO,
          title={Adversarial Manipulation of Deep Representations},
          author={Sara Sabour and Yanshuai Cao and Fartash Faghri and David J. Fleet},
          journal={CoRR},
          year={2016},
          volume={abs/1511.05122}
        }
    output:
        {'id': '@articleSabour2016AdversarialMO',
         'title': 'Adversarial Manipulation of Deep Representations',
         'author': ['Sara Sabour', 'Yanshuai Cao', 'Fartash Faghri', 'David J. Fleet'],
         'journal': 'CoRR',
         'year': '2016',
         'volume': 'abs/1511.05122',
         'ref': 'Sabour, Sara et al. “Adversarial Manipulation of Deep Representations.” CoRR abs/1511.05122 (2016): n. pag.'
         'ref_paper': ''}
    '''
    
    def parse_bibtex(self, ref, bibtex):
        '''
 
        Parameters
        ----------
        ref : TYPE
            DESCRIPTION.
        bibtex : TYPE
            DESCRIPTION.

        Returns
        -------
        parse : TYPE
            DESCRIPTION.
            
        ['id', 'year', 'title', 'ref_papers', 'ref', 'author']
        '''
        parse = {}
        bibtex = self.clean_bibtex(bibtex)
        split_bib = bibtex.split(',  ')
        keys = ['id']
        values = [split_bib[0]]
        for item in split_bib[1:]:
            a,b = item.split('=')
            keys.append(a)
            values.append(b)
        tmp_parse = dict(zip(keys, values))
        parse['author'] = [i for i in tmp_parse['author'].split('and')]
        parse['ref'] = ref
        parse['title'] = tmp_parse['title']
        parse['year'] = tmp_parse['year']
        #parse['journal'] = tmp_parse['journal']
        #parse['volume'] = tmp_parse['volume']
        parse['id'] = tmp_parse['id']

        
        return parse
    
    def delay_do(self, browser, x_path):
        try:
            do = browser.find_element_by_xpath(x_path)
            state = 0
            return do, state
        except:
            state = 1
            return None, state
    
    def excute_action(self, browser, x_path):
        end_time = 10
        do, state = self.delay_do(browser, x_path)
        while(state and end_time>0):
           do, state = self.delay_do(browser, x_path)
           time.sleep(1)
           end_time = end_time-1
        return do
    
    
    def dig_onepaper_title(self, title, mode='ref'):
        paper_titles = []
        loop =True
        while(loop):
            try:
                self.browser.get('https://www.semanticscholar.org')
                loop = False
            except:
                self.browser.quit()
                loop = True
                self.__init__()

        input_ = self.browser.find_element_by_xpath('//*[@id="search-form"]/div/div/input')
        input_.send_keys(title)#传送入关键词
        button1 = self.browser.find_element_by_xpath('//*[@id="search-form"]/div/div/button/div/span')
        button1.click()
        button2 = self.excute_action(self.browser, '//*[@id="main-content"]/div[1]/div/div[1]/a')
        button2.click()
        before_text = ''
        while(1):
            unload_flag = True#check if cl_paper_title loads
            while(unload_flag):
                time.sleep(1)
                if mode == 'ref':
                    block = self.excute_action(self.browser,'//*[@id="references"]')
                if mode == 'cite':
                    block = self.excute_action(self.browser,'//*[@id="citing-papers"]')
                if block == None:
                    break
                bf = BeautifulSoup(block.get_attribute('innerHTML'), "html.parser")
                p_s = bf.find_all('div', class_ ='cl-paper-title')
                paper_titles.extend([i.text for i in p_s])
                unload_flag = p_s[0].text == before_text
                before_text = p_s[0].text
            time.sleep(3)
            if p_s == None:
                    break
            if len([i.text for i in p_s])<10 or len(self.browser.find_elements_by_link_text("›"))==1:
                break
            if mode=='ref':
                button3 = self.browser.find_elements_by_link_text("›")[-1]
            else:
                button3 = self.browser.find_elements_by_link_text("›")[0]
            self.browser.execute_script("arguments[0].click();", button3)
        return paper_titles
    
    def dig_onepaper_refs_standard(self, ref_titles):
        parse = []
        failures = []
        for idx in range(len(ref_titles)):
            try:
                ref, bibtex = self.search_cite_one_time(ref_titles[idx])
                parse.append(self.parse_bibtex(ref, bibtex))
                time.sleep(1)
            except:
                failures.append(idx)
        #parse = parse.extend(self.enhance_refs(ref_titles, failures))
        return parse
    
    
    def download_from_arxiv(self, title):
    
        def get_bs(target):
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
            headers = {'User-Agent':user_agent}
            target=target.format(1)
            req=requests.get(url=target)
            html=req.text
            html=html.replace('<br>',' ').replace('<br/>',' ').replace('/>','>')
            bs=BeautifulSoup(html,"html.parser")
            return bs
        
        def getFile(title, url):
            from win32com.client import Dispatch
            import shutil
            import os
            
            thunder = Dispatch('ThunderAgent.Agent64.1')
            thunder.AddTask(url, title)
            time.sleep(0.5)
            thunder.CommitTasks()
            
            loop = True
            while(loop):
                try:
                    downloadRoot = 'D:\迅雷下载'
                    files = os.listdir(downloadRoot)
                    for file in files:
                        if file.endswith('.pdf'):
                            src_path = os.path.join(downloadRoot, file)
                            dst_path = os.path.join('./download_papers', file)
                    shutil.move(src_path, dst_path)
                    loop = False
                except:
                    time.sleep(2)
                    loop = True
            
            
            
        
        import requests
        url = 'https://arxiv.org/search/?query={}&searchtype=all&source=header'.format(title.replace(' ' , '+'))
        bs = get_bs(url)
        texts = bs.find_all('li', class_ = 'arxiv-result')
        pdf_url = texts[0].find('span').a['href'] 
        pdf_url = pdf_url[:8]+'export.'+pdf_url[8:]
        getFile(title+'.pdf', pdf_url)
                

        
        