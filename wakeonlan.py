import socket
import struct

def wake_on_lan(mac_address, broadcast_ip="255.255.255.255", port=9):
    # Clean MAC address (accepts AA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF)
    mac_address = mac_address.replace(":", "").replace("-", "")
    
    if len(mac_address) != 12:
        raise ValueError("Invalid MAC address format")

    # Magic packet
    mac_bytes = bytes.fromhex(mac_address)
    magic_packet = b'\xff' * 6 + mac_bytes * 16

    # Send packet
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(magic_packet, (broadcast_ip, port))
    sock.close()

    print("Magic packet sent!")

# Example usage
wake_on_lan("9c:6b:00:18:E4:11")
wake_on_lan("9c:6b:00:18:E4:51")
