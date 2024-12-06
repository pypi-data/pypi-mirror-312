# afusion/execution.py

import subprocess
from loguru import logger

def run_alphafold(command, placeholder=None):
    """
    Runs the AlphaFold Docker command and captures output.
    Uses placeholder to update output in real-time if provided.
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
    output_lines = []
    for line in iter(process.stdout.readline, ''):
        if line:
            output_lines.append(line)
            logger.debug(line.strip())
            # Update placeholder if provided
            if placeholder is not None:
                placeholder.markdown(f"```\n{''.join(output_lines)}\n```")
    process.stdout.close()
    process.wait()
    return ''.join(output_lines)
