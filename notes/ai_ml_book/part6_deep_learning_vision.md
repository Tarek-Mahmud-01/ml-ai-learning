# PART VI — Deep Learning and Computer Vision

[📖 Table of contents](README.md) · [← previous part](part5_evaluation_special_ml.md) · [next part →](part7_nlp.md) · [Appendices](appendix.md)

> **Days 48–62 · Category: neural networks (supervised, deep) · Levels: 1 → 3 in every chapter**
> **You will be able to:** build a neural network by hand (forward, loss, backprop), then in PyTorch and Keras; train it well (optimizers, regularization, debugging); and apply CNNs, transfer learning and detection to images.
> **Math you meet here (just-in-time):** activation derivatives (Day 49) · loss functions (50) · backprop = chain rule on matrices (51) · initialization (52) · momentum / Adam moments (55) · BatchNorm (56) · convolution (60) · IoU, mAP (62).
> **Your class notes used:** *Loss Functions, Partial Derivatives & Gradient Descent* (how gradients update neural-network weights).

---

## Chapter 28 — Neural-network foundations (by hand)

> ⚠️ **Common mistakes:** zero weight initialization · forgetting the activation derivative in backprop · wrong tensor shapes · sigmoid in deep hidden layers.

### Level 1 — Beginner: the neuron and the layer
<a id="day-48"></a>
#### ☐ Day 48 — The neuron & the perceptron
- 🧮 **New math today (just-in-time):** the perceptron update rule and linear separability.
- 🧠 **Idea · L1:** a neuron = weighted sum + a bend (activation). One neuron = a linear classifier. It **cannot** solve XOR.
- ➗ **Equation · L1:** `z = w·x + b`, `a = f(z)` · perceptron update `w ← w + η(y − ŷ)x`
- ⌨️ **Build · L2:** perceptron from scratch (AND, OR works; XOR fails) → plot the decision line.
- 📊 **Measure · L2:** epochs until no errors; XOR stays at 50 %.
- 📈 **Improve · L3:** 1 neuron → add a hidden layer (preview of Day 49).
- 🎤 **Interview · L3:** Why can't one neuron solve XOR? · Role of the bias? · Perceptron vs logistic regression?
- ✅ **Done when:** you can explain XOR failure with a drawing.

<a id="day-49"></a>
#### ☐ Day 49 — Multi-layer network: forward pass & activations
- 🧮 **New math today (just-in-time):** activation functions and their derivatives (ReLU, sigmoid, tanh).
- 🧠 **Idea · L1:** stack layers. Without a non-linear activation, many layers = one linear layer.
- ➗ **Equation · L1:** `a⁽ˡ⁾ = f(W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾)` · ReLU `max(0,z)` · sigmoid · tanh · softmax · GELU · parameters of a layer `= n_in·n_out + n_out`
- ⌨️ **Build · L2:** 2-layer forward pass in NumPy with random weights; derivative of every activation; count parameters by hand vs `sum(p.numel())`.
- 📊 **Measure · L2:** shape check for every tensor; saturating sigmoid → tiny gradients.
- 📈 **Improve · L3:** sigmoid → tanh → ReLU: compare output ranges and gradient sizes.
- 🎤 **Interview · L3:** Why non-linear activations? · Why ReLU? · Dying ReLU?
- ✅ **Done when:** you predict every tensor shape before running.


### Level 2 — Intermediate: loss and backpropagation
<a id="day-50"></a>
#### ☐ Day 50 — Loss functions — *your notes: Loss Functions*
- 🧮 **New math today (just-in-time):** loss functions: MSE, MAE, Huber, binary / categorical cross-entropy, hinge.
- 🧠 **Idea · L1:** the loss is the only thing the network "feels". Choose it for the task.
- ➗ **Equation · L1:** MSE `(y−ŷ)²` · MAE `|y−ŷ|` · Huber `½e²` if `|e| ≤ δ` else `δ(|e| − ½δ)` · BCE `−[y log p + (1−y)log(1−p)]` · CE `−Σ y log p` · hinge `max(0, 1 − y·f)` · softmax+CE gradient `= p − y`
- ⌨️ **Build · L2:** all losses from scratch vs `torch.nn`; plot each loss against the error.
- 📊 **Measure · L2:** training with outliers: MSE vs MAE vs Huber.
- 📈 **Improve · L3:** MSE → Huber on noisy targets; BCE with `pos_weight` on imbalance.
- 🎤 **Interview · L3:** Why cross-entropy for classification? · Huber vs MSE? · What is `BCEWithLogitsLoss` and why use it?
- ✅ **Done when:** you can choose a loss for 5 tasks.

<a id="day-51"></a>
#### ☐ Day 51 — Backpropagation by hand
- 🧮 **New math today (just-in-time):** backpropagation = the chain rule applied layer by layer, in matrix form.
- 🧠 **Idea · L1:** the chain rule, applied layer by layer from the loss back to every weight.
- ➗ **Equation · L1:** output error `δ⁽²⁾ = p − y` (softmax + CE) · hidden error `δ⁽¹⁾ = (W⁽²⁾ᵀδ⁽²⁾) ⊙ f′(z⁽¹⁾)` · `∂L/∂W⁽ˡ⁾ = δ⁽ˡ⁾·a⁽ˡ⁻¹⁾ᵀ` · `∂L/∂b⁽ˡ⁾ = δ⁽ˡ⁾`
- ⌨️ **Build · L2:** pen-and-paper backprop for a 2-2-1 net with real numbers; then NumPy; **gradient check** `(L(w+h) − L(w−h))/2h`.
- 📊 **Measure · L2:** analytic vs numeric gradient error < 1e-6.
- 📈 **Improve · L3:** find and fix one bug on purpose (transpose, missing `f′`).
- 🎤 **Interview · L3:** Explain backprop in 3 sentences. · Why is it efficient? · What is a vanishing gradient?
- ✅ **Done when:** you can do one backprop step on paper.


### Level 3 — Advanced: a full network from scratch
<a id="day-52"></a>
#### ☐ Day 52 — Neural network from scratch (NumPy)
- 🧮 **New math today (just-in-time):** weight initialization (He / Xavier) and mini-batch updates.
- 🧠 **Idea · L1:** build the whole loop yourself: forward → loss → backward → update.
- ➗ **Equation · L1:** He init `Var(w) = 2/n_in` · Xavier `Var(w) = 2/(n_in + n_out)` · mini-batch update `w ← w − α·(1/m)Σ∇`
- ⌨️ **Build · L2:** a network class (XOR first, then `digits`); mini-batches; accuracy curve.
- 📊 **Measure · L2:** loss + accuracy per epoch; error analysis on mistakes.
- 📈 **Improve · L3:** zero init (fails — why?) → small random → He init → tuned α.
- 🎤 **Interview · L3:** Why not initialize with zeros? · Mini-batch size trade-offs? · How do you know the net is learning?
- ✅ **Done when:** > 95 % on `digits` with pure NumPy.


## Chapter 29 — PyTorch and the training loop

> ⚠️ **Common mistakes:** forgetting `zero_grad()` · missing `model.eval()` / `no_grad()` at test time · evaluating on training data.

### Level 1–2: tensors, autograd, the loop
<a id="day-53"></a>
#### ☐ Day 53 — PyTorch basics
- 🧠 **Idea · L1:** PyTorch = NumPy + automatic gradients + GPU.
- ➗ **Equation · L1:** `loss.backward()` computes `∂loss/∂θ` for every parameter by the chain rule you did on Day 51.
- ⌨️ **Build · L2:** tensors, `requires_grad`, `autograd`, `nn.Module`, `nn.Linear`; rebuild Day 52's net; **check gradients equal your NumPy gradients**.
- 📊 **Measure · L2:** same loss curve as Day 52.
- 📈 **Improve · L3:** manual weights → `nn.Sequential` → custom `nn.Module`.
- 🎤 **Interview · L3:** What does `zero_grad()` do? · `detach()` vs `no_grad()`? · Static vs dynamic graph?
- ✅ **Done when:** PyTorch and NumPy gradients match.


### Level 3: MNIST end to end
<a id="day-54"></a>
#### ☐ Day 54 — The training loop & MNIST
- 🧠 **Idea · L1:** the 5 steps — zero_grad → forward → loss → backward → step. Datasets, DataLoaders, batches, train/eval mode.
- ➗ **Equation · L1:** accuracy `= correct/total` · epoch = one pass over data
- ⌨️ **Build · L2:** `Dataset` + `DataLoader`; train MNIST; eval loop with `model.eval()` and `no_grad()`; save/load `state_dict`.
- 📊 **Measure · L2:** train vs validation accuracy per epoch; confusion matrix.
- 📈 **Improve · L3:** logistic regression (linear) → 1 hidden layer → 2 hidden layers.
- 🎤 **Interview · L3:** `train()` vs `eval()`? · Why shuffle? · What is an epoch vs a step?
- ✅ **Done when:** > 97 % on MNIST test.


## Chapter 30 — Training better: optimizers, regularization, debugging

> ⚠️ **Common mistakes:** Adam with a huge learning rate · dropout at test time · "loss not decreasing" without first overfitting one batch.

### Level 1: optimizers and schedules
<a id="day-55"></a>
#### ☐ Day 55 — Optimizers & learning-rate schedules
- 🧮 **New math today (just-in-time):** momentum, RMSprop and Adam moment estimates; learning-rate schedules.
- 🧠 **Idea · L1:** smarter steps. Momentum keeps speed. Adam adapts the step per weight.
- ➗ **Equation · L1:** momentum `v ← βv + g; w ← w − αv` · RMSprop `s ← βs + (1−β)g²; w ← w − αg/(√s + ε)` · **Adam** `m ← β₁m + (1−β₁)g; v ← β₂v + (1−β₂)g²; m̂ = m/(1−β₁ᵗ); v̂ = v/(1−β₂ᵗ); w ← w − α·m̂/(√v̂ + ε)` · AdamW = Adam + decoupled weight decay
- ⌨️ **Build · L2:** implement SGD, momentum, Adam by hand on a toy loss; then compare `torch.optim` on MNIST; LR schedules (step, cosine, warm-up); LR range test.
- 📊 **Measure · L2:** loss curves for each optimizer (same seed).
- 📈 **Improve · L3:** SGD → momentum → Adam → AdamW + cosine schedule.
- 🎤 **Interview · L3:** Why Adam? · Adam vs AdamW? · Why warm-up?
- ✅ **Done when:** you can implement Adam without notes.


### Level 2: regularization
<a id="day-56"></a>
#### ☐ Day 56 — Regularization in deep learning
- 🧮 **New math today (just-in-time):** dropout scaling, L2 weight decay, BatchNorm / LayerNorm.
- 🧠 **Idea · L1:** deep nets overfit easily. Tools: dropout, weight decay, normalization, early stopping, augmentation.
- ➗ **Equation · L1:** inverted dropout `a ← a·mask/(1−p)` · L2 `L + (λ/2)Σw²` · **BatchNorm** `x̂ = (x−μ_B)/√(σ_B² + ε); y = γx̂ + β` · LayerNorm = same over features
- ⌨️ **Build · L2:** make a net overfit on purpose; add each fix one by one; implement dropout and BatchNorm forward from scratch.
- 📊 **Measure · L2:** train vs validation curves after each fix.
- 📈 **Improve · L3:** overfit → +weight decay → +dropout → +BatchNorm → +early stopping.
- 🎤 **Interview · L3:** Why does dropout work? · BatchNorm vs LayerNorm? · What does early stopping watch?
- ✅ **Done when:** validation gap shrinks to < 2 %.


### Level 3: debugging and experiment logs
<a id="day-57"></a>
#### ☐ Day 57 — Debugging training & experiment logs
- 🧠 **Idea · L1:** most bugs are silent. Use a checklist.
- ➗ **Equation · L1:** expected initial loss for K classes `≈ ln K` · gradient norm `‖∇‖`
- ⌨️ **Build · L2:** the **debug checklist**: overfit one batch → check initial loss → check shapes → check data labels → gradient clipping `g ← g·min(1, c/‖g‖)` → LR sweep. Log runs to MLflow or a CSV.
- 📊 **Measure · L2:** reproduce 3 classic failures (loss = NaN, loss flat, train ≫ val) and fix each.
- 📈 **Improve · L3:** record the fix for each in `plan120/debug_playbook.md`.
- 🎤 **Interview · L3:** Loss not decreasing — what do you check? · Exploding gradients? · How do you make runs reproducible?
- ✅ **Done when:** your playbook has ≥ 8 symptoms with fixes.


## Chapter 31 — Keras / TensorFlow and tabular deep learning

### Level 2: the second framework
<a id="day-58"></a>
#### ☐ Day 58 — TensorFlow / Keras (same model, second framework)
- 🧠 **Idea · L1:** employers often ask for both. Rebuild the same MNIST model in Keras.
- ➗ **Equation · L1:** same maths; `tf.GradientTape` = autograd.
- ⌨️ **Build · L2:** `Sequential` + `Functional` API; `compile / fit / evaluate`; callbacks (EarlyStopping, ModelCheckpoint); a custom loop with `GradientTape`; save `.keras`.
- 📊 **Measure · L2:** accuracy equals the PyTorch version (± 0.5 %).
- 📈 **Improve · L3:** side-by-side code table PyTorch ↔ Keras (write it as a cheat-sheet).
- 🎤 **Interview · L3:** PyTorch vs TensorFlow? · What does `model.fit` do internally? · When use the functional API?
- ✅ **Done when:** you have the cheat-sheet.


### Level 3: when deep learning beats boosting (and when not)
<a id="day-59"></a>
#### ☐ Day 59 — Tabular deep learning vs boosting
- 🧠 **Idea · L1:** on tables, boosted trees often win. Know *why*, and when a neural net still helps (embeddings, multi-modal).
- ➗ **Equation · L1:** categorical embedding `e = E[idx]` (a learned lookup table).
- ⌨️ **Build · L2:** MLP with embeddings for categoricals vs XGBoost on the same table.
- 📊 **Measure · L2:** score, training time, tuning effort.
- 📈 **Improve · L3:** plain MLP → embeddings → tuned → compare to boosting.
- 🎤 **Interview · L3:** answer **20 questions** (Days 48–59). Why do trees beat NNs on tables?
- ✅ **Checkpoint:** **"MLP on HRM / sales data"** + FastAPI + test.


## Chapter 32 — Computer vision

> **You will learn:** classic CV (OpenCV: filters, edges, colour spaces, histograms, HOG / SIFT), CNNs, transfer learning, detection, segmentation, ViT.
> ⚠️ **Common mistakes:** training a CNN from scratch on 500 images · no augmentation · judging detection by accuracy (use mAP).

### Level 1: convolution and the CNN
<a id="day-60"></a>
#### ☐ Day 60 — Convolution & the CNN
- 🧮 **New math today (just-in-time):** convolution (cross-correlation), output-size and parameter-count formulas.
- 🧠 **Idea · L1:** a small filter slides over the image and looks for patterns (edges → shapes → objects). Shares weights → far fewer parameters than a dense net.
- ➗ **Equation · L1:** `(I∗K)(i,j) = Σₘ Σₙ I(i+m, j+n)·K(m,n)` · output size `⌊(n + 2p − f)/s⌋ + 1` · conv params `= (f·f·C_in + 1)·C_out`
- ⌨️ **Build · L2:** `conv2d` from scratch in NumPy; OpenCV: load, resize, colour spaces, histograms, filters, edge detection (Sobel, Canny), classic features HOG and SIFT; `nn.Conv2d` + pooling CNN on MNIST.
- 📊 **Measure · L2:** CNN vs dense net: accuracy and number of parameters.
- 📈 **Improve · L3:** dense → small CNN → CNN + BatchNorm.
- 🎤 **Interview · L3:** Why do CNNs beat dense nets on images? · Stride, padding, pooling? · Receptive field?
- ✅ **Done when:** you can compute output shape and parameter count on paper.


### Level 2: CIFAR-10, augmentation, transfer learning
<a id="day-61"></a>
#### ☐ Day 61 — CIFAR-10, augmentation & transfer learning
- 🧠 **Idea · L1:** more data via augmentation. Better start via a **pretrained** network (ImageNet = a *dataset*; ResNet = the *model*).
- ➗ **Equation · L1:** residual block `y = F(x) + x`
- ⌨️ **Build · L2:** CNN on CIFAR-10 → augmentation (flip, crop, colour) → fine-tune pretrained ResNet (freeze, then unfreeze).
- 📊 **Measure · L2:** accuracy, per-class errors, confusion matrix, 20 worst images.
- 📈 **Improve · L3:** small CNN → +augmentation → pretrained frozen → fine-tuned (log all).
- 🎤 **Interview · L3:** What is transfer learning? · Why do skip connections help? · Freeze vs fine-tune?
- ✅ **Done when:** ≥ 90 % with transfer learning.


### Level 3: detection, segmentation, ViT
<a id="day-62"></a>
#### ☐ Day 62 — Detection, segmentation, ViT
- 🧮 **New math today (just-in-time):** IoU, Non-Max Suppression, mAP.
- 🧠 **Idea · L1:** classify = *what*; detect = *what + where*; segment = *which pixels*. Vision Transformers cut the image into patches.
- ➗ **Equation · L1:** IoU `= |A∩B|/|A∪B|` · mAP · Non-Max Suppression · ViT patch embedding.
- ⌨️ **Build · L2:** run pretrained YOLO on your own photos; compute IoU by hand; read the U-Net diagram; ViT patch-embedding demo.
- 📊 **Measure · L2:** detections vs your own labels; confidence threshold effect.
- 📈 **Improve · L3:** default threshold → tuned threshold + NMS.
- 🎤 **Interview · L3:** answer **20 questions** (Days 60–62). IoU? mAP? YOLO vs Faster R-CNN?
- ✅ **Checkpoint:** **"Document / receipt image classifier"** (ties to HRM) + FastAPI + test.


---

### ✅ Part VI cheat cards
| Activation | Formula | Use | Watch out |
|---|---|---|---|
| ReLU | `max(0,z)` | default hidden layers | dying ReLU |
| GELU | `z·Φ(z)` | Transformers | slightly slower |
| Sigmoid | `1/(1+e^−z)` | binary output | vanishing gradient |
| Tanh | `(e^z−e^−z)/(e^z+e^−z)` | RNN states | saturates |
| Softmax | `e^zₖ/Σe^zⱼ` | multi-class output | subtract max for stability |

| Task | Output layer | Loss |
|---|---|---|
| Regression | linear | MSE / MAE / Huber |
| Binary classification | 1 unit (logit) | `BCEWithLogitsLoss` |
| Multi-class | K units (logits) | `CrossEntropyLoss` (softmax inside) |
| Multi-label | K units | BCE per label |

| Optimizer | Idea | Typical use |
|---|---|---|
| SGD + momentum | simple, good generalization | CNNs, tuned carefully |
| RMSprop | per-weight step size | RNNs |
| Adam / AdamW | momentum + per-weight step, decoupled weight decay | **default** for Transformers and most models |

[📖 Table of contents](README.md) · [← previous part](part5_evaluation_special_ml.md) · [next part →](part7_nlp.md) · [Appendices](appendix.md)
