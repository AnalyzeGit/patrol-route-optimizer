#!/usr/bin/env python
# coding: utf-8

# In[79]:


# Handling
import numpy as np
import json

# Moduel 
from selectDatasetFluid import *


# In[40]:


def extract_optimized_path_data(optimal_path):
    # 1 데이터 프레임 리스트 
    dataframes = []
    
    # 2. 서울 시 격자 순위 데이터 로드
    data = get_dataframe_from_database_fluid('an_rank')
    
    # 3. 리스트 컴프리헨션을 이용한 ID 추출
    ids_only = [item[2] for item in optimal_path]
    
    # 4. 반복문을 이용한 KEY 데이터 프레임 추출
    for key in ids_only:
        
        # 4.1 최적 경로 격자 데이터 추출
        selected_data = data[data['ID']==key]
        
        # 4.2 선택된 격자 데이터 리스트 추가
        dataframes.append(selected_data)
    
    
    # 5. 데이터 프레임화 시행   
    concat = pd.concat(dataframes)
    
    # 6.중복 제거
    check_columns=['LON','LAT']
    concat = concat.drop_duplicates(subset=check_columns)
    
    return concat,data


# In[41]:


def calculate_risk_scoresa(optimal_path):
        
        # 1. 함수 활용하여 특정 데이터 및 rank 데이터 추출
        data = extract_optimized_path_data(optimal_path)
                    
        # 2. 각 변수 범위 추출
        rank_range =  rank_data['RANK'].max() - rank_data['RANK'].min()
        emergency_bell_and_distance_range = rank_data['EMERGENCY_BELL_AND_DISTANCE'].max() - rank_data['EMERGENCY_BELL_AND_DISTANCE'].min() 
        safety_center_and_distance_range = rank_data['SAFETY_CENTER_AND_DISTANCE'].max() - rank_data['SAFETY_CENTER_AND_DISTANCE'].min()
        shelter_and_distance_score_range = rank_data['GRID_SHELTER_DISTANCE_SCORE'].max() - rank_data['GRID_SHELTER_DISTANCE_SCORE'].min() 
        facility_and_distance_score_range = rank_data['GRID_FACILITIES_DISTANCE_SCORE'].max() - rank_data['GRID_FACILITIES_DISTANCE_SCORE'].min()
        number_of_cctv_range = rank_data['NUMBER_OF_CCTV'].max() - rank_data['NUMBER_OF_CCTV'].min()
        
        # 3. 일정 비율 이상의 격자 추출
        high_ranking_data  = data.sort_values(by='RANK') # 3.1 순서 정리
        threshold = high_ranking_data['RANK'].quantile(0.15) # 3.2 RANK 열의 값에서 하위 15%에 해당하는 임계값 계산
        high_ranking_data = high_ranking_data[high_ranking_data['RANK'] <= threshold] # 3.3 RANK 값이 임계값 이하인 행들만 선택
        
        # 4. 특정 데이터셋 변수 추출
        rank = high_ranking_data['RANK']
        emergency_bell_and_distance = high_ranking_data['EMERGENCY_BELL_AND_DISTANCE']
        safety_center_and_distance = high_ranking_data['SAFETY_CENTER_AND_DISTANCE']
        shelter_and_distance_score = high_ranking_data['GRID_SHELTER_DISTANCE_SCORE']
        facility_and_distance_score = high_ranking_data['GRID_FACILITIES_DISTANCE_SCORE']
        number_of_cctv = high_ranking_data['NUMBER_OF_CCTV']
        
        #  5. 위험지수 추출
        high_ranking_data['RANK_SCORE'] = 100 - (np.round(((rank - rank_data['RANK'].min())/ rank_range * 100),2)) 
        high_ranking_data['EMERGENCY_BELL_AND_DISTANCE_SCORE'] = np.round(((emergency_bell_and_distance - rank_data['EMERGENCY_BELL_AND_DISTANCE'].min()) / emergency_bell_and_distance_range*100),2)
        high_ranking_data['SAFETY_CENTER_AND_DISTANCE_SCORE'] = np.round(((safety_center_and_distance - rank_data['SAFETY_CENTER_AND_DISTANCE'].min()) / safety_center_and_distance_range * 100),2)
        high_ranking_data['GRID_SHELTER_DISTANCE_SCORE_SCORE'] = np.round(((shelter_and_distance_score - rank_data['GRID_SHELTER_DISTANCE_SCORE'].min()) / shelter_and_distance_score_range *100),2)
        high_ranking_data['GRID_FACILITIES_DISTANCE_SCORE_SCORE']  = np.round(((facility_and_distance_score - rank_data['GRID_FACILITIES_DISTANCE_SCORE'].min()) / facility_and_distance_score_range *100),2)
        high_ranking_data['NUMBER_OF_CCTV_SCORE'] =  np.round(((number_of_cctv - rank_data['NUMBER_OF_CCTV'].min()) / number_of_cctv_range *100),2)
        
        high_ranking_data = high_ranking_data[['ID','RANK_SCORE','EMERGENCY_BELL_AND_DISTANCE_SCORE','SAFETY_CENTER_AND_DISTANCE_SCORE',
                         'GRID_SHELTER_DISTANCE_SCORE_SCORE','GRID_FACILITIES_DISTANCE_SCORE_SCORE','NUMBER_OF_CCTV_SCORE']]
        
        return high_ranking_data


# In[112]:


def calculate_risk_scores(optimal_path):
    """
    주어진 경로 데이터를 바탕으로 안전 관련 변수들에 대한 위험 점수를 계산합니다.
    위험도 점수는 데이터의 상대적인 안전도를 나타내는 정규화된 점수로 계산됩니다.
    
    Parameters:
    optimal_path (str): 분석할 최적 경로 데이터의 경로 또는 식별자입니다.
    
    Returns:
    DataFrame: 계산된 위험도 점수가 포함된 데이터프레임을 반환합니다.
    """
    
    try:
        # 데이터 추출
        data, rank_data = extract_optimized_path_data(optimal_path)
        
        # 데이터 유효성 검증
        required_columns = ['RANK','EMERGENCY_BELL_AND_DISTANCE', 'SAFETY_CENTER_AND_DISTANCE', 
                            'GRID_SHELTER_DISTANCE_SCORE', 'GRID_FACILITIES_DISTANCE_SCORE', 'NUMBER_OF_CCTV']
        if not all(column in rank_data.columns for column in required_columns):
            raise ValueError("입력 데이터가 필요한 컬럼을 모두 포함하고 있지 않습니다.")
        
        # 변수 범위 계산
        def calculate_range(column):
            return rank_data[column].max() - rank_data[column].min()
        
        ranges = {column: calculate_range(column) for column in required_columns}
        
        
        
        sorted_rank = data[1:-1].sort_values(by='RANK',ascending=False)[-5:].sort_values(by='RANK')
        
        departure = data.iloc[[0]]
        arrival = data.iloc[[-1]]
        
        # 출발지, 데이터 프레임, 도착지를 결합
        high_ranking_data = pd.concat([departure, sorted_rank , arrival])
        
        # 위험도 점수 계산
        for column in required_columns:
            if ranges[column] == 0:  # 분모가 0인 경우 방지
                high_ranking_data[f'{column}_SCORE'] = 100
            else:
                high_ranking_data[f'{column}_SCORE'] = ((high_ranking_data[column] - rank_data[column].min()) / ranges[column] * 100
                ).round(2)
        
        # Rank Score 정제
        high_ranking_data['RANK_SCORE'] = (100 - high_ranking_data['RANK_SCORE'])
        
        # 필요한 컬럼만 선택
        score_columns = [f'{column}_SCORE' for column in required_columns]
        result_data = high_ranking_data[['ID','LON','LAT'] + score_columns]
        
        return result_data
    
    except Exception as e:
        print(f"에러 발생: {e}")
        return pd.DataFrame()  # 에러 시 빈 데이터프레임 반환


# In[110]:


def throw_tuple_price(data):
    
    # 각 행을 튜플로 변환하여 리스트에 추가
    tuples_list = [tuple(row) for row in data.itertuples(index=False, name=None)]
    
    return tuples_list


# In[121]:


def convert_jason(data_tuples):

    # 튜플의 각 요소에 대한 키 목록
    keys = ['id', 'longitude', 'latitude', 'rank_score', 'emergency_bell_and_distance_score', 'safety_center_and_distacne_score',
            'grid_shelter_distance_score', 'grid_facilities_distance_score', 'number_of_cctv_score']

    # 튜플 데이터를 JSON 객체로 변환
    json_data = [dict(zip(keys, tuple_data)) for tuple_data in data_tuples]
    
    return json_data

def calculate_group_mean(data):
    
    slice_data = data.iloc[1:-1]
    
    # 각 변수의 평균 
    required_columns=['RANK_SCORE','EMERGENCY_BELL_AND_DISTANCE_SCORE','SAFETY_CENTER_AND_DISTANCE_SCORE',
                      'GRID_SHELTER_DISTANCE_SCORE_SCORE','GRID_FACILITIES_DISTANCE_SCORE_SCORE','NUMBER_OF_CCTV_SCORE']
    
    mean_bowl = [slice_data[col].mean() for col in required_columns]
    
    # 튜플의 각 요소에 대한 키 목록
    keys =  ['rank_score_mean', 'emergency_bell_and_distance_score_mean', 'safety_center_and_distacne_score_mean',
            'grid_shelter_distance_score_mean', 'grid_facilities_distance_score_mean', 'number_of_cctv_score_mean']
    
    # 튜플 데이터를 JSON 객체로 변환
    json_mean_data = [dict(zip(keys, mean_bowl))]
    
    return json_mean_data

def combine_dictionaries(dica,dicb):
    # 현재 딕셔너리에 평균 딕셔너리 추가
    dica.append(dicb)
    
    return dica
