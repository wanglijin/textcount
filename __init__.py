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