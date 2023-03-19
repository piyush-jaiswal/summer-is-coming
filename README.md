# Tame of Thrones
The project is written in python3.7.

### Problem
For details please go through `problem_statement.pdf`

#### A Golden Crown
There is no ruler in the universe of Southeros and pandemonium reigns. Shan, the gorilla king of the Space kingdom
wants to rule all Six Kingdoms in the universe of Southeros. He needs the support of 3 more kingdoms to be the ruler. 

Each kingdom has an animal emblem and Shan needs to send a message with the animal in the message to win them over.
LAND emblem - Panda, WATER emblem - Octopus, ICE emblem - Mammoth, AIR emblem - Owl, FIRE emblem - Dragon.

Once he wins 3 more kingdoms, he is the ruler! The secret message needs to contain the letters of the animal in their
emblem. For example, secret message to the Land kingdom (emblem: Panda) needs to have the letter 'p','n','d' atleast
once and 'a' at-least twice. If he sends "a1d22n333a4444p" to the Land kingdom, he will win them over.

Problem is to have King Shan send secret message to each kingdom and win them over.


#### Breaker of Chains
The other kingdoms in the Universe also yearn to be the ruler of Southeros and war is imminent! The High Priest of Southeros
intervenes and is trying hard to avoid a war and he suggests a ballot system to decide the ruler.

The problem is to help the High Priest choose the ruler of Southeros through the ballot system.

<br></br>
### Assumptions
- Ability to form allies, when competing, and when already having previous ally, are problem specific. Hence their logic is not coupled in the member function ```form_allegiance``` in ```universe.py```.
- Every consecutive ballot rounds, the remaining competing kingdoms lose their allies. The previously competing ones can form allegiances.
- The data structures implemented with ```SortedKeyList``` have lookup and insert time of O(log n). If memory is not an issue, these can be replaced with python's inbuilt ```dict``` with lookup time of O(1).

### Dependencies
```pip install -r summer_is_coming/requirements.txt```

### Running the project
The solutions to the problems are implemented in menu driven style. The input format is the same as described in the problem statement. The only change is in ```a_golden_crown.py``` which additionally takes the number of messages as an input.<br>

To run from CLI:<br>
```cd <parent of root dir of project>```<br>
```python -m summer_is_coming.problem1```<br>
```python -m summer_is_coming.problem2```

### Testing
The test suite runs on pytest. Installing dependencies for testing:<br>
```pip install -r summer_is_coming/requirements-test.txt```

Running the test suite:<br>
```cd <root directory of project>```<br>
```pytest -v```
