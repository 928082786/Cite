#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:05:13 2020

@author: cx
"""

from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import re
import numpy as np
from bs4 import BeautifulSoup 

'''
manage papers and dig papers ref network
'''

class Cite():
    def __init__(self):
        pass
    
    '''
    search papertitle on semanticscholar, return paper_ref_format and paper_bibtex(latex format)
    
    ##############################################################################################
    cite = Cite()
    title = “Adversarial Manipulation of Deep Representations.”
    ref, bibtex = cite(title)
    
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
    
    def get_cite(self, title):
        chrome_options=Options()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(options=chrome_options)
        #browser = webdriver.Chrome()
        browser.get('https://www.semanticscholar.org')
        input_ = browser.find_element_by_xpath('//*[@id="search-form"]/div/div/input')
        input_.send_keys(title)#传送入关键词
        button1 = browser.find_element_by_xpath('//*[@id="search-form"]/div/div/button/div/span')
        button1.click()
        time.sleep(5)
        button2 = browser.find_element_by_xpath('//*[@id="main-content"]/div[1]/div/div[1]/div[2]/div[2]/div[4]/button/span[2]')
        button2.click()
        bibtex = browser.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/div[1]/div[2]/cite')
        bibtex = bibtex.text
        button3 = browser.find_element_by_xpath('//*[@id="app"]/div[1]/div/div/div[1]/div[1]/ul/li[2]/button')
        button3.click()
        p_s = browser.find_element_by_xpath('//*[@id="app"]/div[1]/div/div/div[1]/div[2]/cite')
        ref =  p_s.text
        browser.quit()
        return ref, bibtex
    
    def clean_bibtex(self, bibtex):
        mood = ['{', '}', '\n']
        for i in mood:
            bibtex = bibtex.replace(i, '')
        return bibtex
    
    
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
    
    def phrase_bibtex(self, ref, bibtex):
        bibtex = self.clean_bibtex(bibtex)
        split_bib = bibtex.split(',')
        keys = ['id']
        values = [split_bib[0]]
        for item in split_bib[1:]:
            a,b = item.split('=')
            keys.append(a.strip())
            values.append(b)
        phrase = dict(zip(keys, values))
        phrase['author'] = [i.strip() for i in phrase['author'].split('and')]
        phrase['ref'] = ref
        phrase['ref_papers'] = ''
        return phrase
    
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
    
    def dig_ref(self, title):
        ref_titles = []
        chrome_options=Options()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(options=chrome_options)
        #browser = webdriver.Chrome()
        browser.get('https://www.semanticscholar.org')
        input_ = browser.find_element_by_xpath('//*[@id="search-form"]/div/div/input')
        input_.send_keys(title)#传送入关键词
        button1 = browser.find_element_by_xpath('//*[@id="search-form"]/div/div/button/div/span')
        button1.click()
        button2 = self.excute_action(browser, '//*[@id="main-content"]/div[1]/div/div[1]/a')
        button2.click()
        while(1):
            time.sleep(3)
            ref = browser.find_element_by_xpath('//*[@id="references"]/div[2]')
            bf = BeautifulSoup(ref.get_attribute('innerHTML'), "html.parser")
            ref = bf.find_all('div', class_ ='cl-paper-title')
            ref_titles.extend([i.text for i in ref])
            if len(ref)<10:
                break
            button3 = browser.find_element_by_xpath('//*[@id="references"]/div[2]/div/div[3]/ul/li[4]/a')
            time.sleep(3)
            browser.execute_script("arguments[0].click();", button3)
        browser.quit()
        return ref_titles
    