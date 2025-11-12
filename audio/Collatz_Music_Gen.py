import csv
import random

def collatz_seq(n, steps=50):
    """Generate Collatz sequence values"""
    for _ in range(steps):
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        yield n

def harmony_adjustment(value, avg_output):
    """Apply harmony adjustment based on average output"""
    # Use the Collatz value itself as the "temperature"
    temp = (value % 10) / 10.0  # normalize to 0-1
    adjustment = temp - (avg_output % 1)  # compare with fractional part
    if abs(adjustment) < 0.01:
        return temp
    elif adjustment > 0:
        return min(1.0, temp * 1.1)  # slight increase
    else:
        return max(0.1, temp * 0.9)  # slight decrease

# Main execution - Agent_Local's Swarm Algorithm
scale = [60, 62, 64, 65, 67, 69, 71]  # C major
n = 27  # initial value for the Collatz sequence

# Generate Collatz sequence
sequence = list(collatz_seq(n, steps=50))
avg_output = sum(sequence) / len(sequence)

# Apply harmony adjustments
adjusted_values = [harmony_adjustment(val, avg_output) for val in sequence]

# Write output to CSV
with open('collatz_music.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['time', 'pitch', 'velocity', 'duration'])
    
    for i, adj_val in enumerate(adjusted_values):
        time = i * 0.1  # arbitrary time increment
        pitch = scale[int(sequence[i] % len(scale))]
        velocity = int(50 + adj_val * 50)  # velocity based on adjustment
        duration = 0.5 + adj_val  # duration based on adjustment
        writer.writerow([time, pitch, velocity, duration])

print(f"Generated {len(adjusted_values)} musical events from Collatz sequence starting at {n}")
print(f"Average sequence value: {avg_output:.2f}")
print(f"Sequence sample: {sequence[:10]}...")
print("Output saved to collatz_music.csv")