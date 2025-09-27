import cv2

car_cascade = cv2.CascadeClassifier('cars.xml')

def detect_vehicles(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 2)
    return len(cars), cars

def main():
    cap = cv2.VideoCapture('traffic_video3.mp4')  

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        count, cars = detect_vehicles(frame)

        for (x, y, w, h) in cars:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

        cv2.putText(frame, f'Vehicles: {count}', (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        cv2.imshow('Vehicle Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

