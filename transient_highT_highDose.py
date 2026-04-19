import devsim
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Parameters
D0 = 10.5          # cm²/s, P in Si
Ea = 3.66          # eV
k = 8.617e-5       # eV/K
T = 1373           # 1100°C
D = D0 * np.exp(-Ea / (k * T))

times = [0, 60, 300, 900, 1800]
labels = [f't = {t//60} min' if t>0 else 'Initial' for t in times]
Q = 2e14           # higher dose

plt.figure(figsize=(8,5))

for t, label in zip(times, labels):
    mesh_name = f"mesh_t{t}"
    device_name = f"device_t{t}"
    
    devsim.create_1d_mesh(mesh=mesh_name)
    devsim.add_1d_mesh_line(mesh=mesh_name, pos=0.0, ps=1e-6, tag="surface")
    devsim.add_1d_mesh_line(mesh=mesh_name, pos=1e-3, ps=1e-5, tag="bottom")
    devsim.add_1d_contact(mesh=mesh_name, name="surface", tag="surface", material="metal")
    devsim.add_1d_contact(mesh=mesh_name, name="bottom", tag="bottom", material="metal")
    devsim.add_1d_region(mesh=mesh_name, material="Si", region="silicon", tag1="surface", tag2="bottom")
    devsim.finalize_mesh(mesh=mesh_name)
    devsim.create_device(mesh=mesh_name, device=device_name)
    
    if t == 0:
        sigma_sq = 2 * D * 1e-6
    else:
        sigma_sq = 2 * D * t
    amplitude = Q / np.sqrt(np.pi * sigma_sq)
    eqn = f"{amplitude:.6e} * exp( - (x * x) / {sigma_sq:.6e} )"
    devsim.node_model(device=device_name, region="silicon", name="NetDoping", equation=eqn)
    
    x_cm = devsim.get_node_model_values(device=device_name, region="silicon", name="x")
    doping = devsim.get_node_model_values(device=device_name, region="silicon", name="NetDoping")
    x_um = np.array(x_cm) * 1e4
    doping_arr = np.array(doping)
    plt.semilogy(x_um, doping_arr, linewidth=2, label=label)
    
    devsim.delete_device(device=device_name)
    devsim.delete_mesh(mesh=mesh_name)

plt.xlabel("Depth (microns)")
plt.ylabel("Doping Concentration (cm⁻³)")
plt.title("Transient Diffusion: Higher Temp (1100°C) & Higher Dose (2e14)")
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend()
plt.savefig("transient_highT_highDose.png", dpi=150, bbox_inches='tight')
print("Saved: transient_highT_highDose.png")
