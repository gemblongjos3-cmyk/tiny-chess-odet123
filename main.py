D=(16,-16,1,-1,17,15,-15,-17);K=(33,31,18,14,-14,-18,-31,-33);V={'p':100,'n':320,'b':330,'r':500,'q':900,'k':0};U=str.isupper;L=str.lower
CS=((4,6,7,(5,6),(4,5,6),'K'),(4,2,0,(1,2,3),(4,3,2),'Q'))
CR={0:'Q',7:'K',112:'q',119:'k'}
def ld(f):
 a=[0]*128;r=f.split();p=112
 for row in r[0].split('/'):
  for z in row:
   if z>'8':a[p]=z;p+=1
   else:p+=int(z)
  p-=24
 return a,2*(r[1]=='w')-1,r[2].strip('-'),-1 if r[3]=='-' else int(r[3][1])*16+ord(r[3][0])-113,int(r[4])
def gn(a,s,c,e,cap=0,t=-1):
 if t>=0:
  for p in range(128):
   z=a[p]
   if p&136 or not z or U(z)!=(s==1):continue
   z=L(z);ds=K if z=='n' else ((15,17) if s==1 else (-15,-17)) if z=='p' else D if z in 'qk' else D[4:] if z=='b' else D[:4]
   for d in ds:
    q=p+d
    while not q&136:
     if q==t:return 1
     if a[q] or z in 'pnk':break
     q+=d
  return 0
 o=[]
 for p in range(128):
  z=a[p]
  if p&136 or not z or U(z)!=(s==1):continue
  z=L(z)
  def put(q,r=''):
   if a[q] and (U(a[q])==(s==1) or L(a[q])=='k') or cap and not a[q] and q!=e:return
   o.extend((p,q,x) for x in 'qrbn') if z=='p' and q>>4 in (0,7) else o.append((p,q,r))
  if z=='p':
   for d in (16*s,15*s,17*s):
    q=p+d
    if q&136:continue
    if d==16*s:
     if not cap and not a[q]:
      put(q);q+=d
      if p>>4==(1 if s==1 else 6) and not a[q]:put(q)
    elif (a[q] and U(a[q])!=(s==1) and L(a[q])!='k') or q==e:put(q)
  else:
   ds=K if z=='n' else D if z in 'qk' else D[4:] if z=='b' else D[:4]
   for d in ds:
    q=p+d
    while not q&136:
     if a[q]:
      if U(a[q])!=(s==1):put(q)
      break
     put(q)
     if z in 'nk':break
     q+=d
  if z=='k' and not cap:
   for f,g,r,em,att,cr in CS:
    off=112*(s<0);f+=off;g+=off;r+=off
    if p==f and (cr if s==1 else cr.lower()) in c and not any(a[v+off] for v in em) and a[r]==('R' if s==1 else 'r') and not any(gn(a,-s,c,e,0,v+off) for v in att):o.append((p,g,'c'))
 return o
def mv(a,s,c,e,h,m):
 a=a[:];p,q,r=m;z=a[p];cap=a[q];a[p]=0;a[q]=r.upper() if r and r!='c' and s>0 else r if r and r!='c' else z
 if L(z)=='p' and q==e and p&7!=q&7:cap=a[q-16*s];a[q-16*s]=0
 if r=='c':x,y=(q+1,q-1) if q>p else (q-2,q+1);a[y]=a[x];a[x]=0
 if z in 'Kk':c=c.replace(z,'').replace('Q' if z=='K' else 'q','')
 for x in p,q:c=c.replace(CR.get(x,''),'')
 e=(p+q)//2 if L(z)=='p' and abs(q-p)==32 else -1
 return a,c,e,0 if cap or L(z)=='p' else h+1,cap
def lg(a,s,c,e,h=0):
 return [m for m in gn(a,s,c,e) if not gn((v:=mv(a,s,c,e,h,m))[0],-s,v[1],v[2],0,v[0].index('K' if s==1 else 'k'))]
def ev(a):
 return sum((2*U(z)-1)*V[L(z)] for p,z in enumerate(a) if z and not p&136)
N=0;B=30000
def ng(a,s,c,e,h,d,l,b,r=0):
 global N
 if r:
  ms=lg(a,s,c,e,h)
  if not ms:return None,N
  for x in ms:
   z,C,E,F,_=mv(a,s,c,e,h,x);k=z.index('k' if s>0 else 'K')
   if gn(z,s,C,E,0,k) and not lg(z,-s,C,E,F):return x,0
  ms.sort(key=lambda m:bool(a[m[1]]),reverse=True)
  m=ms[0]
  for dep in range(1,8):
   best=-99999
   for x in ms:
    if N>=B:break
    z,c1,e1,h1,cap=mv(a,s,c,e,h,x)
    v=-ng(z,-s,c1,e1,h1,dep-1,-99999,99999)
    if v>best:best=v;m=x
   if N>=B:break
  return m,N
 if h>=100:return 0
 if N>=B:return s*ev(a)
 N+=1;q=d<=0;v=s*ev(a)
 if q:
  if v>=b:return v
  l=max(l,v)
  if d<=-8:return v
 ms=gn(a,s,c,e,1) if q else lg(a,s,c,e,h)
 if not ms:return 0 if q or gn(a,-s,c,e,0,a.index('K' if s==1 else 'k')) else -30000
 if not q:ms.sort(key=lambda m:bool(a[m[1]]),reverse=True)
 for m in ms:
  z,c1,e1,h1,cap=mv(a,s,c,e,h,m)
  v=-ng(z,-s,c1,e1,h1,d-1,-b,-l)
  l=max(l,v)
  if l>=b:break
 return l
def ch(f,b=B):
 global N,B;N=0;B=b;return ng(*ld(f),0,-99999,99999,1)
def uc(m):return chr(97+(m[0]&7))+str((m[0]>>4)+1)+chr(97+(m[1]&7))+str((m[1]>>4)+1)+m[2].strip('c')
import os as O,json as J
from urllib.request import Request as R,urlopen as W
def api(p,d):return J.loads(W(R(O.getenv('MAKEFUN_ENV_URL').rstrip('/')+p,J.dumps(d).encode(),{'Content-Type':'application/json'}),None,10).read())
if __name__=='__main__':
 while (g:=api('/game',{}))['status']!='done':
  while g['status']=='your_move':
   f=g['fen'];m,n=ch(f)
   g=api('/move',{'game':g['game'],'move':uc(m)})
