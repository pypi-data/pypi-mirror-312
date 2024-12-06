#!/usr/bin/env python3

import subprocess
import re

def extract_values(output):
    """
    Extracts the values of A, B, and C from the output string.
    Output format: 'A * B + C = ?'
    """
    match = re.search(r"(\d+)\s*\*\s*(\d+)\s*\+\s*(\d+)\s*=", output)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3))
    else:
        raise ValueError("Failed to parse the output from /flag.")

def run_flag():
    """
    Runs the /flag command, calculates the correct answer, 
    and provides it as input.
    """
    try:
        # Start the /flag process
        process = subprocess.Popen(
            ["/flag"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Read the output
        output = process.stdout.readline().strip()
        print(f"Challenge: {output}")  # For debugging/logging

        # Extract A, B, and C
        A, B, C = extract_values(output)
        answer = A * B + C

        # Send the correct answer
        process.stdin.write(f"{answer}\n")
        process.stdin.flush()

        # Get the result
        result = process.stdout.readline().strip()
        return result

    except FileNotFoundError:
        return "Error: '/flag' executable not found."
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """
    Main entry point for the script.
    """
    print("Executing /flag with automated input...")
    output = run_flag()
    print(f"Result: {output}")

if __name__ == "__main__":
    main()
