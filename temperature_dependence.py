import devsim
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- 1. Define Parameters for Different Temperatures ---
# Temperatures in Kelvin
temperatures_K = [1173, 1273, 1373]  # 900°C, 1000°C, 1100°C
labels = ['T = 900°C', 'T = 1000°C', 'T = 1100°C']
colors = ['blue', 'green', 'red']

# Material constants for Phosphorus diffusion in Silicon
D0 = 10.5  # cm²/s
Ea = 3.66  # eV
k = 8.617e-5  # eV/K
t_diffusion = 1800  # Diffusion time in seconds (30 minutes)

plt.figure(figsize=(8,5))

for T, label, color in zip(temperatures_K, labels, colors):
    # Calculate D and λ
    D = D0 * np.exp(-Ea / (k * T))
    λ = np.sqrt(4 * D * t_diffusion) * 1e4  # Convert from cm to µm
    
    # Create a unique mesh and device name
    mesh_name = f"temp_mesh_{T}"
    device_name = f"temp_device_{T}"
    
    # Create the 1D mesh (same as before)
    devsim.create_1d_mesh(mesh=mesh_name)
    x_start, x_end = 0.0, 1e-3
    spacing = 1e-5
    devsim.add_1d_mesh_line(mesh=mesh_name, pos=x_start, ps=spacing, tag="surface")
    devsim.add_1d_mesh_line(mesh=mesh_name, pos=x_end, ps=spacing, tag="bottom")
    devsim.add_1d_contact(mesh=mesh_name, name="surface", tag="surface", material="metal")
    devsim.add_1d_contact(mesh=mesh_name, name="bottom", tag="bottom", material="metal")
    devsim.add_1d_region(mesh=mesh_name, material="Si", region="silicon", tag1="surface", tag2="bottom")
    devsim.finalize_mesh(mesh=mesh_name)
    devsim.create_device(mesh=mesh_name, device=device_name)
    
    # Define doping profile with the calculated λ
    devsim.node_model(device=device_name, region="silicon", name="NetDoping",
                      equation=f"1e20 * exp(-x / {λ*1e-4:.2e})")
    
    # Get data and plot
    x_cm = devsim.get_node_model_values(device=device_name, region="silicon", name="x")
    doping = devsim.get_node_model_values(device=device_name, region="silicon", name="NetDoping")
    x_um = np.array(x_cm) * 1e4
    doping_arr = np.array(doping)
    plt.semilogy(x_um, doping_arr, color=color, linewidth=2, label=f'{label}, λ ≈ {λ:.2f} µm')
    
    # Clean up
    devsim.delete_device(device=device_name)
    devsim.delete_mesh(mesh=mesh_name)

plt.xlabel("Depth (microns)")
plt.ylabel("Net Doping Concentration (cm⁻³)")
plt.title("Temperature Effect on Diffusion Profile")
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend()
plt.savefig("temperature_dependence.png", dpi=150, bbox_inches='tight')
print("Temperature dependence plot saved as temperature_dependence.png")
