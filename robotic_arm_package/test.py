sort_sequence = [] # 새로운 Sequence 리스트를 생성하기 위한 LIST
used_indices = [] # 조합되지 않은 공을 위한 LIST

# 조합되지 않은 공 중 하나의 공만 정밀 작업하기 위한 스위치
color_modes = {'red': 'mode1', 'green': 'mode1', 'blue': 'mode1'}

target_list = []

# 확인되지 않은 공들을 찾아서 sort_sequence에 추가
for i in range(len(target_list)):
    if i not in used_indices:
        color_info = target_list[i]
        color = color_info.split('_')[0]  # 색상 추출
        
        if color_modes[color] == 'mode1':
            sort_sequence.insert(0,[color, i, 'mode1'])  # 조합되지 않은 공 추가
            color_modes[color] = 'mode2'  # 다음 동일 색상은 mode1로 설정
            color_dic[color] = i 
            
        elif color_modes[color] == 'mode2':
            sort_sequence.insert(0,[color, i, 'mode2'])  # 이미 확인된 동일 색상 공을 mode1로 추가
                

        else :
            pass