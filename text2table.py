#!/usr/bin/python
# -*- coding: UTF-8 -*-
import jieba
import pymysql
def sentencecount(textstr,keycharacter):
    n = len(textstr)
    index = 0
    tindex = [ ]
    while index <= n:
        index = textstr.find(keycharacter,index)
        if index == -1:
            break
        tindex = tindex + [index]
        index += 1
    return tindex
db = pymysql.connect('localhost','root','271828','DistrSentLen')
cx = db.cursor()
sql = '''
CREATE TABLE sentence_table(
sentence_id INT NOT NULL AUTO_INCREMENT,
character_count INT NOT NULL,
word_count INT NOT NULL,
primary key (SENTENCE_ID)
)ENGINE = InnoDB;
'''
cx.execute(sql)
for i in range(10,2000):
    ri = '%d'%i
    pathstr = 'Reduced\\C000008\\'+ ri + '.txt'
    f = open(pathstr,'r',errors = 'ignore')
    textstr = f.read()
    textstr = (textstr.replace(u'\u3000','').replace(' ','').replace('    ','').replace('‘','')
    .replace('’','').replace('“','').replace('”','').replace('、','').replace('（','').replace('）','')
    .replace('《','').replace('》','').replace('%','').replace('\n\n',''))
    textjieba = '/'.join(jieba.cut(textstr))
    symbal_set = ['，','。','？','！','；','：','\n']
    keycharacter_div = '/'
    indexjieba_symbal = [ ]
    symbal_set_len = len(symbal_set)
    for j in range(0,symbal_set_len):
        key_symbal = symbal_set[j]
        indexjieba_symbal += sentencecount(textjieba,key_symbal)
    indexjieba_div = sentencecount(textjieba,keycharacter_div)
    indexjieba = indexjieba_symbal + indexjieba_div
    indexjieba_symbal.sort()
    indexjieba.sort()
    indexjieba_symbal_ini = indexjieba_symbal[0]
    if indexjieba_symbal_ini == 0:
        indexjieba_symbal_ini = indexjieba_symbal[1]
    indexjieba_div_ini = indexjieba_div.index(indexjieba_symbal_ini - 1)
    word_count = len(indexjieba_div[0:indexjieba_div_ini]) + 1
    character_count = indexjieba_symbal_ini - word_count
    sql = '''
    INSERT INTO sentence_table(
    character_count,
    word_count)
    VALUES(%s,%s);
    '''
    cx.execute(sql,(character_count,word_count))
    n = len(indexjieba_symbal)
    for j in range(0,n-1):
        k = j + 1
        indexbegin = indexjieba_symbal[j] + 1
        indexend = indexjieba_symbal[k]
        word_indexbegin = indexjieba_div.index(indexbegin    )
        word_indexend = indexjieba_div.index(indexend - 1)
        word_count = len(indexjieba_div[word_indexbegin:word_indexend])
        character_count = indexend - indexbegin - word_count - 1
        if (word_count and character_count) > 0:
            #checking whether the sentence separate is efficient
            #print(textjieba[indexbegin_indexend],'/n',word_count,character_count)
            sql = '''
            INSERT INTO sentence_table(
            character_count,
            word_count)
            VALUES(%s,%s);
            '''
            cx.execute(sql,(character_count,word_count))
db.commit()
cx.close
db.close
        