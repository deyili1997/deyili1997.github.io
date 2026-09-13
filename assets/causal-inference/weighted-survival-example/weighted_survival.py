"""Synthetic A/B time-to-death tutorial. No clinical data or efficacy claims.
Python + NumPy. Weighted KM and one-parameter weighted Cox point estimates.
Independent random censoring plus 12-month administrative end; no competing risks.
Cox routine assumes distinct event times; no SE/CI or full diagnostics provided.
"""
from pathlib import Path
import runpy,json
import numpy as np
helper=runpy.run_path(str(Path(__file__).resolve().parents[1]/'iptw-lr-example'/'multivariable_iptw.py'))
sigmoid,fit_lr=helper['sigmoid'],helper['fit_lr']

def km(time,event,weight,horizon):
    survival=1.;steps=[]
    for t in np.sort(np.unique(time[(event==1)&(time<=horizon)])):
        risk=float(weight[time>=t].sum())
        deaths=float(weight[(time==t)&(event==1)].sum())
        survival*=1-deaths/risk
        steps.append({'time':float(t),'risk_weight':risk,'death_weight':deaths,'survival':survival})
    return {'survival':float(survival),'risk':float(1-survival),'steps':steps}

def cox(time,event,z,weight):
    assert len(np.unique(time[event==1]))==int(event.sum()),'No event ties supported here'
    order=np.argsort(time);t=time[order];d=event[order];a=z[order];w=weight[order]
    ra=np.cumsum((w*a)[::-1])[::-1];rb=np.cumsum((w*(1-a))[::-1])[::-1]
    idx=np.flatnonzero(d==1)
    def score(beta):
        r=np.exp(beta);return float(np.sum(w[idx]*(a[idx]-ra[idx]*r/(ra[idx]*r+rb[idx]))))
    lo,hi=-15.,15.
    assert score(lo)>0 and score(hi)<0,'No finite root in search interval'
    for _ in range(90):
        mid=(lo+hi)/2
        if score(mid)>0:lo=mid
        else:hi=mid
    beta=(lo+hi)/2
    return {'beta':beta,'HR':float(np.exp(beta)),'score':score(beta)}

# Eight-person transparent hand example. These PS values are supplied for teaching,
# not estimated by fitting a multivariable model to these eight people.
t=np.array([2,3,5,6,1,4,4.5,6.],float)
d=np.array([1,0,1,0,1,1,0,0]);z=np.array([1,1,1,1,0,0,0,0])
w=np.array([2,2,4,2,2,4,2,2.],float)
hand={}
for drug,a in [('A',1),('B',0)]:
 m=z==a
 hand[drug]={'weighted':km(t[m],d[m],w[m],6),'unweighted':km(t[m],d[m],np.ones(m.sum()),6)}
assert np.isclose(hand['A']['weighted']['survival'],4/15)
assert np.isclose(hand['B']['weighted']['survival'],.4)
hand['cox']=cox(t,d,z,w)
# Common multiplier preserves weighted Cox estimate; group-specific multipliers
# need not preserve it. Group-wise KM curves are invariant to either scaling.
assert np.isclose(cox(t,d,z,w*3)['HR'],hand['cox']['HR'])
for a in [0,1]:
 m=z==a
 assert np.isclose(km(t[m],d[m],w[m]*(.4 if a else .6),6)['survival'],km(t[m],d[m],w[m],6)['survival'])

rng=np.random.default_rng(20260909);n=3000
age=np.clip(rng.normal(70,7,n),50,90);age10=(age-70)/10
D=rng.binomial(1,sigmoid(-.9+.3*age10))
S=np.clip(rng.normal(.3*age10+.4*D,1,n),-2.5,3)
H=rng.binomial(1,sigmoid(-.4+.25*S))
x=np.column_stack([np.ones(n),age10,D,S,H])
z=rng.binomial(1,sigmoid(x@np.array([-.6,.5,.8,.6,-.5])))
b,_=fit_lr(x,z);ps=sigmoid(x@b)
w=np.where(z==1,1/ps,1/(1-ps));sw=w*np.where(z==1,z.mean(),1-z.mean())
# NEW time-to-event outcomes: do not reuse the binary outcomes of the baseline note.
rate=np.exp(-4+.35*age10+.45*D+.45*S+.15*H-.4*z)
event_time=rng.exponential(1/rate)
loss_time=rng.exponential(36,size=n)
time=np.minimum(np.minimum(event_time,loss_time),12)
event=(event_time<=np.minimum(loss_time,12)).astype(int)
full={'n':n,'PS_beta':b.tolist(),'A_n':int(z.sum()),'B_n':int(n-z.sum())}
for drug,a in [('A',1),('B',0)]:
 m=z==a
 full[drug]={'events':int(event[m].sum()),'losses':int(((loss_time<event_time)&(loss_time<12)&m).sum()),'crude_event_fraction':float(event[m].mean()),'KM_risk':km(time[m],event[m],np.ones(m.sum()),12)['risk'],'weighted_KM_risk':km(time[m],event[m],sw[m],12)['risk']}
 assert np.isclose(km(time[m],event[m],w[m],12)['risk'],full[drug]['weighted_KM_risk'])
full['weighted_cox_stabilized']=cox(time,event,z,sw)
full['weighted_cox_unstabilized']=cox(time,event,z,w)
full['risk_difference']=full['A']['weighted_KM_risk']-full['B']['weighted_KM_risk']
full['risk_ratio']=full['A']['weighted_KM_risk']/full['B']['weighted_KM_risk']
output={'hand':hand,'multivariable':full}
Path(__file__).with_name('results.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
