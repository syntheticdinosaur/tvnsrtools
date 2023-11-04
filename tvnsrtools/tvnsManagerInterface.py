"""
tVNS Manager Communication Module
author:Joshua Woller

This Python module allows communication with a tVNS-R Stimulator device via HTTP commands.
It includes a Logger class for recording events with timestamps to a log file.

Usage:
1. Replace the 'tvns_manager_url' variable with the actual URL where tVNS Manager is listening.
2. Optionally, set the 'participant_name' and 'log_file_name' variables to specify participant details and the log file name.
3. Create an instance of the TVNSManager class and use its methods to interact with the tVNS device.

Example Usage:
    tvns_manager = TVNSManager(tvns_manager_url, log_file_name)
    tvns_manager.initialize_connection()
    tvns_manager.start_treatment()
    tvns_manager.start_stimulation()
    tvns_manager.pause_stimulation(pause_duration)
    tvns_manager.stop_stimulation()
    tvns_manager.stop_treatment()

Classes:
- Logger: Handles logging of events to a log file with timestamps.
- TVNSManager: Communicates with the tVNS-R Stimulator device via HTTP requests.

Note: Adjust the 'pause_duration' variable as needed to control the duration of stimulation pauses.

"""

import requests
import time
from datetime import datetime
import os


class Logger:
    """
    Logger class for recording events with timestamps to a log file.

    Args:
        log_file (str): The path to the log file. If the file exists, a timestamp
                       will be appended to the file name to create a new log file.

    Methods:
        log(message, participant_name=None):
            Logs a message with an optional participant name and timestamp to the log file.
    """
    def __init__(self, log_file):
        # Check if the log file already exists
        if os.path.exists(log_file):
            # Append a timestamp to create a new log file
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            log_file = f"{log_file}_{current_time}.txt"

        self.log_file = log_file

    def log(self, message, participant_name=None):
        """
        Logs a message with an optional participant name and timestamp to the log file.

        Args:
            message (str): The log message to be recorded.
            participant_name (str, optional): The name of the participant, if applicable.
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_entry = f"{current_time}"
        if participant_name:
            log_entry += f" - Participant: {participant_name}"
        log_entry += f" - {message}\n"

        with open(self.log_file, "a") as file:
            file.write(log_entry)

class TVNSManager:
    """
    TVNSManager class for communicating with a tVNS device via HTTP requests.

    Args:
        base_url (str): The base URL of the tVNS Manager.
        log_file (str, optional): The path to the log file for recording events.

    Methods:
        initialise_connection():
            Initializes the connection with the tVNS device.

        start_treatment():
            Starts the tVNS treatment.

        stop_treatment():
            Stops the tVNS treatment.

        start_stimulation():
            Starts the tVNS stimulation.

        stop_stimulation():
            Stops the tVNS stimulation.

        pause_stimulation(pause_duration):
            Pauses the tVNS stimulation for a specified duration.

        _send_request(endpoint, body=None):
            Sends an HTTP POST request to the tVNS Manager endpoint.
    """
    def __init__(self, base_url:str = "http://localhost:51523/tvnsmanager/", log_file:str = None):
        self.base_url = base_url
        self.logger = Logger(log_file) if log_file else None
        self.stimactive = False

    def _send_request(self, endpoint, body=None):
        """
        Sends an HTTP POST request to the tVNS Manager endpoint.

        Args:
            endpoint (str): The endpoint to which the request is sent.
            body (str, optional): The request body.

        Returns:
            str: The response text from the HTTP request.
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {"Content-Type": "text/plain"}
        response = requests.post(url, data=body, headers=headers)

        if response.status_code == 200:
            return response.text
        else:
            return f"HTTP request failed with status code: {response.status_code}"
    
    def _validate_response(func):
        """Checks whether the response indicates a successful execution of the command."""
        def validate(self, *args, **kwargs):
            response =  func(self, *args, **kwargs)
            validation = 'success' in response 
            if self.logger and not validation:
                self.logger.log(f"Command failed: {response}")
            return validation, response 
        return validate 

    @_validate_response
    def initialise_connection(self):
        """Initializes the connection with the tVNS device."""
        result = self._send_request("initialise", "initialise")
        if self.logger:
            self.logger.log("Initialized connection")
        self._validate_response
        return result
    
    @_validate_response
    def start_treatment(self):
        """Starts the tVNS treatment."""
        result = self._send_request("startTreatment", "startTreatment")
        if self.logger:
            self.logger.log("Started treatment")
        self.stimactive = True
        return result
    
    @_validate_response
    def stop_treatment(self):
        """Stops the tVNS treatment."""
        result = self._send_request("stopTreatment", "stopTreatment")
        if self.logger:
            self.logger.log("Stopped treatment")
        self.stimactive = False
        return result

    @_validate_response
    def start_stimulation(self):
        """Starts the tVNS stimulation."""
        result = self._send_request("startStimulation", "startStimulation")
        if self.logger:
            self.logger.log("Started stimulation")
        self.stimactive = True

        return result

    @_validate_response
    def stop_stimulation(self):
        """Stops the tVNS stimulation."""
        result = self._send_request("stopStimulation", "stopStimulation")
        if self.logger:
            self.logger.log("Stopped stimulation")
        self.stimactive = False

        return result

    @_validate_response    
    def pause_stimulation(self, pause_duration):
        """
        Maintains current stimulation state for a specified duration.

        Args:
            pause_duration (float): The duration (in seconds) to pause the stimulation.

        Returns:
            str: A message indicating the pause duration.
        """
        result = f"Paused stimulation for {pause_duration} seconds / {pause_duration*1000} milliseconds."
        if self.logger:
            self.logger.log(result)
        time.sleep(pause_duration)
        return result
    
    def pulse(self, duration):
        """
        Send a stimulation pulse for a specified duration.
        Due to timing uncertainties and bluetooth delay, it is not highly precise.
        """
        MIN_DURATION = 0
        if duration < MIN_DURATION:
            return False, f"Requested Pulse too short. Min duration {MIN_DURATION}s"
        if not self.stimactive:
            start,_ = self.start_stimulation()
            time.sleep(duration)
            stop, _ = self.stop_stimulation()
            success = start and stop
        elif self.stimactive:
            stop, _  = self.stop_stimulation()
            start, _ = self.start_stimulation()
            time.sleep(duration)
            stop2, _ = self.stop_stimulation()
            
            success = stop and start and stop2
        if self.logger:
            self.logger.log("Started stimulation (pulsed)")
        if success:
            return success, f"success pulsedStimulation ({duration}s)::{datetime.now().strftime('%H:%M:%S.%f')[:-3]} (custom return)"
        else:
            return success, f"failed pulsedStimulation ({duration}s)::{datetime.now().strftime('%H:%M:%S.%f')[:-3]} (custom return)"
        
def test():
    # Replace with the participant's name (if applicable) and log file name
    log_file_name    = "tvnslog_test"
    url = "http://localhost:51523/tvnsmanager/"
    # Create an instance of the TVNSManager with optional logging
    tvns_manager = TVNSManager(url ,log_file_name)

    # Define the stimulation pause time (in seconds)
    pause_duration = 1  # Adjust this value as needed
    n_pulses = 5
    interpulse_interval = 0.1
    
    # Example stimulation protocol:
    # Depending on the connection quality via Bluetooth,
    # it might be necessary to ad additional short pauses between commands
    print('\n')
    print('-'*40)
    print('Test of tvns-R remote triggering')
    print(f'URL: {url}')
    print(f'log: {log_file_name}')
    print('-'*40)
    print('\n')
    
    print(tvns_manager.initialise_connection())
    print(tvns_manager.start_treatment())
    print(tvns_manager.stop_stimulation())
    time.sleep(1)
    print(tvns_manager.start_stimulation())
    time.sleep(2)
    print(tvns_manager.stop_stimulation())
    time.sleep(1)
    for _ in range(n_pulses):
        print(tvns_manager.pulse(0.1))
        time.sleep(interpulse_interval)
    tvns_manager.stop_stimulation()
    time.sleep(2)
    print(tvns_manager.stop_treatment())
    
if __name__ == "__main__":
    test()