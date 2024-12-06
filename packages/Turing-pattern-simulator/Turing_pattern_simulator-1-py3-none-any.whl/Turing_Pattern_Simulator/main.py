import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter, FuncAnimation
import os
from matplotlib.gridspec import GridSpec

def simulate_turing_pattern(grid_size=100, time_steps=10000, F=0.04, k=0.06, D_u=0.16, D_v=0.08, 
                            frame_interval=100, add_noise=False, noise_U_to_V=0.05, noise_V_to_U=0.05):

    U = np.ones((grid_size, grid_size))
    V = np.zeros((grid_size, grid_size))



    U[grid_size // 2 - 10:grid_size // 2 + 10, grid_size // 2 - 10:grid_size // 2 + 10] = 0.50
    V[grid_size // 2 - 10:grid_size // 2 + 10, grid_size // 2 - 10:grid_size // 2 + 10] = 0.25

    if add_noise:
        noise_U = np.random.normal(0, noise_U_to_V, (grid_size, grid_size))
        noise_V = np.random.normal(0, noise_V_to_U, (grid_size, grid_size))
        U += noise_U
        V += noise_V
        U = np.clip(U, 0, 1)  
        V = np.clip(V, 0, 1) 

    history = []
    time_points = []

    for step in range(time_steps):
        laplacian_U = (np.roll(U, 1, axis=0) + np.roll(U, -1, axis=0) +
                       np.roll(U, 1, axis=1) + np.roll(U, -1, axis=1) - 4 * U)
        laplacian_V = (np.roll(V, 1, axis=0) + np.roll(V, -1, axis=0) +
                       np.roll(V, 1, axis=1) + np.roll(V, -1, axis=1) - 4 * V)
        
        reaction = U * V**2
        U += D_u * laplacian_U - reaction + F * (1 - U)
        V += D_v * laplacian_V + reaction - (F + k) * V

        if step % frame_interval == 0:
            history.append(V.copy())
            time_points.append(step)

    return history, time_points

def save_gif(history, time_points, filename='turing_pattern.gif', fps=10, cmap='viridis', 
             params=None, unit_label="Concentration of V"):

    fig, ax = plt.subplots(figsize=(6, 6))
    cax = ax.imshow(history[0], cmap=cmap, extent=[-1, 1, -1, 1])
    ax.axis('off')
    cb = fig.colorbar(cax, ax=ax, orientation='vertical', pad=0.05)
    cb.set_label(unit_label)

    if params:
        param_text = f"F = {params['F']}, k = {params['k']}\nD_u = {params['D_u']}, D_v = {params['D_v']}"
        fig.text(0.5, 0.93, param_text, ha='center', fontsize=12)  


    def update(frame_idx):
        cax.set_array(history[frame_idx])
        ax.set_title(f"Time Step: {time_points[frame_idx]}", fontsize=10)
        return cax,

    anim = FuncAnimation(fig, update, frames=len(history), blit=True)
    anim.save(filename, writer=PillowWriter(fps=fps))
    plt.close(fig)
    print(f"GIF saved to {filename}")

def save_png(final_state, time_point, filename='turing_pattern.png', cmap='viridis', 
             params=None, unit_label="Concentration of V"):

    fig, ax = plt.subplots(figsize=(6, 6))
    cax = ax.imshow(final_state, cmap=cmap, extent=[-1, 1, -1, 1])
    ax.axis('off')
    cb = fig.colorbar(cax, ax=ax, orientation='vertical', pad=0.05)
    cb.set_label(unit_label)

    if params:
        param_text = f"F = {params['F']}, k = {params['k']}\nD_u = {params['D_u']}, D_v = {params['D_v']}"
        fig.text(0.5, 0.93, param_text, ha='center', fontsize=12)

    fig.text(0.5, 0.02, f"Time Step: {time_point}", ha='center', fontsize=10)

    plt.savefig(filename, dpi=150, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    print(f"PNG saved to {filename}")

def simulator(grid_size=100, time_steps=10000, F=0.04, k=0.06, D_u=0.16, D_v=0.08,
                   frame_interval=100, output_type='gif', filename='turing_pattern', fps=10, 
                   add_noise=False, noise_U_to_V=0.05, noise_V_to_U=0.05):

    print(f"Running simulation: grid_size={grid_size}, time_steps={time_steps}, F={F}, k={k}, D_u={D_u}, D_v={D_v}, add_noise={add_noise}")
    history, time_points = simulate_turing_pattern(grid_size, time_steps, F, k, D_u, D_v, frame_interval, add_noise, noise_U_to_V, noise_V_to_U)

    params = {
        "F": F,
        "k": k,
        "D_u": D_u,
        "D_v": D_v
    }

    if output_type == 'gif':
        save_gif(history, time_points, filename=f'{filename}.gif', fps=fps, params=params)
    elif output_type == 'png':
        save_png(history[-1], time_steps, filename=f'{filename}.png', params=params)

def sweeper_1d(param_name, param_range, simulator_args, output_dir='sweeper_results', output_type='matrix'):

    import os
    import numpy as np
    import matplotlib.pyplot as plt

    os.makedirs(output_dir, exist_ok=True)

    start, stop, step = param_range
    param_values = np.arange(start, stop + step, step)

    print(f"Starting 1D sweeper for parameter '{param_name}' with range {param_range}...")

    images = []  

    for value in param_values:
        print(f"Running simulation with {param_name} = {value:.4f}...")
        simulator_args[param_name] = value

        filename = f"{param_name}_{value:.4f}"
        filepath = os.path.join(output_dir, filename) 

        simulator(**simulator_args, output_type='png', filename=filepath)

        png_filepath = f"{filepath}.png"  
        if not os.path.exists(png_filepath):
            raise FileNotFoundError(f"Simulator failed to generate the file: {png_filepath}")

        img = plt.imread(png_filepath)
        images.append((img, value))

    if output_type == 'matrix':
        print(f"Creating matrix plot for parameter '{param_name}'...")
        
        fig, axes = plt.subplots(1, len(images), figsize=(len(images) * 3, 4), constrained_layout=True)
        if len(images) == 1:
            axes = [axes]  

        for ax, (img, value) in zip(axes, images):
            ax.imshow(img)
            ax.axis('off')
            ax.set_title(f"{param_name} = {value:.4f}", fontsize=10, fontweight='bold')

        matrix_filename = os.path.join(output_dir, f"{param_name}_matrix.png")
        plt.savefig(matrix_filename, dpi=200)
        plt.close(fig)
        print(f"Matrix plot saved to {matrix_filename}")

    print("1D sweeping complete!")



def sweeper_2d(param1_name, param1_range, param2_name, param2_range, simulator_args, 
                      output_dir='sweeper_results_2d', output_type='matrix'):


    os.makedirs(output_dir, exist_ok=True)

    param1_values = np.arange(*param1_range)
    param2_values = np.arange(*param2_range)

    print(f"Starting 2D sweeper for parameters '{param1_name}' and '{param2_name}'...")

    images = [] 

    for value2 in param2_values:
        row_images = []
        for value1 in param1_values:
            print(f"Running simulation with {param1_name} = {value1:.4f}, {param2_name} = {value2:.4f}...")
            simulator_args[param1_name] = value1
            simulator_args[param2_name] = value2

            filename = f"{param1_name}_{value1:.4f}_{param2_name}_{value2:.4f}"
            filepath = os.path.join(output_dir, filename)  # No need to add ".png" here

            simulator(**simulator_args, output_type='png', filename=filepath)

            png_filepath = f"{filepath}.png"
            if not os.path.exists(png_filepath):
                raise FileNotFoundError(f"Simulator failed to generate the file: {png_filepath}")

            img = plt.imread(png_filepath)
            row_images.append(img)
        images.append((row_images, value2))

    # Generate matrix output
    if output_type == 'matrix':
        print(f"Creating matrix plot for parameters '{param1_name}' and '{param2_name}'...")
        
        num_rows = len(images)
        num_cols = len(images[0][0])
        
        fig = plt.figure(figsize=(num_cols * 3, num_rows * 3))
        gs = GridSpec(num_rows + 1, num_cols + 1, figure=fig, width_ratios=[0.5] + [1] * num_cols, 
                      height_ratios=[1] * num_rows + [0.5])

        for i, (row_images, param2_value) in enumerate(images):
            for j, img in enumerate(row_images):
                ax = fig.add_subplot(gs[i, j + 1])
                ax.imshow(img)
                ax.axis('off')

        for j, param1_value in enumerate(param1_values):
            ax = fig.add_subplot(gs[num_rows, j + 1])
            ax.axis('off')
            ax.text(0.5, 0.5, f"{param1_value:.4f}", fontsize=20, ha='center', va='center')
        fig.text(0.5, 0.02, f"{param1_name}", fontsize=40, ha='center', va='center')  # Add horizontal axis name

        for i, (row_images, param2_value) in enumerate(images):
            ax = fig.add_subplot(gs[i, 0])
            ax.axis('off')
            ax.text(0.5, 0.5, f"{param2_value:.4f}", fontsize=20, ha='center', va='center', rotation=90)
        fig.text(0.02, 0.5, f"{param2_name}", fontsize=40, ha='center', va='center', rotation=90)  # Add vertical axis name

        param_text = (f"D_u = {simulator_args['D_u']}, D_v = {simulator_args['D_v']}, Time Steps = {simulator_args['time_steps']}")
        fig.suptitle(param_text, fontsize=14, y=0.95, fontweight='bold')

        matrix_filename = os.path.join(output_dir, f"{param1_name}_{param2_name}_matrix.png")
        plt.savefig(matrix_filename, dpi=150)
        plt.close(fig)
        print(f"Matrix plot saved to {matrix_filename}")

    print("2D sweeping complete!")