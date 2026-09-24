import math

DATA = [
    ("Аганин", 7),
    ("Агапонов", 2),
    ("Арсеньев", 2),
    ("Арутюнян", 1),
    ("Буренкова", 7),
    ("Гайдадина", 2),
    ("Голышев", 2),
    ("Горюшин", 6),
    ("Гутче", 1),
    ("Данилов", 1),
    ("Добраницкий", 1),
    ("Дудка", 2),
    ("Елистратов", 1),
    ("Зезюкин", 1),
    ("Колегов", 1),
    ("Конышков", 1),
    ("Корякин", 2),
    ("Косарев", 1),
    ("Край", 1),
    ("Лоскутников", 1),
    ("Мишин", 11),
    ("Морозов", 1),
    ("Новоселов", 1),
    ("Сауткина", 2),
    ("Сафин", 2),
    ("Светличный", 1),
    ("Смоленский", 2),
    ("Снигир", 2),
    ("Степанов", 2),
    ("Сушков", 1),
    ("Труханова", 1),
    ("Шиков", 2),
    ("Широков", 1),
]


def shapley_shubik(weights, quota):
    n = len(weights)
    fact = [math.factorial(k) for k in range(n + 1)]
    phi = [0.0] * n

    for i in range(n):
        w_i = weights[i]
        others = weights[:i] + weights[i + 1:]
        m = len(others)
        maxw = sum(others)

        dp = [[0] * (maxw + 1) for _ in range(m + 1)]
        dp[0][0] = 1
        for wt in others:
            for s in range(m - 1, -1, -1):
                row, nextrow = dp[s], dp[s + 1]
                for wsum in range(maxw - wt, -1, -1):
                    c = row[wsum]
                    if c:
                        nextrow[wsum + wt] += c

        pivot_sum = 0.0
        lo = max(0, quota - w_i)
        hi = min(maxw, quota - 1)
        for s in range(m + 1):
            if lo <= hi:
                cnt = sum(dp[s][lo:hi + 1])
                pivot_sum += fact[s] * fact[n - 1 - s] * cnt
        phi[i] = pivot_sum / fact[n]

    return phi


if __name__ == "__main__":
    names = [d[0] for d in DATA]
    weights = [d[1] for d in DATA]
    total = sum(weights)

    quota = total // 2 + 1

    print(f"Игроков: {len(weights)}, суммарный вес: {total}, кворум: {quota}\n")

    phi = shapley_shubik(weights, quota)
    print(f"Сумма индексов (проверка) = {sum(phi):.6f}\n")

    results = sorted(zip(names, weights, phi), key=lambda x: -x[2])
    print(f"{'Игрок':<15}{'Голоса':>7}{'SSI':>10}{'  (%)':>9}")
    for name, w, p in results:
        print(f"{name:<15}{w:>7}{p:>10.5f}{p*100:>8.2f}%")