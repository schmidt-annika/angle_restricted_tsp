
# Angle Restricted Traveling Salesman Problem

This work deals with the combination of two problems in graph theory, more specifically with the search for a cost-minimal Hamiltonian path while maintaining an angular constraint. If a path is evaluated exclusively based on the sum of all edge weights, this question has already been well investigated. The extension of the angle-constrained Hamilton path considered below is that the cost function also takes into account the angle between two edges of the path in addition to the edge weight. For an angular set W ⊆ {θ | −π2 ≤ θ ≤ π2}, the angle-constrained Hamilton path problem describes the decision as to whether a set P of n nodes in the Euclidean plane can be connected by a Hamilton path consisting of straight lines in a row such that all angles between n consecutive straight lines come from the set W.


## Usage

The combination of the minimal, angle-limited Hamiltonian path is a challenge that not only arouses theoretical interest, but is also of great importance in the real world, especially in robotics. Optimizing routes for robots to reach different points as efficiently as possible is a central concern in the development of autonomous systems. A route planning with a route that is as straight as possible enables the use of robots with limited steering. Skilled path planning can also increase the efficiency of high-speed vehicles such as certain cars, trains or airplanes, as lengthy braking and acceleration phases in curves can be avoided. In addition to performance, this gentle driving style with less frequent and lower occurrence of lateral forces also significantly improves the safety and life of the robots and vehicles.





## Running Tests
To choose one of the algorithms provided, one of the following abbreviations must be entered:
* nn (Nearest Neighbour)
* ni (Nearest Insertion with global Minimum)
* fi (Farthest Insertion with global Maximum)
* nilm (Nearest Insertion with local Minimum)
* film (Farthes Insertion with local Maximum)
* ri (Random Insertion)
* nni (Nearest Neighbour with Insertion)
* mst (Minimum Spanning Tree)

To use the provided algorithms, the name of a .txt file in the same directory should be inserted whose first line consists of a single integer n, representing the number of nodes, and the following n lines consist of two numbers, separated by a space, representing the x and y coordinates of a node.

```bash
  5
  7.567876 4.2387462
  3.482842 5.23848293
  9.29347623 0.237463
  2.234234 3.0
  3.23423 23.2342342
```

Then 'ja' (German for yes) or 'nein' (German for no) must be entered as to whether the path found should be visualized via Turtle graphics or not.



## Screenshots

![Screenshot](screenshot.jpg?raw=true)

