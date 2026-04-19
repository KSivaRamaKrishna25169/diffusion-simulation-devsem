import devsim
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Parameters
D0 = 10.5  # cm²/s, for P in Si
Ea = 3.66  # eV
k = 8.617e-5  # eV/K
T = 1273  # K (1000°C)
D = D0 * np.exp(-Ea / (k * T))  # cm²/s

# Times (seconds)
times = [0, 60, 300, 900, 1800]  # 0, 1, 5, 15, 30 min
labels = [f't = {t//60} min' if t>0 else 'Initial' for t in times]

# Dose (atoms/cm²) – typical for a pre-deposition
Q = 1e14

plt.figure(figsize=(8,5))

for t, label in zip(times, labels):
    # Create unique names
    mesh_name = f"mesh_t{t}"
    device_name = f"device_t{t}"
    
    # 1D mesh
    devsim.create_1d_mesh(mesh=mesh_name)
    devsim.add_1d_mesh_line(mesh=mesh_name, pos=0.0, ps=1e-6, tag="surface")
    devsim.add_1d_mesh_line(mesh=mesh_name, pos=1e-3, ps=1e-5, tag="bottom")
    devsim.add_1d_contact(mesh=mesh_name, name="surface", tag="surface", material="metal")
    devsim.add_1d_contact(mesh=mesh_name, name="bottom", tag="bottom", material="metal")
    devsim.add_1d_region(mesh=mesh_name, material="Si", region="silicon", tag1="surface", tag2="bottom")
    devsim.finalize_mesh(mesh=mesh_name)
    devsim.create_device(mesh=mesh_name, device=device_name)
    
    # Gaussian profile: N(x) = (Q / sqrt(π σ²)) * exp(-x² / σ²)
    # σ² = 2 D t  (for t>0); for t=0, use a very small σ to represent the initial thin layer
    if t == 0:
        sigma_sq = 2 * D * 1e-6  # effectively zero, but small enough to avoid division by zero
    else:
        sigma_sq = 2 * D * t
    amplitude = Q / np.sqrt(np.pi * sigma_sq)
    # Build the equation string – careful with exponent: use pow(x,2) or x*x
    eqn = f"{amplitude:.6e} * exp( - (x * x) / {sigma_sq:.6e} )"
    devsim.node_model(device=device_name, region="silicon", name="NetDoping", equation=eqn)
    
    # Get data
    x_cm = devsim.get_node_model_values(device=device_name, region="silicon", name="x")
    doping = devsim.get_node_model_values(device=device_name, region="silicon", name="NetDoping")
    x_um = np.array(x_cm) * 1e4
    doping_arr = np.array(doping)
    plt.semilogy(x_um, doping_arr, linewidth=2, label=label)
    
    # Clean up
    devsim.delete_device(device=device_name)
    devsim.delete_mesh(mesh=mesh_name)

plt.xlabel("Depth (microns)")
plt.ylabel("Doping Concentration (cm⁻³)")
plt.title("Transient Diffusion: Gaussian Profile Broadening Over Time")
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend()
plt.savefig("transient_diffusion.png", dpi=150, bbox_inches='tight')
print("Transient diffusion plot saved as transient_diffusion.png")
