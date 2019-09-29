# Summer is Coming
The project is written in python3.7.

### Assumptions
- Ability to form allies, when competing, and when already having previous ally, are problem specific. Hence their logic is not coupled in the member function ```form_allegiance``` in ```universe.py```.
- Every consecutive ballot rounds, the remaining competing kingdoms lose their allies. The previously competing ones can form allegiances.
- The data structures implemented with ```SortedKeyList``` have lookup and insert time of O(log n). If memory is not an issue, these can be replaced with python's inbuilt ```dict``` with lookup time of O(1).

### Dependencies
```pip install -r requirements.txt```

### Running the project
The solutions to the problems are implemented in menu driven style. The input format is the same as described in the problem statement. The only change is in ```a_golden_crown.py``` which additionally takes the number of messages as an input.<br>

To run from CLI:<br>
```cd <parent of root dir of project>```<br>
```python -m summer_is_coming.problem1```<br>
```python -m summer_is_coming.problem2```

### Testing
The test suite runs on pytest. Installing dependencies for testing:<br>
```pip install -r requirements-test.txt```

Running the test suite:<br>
```cd <root directory of project>```<br>
```pytest -v```
