import can
import threading
import time
import queue
import matplotlib.pyplot as plt
from threading import Thread
from matplotlib.animation import FuncAnimation

# Define message priorities
LOW_PRIORITY = 2
MEDIUM_PRIORITY = 1
HIGH_PRIORITY = 0

# Define message IDs
EMERGENCY_ID = 0x100
REGULAR_ID = 0x200

# Define a message queue for message storage
message_queue = queue.PriorityQueue()

# Function to send a message to the queue
def send_message(message, priority):
    message_queue.put((priority, message))

# Function to simulate message handling
def message_handler(node_name):
    while True:
        try:
            priority, message = message_queue.get(timeout=1)  # Timeout to allow for message handling
            if priority == HIGH_PRIORITY and node_name == "Main Control":
                print(f"{node_name}: Handling EMERGENCY message: {message}")
                handle_emergency_message()
            elif node_name != "Main Control":
                print(f"{node_name}: Handling message: {message}")
            message_queue.task_done()
        except queue.Empty:
            pass

# Function to handle emergency messages
def handle_emergency_message():
    print("Main Control: Emergency message received and handled.")

# Create threads for message handling
handler_thread_main_control = threading.Thread(target=message_handler, args=("Main Control",))
handler_thread_main_control.daemon = True  # Allow the program to exit when all threads are done
handler_thread_main_control.start()

handler_thread_node_1 = threading.Thread(target=message_handler, args=("Node 1",))
handler_thread_node_1.daemon = True
handler_thread_node_1.start()

handler_thread_node_2 = threading.Thread(target=message_handler, args=("Node 2",))
handler_thread_node_2.daemon = True
handler_thread_node_2.start()

# Function to simulate sending messages with different priorities
def simulate_message_generation():
    for i in range(1, 11):
        if i % 3 == 0:
            send_message(f"Emergency message {i}", HIGH_PRIORITY)
        elif i % 2 == 0:
            send_message(f"Medium priority message {i}", MEDIUM_PRIORITY)
        else:
            send_message(f"Low priority message {i}", LOW_PRIORITY)
        time.sleep(1)  # Simulate message generation delay

# Create a figure for visualization
fig, (ax_node_1, ax_node_2, ax_main_control) = plt.subplots(3, 1, sharex=True)
timestamps_node_1, data_values_node_1 = [], []
timestamps_node_2, data_values_node_2 = [], []
timestamps_main_control, data_values_main_control = [], []

# Function to update the plot with new data for Node 1
def update_node_1(frame):
    ax_node_1.clear()
    priority_mapping = {HIGH_PRIORITY: 0, MEDIUM_PRIORITY: 1, LOW_PRIORITY: 2}
    ax_node_1.plot(timestamps_node_1, [priority_mapping[p] for p in data_values_node_1], label='Node 1 Messages')
    ax_node_1.legend()
    ax_node_1.set_title('Node 1 CAN Message Visualization')
    ax_node_1.set_ylabel('Message Priority')

# Function to update the plot with new data for Node 2
def update_node_2(frame):
    ax_node_2.clear()
    priority_mapping = {HIGH_PRIORITY: 0, MEDIUM_PRIORITY: 1, LOW_PRIORITY: 2}
    ax_node_2.plot(timestamps_node_2, [priority_mapping[p] for p in data_values_node_2], label='Node 2 Messages')
    ax_node_2.legend()
    ax_node_2.set_title('Node 2 CAN Message Visualization')
    ax_node_2.set_ylabel('Message Priority')

# Function to update the plot with new data for Main Control
def update_main_control(frame):
    ax_main_control.clear()
    priority_mapping = {HIGH_PRIORITY: 0, MEDIUM_PRIORITY: 1, LOW_PRIORITY: 2}
    ax_main_control.plot(timestamps_main_control, [priority_mapping[p] for p in data_values_main_control], label='Main Control Messages')
    ax_main_control.legend()
    ax_main_control.set_title('Main Control CAN Message Visualization')
    ax_main_control.set_xlabel('Time')
    ax_main_control.set_ylabel('Message Priority')

# Create a thread for simulating message generation
generation_thread = Thread(target=simulate_message_generation)
generation_thread.start()

# Function to receive and store messages for visualization
def receive_and_visualize():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
    
    while True:
        message = bus.recv()  # Receive a message from the bus
        timestamp = time.time()
        
        if message.arbitration_id == EMERGENCY_ID:
            timestamps_main_control.append(timestamp)
            data_values_main_control.append(message.arbitration_id)
        elif message.arbitration_id == REGULAR_ID and "Node 1" in message.data.decode():
            timestamps_node_1.append(timestamp)
            data_values_node_1.append(message.arbitration_id)
        elif message.arbitration_id == REGULAR_ID and "Node 2" in message.data.decode():
            timestamps_node_2.append(timestamp)
            data_values_node_2.append(message.arbitration_id)

# Create a thread for receiving and visualizing messages
visualization_thread = Thread(target=receive_and_visualize)
visualization_thread.start()

# Create animations to update the plots
ani_node_1 = FuncAnimation(fig, update_node_1, blit=False, interval=1000, save_count=10)
ani_node_2 = FuncAnimation(fig, update_node_2, blit=False, interval=1000, save_count=10)
ani_main_control = FuncAnimation(fig, update_main_control, blit=False, interval=1000, save_count=10)

# Show the visualization plots
plt.show()

# Wait for the threads to finish
generation_thread.join()
visualization_thread.join()
handler_thread_main_control.join()
handler_thread_node_1.join()
handler_thread_node_2.join()

