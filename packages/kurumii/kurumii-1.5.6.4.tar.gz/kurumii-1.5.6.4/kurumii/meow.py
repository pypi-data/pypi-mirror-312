from typing import Union
import math
def loadingbar (current_value:Union[int,float], bar_amount:int=40, total_value:Union[int,float]=100, no_overflow:bool = True, bar_done:str = "=", bar_missig:str = "-",current_bar:str = ">", colored:bool=True):
    if no_overflow:
        if current_value > total_value:
            current_value = total_value
        if current_value < 0:
            current_value = 0
    amount_of_bars = math.floor(bar_amount/total_value*current_value)
    done = bar_done
    not_dont = bar_missig
    missing_bars = bar_amount - amount_of_bars
    string = f"[{"\033[92m"if colored else ""}{done*(amount_of_bars-1)}{"\033[0m\033[38;2;255;255;0m" if colored else ""}{current_bar}{"\033[91m" if colored else ""}{not_dont*missing_bars}{"\033[0m]"if colored else ""}"
    next_string = f"{string}({round((current_value / total_value) * 100,2)}%)" 
    return(next_string)
i = 0
while i < 64:
    print(loadingbar(bar_amount=37,current_value = i,total_value=63, bar_done = ":3 ", bar_missig = ":( " ,current_bar="Meow "))
    i = i + 1