current_number = 0
def decide_action(wood_flag, detected_number, glass_detected, lantern_detected,direction):
    global current_number
    steps = 1  
    if wood_flag == -1:  
        direction = "right"
    elif wood_flag == 1: 
        direction = "left"
    
    if detected_number > 0 and current_number == 0:  #  رقم جديد
        current_number = detected_number

    if current_number > 0:  
        current_number -= 1
        steps += detected_number 
        direction = "right" if wood_flag == -1 else "left"

    if current_number <= 0:
        current_number = 0    

    if glass_detected:  
        direction = "right" if wood_flag == -1 else "left"
        steps +=1   

    if lantern_detected == 1 : 
        direction = "right"
        
    elif lantern_detected == -1 :
        direction = "left"

    return direction, steps
