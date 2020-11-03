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
        self.browser = webdriver.Chrome()

    
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
        do, state = self.delay_do(browser, x_path)
        while(state):
           do, state = self.delay_do(browser, x_path)
           time.sleep(1)
        return do
    
    
    def dig_onepaper_refs_title(self, title):
        ref_titles = []
        self.browser.get('https://www.semanticscholar.org')
        input_ = self.browser.find_element_by_xpath('//*[@id="search-form"]/div/div/input')
        input_.send_keys(title)#传送入关键词
        button1 = self.browser.find_element_by_xpath('//*[@id="search-form"]/div/div/button/div/span')
        button1.click()
        button2 = self.excute_action(self.browser, '//*[@id="main-content"]/div[1]/div/div[1]/a')
        button2.click()
        while(1):
            before_text = ''
            unload_flag = True#check if cl_paper_title loads
            while(unload_flag):
                time.sleep(1)
                ref = self.excute_action(self.browser,'//*[@id="references"]/div[2]')
                bf = BeautifulSoup(ref.get_attribute('innerHTML'), "html.parser")
                ref = bf.find_all('div', class_ ='cl-paper-title')
                ref_count = bf.find('div', class_='citation-list__label')
                ref_titles.extend([i.text for i in ref])
                unload_flag = ref[0].text == before_text
                before_text = ref[0].text
            time.sleep(2)
            if len([i.text for i in ref])<10 or len(self.browser.find_elements_by_link_text("›"))==1:
                break
            button3 = self.browser.find_elements_by_link_text("›")[-1]
            self.browser.execute_script("arguments[0].click();", button3)
        return ref_titles
    
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
