from itertools import chain, product

rules = [("1!", "!110"), ("0!", "!0"), ("22!", "!22"),
         ("@0", "01@"), ("@1", "1@"), ("@2", "22@"),
         ("@", "!"), ("?!", "", True), ("", "?@")]

rules = list(map(lambda x: x + (False,) if len(x) == 2 else x, rules))


inputs = list(map(lambda x: ''.join(x), chain(*[product("012", repeat=i) for i in range(1, 7)])))
ready = {}
tree = {x: [x] for x in inputs}


def step(word):
    for r in rules:
        if word.find(r[0]) != -1:
            return word.replace(r[0], r[1], 1), r[2]
    return word, True


def stop(all_examples = False):
    if not hasattr(stop, "old"):
        stop.old = set()
    for w in ready:
        if (all_examples or w not in stop.old) and ready[w][-1] == "110222211001100110":
            print("******FOUND******", w, "----", ready[w])
            stop.old.add(w)


while len(tree) > 0:
    for w in tree.copy():
        next, end = step(tree[w][-1])
        if next != tree[w][-1]:
            tree[w].append(next)
        if end:
            ready[w] = tree.pop(w)
    # print(tree)
    stop()
print("************RESULT****************")
stop(all_examples=True)