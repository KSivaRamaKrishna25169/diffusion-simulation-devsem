
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Depth in nm (from interface into silicon)
x = np.linspace(0, 20, 200)

# Classical: sharp peak at interface
classical = 1e20 * np.exp(-x / 2.0)   # arbitrary decay length

# Quantum (Density Gradient): lower peak, broader, shifted slightly
quantum = 0.7e20 * np.exp(- (x - 0.3) / 3.0)
quantum[x < 0.3] = 0.7e20  # peak shifted by 0.3 nm

plt.figure(figsize=(8,5))
plt.plot(x, classical, 'b-', linewidth=2, label='Classical')
plt.plot(x, quantum, 'r-', linewidth=2, label='Density Gradient (quantum)')
plt.xlabel('Distance from Si-SiO₂ interface (nm)')
plt.ylabel('Electron density (cm⁻³)')
plt.title('Electron density in MOS capacitor (tₒₓ = 1.5 nm)')
plt.yscale('log')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig('Electrons_1.5nm_representative.png', dpi=150)
print('Electrons_1.5nm_representative.png saved')
