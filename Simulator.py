import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import lineStyles
from matplotlib.pyplot import quiver
from matplotlib.animation import FuncAnimation
from collections import deque


def getAcceleration ( position, mass, G, soft):

    N = position.shape[0]

    d = position[None, :, :] - position [:, None, :]

    r2 = (d ** 2).sum(axis = -1) + soft ** 2

    inverseR3 = r2 ** (-1.5)
    np.fill_diagonal(inverseR3, 0.0)

    acceleration = (G * (d * inverseR3[:, :, None]) * mass [None, :, None] ).sum(axis = 1)

    return acceleration

N = 100
np.random.seed(0)
pos = np.random.uniform(-1, 1, (N, 3))
velocity = np.random.uniform(-0.5, 0.5, (N, 3))
mass = np.random.uniform(0.5, 2.0, N)
G, soft, dt = 1.0, 0.05, 0.01

#Trail
trail = 80
hist_x = [deque(maxlen=trail) for _ in range(N)]
hist_y = [deque(maxlen=trail) for _ in range(N)]

for i in range (N):
    hist_x[i].append(pos[i, 0])
    hist_y[i].append(pos[i, 1])




fig, ax = plt.subplots(figsize= (6, 6))
ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect('equal')
ax.grid(True)
pts = ax.scatter(pos[:, 0], pos[:, 1], s=12)

trail_lines = []
for _ in range (N):
    (ln,) = ax.plot([], [], linestyle = ':', linewidth = 1, alpha = 0.35)
    trail_lines.append(ln)

velocity += 0.5 * getAcceleration(pos, mass, G, soft) * dt

def updateOverTime (frame):
    global pos, velocity
    pos += velocity * dt

    acceleration = getAcceleration(pos, mass, G, soft)
    velocity += acceleration * dt

    for i in range (N):
        hist_x[i].append(pos[i, 0])
        hist_y[i].append(pos[i, 1])
        trail_lines[i].set_data(hist_x[i], hist_y[i])


    pts.set_offsets(pos[:, :2])
    return (*trail_lines, pts)

animation = FuncAnimation(fig, updateOverTime, frames = 600, interval=20, blit=True)
plt.show()


