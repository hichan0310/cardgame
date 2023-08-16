import cv2

# 동영상 파일 경로 설정
video_path = 'mp4_file.mp4'

# 동영상 캡처 객체 생성
cap = cv2.VideoCapture(video_path)

# 저장될 이미지 파일 경로와 이름 패턴 설정
output_folder = 'C:/Users/maxma/PycharmProjects/cardgame/gacha/'
image_name_pattern = 'frame_{}.png'

# 이미지 파일 저장을 위한 카운터 초기화
frame_count = 0

while True:
    ret, frame = cap.read()
    print("asdf")
    if not ret:
        break

    # 이미지 파일 이름 생성
    image_name = image_name_pattern.format(frame_count)

    # 이미지 파일 저장
    cv2.imwrite(output_folder + image_name, frame)

    frame_count += 1

# 작업이 끝났으면 동영상 캡처 객체 해제
cap.release()
cv2.destroyAllWindows()