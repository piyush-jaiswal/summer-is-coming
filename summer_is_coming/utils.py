import io

from sortedcontainers import SortedKeyList


def sorted_list_get_with_key(sorted_list: SortedKeyList, key: object) -> object:
    idx = sorted_list.bisect_key_left(key)
    if idx < len(sorted_list) and sorted_list.key(sorted_list[idx]) == key:
        return sorted_list[idx]
    else:
        raise ValueError(
            "key '{}' not present in sorted list '{}'".format(key, sorted_list)
        )


def clear_stringio(stringio: io.StringIO):
    stringio.truncate(0)
    stringio.seek(0)


def show_universe_state(universe_name: str, king: str, allies: str):
    print()
    print(f"Who is the ruler of {universe_name}?")
    print("Output:", king)
    print("Allies of Ruler?")
    print("Output:", allies)
    print()
