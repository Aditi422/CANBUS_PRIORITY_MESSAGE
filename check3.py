import can
import threading
import queue
import time

# Define message priorities
LOW_PRIORITY = 2
MEDIUM_PRIORITY = 1
HIGH_PRIORITY = 0

# Define message IDs
EMERGENCY_ID = 0x100
REGULAR_ID = 0x200

# Define a message queue for message storage
message_queue = queue.PriorityQueue()

# Dictionary to store statistics for each message ID
message_stats = {}

# Shared variable introduced to create a potential race condition
shared_variable = 0

# Lock for synchronization
lock = threading.Lock()

# Function to send a message to the queue
def send_message(message, priority):
    with lock:
        message_queue.put((priority, message))

# Function to simulate message handling
def message_handler(node_name):
    global shared_variable  # Using the shared variable without proper synchronization
    while True:
        try:
            priority, message = message_queue.get(timeout=1)
            if node_name == "Main Control" and "Emergency" in message[1]:
                handle_emergency_message()
            
            # Simulate a race condition by accessing and modifying a shared variable
            with lock:
                shared_variable += 1
                print(f"{node_name}: Shared Variable: {shared_variable}")
            
            msg_id = int.from_bytes(message[0].arbitration_id.to_bytes(4, 'big'), byteorder='big')
            if msg_id not in message_stats:
                message_stats[msg_id] = {'count': 0, 'timestamps': []}
            message_stats[msg_id]['timestamps'].append(time.time())
            message_stats[msg_id]['count'] += 1

            print(f"{node_name}: Handling message: Timestamp: {message_stats[msg_id]['timestamps'][-1]:.6f} - {message[1]}")
            print_statistics()
            message_queue.task_done()
        except queue.Empty:
            pass

# Function to handle emergency messages
def handle_emergency_message():
    with lock:
        # Simulate a race condition by accessing and modifying a shared variable
        shared_variable += 1
        print(f"Emergency Handler: Shared Variable: {shared_variable}")

# Function to print statistics for each message ID
def print_statistics():
    with lock:
        for msg_id, stats in message_stats.items():
            intervals = [t - s for s, t in zip(stats['timestamps'], stats['timestamps'][1:])]
            average_interval = sum(intervals) / len(intervals) if intervals else 0
            print(f"ID: 0x{msg_id:X} - Message count: {stats['count']} - Average interval: {average_interval:.4f} seconds")

# ... (rest of the code remains the same)

# Create threads for message handling
handler_thread_main_control = threading.Thread(target=message_handler, args=("Main Control",))
handler_thread_main_control.daemon = True
handler_thread_main_control.start()

handler_thread_node_1 = threading.Thread(target=message_handler, args=("Node 1",))
handler_thread_node_1.daemon = True
handler_thread_node_1.start()

handler_thread_node_2 = threading.Thread(target=message_handler, args=("Node 2",))
handler_thread_node_2.daemon = True
handler_thread_node_2.start()

# Function to simulate sending messages with different priorities
def simulate_message_generation():
    for i in range(1, 51):
        print(f"Generating message {i}")
        if i % 3 == 0:
            send_message((can.Message(arbitration_id=EMERGENCY_ID, data=[i]), f"Emergency message {i}"), HIGH_PRIORITY)
        elif i % 2 == 0:
            send_message((can.Message(arbitration_id=REGULAR_ID, data=[i]), f"Medium priority message {i}"), MEDIUM_PRIORITY)
        else:
            send_message((can.Message(arbitration_id=REGULAR_ID, data=[i]), f"Low priority message {i}"), LOW_PRIORITY)
        time.sleep(1)

# Create a thread for simulating message generation
generation_thread = threading.Thread(target=simulate_message_generation)
generation_thread.start()

# Wait for the threads to finish
generation_thread.join()
handler_thread_main_control.join()
handler_thread_node_1.join()
handler_thread_node_2.join()

# Calculate and print statistics for each message ID
for msg_id, stats in message_stats.items():
    intervals = [t - s for s, t in zip(stats['timestamps'], stats['timestamps'][1:])]
    average_interval = sum(intervals) / len(intervals) if intervals else 0
    print(f"ID: 0x{msg_id:X} - Message count: {stats['count']} - Average interval: {average_interval:.4f} seconds")

