# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 15:53:59 2022

@author: CodingApe_User
"""

global skill

skill = {'魔法師':['冰矛','火球'],
         '騎士':['盾衝','旋風斬'],
         '獵人':['火箭矢','二連矢'],
         '祭司':['治癒術','神聖之光']}

class Game:
    
    def __init__(self,job,life):
        self.job = job
        self.life = life
        

knightape = Game("騎士",200)

print('job:',knightape.job,'life:',knightape.life,'skill:',skill[knightape.job])

skill['騎士'].append('霹靂一閃')

print('騎士現在持有的技能:',skill['騎士'])

