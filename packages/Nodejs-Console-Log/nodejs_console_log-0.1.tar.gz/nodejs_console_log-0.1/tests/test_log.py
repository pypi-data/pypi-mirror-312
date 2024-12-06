import unittest
from nodejs_console_log import console.log

class TestNodejsConsoleLog(unittest.TestCase):
    
    def test_console.log(self):
        # You can test the output of the log function here
        with self.assertLogs('nodejs_console_log.log', level='INFO') as log_output:
            console.log('Test message')
            self.assertIn('Test message', console.log_output.output)
