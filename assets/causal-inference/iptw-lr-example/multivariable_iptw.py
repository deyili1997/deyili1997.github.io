"""Reproducible synthetic teaching example; no clinical data or efficacy claims.
Run with Python + NumPy. Outputs JSON beside this script.
a=1 means initiation of drug A; a=0 means initiation of active comparator B.
Both groups receive treatment. y is a fully observed one-year hospitalization indicator.
The script generates an already-eligible cohort; it does not implement EHR screening.
"""
import json
from pathlib import Path
import numpy as np


def sigmoid(z):
    return np.exp(-np.logaddexp(0.0, -z))


def fit_lr(x, a):
    """Unpenalized logistic MLE via Newton steps, with loss backtracking."""
    b = np.zeros(x.shape[1])
    for iteration in range(100):
        p = sigmoid(x @ b)
        score = x.T @ (a - p)
        if np.max(np.abs(score)) < 1e-8:
            return b, iteration
        information = x.T @ ((p * (1-p))[:, None] * x)
        delta = np.linalg.solve(information, score)
        loss = np.sum(np.logaddexp(0, x @ b) - a * (x @ b))
        step = 1.0
        while step > 1e-10:
            candidate = b + step * delta
            new_loss = np.sum(np.logaddexp(0, x @ candidate) - a * (x @ candidate))
            if new_loss <= loss + 1e-10:
                b = candidate
                break
            step *= .5
        else:
            raise RuntimeError('Newton update failed')
    raise RuntimeError('LR failed to converge')


def moments(x, w):
    mean = np.sum(w*x)/w.sum()
    var = w.sum()/(w.sum()**2-np.sum(w*w))*np.sum(w*(x-mean)**2)
    return float(mean), float(var)


def main():
    rng = np.random.default_rng(20260909)
    n = 3000
    age = np.clip(rng.normal(70, 7, n), 50, 90)
    age10 = (age-70)/10
    diabetes = rng.binomial(1, sigmoid(-.9+.3*age10))
    severity = np.clip(rng.normal(0.3*age10+.4*diabetes, 1, n), -2.5, 3)
    prior = rng.binomial(1, sigmoid(-.4+.25*severity))
    x = np.column_stack([np.ones(n), age10, diabetes, severity, prior])
    truth = np.array([-.6, .5, .8, .6, -.5])
    a = rng.binomial(1, sigmoid(x @ truth))
    # Treatment has a constant -0.4 conditional log-odds effect in this generator.
    y0prob = sigmoid(-2.3+.45*age10+.55*diabetes+.6*severity+.15*prior)
    y1prob = sigmoid(-2.3+.45*age10+.55*diabetes+.6*severity+.15*prior-.4)
    y = rng.binomial(1, np.where(a == 1, y1prob, y0prob))
    b, iterations = fit_lr(x, a)
    ps = sigmoid(x @ b)
    w = np.where(a == 1, 1/ps, 1/(1-ps))
    sw = w*np.where(a == 1, a.mean(), 1-a.mean())
    att = np.where(a == 1, 1.0, ps/(1-ps))
    diagnostics=[]
    for name, values in [('age',age),('diabetes',diabetes),('severity',severity),('prior',prior)]:
        row={'variable':name}
        for label, weights in [('before',np.ones(n)),('after',sw)]:
            m1,v1=moments(values[a==1],weights[a==1]);m0,v0=moments(values[a==0],weights[a==0])
            row[label]={'treated_mean':m1,'control_mean':m0,'smd':abs(m1-m0)/np.sqrt((v1+v0)/2)}
        diagnostics.append(row)
    risks={}
    for label, weights in [('crude',np.ones(n)),('iptw',w),('stabilized',sw),('att',att)]:
        r1=float(np.average(y[a==1],weights=weights[a==1]));r0=float(np.average(y[a==0],weights=weights[a==0]))
        risks[label]={'r1':r1,'r0':r0,'rd':r1-r0,'rr':r1/r0}
    assert np.allclose(list(risks['iptw'].values()),list(risks['stabilized'].values()))
    assert np.max(np.abs(x.T@(a-ps)))<1e-7
    rows=[]
    for i in range(8):
        rows.append(dict(id=i+1,age=float(age[i]),age10=float(age10[i]),diabetes=int(diabetes[i]),severity=float(severity[i]),prior=int(prior[i]),a=int(a[i]),y=int(y[i]),eta=float(x[i]@b),ps=float(ps[i]),weight=float(w[i]),sw=float(sw[i])))
    output={'seed':20260909,'n':n,'treated':int(a.sum()),'control':int(n-a.sum()),'treated_fraction':float(a.mean()),'coefficient_names':['intercept','age10','diabetes','severity','prior'],'generating_coefficients':truth.tolist(),'fitted_coefficients':b.tolist(),'iterations':iterations,'score_max_abs':float(np.max(np.abs(x.T@(a-ps)))),'rows':rows,'balance':diagnostics,'risks':risks,'synthetic_expected_risks':{'r1':float(y1prob.mean()),'r0':float(y0prob.mean())},'weight_diagnostics':{'ps_min':float(ps.min()),'ps_max':float(ps.max()),'sw_quantiles':np.quantile(sw,[0,.5,.95,.99,1]).tolist(),'ess_treated':float(sw[a==1].sum()**2/np.sum(sw[a==1]**2)),'ess_control':float(sw[a==0].sum()**2/np.sum(sw[a==0]**2))}}
    # Outcome regression + standardization on the identical eligible cohort.
    outcome_x = np.column_stack([x, a])
    outcome_beta, _ = fit_lr(outcome_x, y)
    all_a = outcome_x.copy(); all_a[:, -1] = 1
    all_b = outcome_x.copy(); all_b[:, -1] = 0
    risk_a = float(sigmoid(all_a @ outcome_beta).mean())
    risk_b = float(sigmoid(all_b @ outcome_beta).mean())
    output['g_computation'] = {
        'coefficient_names': ['intercept', 'age10', 'diabetes', 'severity', 'prior', 'drug_A'],
        'fitted_coefficients': outcome_beta.tolist(),
        'r1': risk_a, 'r0': risk_b, 'rd': risk_a-risk_b, 'rr': risk_a/risk_b,
    }
    destination=Path(__file__).with_name('results.json')
    destination.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))

if __name__=='__main__':
    main()
