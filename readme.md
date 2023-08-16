# maze_generation.py
## Description
This program visualizes the Recursive Backtracking, Prims and Eller's maze generation algorithms.

## Installation and use
To run the program:
- Activate the virtual environment by typing: source venv/bin/activate
- Once the virtual environment is running, type: python3 maze_generation.py

- Once you have Pygame installed, you can run the program
- When you initially run the program, you should see a blank black screen. 
- Simply press the space bar and the program will begin visualizing the different algorithms.
- You can also set a start and end point on the maze by clicking on any of the white spaces. 
- After having set the start and end points, click the up arrow and the program will solve the created maze. 

## Credits
I found the logic for the different algorithms here:
https://en.wikipedia.org/wiki/Maze_generation_algorithm 


# pathfinding_algorithms.py
## Description 
This program visualizes the Breadth First Search, A Star and greedy pathfinding algorithms. You can draw your own maze and then select which algorithm you would like to solve the maze with. This allows you to visually compare the process and effectiveness of these common pathfinding algorithms. 

## Installation and use 
To run the program:
- Activate the virtual environment by typing: source venv/bin/activate
- Once the virtual environment is running, type: python3 pathfinding_algorithms.py

Once the program is running:
- Your first click on the display will set the maze's start point (in orange)
- Your second click on the display will set the maze's end point (in red)
- After that, click anywhere to set the borders of the maze (in black)
- Once you are satisfied with the maze you have created, you can choose which pathfinding algorithm you wish to use to solve the maze:
    - Space bar: runs the Breadth Fist Search (BFS) algorithm
    - Up arrow: runs the A Star algorithm
    - Down arrow: runs the Greedy algorithm
    - Left arrow: clears resets the maze so that a new algorithm can be run

## Credits
I followed a tutorial in order to set up the visualizer:
https://www.youtube.com/watch?v=JtiK0DOeI4A 

I found the logic for the algorithms here:
https://en.wikipedia.org/wiki/Pathfinding 






