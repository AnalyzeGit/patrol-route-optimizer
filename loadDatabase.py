#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
import io

def load_database(data,table_name):

    # MariaDB 연결을 설정합니다.
    # 'username', 'password', 'host', 'port', 'database'를 실제 값으로 대체하세요.
    username = 'admin'
    password = 'seoul1234!'
    host = 'seoul-rds.cteyic8ukah5.ap-northeast-2.rds.amazonaws.com'  # 또는 서버의 IP 주소
    port = 3306  # MariaDB의 기본 포트
    database = 'myappDB'
    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}',
    pool_size=10,  # 연결 풀 내 연결의 수
    max_overflow=5,  # 풀 크기 이상으로 생성할 수 있는 연결 수
    pool_timeout=30,  # 풀에서 연결을 기다리는 최대 시간(초)
    pool_recycle=1800)  # 연결 재사용 타임아웃(초))

    # 데이터 프레임을 MariaDB에 적재합니다.
    # 'your_table_name'을 실제 테이블 이름으로 대체하세요.

    try:
        # DataFrame 'data'가 비어있는지 확인
        if not data.empty:
            data.to_sql(table_name, con=engine, if_exists='append', index=False)
            print(f'DataFrame has been successfully loaded into {table_name} table in {database} database.')
        else:
            # 빈 데이터 프레임인 경우
            print("The DataFrame is empty. No data was loaded into the table.")
            
    except Exception as e:
        if "Too many connections" in str(e):
            print("Too many connections. Waiting before retrying...")
            time.sleep(60)  # 60초 대기
            try:
                data.to_sql(table_name, con=engine, if_exists='append', index=False)
                print(f"Retry successful: DataFrame has been loaded into {table_name}.")
            except Exception as e:
                print(f"Failed to load data after retry: {e}")
        else:
            print(f"Failed to load data: {e}")

