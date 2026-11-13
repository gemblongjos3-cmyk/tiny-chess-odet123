import os,sys,json,urllib.request
sys.setrecursionlimit(100000)
U=os.getenv('MAKEFUN_ENV_URL','')
V={'p':100,'n':320,'b':330,'r':500,'q':900,'k':0}
D8=(16,-16,1,-1,17,15,-15,-17);KN=(33,31,18,14,-14,-18,-31,-33)
PT={
'p':[0,0,0,0,0,0,0,0,50,50,50,50,50,50,50,50,12,14,20,26,26,20,14,12,8,10,16,24,24,16,10,8,6,8,12,20,20,12,8,6,5,6,10,14,14,10,6,5,5,8,10,12,12,10,8,5,0,0,0,0,0,0,0,0],
'n':[-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,10,15,15,10,0,-10,-10,5,15,20,20,15,5,-10,-10,0,15,20,20,15,0,-10,-10,5,10,15,15,10,5,-10,-10,0,5,10,10,5,0,-10,-20,-10,-10,-5,-5,-10,-10,-20],
'b':[-10,-5,-5,-5,-5,-5,-5,-10,-5,5,5,5,5,5,5,-5,-5,5,12,15,15,12,5,-5,-5,8,15,20,20,15,8,-5,-5,8,14,20,20,14,8,-5,-5,6,12,15,15,12,6,-5,-5,4,8,10,10,8,4,-5,-10,-5,-5,-5,-5,-5,-5,-10],
'r':[0,0,5,10,10,5,0,0,5,10,10,10,10,10,10,5,0,0,5,8,8,5,0,0,0,0,5,8,8,5,0,0,0,0,5,8,8,5,0,0,0,0,5,8,8,5,0,0,5,10,10,12,12,10,10,5,0,0,5,10,10,5,0,0],
'q':[-5,0,0,5,5,0,0,-5,0,5,5,8,8,5,5,0,0,5,10,12,12,10,5,0,5,8,12,15,15,12,8,5,5,8,12,15,15,12,8,5,0,5,10,12,12,10,5,0,0,5,5,8,8,5,5,0,-5,0,0,5,5,0,0,-5],
'k':[-40,-30,-30,-30,-30,-30,-30,-40,-30,-20,-25,-25,-25,-25,-20,-30,-20,-15,-20,-20,-20,-20,-15,-20,-15,-10,-15,-18,-18,-15,-10,-15,-10,-5,-12,-15,-15,-12,-5,-10,-5,-2,-8,-10,-10,-8,-2,-5,5,10,0,-5,-5,0,10,5,20,25,15,0,0,15,25,20]}
KGE=[-10,-5,0,5,5,0,-5,-10,-5,5,10,15,15,10,5,-5,0,10,20,25,25,20,10,0,5,15,25,30,30,25,15,5,5,15,25,30,30,25,15,5,0,10,20,25,25,20,10,0,-5,5,10,15,15,10,5,-5,-10,-5,0,5,5,0,-5,-10]
PH={'n':1,'b':1,'r':2,'q':4}
def pst(t,i,up,phase):
 r=i//16 if up else 7-i//16;f=i%16;idx=(7-r)*8+f
 if t=='k':
  mg=PT['k'][idx];eg=KGE[idx]
  return (mg*min(phase,12)+eg*max(0,12-phase))//12
 return PT[t][idx]
def pval(p,i,phase):
 up=p.isupper()
 return (V[p.lower()]+pst(p.lower(),i,up,phase))*(1 if up else -1)
class TO(Exception):pass
N=[0];CAP=[68000];TT={};KILL={};HIST={}
def att(b,sq,by):
 if by==1:
  for d in (-15,-17):
   z=sq+d
   if not z&0x88 and b[z]=='P':return 1
 else:
  for d in (15,17):
   z=sq+d
   if not z&0x88 and b[z]=='p':return 1
 for d in KN:
  z=sq+d
  if not z&0x88 and b[z]==('N' if by==1 else 'n'):return 1
 for i,d in enumerate(D8):
  z=sq+d
  while not z&0x88 and b[z]=='.':
   z+=d
  if not z&0x88:
   p=b[z]
   if p!='.' and (p.isupper()==(by==1)):
    t=p.lower()
    if t=='k' and z==sq+d:return 1
    if i<4 and t in 'rq':return 1
    if i>=4 and t in 'bq':return 1
 return 0
def gen(b,s,c,e,capsonly=False):
 out=[];up=(s==1)
 for i in range(128):
  if i&0x88:continue
  p=b[i]
  if p=='.' or p.isupper()!=up:continue
  t=p.lower()
  if t=='p':
   fwd=16*s;one=i+fwd
   if b[one]=='.':
    if not capsonly:
     if one//16 in (0,7):
      for pr in 'qrbn':out.append((i,one,pr,''))
     else:
      out.append((i,one,'',''))
      if i//16==(1 if up else 6) and b[i+2*fwd]=='.':out.append((i,i+2*fwd,'',''))
    elif one//16 in (0,7):
     for pr in 'qrbn':out.append((i,one,pr,''))
   for d in (15*s,17*s):
    z=i+d
    if z&0x88:continue
    if (b[z]!='.' and b[z].isupper()!=up and b[z].lower()!='k') or z==e:
     if z//16 in (0,7):
      for pr in 'qrbn':out.append((i,z,pr,''))
     else:out.append((i,z,'','e' if z==e else ''))
  elif t=='n' or t=='k':
   for d in (KN if t=='n' else D8):
    z=i+d
    if not z&0x88 and (b[z]!='.' and b[z].isupper()!=up and b[z].lower()!='k' or (not capsonly and b[z]=='.')):out.append((i,z,'',''))
   if t=='k' and not capsonly:
    home=4 if up else 116
    if i==home:
     if ('K' if up else 'k') in c and b[home+1]=='.' and b[home+2]=='.' and b[home+3]==('R' if up else 'r'):
      if not att(b,home,-s) and not att(b,home+1,-s) and not att(b,home+2,-s):out.append((i,home+2,'','c'))
     if ('Q' if up else 'q') in c and b[home-1]=='.' and b[home-2]=='.' and b[home-3]=='.' and b[home-4]==('R' if up else 'r'):
      if not att(b,home,-s) and not att(b,home-1,-s) and not att(b,home-2,-s):out.append((i,home-2,'','c'))
  else:
   dirs=D8[:4] if t=='r' else D8[4:] if t=='b' else D8
   for d in dirs:
    z=i+d
    while not z&0x88:
     if b[z]=='.':
      if not capsonly:out.append((i,z,'',''))
     else:
      if b[z].isupper()!=up and b[z].lower()!='k':out.append((i,z,'',''))
      break
     z+=d
 return out
def mk(b,m,s,c,e,sc,phase):
 f,t,pr,fl=m;p=b[f];up=(s==1)
 delta=0;nphase=phase
 cap=b[t]
 if cap!='.':
  delta-=pval(cap,t,phase);nphase-=PH.get(cap.lower(),0)
 if fl=='e':
  csq=t-16*s;cp=b[csq]
  delta-=pval(cp,csq,phase)
  nb=b[:csq]+'.'+b[csq+1:]
 else:
  nb=b
 delta-=pval(p,f,phase)
 np=(pr.upper() if up else pr) if pr else p
 if pr:nphase+=PH.get(pr,0)
 delta+= (V[pr]+pst(pr,t,up,phase))*(1 if up else -1) if pr else pval(p,t,phase)
 nb=nb[:f]+'.'+nb[f+1:]
 nb=nb[:t]+np+nb[t+1:]
 if fl=='c':
  if t>f:rf,rt=t+1,t-1
  else:rf,rt=t-2,t+1
  r=nb[rf]
  delta-=pval(r,rf,phase);delta+=pval(r,rt,phase)
  nb=nb[:rf]+'.'+nb[rf+1:]
  nb=nb[:rt]+r+nb[rt+1:]
 if nphase!=phase:
  for kp in 'Kk':
   sq=nb.index(kp);up2=(kp=='K')
   delta+=(1 if up2 else -1)*(pst('k',sq,up2,nphase)-pst('k',sq,up2,phase))
 delta+=30*((nb.count('B')>=2)-(b.count('B')>=2))-30*((nb.count('b')>=2)-(b.count('b')>=2))
 nc=c
 if p=='K':nc=nc.replace('K','').replace('Q','')
 if p=='k':nc=nc.replace('k','').replace('q','')
 for sq,rk in ((0,'Q'),(7,'K'),(112,'q'),(119,'k')):
  if f==sq or t==sq:nc=nc.replace(rk,'')
 ne=(f+t)//2 if p.lower()=='p' and abs(t-f)==32 else -1
 return nb,nc,ne,sc+delta,nphase
def key(b,s,c,e):return b+str(s)+c+str(e)
def full_ev(b):
 phase=0;sc=0
 for i in range(128):
  if i&0x88:continue
  p=b[i]
  if p=='.':continue
  if p.lower()!='k' and p.lower()!='p':phase+=PH[p.lower()]
 for i in range(128):
  if i&0x88:continue
  p=b[i]
  if p!='.':sc+=pval(p,i,phase)
 nb=b.count('B');bb=b.count('b')
 if nb>=2:sc+=30
 if bb>=2:sc-=30
 return sc,phase
def legal(b,m,s,c,e,sc,phase):
 nb,nc,ne,nsc,nph=mk(b,m,s,c,e,sc,phase)
 return not att(nb,nb.index('K' if s==1 else 'k'),-s)
def order_key(b,m,tm,ply):
 k1,k2=KILL.get(ply,(None,None))
 f,t,pr,fl=m
 if tm is not None and m==tm:return 10**7
 if b[t]!='.':return 10**6+10*V[b[t].lower()]-V[b[f].lower()]//10
 if fl=='e':return 10**6+900
 if pr:return 9*10**5+V[pr]
 if m==k1:return 5*10**5
 if m==k2:return 4*10**5
 return HIST.get(m,0)
def qs(b,s,c,e,sc,phase,al,be,ply):
 N[0]+=1
 if N[0]>CAP[0]:raise TO()
 ksq=b.index('K' if s==1 else 'k')
 inch=att(b,ksq,-s)
 stm=sc*s
 if ply>=18:
  return stm
 if inch:
  ms=[]
  for m in gen(b,s,c,e):
   nb,nc,ne,nsc,nph=mk(b,m,s,c,e,sc,phase)
   if not att(nb,nb.index('K' if s==1 else 'k'),-s):ms.append((m,nb,nc,ne,nsc,nph))
  if not ms:return -29000+ply
  bt=-30000
  for m,nb,nc,ne,nsc,nph in sorted(ms,key=lambda x:10*V[b[x[0][1]].lower()] if b[x[0][1]]!='.' else 0,reverse=True):
   v=-qs(nb,-s,nc,ne,nsc,nph,-be,-al,ply+1)
   if v>bt:bt=v
   if v>al:al=v
   if al>=be:break
  return bt
 if stm>=be:return stm
 if stm>al:al=stm
 bt=stm
 for m in gen(b,s,c,e,True):
  if b[m[1]]!='.' and stm+V[b[m[1]].lower()]+200<al:continue
  nb,nc,ne,nsc,nph=mk(b,m,s,c,e,sc,phase)
  if att(nb,nb.index('K' if s==1 else 'k'),-s):continue
  v=-qs(nb,-s,nc,ne,nsc,nph,-be,-al,ply+1)
  if v>bt:bt=v
  if v>al:al=v
  if al>=be:break
 return bt
def S(b,s,c,e,sc,phase,d,al,be,ply,hist):
 N[0]+=1
 if N[0]>CAP[0]:raise TO()
 if ply>0 and key(b,s,c,e) in hist:return 0
 ksq=b.index('K' if s==1 else 'k')
 inch=att(b,ksq,-s)
 if d<=0:return qs(b,s,c,e,sc,phase,al,be,ply)
 kk=key(b,s,c,e)
 ent=TT.get(kk);tm=None
 if ent and ent[0]>=d:
  if ent[2]==0:return ent[1]
  if ent[2]==1 and ent[1]>al:al=ent[1]
  if ent[2]==-1 and ent[1]<be:be=ent[1]
  if al>=be:return ent[1]
  tm=ent[3]
 ms=[]
 for m in gen(b,s,c,e):
  nb,nc,ne,nsc,nph=mk(b,m,s,c,e,sc,phase)
  if not att(nb,nb.index('K' if s==1 else 'k'),-s):ms.append((m,nb,nc,ne,nsc,nph))
 if not ms:
  return -29000+ply if inch else 0
 if d>=3 and not inch and ply>0 and (sc*s)>=be and any(ch in ('NBRQ' if s==1 else 'nbrq') for ch in b):
  v=-S(b,-s,c,-1,sc,phase,d-3,-be,-be+1,ply+1,hist)
  if v>=be:return v
 bt=-30000;bm=None;flag=-1;mi=0
 ext=1 if inch else 0
 for m,nb,nc,ne,nsc,nph in sorted(ms,key=lambda x:order_key(b,x[0],tm,ply),reverse=True):
  rd=1
  if d>=3 and mi>3 and b[m[1]]=='.' and not m[2] and not inch:rd=2
  if mi==0:
   v=-S(nb,-s,nc,ne,nsc,nph,d-rd,-be,-al,ply+1,hist)
  else:
   v=-S(nb,-s,nc,ne,nsc,nph,d-rd+ext,-al-1,-al,ply+1,hist)
   if v>al and (rd>1 or v<be):v=-S(nb,-s,nc,ne,nsc,nph,d-1,-be,-al,ply+1,hist)
  mi+=1
  if v>bt:bt,bm=v,m
  if v>al:al=v;flag=0
  if al>=be:
   flag=1
   if b[m[1]]=='.' and not m[2]:
    k1,k2=KILL.get(ply,(None,None));KILL[ply]=(m,k1)
    HIST[m]=HIST.get(m,0)+d*d
   break
 if len(TT)<600000:TT[kk]=(d,bt,flag,bm)
 return bt
def parse(fen):
 x=fen.split();b=['.']*128;i=112
 for z in x[0]:
  if z=='/':i-=24
  elif z.isdigit():i+=int(z)
  else:b[i]=z;i+=1
 s=1 if x[1]=='w' else -1
 c='' if x[2]=='-' else x[2]
 e=-1 if x[3]=='-' else (ord(x[3][0])-97)+16*(int(x[3][1])-1)
 return ''.join(b),s,c,e
def uc(m):
 f,t,pr,fl=m
 return '%c%d%c%d'%(97+f%16,f//16+1,97+t%16,t//16+1)+pr
def choose(fen,hist,fresh=False):
 b,s,c,e=parse(fen)
 sc,phase=full_ev(b)
 ms=[]
 for m in gen(b,s,c,e):
  if legal(b,m,s,c,e,sc,phase):ms.append(m)
 N[0]=0
 if fresh:TT.clear();KILL.clear();HIST.clear()
 bt=ms[0]
 for d in range(1,64):
  try:
   al=-30000;bm=bt
   ms.sort(key=lambda m:m!=bt)
   for m in ms:
    nb,nc,ne,nsc,nph=mk(b,m,s,c,e,sc,phase)
    v=-S(nb,-s,nc,ne,nsc,nph,d-1,-30000,-al,1,hist)
    if v>al:al,bm=v,m
   bt=bm
  except TO:
   break
 return bt
def post(p,d):
 return json.load(urllib.request.urlopen(U+p,data=json.dumps(d).encode()))
if __name__=='__main__':
 hist=set()
 while 1:
  g=post('/game',{})
  if g['status']=='done':break
  fresh=True
  while g['status']=='your_move':
   b,s,c,e=parse(g['fen'])
   hist.add(key(b,s,c,e))
   m=choose(g['fen'],hist,fresh);fresh=False
   g=post('/move',{'game':g['game'],'move':uc(m)})
