import numpy as np
import matplotlib.pyplot as plt
import pymysql
from asyncore import write
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
sentence_num = np.zeros(n,np.int)
for i in range(0,n):
    word = word_count[i]
    sentence_len[i] = word[0]
    sentence_num[i] = word[1]
sentence_freq = sentence_num / np.sum(sentence_num)
plt.plot(sentence_len,sentence_freq, linestyle = '-', marker = 'o')
plt.xlabel('sentence length')
plt.ylabel('frequency')
plt.show()
plt.plot(sentence_len,np.cumsum(sentence_freq), color = '#FFA500', linestyle = '-', marker = 'o')
plt.xlabel('sentence length')
plt.ylabel('cumulative frequency')
plt.show()
expectation = np.dot(sentence_len,sentence_freq)
res = (sentence_len - expectation)
square_res = np.multiply(res,res)
variance = np.dot(square_res,sentence_freq)
std = np.sqrt(variance)
mostfreq = np.max(sentence_freq)
mostfreq_len = sentence_len[sentence_freq == mostfreq]
right_peak = np.sum(sentence_freq[sentence_len > mostfreq_len])
right_expectation = np.sum(sentence_freq[sentence_len > expectation])
plt.fill_between (sentence_len[sentence_len > mostfreq_len],sentence_freq[sentence_len > mostfreq_len],facecolor = '#FF4500')
plt.fill_between (sentence_len[sentence_len > expectation],sentence_freq[sentence_len > expectation],facecolor = '#40E0D0')
plt.plot(sentence_len,sentence_freq, linestyle = '-')
plt.xlabel('sentence length')
plt.ylabel('frequency')
plt.show()
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
f.write('\n')
f.write('right peak:    ')
f.write(str(right_peak))
f.write('\n')
f.write('right expectation:    ')
f.write(str(right_expectation))
f.close()
