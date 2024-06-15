#!/usr/bin/env python
# _*_ coding:utf-8 _*_


import xlrd
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
print(curPath)
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
sys.path.append('D:\\python_project\\untitled_1\\jiling_pengmo\\lib2')
sys.path.append('D:\\python_project\\untitled_1\\jiling_pengmo\\testAPI')

class ReadExcel():
     """读取excel文件数据"""
     def __init__(self,fileName=r'C:\Users\10043\Desktop\test_1.xls', SheetName="test_1"):
         self.data = xlrd.open_workbook(fileName)
         self.table = self.data.sheet_by_name(SheetName)

         # 获取总行数、总列数
         self.nrows = self.table.nrows
         self.ncols = self.table.ncols
     def read_data(self):
         if self.nrows > 1:
             # 获取第一行的内容，列表格式
             keys = self.table.row_values(0)
             listApiData = []
             # 获取每一行的内容，列表格式
             for col in range(1, self.nrows):
                 values = self.table.row_values(col)
                 # keys，values组合转换为字典
                 api_dict = dict(zip(keys, values))
                 listApiData.append(api_dict)
             return listApiData
         else:
             print("表格是空数据!")
             return None



if __name__ == '__main__':
    readexcel = ReadExcel().read_data()
    method = readexcel[0]['body']
    if readexcel[0]['headers'] == '':
        print('None')
    else:
        met = readexcel[0]['headers']
        print(met)

    print(readexcel)