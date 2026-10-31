"""BM25 plus character-trigram retrieval, selected on development cases."""
import collections,json,math,re,sqlite3,threading
from pathlib import Path

STOP=set('a an the is are of to in on for and or how what which do does can i we my me this that it with from by as be at about'.split())
def tokens(text):return [t for t in re.findall(r'[a-z0-9]+',text.lower()) if t not in STOP]
def grams(text):
    value=' '.join(tokens(text));return {value[i:i+3] for i in range(max(0,len(value)-2))}
def blocked(text):
    return bool(re.search(r'ignore (all |the )?(previous|system|instructions)|system prompt|api.?key|password|patient|prescription|walgreens.{0,40}(actual|internal|confidential)|(?:actual|internal|confidential).{0,40}walgreens',text,re.I))

class Retriever:
    def __del__(self):
        try:self.connection.close()
        except Exception:pass
    def __init__(self,documents):
        self.docs={d['id']:d for d in documents};self.lock=threading.RLock()
        if len(self.docs)!=len(documents):raise ValueError('Duplicate evidence ID')
        self.connection=sqlite3.connect(':memory:',check_same_thread=False)
        self.connection.execute('CREATE VIRTUAL TABLE evidence USING fts5(id UNINDEXED,title,body)')
        self.connection.executemany('INSERT INTO evidence VALUES (?,?,?)',[(d['id'],d['title'],d['body']) for d in documents])
        self.docgrams={d['id']:grams(d['title']+' '+d['body']) for d in documents}
    def search(self,question,method='hybrid',k=3):
        terms=list(dict.fromkeys(tokens(question)))[:40]
        if not terms:return []
        match=' OR '.join('"'+t+'"' for t in terms)
        with self.lock:
            hits=self.connection.execute('SELECT id,bm25(evidence,0,2,1) AS score FROM evidence WHERE evidence MATCH ? ORDER BY score,id LIMIT 30',(match,)).fetchall()
        lexical=[r[0] for r in hits]
        if method=='bm25':order=lexical
        elif method=='hybrid':
            qgrams=grams(question)
            fuzzy=sorted(self.docs,key=lambda key:(-len(qgrams&self.docgrams[key])/max(1,len(qgrams|self.docgrams[key])),key))
            fusion=collections.defaultdict(float)
            for ranking in [lexical,fuzzy]:
                for rank,key in enumerate(ranking):fusion[key]+=1/(20+rank+1)
            order=sorted(fusion,key=lambda key:(-fusion[key],key))
        else:raise ValueError('Unknown retrieval method')
        result=[]
        for key in order[:k]:
            d=self.docs[key];overlap=len(set(terms)&set(tokens(d['title']+' '+d['body'])))/len(set(terms))
            result.append({**d,'confidence':overlap})
        return result
