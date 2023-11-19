# CANBUS_PRIORITY_MESSAGE
Controller Area Network (CAN) is a robust and widely used. In this process I am focusing on message  prioritization which means When a CAN device transmits data onto the network, an identifier that is unique throughout the network precedes the data.
Summary:

The provided work revolves around simulating and visualizing a Controller Area Network (CAN) system, a communication protocol widely used in automotive and industrial applications. The focus is on message prioritization, where the identifier (CAN ID) not only defines the content of the data but also determines the priority. The work includes the use of virtual CAN interfaces ("vcan0" and "vcan1"), the "python-can" library, and visualization using the "matplotlib" library.

1. **Virtual CAN Interfaces ("vcan0" and "vcan1"):**
   - "vcan0" and "vcan1" are virtual CAN interfaces used for testing and development in a virtual environment.
   - The "can_simulation" function simulates CAN messages on these virtual channels.
   - "candump" is used to monitor CAN messages on "vcan0" and "vcan1," confirming successful message transmission.

2. **CAN Message Visualization:**
   - The "receive_and_plot" script visualizes CAN messages received on "vcan0" and "vcan1" in real-time using "matplotlib."
   - Each line in the plot represents the data bytes of a CAN message, updating dynamically as messages are received.

3. **Central Control Script ("central_control.py"):**
   - This script listens to a CAN bus using the "python-can" library and serves as a basic framework for handling CAN messages.
   - It continuously listens for incoming CAN messages, distinguishing between regular and emergency messages.

4. **Message Handling and Visualization Simulation:**
   - A script simulates a CAN system with three nodes: Engine Heat Monitor, Obstacle Finder, and Main Control.
   - Message priorities (low, medium, high) and IDs (emergency, regular) are defined.
   - Threads simulate message handling by different nodes, and visualization threads update plots in real-time.

5. **Race Condition Mitigation:**
   - The "check3.py" code introduces a shared variable and demonstrates a race condition.
   - A lock is implemented to synchronize access to the shared variable, mitigating the race condition.

6. **Output Visualization and Analysis:**
   - The output of the race condition simulation demonstrates the handling of messages by different nodes, shared variable updates, and the importance of proper synchronization.

The work results are interrelated in simulating various aspects of a CAN system, from virtual interfaces and message visualization to message handling by different nodes. The introduction of a shared variable and the demonstration of a race condition highlight the necessity of synchronization in multi-threaded environments. Overall, the work provides a comprehensive exploration of CAN communication, simulation, and potential challenges in concurrent execution.
