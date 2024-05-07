#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sqlalchemy import create_engine
import pandas as pd

def get_dataframe_from_database_fluid(table_name,col=None):
    # 테이블 정보 설정
    
    # 연결 정보 설정
    username = 'admin'  # 사용자 이름
    password = 'seoul1234!'  # 비밀번호
    host = 'seoul-rds.cteyic8ukah5.ap-northeast-2.rds.amazonaws.com'  # 서버 주소
    port = 3306  # 포트
    #port = 16002  # 포트
    database = 'myappDB'  # 데이터베이스 이름
    connect_timeout = 7200
    #engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}?connect_timeout={connect_timeout}')
    # SQLAlchemy 엔진 생성
    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}',
                          connect_args={"connect_timeout": connect_timeout, "read_timeout": 7200, "write_timeout": 7200}, pool_size=10, max_overflow=20, pool_pre_ping=True)
    
    
    # SQL 쿼리
    # 쿼리 동적 구성
    # 데이터베이스 세션 설정 변경
    with engine.connect() as connection:
        connection.execute("SET @@session.wait_timeout = 7200")  # wait_timeout 세션 값 설정
        connection.execute("SET @@session.interactive_timeout = 7200")  # interactive_timeout 세션 값 설정
    
        base_query = f"SELECT * FROM `{table_name}`"
        
        if col:
            # col 값이 있을 경우 WHERE 조건을 추가합니다.
            query = f"SELECT * FROM `{table_name}` WHERE `LOCATION` = '{col}'"
    
        else:
            # col 값이 없을 경우 WHERE 조건 없이 기본 쿼리를 반환합니다.
            query =  base_query
            
        # Pandas를 사용하여 데이터 프레임으로 로드
        df = pd.read_sql(query, engine)

    
    return df

