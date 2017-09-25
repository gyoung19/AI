Team:
  <jekim14@amherst.edu gyoung19@amherst.edu>
Heuristic for Q6:
  <We have constructed several different heuristics, but to mention the one that we are going to use: 
  1. DESIDERATA
   (1) distance D1 from the current position to the nearest corner C  
   (2) distance D2 from that corner C to the farthest remaining corner C' 
    (distance = Manhattan)
  2. STRATEGY
    h(n) = D1 + D2.
    In other words, the heuristic value is the optimistic estimate of 
     the distance to the nearest food 
      plus 
     the distance to be traversed from that food to the farthest food left.

    We had discussed whether this heuristic is really consistent, and we agreed that it should be:

    "The optimal path for any of these mazes should be a continuous path from the starting point through all pellets in the maze that retraces steps as few times as possible. To be consistent, the heuristic estimate has to be always less than the total path from any node to the goal for any node ... [T]his heuristic fulfills that requirement since the straight line distance starting from the closest food to the farthest food will approximate the optimal path under ideal conditions (maze is a straight line from nearest to farthest food with no turns, walls, corners, etc) and be less than the optimal path under all other conditions (if there is any deviation from the straight line the optimal path will take longer than the straight line estimate)." (Gabriel's comment on Github)

    This heuristic is more optimistic than our previous heuristic, cornersHeuristic_totalTraversal.>
Resources used:
  <https://docs.python.org/2/library/itertools.html#itertools.permutations (We ended up not using permutations, though.)>
Time spent on assignment: <30 hrs>
On a scale from -2 to 2:
  How hard was the assignment? 
  <1>
  How much did you learn from the assignment? 
  <2>
  How much did you enjoy the assignment? 
  <2>
Additional notes: <Our work can be also found on Github: https://github.com/gyoung19/AI>