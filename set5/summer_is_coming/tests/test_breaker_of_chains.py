def concreter(abclass):
    if "__abstractmethods__" not in abclass.__dict__:
        return abclass
    new_dict = abclass.__dict__.copy()
    for abstractmethod in abclass.__abstractmethods__:
        # replace each abc method or property with an identity function:
        new_dict[abstractmethod] = lambda x, *args, **kw: (x, args, kw)
    # creates a new class, with the overriden ABCs:
    return type(f"dummy_concrete_{abclass.__name__}", (abclass,), new_dict)


def high_priest():
    return concreter(UniverseCompetition)

def test__crown_king():
