#!/usr/bin/python
# -*- coding:utf-8 -*- 

import pandas as pd
import sys
import os
import random


def path_isExists(path):
    # 引入模块
    import os
 
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    return isExists


def mkdir(path):
    # 引入模块
    import os
 
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print(path+' 创建成功')
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
        return False



os.chdir("D:\\myworkstation\\")


with open("data_selected_file_path.txt", "r") as result_file:
    for file_path in result_file.readlines():
        file_path = file_path.strip()
#        file_path = ".\\data\\gene\\brain\\"
        data_file_name = "data.txt"
        feature_file_name = "features.txt"
        cluster_name_file_name = "row.label"
        
#        print(file_path.split("data")[-1])
        
        file_output_path = ".\\data_selected" + file_path.split("data")[-1]
        
        # 调用函数创建的目录
        mkdir(file_output_path)
        
        data = pd.read_csv(file_path+data_file_name,sep=",| |\t",header=None, engine='python')
        cluster_names = pd.read_csv(file_path+cluster_name_file_name,sep=",",header=None, engine='python')
        
        row_num ,column_num = data.shape
        print(row_num ,column_num)
        
        # 根据比例筛选数据
        row_selected_rate = 0.3
        column_selected_rate = 0.1
        row_selected = random.sample(range(row_num), int(row_selected_rate*row_num))
        column_selected = random.sample(range(column_num), int(column_selected_rate*column_num))
        print("row_selected=>", len(row_selected))
        print("column_selected=>", len(column_selected))
        
        row_unselected = list(set(range(row_num)) - set(row_selected))
        column_unselected = list(set(range(column_num)) - set(column_selected))
        
        print("row_unselected=>", len(row_unselected))
        print("row_unselected=>", len(column_unselected))
        
        with open(file_output_path + "row_selected_" + str(int(row_selected_rate*100)) + "_" + str(int(column_selected_rate*100)) +  ".txt", "w+") as result_file:
            print("\n".join([str(w) for w in row_selected]), file=result_file)
    
        with open(file_output_path + "column_selected_" + str(int(row_selected_rate*100)) + "_" + str(int(column_selected_rate*100)) +  ".txt", "w+") as result_file:
            print("\n".join([str(c) for c in column_selected]), file=result_file)
            
        # 作为类别已知的数据
        selected_data = data.ix[row_selected, column_selected]
        selected_cluster_names = cluster_names.ix[row_selected,:]
        
        
        # 输出数据
        selected_data.to_csv(file_output_path + "selected_data_" + str(int(row_selected_rate*100)) + "_" + str(int(column_selected_rate*100)) +  ".txt", sep=",", header=None, index=False)
        selected_cluster_names.to_csv(file_output_path + "selected_cluster_names_" + str(int(row_selected_rate*100)) + "_" + str(int(column_selected_rate*100)) +  ".txt", sep=",", header=None, index=False)    
        
        
        # 作为类别未知的数据
        unselected_data = data.ix[row_unselected, column_selected]
        unselected_cluster_names = cluster_names.ix[row_unselected,:]


        # 输出数据
        unselected_data.to_csv(file_output_path + "unselected_data_" + str(int((row_selected_rate)*100)) + "_" + str(int(column_selected_rate*100)) +  ".txt", sep=",", header=None, index=False)
        unselected_cluster_names.to_csv(file_output_path + "unselected_cluster_names_" + str(int((row_selected_rate)*100)) + "_" + str(int(column_selected_rate*100)) +  ".txt", sep=",", header=None, index=False)
        
        
        if path_isExists(file_path+feature_file_name):
    
            features = pd.read_csv(file_path+feature_file_name,sep=",",header=None, engine='python')
            
            selected_features = features.ix[column_selected,:]
            selected_features.to_csv(file_output_path + "selected_features_"+ str(int(row_selected_rate*100)) + "_" + str(int(column_selected_rate*100)) +  ".txt", sep=",", header=None, index=False)
    
            unselected_features = features.ix[column_unselected,:]
            unselected_features.to_csv(file_output_path + "unselected_features_"+ str(int(row_selected_rate*100)) + "_" + str(int((column_selected_rate)*100)) +  ".txt", sep=",", header=None, index=False)
