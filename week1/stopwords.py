import nltk
from nltk.corpus import stopwords
import pandas as pd
import json

class RemoveStopWords():
    """
    class designed for removing stop words
    """
    
    df = {}
    
    def __init__(self, filepath=None):
        if filepath == None:
            filepath = 'data/2022 09 12 Computational Liinguistics  WK 1 作業語料.xlsx'
        self._sourcefilepath = filepath
        fileext = filepath.split(".")[len(filepath.split("."))-1]
        
        if fileext in ['xls','xlsx']: self.read_excel()
        else: return {"message":f'file ext is {fileext}, currently not support'}
        self.outputfile = f'{filepath.split(".")[0]}_result.json'
        
    def read_excel(self):
        self.workbook = pd.read_excel(self._sourcefilepath, sheet_name=None, header=None)
        self.sheet_names = self.workbook.keys()
        for sheet_name in self.sheet_names:
            self.df[sheet_name] = self.workbook[sheet_name]



    def remove_stopwords(self):
        self.process_stopwords()
        
        result = {}
        
        for page in self.processed_corpus.keys():
            print(f"work sheet: {page}")
            result[f'Worksheet:{page}'] = {}
            content1 = self.processed_corpus[page]['raw sentence']
            content2 = self.processed_corpus[page]['found stop words']
            content3 = self.processed_corpus[page]['segmented words']
            for index in content1:      # content['raw_sentence'] is the dict of raw_sentences
                result[f'Worksheet:{page}'] [f'Index:{index}'] = {}
                result[f'Worksheet:{page}'] [f'Index:{index}']["raw sentence"] = f'{content1[index]}'
                result[f'Worksheet:{page}'] [f'Index:{index}']["found stop words"] = f'{content2[index]}'
                result[f'Worksheet:{page}'] [f'Index:{index}']["segmeted words"] = f'{content3[index]}'
                print(f"index:{index}")
                print(f"raw sentence: {content1[index]} ")
                print(f"found stop words: {content2[index]} ")
                print(f"segmeted words: {content3[index]}")
        
        self.rm_stopw_res = result
        self.save_result()
            
    def save_result(self):
        with open(self.outputfile, 'w', encoding='utf-8') as fp:
            json.dump(self.rm_stopw_res, fp, ensure_ascii=False, indent=4)
       
            
    def process_stopwords(self):
        cstopw = CstopWords()
        self.processed_corpus = {}
        for sheet_name in self.sheet_names:
            df = self.df[sheet_name]
            raw_sentences = {}
            bagofstopwords = {}
            seg_words = {}
            for line in df.values:
                index = line[:3]
                idx = f'{index[0]} {index[1]} {index[2]}'
                sentence = line[3:][0]
                raw_sentences[idx] = sentence 
                cstopw.seg_by_stopwords(sentence)
                bagofstopwords[idx] = cstopw.bagofstopwords
                seg_words[idx] = cstopw.seg
            
            self.processed_corpus[sheet_name] = {"raw sentence": raw_sentences,"found stop words":bagofstopwords,"segmented words":seg_words}
            

class CstopWords():
    """ 
        cswl chinese stop words list
        scswlbync seperate chinese stop words list by number of character 
        leadingcharbyswn take the leading char as a list by group of chars number
    """
    cswl = stopwords.words('chinese')
    scswlbync = {}
    leadingchar = []
    swdictkeybyleadingchar = {}
    
    def __init__(self):
        self.remove_my_sw()
        self.add_my_sw()
        self.sep_words_by_charn()
    
    def sep_words_by_charn(self):
        """ 
        sep into 1 char 2 char 3 char etc..
        """    
        for w in self.cswl:
            n = len(w)
            if n not in self.scswlbync.keys(): self.scswlbync[n] = []
            self.scswlbync[n].append(w)
            if w[0] not in self.leadingchar: self.leadingchar.append(w[0])
            if w[0] not in self.swdictkeybyleadingchar.keys(): self.swdictkeybyleadingchar[w[0]] = []
            self.swdictkeybyleadingchar[w[0]].append(w)
        
        for leadingchar in self.swdictkeybyleadingchar.keys():
            self.swdictkeybyleadingchar[leadingchar] = sorted(self.swdictkeybyleadingchar[leadingchar], key=len, reverse = True)
            
    def search_stopwords_by_sentence(self, sentence):
        """
        sentence s1 has m chars
        s1(1) has possible words s1(1), s1(1:2), s1(1:3) .. s1(1:m)
        stopwords has the max chars by max(self.scswlbync.keys()), thus m == max(self.scswlbync.keys())
        Thus, the compare will start with the first char and 
            1. take the char as the leading char to check the existence in stop words with only one char
            2. take the char as the leading char and sucessed the 2nd char to form a multiple chars set and then check the existence in stopwords with 2 chars
            3.  
        """
        n = 0
        self.bagofstopwords = {}
        bagofstopwords = {}
        maxcharsn = max(self.scswlbync.keys())
        while n < len(sentence):
            char = sentence[n]
            if char in self.leadingchar:
                m = len(self.swdictkeybyleadingchar[char][0])
                while m >= 1:
                    charset = sentence[n:n+m]
                    for swcharset in self.swdictkeybyleadingchar[char]:
                        if charset == swcharset:
                            if n not in bagofstopwords.keys(): bagofstopwords[n] = []
                            bagofstopwords[n].append(charset)
                    m -= 1
            n += 1
            
        self.bagofstopwords = bagofstopwords    
        return bagofstopwords
    
    def seg_by_stopwords(self, sentence):
        
        self.search_stopwords_by_sentence(sentence)
        if self.bagofstopwords == {}: 
            self.raw_seg = sentence
            self.seg = sentence
            return {1:sentence}
        
        self.raw_seg = {}
        self.seg = {}
        
        seg_sentence = ''
        i = 0                                          # Count index of the bagofstopwords
        swil = {}                                      # container store the seqence count for each stop words
        seg = {}
        for swi in self.bagofstopwords:                      # bagofstopwords example {5: ['像'], 6: ['是'], 7: ['一個', '一']}, swi = 5, 6, 7 
            swil[i] = swi + len(self.bagofstopwords[swi][0]) # swi = 7, bagofstopwords[7][0] = '一個', len('一個') == 2 , swi + 2 = 9 : next index by the end of stop words
            if i == 0:seg[0] = sentence[0:swi]        # 如果是第一個 stop word, 起始斷詞從0開始
            else: seg[i] = sentence[swil[i-1]:swi]    # 上一個 stopword 的結束後 到 下一個 stopword 的開始)
            i += 1
            
        if swil[i-1] < len(sentence)-1: seg[i] = sentence[swil[i-1]+1:]
            
        self.raw_seg = seg
            
        lined_seg = {}
        j = 1
        for wi in seg:
            if seg[wi] is None : next
            if seg[wi] == ''   : next
            ws = seg[wi].strip()
            for w in ws.split(" "):
                if w != ' ' and w != '': 
                    lined_seg[j] = w
                    j += 1
        
        self.seg = lined_seg
        return lined_seg
        
    def add_my_sw(self):
        my_stop_words_list = ['*','(',')',',','!','。']
        self.cswl.extend(my_stop_words_list)
        
    def remove_my_sw(self):
        remove_my_stop_words_list = ['一']
        for rw in remove_my_stop_words_list:
            if rw in self.cswl: self.cswl.remove(rw)