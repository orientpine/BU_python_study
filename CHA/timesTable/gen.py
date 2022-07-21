import pandas as pd

with pd.ExcelWriter("output.xlsx", engine="xlsxwriter") as writer:  # 빈테이블 만들기
    for col in range(2, 10):  # for loop # 열 순회
        single_col = []  # 빈 줄
        for row in range(1, 10):  # 행 순회
            s = f"{col} X {row} = {col*row}"
            single_col.append(s)
        df_single_col = pd.DataFrame(single_col, columns=[f"{col}단"])
        # df_single_row = single_col
        df_single_col.to_excel(writer, sheet_name=f"{col}단", index=False)  # 저장하자!
