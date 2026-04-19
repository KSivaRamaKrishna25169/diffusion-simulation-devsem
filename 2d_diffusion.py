import devsim
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Create a 2D mesh
devsim.create_2d_mesh(mesh="my_2d_mesh")

# Define mesh lines in x-direction (width)
x_points = np.linspace(0, 5e-4, 20)  # 0 to 5 µm
for x in x_points:
    devsim.add_2d_mesh_line(mesh="my_2d_mesh", dir="x", pos=x)

# Define mesh lines in y-direction (depth)
y_points = np.linspace(0, 1e-3, 40)  # 0 to 10 µm
for y in y_points:
    devsim.add_2d_mesh_line(mesh="my_2d_mesh", dir="y", pos=y)

# Add contacts at top (y_max) and bottom (y_min)
devsim.add_2d_contact(mesh="my_2d_mesh", name="top", interface="y_max", material="metal")
devsim.add_2d_contact(mesh="my_2d_mesh", name="bottom", interface="y_min", material="metal")

# Add the silicon region between the contacts
devsim.add_2d_region(mesh="my_2d_mesh", region="silicon", material="Si",
                     xl=0, xh=5e-4, yl=0, yh=1e-3,
                     tag1="top", tag2="bottom")
devsim.finalize_mesh(mesh="my_2d_mesh")

# Create device
devsim.create_device(mesh="my_2d_mesh", device="my_2d_device")

# Doping profile: exponential decay in y (depth), constant in x
devsim.node_model(device="my_2d_device", region="silicon", name="NetDoping",
                  equation="1e20 * exp(-y / 0.5e-4)")

# Get node coordinates and doping values
x_coords = devsim.get_node_model_values(device="my_2d_device", region="silicon", name="x")
y_coords = devsim.get_node_model_values(device="my_2d_device", region="silicon", name="y")
doping = devsim.get_node_model_values(device="my_2d_device", region="silicon", name="NetDoping")

# Convert to numpy arrays and to microns
x_arr = np.array(x_coords) * 1e4
y_arr = np.array(y_coords) * 1e4
doping_arr = np.array(doping)

# Plot as a scatter plot with color mapping
plt.figure(figsize=(8,6))
sc = plt.scatter(x_arr, y_arr, c=np.log10(doping_arr), cmap='viridis', s=1)
plt.colorbar(sc, label='log10(Doping Concentration [cm⁻³])')
plt.xlabel("Width (microns)")
plt.ylabel("Depth (microns)")
plt.title("2D Diffusion Profile (Exponential Decay in Depth)")
plt.gca().invert_yaxis()  # depth increases downward
plt.savefig("2d_diffusion.png", dpi=150, bbox_inches='tight')
print("2D diffusion plot saved as 2d_diffusion.png")
