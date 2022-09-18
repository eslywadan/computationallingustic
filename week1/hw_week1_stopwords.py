from week1.stopwords import RemoveStopWords

filepath = 'data/2022 09 12 Computational Liinguistics  WK 1 作業語料.xlsx'
rmstopw = RemoveStopWords(filepath)
rmstopw.remove_stopwords()