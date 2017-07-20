# -*- coding: utf-8 -*-
'''
Created on Thu Jul 20 14:35:40 2017

@author: sande
'''

#importing libraries
from nltk.corpus import stopwords
import re
from collections import Counter  
import string 
from nltk.tokenize import word_tokenize
from time import sleep
import gensim
import csv
import requests, bs4
import textacy
from gensim.models import Word2Vec

each_review=[]
total_reviews=[] 

#Webscraping of amazon reviews for Asus Chromebook with 1 and 2 star reviews alone
for i in range(1,13):
#https://www.amazon.com/Chromebook-Rockchip-Pearl-White-Light/product-reviews/B01EGBAQXY/ref=cm_cr_dp_d_hist_1?ie=UTF8&filterByStar=one_star&reviewerType=avp_only_reviews
#https://www.amazon.com/Chromebook-Rockchip-Pearl-White-Light/product-reviews/B01EGBAQXY/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&filterByStar=one_star&reviewerType=avp_only_reviews&pageNumber=1    
    baseurl='https://www.amazon.com/Chromebook-Rockchip-Pearl-White-Light/product-reviews/B01EGBAQXY/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&filterByStar=one_star&reviewerType=avp_only_reviews&pageNumber={}'.format(i)
    #sleep(5)
    page=requests.get(baseurl)
    sleep(5)
    page.raise_for_status()
    result = bs4.BeautifulSoup(page.content,'html.parser')
    #result.prettify()
        
    for reviews in result.find_all('div',{'class':'a-section a-spacing-none review-views celwidget'}):
        all_reviews=reviews.find_all('span',{'a-size-base review-text'})
        #print(all_reviews)
    each_review=[each_review.text for each_review in all_reviews]  
    total_reviews.extend(each_review)
    
    with open('amazon.txt','w') as file:
        for line in total_reviews:            
            file.write(line+'\n\n')
        file.close()

#Reading from the saved file and preprocessing of texts
with open('amazon.txt','r') as f:
    words=nltk.word_tokenize(f.read().lower())
       
    words1=[]
    words2=[]
    for w in words:
        if w not in stops and len(w) > 1:
            words1.append(w)
    addition_words=['asus','update','chromebook','n\'t','one','time','would','work','s','get']
    for word in words1:
        if word not in addition_words:
            words2.append(word)
    
    #Using Textacy library for easy preprocessing  
    tok_word=textacy.preprocess.preprocess_text(str(words2),no_punct=True,no_numbers=True,no_currency_symbols=True,no_accents=True)
    tok_word=re.sub('NUMBER','',tok_word)
    tok_word=nltk.word_tokenize(tok_word)
    lemmtok_words=[]
    for word in tok_word:        
        lemmtok_words.append(WordNetLemmatizer.lemmatize(word))
    lemmtok_words_new=[nltk.word_tokenize(sent) for sent in lemmtok_words]
    
    #Usage of word2Vec model
    model=gensim.models.Word2Vec(lemmtok_words_new,min_count=1,size=32)
    model.most_similar('chrome')
    lemmtok_words_new=Counter(lemmtok_words_new)
    lemmtok_words_new.most_common(50)
    sorted(lemmtok_words_new,key=lemmtok_words_new.get)[:50]
    #keylist=summarize(str(total_reviews))
    #keywords(keylist)   

    #Getting the most similar words from the top 50 frequent words 
    most_similar_words=[]
    for i in sorted(lemmtok_words_new,key=lemmtok_words_new.get,reverse=True)[:50]:
        if len(i) > 2:
            most_similar_words.append(model.most_similar(i))
    
    
            
            
        
