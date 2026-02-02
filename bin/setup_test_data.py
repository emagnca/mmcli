#!/usr/bin/env python3
"""
Automated setup script for test data using pexpect.
Executes a sequence of admin commands to create fields, types, permissions, roles, templates, and users.

Usage:
    python setup_test_data.py [test_name]
    
Example:
    python setup_test_data.py test
"""

import sys
import os
import pexpect
import time

def run_setup(test_name="test"):
    """
    Run the automated setup sequence for the given test name.
    
    Args:
        test_name: The name of the test (used to construct file paths)
    """
    
    # Start the mmadmin CLI
    try:
        child = pexpect.spawn('python -c "from mmcli import mmadmin; mmadmin.run()"', timeout=10, encoding='utf-8')
        child.logfile = sys.stdout
    except Exception as e:
        print(f"Error starting mmadmin CLI: {e}")
        sys.exit(1)
    
    commands = [
        f"create field data\\fields\\{test_name}.json",
        f"create type data\\types\\{test_name}.json",
        f"create permission data\\permissions\\{test_name}.json",
        f"create role data\\roles\\{test_name}.json",
        f"create template data\\templates\\{test_name}.json",
        f"create user data\\users\\{test_name}.json",
        "quit"
    ]
    
    try:
        # Wait for the initial (Cmd) prompt
        child.expect(r'\(Cmd\)', timeout=10)
        
        for cmd in commands:
            print(f"\n(Cmd) {cmd}")
            child.sendline(cmd)
            
            # Wait for the command prompt to return
            try:
                child.expect(r'\(Cmd\)', timeout=10)
            except pexpect.TIMEOUT:
                pass
        
        # Wait for the process to finish
        child.expect(pexpect.EOF, timeout=5)
        child.close()
        
        print("\nSetup completed successfully!")
        
    except pexpect.TIMEOUT:
        print(f"\nTimeout waiting for response")
        child.close()
        sys.exit(1)
    except Exception as e:
        print(f"\nError during setup: {e}")
        child.close()
        sys.exit(1)

if __name__ == "__main__":
    test_name = sys.argv[1] if len(sys.argv) > 1 else "test"
    run_setup(test_name)
