def search_pairs_two_cycles(array, n):
    """
    алгоритм поиска уникальных пар сумма которых равна n. O(n**2/2).
    """
    pairs = []
    checked = set()  # обеспечивает уникальность
    while array:
        number1 = array.pop(0)
        for i in range(len(array)):
            if array[i] not in checked and n == array[i] + number1:
                number2 = array.pop(i)
                pairs.append((number1, number2))
                checked.add(number1)
                checked.add(number2)
                break
    print(pairs)
    return pairs


def search_pairs_through_set(array, n):
    """
    алгоритм поиска уникальных пар сумма которых равна n. O(3*n).
    дополнительная память в размере множества от array.
    """
    pairs = []
    numbers = set(array)
    checked = set()  # обеспечивает уникальность
    for number in numbers:
        if n - number in numbers and number not in checked:
            pairs.append((number, n - number))
            checked.add(number)
            checked.add(n - number)
    if n % 2 == 0:  # для четного n добавляется пара (n//2, n//2)
        count = 0
        for a in array:
            if count == 2:
                pairs.append((n//2, n//2))
                break
            if a == n//2:
                count += 1
    print(pairs)
    return pairs


def test_search_pairs(func):
    # положительные целые
    func([1, 2, 6, 5, 3, 4, 7, 8, 3, 2], 5) == [(1, 4), (2, 3)]
    # отрицательные целые
    func([1, 6, -6, 3, 4, 7, 8, 3, 2, 11], -5) == [(1, -6)]
    # четное n
    func([-3, -2, 3, -5, 7, 8, 10, -6, 11, 2, 2], 4) == [(2, 2), (7, -3), (10, -6)]
    # n = 0
    func([-3, -2, 3, -5, 7, 8, 10, -6, 11], 0) == [(3, -3)]


test_search_pairs(search_pairs_two_cycles)
test_search_pairs(search_pairs_through_set)
