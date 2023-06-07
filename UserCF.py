# coding: utf-8 -*-
import math
import pandas as pd
from sqlalchemy import create_engine


engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/graduation_thesis?charset=utf8")


class UserCf:
    # 这个类的主要功能是提供一个基于用户的协调过滤算法接口

    def __init__(self):
        self.sql = 'select * from ratings'
        self._init_frame()

    def _init_frame(self):
        self.frame = pd.read_sql_query(self.sql, engine)
        self.frame.columns = ['rID', 'uID', 'mID', 'rating']  # 数据预处理，读出评分表并转换为DataFrame格式存入self.frame

    @staticmethod
    def _cosine_sim(target_meals, meals):
        union_len = len(set(target_meals) & set(meals))
        if union_len == 0: return 0.0
        product = len(target_meals) * len(meals)
        cosine = union_len / math.sqrt(product)
        return cosine

    # 得到最相似的top_n个用户
    def _get_top_n_users(self, target_user_id, top_n):
        target_meals = self.frame[self.frame['uID'] == target_user_id]['mID']
        other_users_id = [i for i in set(self.frame['uID']) if i != target_user_id]
        other_meals = [self.frame[self.frame['uID'] == i]['mID'] for i in other_users_id]

        sim_list = [self._cosine_sim(target_meals, meals) for meals in other_meals]
        sim_list = sorted(zip(other_users_id, sim_list), key=lambda x: x[1], reverse=True)
        return sim_list[:top_n]

    # 得到目标用户没有评价过的餐品
    def _get_candidates_items(self, target_user_id):
        target_user_meals = set(self.frame[self.frame['uID'] == target_user_id]['mID'])
        other_user_meals = set(self.frame[self.frame['uID'] != target_user_id]['mID'])
        candidates_meals = list(target_user_meals ^ other_user_meals)
        return candidates_meals

    # interest = sum(sim * normalize_rating)
    def _get_top_n_items(self, top_n_users, candidates_meals, top_n):
        top_n_user_data = [self.frame[self.frame['uID'] == k] for k, _ in top_n_users]
        interest_list = []
        for meal_id in candidates_meals:
            tmp = []
            for user_data in top_n_user_data:
                if meal_id in user_data['mID'].values:
                    choosedf = user_data[user_data['mID'] == meal_id]
                    tmp.append(round(choosedf['rating'].mean(), 2))
                else:
                    tmp.append(0)
            interest = sum([top_n_users[i][1] * tmp[i] for i in range(len(top_n_users))])
            interest_list.append((meal_id, interest))
        interest_list = sorted(interest_list, key=lambda x: x[1], reverse=True)
        return interest_list[:top_n]

    def calculate(self, target_user_id, top_n):
        # 最相似的top_n个用户
        top_n_users = self._get_top_n_users(target_user_id, top_n)
        # 备选餐品
        candidates_meals = self._get_candidates_items(target_user_id)
        # 匹配度最高的top_n个餐品
        top_n_meals = self._get_top_n_items(top_n_users, candidates_meals, top_n)

        name = []
        values = []
        for x in top_n_meals:
            name.append(x[0])
            values.append(x[1])
        df = pd.DataFrame({'uID': target_user_id, 'mID': name, 'score': values})
        return df


def run(i):
    global res
    target_user_id = i
    DF = usercf.calculate(target_user_id, top_n)
    ans = pd.concat([res, DF], ignore_index=True)
    return ans


res = pd.DataFrame(columns=['uID', 'mID', 'score'])
usercf = UserCf()
top_n = 6
