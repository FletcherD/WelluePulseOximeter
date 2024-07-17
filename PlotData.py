from collections import deque
import threading
import matplotlib
matplotlib.use('qtagg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import Wellue

mac_address = 'BA:03:8C:12:E2:AC'

plot_lines = ['oximeter', 'pulse', 'status']
x_len = 500

# Buffer to store values for each plot line
value_buffers = {k: deque(maxlen=x_len) for k in plot_lines}

fig, ax = plt.subplots()
lines = {k: ax.plot([], [], label=f'{k}')[0] for k in plot_lines}
ax.set_xlim(0, x_len)
ax.set_ylim(0, 100)  # Adjust this range based on your data
ax.set_title('Live BLE Data Plot')
ax.set_xlabel('Sample')
ax.set_ylabel('Value')
ax.grid(True)


def update_plot(frame):
    while len(Wellue.reading_queue) != 0:
        reading = Wellue.reading_queue.pop()
        for i, (key, value) in enumerate(reading.items()):
            if key in value_buffers:
                value_buffers[key].append(value)

    for i, (key, buffer) in enumerate(value_buffers.items()):
        lines[key].set_data(range(len(buffer)), buffer)

    ax.relim()
    ax.autoscale_view()
    return lines.values()


def main():
    # Start the data reading thread
    ble_thread = threading.Thread(target=Wellue.connect, args=(mac_address,), daemon=True)
    ble_thread.start()

    # Set up the animation
    ani = FuncAnimation(fig, update_plot, interval=100, blit=True)
    plt.show()


if __name__ == "__main__":
    main()

