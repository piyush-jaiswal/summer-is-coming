## Design considerations

### Problem of Kingdom and Universe
- Universe provides a `get_kingdom` method to get the kingdom object that is part of the universe.
- Thus the client code can receive the kingdom object and can also form allegiances with other kingdoms using the kingdom object, not necessarily belonging to the same universe. This would be a problem.
- On the other hand if the `give_allegiance` and `ask_allegiance` methods of the Kingdom class are internal, it wouldn't make sense semantically to call the internal method from the universe class.
- Making `Kingdom` a nested class of `Universe`, in order for `Universe` to call internal methods of `Kingdom` for semantic correctness, would seem ugly.
- Another solution was to make separate methods for the kingdom properties such as `name` and `emblem`, but this would increase coupling with the `Kingdom` class and would break the `open-closed principle` as the `Universe` class would need to be changed, each time a property was added to the `Kingdom` class. This is the reason `Universe` provides an API to get the whole kingdom object.
- As a solution to this the `get_kingdom` API returns a deepcopy of the `Kingdom` object, preventing client code from modifying the state of the kingdom objects that belong to the universe.



### Assumptions
- Ability to form allies, when competing, and when already having previous ally, are problem specific. Hence their logic is not coupled in the member function ```form_allegiance``` in ```universe.py```.
- Every consecutive ballot rounds, the remaining competing kingdoms lose their allies. The previously competing ones can form allegiances.
- The data structures implemented with ```SortedKeyList``` have lookup and insert time of `O(log n)`. If memory is not an issue, these can be replaced with python's inbuilt ```dict``` with lookup time of `O(1)`.