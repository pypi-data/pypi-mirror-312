import numpy as np
from scipy.optimize import fsolve

def equation(EI):
    left_side = 2 * (0.0331456303681194 * EI - 18.5615530061469)
    right_side = -0.25689 * (0.00621480569402239 * EI**2 + 17.5251242829788 * EI + 974.481532822711)
    return left_side - right_side  # 必须使这个返回值为零

# 初始猜测值
initial_guess = 100  # 选择一个合理的初始值

# 求解EI
solution = fsolve(equation, initial_guess)

print(f'Solution for EI: {solution[0]}')
