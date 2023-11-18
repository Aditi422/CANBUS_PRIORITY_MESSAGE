import can
import matplotlib.pyplot as plt
import numpy as np
from threading import Thread

def receive_and_plot(channel, ax, lines, color):
    bus = can.interface.Bus(channel=channel, bustype='socketcan')
    
    timestamps = []
    data_values = [[] for _ in range(8)]  # Create a list for each data byte
    
    while True:
        message = bus.recv()  # Receive a message from the bus
        
        timestamp = message.timestamp
        
        print(f"Received message: {message}")
        print(f"Data values: {message.data}")
        print(f"Timestamp: {timestamp}")
        
        for i in range(8):  # Loop through all data bytes
            data_values[i].append(message.data[i])
        
        timestamps.append(timestamp)
        
        # Update the plot with new data for each byte
        for i in range(8):
            lines[i].set_data(np.array(timestamps), np.array(data_values[i]))
            
        plt.pause(0.01)  # Adjust the pause time as needed
        
        # Adjust axes dynamically
        ax.set_xlim(min(timestamps), max(timestamps) + 1)
        ax.set_ylim(0, 255)

if __name__ == '__main__':
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    
    lines_vcan0 = [ax1.plot([], [], color=color, lw=2)[0] for color in ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'orange']]
    lines_vcan1 = [ax2.plot([], [], color=color, lw=2)[0] for color in ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'orange']]
    
    ax1.set_title('vcan0 CAN Message Visualization')
    ax1.set_ylabel('Data')
    
    ax2.set_title('vcan1 CAN Message Visualization')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Data')
    
    thread_vcan0 = Thread(target=receive_and_plot, args=('vcan0', ax1, lines_vcan0, 'b'))
    thread_vcan1 = Thread(target=receive_and_plot, args=('vcan1', ax2, lines_vcan1, 'r'))

    thread_vcan0.start()
    thread_vcan1.start()

    plt.show()  # This will block until you close the matplotlib window

    thread_vcan0.join()
    thread_vcan1.join()

