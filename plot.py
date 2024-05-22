from matplotlib import pyplot as plt
import numpy as np

#data = np.genfromtxt('data.csv', delimiter=',', skip_header=1)
#plt.plot(data[:, 0], data[:, 1])
data = np.genfromtxt('data_1K.csv', delimiter=',', skip_header=1)
plt.plot(data[:, 0],(data[:, 0]-data[:, 1])/data[:,0])
data = np.genfromtxt('data_4.csv', delimiter=',', skip_header=1)
plt.plot(data[:, 0], (data[:, 0]-data[:, 1])/data[:,0])
plt.show()