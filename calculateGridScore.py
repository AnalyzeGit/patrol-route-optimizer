#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Handling
import pandas as pd

# Module
from loadDatabase import *
from preprocessingPoint import *
from selectDatasetFluid import *

# Gis

import geopandas as gpd

# Preprocessing
from sklearn.preprocessing import StandardScaler

# Calculate
from math import radians, cos, sin, asin, sqrt


# In[2]:


# Action: 표준화 함수 생성

def standardize(data,col_list):
    
    # 스케일러 생성
    scaler = StandardScaler()
    
    # 데이터 스케일러
    data[col_list] = scaler.fit_transform(data[col_list])
    
    return data


# In[3]:


def calculate_gradient_effect(data,gradient):
    
    # 마지막 순위 추출
    rank_max = data['RANK'].max()
    
    # 만약 경사 25% 초과 시 순위에서 제거
    data.loc[data['GRADIENT']>=gradient, 'RANK'] = rank_max
    
    return data


# In[4]:


def reset_values(data):

    # 고유 값들을 정렬하여 새로운 값을 매핑할 사전 생성
    unique_values = sorted(data['RANK'].unique())
    new_values = range(len(unique_values))
    mapping_dict = {old: new for old, new in zip(unique_values, new_values)}

    # replace 함수를 사용하여 값을 새로운 값으로 매핑
    data['RANK'] = data['RANK'].replace(mapping_dict)
    
    return data


# <span style = 'background-color:rgba(0,0,255,0.3); color:white; padding:5px; border-radius:5px;'> 프로세스 </span>
# 1. 데이터 로드
# 2. 데이터 전처리
# 3. 데이터 병합
# 4. 점수 계산
# 5. 데이터 적재
# 6. 알고리즘 개발

# <span style = 'border:0.5px solid black; padding:5px; border-radius:5px;'>  1. 데이터 로드 </span>

# In[5]:


# Action: 데이터 로드

# 1.1 그리드 - 안전센터와의 거리
grid_safety_center = get_dataframe_from_database_fluid('an_distance_safety_center')

# 1,2 그리도 - 안전 비상벨과의 거리
grid_safety_emergency_bell = get_dataframe_from_database_fluid('an_distance_safety_emergency_bell')

# 1.3 그리드 위치
grid_point = get_dataframe_from_database_fluid('an_grid_point')

# 1.4 그리도 - 서울 쉼터(buffer) 점수
grid_shelter = get_dataframe_from_database_fluid('an_distance_score_shelter')

# 1,5 그리드 - 경사 
#grid_gradient = get_dataframe_from_database_fluid('an_gird_gradiednt')

# 1,6 그리드 - 안전시설물 
grid_safety_facilities = get_dataframe_from_database_fluid('an_distance_score_facilities')

# 1,7 그리드 - cctv 
grid_safety_cctv = get_dataframe_from_database_fluid('an_numpoins_cctv') # 23살


# <span style = 'border:0.5px solid black; padding:5px; border-radius:5px;'>  2. 데이터 전처리 </span>

# In[6]:


# Action: 데이터 전처리

# 2.1 데이터 그룹화
grid_safety_center = grid_safety_center.groupby('INPUT_ID').mean()[['DISTANCE']].reset_index() # 안전센터 거리 그룹화
grid_safety_emergency_bell = grid_safety_emergency_bell.groupby('INPUT_ID').mean()[['DISTANCE']].reset_index() # 비상벨 거리 그룹화
grid_shelter = grid_shelter.groupby('ID').mean()[['GRID_SHELTER_DISTANCE_SCORE']].reset_index() # 무더위 쉼터 거리 그룹화
grid_safety_facilities = grid_safety_facilities.groupby('ID').mean()[['GRID_FACILITIES_DISTANCE_SCORE']].reset_index() # 안전시설물 그룹화

# 2.2 데이터 변수명 변경
grid_safety_center.columns = ['ID','SAFETY_CENTER_AND_DISTANCE'] # 안전센터 변수명 변경
grid_safety_emergency_bell.columns = ['ID','EMERGENCY_BELL_AND_DISTANCE'] # 비상벨 변수명 변경

# 2.3 위도, 경도 추출
grid_point = grid_point[['ID','LON','LAT','DISTRICT']]

# 2.4.데이터 변수 추출
grid_shelter = grid_shelter[['ID','GRID_SHELTER_DISTANCE_SCORE']] # 서울 쉼터 변수 추출

# 2.5 CCTV 변수 변환(방향에 맞게)
grid_safety_cctv['NUMBER_OF_CCTV']  = grid_safety_cctv['NUMBER_OF_CCTV'] + 1

grid_safety_cctv['NUMBER_OF_CCTV'] = 1/ grid_safety_cctv['NUMBER_OF_CCTV']


# <span style = 'border:0.5px solid black; padding:5px; border-radius:5px;'>  3. 데이터 병합 </span>

# In[7]:


# Action: 데이터 병합

# 3.1 안전센터, 비상벨 병합
merge = pd.merge(grid_safety_emergency_bell,grid_safety_center,on='ID',how='left')

# 3.2 그리드 위치 - 안전센터,비상벨 병합
mergeb = pd.merge(grid_point,merge,on='ID',how='left')

# 3.3 # - 서울 쉼터 병합
mergec = pd.merge(mergeb,grid_shelter,on='ID',how='left')

# 3.4 - 그리드 - 경사도 병합
#merged = pd.merge(mergec, grid_gradient[['ID','GRADIENT']], on='ID', how='left')

# 3.5 - 그리드 - 안전 시설물
merged = pd.merge(mergec, grid_safety_facilities[['ID','GRID_FACILITIES_DISTANCE_SCORE']], on='ID', how='left')

# 3.6 - 그리드 - 안전 시설물
mergee = pd.merge(merged, grid_safety_cctv[['ID','NUMBER_OF_CCTV']], on='ID', how='left')


# <span style = 'border:0.5px solid black; padding:5px; border-radius:5px;'>  4. 점수 계산 </span>

# In[8]:


# Action: 처리 전 데이터 정제

# 1 .변수 순서 변경
mergee = mergee[['ID','EMERGENCY_BELL_AND_DISTANCE','SAFETY_CENTER_AND_DISTANCE','GRID_SHELTER_DISTANCE_SCORE','GRID_FACILITIES_DISTANCE_SCORE','NUMBER_OF_CCTV','LON','LAT','DISTRICT']]

# 2, 스케일(점수 합산 변수) 
standarize_list = ['EMERGENCY_BELL_AND_DISTANCE','SAFETY_CENTER_AND_DISTANCE','GRID_SHELTER_DISTANCE_SCORE','GRID_FACILITIES_DISTANCE_SCORE','NUMBER_OF_CCTV'] # 스케일 사용 변수
standarize_data = standardize(mergee,standarize_list) # 표준화


# In[9]:


# Action: 점수 계산

# 1. 점수 계산  
standarize_data['SCORE'] = standarize_data['EMERGENCY_BELL_AND_DISTANCE'] + standarize_data['SAFETY_CENTER_AND_DISTANCE'] + standarize_data['GRID_SHELTER_DISTANCE_SCORE'] 
+  standarize_data['GRID_FACILITIES_DISTANCE_SCORE'] + standarize_data['NUMBER_OF_CCTV']

# 2. 순위 선정
standarize_data['RANK'] = standarize_data['SCORE'].rank(ascending=False)

# 3, 경사 4 이상 순위 수정
#standarize_data = calculate_gradient_effect(standarize_data,3)

# 4. rank 정리
standarize_data = reset_values(standarize_data)
#labels, unique = pd.factorize(standarize_data['RANK'])

#standarize_data['RANK'] = labels


# In[10]:


# Action: 구간화

# 1. 데이터 시리즈를 9개의 균등한 구간으로 구간화
labels = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 2. 구간화  
categories = pd.cut(standarize_data['SCORE'], 9,  labels=labels)

# 3. 구간화 파생변수 생성
standarize_data['SCORE_CATEGORY'] = categories


# <span style = 'border:0.5px solid black; padding:5px; border-radius:5px;'>  5. 데이터 적재 </span>

# In[25]:


# Action: 데이터 저장

standarize_data.to_csv('서울시_점수.csv',index=False)


# In[11]:


# Action: DB 적재

load_database(standarize_data,'an_rank')


# <span style = 'border:0.5px solid black; padding:5px; border-radius:5px;'>  6. 알고리즘 개발(사용 X) </span>

# In[12]:


# Action: 경도, 위도 변환

# 경도, 위도 연속형 변수 변환

standarize_data['LON'] = standarize_data['LON'].astype(float)
standarize_data['LAT'] = standarize_data['LAT'].astype(float)


# In[36]:


# Action: 경도, 위도 변환

# 경도, 위도 연속형 변수 변환

standarize_data['LON'] = standarize_data['LON'].astype(float)
standarize_data['LAT'] = standarize_data['LAT'].astype(float)


# In[37]:


def haversine(lon1, lat1, lon2, lat2):
    
    # 위도와 경도를 라디안으로 변환
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # haversine 공식
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # 지구의 반지름(km 단위)
    return c * r

# 현재 위치 (예: 서울 시청)
current_lon, current_lat = test[['LON','LAT']].values[0]

# DataFrame의 각 위치까지의 거리 계산
standarize_data['거리(km)'] = standarize_data.apply(lambda x: haversine(current_lon, current_lat, x['LON'], x['LAT']), axis=1)


# In[38]:


# Action: 거리를 기준으로 정렬 및 RANK 조건을 이용한 추출

# 거리 순서 정렬
standarize_data = standarize_data.sort_values(by=['거리(km)','RANK'])

# rank가 200 미만인 위치 찾기
valid_locations_indices  = standarize_data[standarize_data['RANK'] < 200]

lon, lat = valid_locations_indices.iloc[5][['LON','LAT']]
lonb, latb = valid_locations_indices.iloc[1][['LON','LAT']]
lonc, latc = valid_locations_indices.iloc[2][['LON','LAT']]
lond, latd = valid_locations_indices.iloc[3][['LON','LAT']]
lone, late = valid_locations_indices.iloc[4][['LON','LAT']]


# In[40]:


import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.scatter(standarize_data['LON'], standarize_data['LAT'], c='blue', label='위치')
plt.scatter(current_lon, current_lat, c='green', label='현재 위치')
plt.scatter(lon, lat, c='red', label='현재 위치')
plt.scatter(lonb, latb, c='red', label='현재 위치')
plt.scatter(lonc, latc, c='red', label='현재 위치')
plt.scatter(lond, latd, c='red', label='현재 위치')
plt.scatter(lone, late, c='red', label='현재 위치')
plt.xlabel('경도')
plt.ylabel('위도')
plt.legend()
plt.show()

