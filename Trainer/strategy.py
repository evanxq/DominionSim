

# 32 cards to buy (all of first set except one kind)
CARDS = (
    'Copper', 'Silver', 'Gold',
    'Estate', 'Duchy', 'Province',
    # 'Curse',
    'Artisan', 'Bandit', 'Bureaucrat', 'Cellar', 'Chapel', 'Council_Room',
    'Festival', 'Harbinger', 'Laboratory', 'Library', 'Market', 'Merchant',
    'Militia', 'Mine', 'Moat', 'Moneylender', 'Poacher', 'Remodel', 'Sentry',
    'Smithy', 'Throne_Room', 'Vassal', 'Village', 'Witch', 'Workshop',
    'Gardens'
)

# 16 functions
FUNCTIONS = (
    'constant', 'countCardsInDeck', 'countCardsInSupply',
    'gainsNeededToEndGame', 'countAvailableMoney', 'countAllCardsInDeck',
    'countTurns', 'countEmptyPiles', 'countBuysLeft',
    'getTotalMoney', 'countCardsLeftInDrawDeck', 'countCardsLeftInSmallestPile',
    'countCardsInPlay', 'countCardsInHand', 'countVP',
    'countMAXOpponentVP'
)

N_PRIORITY_BITS = 5
N_FUNC_BITS = 4
N_ATTR_BITS = 5
N_COMPARE_BITS = 1
N_BUY_CONDITION_BITS = N_PRIORITY_BITS + N_COMPARE_BITS + 2*(N_FUNC_BITS + N_ATTR_BITS)
N_VECTOR_BITS = pow(2, N_ATTR_BITS) * N_BUY_CONDITION_BITS


class Strategy:
    id_counter = 0

    def __init__(self, vec):
        if len(vec) != N_VECTOR_BITS:
            print("Error: vector is the wrong size. Wanted %d, got %d"
                  % (N_VECTOR_BITS, len(vec)))
            return

        self.name = str(Strategy.id_counter)
        Strategy.id_counter += 1

        self.conditions = []
        for i in range(len(CARDS)):
            start = N_BUY_CONDITION_BITS*i
            end = start + N_BUY_CONDITION_BITS
            self.conditions.append(BuyCondition(i, vec[start:end]))

    def xml(self):
        out = '<player name="%s">' % self.name
        for c in self.conditions:
            out += c.xml()
        out += '</player>'
        return out


class BuyCondition:
    def __init__(self, cardIndex, subvec):
        if len(subvec) != N_BUY_CONDITION_BITS:
            print("Error: sub-vector %d is the wrong size. Wanted %d, got %d"
                  % (cardIndex, N_BUY_CONDITION_BITS, len(subvec)))
            return

        self.name = CARDS[cardIndex]

        self.priority = int(subvec[:N_PRIORITY_BITS], 2)
        i = N_PRIORITY_BITS

        index = int(subvec[i: i + N_FUNC_BITS], 2)
        self.func1 = FUNCTIONS[index]
        i += N_FUNC_BITS

        index = int(subvec[i: i + N_ATTR_BITS], 2)
        self.attr1 = CARDS[index] if self.func1 != FUNCTIONS[0] else str(index)
        i += N_ATTR_BITS

        index = int(subvec[i: i + N_COMPARE_BITS], 2)
        self.comparison = 'smallerThan' if index == 0 else 'greaterThan'
        i += N_COMPARE_BITS

        index = int(subvec[i: i + N_FUNC_BITS], 2)
        self.func2 = FUNCTIONS[index]
        i += N_FUNC_BITS

        index = int(subvec[i: i + N_ATTR_BITS], 2)
        self.attr2 = CARDS[index] if self.func2 != FUNCTIONS[0] else str(index)
        i += N_ATTR_BITS

    def xml(self):
        return (('<buy name="%s"><condition><left type="%s" attribute="%s"/>'
               + '<operator type="%s"/><right type="%s" attribute="%s"/></condition></buy>')
               % (self.name, self.func1, self.attr1, self.comparison, self.func2, self.attr2))
