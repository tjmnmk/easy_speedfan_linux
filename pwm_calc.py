"""
Fuctions to calculate the PWM Value based on the temperature
"""

def linear_pwm(temp, min_temp, max_temp, min_pwm, max_pwm, step = 1):
    """
    Calculate the PWM value based on the temperature using a linear function
    """
    if temp < min_temp:
        return min_pwm
    elif temp > max_temp:
        return max_pwm
    else:
        c = int(min_pwm + (max_pwm - min_pwm) * (temp - min_temp) / (max_temp - min_temp))
        return steps(c, min_pwm, max_pwm, step)

def quadratic_pwm(temp, min_temp, max_temp, min_pwm, max_pwm, step = 1):
    """
    Calculate the PWM value based on the temperature using a quadratic function
    """
    if temp < min_temp:
        return min_pwm
    elif temp > max_temp:
        return max_pwm
    else:
        c = int(min_pwm + (max_pwm - min_pwm) * ((temp - min_temp) / (max_temp - min_temp)) ** 2)
        return steps(c, min_pwm, max_pwm, 1)
    
def cubic_pwm(temp, min_temp, max_temp, min_pwm, max_pwm):
    """
    Calculate the PWM value based on the temperature using a cubic function
    """
    if temp < min_temp:
        return min_pwm
    elif temp > max_temp:
        return max_pwm
    else:
        c = int(min_pwm + (max_pwm - min_pwm) * ((temp - min_temp) / (max_temp - min_temp)) ** 3)
        return steps(c, min_pwm, max_pwm, 1)
    
def exponential_pwm(temp, min_temp, max_temp, min_pwm, max_pwm):
    """
    Calculate the PWM value based on the temperature using an exponential function
    """
    if temp < min_temp:
        return min_pwm
    elif temp > max_temp:
        return max_pwm
    else:
        c = int(min_pwm + (max_pwm - min_pwm) * (1 - (max_temp - temp) / (max_temp - min_temp)) ** 2)
        return steps(c, min_pwm, max_pwm, 1)
    
def steps(pwm, min_pwm, max_pwm, step):
    if pwm in (min_pwm, max_pwm) or step in (0, 1):
        return pwm
    
    calc = int(pwm / step) * step + step
    if calc < min_pwm:
        return min_pwm
    elif calc > max_pwm:
        return max_pwm
    else:
        return calc
    
def smooth_pwm(previous_pwm, current_pwm, step = 1, burst_diff = 20):
    """
    Smooth the PWM value based on the previous PWM value
    """
    if abs(current_pwm - previous_pwm) > burst_diff:
        return current_pwm
    
    if current_pwm > previous_pwm:
        return previous_pwm + step
    elif current_pwm < previous_pwm:
        return previous_pwm - step
    
    return current_pwm
        