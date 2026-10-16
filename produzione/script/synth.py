import numpy as np, wave, sys, json
SR=44100
def env(n,a,r):
    e=np.ones(n); a=int(a*SR); r=int(r*SR)
    if a: e[:a]=np.linspace(0,1,a)
    if r: e[-r:]*=np.linspace(1,0,r)
    return e
def lp(x,alpha):  # simple one-pole lowpass
    y=np.zeros_like(x); acc=0.0
    for i in range(len(x)): acc+=alpha*(x[i]-acc); y[i]=acc
    return y
def music(dur,bpm=88,seed=1):
    rng=np.random.default_rng(seed); n=int(dur*SR); out=np.zeros(n); beat=60/bpm
    chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]  # Am F C G
    f=lambda m:440*2**((m-69)/12)
    bar=beat*4; t=np.arange(int(bar*SR))/SR
    for bi in range(int(dur/bar)+1):
        c=chords[bi%4]; s=int(bi*bar*SR)
        pad=sum(np.sin(2*np.pi*f(m-12)*t+0.3*np.sin(2*np.pi*0.2*t))+0.4*np.sin(2*np.pi*f(m)*t*1.003) for m in c)
        pad*=env(len(t),0.8,0.8)*0.06
        bass=np.sin(2*np.pi*f(c[0]-24)*t)*env(len(t),0.05,0.5)*0.18
        seg=pad+bass; e=min(n,s+len(seg)); out[s:e]+=seg[:e-s]
    kt=np.arange(int(0.35*SR))/SR
    kick=np.sin(2*np.pi*(45+90*np.exp(-kt*30))*kt)*np.exp(-kt*9)*0.55
    hat=rng.standard_normal(int(0.05*SR)); hat=(hat-lp(hat,0.3))*np.exp(-np.arange(len(hat))/SR*80)*0.05
    k=0; tt=0.0
    while tt<dur:
        s=int(tt*SR)
        if k%2==0: e=min(n,s+len(kick)); out[s:e]+=kick[:e-s]
        s2=int((tt+beat/2)*SR); e=min(n,s2+len(hat)); 
        if s2<n: out[s2:e]+=hat[:e-s2]
        tt+=beat; k+=1
    out*=env(n,1.5,1.5)
    return out
def whoosh(d=0.6):
    n=int(d*SR); x=np.random.default_rng(3).standard_normal(n)
    a=np.linspace(0.02,0.4,n)**1.5; y=np.zeros(n); acc=0
    for i in range(n): acc+=a[i]*(x[i]-acc); y[i]=acc
    return y*np.sin(np.linspace(0,np.pi,n))**2*0.5
def impact():
    t=np.arange(int(1.6*SR))/SR
    boom=np.sin(2*np.pi*(38+60*np.exp(-t*12))*t)*np.exp(-t*2.5)*0.9
    nz=np.random.default_rng(5).standard_normal(len(t))*np.exp(-t*18)*0.25
    glitch=np.sign(np.sin(2*np.pi*220*t))*((t*30).astype(int)%2)*np.exp(-t*6)*0.08
    return boom+nz+glitch
def riser(d=2.5):
    t=np.arange(int(d*SR))/SR
    return np.sin(2*np.pi*(200+600*(t/d)**2)*t)*(t/d)**2*0.08
def tick():
    t=np.arange(int(0.03*SR))/SR; return np.sin(2*np.pi*2400*t)*np.exp(-t*200)*0.15
def place(buf,x,at):
    s=int(at*SR); e=min(len(buf),s+len(x)); buf[s:e]+=x[:e-s]
def save(path,x):
    x=x/max(1e-9,np.abs(x).max())*0.9
    with wave.open(path,'w') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((x*32767).astype(np.int16).tobytes())
if __name__=='__main__':
    cfg=json.load(open(sys.argv[1])); dur=cfg['dur']
    save(sys.argv[2],music(dur))
    sfx=np.zeros(int(dur*SR))
    for c in cfg.get('whoosh',[]): place(sfx,whoosh(),c-0.35)
    for c in cfg.get('impact',[]): place(sfx,impact(),c)
    for c in cfg.get('riser',[]): place(sfx,riser(),c-2.5)
    for a,b in cfg.get('ticks',[]):
        for tt in np.arange(a,b,0.09): place(sfx,tick(),tt)
    save(sys.argv[3],sfx)
