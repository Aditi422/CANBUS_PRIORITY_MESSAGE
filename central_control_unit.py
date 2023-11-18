import can

def central_control_unit(channel):
    bus = can.interface.Bus(channel=channel, bustype='socketcan')

    while True:
        message = bus.recv()  # Receive a message from the bus
        
        # Check the message ID to determine its priority
        if message.arbitration_id == 0x100:  # Emergency ID
            handle_emergency_message(message)
        else:
            handle_regular_message(message)

def handle_emergency_message(message):
    print("!!! EMERGENCY Message received !!!")
    # Here, you can add further specific logic to handle the emergency message
    # For example, sending signals to other nodes, triggering alarms, etc.
    
def handle_regular_message(message):
    print(f"Regular message received: {message.data}")

if __name__ == '__main__':
    central_control_unit('vcan0')  # Adjust the channel as needed

