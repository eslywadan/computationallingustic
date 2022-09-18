# ligusticcomputing
The repository is the programming work for the 'Computational Linguistics' course taught by professor Lu @NTHU
## week1  - removed the stopwords
- corpus data is the 'data/2022 09 12 Computational Liinguistics  WK 1 作業語料.xlsx' and the sample result is '2022 09 12 Computational Liinguistics  WK 1 作業語料_result.json'
- class CstopWords has the 'cswl' property read the basic stop words list from nltk with extending and substracting list by my own.                                     
- class RemoveStopWords read the corpus and use the CstopWords to search stop words and output the result
-  execute
```shell
$ python week1/hw_week1_stopwords.py
```
The week1 result has some issuses recorded in https://hackmd.io/@Esly/Bkxaq_mZi
