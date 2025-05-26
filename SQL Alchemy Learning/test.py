# Create a new file called check_locks.py
import os
import psutil
import time

def find_processes_using_file(file_path):
    """Find all processes that have the specified file open."""
    file_path = os.path.abspath(file_path)
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            open_files = proc.info.get('open_files', [])
            if open_files:
                for file in open_files:
                    if file_path.lower() == getattr(file, 'path', '').lower():
                        processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name']
                        })
                        break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return processes

if __name__ == "__main__":
    db_path = os.path.abspath("sample.db")
    print(f"Checking processes using {db_path}...")
    
    processes = find_processes_using_file(db_path)
    if processes:
        print(f"Found {len(processes)} processes using the database:")
        for proc in processes:
            print(f"PID: {proc['pid']}, Name: {proc['name']}")
    else:
        print("No processes found using the database file directly.")