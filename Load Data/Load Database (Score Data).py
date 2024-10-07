#!/usr/bin/env python
# coding: utf-8

# In[97]:


# Handling
import pandas as pd

# Module
from loadDatabase import *
from preprocessingPoint import *

# gis
import geopandas as gpd


# <span style='background-color:rgba(0,0,255,0.3); color:white; padding: 5px; border-radius:5px;'> 프로세스 </span>
# 
# * 데이터 로드
# * 격자 위치 - 좌표 변경(함수)
# * 데이터 정제
# * 데이터 적재

# <span style='border:0.5px solid black; padding:5px; border-radius:5px;'> 데이터 로드 </span>

# In[100]:


# Action: 그룹화 및 집계

# 그룹화 및 집계 함수 정의
def most_frequent(series):
    return series.mode().iloc[0]


grid_point = grid_point.groupby(['id','geometry']).agg({ 'left':most_frequent,'right':most_frequent,'bottom':most_frequent,
                                        'SIG_KOR_NM':most_frequent,'EMD_NM':most_frequent,
                                        }).reset_index()

# GeoDataFrame으로 변환
grid_point = gpd.GeoDataFrame(grid_point, geometry='geometry')

# 서울 시 격자 위치 최신버전
output_path = r"C:\Users\pc021\Desktop\성장\공모전\QGIS\SHP\격자 위치\서울 시\고도화\서울시 위치_최신_5179_UTF8"

grid_point.to_file(output_path, driver='ESRI Shapefile',encoding='utf-8')


# In[2]:


def bring_in_data(file_path, data_type='standard'):
    """
    데이터 파일을 로드하는 함수.
    
    파라미터:
    - file_path (str): 파일의 경로.
    - data_type (str): 로드할 데이터의 유형 ('standard' 또는 'geo').
    
    반환:
    - 로드된 데이터프레임.
    """
    if data_type == 'geo':
        # 지리적 데이터 로드
        return gpd.read_file(file_path)
    else:
        # 표준 데이터 로드
        return pd.read_csv(file_path)  # CSV 파일을 예로 들었습니다. 필요에 따라 수정 가능합니다.

# 사용 예시
# standard_df = load_data('data/my_data.csv', 'standard')
# geo_df = load_data('data/my_geo_data.shp', 'geo')    


# In[3]:


# Action: 데이터 로드(관악구)

# 1. 격자 위치
grid_point = gpd.read_file(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\SHP\격자 위치\관악구\보행자도로 포함\관악구_그리드_보행자도로_5179_utf8.shp")

# 2. 격자 - 안전센터 거리
safety_center =  pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_안전센터\거리 데이터(관악구).csv")

# 3. 격자 - 안전 비상벨 거리
safety_emergency_bell = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_안전비상벨\거리 데이터(관악구).csv")

# 4. 격자 - 무더위 쉼터 거리
heat_shelter = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_무더위쉼터\격자(관악구)_무더위 쉼터\GRID(관악구)-SHELTER.csv")

# 격자 - 경사도
grid_gradient = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\경사도\관악구\경사도.csv")

# 격자 - 안심귀갓물 안전시설물
grid_safety_facilities = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_안심귀갓길 안전시설물\격자_안심귀갓길 안전시설물_5179_utf8.csv")

# 격자 - 안심이 CCTV
grid_safety_cctv = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_안심이 CCTV\격자_안심이 CCTV_5179_utf8.csv")


# In[ ]:


# Action: 데이터 로드(동작구)

# 1. 격자 위치
grid_point = gpd.read_file(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\SHP\격자 위치\동작구\동작구_그리드위치_5179_UTF8.shp")

# 2. 격자 - 안전센터 거리
safety_center =  pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_안전센터\동작구\동작구_안전센터_거리_5179_UTF8.csv")

# 3. 격자 - 안전 비상벨 거리
safety_emergency_bell = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_안전비상벨\동작구\동작구_안전비상벨_거리_5179_UTF8.csv")

# 4. 격자 - 무더위 쉼터 거리
heat_shelter = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_무더위쉼터\동작구\동작구_무더위쉼터_버퍼_5179_UTF8.csv")

# 격자 - 경사도
#grid_gradient = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\경사도\관악구\경사도.csv")

# 격자 - 안심귀갓물 안전시설물
grid_safety_facilities = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_안심귀갓길 안전시설물\동작구\동작구_안전시설물_버퍼_5179_UTF8.csv")

# 격자 - 안심이 CCTV
grid_safety_cctv = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_안심이 CCTV\동작구\동작구_CCTV_개수포함_5179_UTF8.csv",encoding='utf-8')


# In[33]:


# Action: 데이터 로드(서울시)

# 1. 격자 위치
#grid_point = gpd.read_file(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\SHP\격자 위치\서울 시\서울시_보행자도로(시군구 포함)_격자_5179_UTF8.shp")

# 2. 격자 - 안전센터 거리
#safety_center =  pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_안전센터\서울시\서울시_격자_안전센터_5179_UTF8b.csv")

# 3. 격자 - 안전 비상벨 거리
#safety_emergency_bell = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_안전비상벨\서울시\서울시_격자_안전비상벨_5179_UTF8.csv")

# 4. 격자 - 무더위 쉼터 거리
#heat_shelter = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_무더위쉼터\서울시\서울시_격자_무더위 쉼터_5179_UTF8.csv")

# 격자 - 경사도
#grid_gradient = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\경사도\관악구\경사도.csv")

# 격자 - 안심귀갓물 안전시설물 
#grid_safety_facilities = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_안심귀갓길 안전시설물\서울시\격자_안전시서물_5179_UTF8.csv")

# 격자 - 안심이 CCTV
grid_safety_cctv = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_안심이 CCTV\서울시\서울 시_격자_CCTV개수_5179_UTF8.csv")


# In[45]:


# Action: 데이터 로드(서울시 200 * 200)

# 1. 격자 위치
grid_point = gpd.read_file(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\SHP\격자 위치\서울 시\200_200\서울시_격자(시군구)_5179_UTF8.shp")

# 2. 격자 - 안전센터 거리
safety_center =  pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_안전센터\서울시\200_200\서울 시_격자_안전센터_5179_UTF8.csv")

# 3. 격자 - 안전 비상벨 거리
safety_emergency_bell = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_안전비상벨\서울시\200_200\서울시_격자_안전비상벨_5179_UTF8.csv")

# 4. 격자 - 무더위 쉼터 거리
heat_shelter = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_무더위쉼터\서울시\200_200\서울 시_격자_무더위쉼터_5179_UTF8.csv")

# 5. 격자 - 안심귀갓물 안전시설물
grid_safety_facilities = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_안심귀갓길 안전시설물\서울시\200_200\서울 시_격자_안전시설물_5179_UTF8.csv")

# 6. 격자 - 안심이 CCTV
grid_safety_cctv = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\격자_안심이 CCTV\서울시\200_200\서울 시_격자_CCTV개수_5179_UTF8.csv")


# In[98]:


# 

grid_point = gpd.read_file(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\SHP\격자 위치\서울 시\고도화\서울시 위치_5179_UTF8\서울시 위치_5179_UTF8.shp")

density =gpd.read_file(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\SHP\인구밀도\인구 밀도_그룹_5179_UTF8.shp")


# <span style= 'border:0.5px solid black; padding:5px; border-radius:5px;'> 격자 위치 - 자표 변경 </span>

# In[85]:


# Action: safety_center 좌표계 변환
def change_data_coordinates(data):
    
    # 1 shp 좌표계 변환
    data_shp = data.to_crs(epsg = 4326)

    # 2. point 생성
    point_shp = preprocess_point(data_shp,'geometry')
    
    return point_shp

grid_point = change_data_coordinates(grid_point)


# <span style= 'border:0.5px solid black; padding:5px; border-radius:5px;'> 데이터 정제 </span>

# In[27]:


# Action: 격자 데이터 정제

def preprocess_grid_point(data):

    # 1. 변수 선택
    grid_point_shp = data[['id','경도','위도','SIG_KOR_NM','EMD_NM']]

    # 2, 컬럼 변경
    grid_point_shp.columns = ['ID','LON','LAT','DISTRICT','DONG']
    
    # 3. 버전 입력
    grid_point_shp['VERSION'] = 200
    
    return grid_point_shp


# In[50]:


def preprocess_distance(data):
    data.columns = ['INPUT_ID','TARGET_ID','DISTANCE'] 
    
    data['VERSION'] = 200
    
    return data


# In[51]:


# Action: 데이터 정제

def preprocess_buffer_shelter(data):

    # 1. 변수 선택
    data = data[['id','mrb_dist']]

    # 2, 컬럼 변경
    data.columns = ['ID','GRID_SHELTER_DISTANCE_SCORE']
    
    # 3. 결측치 대체
    data['GRID_SHELTER_DISTANCE_SCORE'] = data['GRID_SHELTER_DISTANCE_SCORE'].fillna(300)
    
    data['VERSION'] = 200
    
    return data


# In[26]:


def preprocess_gradient(data):
    
    # 1.  변수 선택 
    data = data[['id','_sum']]
    
    # 2. 컬럼 변경
    data.columns = ['ID','GRADIENT']
    
    data['VERSION'] = 200
    
    return data


# In[53]:


# Action: 데이터 정제

def preprocess_buffer_facilities(data):

    # 1. 변수 선택
    data = data[['id','mrb_dist']]

    # 2, 컬럼 변경
    data.columns = ['ID','GRID_FACILITIES_DISTANCE_SCORE']
    
    # 3. 결측치 대체
    data['GRID_FACILITIES_DISTANCE_SCORE'] = data['GRID_FACILITIES_DISTANCE_SCORE'].fillna(300)
    
    data['VERSION'] = 200
    
    return data


# In[54]:


# Action: 데이터 정제

def preprocess_numpoint_cctv(data):

    # 1. 변수 선택
    data = data[['id','NUMPOINTS']]

    # 2, 컬럼 변경
    data.columns = ['ID','NUMBER_OF_CCTV']
    
    # 3. 시군구 할당
    #data['LOCATION'] = col
    
    # 4. 결측치 대체
    data['NUMBER_OF_CCTV'] = data['NUMBER_OF_CCTV'].fillna(300)
    
    data['VERSION'] = 200
    
    return data


# In[52]:


def preprocess_density(data):

     # 1. 변수 선택
    data = data[['id','val']]

    # 2, 컬럼 변경
    data.columns = ['ID','densify']
    
    # 3. 시군구 할당
    #data['LOCATION'] = col
    
    # 4. 결측치 대체
    #data['NUMBER_OF_CCTV'] = data['NUMBER_OF_CCTV'].fillna(300)
    
    data['VERSION'] = 200

    return data


# In[55]:


# Action: 정제 함수 사용

# 함수 사용
grid_point = preprocess_grid_point(grid_point)
safety_center = preprocess_distance(safety_center)
safety_emergency_bell = preprocess_distance(safety_emergency_bell)
heat_shelter = preprocess_buffer_shelter(heat_shelter)
#grid_gradient = preprocess_gradient(grid_gradient,'관악구')
grid_safety_facilities = preprocess_buffer_facilities(grid_safety_facilities)
grid_safety_cctv = preprocess_numpoint_cctv(grid_safety_cctv)


# In[86]:


grid_point = preprocess_grid_point(grid_point)
#density = preprocess_density(density)


# <span style= 'border:0.5px solid black; padding:5px; border-radius:5px;'> 데이터 적재 </span>

# In[66]:


# Action: 데이터 적재

load_database(safety_center,'an_distance_safety_center')
load_database(safety_emergency_bell,'an_distance_safety_emergency_bell')
load_database(heat_shelter,'an_distance_score_shelter')
load_database(grid_point,'an_grid_point')
#load_database(grid_gradient,'an_gird_gradiednt')
load_database(grid_safety_facilities,'an_distance_score_facilities')
load_database(grid_safety_cctv,'an_numpoins_cctv')


# In[91]:


# Action: 고도화 추가

load_database(grid_point,'an_grid_point')
load_database(grid_point,'an_density')


# In[102]:


output_path = r"C:\Users\pc021\Desktop\성장\공모전\QGIS\SHP\격자 위치\서울 시\고도화\서울시 위치_최신c_5179_UTF8"

grid_point.to_file(output_path, driver='ESRI Shapefile',encoding='utf-8')

