from itertools import chain, product

characters = tuple("ab1_")

rules = [("a", 0, "r"), ("b", 0, "r"), ("1", 0, "r"), ("_", 1, "l"),
         ("_", 2, "l"), ("_", 1, "l"), ("1", 1, "l"), ("_", -1, "r"),
         ("a", 2, "l"), ("b", 2, "l"), ("1", 2, "l"), ("1", 0, "r")]

inputs = list(map(lambda x: ''.join(x), chain(*[product("ab", repeat=i) for i in range(1, 4)])))

# inputs = ["a"]

class TurTable():
    def __init__(self, rules, characters):
        assert(len(rules) % len(characters) == 0)
        self.states_num = len(rules) // len(characters)
        self.characters_num = len(characters)
        self.rules = {c: rules[i::self.characters_num] for i, c in enumerate(characters)}

    def __getitem__(self, key):
        return self.rules[key[1]][key[0]]


table = TurTable(rules, characters)

ready = {}
tree = {x: [(x, 0, 0)] for x in inputs}
print(tree)

def step(triple):
    word, state, pos = triple
    if pos == -1:
        word = "_" + word
        pos = 0
    if pos == len(word):
        word += "_"

    r = table[state, word[pos]]
    return word[:pos] + r[0] + word[pos+1:], r[1], pos if r[2] == "n" else pos-1 if r[2] == "l" else pos+1


def stop(all_examples = False):
    if not hasattr(stop, "old"):
        stop.old = set()
    for w in ready:
        if all_examples or w not in stop.old:
            print("******FOUND******", w, "---- len =",len(ready[w]), ":" , ready[w])
            stop.old.add(w)


def postprocess(triple):
    word, state, pos = triple
    while len(word) > 1 and pos != 0 and word[0] == "_":
        pos -= 1
        word = word[1:]
    while len(word) > 1 and pos != len(word) -1 and word[-1] == "_":
        word = word[:-1]
    return word, state, pos


while len(tree) > 0:
    for w in tree.copy():
        next_state = step(tree[w][-1])
        tree[w].append(postprocess(next_state))
        if next_state[1] == -1:
            ready[w] = tree.pop(w)
    # print(tree)
    stop()
print("************RESULT****************")
stop(all_examples=True)