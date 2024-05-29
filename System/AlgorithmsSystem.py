#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 20 years old


# In[29]:


# Handling
import sys
import os

# System 
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, StringVar

# Visualize
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import font_manager, rc
from matplotlib.ticker import FuncFormatter

# Moduel
from Algorithms_system import *


# In[26]:


def search_concordance():
    
    # 입력된 텍스트 가져오기
    departure = concordance_entry.get()
    departure = concordance_entry.get()
    
    find_best_route()
    
    
    # 검색 결과를 저장할 리스트
    results = []
    
    # 검색 로직: 예시 데이터셋에서 단어 검색
    for word in word_list:
        for key, sentences in data.items():
            for sentence in sentences:
                if word in sentence:
                    results.append((key, sentence))
    
    
    
    
    
    
    
    # 결과 텍스트 업데이트
    result_text.delete('12.0', tk.END)  # 기존 결과 지우기
    result_text.insert(tk.END, '\n'.join(f"{k}: {s}" for k, s in results))  # 새 결과 추가

# GUI 설정
root = tk.Tk()
root.title("순찰 경로 시스템")
root.geometry("800x800")


# 콘코던스 단어 레이블 및 입력 필드
departure_label = tk.Label(root, text="출발지", anchor='w')
departure_label.grid(row=0, column=0, sticky='we', padx=10, pady=5)

destination_label = tk.Label(root, text="도착지", anchor='w')
destination_label.grid(row=1, column=0, sticky='we', padx=10, pady=5)

departure_entry = ttk.Entry(root)
departure_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=5)

destination_entry = ttk.Entry(root)
destination_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=5)

# 검색 버튼
search_button = ttk.Button(root, text="검색", command=search_concordance)
search_button.grid(row=2, column=0, columnspan=2, pady=10)

# 결과 출력
result_text = tk.Text(root, height=30)
result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky='ew')

root.mainloop()

