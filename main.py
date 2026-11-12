import os,json,urllib.request
U=os.environ.get('MAKEFUN_ENV_URL','')
V={'p':100,'n':320,'b':330,'r':500,'q':900,'k':0}
D=[1,-1,16,-16,15,17,-15,-17]
def ld(f):
 x=f.split();a=['']*128;i=112
 for c in x[0]:
  if c=='/':i-=24
  elif c.isdigit():i+=int(c)
  else:a[i]=c;i+=1
 return a,1 if x[1]=='w' else -1,x[2],-1 if x[3]=='-' else ord(x[3][0])-97+16*(int(x[3][1])-1),int(x[4])
def att(a,q,s):
 for d in (15,17):
  z=q-d*s
  if not z&0x88 and a[z]==('P' if s==1 else 'p'):return 1
 for d in (-33,-31,-18,-14,14,18,31,33):
  z=q+d
  if not z&0x88 and a[z]==('N' if s==1 else 'n'):return 1
 for d in D:
  z=q+d
  while not z&0x88:
   p=a[z]
   if p:
    if p.isupper()==(s==1) and (p.lower()=='q' or d in D[:4] and p.lower()=='r' or d in D[4:] and p.lower()=='b' or z==q+d and p.lower()=='k'):return 1
    break
   z+=d
 return 0
def mv(a,s,c,e,h,m):
 p,q,r=m;b=a[:];z=b[p];cap=b[q];b[p]='';b[q]=(r.upper() if s==1 else r) if r not in ('','c') else z
 if z.lower()=='p' and q==e and p%16!=q%16:cap=b[q-16*s];b[q-16*s]=''
 if r=='c':
  x,y=(q+1,q-1) if q>p else (q-2,q+1);b[y]=b[x];b[x]=''
 if z.lower()=='k':c=c.replace('K','').replace('Q','') if s==1 else c.replace('k','').replace('q','')
 for x,R in ((0,'Q'),(7,'K'),(112,'q'),(119,'k')):
  if p==x or q==x:c=c.replace(R,'')
 return b,c,(p+q)//2 if z.lower()=='p' and abs(q-p)==32 else -1,0 if cap or z.lower()=='p' else h+1,cap
def lg(a,s,c,e,h):
 out=[]
 for p,z in enumerate(a):
  if p&0x88 or not z or z.isupper()!=(s==1):continue
  t=z.lower()
  if t=='p':
   q=p+16*s
   if not q&0x88 and not a[q]:
    out.append((p,q,''))
    if p//16==(1 if s==1 else 6) and not a[q+16*s]:out.append((p,q+16*s,''))
   for d in (15*s,17*s):
    q=p+d
    if not q&0x88 and ((a[q] and a[q].isupper()!=(s==1) and a[q].lower()!='k') or q==e):out.append((p,q,''))
  else:
   ds=(-33,-31,-18,-14,14,18,31,33) if t=='n' else D
   for d in ds:
    if t=='b' and d in D[:4] or t=='r' and d in D[4:]:continue
    q=p+d
    while not q&0x88:
     if a[q]:
      if a[q].isupper()!=(s==1) and a[q].lower()!='k':out.append((p,q,''))
      break
     out.append((p,q,''))
     if t in 'nk':break
     q+=d
   if t=='k':
    for dest,rook,empty,through,R in ((p+2,p+3,(p+1,p+2),(p,p+1,p+2),'K'),(p-2,p-4,(p-1,p-2,p-3),(p,p-1,p-2),'Q')):
     R=R if s==1 else R.lower()
     if p==(4 if s==1 else 116) and R in c and a[rook]==('R' if s==1 else 'r') and not any(a[v] for v in empty) and not any(att(a,v,-s) for v in through):out.append((p,dest,'c'))
 legal=[]
 for m in out:
  b,_,_,_,_=mv(a,s,c,e,h,m);k=b.index('K' if s==1 else 'k')
  if not att(b,k,-s):
   p,q,r=m
   legal.extend((p,q,x) for x in 'qrbn') if a[p].lower()=='p' and q//16 in (0,7) else legal.append(m)
 return legal
def uc(m):
 p,q,r=m
 return chr(97+p%16)+str(p//16+1)+chr(97+q%16)+str(q//16+1)+(r if r not in ('','c') else '')
nodes=0
def ev(a):return sum(V[z.lower()]*(1 if z.isupper() else -1) for z in a if z)
def search(a,s,c,e,h,d,al,be):
 global nodes
 nodes+=1
 if nodes>30000:return ev(a)*s
 if h>=100:return 0
 if d<=0:
  v=ev(a)*s
  if v>=be:return v
  al=max(al,v);ms=[m for m in lg(a,s,c,e,h) if a[m[1]] or m[2]]
 else:ms=lg(a,s,c,e,h);v=-99999
 if not ms:return v if d<=0 else (-30000 if att(a,a.index('K' if s==1 else 'k'),-s) else 0)
 ms.sort(key=lambda m:(-(V.get(a[m[1]].lower(),0) if a[m[1]] else 100 if m[2] else 0),uc(m)))
 for m in ms:
  b,C,E,H,_=mv(a,s,c,e,h,m);v=max(v,-search(b,-s,C,E,H,d-1,-be,-al))
  al=max(al,v)
  if al>=be:break
 return v
def ch(f,budget=30000):
 global nodes
 a,s,c,e,h=ld(f);nodes=0;best=None;score=-99999
 for m in lg(a,s,c,e,h):
  b,C,E,H,_=mv(a,s,c,e,h,m);v=-search(b,-s,C,E,H,2,-99999,99999)
  if v>score:best,score=m,v
  if v>=29999 or nodes>=budget:break
 return best,nodes
def post(path,data):
 r=urllib.request.Request(U+path,data=json.dumps(data).encode(),headers={'content-type':'application/json'})
 return json.load(urllib.request.urlopen(r))
if __name__=='__main__':
 while 1:
  g=post('/game',{})
  if g['status']=='done':break
  while g['status']=='your_move':
   m,n=ch(g['fen']);g=post('/move',{'game':g['game'],'move':uc(m)})
