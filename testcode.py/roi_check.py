import cv2

# 변수 초기화
roi_list = []
n_rois = 2  # 원하는 ROI 개수
drawing = False
ix, iy = -1, -1

# 마우스 콜백 함수
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, roi_list

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('image', img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
        roi_list.append((ix, iy, x, y))
        cv2.imshow('image', img)

# 카메라에서 프레임 캡처
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)  # 0번 카메라 장치(기본 웹캠)를 사용
if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

# 카메라에서 한 장의 프레임을 캡처
ret, img = cap.read()
if not ret:
    print("프레임을 가져올 수 없습니다.")
    cap.release()
    exit()

# 캡처한 이미지 저장 (원한다면 저장하지 않고 바로 사용 가능)
# cv2.imwrite('captured_frame.jpg', img)

# 카메라 종료
cap.release()

# 윈도우 생성 및 마우스 콜백 함수 설정
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_rectangle)

print("이미지에서 ROI를 선택하세요. 좌클릭으로 드래그하여 ROI를 선택하세요.")

# ROI 선택 루프 (2개의 ROI를 선택할 때까지 반복)
while len(roi_list) < n_rois:
    cv2.imshow('image', img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC 키를 누르면 종료
        break

cv2.destroyAllWindows()

# 선택한 ROI 출력
print("선택한 ROI 목록:")
for i, roi in enumerate(roi_list):
    print(f"ROI {i+1}: {roi}")

# ROI 저장 예시
# 각 ROI에 해당하는 이미지를 따로 저장할 수도 있음
for i, roi in enumerate(roi_list):
    roi_img = img[roi[1]:roi[3], roi[0]:roi[2]]  # (y1:y2, x1:x2)
    cv2.imwrite(f'roi_{i+1}.jpg', roi_img)

print("ROI 저장 완료!")
