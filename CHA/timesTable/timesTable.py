import pandas as pd

# 구구단을 아래와 같이 생성해야함
# 1 X 1  = 1
# 1 X 2 = 2
# .....
print("프로그램 실행")
with pd.ExcelWriter("output.xlsx") as writer:
    # 일단 기초적인 구구단 생성
    for i in range(2, 10):
        table = []
        for j in range(1, 10):
            s = f"{i} X {j} = {i * j}"
            # 작성된 구구단 저장
            table.append(s)
        # 모여진 구구단 df로 만들기
        df = pd.DataFrame(table, columns=[f"{i}단"])
        # 만들어진 df 엑셀로 저장
        df.to_excel(writer, sheet_name=f"{i}단")
