
import unittest


def matching(ref, test, key=None):
    if key is None:
        def key(x): return x
    result = list()
    for r in ref:
        filtered = list(filter(lambda x: key(r) == key(x[1]),
                               enumerate(test)))
        assert len(filtered) <= 1, "matching: More than one matched!"
        if any(filtered):
            result.append(filtered[0][0])
        else:
            result.append(None)
    return result


def diff(list1, list2, key=None):
    if key is None:
        def key(x): return x

    # Sort by key first
    l1Sorted = sorted(list1, key=key)
    l2Sorted = sorted(list2, key=key)
    # find matched with ref. to l1 and l2:
    matchedToL1 = matching(l1Sorted, l2Sorted, key=key)
    matchedToL2 = matching(l2Sorted, l1Sorted, key=key)
    # Transform matchedToL1 to tuple
    matchedTuples1 = list()
    for idx1, idx2 in enumerate(matchedToL1):
        if idx2 is not None:
            matchedTuples1.append((l1Sorted[idx1], l2Sorted[idx2]))
        else:
            matchedTuples1.append((l1Sorted[idx1], None))
    # Transform matchedToL2 to tuple, ignoring matched
    matchedTuples2 = list()
    for idx2, idx1 in enumerate(matchedToL2):
        if idx1 is not None:
            pass
        else:
            matchedTuples2.append((None, l2Sorted[idx2]))
    # Merging matchedTuples1 and matchedTuples2 then sort
    matchedTuples = matchedTuples1 + matchedTuples2
    return sorted(matchedTuples,
                  key=lambda x:
                      key(list(filter(None, x))[0]))


class TestDiffFunction(unittest.TestCase):

    def testOrderedList(self):
        list1 = ['b', 'c', 'd', 'e', 'h', 'i', 'k']
        list2 = ['a', 'b', 'c', 'h', 'l']

        result = diff(list1, list2)

        self.assertEqual(
            result,
            [(None, 'a'),
             ('b', 'b'),
             ('c', 'c'),
             ('d', None),
             ('e', None),
             ('h', 'h'),
             ('i', None),
             ('k', None),
             (None, 'l')])

        list1FromResult = list(filter(None, map(lambda x: x[0], result)))
        list2FromResult = list(filter(None, map(lambda x: x[1], result)))
        self.assertEqual(list1FromResult, list1)
        self.assertEqual(list2FromResult, list2)

    def testOrderedListWithKey(self):
        list1 = [('b', 'l1'), ('c', 'l1'), ('d', 'l1'), ('e', 'l1'),
                 ('h', 'l1'), ('i', 'l1'), ('k', 'l1')]
        list2 = [('a', 'l2'), ('b', 'l2'), ('c', 'l2'), ('h', 'l2'),
                 ('l', 'l2')]
        result = diff(list1, list2, key=lambda x: x[0])

        self.assertEqual(
            result,
            [(None, ('a', 'l2')),
             (('b', 'l1'), ('b', 'l2')),
             (('c', 'l1'), ('c', 'l2')),
             (('d', 'l1'), None),
             (('e', 'l1'), None),
             (('h', 'l1'), ('h', 'l2')),
             (('i', 'l1'), None),
             (('k', 'l1'), None),
             (None, ('l', 'l2'))])

        list1FromResult = list(filter(None, map(lambda x: x[0], result)))
        list2FromResult = list(filter(None, map(lambda x: x[1], result)))
        self.assertEqual(list1FromResult, list1)
        self.assertEqual(list2FromResult, list2)

    def testNotOrderedList(self):
        list1 = ['e', 'c', 'd', 'b', 'i', 'k', 'h']
        list2 = ['h', 'b', 'c', 'l', 'a']

        result = diff(list1, list2)

        self.assertEqual(
            result,
            [(None, 'a'),
             ('b', 'b'),
             ('c', 'c'),
             ('d', None),
             ('e', None),
             ('h', 'h'),
             ('i', None),
             ('k', None),
             (None, 'l')])

        list1FromResult = list(filter(None, map(lambda x: x[0], result)))
        list2FromResult = list(filter(None, map(lambda x: x[1], result)))
        self.assertEqual(list1FromResult, sorted(list1))
        self.assertEqual(list2FromResult, sorted(list2))

    def testNotOrderedListWithKey(self):
        list1 = [('c', 'l1'), ('d', 'l1'), ('e', 'l1'), ('k', 'l1'),
                 ('h', 'l1'), ('b', 'l1'), ('i', 'l1')]
        list2 = [('l', 'l2'), ('a', 'l2'), ('b', 'l2'), ('h', 'l2'),
                 ('c', 'l2')]
        result = diff(list1, list2, key=lambda x: x[0])

        self.assertEqual(
            result,
            [(None, ('a', 'l2')),
             (('b', 'l1'), ('b', 'l2')),
             (('c', 'l1'), ('c', 'l2')),
             (('d', 'l1'), None),
             (('e', 'l1'), None),
             (('h', 'l1'), ('h', 'l2')),
             (('i', 'l1'), None),
             (('k', 'l1'), None),
             (None, ('l', 'l2'))])

        list1FromResult = list(filter(None, map(lambda x: x[0], result)))
        list2FromResult = list(filter(None, map(lambda x: x[1], result)))
        self.assertEqual(list1FromResult, sorted(list1, key=lambda x: x[0]))
        self.assertEqual(list2FromResult, sorted(list2, key=lambda x: x[0]))
