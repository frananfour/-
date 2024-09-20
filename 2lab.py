import cv2
from pyzbar.pyzbar import decode

# нужно вставить свой юрл
rtsp_url = "rtsp://<ip-адрес>:<порт>/stream"

# захваетываем видео
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Не удалось подключиться к RTSP потоку.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Не удалось получить кадр.")
        break

    # распознавание штрих-кодов на кадре
    barcodes = decode(frame)

    for barcode in barcodes:
        # дЕкодирование штрих-кода
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type

        # рисуем рамку вокруг штрих-кода
        points = barcode.polygon
        if len(points) == 4:
            pts = [(point.x, point.y) for point in points]
            pts = np.array(pts, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

        # Печать данных штрих-кода на кадре
        cv2.putText(frame, f'{barcode_data} ({barcode_type})', (barcode.rect.left, barcode.rect.top), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        print(f"Штрих-код: {barcode_data}, Тип: {barcode_type}")

    # Отображение видео с распознанными штрих-кодами
    cv2.imshow('RTSP Stream', frame)

    # Для выхода нажмите клавишу 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Закрытие окна
cap.release()
cv2.destroyAllWindows()