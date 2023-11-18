import can
import time
from multiprocessing import Process

def can_simulation(channel, node_id):
    bus = can.interface.Bus(channel=channel, bustype='socketcan')
    while True:
        message = can.Message(
            arbitration_id=0x100 + node_id,
            data=[node_id, 1, 2, 3, 4, 5, 6, 7],
            is_extended_id=False
        )
        bus.send(message)
        time.sleep(1)
        
#the following function has values proportional to the c++ implementation
def can_simulation2(channel, node_id):
    bus = can.interface.Bus(channel=channel, bustype='socketcan')
    
    # Convert "HelloCAN" to its ASCII values
    message_data = [ord(char) for char in "HelloCAN"]
    
    while True:
        message = can.Message(
            arbitration_id=0x100 + node_id,
            data=message_data,
            is_extended_id=False
        )
        bus.send(message)
        time.sleep(1)


if __name__ == '__main__':
    p1 = Process(target=can_simulation2, args=('vcan0', 1))
    p2 = Process(target=can_simulation2, args=('vcan1', 2))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
