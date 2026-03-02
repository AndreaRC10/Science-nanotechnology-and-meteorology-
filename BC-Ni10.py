#!/usr/bin/env python
# coding: utf-8

# In[12]:


import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import VoigtModel, PolynomialModel
from scipy.integrate import cumulative_trapezoid
import pandas as pd

# === 1. Simula o carga tus datos reales ===
# Simulación con ruido (sólo para ejemplo; reemplázalo con tus datos reales)
binding_energy = np.linspace(525.08, 545.08, 1000)
np.random.seed(0)
noise = np.random.normal(0, 100, binding_energy.size)

# Componentes centrales: piridínico, pirrólico, N-óxido (ligeramente desplazados de los valores de referencia)
peak_positions = [529.7, 531.2, 532.5]
peak_intensities = [30000, 22000, 12000]
peak_widths = [0.5, 0.5, 0.5]

true_signal = (
    peak_intensities[0] * np.exp(-((binding_energy - peak_positions[0]) ** 2) / (2 * (peak_widths[0] ** 2))) +
    peak_intensities[1] * np.exp(-((binding_energy - peak_positions[1]) ** 2) / (2 * (peak_widths[1] ** 2))) +
    peak_intensities[2] * np.exp(-((binding_energy - peak_positions[2]) ** 2) / (2 * (peak_widths[2] ** 2))) 
)
intensity = true_signal + noise

# === 2. Shirley background function ===
def shirley_background(x, y):
    """Computa fondo tipo Shirley para espectros XPS"""
    I0, If = y[0], y[-1]
    integral = cumulative_trapezoid(y[::-1] - If, x[::-1], initial=0)
    shirley = I0 - (I0 - If) * integral[::-1] / integral[-1]
    return shirley

background = shirley_background(binding_energy, intensity)

# === 3. Define modelos de Voigt + fondo polinómico para el ajuste ===
model = PolynomialModel(degree=1, prefix='bkg_')
params = model.guess(intensity - background, x=binding_energy)

for i, (pos, amp, wid) in enumerate(zip(peak_positions, peak_intensities, peak_widths)):
    prefix = f'p{i}_'
    voigt = VoigtModel(prefix=prefix)
    model += voigt
    params.update(voigt.make_params())
    params[f'{prefix}center'].set(value=pos, min=pos-0.5, max=pos+0.5)
    params[f'{prefix}amplitude'].set(value=amp, min=0)
    params[f'{prefix}sigma'].set(value=wid/2.35, min=0.1, max=2.0)  # Aproximación inicial para Voigt

# === 4. Ajuste ===
result = model.fit(intensity, params, x=binding_energy)

# === 5. Visualización ===
fig, ax = plt.subplots(figsize=(10, 6))

# Señal original y ajuste total

ax.plot(binding_energy, result.best_fit, label='Ajuste total', color='red', linewidth=2)

# Fondo

# Curvas individuales con etiquetas conectadas
colors = ['tab:blue', 'tab:orange', 'tab:green']
labels = ['M–O', 'O=C', 'OH-C']

for i, (color, label_text) in enumerate(zip(colors, labels)):
    prefix = f'p{i}_'
    peak = VoigtModel(prefix=prefix).eval(params=result.params, x=binding_energy)
    ax.fill_between(binding_energy, peak, alpha=0.5, color=color, label=label_text)
    
    # Etiqueta con línea conectada
    peak_pos = result.params[f'{prefix}center'].value
    peak_max = np.max(peak)
    
    ax.annotate(
        f"{label_text}\n{peak_pos:.2f} eV",  # Etiqueta con nombre y energía
        xy=(peak_pos, peak_max),
        xytext=(peak_pos + 3.0, peak_max + 50),  # Desplazar la etiqueta hacia afuera
        arrowprops=dict(arrowstyle='-', color=color, lw=1),
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=color, lw=0.8),
        fontsize=11,
        color=color,
        horizontalalignment='left',
        verticalalignment='center'
    )


# Estética
ax.set_xlabel("Energía de enlace (eV)", fontsize=14, weight='bold')
ax.set_ylabel("Intensidad (u.a.)", fontsize=14, weight='bold')
ax.set_title("O 1s BC-Ni10", fontsize=16, weight='bold')
ax.set_xlim(526, 537)
ax.legend()
ax.invert_xaxis()
plt.gca().tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
ax.grid(alpha=0.3)
ax.grid(False)
plt.tight_layout()
plt.show()


# In[ ]:




