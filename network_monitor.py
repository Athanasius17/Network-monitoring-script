#!/usr/bin/env python3
"""
Simple Network Monitoring Script
Author: Athanasius Otieno
Description: Basic network monitoring tool that checks connectivity and network health
"""

import os
import time
import datetime
import subprocess
import platform

def ping_host(host):
    """
    Ping a host and return True if successful, False otherwise
    """
    # Determine ping command based on operating system
    param = "-n" if platform.system().lower() == "windows" else "-c"
    
    # Run ping command
    command = ["ping", param, "1", host]
    
    try:
        # Execute ping command
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False

def get_response_time(host):
    """
    Get response time for a host
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            # Extract response time from ping output
            output = result.stdout
            if "time=" in output:
                # Parse response time (works for both Windows and Linux)
                import re
                time_match = re.search(r'time[<=](\d+(?:\.\d+)?)m?s', output)
                if time_match:
                    return float(time_match.group(1))
        return None
    except Exception:
        return None

def check_internet_connection():
    """
    Check if internet connection is available
    """
    test_hosts = ["8.8.8.8", "1.1.1.1", "google.com"]
    
    for host in test_hosts:
        if ping_host(host):
            return True
    return False

def log_result(message, log_file="network_monitor.log"):
    """
    Log monitoring results to file
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    
    try:
        with open(log_file, "a") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Error writing to log file: {e}")

def monitor_hosts(hosts, interval=60, log_to_file=True):
    """
    Monitor multiple hosts continuously
    """
    print("Starting Network Monitor...")
    print(f"Monitoring hosts: {', '.join(hosts)}")
    print(f"Check interval: {interval} seconds")
    print("Press Ctrl+C to stop monitoring\n")
    
    try:
        while True:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Network Check at {timestamp} ---")
            
            # Check internet connectivity
            if check_internet_connection():
                print("✓ Internet connection: ONLINE")
                if log_to_file:
                    log_result("Internet connection: ONLINE")
            else:
                print("✗ Internet connection: OFFLINE")
                if log_to_file:
                    log_result("Internet connection: OFFLINE")
            
            # Check each host
            for host in hosts:
                if ping_host(host):
                    response_time = get_response_time(host)
                    if response_time:
                        status_msg = f"✓ {host}: REACHABLE ({response_time}ms)"
                    else:
                        status_msg = f"✓ {host}: REACHABLE"
                    print(status_msg)
                    if log_to_file:
                        log_result(status_msg)
                else:
                    status_msg = f"✗ {host}: UNREACHABLE"
                    print(status_msg)
                    if log_to_file:
                        log_result(status_msg)
            
            print(f"\nNext check in {interval} seconds...")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")
        if log_to_file:
            log_result("Network monitoring stopped by user")

def single_check(hosts):
    """
    Perform a single network check
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Network Status Check - {timestamp}")
    print("=" * 50)
    
    # Check internet
    if check_internet_connection():
        print("Internet Connection: ✓ ONLINE")
    else:
        print("Internet Connection: ✗ OFFLINE")
    
    print("\nHost Connectivity:")
    for host in hosts:
        if ping_host(host):
            response_time = get_response_time(host)
            if response_time:
                print(f"{host:20} ✓ REACHABLE ({response_time}ms)")
            else:
                print(f"{host:20} ✓ REACHABLE")
        else:
            print(f"{host:20} ✗ UNREACHABLE")

def main():
    """
    Main function
    """
    # Default hosts to monitor (you can modify this list)
    default_hosts = [
        "8.8.8.8",          # Google DNS
        "1.1.1.1",          # Cloudflare DNS
        "google.com",       # Google
        "github.com",       # GitHub
        "192.168.1.1"       # Common router IP (modify as needed)
    ]
    
    print("Network Monitoring Script")
    print("=" * 30)
    print("1. Single check")
    print("2. Continuous monitoring")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == "1":
                single_check(default_hosts)
                
            elif choice == "2":
                try:
                    interval = int(input("Enter check interval in seconds (default 60): ") or "60")
                    monitor_hosts(default_hosts, interval)
                except ValueError:
                    print("Invalid interval. Using default 60 seconds.")
                    monitor_hosts(default_hosts, 60)
                    
            elif choice == "3":
                print("Exiting...")
                break
                
            else:
                print("Invalid option. Please select 1-3.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()