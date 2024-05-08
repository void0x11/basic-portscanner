'''
Void Scanner - Comprehensive Network Scanning Tool
==================================================

Description:
------------
Void Scanner is a robust and versatile network scanning tool designed to perform various
networking tasks using basic network methods. Its core functionality includes setting targets 
(individual IP addresses or ranges), ping scanning, and TCP port scanning.

The program is built to be OS-agnostic, optimizing itself for UNIX-like and Windows 
systems by adjusting terminal clearing methods and ping parameters accordingly.

Results of the scans can be saved in a structured JSON format for future reference, 
enabling a user to retrieve, analyze, or share the obtained data. The results are stored 
in the "scan_results" directory, with each file named after the scanned IP address.

Features:
---------
1. Set Target: Define the target IP or range for scanning.
2. Ping Target: Check the activeness of a specific target.
3. TCP Scan: Scan a range of TCP ports on a target to determine their state (open, closed, or filtered).
4. Save Results: Store the results of the scans in a JSON format.
5. Retrieve Saved Results: Access previously saved results using the target's IP address.

Design Choices:
---------------
1. Modularity: Functions are broken down based on their specific roles, promoting readability and reusability.
2. Global Variables: Some global variables, like "Target" and "tcp_results", are used to hold data shared among functions. 
While the use of global variables can be debated, they provide simplicity for this tool's context.
3. Error Handling: Basic error handling and input validations are provided, ensuring the program doesn't crash on invalid input.
4. Feedback System: Color-coded feedback helps users easily identify the state or results of their actions, enhancing user experience.
5. File Management: Checks are in place to ensure scan results are saved correctly, and the appropriate directories exist. 
File naming conventions are adopted to make retrieving specific scan results intuitive.
6. OS Compatibility: To ensure the tool functions across different operating systems, system checks are incorporated to 
adjust methods and commands accordingly.

Future Improvements:
--------------------
1. Enhanced Error Handling: Provide more granular error messages and handle edge cases to improve the tool's robustness.
2. Expand Scanning Capabilities: Introduce other scanning methods, such as UDP scanning, OS fingerprinting, and banner grabbing.
3. Logging System: Implement a logging system to track the tool's activities and potentially debug issues.
4. Configuration File: Introduce a configuration file where users can set default behaviors, saved results locations, and other preferences.

Dependencies:
-------------
- colorama: For color-coded terminal text.

Usage:
------
Run the script in a terminal or command prompt. Follow the on-screen options to navigate through the tool's functionalities.

Author: Ahmed Amin
Class: CSCY 1350
Github: void0x11
'''

import os
import json
import socket
from colorama import Fore
import ipaddress
import subprocess
import platform

# Using global variables is a design decision that simplifies our current approach, 
# but it can make the code harder to maintain and debug in the long run.
Target = "0"
tcp_results = {}

# Hardcoding paths might lead to potential issues in certain environments.
# Consider allowing the user to configure the path, or determine it programmatically.
RESULTS_DIR = "scan_results"

# It's good practice to check and create required directories on startup.
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

def clear_screen():
    """Clear the terminal screen based on the host OS."""
    os_name = os.name  # 'posix' for UNIX-like, 'nt' for Windows

    # It's always a good idea to accommodate the tool to different OSes.
    if os_name == 'posix':
        os.system('clear')
    elif os_name == 'nt':
        os.system('cls')
    else:
        print("\n" * 50)  # Fallback. This will print 50 new lines to simulate a clear screen.

def reset_color():
    """Reset the terminal color to LIGHTMAGENTA_EX."""
    print(Fore.CYAN, end="")

def print_terminal_header():
    '''Prints the tool's header art and name in the terminal.'''

    print(Fore.BLUE + r"""
    
888     888          d8b      888       .d8888b.                             
888     888          Y8P      888      d88P  Y88b                            
888     888                   888      Y88b.                                 
Y88b   d88P  .d88b.  888  .d88888       "Y888b.    .d8888b  8888b.  88888b.  
 Y88b d88P  d88""88b 888 d88" 888          "Y88b. d88P"        "88b 888 "88b 
  Y88o88P   888  888 888 888  888            "888 888      .d888888 888  888 
   Y888P    Y88..88P 888 Y88b 888      Y88b  d88P Y88b.    888  888 888  888 
    Y8P      "Y88P"  888  "Y88888       "Y8888P"   "Y8888P "Y888888 888  888 
                                                                             
                                                                             
                                                                             

    [!] Network Scanning Tool Using Basic Network Methods [!]
    """)
    reset_color()


def print_options():
    """Display the list of functionalities provided by the Void Scanner tool."""
    print("\nOptions:")
    print("[1] Set Target")
    print("[2] Ping Target")
    print("[3] Scan Ports")
    print("[4] Save Results")
    print("[5] Retrieve Saved Results")
    print("[6] Exit")

def check_ip_format(ip):
    """
    Validate the format of an IP address.
    
    Parameters:
    - ip (str): The IP address to be validated.

    Returns:
    - bool: True if valid IP format, False otherwise.
    """

    # Leveraging the ipaddress module is a neat way to verify IP addresses.
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def ping_scan(target):
    """
    Determine the activeness of a target using ICMP ping.

    Parameters:
    - target (str): IP address or IP range to be pinged.

    Returns:
    None
    """

    # Determine the current operating system
    param = "-n" if platform.system().lower() == "windows" else "-c"

    # Consider using a threaded approach to speed up scanning multiple IP addresses.
    def ping_single_ip(ip):
        result = subprocess.run(["ping", param, "1", ip], capture_output=True, text=True)
        return "1 packets received" in result.stdout or "Received = 1" in result.stdout

    # This assumes the range is within a single class C subnet (i.e., 192.168.1.x). 
    # Consider expanding this or clarifying in the documentation.
    # Split target if a range is provided
    if "-" in target:
        start_ip, end_ip = map(int, target.split("-"))
        for ip in range(start_ip, end_ip + 1):
            ip_str = f"192.168.1.{ip}"
            if ping_single_ip(ip_str):
                print(Fore.GREEN + f"{ip_str} is active")
            else:
                print(Fore.RED + f"{ip_str} is inactive")
    else:
        if ping_single_ip(target):
            print(Fore.GREEN + f"[+] {target} is active")
        else:
            print(Fore.RED + f"[-] {target} is inactive")
    reset_color()


def tcp_scan(target, start_port, end_port=None, speed='normal'):
    """
    Perform a TCP port scan on a target to determine open, closed, and filtered ports.
    
    Parameters:
    - target (str): IP address of the target host.
    - start_port (int): Start of the port range for scanning.
    - end_port (int, optional): End of the port range. If not provided, scans only start_port.
    - speed (str): Defines the speed of the scan (fast, normal, slow). Default is 'normal'.

    Returns:
    None
    """
    global tcp_results

    # Handling speed by just setting timeouts might be too simplistic.
    # Perhaps, for faster scans, consider more parallelism (e.g., multi-threading) rather than just reducing the timeout.
    if end_port is None:
        end_port = start_port  # if only one port is provided, start and end are the same

    if speed == 'fast':
        timeout = 0.5
    elif speed == 'slow':
        timeout = 2
    else:
        timeout = 1

    print(Fore.GREEN + f"\nStarting TCP scan on {target} with {speed} speed\n")
    open_ports = []
    closed_ports = []
    filtered_ports = []

    # Configuring timeout for socket operations
    socket.setdefaulttimeout(timeout)

    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                result = s.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                else:
                    closed_ports.append(port)
        except socket.timeout:
            filtered_ports.append(port)

    print("PORT     STATE")
    for port in open_ports:
        print(f"{port:5}/tcp  open")
    for port in filtered_ports:
        print(f"{port:5}/tcp  filtered")

    print(f"\nScan completed: {len(open_ports)} open ports, {len(closed_ports)} closed ports, {len(filtered_ports)} filtered ports.\n")
    reset_color()
    results = {
        'open_ports': open_ports,
        'filtered_ports': filtered_ports
    }


    tcp_results = results

def save_results_to_json(filename, data):
    """
    Save the scan results to a JSON file.

    Parameters:
    - filename (str): The name of the file to save the results in.
    - data (dict): The scan results data.

    Returns:
    None
    """

    # Make sure the filename has .json extension
    if not filename.endswith(".json"):
        filename += ".json"

    filepath = os.path.join(RESULTS_DIR, filename)
    # Consider sanitizing the filename to ensure no harmful strings are passed.

    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print(Fore.GREEN + f"[+] Results saved to {filepath}")
    except Exception as e:
        print(Fore.RED + f"[-] Error saving results to {filepath}. Reason: {e}")
    finally:
        reset_color()

def retrieve_and_print_results():
    """
    Fetch scan results for a specific IP address from its corresponding JSON file
    and display them in the terminal.
    """

    # Mixing input gathering and result printing in the same function is not recommended. 
    # It might be better to separate these concerns.
    ip = input("Enter the IP address of the results you'd like to retrieve: ")
    if check_ip_format(ip) is False:
        print(Fore.RED + "[-] Invalid IP Format. Try Again ...")
        reset_color()
        del ip
        retrieve_and_print_results()
    filename = f"{RESULTS_DIR}/{ip.replace('.', '_')}.json"

    # This nested approach of error-checking and input gathering could be streamlined.
    if not os.path.exists(filename):
        print(Fore.RED + f"[-] No saved results found for IP: {ip}")
        reset_color()
        return

    with open(filename, 'r') as file:
        data = json.load(file)

    print(Fore.MAGENTA + f"Results for {ip.replace('.', '_')}:\n")
    reset_color()

    print(Fore.YELLOW + "[+] Ping Scan:")
    reset_color()
    if 'ping_scan' in data:
        if data['ping_scan'] == "active":
            print(f"{ip} is active")
        else:
            print(f"{ip} is inactive")
    else:
        print("No Ping Scan Data available")

    print(Fore.YELLOW + "\n[+] TCP Scan:")
    reset_color()
    tcp_results = data.get('tcp_scan', "No TCP Scan Data")

    if tcp_results != "No TCP Scan Data":
        print("PORT     STATE")
        for port, state in tcp_results.items():
            print(f"{port:5}/tcp  {state}")
    else:
        print(tcp_results)

    reset_color()



def handle_choice(choice):
    """
    Handle user's menu choice and direct to the appropriate functionality.

    Parameters:
    - choice (str): User's selected menu option.

    Returns:
    None
    """

    global Target  # Declare Target as global to modify its value
    global tcp_results
    reset_color()

    # This function is quite large and handles multiple functionalities. 
    # It might be beneficial to break this down further for maintainability.

    # Repeated code (like setting the target) should be avoided and can be factored into its function.
    if choice == "1":
        Target = input("Enter the Target IP: ")
        if check_ip_format(Target) is True:
            reset_color()
        while not check_ip_format(Target):
            print(Fore.RED + "[-] Invalid IP Format. Try Again ...")
            reset_color()
            Target = input("Enter the Target IP: ")
        print(Fore.GREEN + "[+] Target Added ...")
        reset_color()

    # Repeated code (like setting the target) should be avoided and can be factored into its function.
    elif choice == "2":
        if Target != "0":
            ping_scan(Target)
        while Target == "0":
            print(Fore.RED + "[-] No Target Set. Please Set it First!")
            reset_color()
            Target = input("Enter the Target IP: ")
            if check_ip_format(Target) is True:
                reset_color()
            while not check_ip_format(Target):
                print(Fore.RED + "[-] Invalid IP Format. Try Again ...")
                reset_color()
                Target = input("Enter the Target IP: ")
            print(Fore.GREEN + "[+] Target Added ...")
            reset_color()

    # Repeated code (like setting the target) should be avoided and can be factored into its function.

    elif choice == "3":
        if Target != "0":
            port_input = input("Enter port or range (e.g. 22 or 20-80): ")
            if "-" in port_input:
                start_port, end_port = map(int, port_input.split("-"))
            else:
                start_port = int(port_input)
                end_port = None

            speed = input("Choose scan speed (fast, normal, slow): ").lower()
            while speed not in ['fast', 'normal', 'slow']:
                print(Fore.RED + "[-] Invalid speed choice. Try Again ...")
                speed = input("Choose scan speed (fast, normal, slow): ").lower()

            tcp_scan(Target, start_port, end_port, speed)

        while Target == "0":
            print(Fore.RED + "[-] No Target Set. Please Set it First!")
            reset_color()
            Target = input("Enter the Target IP: ")
            if check_ip_format(Target) is True:
                reset_color()
            while not check_ip_format(Target):
                print(Fore.RED + "[-] Invalid IP Format. Try Again ...")
                reset_color()
                Target = input("Enter the Target IP: ")
            print(Fore.GREEN + "[+] Target Added ...")
            reset_color()

    # Repeated code (like setting the target) should be avoided and can be factored into its function.
    elif choice == "4":
        if Target != "0":
            data = {
                "ping": {
                    "Target": Target,
                    "Status": "active" if ping_scan(Target) else "inactive"
                },
                "tcp_scan": tcp_results if tcp_results else "No TCP Scan Data"
            }
            filename = Target.replace(".", "_")
            save_results_to_json(filename, data)
            tcp_results = {}  # Clear the tcp_results after saving

        else:
            print(Fore.RED + "[-] No Target Set. Please Set it First!")
            reset_color()


    elif choice == "5":
        retrieve_and_print_results()

    elif choice == "6":
        print("Exiting...")
        exit(0)

    else:
        print("Invalid choice. Please select a valid option.")

def main():
    """
    The primary execution point of the Void Scanner tool.
    Presents the user with a menu to interact with the various functionalities.
    """

    clear_screen()
    print_terminal_header()
    while True:
        print_options()
        choice = input("\nVoid Scanner > ")
        handle_choice(choice)

if __name__ == "__main__":
    main()
