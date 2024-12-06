

def print_output(stdout, stderr):
    """Print the output of a command."""
    if stdout:
        print("Output:\n", stdout)
    if stderr:
        print("Error:\n", stderr)