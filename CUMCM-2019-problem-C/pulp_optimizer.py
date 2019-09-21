from pulp import *

prob = LpProblem("problem1", LpMaximize)
x1 = LpVariable("x1", 0, None, LpContinuous)
x2 = LpVariable("x2", 0, None, LpContinuous)
prob += 40 * x1 + 90 * x2
prob += 9 * x1 + 7 * x2 <= 56
prob += 7 * x1 + 20 * x2 <= 70
prob += x1 + 0 * x2 <= 4
prob += 0 * x1 + x2 <= 2
prob.writeLP("problem1.lp")
prob.solve()
print("最大值 z为，", value(prob.objective), "个单位")
for v in prob.variables():
    print("最优值", v.name, ":", v.varValue, "个单位")

prob = LpProblem("problem2", LpMaximize)
C = LpVariable("C", 0, None, LpContinuous)

