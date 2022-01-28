#!/usr/bin/env python
# coding: utf-8

# In[1]:


def delzero(df):
    df_new = df.copy()
    df_new = df_new.dropna(how='any')

    col_list = []
    for i in df_new.columns :
        col_list.append(i)

    for i in col_list :
        df_new = df_new[df_new[i] != 0]

    return df_new

