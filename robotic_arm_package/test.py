import threading

# 공유할 변수
shared_var = 0

# Lock 객체 생성
lock = threading.Lock()

def increment():
    global shared_var
    thread_name = threading.current_thread().name  # 현재 스레드의 이름
    for _ in range(100):
        with lock:
            shared_var += 1
            # Lock을 이용해 공유 변수와 관련된 출력을 동기화
            print(f"{thread_name}가 값을 증가시킴: {shared_var}")

# 스레드 생성
thread1 = threading.Thread(target=increment, name='Thread-1')
thread2 = threading.Thread(target=increment, name='Thread-2')

# 스레드 시작
thread1.start()
thread2.start()

# 스레드 종료 대기
thread1.join()
thread2.join()

print(f'최종 shared_var 값: {shared_var}')
