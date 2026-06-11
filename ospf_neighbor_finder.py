from netmiko import ConnectHandler


def get_ospf_neighbors(host, username, password):
    """
    Discovers OSPF neighbors in FULL state on Cisco IOS devices.

    Args:
        host: IP address of the device
        username: SSH username
        password: SSH password
    """
    device = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
    }

    try:
        connection = ConnectHandler(**device)

        neighbors = connection.send_command(
            'show ip ospf neighbor',
            use_textfsm=True
        )

        print(f"\nDevice: {host}")
        print(f"{'='*50}")
        print("OSPF Neighbors in FULL state:")
        print(f"{'-'*50}")

        full_neighbors = [n for n in neighbors if 'FULL' in n['state']]

        if not full_neighbors:
            print("No FULL state neighbors found.")
        else:
            for neighbor in full_neighbors:
                print(
                    f"Neighbor ID : {neighbor.get('neighbor_id', '')}\n"
                    f"Address     : {neighbor.get('ip_address', '')}\n"
                    f"State       : {neighbor.get('state', '')}\n"
                    f"Interface   : {neighbor.get('interface', '')}\n"
                    f"{'-'*50}"
                )

        connection.disconnect()

    except Exception as e:
        print(f"Connection failed to {host}: {str(e)}")


if __name__ == '__main__':
    # Example usage - replace with your device details
    devices = [
        "192.168.1.1",
        "192.168.1.2",
    ]

    USERNAME = "admin"
    PASSWORD = "cisco123"

    for device in devices:
        get_ospf_neighbors(device, USERNAME, PASSWORD)
