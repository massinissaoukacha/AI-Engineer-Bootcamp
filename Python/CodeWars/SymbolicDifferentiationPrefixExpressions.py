import re

def diff(s: str) -> str:
    """
    Dérive une expression préfixe (variable x) et simplifie:
      - retrait des 0/1 dans * et /
      - évaluation des constantes (+ - * / ^)
      - (^ a 0) -> 1 sauf (^ 0 0), (^ a 1) -> a
      - NE RÉORDONNE PAS les sommes: (+ a b) conserve l'ordre d'entrée
      - produits: normalisation stable (voir build_mul_from_factors)
      - (* (/ 1 D) c) -> (/ c D) et commuté
      - division constante -> entier si possible, sinon décimal minimal (ex: 2/4 -> 0.5)
    Opérations/fonctions: + - * / ^ sin cos tan exp ln
    """

    # ---------- Tokenizer ----------
    def tokenize(s):
        s = s.replace('(', ' ( ').replace(')', ' ) ')
        return [t for t in s.split() if t]

    # ---------- Parser ----------
    def parse(tokens):
        tok = tokens.pop(0)
        if tok == '(':
            lst = []
            while tokens[0] != ')':
                lst.append(parse(tokens))
            tokens.pop(0)
            return lst
        elif tok == ')':
            raise ValueError('Unexpected )')
        else:
            if re.fullmatch(r'-?\d+', tok):
                return int(tok)
            if re.fullmatch(r'-?\d+\.\d+', tok):
                return float(tok)
            return tok

    # ---------- Printer ----------
    def num_to_str(n):
        if isinstance(n, int):
            return str(n)
        if isinstance(n, float):
            if n.is_integer():
                return str(int(n))
            return format(n, '.15g')
        return str(n)

    def to_str(node):
        if isinstance(node, (int, float)):
            return num_to_str(node)
        if isinstance(node, str):
            return node
        return '(' + ' '.join(to_str(x) for x in node) + ')'

    # ---------- Utils ----------
    def is_num(x): return isinstance(x, (int, float))
    def is_zero(x): return is_num(x) and x == 0
    def is_one(x): return is_num(x) and x == 1

    def as_int_if_whole(x):
        return int(x) if isinstance(x, float) and x.is_integer() else x

    def fold(op, a, b):
        if not (is_num(a) and is_num(b)):
            return None
        if op == '^':
            if isinstance(a, int) and isinstance(b, int):
                if a == 0 and b == 0:
                    return None
                try:
                    return int(pow(a, b))
                except OverflowError:
                    return None
            return None
        if op == '+': return as_int_if_whole(a + b)
        if op == '-': return as_int_if_whole(a - b)
        if op == '*': return as_int_if_whole(a * b)
        if op == '/':
            if b == 0:
                return None
            return as_int_if_whole(a / b)
        return None

    def is_mul(node):
        return isinstance(node, list) and len(node) == 3 and node[0] == '*'

    # ---------- Construction produit canonique ----------
    def build_mul_from_factors(factors, const_factor):
        # zéro annule
        if is_zero(const_factor):
            return 0

        def pack_tail(rest, c):
            if not rest:
                return c if c != 1 else 1
            if len(rest) == 1:
                return rest[0] if c == 1 else ['*', c, rest[0]]
            return ['*', rest[0], pack_tail(rest[1:], c)]

        if not factors:
            return const_factor if const_factor != 1 else 1
        if len(factors) == 1:
            return factors[0] if const_factor == 1 else ['*', const_factor, factors[0]]
        right = pack_tail(factors[1:], const_factor)
        return ['*', factors[0], right]

    # ---------- Simplification ----------
    def simp(node):
        if isinstance(node, (int, float, str)):
            return node

        op = node[0]
        args = [simp(a) for a in node[1:]]

        # Fonctions unaires
        if op in ('sin', 'cos', 'tan', 'exp', 'ln'):
            return [op, args[0]]

        a, b = args[0], args[1]

        if op == '^':
            if is_num(b):
                if b == 0:
                    if a == 0:
                        return ['^', 0, 0]
                    return 1
                if b == 1:
                    return a
            val = fold('^', a, b)
            return val if val is not None else ['^', a, b]

        if op == '+':
            # Conserver l'ordre; juste gérer 0 et constants purs
            if is_zero(a): return b
            if is_zero(b): return a
            val = fold('+', a, b)
            if val is not None:
                return val
            return ['+', a, b]

        if op == '-':
            if is_zero(b): return a
            val = fold('-', a, b)
            return val if val is not None else ['-', a, b]

        if op == '*':
            if is_zero(a) or is_zero(b): return 0
            if is_one(a): return b
            if is_one(b): return a

            val = fold('*', a, b)
            if val is not None:
                return val

            # (* (/ 1 D) c) -> (/ c D) et commuté
            if isinstance(a, list) and a[0] == '/' and is_one(a[1]) and is_num(b):
                return simp(['/', b, a[2]])
            if isinstance(b, list) and b[0] == '/' and is_one(b[1]) and is_num(a):
                return simp(['/', a, b[2]])

            # Aplatir pour collecter facteurs en conservant l'ordre relatif
            flat = []
            def flatten_mul(x):
                if is_mul(x):
                    flatten_mul(x[1]); flatten_mul(x[2])
                else:
                    flat.append(x)
            flatten_mul(a); flatten_mul(b)

            const = 1
            nonconst = []
            for f in flat:
                if is_num(f):
                    val = fold('*', const, f)
                    const = val if val is not None else const * f
                else:
                    nonconst.append(f)

            return build_mul_from_factors(nonconst, const)

        if op == '/':
            if is_zero(a): return 0
            if is_one(b): return a
            if is_num(a) and is_num(b):
                val = fold('/', a, b)
                if val is not None:
                    return val
            return ['/', a, b]

        return [op] + args

    def simplify(node):
        prev = None
        cur = node
        for _ in range(80):
            cur = simp(cur)
            if cur == prev:
                break
            prev = cur
        return cur

    # ---------- Diff ----------
    def d(node):
        if is_num(node):
            return 0
        if node == 'x':
            return 1
        if isinstance(node, str):
            return 0

        op = node[0]

        if op in ('sin', 'cos', 'tan', 'exp', 'ln'):
            u = simplify(node[1])
            du = simplify(d(u))
            if op == 'sin':
                return simplify(['*', ['cos', u], du])
            if op == 'cos':
                return simplify(['*', -1, ['*', ['sin', u], du]])
            if op == 'tan':
                return simplify(['*', ['/', 1, ['^', ['cos', u], 2]], du])
            if op == 'exp':
                return simplify(['*', ['exp', u], du])
            if op == 'ln':
                return simplify(['/', du, u])

        a, b = node[1], node[2]
        sa, sb = simplify(a), simplify(b)
        da, db = simplify(d(sa)), simplify(d(sb))

        if op == '+':
            return simplify(['+', da, db])
        if op == '-':
            return simplify(['-', da, db])
        if op == '*':
            return simplify(['+', ['*', da, sb], ['*', sa, db]])
        if op == '/':
            num = ['-', ['*', da, sb], ['*', sa, db]]
            den = ['^', sb, 2]
            return simplify(['/', simplify(num), simplify(den)])
        if op == '^':
            if isinstance(sb, (int, float)):
                n = sb
                # Préférence de forme: da d'abord, puis (* n (^ sa n-1))
                return simplify(['*', da, ['*', n, ['^', sa, n - 1]]])
            term1 = ['*', db, ['ln', sa]]
            term2 = ['/', ['*', sb, da], sa]
            return simplify(['*', ['^', sa, sb], ['+', simplify(term1), simplify(term2)]])

        return 0

    ast = parse(tokenize(s))
    return to_str(simplify(d(ast)))