import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

temp = ctrl.Antecedent(np.arange(0, 45, 1), 'temp')  # Degrees Celsius
mois = ctrl.Antecedent(np.arange(0, 100, 1), 'mois')  # %
kind = ctrl.Antecedent(np.arange(0, 2, 0.01), 'kind')
soil = ctrl.Antecedent(np.arange(0, 5, 0.01), 'soil') 
stage = ctrl.Antecedent(np.arange(0, 4, 1), 'stage')

water = ctrl.Consequent(np.arange(0, 30, 0.1), 'water')  
times = ctrl.Consequent(np.arange(0, 3, 1), 'times') 

kind['h'] = fuzz.trapmf(kind.universe, [0, 0, 0.5, 0.5])  # Herbaceous
kind['w'] = fuzz.trapmf(kind.universe, [0.5, 0.5, 1.5, 1.5])  # Woody
# kind.view()
# plt.show()

temp['c'] = fuzz.trimf(temp.universe, [0, 15, 25])  
temp['n'] = fuzz.trimf(temp.universe, [17, 27, 33])  
temp['h'] = fuzz.trapmf(temp.universe, [25, 40, 45, 45])  
# temp.view()
# plt.show()

mois['d'] = fuzz.trimf(mois.universe, [0, 15, 45])
mois['m'] = fuzz.trimf(mois.universe, [20, 50, 80])
mois['w'] = fuzz.trapmf(mois.universe, [50, 85, 100, 100])
# mois.view()
# plt.show()

soil['s'] = fuzz.trapmf(soil.universe, [0, 0, 0.5, 0.5])  # Sand 
soil['a'] = fuzz.trapmf(soil.universe, [0.5, 0.5, 1.5, 1.5])  # Alluvium 
soil['l'] = fuzz.trapmf(soil.universe, [1.5, 1.5, 2.5, 2.5])  # Loam 
soil['c'] = fuzz.trapmf(soil.universe, [2.5, 2.5, 3.5, 3.5])  # Clay 
# soil.view()
# plt.show()

stage['ge'] = fuzz.trapmf(stage.universe, [0, 0, 0.5, 0.5])  # Germination 
stage['gr'] = fuzz.trapmf(stage.universe, [0.5, 0.5, 1.5, 1.5])  # Growing 
stage['fg'] = fuzz.trapmf(stage.universe, [1.5, 1.5, 2.5, 2.5])  # Full-growing 
# stage.view()
# plt.show()

water['n'] = fuzz.trimf(water.universe, [0, 0, 0])
water['vl'] = fuzz.trimf(water.universe, [0, 0.3, 0.7])
water['l'] = fuzz.trimf(water.universe, [0.3, 1, 1.5])
water['a'] = fuzz.trimf(water.universe, [1, 4, 7])
water['m'] = fuzz.trimf(water.universe, [5, 13, 20])
water['vm'] = fuzz.trimf(water.universe, [15, 25, 30])
# water.view()
# plt.show()

times['0'] = fuzz.trimf(times.universe, [0, 0, 0])
times['1'] = fuzz.trimf(times.universe, [1, 1, 1])
times['2'] = fuzz.trimf(times.universe, [2, 2, 2])
times['3'] = fuzz.trimf(times.universe, [3, 3, 3])
times['4'] = fuzz.trimf(times.universe, [4, 4, 4])
# times.view()
# plt.show()

# RULE-----------------------
very_little_1_time = ctrl.Rule(
    (
        (kind['h'] & (
            (temp['c'] & (
                ((mois['d'] | mois['m']) & soil['c'] & stage['fg']) |
                (mois['w'] & soil['s'] & stage['gr']) |
                (mois['w'] & soil['a'] & stage['ge'])
            )) |
            (temp['n'] & (
                (mois['m'] & soil['c'] & (stage['gr'] | stage['fg'])) |
                (mois['w'] & soil['s'] & (stage['ge'] | stage['gr'])) |
                (mois['w'] & soil['a'] & stage['ge'])
            )) |
            (temp['h'] & (
                (mois['w'] & (soil['s'] | soil['a']) & stage['gr']) |
                (mois['w'] & (soil['a'] | soil['l']) & stage['ge'])
            ))
        )) |
        (kind['w'] & (
            (temp['c'] & (
                (mois['m'] & soil['c'] & stage['ge']) |
                (mois['w'] & (soil['s'] | soil['a'] | soil['l']) & stage['ge']) |
                (mois['w'] & soil['s'] & stage['gr'])
            )) |
            (temp['n'] & (
                (mois['m'] & soil['c'] & stage['ge']) |
                (mois['w'] & soil['s'] & stage['gr']) |
                (mois['w'] & (soil['l'] | soil['c']) & stage['ge'])
            )) |
            (temp['h'] & mois['w'] & soil['c'] & stage['ge'])
        ))
    ), (water['vl'], times['1'])
)

very_little_2_times = ctrl.Rule(
    (
        (kind['h'] & (
            (temp['c'] & (
                (mois['d'] & (soil['a'] | soil['l'] | soil['c']) & stage['ge']) |
                (mois['m'] & (soil['a'] | soil['l'] | soil['c']) & stage['ge'])
            )) |
            (temp['n'] & (
                (mois['d'] & (soil['l'] | soil['c']) & stage['ge']) |
                (mois['m'] & soil['l'] & (stage['ge'] | stage['gr'] | stage['fg'])) |
                (mois['m'] & soil['c'] & stage['ge'])
            )) |
            (temp['h'] & mois['w'] & soil['s'] & stage['ge'])
        )) |
        (kind['w'] & temp['n'] & mois['w'] & (soil['s'] | soil['a']) & stage['ge'])
    ), (water['vl'], times['2'])
)

very_little_3_times = ctrl.Rule(
    (kind['h'] & temp['n'] & (mois['d'] | mois['m']) & soil['a'] & stage['ge']), (water['vl'], times['3'])
)

little_1_time = ctrl.Rule(
    (
        (kind['h'] & (
            (temp['c'] & (
                (mois['d'] & soil['l'] & stage['fg']) |
                (mois['m'] & (soil['a'] | soil['l']) & stage['fg']) |
                (mois['m'] & (soil['l'] | soil['c']) & stage['gr'])
            )) |
            (temp['n'] & mois['d'] & soil['c'] & stage['fg']) |
            (temp['h'] & (
                (mois['m'] & soil['l'] & stage['fg']) |
                (mois['m'] & soil['c'] & (stage['gr'] | stage['fg']))
            ))
        )) |
        (kind['w'] & (
            (temp['c'] & (
                (mois['m'] & soil['l'] & stage['fg']) |
                (mois['m'] & soil['c'] & (stage['gr'] | stage['fg']))
            )) |
            (temp['n'] & (
                (mois['m'] & soil['l'] & stage['fg']) |
                (mois['m'] & soil['c'] & (stage['gr'] | stage['fg']))
            )) |
            (temp['h'] & (
                (mois['w'] & soil['s'] & (stage['gr'] | stage['fg'])) |
                (mois['w'] & soil['a'] & stage['fg'])
            ))
        ))
    ), (water['l'], times['1'])
)

little_2_times = ctrl.Rule(
    (
        (kind['h'] & (
            (temp['c'] & (
                (mois['d'] & (soil['s'] | soil['a'] | soil['l'] | soil['c']) & stage['gr']) |
                (mois['d'] & (soil['s'] | soil['a']) & stage['fg']) |
                (mois['m'] & soil['s'] & (stage['ge'] | stage['gr'] | stage['fg'])) |
                (mois['m'] & soil['a'] & stage['gr'])
            )) |
            (temp['n'] & (
                (mois['d'] & (soil['s'] | soil['a'] | soil['l']) & stage['fg']) |
                (mois['d'] & (soil['a'] | soil['l'] | soil['c']) & stage['gr']) |
                (mois['m'] & soil['s'] & (stage['ge'] | stage['gr'] | stage['fg'])) |
                (mois['m'] & soil['a'] & (stage['gr'] | stage['fg']))
            )) |
            (temp['h'] & (
                (mois['d'] & (soil['s'] | soil['a'] | soil['l'] | soil['c']) & stage['fg']) |
                (mois['d'] & (soil['l'] | soil['c']) & stage['ge']) |
                (mois['d'] & soil['l'] & stage['gr']) |
                (mois['m'] & (soil['a'] | soil['l'] | soil['c']) & stage['ge']) |
                (mois['m'] & soil['a'] & stage['fg'])
            ))
        )) |
        (kind['w'] & (
            ((temp['c'] | temp['n']) & mois['m'] & soil['l'] & stage['ge']) |
            (temp['h'] & (
                (mois['w'] & (soil['s'] | soil['a'] | soil['l']) & stage['ge']) |
                (mois['w'] & soil['a'] & stage['gr'])
            ))
        ))
    ), (water['l'], times['2'])
)

little_3_times = ctrl.Rule(
    (
        kind['h'] & (
            (temp['c'] & mois['d'] & soil['s'] & stage['ge']) |
            (temp['n'] & mois['d'] & soil['s'] & (stage['ge'] | stage['gr'])) |
            (temp['h'] & mois['d'] & soil['a'] & stage['ge']) |
            (temp['h'] & mois['m'] & soil['s'] & stage['ge'])
        )
    ), (water['l'], times['3'])
)

average_1_time = ctrl.Rule(
    (
        (kind['h'] & temp['h'] & mois['m'] & soil['s'] & stage['fg']) |
        (kind['w'] & (
            (temp['c'] & (
                (mois['m'] & soil['a'] & stage['fg']) |
                (mois['m'] & soil['l'] & stage['gr'])
            )) |
            (temp['h'] & mois['m'] & soil['c'] & stage['gr'])
        ))
    ), (water['a'], times['1'])
)

average_2_times = ctrl.Rule(
    (
        (kind['h'] & (
            (temp['h'] & mois['d'] & soil['c'] & stage['gr']) |
            (temp['h'] & mois['m'] & (soil['s'] | soil['a'] | soil['l']) & stage['gr'])
        )) |
        (kind['w'] & (
            (temp['c'] & (
                (mois['d'] & (soil['s'] | soil['a'] | soil['l'] | soil['c']) & stage['fg']) |
                (mois['d'] & (soil['a'] | soil['l'] | soil['c']) & stage['ge']) |
                (mois['d'] & soil['c'] & stage['gr']) |
                (mois['m'] & soil['s'] & (stage['gr'] | stage['fg'])) |
                (mois['m'] & soil['a'] & stage['gr'])
            )) |
            (temp['n'] & (
                (mois['d'] & (soil['s'] | soil['a'] | soil['l'] | soil['c']) & stage['fg']) |
                (mois['d'] & soil['c'] & stage['ge']) |
                (mois['m'] & (soil['s'] | soil['a']) & stage['fg']) |
                (mois['m'] & soil['l'] & stage['gr'])
            )) |
            (temp['h'] & mois['m'] & soil['c'] & stage['ge'])
        ))
    ), (water['a'], times['2'])
)

average_3_times = ctrl.Rule(
    (
        (kind['h'] & temp['h'] & mois['d'] & soil['a'] & stage['gr']) |
        (kind['w'] & (
            (temp['c'] & mois['m'] & (soil['s'] | soil['a']) & stage['ge']) |
            (temp['n'] & mois['m'] & (soil['s'] | soil['a']) & stage['ge']) |
            (temp['h'] & mois['m'] & soil['l'] & stage['ge'])
        ))
    ), (water['a'], times['3'])
)

average_4_times = ctrl.Rule(
    (kind['h'] & temp['h'] & mois['d'] & soil['s'] & (stage['ge'] | stage['gr'])), (water['a'], times['4'])
)

much_1_time = ctrl.Rule(
    (kind['w'] & temp['h'] & mois['m'] & (soil['l'] | soil['c']) & stage['fg']), (water['m'], times['1'])
)

much_2_times = ctrl.Rule(
    (
        kind['w'] & (
            (temp['c'] & mois['d'] & (soil['s'] | soil['l']) & stage['gr']) |
            (temp['n'] & (
                (mois['d'] & (soil['a'] | soil['l'] | soil['c']) & stage['gr']) |
                (mois['d'] & soil['l'] & stage['ge']) |
                (mois['m'] & soil['a'] & stage['gr'])
            )) |
            (temp['h'] & (
                (mois['d'] & (soil['a'] | soil['l']) & stage['fg']) |
                (mois['d'] & soil['c'] & stage['ge']) |
                (mois['m'] & soil['a'] & stage['fg']) |
                (mois['m'] & soil['l'] & stage['gr'])
            ))
        )
    ), (water['m'], times['2'])
)

much_3_times = ctrl.Rule(
    (
        kind['w'] & (
            (temp['c'] & (
                (mois['d'] & soil['s'] & stage['ge']) |
                (mois['d'] & soil['a'] & stage['gr'])
            )) |
            (temp['n'] & (
                (mois['d'] & (soil['s'] | soil['a']) & stage['ge']) |
                (mois['m'] & soil['s'] & stage['gr'])
            )) |
            (temp['h'] & (
                (mois['d'] & soil['l'] & stage['ge']) |
                (mois['m'] & soil['s'] & stage['ge']) |
                (mois['m'] & soil['a'] & (stage['ge'] | stage['gr']))
            ))
        )
    ), (water['m'], times['3'])
)

much_4_times = ctrl.Rule(
    (kind['w'] & temp['h'] & mois['d'] & soil['s'] & stage['ge']), (water['m'], times['4'])
)

very_much_2_times = ctrl.Rule(
    (
        (kind['w'] & temp['h'] & (
            (mois['d'] & (soil['s'] | soil['c']) & stage['fg']) |
            (mois['d'] & (soil['l'] | soil['c']) & stage['gr']) |
            (mois['m'] & soil['s'] & (stage['gr'] | stage['fg']))
        ))
    ), (water['vm'], times['2'])
)

very_much_3_times = ctrl.Rule(
    (
        (kind['w'] & (
            ((temp['n'] | temp['h']) & mois['d'] & soil['s'] & stage['gr']) |
            (temp['h'] & mois['d'] & soil['a'] & (stage['ge'] | stage['gr']))
        ))
    ), (water['vm'], times['3'])
)

no_watering = ctrl.Rule(
    (
        (kind['h'] & (
            (temp['c'] & (
                (mois['w'] & (soil['s'] | soil['l'] | soil['c']) & stage['ge']) |
                (mois['w'] & (soil['a'] | soil['l'] | soil['c']) & stage['gr']) |
                (mois['w'] & (soil['s'] | soil['a'] | soil['l'] | soil['c']) & stage['fg'])
            )) |
            (temp['n'] & (
                (mois['w'] & (soil['s'] | soil['a'] | soil['l'] | soil['c']) & stage['fg']) |
                (mois['w'] & (soil['a'] | soil['l'] | soil['c']) & stage['gr']) |
                (mois['w'] & (soil['l'] | soil['c']) & stage['ge'])
            )) |
            (temp['h'] & (
                (mois['w'] & (soil['s'] | soil['a'] | soil['l'] | soil['c']) & stage['fg']) |
                (mois['w'] & (soil['l'] | soil['c']) & stage['gr']) |
                (mois['w'] & soil['c'] & stage['ge'])
            ))
        )) |
        (kind['w'] & (
            (temp['c'] & (
                (mois['w'] & (soil['s'] | soil['a'] | soil['l'] | soil['c']) & stage['fg']) |
                (mois['w'] & (soil['a'] | soil['l'] | soil['c']) & stage['gr']) |
                (mois['w'] & soil['c'] & stage['ge'])
            )) |
            (temp['n'] & (
                (mois['w'] & (soil['s'] | soil['a'] | soil['l'] | soil['c']) & stage['fg']) |
                (mois['w'] & (soil['a'] | soil['l'] | soil['c']) & stage['gr'])
            )) |
            (temp['h'] & (
                (mois['w'] & soil['l'] & (stage['gr'] | stage['fg'])) |
                (mois['w'] & soil['c'] & (stage['gr'] | stage['fg']))
            ))
        ))
    ), (water['n'], times['0'])
)

# Training model
ctrl_watering = ctrl.ControlSystem(
    rules=[very_little_2_times, very_little_3_times,
           little_1_time, little_2_times, little_3_times,
           average_1_time, average_2_times, average_3_times, average_4_times,
           much_1_time, much_2_times, much_3_times, much_4_times,
           very_much_2_times, very_much_3_times,
           no_watering, ]
)
watering = ctrl.ControlSystemSimulation(ctrl_watering)

# watering.compute()
# print('Water', watering.output['water'], 'Time:', watering.output['times'])
# water.view(sim=watering)
# plt.show()

# watering.input['kind'] = 0
# watering.input['temp'] = 36
# watering.input['mois'] = 42
# watering.input['soil'] = 2
# watering.input['stage'] = 1  # 4-1.64

# watering.input['kind'] = 1
# watering.input['temp'] = 40
# watering.input['mois'] = 25
# watering.input['soil'] = 1
# watering.input['stage'] = 1  # 23.14-1.54
