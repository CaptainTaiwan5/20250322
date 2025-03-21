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
        

magicape = Game("騎士",200)

print('job:',magicape.job,'life:',magicape.life,'skill:',skill[magicape.job])


