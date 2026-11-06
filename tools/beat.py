import numpy as np, wave
sr=44100;bpm=118;beat=60/bpm;dur=48;n=int(sr*dur);out=np.zeros(n)
def add(w,s):
    if s>=n: return
    e=min(n,s+len(w));out[s:e]+=w[:e-s]
def note(f,start,length,amp):
    tt=np.arange(int(length*sr))/sr
    add((np.sin(2*np.pi*f*tt)+0.4*np.sin(4*np.pi*f*tt)+0.2*np.sin(6*np.pi*f*tt))*np.exp(-tt*3.5)*amp,int(start*sr))
chords=[[220,261.6,329.6],[174.6,220,261.6],[261.6,329.6,392],[196,246.9,293.7]]
for b in range(int(dur/(4*beat))+1):
    c=chords[b%4]
    for k in range(8): note(c[k%3]*2,b*4*beat+k*beat/2,beat*0.9,0.08)
    for f in c: note(f,b*4*beat,4*beat,0.05)
    note(c[0]/2,b*4*beat,2*beat,0.18)
rng=np.random.default_rng(1)
for k in range(int(dur/beat)):
    tt=np.arange(int(0.25*sr))/sr
    add(np.sin(2*np.pi*(55+90*np.exp(-tt*30))*tt)*np.exp(-tt*9)*0.6,int(k*beat*sr))
    L=int(0.05*sr);add(rng.standard_normal(L)*np.exp(-np.arange(L)/sr*80)*0.08,int((k+0.5)*beat*sr))
    if k%2: L=int(0.15*sr);add(rng.standard_normal(L)*np.exp(-np.arange(L)/sr*25)*0.18,int(k*beat*sr))
f=int(2*sr);out[-f:]*=np.linspace(1,0,f);h=int(0.5*sr);out[:h]*=np.linspace(0,1,h)
out=out/np.abs(out).max()*0.9
w=wave.open("beat.wav","wb");w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((out*32767).astype(np.int16).tobytes());w.close()
