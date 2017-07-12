# -*- coding: cp949 -*-
from bs4 import BeautifulSoup
import xlrd
import requests
import xlsxwriter
import numpy as np

workbook = xlrd.open_workbook("D://python_workspaces/keps_energy_crawling/�������¾��������.xlsx")
worksheet = workbook.sheet_by_index(0)

nrow = worksheet.nrows # ��Ʈ�� �� ����

data = []
i = 1 # ù ��° ���� ���� ���̱� ������ �� ���� �� ��ȣ ����
j = 0 # th Ȧ����° ��Ҹ� ũ�Ѹ��ϱ� ���� ����

content_workbook = xlsxwriter.Workbook('�������¾��������_�󼼳���.xlsx')  #�� �������� ����
content_worksheet = content_workbook.add_worksheet()

while i < nrow:
    # 0�� i���� �����Ͽ� ǰ�� �ڵ� ��ȣ�� ������ͼ� URL�� �ٿ��ش�.
    url = 'http://keps.energy.or.kr/beps/ST/MD/efficiencyDetail.do?viewCode=new&np20Index='+str(worksheet.col_values(0)[i])

    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    table_list = soup.find_all('table', {'class': 'dataTable'})

    # Class���� dataTable�� ù��° table �±��� tr�� �� �����´�.
    for tr in table_list[0].find_all('tr'):
        for td in tr.find_all('td'):
            #strip �Լ� : ���ڿ��� ���� ������ ��� �����ִ� �Լ�
            data.append(td.text.strip())

    # Class���� dataTable�� �ι�° table �±� ���� tbody�� �ڽ��� tr�� �� �����´�.
    for tr in table_list[1].tbody.find_all('tr'):
        for th in tr.find_all('th'):
            # ��Ҵ� 0���� �����ϱ� ������ Ȧ���� �Ǻ�
            if j%2 == 1:
                data.append(th.text.strip())
            j += 1

    # worksheet �� ��ȣ ī��Ʈ
    i += 1

# content_worksheet�� �� ������ �����ؾ��ϱ� ������ �ش� �׸� ����� ������ �����´�.
# len �Լ� : ��ü�� ������ ��ȯ�ϴ� �Լ�
ncols = len(table_list[1].tbody.find_all('th'))

# Class���� dataTable�� �ι�° table �±��� th �׸��� 2���� ���еǾ�����
# �ش� ������ ��� �±� ������ ����� ���� 2�� ����
ncols = (ncols/2)+len(table_list[0].find_all('td'))

# 2���� �迭�� ���� ������ �������� ���� numpy ���̺귯�� ���
# reshape �Լ� : n������ �迭 ����� �缳�����ִ� �Լ�
# -1 : �ٸ� ������ ���� ũ��( == ncols : 2���� ũ��)�� ���߰� ���� ũ�⸦ �ش� ������ �Ҵ����ִ� �Ķ���� ��
arr = np.reshape(data, (-1, int(ncols)))

# nrow-1 : ���� �� ����
for r in range(0, nrow-1):
    for c in range(0, int(ncols)):
        # ' '.join : ��ҵ� ���̿� ���� ����
        # split() : ��ȣ ���� ���� �������� ���ڿ��� �������ش�.
        # ���� ������ ������ �������� ���ڸ� ������.
        # (== ����(split)�� �������� ���ڿ��� ������, �ٽ� ����(join)�Ͽ� ���)
        arr_data = ' '.join((arr[r][c]).split())

        content_worksheet.write(r, c, arr_data)

content_workbook.close()