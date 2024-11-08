# tests/test_call_rclone.py
import unittest
from unittest.mock import patch, MagicMock
from call_rclone import call_rclone
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
RCLONE_PATH = os.getenv('RCLONE_PATH')

class TestCallRclone(unittest.TestCase):

    @patch('subprocess.run')
    def test_call_rclone_success(self, mock_run):
        # Arrange
        mock_run.return_value = MagicMock(stdout='file1.txt\nfile2.txt\n', returncode=0)
        
        # Act
        with patch('builtins.print') as mock_print:  # Correct context for the print mock
            call_rclone('ls', RCLONE_PATH)
        
        # Assert
        mock_run.assert_called_once_with(['rclone', 'ls', RCLONE_PATH], check=True, text=True, capture_output=True)
        mock_print.assert_called_once_with("Output:\n", 'file1.txt\nfile2.txt\n')

    @patch('subprocess.run')
    def test_call_rclone_error(self, mock_run):
        # Arrange
        mock_run.side_effect = subprocess.CalledProcessError(1, 'rclone', output='Error occurred')
        
        # Act
        with patch('builtins.print') as mock_print:
            call_rclone('ls', RCLONE_PATH)
        
        # Assert error handling
        mock_run.assert_called_once_with(['rclone', 'ls', RCLONE_PATH], check=True, text=True, capture_output=True)
        mock_print.assert_any_call(f"Error calling rclone: {mock_run.side_effect}")
        mock_print.assert_any_call('Output:\n', 'Error occurred')

if __name__ == '__main__':
    unittest.main()
