# Handling
import pandas as pd
import requests 
import heapq
import warnings
import time
import dill as pickle
import sys

# Math
from math import radians, cos, sin, asin, sqrt

# Visualize
import matplotlib.pyplot as plt

# Warings
warnings.filterwarnings('ignore')

# Moduel
from select_dataset import *
from calculateRiskIndex import *
from load_database import *

import pandas as pd
from sklearn.neighbors import KDTree
import numpy as np


def load_nodes(df):
    """
    데이터프레임으로부터 그래프를 생성합니다. radius는 이웃을 결정하기 위한 반경(km)입니다.
    """
    node_bowl = []
    
    for index, row in df.iterrows():
        
        # 1.각 격자의 노드 생성 
        # 비용 함수,휴리스틱 디폴트 값 설정        
        node_dict={'ID':row['ID'],'LAT':row['LAT'],'LON':row['LON'],'RANK':row['RANK'],'G':sys.maxsize, 'F':sys.maxsize}
        node_bowl.append(node_dict)
        
    node = pd.DataFrame(node_bowl)
    
    #2. 격자 노드 적재
    load_database(node,'nodes')


def create_graph(df, radius=0.40):
    # 좌표를 radians로 변환 (KDTree는 이를 요구함)
    coords = np.radians(df[['LAT', 'LON']].values)

    # KDTree 생성
    tree = KDTree(coords)

    # 반경 내의 모든 이웃 찾기
    indices = tree.query_radius(coords, r=radius/6371., count_only=False)  # 6371km는 지구의 반경

    # 결과를 저장할 리스트
    neighbor_bowl = []
    
    # 이웃을 데이터프레임으로 변환
    for idx, neighbors in enumerate(indices):
        current_grid = df.iloc[idx]['ID']
        for neighbor in neighbors:
            if idx != neighbor:  # 자기 자신을 제외
                neighbor_dict = {'ID': current_grid, 'NEIGHBOR_ID': df.iloc[neighbor]['ID']}
                neighbor_bowl.append(neighbor_dict)
                
    neighbor_node = pd.DataFrame(neighbor_bowl)

    load_database(neighbor_node,'neighbors')

