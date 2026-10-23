from bible import chap, NR
from concurrent.futures import ThreadPoolExecutor
CH={'徒':28,'罗':16,'林前':16,'林后':13,'加':6,'弗':6,'腓':4,'西':4,'帖前':5,'帖后':3,'提前':6,'提后':4,'多':3,'门':1,'来':13,'雅':5,'彼前':5,'彼后':3,'约壹':5,'约贰':1,'约叁':1,'犹':1}
jobs=[(NR[b],c) for b,n in CH.items() for c in range(1,n+1)]
def f(j):
    for i in range(3):
        try: chap(*j); return None
        except Exception as e: err=e
    return (j,str(err))
with ThreadPoolExecutor(8) as ex: r=[x for x in ex.map(f,jobs) if x]
print(len(jobs),'fail',r)
