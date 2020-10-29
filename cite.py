#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:05:13 2020

@author: cx
"""

from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

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
         'ref': 'Sabour, Sara et al. “Adversarial Manipulation of Deep Representations.” CoRR abs/1511.05122 (2016): n. pag.'}
    '''
    
    def phrase_bibtex(self, bibtex):
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
    
        return phrase
    
    def dig_ref(self, title):
        pass
        
    
        