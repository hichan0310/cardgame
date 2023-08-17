import cv2



for name in ["tania", "chloe", "lucifer", "gidon", "astin", "petra"]:
    # 동영상 파일 경로 설정
    video_path = f'{name}.mp4'

    # 동영상 캡처 객체 생성
    cap = cv2.VideoCapture(video_path)

    # 저장될 이미지 파일 경로와 이름 패턴 설정
    output_folder = f'C:/Users/maxma/PycharmProjects/cardgame/gacha/{name}/frame'
    image_name_pattern = '_{}.png'

    # 이미지 파일 저장을 위한 카운터 초기화
    frame_count = 0

    while True:
        ret, frame = cap.read()
        print('\r', frame_count, end='')
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
    print()