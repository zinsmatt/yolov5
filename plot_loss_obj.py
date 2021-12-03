import numpy as np
import matplotlib.pyplot as plt


a = np.loadtxt("/home/mzins/dev/yolov5/runs/debug_sampling_mse_anlge.txt")
b = np.loadtxt("/home/mzins/dev/yolov5/runs/debug_sampling_angle.txt")

plt.plot(a, label="sampling L1 angle")
plt.plot(b, label="sampling with angle")
plt.legend()
plt.show()