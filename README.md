# Void Scanner

## Comprehensive Network Scanning Tool

Void Scanner is a robust and versatile network scanning tool designed to assess and analyze network security. It offers functionality for setting targets (individual IP addresses or ranges), performing ping scans, and scanning TCP ports.

### Features

- **Set Target:** Define the target IP or range for scanning.
- **Ping Target:** Check the activeness of a specific target.
- **TCP Scan:** Scan a range of TCP ports on a target to determine their state (open, closed, or filtered).
- **Save Results:** Store the results of the scans in a JSON format.
- **Retrieve Saved Results:** Access previously saved results using the target's IP address.

### Prerequisites

- Python 3.x
- Required Python packages:
  - `json`
  - `os`
  - `sys`
  - `subprocess` (for ping functionality)
  - `colorama` (for colored terminal output)

### Installation

1. Clone the repository or download the `port_scanner.py` script.
2. Ensure that Python 3.x is installed on your system.
3. Install the required Python packages:

   ```bash
   pip install colorama

### To use Void Scanner, run the script from the command line:
```bash
python port_scanner.py
