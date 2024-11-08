import subprocess
import os
from dotenv import load_dotenv

def call_rclone(command, *args):
    """
    Function to call rclone with the specified command and arguments.

    Parameters:
    command (str): The rclone command to execute (e.g., 'list', 'sync', etc.).
    *args: Additional arguments for the rclone command.
    """

    # Build the rclone command
    rclone_command = ['rclone', command] + list(args)

    try:
        # Call rclone and capture the output
        result = subprocess.run(rclone_command, check=True, text=True, capture_output=True)
        
        # Print the result (output from rclone)
        print("Output:\n", result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"Error calling rclone: {e}")
        print("Output:\n", e.output)  # Show the output if there's an error
        
# Example usage
if __name__ == "__main__":
    load_dotenv()
    RCLONE_PATH = os.getenv('RCLONE_PATH')
    # Example: List files in a remote storage (replace 'remote:path' with your actual remote path).
    call_rclone('ls', RCLONE_PATH)
