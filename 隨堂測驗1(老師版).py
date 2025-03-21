class GameCharacter:
    def __init__(self, title, job, mana, skill):
        self.title = title
        self.job = job
        self.mana = mana
        self.skill = skill
        

magicape = GameCharacter("王國最強的",
                          "魔法師",
                          999,
                          ["火焰風暴","急凍光線","十萬伏特"]
                          )


print(magicape.title,magicape.job,"魔力值:",magicape.mana)
print("魔法技能:",magicape.skill[0],magicape.skill[1])


