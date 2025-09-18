from math import sin, cos
from statistics import mean, stdev
import random
import pandas as pd
from collections import defaultdict

STEPS = [0.01, 0.05, 0.1, 0.2]
BEAM_WIDTHS = [2,4,8,16]

def f1(x, y):
    return sin(sin(x/2)) + cos(cos(2*y))

def f2(x,y):
    return -1*abs(x-2) - abs(y/2+1) + 3

def get_random_point():
    return (random.uniform(0,10), random.uniform(0,10))

def get_neighbors(point, ada):
    x, y = point
    return [(x+ada, y), (x-ada, y), (x, y+ada), (x, y-ada),
            (x+ada, y+ada), (x+ada, y-ada), (x-ada, y+ada), (x-ada, y-ada)]
    

def hill_climb(init, ada, func):
    x, y = init
    maxx = func(x, y)
    argmaxx = (x, y)
    steps = 0
    while True:
        neighbors = get_neighbors(argmaxx, ada)
        found_better = False
        for nx, ny in neighbors:
            if 0 <= nx <= 10 and 0 <= ny <= 10:
                val = func(nx, ny)
                if val > maxx:
                    maxx = val
                    argmaxx = (nx, ny)
                    found_better = True
        if not found_better:
            break
        steps += 1
    return 1 if func==f1 else 2, steps, argmaxx, maxx
        

def beam_search(ada, beam_width, func):
    beam = []
    for _ in range(beam_width):
        point = get_random_point()
        beam.append((point, func(*point)))
    steps = 0
    maxx = max(beam, key=lambda x: x[1])[1]
    argmaxx = max(beam, key=lambda x: x[1])[0]
    while True:
        curr = []
        for point, val in beam:
            for neighbor in get_neighbors(point, ada):
                if 0<=neighbor[0]<=10 and 0<=neighbor[1]<=10:
                    curr.append((neighbor, func(*neighbor)))
        curr.sort(key = lambda x: x[1], reverse=True)
        if curr and curr[0][1]>maxx:
            beam = curr[:beam_width]
            maxx = beam[0][1]
            argmaxx = beam[0][0]
            steps += 1
        else:
            break
    return 1 if func==f1 else 2, steps, argmaxx, maxx
    
hill_climb_results = defaultdict(dict)
for j, f in enumerate([f1, f2]):
    for step in STEPS:
        num_til_convergence = []
        max_vals = []
        for i in range(100):
            init = get_random_point()
            func, iterations, point, value = hill_climb(init, step, f)
            num_til_convergence.append(iterations)
            max_vals.append(value)
        print("Iterations:", mean(num_til_convergence), "Values:", stdev(num_til_convergence), mean(max_vals), stdev(max_vals))
        hill_climb_results[f'f{j+1}'][step] = f"Mean Steps, {mean(num_til_convergence):.3f}<br>Deviation Steps: {stdev(num_til_convergence):.3f}<br>Mean Value: {mean(max_vals):.3f}<br>Deviation Value: {stdev(max_vals):.3f}"
        
hill_frame = pd.DataFrame(hill_climb_results).T
hill_frame.index.name = 'Function'
hill_frame.columns.name = 'Step Size'
hill_frame.to_html('outputs/hill_climb_results.html', escape=False)

for j,f in enumerate([f1, f2]):
    beam_search_results = defaultdict(dict)
    for w in BEAM_WIDTHS:
        for step in STEPS:
            num_til_convergence = []
            max_vals = []
            for i in range(100):
                func, iterations, point, value = beam_search(step, w, f)
                num_til_convergence.append(iterations)
                max_vals.append(value)
            print("Iterations:", mean(num_til_convergence), "Values:", stdev(num_til_convergence), mean(max_vals), stdev(max_vals))
            beam_search_results[w][step] = f"Mean Steps, {mean(num_til_convergence):.3f}<br>Deviation Steps: {stdev(num_til_convergence):.3f}<br>Mean Value: {mean(max_vals):.3f}<br>Deviation Value: {stdev(max_vals):.3f}"
    beam_frame = pd.DataFrame(beam_search_results).T
    beam_frame.index.name = 'Beam Width'
    beam_frame.columns.name = 'Step Size'
    beam_frame.to_html(f'outputs/beam_search_results_f{j+1}.html', escape=False)




    
        
        
    