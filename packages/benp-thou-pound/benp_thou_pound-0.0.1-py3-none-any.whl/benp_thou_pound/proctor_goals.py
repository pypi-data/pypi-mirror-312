#############################################################################
# inputs:
#   weight:
#   loss_goal:
#   time_goals:
# outputs:
#   daily_loss_rate:
#   weekly_loss_rate:
#   monthly_loss_rate:
#############################################################################
import math


class bariatric_candidate:

    def __init__(self,start_weight:float,current_weight:float=None,loss_goal:float = 0,time_goal:int=0,surgery:bool=False):
        self.start_weigth = start_weight
        self.loss_goal = loss_goal
        self.time_goal = time_goal
        self.surgery = surgery
        if current_weight == None:
            current_weight = start_weight

    def set_current_weight(self,new_current_weight:float):
        self.current_weight = new_current_weight

    def set_new_goal(self,new_loss_goal:float,new_time_goal:int):
        self.loss_goal = new_loss_goal
        self.time_goal = new_time_goal

    def get_daily_rate(self,exponential=False) -> float:
        if exponential:
            goal_weight = self.current_weight - self.loss_goal
            return math.log(goal_weight/self.current_weight)/self.time_goal
        return self.loss_goal/self.time_goal

    def get_weekly_rate(self,exponential=False) -> float:
        if exponential:
            goal_weight = self.current_weight - self.loss_goal
            return math.log(goal_weight/self.current_weight)/(self.time_goal/7)
        return self.loss_goal/(self.time_goal/7)
    
    def get_monthly_rate(self,exponential=False) -> float:
        if exponential:
            goal_weight = self.current_weight - self.loss_goal
            return math.log(goal_weight/self.current_weight)/(self.time_goal/30.5)
        return self.loss_goal/(self.time_goal/30.5)
    
    def get_percent_weight_to_lost(self):
        return (self.current_weight - self.loss_goal) * 100
    
    def get_percent_weight_diff(self,weight):
        return (weight/self.current_weight)*100