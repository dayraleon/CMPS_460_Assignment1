import pandas as pd

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0
        self.remaining_time = burst_time  # Only for preemptive scheduling

def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0
    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        process.waiting_time = current_time - process.arrival_time
        process.turnaround_time = process.waiting_time + process.burst_time
        current_time += process.burst_time
    return processes

def sjf_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0
    completed_processes = []

    while processes:
        ready_queue = [p for p in processes if p.arrival_time <= current_time]
        if ready_queue:
            ready_queue.sort(key=lambda x: x.burst_time)
            process = ready_queue[0]
            processes.remove(process)
            process.waiting_time = current_time - process.arrival_time
            current_time += process.burst_time
            process.turnaround_time = process.waiting_time + process.burst_time
            completed_processes.append(process)
        else:
            current_time += 1  # No process is ready, increment time

    return completed_processes

def round_robin_scheduling(processes, time_quantum):
    current_time = 0
    ready_queue = []
    completed_processes = []

    while processes or ready_queue:
        while processes and processes[0].arrival_time <= current_time:
            ready_queue.append(processes.pop(0))
        
        if ready_queue:
            process = ready_queue.pop(0)
            if process.remaining_time > time_quantum:
                current_time += time_quantum
                process.remaining_time -= time_quantum
                ready_queue.append(process)  # Re-add to the queue
            else:
                current_time += process.remaining_time
                process.turnaround_time = current_time - process.arrival_time
                process.remaining_time = 0
                completed_processes.append(process)
        else:
            current_time += 1  # No process is ready, increment time

    return completed_processes

def display_results(algorithm_name, processes):
    print(f"\nResults for {algorithm_name}:")
    data = []
    for process in processes:
        data.append({
            'Process ID': process.pid,
            'Arrival Time': process.arrival_time,
            'Burst Time': process.burst_time,
            'Waiting Time': process.waiting_time,
            'Turnaround Time': process.turnaround_time
        })
    
    df = pd.DataFrame(data)
    print(df.to_string(index=False)) 
    print(f"Average Waiting Time: {df['Waiting Time'].mean():.2f}")
    print(f"Average Turnaround Time: {df['Turnaround Time'].mean():.2f}")

# Example processes
processes = [
    Process(1, 0, 8),
    Process(2, 1, 4),
    Process(3, 2, 9),
    Process(4, 3, 5)
]

# Run the algorithms and display results
fcfs_processes = fcfs_scheduling(processes.copy())
display_results("First-Come, First-Serve (FCFS)", fcfs_processes)

sjf_processes = sjf_scheduling(processes.copy())
display_results("Shortest Job First (SJF)", sjf_processes)

rr_processes = round_robin_scheduling(processes.copy(), time_quantum=3)
display_results("Round Robin", rr_processes)
