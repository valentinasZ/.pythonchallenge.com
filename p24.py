from PIL import Image
import cv2
import numpy as np
from collections import deque


class MazeSolver:
    def __init__(self, path):
        self.path = path

    def load_maze(self):
        maze_image = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        maze = np.where(np.all(maze_image == [255,255,255,255], axis = -1),0 ,1)
        return maze

    def find_entry_exit(self):
        image = Image.open(self.path)
        width, height = image.size
        points = []


        for x in range(width):
            if image.getpixel((x, 0)) == (0, 0, 0, 255):
                points.append((x, 0))
            if image.getpixel((x, height - 1)) == (0, 0, 0, 255):
                points.append((x, height - 1))

        print(f"Entry: {points[1]}")
        print(f"Exit:  {points[0]}")
        return points[1], points[0]

    def solve(self):
        maze = self.load_maze()
        entry, exit = self.find_entry_exit()

        queue = deque([(entry, [entry])])
        visited = set([entry])

        while queue:
            current, path = queue.popleft()

            if current == exit:
                print(f"\nPath found! {len(path)} steps\n")
                for step, (x, y) in enumerate(path):
                    print(f"Step {step:4d}: ({x}, {y})")
                return path

            x, y = current
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < maze.shape[1] and
                        0 <= ny < maze.shape[0] and
                        maze[ny, nx] == 1 and  # is it a path?
                        (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))

        print("No path found!")
        return None

    def extract_data(self,path):
        image = Image.open(self.path)
        chars = []
        for (x,y) in path:
            if x % 2 == 1 and y % 2 == 1:
                r = image.getpixel((x, y))[0]
                chars.append(chr(r))
                print(f"  ({x}, {y}) -> red={r} -> '{chr(r)}'")

        result = "".join(chars)

        with open("24_challenge.zip", 'wb') as f:
            f.write(result.encode('latin-1'))

        return result




solver = MazeSolver("maze.png")
path = solver.solve()

if path:
    data = solver.extract_data(path)





