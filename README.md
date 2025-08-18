
# N-Body Gravity Simulator

This project is a compact, NumPy-powered N-body gravitational simulation with softening and a live Matplotlib animation. Bodies attract each other via the inverse-square law; the animation can render moving points (and optionally velocity vectors) with optional trailing paths.

## Table of Contents

- [Overview](#overview)
- [Demo](#demo)
- [Requirements](#requirements)
- [Installation](#installation)
- [Run](#run)
- [Simulation Parameters](#simulation-parameters)
- [How it works](#how-it-works)
- [Customize](#customize)
- [License](#license)

## Features

- **Newtonian gravity** + softening to prevent singularities at very small separations.
- **Vectorized acceleration computation** for all bodies (fast NumPy math).
- Live animation using **matplotlib.animation.FuncAnimation.**
- Optional trails using collections.deque to visualize recent paths.
- **Toggleable scatter** (points) and quiver (velocity arrows) styles.

## Prerequisites

- **Python 3.8**
- **NumPy**: For numerical computations.
- **Matplotlib**: For visualization.

Install the required Python packages using pip:

```bash
pip install numpy matplotlib
```

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/delwow/N-body-simulation.git
   cd N-body-simulation
   ```


Run the simulation script:

```bash
python simulation.py
```

*Replace `simulation.py` with the actual filename if different.*

The simulation will start, and a visualization window will display the flow field evolution. The simulation may take some time depending on the number of time steps and grid resolution.

## Simulation Parameters
Common parameters you’ll see in the script (names may vary slightly):

N — number of bodies.
pos — initial positions (typically shape (N, 3) with z ignored for 2D plotting).
velocity — initial velocities.
mass — per-body masses.
G — gravitational constant (simulation units).
soft — softening length to avoid infinite forces at zero distance.
dt — time step for integration.
plot_every / animation interval — frame update rate and pacing.
Trails — history length controlled via a deque per body.
Tip: Increase soft or reduce dt if the system “blows up”; reduce N to keep frame rates high.

## How it works

Acceleration: getAcceleration(position, mass, G, soft) computes all-pairs displacements in a single vectorized pass, builds 
𝑟
2
r
2
 with softening, and returns accelerations via the inverse-square law.

Integration: Positions and velocities are stepped forward each frame (simple explicit integration).

Rendering:

Scatter shows body positions.

Trails: Each body appends its latest (x, y) into a fixed-length deque; corresponding Line2D objects are updated.

Quiver (optional): Draws arrows to indicate velocity direction/magnitude.

Animation: FuncAnimation(fig, updateOverTime, ...) repeatedly calls an update function that advances the physics and redraws artists (scatter, trails, quiver).

<img width="635" alt="Screenshot 2024-11-14 at 7 46 03 PM" src="https://github.com/user-attachments/assets/24b26fda-370d-444f-985a-ead7e55c30eb">

*An example snapshot of the flow field during the simulation.*

## Code Explanation

### Functions

- **`distance(x1, y1, x2, y2)`**: Calculates the Euclidean distance between two points.
- **`main()`**: The main function where the simulation is set up and executed.

### Key Variables

- **`F`**: Distribution function representing particle probabilities in each lattice direction.
- **`rho`**: Fluid density at each lattice point.
- **`ux`, `uy`**: Fluid velocity components in x and y directions.
- **`Feq`**: Equilibrium distribution function used in the collision step.

### Lattice Velocities and Weights

Defined for the D2Q9 model (2 dimensions, 9 velocities):

```python
cxs = np.array([0, 0, 1, 1, 1, 0, -1, -1, -1])
cys = np.array([0, 1, 1, 0, -1, -1, -1, 0, 1])
weights = np.array([4/9, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36])
```

### Simulation Steps

1. **Initialization**: Set up the initial conditions for `F`, `rho`, and the cylinder obstacle.
2. **Main Loop**: Iterate over time steps:
   - **Streaming (Drift)**: Shift the distribution functions according to their velocities.
   - **Boundary Conditions**: Apply reflective boundary conditions at the cylinder surface.
   - **Collision**: Relax the distribution functions towards equilibrium (`Feq`).
   - **Macroscopic Variables**: Compute density and velocity fields.
   - **Visualization**: Plot the curl of the velocity field at specified intervals.


## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

