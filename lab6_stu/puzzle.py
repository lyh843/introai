from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave"
knowledge0 = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "I am a knave, but B isn't."
knowledge1 = And(
    Biconditional(AKnave, Not(AKnight)),
    Biconditional(BKnave, Not(BKnight)),
    Biconditional(AKnight, And(AKnave, BKnight))
)

# Puzzle 2
# A says "We are both knaves."
# B says nothing.
knowledge2 = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 3
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge3 = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Biconditional(BKnight, Or(And(BKnight, AKnave), And(BKnave, AKnight)))
)

# Puzzle 4
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge4 = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),
    Or(Biconditional(AKnight, AKnight), Biconditional(AKnight, AKnave)),
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    Biconditional(BKnight, CKnave),
    Biconditional(CKnight, AKnight)
)

# Puzzle 5
# I asked A "How many knights are there among you?"
# A answered indistinctly.
# B said "A said 'There's only one'"
# C said "B is lying."
knowledge5 = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),
    Biconditional(BKnight, Biconditional(AKnight, Or(And(AKnight, BKnave, CKnave), And(AKnave, BKnight, CKnave), And(AKnave, BKnave, CKnight)))),
    Biconditional(CKnight, Not(Or(BKnave, CKnave)))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
        ("Puzzle 4", knowledge4),
        ("Puzzle 5", knowledge5),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
