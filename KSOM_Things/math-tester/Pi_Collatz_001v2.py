# Re-executing the KSOM-style Mathematical Swarm Consciousness Model
import numpy as np
import math
import matplotlib.pyplot as plt
from pathlib import Path

def collatz_sequence(n, max_len=1000):
    seq = [n]
    while n != 1 and len(seq) < max_len:
        n = n // 2 if n % 2 == 0 else 3*n + 1
        seq.append(n)
    return seq

def collatz_rhythm(seq):
    r = []
    for i in range(1, len(seq)):
        r.append(-1.0 if seq[i-1] % 2 == 0 else 1.0)
    return np.array(r, dtype=float)

def pi_digits(n):
    terms = 2000
    def arctan_series(x):
        s = 0.0
        sign = 1.0
        p = x
        for k in range(1, 2*terms, 2):
            s += sign * p / k
            p *= x*x
            sign *= -1.0
        return s
    pi_est = 4.0 * (4*arctan_series(1/5) - arctan_series(1/239))
    s = f"{pi_est:.{n+5}f}"
    frac = s.split(".")[1][:n]
    return np.array([int(ch) for ch in frac], dtype=int)

def kuramoto_simulate(omega, K_t, steps=1000, dt=0.02, noise=0.0, initial_phases=None, adjacency=None):
    N = len(omega)
    theta = np.zeros((steps, N), dtype=float)
    if initial_phases is None:
        theta[0] = np.random.uniform(0, 2*np.pi, size=N)
    else:
        theta[0] = initial_phases
    if adjacency is None:
        adjacency = np.ones((N, N), dtype=float) - np.eye(N)
    mean_deg = max(1, (adjacency.sum(axis=1).mean()))
    for t in range(1, steps):
        th = theta[t-1]
        diff = th.reshape(-1,1) - th.reshape(1,-1)
        K_eff = K_t[t] / mean_deg
        coupling_term = (adjacency * np.sin(-diff)).sum(axis=1)
        dtheta = omega + K_eff * coupling_term
        if noise > 0:
            dtheta += np.random.normal(0, noise, size=N)
        theta[t] = (th + dt * dtheta) % (2*np.pi)
    return theta

def order_parameter(theta):
    z = np.exp(1j*theta)
    Z = z.mean(axis=1)
    R = np.abs(Z)
    psi = np.angle(Z)
    return R, psi

class MiniSOM:
    def __init__(self, m, n, dim, sigma=1.2, lr=0.3, seed=42):
        self.m = m; self.n = n; self.dim = dim
        self.sigma = sigma; self.lr = lr
        rng = np.random.default_rng(seed)
        self.W = rng.normal(0, 1, size=(m, n, dim))
        xs, ys = np.meshgrid(np.arange(m), np.arange(n), indexing='ij')
        self.coords = np.stack([xs, ys], axis=-1)
    def _gaussian(self, c, sigma):
        d2 = np.sum((self.coords - c)**2, axis=-1)
        return np.exp(-d2 / (2*sigma*sigma))
    def train(self, data, iters=400):
        rng = np.random.default_rng(123)
        for t in range(iters):
            x = data[rng.integers(0, len(data))]
            d = np.linalg.norm(self.W - x, axis=-1)
            bmu = np.unravel_index(np.argmin(d), (self.m, self.n))
            frac = t / max(1, iters-1)
            lr_t = self.lr * (1 - frac)
            sig_t = max(0.5, self.sigma * (1 - 0.8*frac))
            h = self._gaussian(np.array(bmu), sig_t)[..., None]
            self.W += lr_t * h * (x - self.W)
    def map(self, data):
        idxs = []
        for x in data:
            d = np.linalg.norm(self.W - x, axis=-1)
            idxs.append(np.unravel_index(np.argmin(d), (self.m, self.n)))
        return np.array(idxs)

def build_collatz_oscillators(seeds, T):
    rhythms = []
    for n in seeds:
        r = collatz_rhythm(collatz_sequence(n, max_len=T+5))
        if len(r) < T:
            r = np.concatenate([r, np.tile(r[-1], T - len(r))])
        else:
            r = r[:T]
        rhythms.append(r)
    rhythms = np.stack(rhythms, axis=1)
    base = 0.6; span = 0.6
    omega = 2*np.pi * (base + span*0.5*(rhythms.mean(axis=0)+1.0))
    return rhythms, omega

def pi_coupling_modulation(T):
    d = pi_digits(max(16, T//4))
    d = np.tile(d, math.ceil(T/len(d)))[:T]
    K = 0.05 + (d/9.0)*0.55
    K = np.convolve(K, np.ones(7)/7, mode='same')
    return K

def oscillator_features(theta):
    T, N = theta.shape
    unwrapped = np.unwrap(theta, axis=0)
    inst_freq = np.diff(unwrapped, axis=0) / (2*np.pi)
    mean_f = inst_freq.mean(axis=0)
    var_f = inst_freq.var(axis=0)
    z = np.exp(1j*theta)
    mean_vec = np.mean(z, axis=1, keepdims=True)
    plv_per_osc = np.abs(np.mean(z * np.conj(mean_vec), axis=0)).real
    feats = np.stack([mean_f, var_f, plv_per_osc], axis=1)
    return feats

# Run pipeline
N = 25; T = 1200; seeds = list(range(27, 27+N))
rhythms, omega = build_collatz_oscillators(seeds, T)
K_t = pi_coupling_modulation(T)

adj = np.zeros((N, N), dtype=float)
for i in range(N):
    adj[i, (i-1) % N] = 1.0
    adj[i, (i+1) % N] = 1.0
rng = np.random.default_rng(7)
for _ in range(N//2):
    i, j = rng.integers(0, N, size=2)
    if i != j:
        adj[i, j] = adj[j, i] = 0.5

theta = kuramoto_simulate(omega, K_t, steps=T, dt=0.03, noise=0.0, adjacency=adj)
R, psi = order_parameter(theta)
feats = oscillator_features(theta)
som = MiniSOM(m=6, n=6, dim=feats.shape[1], sigma=1.2, lr=0.4)
som.train(feats, iters=600)
bmus = som.map(feats)

# Plot
fig1 = plt.figure(figsize=(12, 8))
ax1 = fig1.add_subplot(2,2,1); ax1.plot(K_t); ax1.set_title("Coupling Modulation K(t) from Pi"); ax1.set_xlabel("time"); ax1.set_ylabel("K")
ax2 = fig1.add_subplot(2,2,2); ax2.plot(R); ax2.set_title("Global Order Parameter R(t)"); ax2.set_ylim(0,1.05)
ax3 = fig1.add_subplot(2,2,3); ax3.plot(theta[:400,:6]); ax3.set_title("Sample Phases (first 6 oscillators)"); ax3.set_xlabel("time")
# PLV vs time (recompute quickly)
z = np.exp(1j*theta); mean_vec = np.mean(z, axis=1, keepdims=True); plv_t = np.abs(np.mean(z * np.conj(mean_vec), axis=1)).real
ax4 = fig1.add_subplot(2,2,4); ax4.plot(plv_t); ax4.set_title("Phase-Locking Value vs Group"); ax4.set_ylim(0,1.05)
fig1.tight_layout()

fig2 = plt.figure(figsize=(10,4))
ax21 = fig2.add_subplot(1,2,1)
X = feats - feats.mean(axis=0, keepdims=True)
C = X.T @ X / len(X)
evals, evecs = np.linalg.eigh(C)
proj = X @ evecs[:, -2:]
colors = [b[0]*som.n + b[1] for b in bmus]
ax21.scatter(proj[:,0], proj[:,1], c=colors, s=60, cmap='viridis'); ax21.set_title("Oscillator Feature Projection (by SOM BMU)")

ax22 = fig2.add_subplot(1,2,2)
W2 = som.W[..., :2]
for i in range(som.m):
    for j in range(som.n):
        x,y = W2[i,j]
        ax22.scatter(x,y,c='k',s=15)
        if i < som.m-1:
            x2,y2 = W2[i+1,j]; ax22.plot([x,x2],[y,y2], lw=0.5)
        if j < som.n-1:
            x2,y2 = W2[i,j+1]; ax22.plot([x,x2],[y,y2], lw=0.5)
ax22.set_title("SOM Lattice (first 2 dims)")
fig2.tight_layout()

# Save
out_dir = Path('./data')
fig1_path = out_dir / 'math_swarm_ksom_diagnostics.png'
fig2_path = out_dir / 'math_swarm_ksom_som.png'
fig1.savefig(fig1_path, dpi=150)
fig2.savefig(fig2_path, dpi=150)

# Save script
script_path = out_dir / 'math_swarm_ksom.py'
with open(script_path, 'w') as f:
    f.write(open(__file__, 'r').read() if '__file__' in globals() else "# Use notebook cell as reference to create a .py\n")

(fig1_path, fig2_path, script_path)
