import json,os,sys,urllib.error,urllib.request as u
U=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("MAKEFUN_ENV_URL is not set")
V=[0,100,320,330,500,920,0]
I=100000
def R(p,b):
 r=u.Request(U+p,json.dumps(b).encode(),{"content-type":"application/json"})
 try:
  with u.urlopen(r)as r:return json.load(r)
 except u.HTTPError as e:sys.exit(f"{p}: HTTP {e.code} {e.read().decode(errors='replace')}")
def F(f):
 b=[0]*64;s=0;c=0;e=-1;k=[-1,-1];p=f.split();q=0
 for r in p[0].split("/"):
  for ch in r:
   if ch.isdigit():q+=int(ch)
   else:
    t="pnbrqk".index(ch.lower());o=ch<"a";b[q]=t+1+o*6
    if t==5:k[o]=q
    q+=1
 s=0if p[1]=="w"else 1
 for ch in p[2]:
  if ch=="K":c|=1
  elif ch=="Q":c|=2
  elif ch=="k":c|=4
  elif ch=="q":c|=8
 if p[3]!="-":e=("abcdefgh".index(p[3][0])+(8-int(p[3][1]))*8)
 return b,s,c,e,k
def E(b,s):
 v=0
 for i,p in enumerate(b):
  if not p:continue
  t=(p-1)%6;c=p>6;r=i//8
  if c:r=7-r
  if t==5:continue
  x=V[t]+(t==0)*r*10+(t in(1,2))*abs(r-3)*20
  v+=x if not c else-x
 return v if s==0else-v
def A(b,i,c):
 r=i//8;f=i%8;o=c*6
 if c==0:
  if r<7 and f>0 and b[i+7]==1:return 1
  if r<7 and f<7 and b[i+9]==1:return 1
 else:
  if r>0 and f>0 and b[i-9]==7:return 1
  if r>0 and f<7 and b[i-7]==7:return 1
 for d in(17,15,10,6,-6,-10,-15,-17):
  j=i+d
  if 0<=j<64 and abs(j%8-f)<=2 and b[j]==2+o:return 1
 for d in(1,8,-1,-8):
  for j in range(i+d,64 if d>0 else -1,d):
   if not 0<=j<64 or(d in(1,-1)and j//8!=r):break
   if b[j]:
    if b[j]in(3+o,5+o):return 1
    break
 for d in(9,7,-7,-9):
  for j in range(i+d,64 if d>0 else -1,d):
   if not 0<=j<64 or abs(j%8-(j-d)%8)>1:break
   if b[j]:
    if b[j]in(4+o,5+o):return 1
    break
 return 0
def M(f,t,p=0):return f|t<<6|p<<12
def G(b,s,c,e,o=0):
 m=[];u=s;d=8if u==0else-8;L=56if u==0else 7
 for i,p in enumerate(b):
  if not p or(p>6)==u:continue
  t=(p-1)%6;r=i//8;f=i%8
  if t==0:
   n=i+d
   if 0<=n<64 and not b[n]:
    if(i>=L if u==0else i<=L):m.append(M(i,n,5))
    elif not o:m.append(M(i,n,0))
   for s in(d-1,d+1):
    n=i+s
    if 0<=n<64 and abs(n%8-f)==1:
     g=b[n]
     if g and(g>6)!=u:
      if(i>=L if u==0else i<=L):m.append(M(i,n,5)|1<<17)
      else:m.append(M(i,n,0)|1<<17)
     elif n==e:m.append(M(i,n,0)|1<<17|1<<18)
  elif t in(1,5):
   for d in(17,15,10,6,-6,-10,-15,-17)if t==1else(1,8,-1,-8):
    n=i+d
    if 0<=n<64 and(t!=1 or abs(n%8-f)<=2):
     g=b[n]
     if not g:
      if not o:m.append(M(i,n,0))
     elif(g>6)!=u:m.append(M(i,n,0)|1<<17)
  else:
   for d in(9,7,-7,-9)if t==2else(1,8,-1,-8)if t==3else(1,8,-1,-8,9,7,-7,-9):
    for n in range(i+d,64 if d>0 else -1,d):
     if not 0<=n<64 or(t in(2,4)and abs(n%8-(n-d)%8)>1):break
     g=b[n]
     if not g:
      if not o:m.append(M(i,n,0))
      continue
     if(g>6)!=u:m.append(M(i,n,0)|1<<17)
     break
 return m
def Z(b,s,c,e,k,d,a,B):
 if d<=0:
  v=E(b,s)
  if v>=B:return v
  if v>a:a=v
  for m in G(b,s,c,e,1):
   n=b[:];S=s;C=c;Ee=e;Kk=k[:]
   f=m&63;t=m>>6&63;p=m>>12&7;P=b[f]
   n[f]=0;n[t]=p+1+u*6 if p else P
   C&=15;Ee=-1;S^=1
   if A(n,Kk[S],S):continue
   v=-Z(n,S,C,Ee,Kk,0,-B,-a)
   if v>a:a=v
   if v>=B:break
  return a
 m=G(b,s,c,e)
 m.sort(key=lambda x:(-V[(b[x>>6&63]-1)%6]*10 if x&1<<17 else 0))
 v=-I
 for m in m:
  n=b[:];S=s;C=c;Ee=e;Kk=k[:]
  f=m&63;t=m>>6&63;p=m>>12&7;P=b[f]
  n[f]=0;n[t]=p+1+u*6 if p else P
  C&=15;Ee=-1;S^=1
  if A(n,Kk[S],S):continue
  v=-Z(n,S,C,Ee,Kk,d-1,-B,-a)
  if v>a:a=v
  if a>=B:break
 return v
def C(f,l):
 b,s,c,e,k=F(f)
 B=l[0];bS=-I
 for u in l:
  f="abcdefgh".index(u[0])+(8-int(u[1]))*8;t="abcdefgh".index(u[2])+(8-int(u[3]))*8;p=" nbrq".index(u[4])if len(u)==5else 0
  m=M(f,t,p)
  if m not in G(b,s,c,e):continue
  n=b[:];S=s;C=c;Ee=e;Kk=k[:]
  P=b[f]
  n[f]=0;n[t]=p+1+u*6 if p else P
  C&=15;Ee=-1;S^=1
  if A(n,Kk[S],S):continue
  v=-Z(n,S,C,Ee,Kk,4,-I,I)
  if v>bS:bS=v;B=u
 return B
while 1:
 g=R("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":g=R("/move",{"game":g["game"],"move":C(g["fen"],g["legal_moves"])})