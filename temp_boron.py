import devsim
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

D0 = 0.76          # cm²/s for Boron in Si
Ea = 3.46          # eV
k = 8.617e-5
t_diffusion = 3600   # 60 min

temperatures_K = [1223, 1323, 1423]   # 950, 1050, 1150°C
labels = ['T = 950°C', 'T = 1050°C', 'T = 1150°C']
colors = ['blue', 'green', 'red']

plt.figure(figsize=(8,5))

for T, label, color in zip(temperatures_K, labels, colors):
    D = D0 * np.exp(-Ea / (k * T))
    λ_cm = np.sqrt(4 * D * t_diffusion)   # characteristic length in cm
    λ_um = λ_cm * 1e4
    mesh_name = f"temp_mesh_{T}"
    device_name = f"temp_device_{T}"
    
    devsim.create_1d_mesh(mesh=mesh_name)
    devsim.add_1d_mesh_line(mesh=mesh_name, pos=0.0, ps=1e-6, tag="surface")
    devsim.add_1d_mesh_line(mesh=mesh_name, pos=1e-3, ps=1e-5, tag="bottom")
    devsim.add_1d_contact(mesh=mesh_name, name="surface", tag="surface", material="metal")
    devsim.add_1d_contact(mesh=mesh_name, name="bottom", tag="bottom", material="metal")
    devsim.add_1d_region(mesh=mesh_name, material="Si", region="silicon", tag1="surface", tag2="bottom")
    devsim.finalize_mesh(mesh=mesh_name)
    devsim.create_device(mesh=mesh_name, device=device_name)
    
    devsim.node_model(device=device_name, region="silicon", name="NetDoping",
                      equation=f"1e20 * exp(-x / {λ_cm:.6e})")
    
    x_cm = devsim.get_node_model_values(device=device_name, region="silicon", name="x")
    doping = devsim.get_node_model_values(device=device_name, region="silicon", name="NetDoping")
    x_um = np.array(x_cm) * 1e4
    doping_arr = np.array(doping)
    plt.semilogy(x_um, doping_arr, color=color, linewidth=2,
                 label=f'{label}, λ = {λ_um:.2f} µm')
    
    devsim.delete_device(device=device_name)
    devsim.delete_mesh(mesh=mesh_name)

plt.xlabel("Depth (microns)")
plt.ylabel("Net Doping Concentration (cm⁻³)")
plt.title("Temperature Dependence: Boron Diffusion (60 min)")
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend()
plt.savefig("temp_boron.png", dpi=150, bbox_inches='tight')
print("Saved: temp_boron.png")
