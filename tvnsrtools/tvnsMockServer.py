"""
TVNS Mock Server
author: Joshua Woller

This script creates a mock server that simulates an HTTP interface to control a tVNS-R device.
It allows the initiation of treatment and stimulation commands with a specified failure
probability.
Can be used via command line.

Usage:
- Run the script with optional command-line arguments to set the port and
  failure probability.
- The server listens for HTTP POST requests with specific command bodies and
  responds accordingly.
- Each specific command can fail with the specified failure probability.

Valid POST Requests:
- 'initialise': Initializes the tVNS device.
- 'startTreatment': Starts the treatment.
- 'stopTreatment': Stops the treatment.
- 'startStimulation': Starts the stimulation.
- 'stopStimulation': Stops the stimulation.

Command-line Arguments:
    --port:             Port for the HTTP server (default: 51523).
    --failure-probability: Failure probability for commands (0.0 to 1.0,
                         default: 0.0).

Example:
    To start the server on port 8080 with a 20% failure probability for
    commands:
    > python tVNS_mock_server.py --port 8080 --failure-probability 0.2
"""

import http.server
import socketserver
from http import HTTPStatus
import random
from datetime import datetime
import argparse


TIMEFORMAT = '%H:%M:%S.%f'
class TVNSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.failure_probability = kwargs.pop('failure_probability', 0.0)
        super().__init__(*args, **kwargs)
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        def send_formatted_response(response_message, success=True):
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            timestamp = datetime.now().strftime(TIMEFORMAT)[:-3]
            outcome = 'success' if success else 'failed'
            self.wfile.write(f'{outcome}: {response_message}::{timestamp} (mocked output) \n'.encode('utf-8'))

        if post_data == 'initialise':
            send_formatted_response('The tVNS-R device has been initialized')
        elif post_data == 'startTreatment':
            if random.random() < self.failure_probability:
                send_formatted_response('Treatment not started', success=False)
            else:
                send_formatted_response('Treatment started')
        elif post_data == 'stopTreatment':
            if random.random() < self.failure_probability:
                send_formatted_response('Treatment not stopped', success=False)
            else:
                send_formatted_response('Treatment stopped')
        elif post_data == 'startStimulation':
            if random.random() < self.failure_probability:
                send_formatted_response('Stimulation not started', success=False)
            else:
                send_formatted_response('Stimulation started')
        elif post_data == 'stopStimulation':
            if random.random() < self.failure_probability:
                send_formatted_response('Stimulation not stopped', success=False)
            else:
                send_formatted_response('Stimulation stopped')
        else:
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            timestamp = datetime.now().strftime(TIMEFORMAT)[:-3]
            self.wfile.write(f'illegal command: The command was not recognized::{timestamp}\n'.encode('utf-8'))

def main():
    parser = argparse.ArgumentParser(description="Simulate a tVNS-R HTTP server with specified failure probability.")
    parser.add_argument("-p", "--port", type=int, default=51523, help="Port for the HTTP server")
    parser.add_argument("-f", "--failure-probability", type=float, default=0.0, help="Failure probability for tVNS-R commands (0.0 to 1.0)")
    args = parser.parse_args()
    port = args.port
    fail = args.failure_probability

    with socketserver.TCPServer(('', port),
                               lambda *args, **kwargs: TVNSRequestHandler(*args, **kwargs, failure_probability = fail)
                              ) as httpd:
        print('Initializing tVNS-R Mock Server...')
        print(f'Serving on port {port} with {fail * 100}% failure probability...')
        httpd.serve_forever()

if __name__ == '__main__':
    main()


