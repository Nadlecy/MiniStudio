import time

class PowerUp:
    def __init__(self, duration:float,player):
        self.duration = duration
        self.begin_time = time.time()
        self.player = player
        
    def isOver(self):
        if (time.time() - self.begin_time) >= self.duration:
            self.clean()
            return True
        return False
    
    def effect(self,dt):
        pass

    def clean(self):
        pass
        
class ASPBoost(PowerUp):
    def __init__(self, duration:float, player):
        super().__init__(self,duration)
        self.duration = duration
        self.player = player
        self.player.shotCoolDown -= 5
        self.player.shotSpeed += 1
        
    def effect(self,dt):
        super().effect(dt)

    def clean(self):
        super().clean()
        self.player.shotCoolDown += 5
        self.player.shotSpeed -= 1

class Shield(PowerUp):
    def __init__(self,duration:float,player):
        super().__init__(self,duration)
        self.duration = duration
        self.player = player
        self.player.shield = True

    def effect(self,dt):
        super().effect(dt)

    def clean(self):
        super().clean()
        self.player.shield = False

class Heal(PowerUp):
    def __init__(self,player,duration):
        super().__init__(self,duration)
        self.duration = duration
        self.player = player
        self.player.lives += 1

    def effect(self,dt):
        super().effect(dt)
    
    def clean(self):
        super().clean()

class Laser(PowerUp):
    def __init__(self,player,duration):
        super().__init__(self,duration)
        self.duration = duration
        self.player = player
        self.player.laser = True

    def effect(self,dt):
        super().effect(dt)
    
    def clean(self):
        super().clean()
        self.player.laser = False