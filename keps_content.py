# -*- coding: cp949 -*-
from bs4 import BeautifulSoup
import xlrd
import requests
import xlsxwriter
import numpy as np

workbook = xlrd.open_workbook("D://python_workspaces/keps_energy_crawling/결정질태양전지모듈.xlsx")
worksheet = workbook.sheet_by_index(0)

nrow = worksheet.nrows # 시트의 행 갯수

data = []
i = 1 # 첫 번째 행은 제목 행이기 때문에 그 다음 행 번호 선택
j = 0 # th 홀수번째 요소를 크롤링하기 위한 변수

content_workbook = xlsxwriter.Workbook('결정질태양전지모듈_상세내역.xlsx')  #새 엑셀파일 실행
content_worksheet = content_workbook.add_worksheet()

while i < nrow:
    # 0열 i행을 선택하여 품목 코드 번호를 가지고와서 URL에 붙여준다.
    url = 'http://keps.energy.or.kr/beps/ST/MD/efficiencyDetail.do?viewCode=new&np20Index='+str(worksheet.col_values(0)[i])

    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    table_list = soup.find_all('table', {'class': 'dataTable'})

    # Class명이 dataTable인 첫번째 table 태그의 tr을 다 가져온다.
    for tr in table_list[0].find_all('tr'):
        for td in tr.find_all('td'):
            #strip 함수 : 문자열의 양쪽 공백을 모두 지워주는 함수
            data.append(td.text.strip())

    # Class명이 dataTable인 두번째 table 태그 하위 tbody의 자식인 tr을 다 가져온다.
    for tr in table_list[1].tbody.find_all('tr'):
        for th in tr.find_all('th'):
            # 요소는 0부터 시작하기 때문에 홀수로 판별
            if j%2 == 1:
                data.append(th.text.strip())
            j += 1

    # worksheet 행 번호 카운트
    i += 1

# content_worksheet의 열 갯수를 지정해야하기 때문에 해당 항목 요소의 갯수를 가져온다.
# len 함수 : 객체의 갯수를 반환하는 함수
ncols = len(table_list[1].tbody.find_all('th'))

# Class명이 dataTable인 두번째 table 태그의 th 항목이 2개로 구분되어있음
# 해당 내용이 담긴 태그 갯수만 들오기 위해 2로 나눔
ncols = (ncols/2)+len(table_list[0].find_all('td'))

# 2차원 배열을 쉽고 빠르게 가져오기 위해 numpy 라이브러리 사용
# reshape 함수 : n차원의 배열 모양을 재설정해주는 함수
# -1 : 다른 나머지 차원 크기( == ncols : 2차원 크기)를 맞추고 남은 크기를 해당 차원에 할당해주는 파라미터 값
arr = np.reshape(data, (-1, int(ncols)))

# nrow-1 : 제목 행 제외
for r in range(0, nrow-1):
    for c in range(0, int(ncols)):
        # ' '.join : 요소들 사이에 공백 삽입
        # split() : 괄호 안의 값을 기준으로 문자열을 나누어준다.
        # 값이 없으면 공백을 기준으로 문자를 나눈다.
        # (== 공백(split)을 기준으로 문자열을 나누고, 다시 연결(join)하여 출력)
        arr_data = ' '.join((arr[r][c]).split())

        content_worksheet.write(r, c, arr_data)

content_workbook.close()