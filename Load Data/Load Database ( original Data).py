#!/usr/bin/env python
# coding: utf-8

# In[12]:


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
# * 데이터 정제
# * 데이터 로드

# <span style='border:0.5px solid blue; padding:5px; border-radius:5px; font-size:13.5px'> 서울 시 무더위 쉼터 </span>

# <span style='border:0.5px solid black; padding:5px; border-radius:5px;'> 데이터 로드 </span>

# In[22]:


# Action: 무더위 쉼터 데이터 로드

heat_shelter = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\서울 시 무더위쉼터\서울시 무더위쉼터.csv", encoding='cp949')


# In[23]:


heat_shelter = heat_shelter.reset_index()

heat_shelter = heat_shelter.rename({'index':'ID'}, axis=12)


# In[25]:


heat_shelter.to_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\서울 시 무더위쉼터\서울시 무더위쉼터(ID.csv", encoding='utf-8')


# <span style='border:0.5px solid black; padding:5px; border-radius:5px;'> 데이터 정제 </span>

# In[ ]:


# Action: 무더위 쉼터 데이터 정제

# 변수 선택
heat_shelter = heat_shelter[['쉼터명칭','도로명주소','위도','경도']]


# <span style='border:0.5px solid blue; padding:5px; border-radius:5px; font-size:13.5px'> 서울 시 안전센터 </span>

# <span style='border:0.5px solid black; padding:5px; border-radius:5px;'> 데이터 로드 </span>

# In[ ]:


# 11. safety_center 좌표계 변환

# 11.1 shp 좌표계 변환
safety_center_shp = safety_center_shp.to_crs(epsg = 4326)

# 11.2 point 생성
safety_center_shp = preprocess_point(safety_center_shp,'geometry')


# In[ ]:


# Action: 안전센터 데이터 로드

#safety_center = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\서울시 소방서,안전센터,구조대 위치정보.csv", encoding='cp949')

# safety_center_shp
#safety_center_shp = gpd.read_file(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\SHP\안전센터, 소방서 위치\서울 시 안전센터, 소방서, 구조대 위치.shp", encoding='euc_kr')


# <span style='border:0.5px solid black; padding:5px; border-radius:5px;'> 데이터 정제 </span>

# In[ ]:


# 10. safety_center 좌표계 변환

# 좌표 설정
emergency_bell_geo = emergency_bell_geo.set_crs(epsg=5178, inplace=False)

# 10.1 shp 좌표계 변환
emergency_bell_geo = emergency_bell_geo.to_crs(epsg = 4326)

# 10.2 point 생성
emergency_bell_geo = preprocess_point(emergency_bell_geo,'geometry')


# In[ ]:


# Action: 안전센터

# 1, 변수 선택
safety_center = safety_center_shp[['연번','서ㆍ센터명','유형구분명','경도','위도']]

# 2, 변수 명칭 변경
safety_center.columns = ['ID','CENTER_NAME','TYPE','LON','LAT']


# <span style='border:0.5px solid blue; padding:5px; border-radius:5px; font-size:13.5px'> 서울 시 안전비상벨 </span>

# <span style='border:0.5px solid black; padding:5px; border-radius:5px;'> 데이터 로드 </span>

# In[ ]:


# Action: 안전비상벨 데이터 로드

#emergency_bell_geo = gpd.read_file(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\SHP\안전비상벨 위치\서울특별시_안전비상벨위치_20220316_UTMK.shp", encoding='cp949')


# <span style='border:0.5px solid black; padding:5px; border-radius:5px;'> 데이터 정제 </span>

# In[ ]:


# Action: 안전 비상벨 좌표계 변환

# 1. 좌표 설정
emergency_bell_geo = emergency_bell_geo.set_crs(epsg=5178, inplace=False)

# 2. shp 좌표계 변환
emergency_bell_geo = emergency_bell_geo.to_crs(epsg = 4326)

# 3. point 생성
emergency_bell_geo = preprocess_point(emergency_bell_geo,'geometry')


# In[11]:


# Action: 안전 비상벨 데이터 정제 

# 1 변수 선택
emergency_bell = emergency_bell_geo[['설치위치','소재지지번','부가기능','경도','위도']]

# 2 변수 명칭 변경
emergency_bell.columns = ['INSTALLATION_LOCATION','ADDRESS','FUNTION','LON','LAT']


# <span style='border:0.5px solid blue; padding:5px; border-radius:5px; font-size:13.5px'> 서울 시 안전시설물 </span>

# <span style='border:0.5px solid black; padding:5px; border-radius:5px;'> 데이터 로드 </span>

# In[ ]:


# Action: 안전 시설물 데이터 로드

#safety_facilities = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\안심귀갓길 안전시설물\서울시 안심귀갓길 안전시설물(전처리).csv",encoding='cp949')


# <span style='border:0.5px solid black; padding:5px; border-radius:5px;'> 데이터 정제 </span>

# In[ ]:


# Action: 안전 시설물 데이터 정제

# 1 변수 선택
safety_facilities = safety_facilities[['시군구명','읍면동명','안심귀갓길 명','설치대수','경도','위도','시설명']]

# 2 변수 명칭 변경
safety_facilities.columns = ['CITY','DONG','ROAD_NAME','NUMBER','LON','LAT','FACILITY_NAME']


# <span style='border:0.5px solid blue; padding:5px; border-radius:5px; font-size:13.5px'> 서울 시 CCTV </span>

# <span style='border:0.5px solid black; padding:5px; border-radius:5px;'> 데이터 로드 </span>

# In[10]:


# Action: CCTV 데이터 로드
#cctv = pd.read_csv(r"C:\Users\pc021\Desktop\성장\공모전\QGIS\CSV\서울시 안심이 CCTV\서울시 안심이 CCTV 연계 현황.csv", encoding='cp949')


# <span style='border:0.5px solid black; padding:5px; border-radius:5px;'> 데이터 정제 </span>

# In[ ]:


# Action: CCTV 데이터 정제

# 1. 변수 선택
cctv = cctv[['자치구','안심 주소','CCTV 수량','경도','위도']]

# 2. 변수 명칭 변경
cctv.columns = ['AUTONOMOUS_REGION','ADDRESS','NUMBER','LON','LAT']


# In[6]:


# 데이터 적재

#load_database(heat_shelter,'an_heat_shelter')
#load_database(safety_center,'an_safety_center')
#load_database(cctv,'an_cctv')
#load_database(emergency_bell,'an_safety_emergency_bell')
#load_database(safety_facilities,'an_safety_facilities') 

