def alert_driver(congestion_level):
    if congestion_level == 'high':
        print('ALERT: High traffic congestion ahead. Please consider alternate routes.')
    elif congestion_level == 'medium':
        print('Traffic is moderate. Drive carefully.')
    else:
        print('Traffic flow is smooth.')

if __name__ == '__main__':
    alert_driver('high')  # Example alert for high congestion
