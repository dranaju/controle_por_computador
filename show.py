import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
import csv 
import sys

def animate(i):
    try:
        file = open("caso.csv")
        reader = csv.reader(file)
        xs = []
        ys = []

        for row in reader:
            if len(row) > 1:
                print(row[0],row[1])
                try:
                    x, y = np.int64(row[0]), np.float128(row[1])
                    xs.append(x)
                    ys.append(y)
                except:
                    continue
        ax1.clear()
        ax1.plot(xs,ys)
    except KeyboardInterrupt:
        print("Saiu")
        sys.exit()
ani = animation.FuncAnimation(fig,animate, interval=1)
plt.show()
