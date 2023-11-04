# TVNS-R Tools

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Version
The current version is 0.1. It has been tested, but not thoroughly so.

## Introduction

This Python package provides two components:

1. **TVNS Mock Server**: A mock server that simulates an HTTP interface to control a tVNS-R device. It allows you to initiate treatment and stimulation commands with a specified failure probability. The server can be used via the command line.

2. **TVNS Manager Interface Module**: This Python module allows communication with a tVNS-R Stimulator device via HTTP commands. It includes a Logger class for recording events with timestamps to a log file.

## TVNS Mock Server

The TVNS Mock Server creates a mock server that simulates an HTTP interface for controlling a tVNS-R device. It provides the following functionality:

- Simulates failures with a specified probability for each command.
- Command-line usage.

It responds to the HTTP Post requests as the tVNS-R decive would and can be used as a replacement while developing experiments.

### Usage
After a successful install tvnsMockServer is available from the command line.
Run the script with optional command-line arguments to set the port and failure probability.

- The server listens for HTTP POST requests with specific command bodies and responds accordingly.
- Each specific command can fail with the specified failure probability.

### Command-line Arguments

- `--port`: Port for the HTTP server (default: 51523).
- `--failure-probability`: Failure probability for tVNS-R commands (0.0 to 1.0, default: 0.0).

### Example

To start the server on port 8080 with a 20% failure probability for commands:

```bash
tvnsMockServer --port 8080 --failure-probability 0.2
```

## TVNS Manager Interface Module

The TVNS Manager Interface Module allows communication with a tVNS-R Stimulator device via HTTP commands. It includes a Logger class for recording events with timestamps to a log file.

### Usage

1. Replace the `tvns_manager_url` variable with the actual URL where tVNS Manager is listening.
2. Optionally, set the `log_file_name` variable to specify the log file name.
3. Create an instance of the TVNSManager class and use its methods to interact with the tVNS device.

### Example Usage

```python
tvns_manager = TVNSManager(tvns_manager_url, log_file_name)
tvns_manager.initialize_connection()
tvns_manager.start_treatment()
tvns_manager.start_stimulation()
tvns_manager.pause_stimulation(pause_duration)
tvns_manager.stop_stimulation()
tvns_manager.stop_treatment()
```

### Classes

- **Logger**: Handles logging of events to a log file with timestamps.
- **TVNSManager**: Communicates with the tVNS-R Stimulator device via HTTP requests.

### Note

- Adjust the `pause_duration` variable as needed to control the duration of stimulation pauses.

## Testing

A sample test script is included in the module to demonstrate the TVNS Manager Interface Module's usage. The test script initiates the connection, starts treatment, starts and stops stimulation, and performs a series of stimulation pulses.

## License

This package is open-source and is provided under the MIT License. You are free to use, modify, and distribute it according to the terms of the license.

## Author

- Author: Joshua P. Woller

## Acknowledgments

The TVNS Mock Server and TVNS Manager Interface Module were developed for simulating and communicating with a tVNS-R Stimulator device. They can be adapted and extended to suit specific project requirements.

---

**Disclaimer**: This package is for research and testing purposes only. Use at your own risk, the software is provided as is. No liability is taken and warranty given. It is not intended for medical use, and any medical applications should be implemented with appropriate medical device certifications and regulatory approvals.