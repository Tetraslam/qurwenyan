import matplotlib.pyplot as plt
import numpy as np
import random
from itertools import combinations

n = 26
vowels = ['a', 'e', 'i', 'o', 'u', 'y']
radical = 'y'

# Define the radicals as line segments
radicals = {
    'a': [(1, 0.5), (1.5, 1)],
    'e': [(1, 1), (1.5, 0.5)],
    'i': [(1, 1), (1.5, 0.5), (2, 1)],
    'o': [(1, 0.5), (1.5, 1), (2, 0.5)],
    'u': [(1.5, 1.5), (2, 1), (1.5, 0.5)],
    'y': [(2, 1.5), (1.5, 1), (2, 0.5)]
}

def check_intersection(p1, p2, p3, p4):
    # Helper function to check if two line segments (p1p2 and p3p4) intersect
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

def glyph_generator(grid_size=5, num_points=5):
    while True:
        points = set()
        while len(points) < num_points:
            points.add((random.randint(1, grid_size - 2), random.randint(1, grid_size - 2)))
        points = list(points)
        random.shuffle(points)

        segments = [(points[i], points[i + 1]) for i in range(len(points) - 1)]
        intersection_count = sum(check_intersection(s1[0], s1[1], s2[0], s2[1]) for s1, s2 in combinations(segments, 2))

        if intersection_count <= 1:
            x_values, y_values = zip(*points)
            yield x_values, y_values

def save_glyphs(num_glyphs, grid_size=5, num_points=5):
    generator = glyph_generator(grid_size, num_points)
    chosen_radical = radical
    
    for i in range(num_glyphs):
        x_values, y_values = next(generator)
        
        fig, ax = plt.subplots()
        ax.set_xlim(0.5, grid_size - 1.5)
        ax.set_ylim(0.5, grid_size - 1.5)
        ax.set_xticks(np.arange(0, grid_size, 1))
        ax.set_yticks(np.arange(0, grid_size, 1))
        ax.grid(True)
        
        ax.plot(x_values, y_values, marker='o', linewidth=10)
        
        # Add the chosen radical at the top of the grid
        radical_points = radicals[chosen_radical]
        radical_x, radical_y = zip(*radical_points)
        ax.plot(radical_x, radical_y, marker='o', color='red', linewidth=10)
        
        plt.gca().invert_yaxis()
        plt.axis('off')
        plt.savefig(f'{radical}_glyph_{i+1}.png')
        plt.close()

# Save n glyphs to the current folder
save_glyphs(n)
