import random
import time
import csv

def simulate_sensor_data(file_path='sensor_data.csv', duration=60, interval=5):
    """
    Simulate traffic sensor data for 'duration' seconds, generating vehicle count and average speed every 'interval' seconds.
    """
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'vehicle_count', 'average_speed_kmph'])

        start_time = time.time()
        while time.time() - start_time < duration:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            vehicle_count = random.randint(5, 20)
            average_speed = random.uniform(20, 80)

            writer.writerow([timestamp, vehicle_count, round(average_speed, 2)])
            print(f'{timestamp} - Vehicles: {vehicle_count}, Speed: {average_speed:.2f} km/h')

            time.sleep(interval)

if __name__ == '__main__':
    simulate_sensor_data()
