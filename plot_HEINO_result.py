#!/usr/bin/env python3

import numpy as np

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import argparse

# the following is in km
x = np.linspace(0, 4000, num=81)
y = np.linspace(0, 4000, num=81)
X, Y = np.meshgrid(x, y)

distance_from_center = np.sqrt((X - 2000) ** 2 + (Y - 2000) ** 2)
radius = 2000

ocean = distance_from_center >= radius
land = distance_from_center < radius

hudson_bay = np.logical_and.reduce(
    (2300 <= X, X <= 3300,
     1500 <= Y, Y <= 2500))

hudson_strait = np.logical_and.reduce(
    (3300 <= X, X <= 4000,
     1900 <= Y, Y <= 2100))


sediment_area = np.logical_or(hudson_bay, hudson_strait)


parser = argparse.ArgumentParser(description='Generate model setup files')
parser.add_argument('ncfile')
parser.add_argument('--full', action="store_true",
                    help="plot full time, not only last 50ka")
args = parser.parse_args()

root_grp = Dataset(args.ncfile, "r")
thk = root_grp.variables["thk"][:]
time = root_grp.variables["time"][:]
root_grp.close()

time_ka = time / 60 / 60 / 24 / 365 / 1000

mask3d = np.zeros_like(thk)
mask3d[:, :, :] = sediment_area[np.newaxis, :, :] == 0

thk_masked = np.ma.array(thk, mask=mask3d)
thk_mean = []
for i in range(thk.shape[0]):
    thk_mean.append(np.mean(thk_masked[i, :, :]))

# thk_mean = np.mean(thk_masked, axis=-1)

# plt.imshow(thk_masked[-1,:,:])

if not args.full:
    time_ka = time_ka[150:]
    thk_mean = thk_mean[150:]


plt.plot(time_ka, thk_mean)
plt.xlabel("time (ka)")
plt.ylabel("mean ice thickness over sediment area (m)")
plt.show()

plt.tight_layout()
plt.savefig(args.ncfile + ".png", dpi=300)
