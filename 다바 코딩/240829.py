T = int(input())
for tc in range(1, T+1):
    N, M = map(int, input().split())
    arr = [input() for _ in range(N)]

    pwd = [0]*8 # 암호
    
    for i in range(N):
        for j in range(M-1, 54, -1): # 암호 코드 길이가 56이므로 55번째 인덱스까지 확인
            if arr[i][j] == '1': # 암호 코드의 끝을 찾으면..
                pcode = arr[i][j-55:j+1]
                break
        if pcode:
            break
    for i in range(8):
        pwd[i] = pat[pcode[i*7:(i+1)*7]]
    print(pwd)