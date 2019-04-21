import numpy as np
import matplotlib.pyplot as plt
import pymysql
db = pymysql.connect('localhost','root','271828','DistrSentLen')
cx = db.cursor()
sql = '''
SELECT word_count, COUNT(word_count)
FROM sentence_table
GROUP BY word_count
ORDER BY word_count ASC
'''
cx.execute(sql)
word_count = cx.fetchall()
n = len(word_count)
sentence_len = np.zeros(n,np.int)
sentence_freq = np.zeros(n,np.int)
for i in range(0,n):
    word = word_count[i]
    sentence_len[i] = word[0]
    sentence_freq[i] = word[1]
plt.plot(sentence_len,sentence_freq,'o-')
plt.show()
expectation = np.sum(sentence_len * sentence_freq)
variance = np.sum((sentence_len - expectation)**2 * sentence_freq)
std = np.sqrt(variance)
mostfreq = np.max(sentence_freq)
mostfreq_len_index = np.where(sentence_freq == mostfreq)
mostfreq_len = sentence_len[mostfreq_len_index]
f = open('sentence_info.txt','a')
f.write('expectation:    ')
f.write(str(expectation))
f.write('\n')
f.write('variance:    ')
f.write(str(variance))
f.write('\n')
f.write('std:    ')
f.write(str(std))
f.write('\n')
f.write('maximum frequency sentence length:    ')
f.write(str(mostfreq_len))
f.write('\n')
f.write('rate:    ')
f.write(str(mostfreq))
f.close()
