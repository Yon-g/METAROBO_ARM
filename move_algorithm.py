import itertools
import time

D_DIC = {
    'BLUE' : 0,
    'GREEN' : 1,
    'RED' : 2,
    'BUTTON' : 3,
    'ERROR' : 4,
    'ARRIVE_IDX' : 6
}

start = time.time()

ball_squence = [0,1,2,3,4,5] # 공 번호 리스트
ball_dst = ['BLUE','GREEN','RED','ERROR','ERROR','ERROR'] #공을 잡았을 때의 목적지,' 인덱스' 번호 = 공번호
perms = list(itertools.permutations(ball_squence)) # 순열 생성
perms_2 = list(itertools.permutations(ball_dst)) # 순열 생성
# perms: 모든 경우의 공 잡는 순서가 들어있는 리스트

#각 공으로부터 도착지점까지 거리값 리스트 , 거리값 테이블 참고
cost_list = [
    [26.0, 22.0, 21.0, 10.0, 15.0],
    [23.0, 17.5, 16.5, 15.0, 18.5],
    [20.0, 13.0, 12.0, 19.0, 22.0],
    [24.0, 20.5, 22.0, 10.0, 19.0],
    [20.0, 16.0, 17.0, 15.0, 21.5],
    [16.5, 11.5, 13.5, 19.0, 25.0],
    [34.0, 31.0, 30.0, 0.0 , 25.0]
]

# 공 잡는 순서와 총 비용이 들어가는 리스트
result_list = []
count = 0
PATH_PRINT = False
for ball_destination in perms_2:
    for sequence in perms: # 공 잡는 순서의 경우의 수를 하나씩 꺼내서 총 비용 계산
        total_cost = 0 # 총 비용값 저장 변수
        n_loc = 'BUTTON' # 현재 로봇팔 위치

        for ball in sequence: # 공 잡는 순서를 하나씩 꺼내서 순서대로 진행
            loc_2_ball = cost_list[ball][D_DIC[n_loc]] # 현재 위치부터 공까지 비용
            total_cost += loc_2_ball # 총 비용에 합산

            ball_2_loc = cost_list[ball][D_DIC[ball_destination[ball]]] # 공부터 공 도착지까지 비용
            total_cost += ball_2_loc # 총 비용에 합산
            
            n_loc = ball_destination[ball] # 로봇팔의 현재 위치 변경
    
            if PATH_PRINT: # 이동 경로 출력
                print('{:>6} -> {:<6}: {:<6}'.format(n_loc, ball, loc_2_ball)) # 현재위치 -> 공 번호 : 비용
                print('{:>6} -> {:<6}: {:<6}'.format(ball, ball_destination[ball], ball_2_loc)) # 공 번호 -> 도착지 : 비용

        total_cost += cost_list[D_DIC['ARRIVE_IDX']][D_DIC[n_loc]] # 마지막으로 현재위치부터 버튼까지 이동

        if PATH_PRINT:
            print('{:>6} -> {:<6}: {:<6}'.format(n_loc,'BUTTON' , cost_list[D_DIC['ARRIVE_IDX']][D_DIC[n_loc]])) # 현재 위치 -> BUTTON : 비용
            
        result_list.append([sequence,total_cost])

    result_list.sort(key=lambda x:x[1], reverse=True) # 총 비용값을 기준으로 내림차순 정렬

    finish = time.time()- start # 걸린 시간 측정
    worst_path = result_list[0]
    best_path = result_list[-1]

    print("가장 안좋은 공 잡는 순서", worst_path[0])
    print("가장 긴 경로 비용 :", worst_path[1] )
    print("가장 좋은 공 잡는 순서 : ", best_path[0])
    print("가장 짧은 경로 비용 : ", best_path[1])
    print("걸린시간:",finish)
    if ball_dst[best_path[0][-1]] != "ERROR":
        print("마지막이 에러가 아닐경우가 최선")
        count+=1

print("에러가 아닌경우 최선 개수:",count)
print("총 경우의 수",len(perms)*len(perms_2))