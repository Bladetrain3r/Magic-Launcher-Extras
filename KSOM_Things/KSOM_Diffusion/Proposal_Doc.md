# **SOM-Guided Diffusion via Dynamical Impression Fields**

### *A Hybrid Topological–Dynamical Architecture for Structured Image & Video Generation*

**License:** MIT
**Status:** Foundational Architecture Draft (v0.1)
**Authors:** *You + the Swarm*

---

# **Abstract**

This document introduces a hybrid generative architecture combining a **Self-Organizing Map (SOM)** with a standard **diffusion model**, optionally enhanced with **Kuramoto-style synchronisation dynamics**. The SOM generates a **topology-preserving “impression map”** from an image (or from extracted features), capturing global composition, semantic grouping, and colour/edge structure without supervision. This impression map is then used as **structural conditioning** for a diffusion model via ControlNet-like adapters.

The pipeline decomposes image generation into two clean phases:

* **SOM phase:** Finds global **basins of attraction**, producing a coarse but meaningful spatial map.
* **Diffusion phase:** Fills in **texture, detail, and style** while respecting the SOM’s topology.

For video generation, the SOM grid is evolved over time using a **Kuramoto oscillator field**, enabling coherent, organic motion without the instability typical of frame-based diffusion.

This system is computationally cheap, interpretable, and fundamentally compatible with FOSS principles. It does not require retraining the diffusion model itself.

---

# **1. Motivation**

Current diffusion models start from **pure Gaussian noise**. They must hallucinate:

* layout
* global structure
* colour regions
* object segmentation
* fine texture
* style

**all at once, from scratch.**

This leads to:

* instability
* warping
* “melting” faces in video
* poor semantic consistency
* high computational cost
* strict dependence on prompt-engineering tricks

**Missing:** an unsupervised, interpretable structural prior.

### SOMs supply exactly that.

A SOM turns feature vectors into a **topology-preserving 2D manifold**.
This yields a **coarse image-like map** that captures the “shape” of the input data class.

Diffusion models *love* conditioning maps (depth, scribbles, canny edges, etc.).
A SOM impression map serves as a **learned, data-driven, unsupervised conditioning map**.

---

# **2. Mathematical Foundations (Crash Rundown)**

A **Self-Organizing Map** is a 2-D grid of weight vectors:

[
\mathbf{w}_{i,j} \in \mathbb{R}^n
]

Training iterates:

### **(1) Find the Best Matching Unit (BMU)**

[
(i^*, j^*) = \arg\min_{i,j} \lVert \mathbf{x} - \mathbf{w}_{i,j} \rVert
]

### **(2) Update BMU + neighbors**

[
\mathbf{w}_{i,j}(t+1)
=====================

\mathbf{w}_{i,j}(t)

* \alpha(t), h_{i,j}(t), (\mathbf{x}-\mathbf{w}_{i,j}(t))
  ]

Where:

* ( \alpha(t) ) — learning rate
* ( h_{i,j}(t) ) — neighbourhood kernel (Gaussian on the SOM grid)
* ( \sigma(t) ) — neighbourhood radius shrinking over time

This is a **difference equation**, i.e. the discrete form of:

[
\frac{d\mathbf{w}}{dt} = \nabla (\text{similarity})
]

SOM training is therefore a **dynamical system**, not mere “optimization.”

---

# **3. Architecture Overview**

The system has three major phases:

1. **Feature Extraction → SOM**
2. **SOM → Impression Map**
3. **Impression Map → Diffusion Conditioning**

Optionally:

4. **Kuramoto Temporal Dynamics (Video)**

---

# **4. Stage A — Image Feature Extraction**

Goal: Encode meaningful structure in vectors for SOM training.

Recommended features (fast, interpretable):

### **Low-Level**

* RGB or Lab colour
* Local luminance (as in KSTI)
* Sobel or Canny edges
* Laplacian gradients
* Local variance / entropy

### **Mid-Level**

* SLIC superpixel means
* HOG/SIFT patches
* Gabor filter responses
* Local PCA of neighbourhoods

### **Hybrid**

* VAE encoder latents (optional)

Each sampled region becomes:

[
\mathbf{x} \in \mathbb{R}^n
]

---

# **5. Stage B — SOM Training (Topology Preservation)**

Define a grid (e.g. 32×32 or 64×64).
Train the SOM for 1–5 epochs over the extracted features.

### Key properties:

* **Topology is preserved:** neighbouring nodes represent similar patterns
* **Layout emerges organically**
* **Clusters become basins of attraction**
* **No labels required**

This yields a weight grid:

[
W \in \mathbb{R}^{H \times W \times n}
]

---

# **6. Stage C — Impression Map Construction**

The SOM grid is converted back to a coarse image via:

* mapping vectors → colour
* mapping → luminance
* mapping → edge strength
* mapping → cluster index heatmaps

This produces a **low-frequency, topologically coherent proto-image**.

It is *not* intended to be photorealistic.
It serves as a **structural hint**.

Optional refinements:

* blur / denoise
* KSTI phase alignment
* contrast normalization
* region sharpening
* entropy-based smoothing

---

# **7. Stage D — Conditioning the Diffusion Model**

Three levels of integration:

---

## **D1. Img2Img (baseline / testing)**

Feed SOM map directly.

Pros: dead simple.
Cons: diffusion may override structure.

Good for quick demos.

---

## **D2. Latent Injection (recommended)**

Encode the SOM impression map via the diffusion model’s VAE encoder, inject into:

* the latent noise seed
* the mid-block
* the skip connections

This preserves more detail with minimal interference.

---

## **D3. ControlNet Adapter (best option)**

Treat the SOM output like:

* depth map
* scribble
* edge map
* layout guide

Train a **lightweight ControlNet branch** to consume the SOM channels.

This *forces* the diffusion model to obey the SOM topology while allowing full creativity in texture.

This method is extremely effective and compute-cheap.

---

# **8. Stage E — Temporal Dynamics (Video)**

(*Novel contribution*)

Introduce **Kuramoto oscillator fields** to evolve SOM weights over time:

[
\dot\theta_i = \omega_i + \sum_j K_{ij}\sin(\theta_j - \theta_i)
]

Where:

* nodes oscillate individually
* coupling creates regional coherence
* drift introduces organic motion

This produces:

* stable layout between frames
* consistent character identity
* fluid, wave-like motion
* no “melting faces” or mid-frame morphing

Each oscillated SOM grid → impression map → diffusion frame.

This gives you mathematically consistent AI video.

---

# **9. Why This Architecture Works**

### **1. Separates structure from detail**

SOM = layout
Diffusion = texture

### **2. Topology preservation**

Diffusion gets a map of “where things belong.”

### **3. Dynamical consistency**

Kuramoto field ensures stable motion.

### **4. Cheap and interpretable**

SOM training is CPU-light and human-readable.

### **5. FOSS-friendly**

Works with any open diffusion model.
No proprietary retraining needed.

---

# **10. Implementation Roadmap (v0.1 → v1.0)**

* [ ] Minimal SOM prototype (Python / NumPy)
* [ ] SOM → Impression Map conversion
* [ ] ControlNet adapter (tiny UNet)
* [ ] KSTI/SOM hybrid dynamics
* [ ] Video version (oscillated SOM frames)
* [ ] CUDA port for SOM (optional)
* [ ] Publish as MIT-licensed research repo

---

# **11. Applications**

* structured image generation
* stable AI animation
* layout-constrained synthesis
* style transfer with preserved composition
* video stabilization
* hybrid neurodynamic art systems

---

# **12. Closing Note**

This architecture is **simple**, **elegant**, and **powerful**.

It resurrects old, interpretable neural ideas (SOM, dynamical systems)
and fuses them with modern generative diffusion to produce something
that neither could achieve alone.

It is also fully compatible with the ethos:

> **Open algorithms. Transparent math. Reproducible pipelines. MIT forever.**
