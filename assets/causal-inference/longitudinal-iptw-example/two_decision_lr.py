"""Synthetic A-vs-B two-decision IPTW. All outcomes occur after decision 1.
No clinical claims, missingness, early events or censoring. Python + NumPy.
Uses the previously verified LR fitting helper; does not run its main program.
"""
import json
from pathlib import Path
import runpy
import numpy as np

helper = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'iptw-lr-example' / 'multivariable_iptw.py'))
fit_lr, sigmoid = helper['fit_lr'], helper['sigmoid']
rng = np.random.default_rng(20260910)
n = 6000
age = np.clip(rng.normal(70, 7, n), 50, 90)
age10 = (age-70)/10
d = rng.binomial(1, sigmoid(-.9+.3*age10))
s0 = np.clip(rng.normal(.3*age10+.4*d, 1, n), -2.5, 3)
h = rng.binomial(1, sigmoid(-.4+.25*s0))
x0 = np.column_stack([np.ones(n), age10, d, s0, h])
z0 = rng.binomial(1, sigmoid(x0 @ np.array([-.4,.3,.5,.5,-.4])))
s1 = .5*s0+.2*d-.6*z0+.15*age10+rng.normal(0, .8, n)
x1 = np.column_stack([np.ones(n), age10, d, s0, h, z0, s1])
z1 = rng.binomial(1, sigmoid(x1 @ np.array([-.3,.25,.4,.2,-.2,.8,.7])))
y = rng.binomial(1, sigmoid(-2+.3*age10+.5*d+.3*s0+.6*s1+.15*h-.25*z0-.4*z1))
b0,_=fit_lr(x0,z0);b1,_=fit_lr(x1,z1)
e0=sigmoid(x0@b0);e1=sigmoid(x1@b1)
p0=np.where(z0==1,e0,1-e0);p1=np.where(z1==1,e1,1-e1)
w0=1/p0;factor1=1/p1;w1=w0*factor1
rows=[]
for a,b in [(1,1),(0,0),(1,0),(0,1)]:
 i=int(np.flatnonzero((z0==a)&(z1==b))[0])
 rows.append({'id':i+1,'age10':float(age10[i]),'D':int(d[i]),'S0':float(s0[i]),'H':int(h[i]),'S1':float(s1[i]),'Z0':a,'Z1':b,'e0':float(e0[i]),'e1':float(e1[i]),'w0':float(w0[i]),'factor1':float(factor1[i]),'w1':float(w1[i])})
risks={}
for drug,z in [('AA',1),('BB',0)]:
 mask=(z0==z)&(z1==z)
 risks[drug]={'n':int(mask.sum()),'events':int(y[mask].sum()),'naive_risk':float(y[mask].mean()),'weighted_risk':float(np.average(y[mask],weights=w1[mask])),'weight_sum':float(w1[mask].sum())}
# Verify the separate hand-calculation example, which is not these 6,000 records.
n_path=np.array([64.,5.,30.,30.]);events=np.array([8.,2.,6.,15.])
ww=np.array([2/.8,2/.25,2/.75,2/.5])
assert np.allclose(n_path*ww,[160,40,80,120])
assert np.allclose(events*ww,[20,16,16,60])
assert np.isclose((events[:2]*ww[:2]).sum()/(n_path[:2]*ww[:2]).sum(),.18)
assert np.isclose((events[2:]*ww[2:]).sum()/(n_path[2:]*ww[2:]).sum(),.38)
assert np.allclose(w1,1/(p0*p1))
output={'seed':20260910,'n':n,'model0_features':['intercept','age10','D','S0','H'],'beta0':b0.tolist(),'model1_features':['intercept','age10','D','S0','H','Z0','S1'],'beta1':b1.tolist(),'rows':rows,'risks':risks,'RD':risks['AA']['weighted_risk']-risks['BB']['weighted_risk'],'hand_example_verified':True}
Path(__file__).with_name('results.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
