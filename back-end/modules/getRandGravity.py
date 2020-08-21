# 중력을 랜덤 변경하는 모듈
import random
def getRandGravity():
    tmp = random.randint(0,3)
    res = ''
    if tmp == 0: res = 'N'
    if tmp == 1: res = 'S'
    if tmp == 2: res = 'W'
    if tmp == 3: res = 'E'

    return res

# DEBUGGING CODE
#print(getRandGravity())