from functools import reduce
import numpy as np


# return matrix_ci
def Ci(I, n, s):
    matrix_ci = np.zeros((n, n * (s + 1)))
    for _ in range(n):
        matrix_ci[_][I * n + _] = 1
    return matrix_ci

# return F, Psi, H, R, x0, u
def initVariables(tetta, mode):
    if mode == 2:
        F = np.array([[-0.8, 1.0], [tetta[0], 0]])
        Psi = np.array([[tetta[1]], [1.0]])
        H = np.array([[1.0, 0]])
        R = np.array([[0.1]])
        x0 = np.zeros((n, 1))
        u = np.zeros((N, 1))
        for i in range(N):
            u[i] = 1.0
    if mode == 1:
        F = np.array([[0]])
        Psi = np.array([[tetta[0], tetta[1]]])
        H = np.array([[1.0]])
        R = np.array([[0.3]])
        x0 = np.zeros((n, 1))
        u = np.array([[[2], [1]], [[1], [2]]])
    return F, Psi, H, R, x0, u


# return dF, dPsi, dH, dR, dx0
def initGraduates(mode):
    if mode == 2:
        dF = [np.array([[0, 0], [1, 0]]), np.array([[0, 0], [0, 0]])]
        dPsi = [np.array([[0], [0]]), np.array([[1], [0]])]
        dH = [np.array([[0, 0]]), np.array([[0, 0]])]
        dR = [np.array([[0]]), np.array([[0]])]
        dx0 = [np.zeros((n, 1)) for i in range(s)]
        du_dua = 1
    elif mode == 1:
        dF = [np.array([[0]]), np.array([[0]])]
        dPsi = [np.array([[1, 0]]), np.array([[0, 1]])]
        dH = [np.array([[0]]), np.array([[0]])]
        dR = [np.array([[0]]), np.array([[0]])]
        dx0 = [np.zeros((n, 1)) for i in range(s)]
        du_dua = np.array([[[1], [0]], [[0], [1]]])
    return dF, dPsi, dH, dR, dx0, du_dua


# Здесь можно проверять сразу основную лабу(mode=2) и 6 пункт из контрольных вопросов(mode=1). При смене mode не забывай менять n
def IMF(tetta):
    mode = n
    F, Psi, H, R, x0, u = initVariables(tetta, mode=mode) # mode - задание, которое мы сейчас отрабатываем. 0 - обычная лаба(n==2), 1 - пункт 6 2 лр(n==1),
    dF, dPsi, dH, dR, dx0, du_dua = initGraduates(mode=mode)
    Fa = np.zeros((n * (s + 1), n * (s + 1)))

    ####################_____2 пункт____________##############
    # Заполняем матрицу Fa (вертикальные элементы)
    for i in range(n):
        for j in range(n):
            Fa[i][j] = F[i][j]

    for _ in range(s):
        for i in range(n):
            for j in range(n):
                Fa[_*n + n + i][j] = dF[_][i][j]

    # Заполняем матрицу Fa (диагональные элементы)
    for _ in range(s):
        for i in range(n):
            for j in range(n):
                Fa[_*n + n + i][_*n + n + j] = F[i][j]

    # Определение PsiA
    PsiA = np.zeros((n * (s + 1), len(Psi[0])))

    # Заполнение первых двух элементов PsiA значениями из Psi
    for i in range(len(Psi)):
        for j in range(len(Psi[0])):
            PsiA[i][j] = Psi[i][j]

    # Заполнение остальных элементов PsiA значениями из dPsi
    for _ in range(s):
        for i in range(len(Psi)):
            for j in range(len(Psi[0])):
                PsiA[_*n + n + i][j] = dPsi[_][i][j]

    ####################_____3 пункт____________##############
    # Инициализация Матрицы Фишера
    delta_M = np.zeros((2, 2))

    # Инициализация Xatk



    # Инициализация всего, чтобы сымитировать производную
    M1 = np.zeros((2, 2))
    M2 = M1
    for _ in range(N):
        u[_] = u[_] + delta

    ####################_____4, 5, 6 пункты____________##############
    # Расчёт матрицы Фишера
    for _ in range(2):
        Xa_tk_plus_one = np.zeros((n * (s + 1), 1))
        Xa_tk = np.zeros((n * (s + 1), 1))
        M = N / 2. * (dR[0] * pow(R, -1) * dR[1] * pow(R, -1))
        for k in range(N):
            # Расчёт первого значения для Xa_tk, k == 0:
            if n >= 2:
                if k == 0:
                    x_0 = np.matmul(F, x0) + np.dot(Psi, u[k][0])
                    x_1 = np.matmul(dF[0], x0) + np.matmul(F, dx0[0]) + np.dot(dPsi[0], u[k][0])
                    x_2 = np.matmul(dF[1], x0) + np.matmul(F, dx0[1]) + np.dot(dPsi[1], u[k][0])
                    Xa_tk_plus_one = np.concatenate((x_0, x_1, x_2))


                # Расчёт последующих значений для Xa_tk, k > 0:
                if k > 0:
                    Xa_tk_plus_one = np.matmul(Fa, Xa_tk) + np.dot(PsiA, u[k][0])
                # print("\nXa_tk_plus_one\n", Xa_tk_plus_one)
            elif n == 1:
                if k == 0:
                    x_0 = np.matmul(F, x0) + np.dot(Psi, u[k])
                    x_1 = np.matmul(dF[0], x0) + np.matmul(F, dx0[0]) + np.dot(dPsi[0], u[k])
                    x_2 = np.matmul(dF[1], x0) + np.matmul(F, dx0[1]) + np.dot(dPsi[1], u[k])
                    Xa_tk_plus_one = np.concatenate((x_0, x_1, x_2))
                    # print(Xa_tk_plus_one)

                # Расчёт последующих значений для Xa_tk, k > 0:
                if k > 0:
                    Xa_tk_plus_one = np.matmul(Fa, Xa_tk) + np.dot(PsiA, u[k])
                    Xa_tk = Xa_tk_plus_one
            Xa_tk = Xa_tk_plus_one

            for i in range(2):
                for j in range(2):
                    A0 = reduce(np.dot, [dH[i], Ci(I=0, n=n, s=s),
                                         Xa_tk_plus_one, Xa_tk_plus_one.transpose(),
                                         Ci(I=0, n=n, s=s).transpose(), dH[j].transpose(), pow(R, -1)])
                    # print("A0_M2", A0)

                    A1 = reduce(np.dot, [dH[i], Ci(I=0, n=n, s=s),
                                         Xa_tk_plus_one, Xa_tk_plus_one.transpose(),
                                          Ci(I=j + 1, n=n, s=s).transpose(), H.transpose(), pow(R, -1)])
                    # print("A1_M2", A1)

                    A2 = reduce(np.dot, [H, Ci(I=i + 1, n=n, s=s),
                                         Xa_tk_plus_one, Xa_tk_plus_one.transpose(),
                                         Ci(I=0, n=n, s=s).transpose(), dH[j].transpose(), pow(R, -1)])
                    # print("A2_M2", A2)

                    A3 = reduce(np.dot, [H, Ci(I=i + 1, n=n, s=s),
                                         Xa_tk_plus_one, Xa_tk_plus_one.transpose(),
                                         Ci(I=j + 1, n=n, s=s).transpose(), H.transpose(), pow(R, -1)])
                    # print("A3_M2", A3)
                    delta_M[i][j] = A0 + A1 + A2 + A3
            M = np.add(M, delta_M)
        print("\nM[",_,"]", M)
        if _ == 0:
            M1 = M
            for _ in range(N):
                u[_] = 1.
        elif _ == 1:
            M2 = M

    print("\nDerivative:\n", (M1 - M2) / delta)



def dIMF(tetta):
    ####################_____1 пункт____________##############
    mode = n
    F, Psi, H, R, x0, u = initVariables(tetta, mode=mode)
    dF, dPsi, dH, dR, dx0, du_dua = initGraduates(mode=mode)
    Fa = np.zeros((n * (s + 1), n * (s + 1)))

    # Заполняем матрицу Fa (вертикальные элементы)
    for i in range(n):
        for j in range(n):
            Fa[i][j] = F[i][j]

    for _ in range(s):
        for i in range(n):
            for j in range(n):
                Fa[_ * n + n + i][j] = dF[_][i][j]

    # Заполняем матрицу Fa (диагональные элементы)
    for _ in range(s):
        for i in range(n):
            for j in range(n):
                Fa[_ * n + n + i][_ * n + n + j] = F[i][j]

    # Определение PsiA
    PsiA = np.zeros((n * (s + 1), len(Psi[0])))

    # Заполнение первых двух элементов PsiA значениями из Psi
    for i in range(len(Psi)):
        for j in range(len(Psi[0])):
            PsiA[i][j] = Psi[i][j]

    # Заполнение остальных элементов PsiA значениями из dPsi
    for _ in range(s):
        for i in range(len(Psi)):
            for j in range(len(Psi[0])):
                PsiA[_ * n + n + i][j] = dPsi[_][i][j]

    ####################_____2 пункт____________##############
    dMdu = [np.zeros((2, 2)) for alpha in range(r) for betta in range(N)]
    # Psi_du_dua_betta = [np.zeros((6, 1)) for alpha in range(r)]
    if mode == 2:
        dxa_tk_plus_one_dua_tbetta = [np.zeros((6, 1)) for alpha in range(r) for betta in range(N)]
        dxa_tk_dua_tbetta = [np.zeros((6, 1)) for alpha in range(r) for betta in range(N)]
    elif mode == 1:
        dxa_tk_plus_one_dua_tbetta = [np.zeros((3, 1)) for alpha in range(r) for betta in range(N)]
        dxa_tk_dua_tbetta = [np.zeros((3, 1)) for alpha in range(r) for betta in range(N)]

    delta_M = np.zeros((2, 2))

    # Инициализация Xatk
    Xa_tk_plus_one = np.zeros((n * (s + 1), 1))
    Xa_tk = np.zeros((n * (s + 1), 1))

    # Определяю размерности для Psi_du_dua_betta dxa_tk_dua_tbetta
    Psi_du_dua_betta = PsiA

    for k in range(N):
        count = 0
        ####################_____4 пункт____________##############
        if n == 2:
            if k == 0:
                x_0 = np.matmul(F, x0) + np.dot(Psi, u[k][0])
                x_1 = np.matmul(dF[0], x0) + np.matmul(F, dx0[0]) + np.dot(dPsi[0], u[k][0])
                x_2 = np.matmul(dF[1], x0) + np.matmul(F, dx0[1]) + np.dot(dPsi[1], u[k][0])
                Xa_tk_plus_one = np.concatenate((x_0, x_1, x_2))
                # print(Xa_tk_plus_one)

            # Расчёт последующих значений для Xa_tk, k > 0:
            if k > 0:
                Xa_tk_plus_one = np.matmul(Fa, Xa_tk) + np.dot(PsiA, u[k][0])

        elif n == 1:
            if k == 0:
                x_0 = np.matmul(F, x0) + np.dot(Psi, u[k])
                x_1 = np.matmul(dF[0], x0) + np.matmul(F, dx0[0]) + np.dot(dPsi[0], u[k])
                x_2 = np.matmul(dF[1], x0) + np.matmul(F, dx0[1]) + np.dot(dPsi[1], u[k])
                Xa_tk_plus_one = np.concatenate((x_0, x_1, x_2))
                # print(Xa_tk_plus_one)

            # Расчёт последующих значений для Xa_tk, k > 0:
            if k > 0:
                Xa_tk_plus_one = np.matmul(Fa, Xa_tk) + np.dot(PsiA, u[k])
        Xa_tk = Xa_tk_plus_one

        ####################_____5,6 пункт____________##############
        for betta in range(N):
            for alpha in range(r):
                if mode == 1:
                    if betta == k:
                        Psi_du_dua_betta = np.dot(PsiA, du_dua[alpha])
                    else:
                        Psi_du_dua_betta = np.dot(PsiA, [[0], [0]])
                elif mode == 2:
                    if betta == k:
                        Psi_du_dua_betta = PsiA
                    else:
                        Psi_du_dua_betta = np.dot(PsiA, [[0]])

                if k == 0:
                    dxa_tk_plus_one_dua_tbetta[betta] = Psi_du_dua_betta

                else:
                    dxa_tk_plus_one_dua_tbetta[betta] = np.add(np.dot(Fa, dxa_tk_dua_tbetta[betta]), Psi_du_dua_betta)
                dxa_tk_dua_tbetta[betta] = dxa_tk_plus_one_dua_tbetta[betta]

                coeff_dxa_tk_plus_one = np.add(np.dot(dxa_tk_plus_one_dua_tbetta[betta], Xa_tk_plus_one.transpose()),
                                       np.dot(Xa_tk_plus_one, dxa_tk_plus_one_dua_tbetta[betta].transpose()))

                for i in range(2):
                    for j in range(2):
                        A0 = reduce(np.dot, [dH[i], Ci(I=0,n=n,s=s),
                                    coeff_dxa_tk_plus_one,
                                     Ci(I=0,n=n,s=s).transpose(), dH[j].transpose(), pow(R, -1)])
                        # print("A0", A0)

                        A1 = reduce(np.dot, [dH[i], Ci(I=0,n=n,s=s),
                                    coeff_dxa_tk_plus_one,
                                    Ci(I=j + 1,n=n,s=s).transpose(), H.transpose(), pow(R, -1)])
                        # print("A1", A1)

                        A2 = reduce(np.dot, [H, Ci(I=i + 1,n=n,s=s),
                                    coeff_dxa_tk_plus_one,
                                    Ci(I=0,n=n,s=s).transpose(), dH[j].transpose(), pow(R, -1)])
                        # print("A2", A2)

                        A3 = reduce(np.dot, [H, Ci(I=i + 1,n=n,s=s),
                                    coeff_dxa_tk_plus_one,
                                    Ci(I=j + 1,n=n,s=s).transpose(), H.transpose(), pow(R, -1)])
                        delta_M[i][j] = A0 + A1 + A2 + A3
                dMdu[count] = np.add(dMdu[count], delta_M)
                count += 1

    dMdu_count = np.zeros((2, 2))
    for i in range(r*N):
        dMdu_count += dMdu[i]
        # print("\nM[", i, "]\n",dMdu[i])
    print("\ndMdu_count:\n", dMdu_count)



if __name__ == '__main__':
    # Определение переменных
    m = q = v = nu = 1

    r = 2 # Количество начальных сигналов, альфа
    n = 1 # Размерность вектора х0
    s = 2 # Количество производных по тетта
    N = 2 # Число испытаний

    delta = 0.00001

    tetta_true = np.array([-1.5, 1.0])
    tetta_false = np.array([-2, 0.01])

    IMF(tetta_false)
    dIMF(tetta_false)
