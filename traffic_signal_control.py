def traffic_signal_control(vehicle_count):
    """
    Simple rule-based traffic signal green light duration controller.
    """
    if vehicle_count > 15:
        green_light_duration = 60
    elif vehicle_count > 5:
        green_light_duration = 30
    else:
        green_light_duration = 10

    print(f'Green light duration set to {green_light_duration} seconds based on vehicle count {vehicle_count}')
    return green_light_duration

if __name__ == '__main__':
    vehicle_count = 12  # Example vehicle count
    traffic_signal_control(vehicle_count)
