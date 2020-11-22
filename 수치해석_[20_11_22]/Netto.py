"""
Newton Raphson 법을 사용한 근 계산기 (by Daeil Lee)

Ref
    1. https://www.codesansar.com/numerical-methods/newton-raphson-method-python-program.htm
    2. https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.newton.html
"""
import matplotlib.pylab as plt
import argparse
from math import *


class NewtonRaphsonFun:
    def __init__(self, fun=object, x_min=float, x_max=float, err=float):
        """
        이분법을 사용한 근 계산기

        :param fun: lambda 함수로 작성된 함수를 사용하거나 def 로 작성된 함수 사용
                    (e.x)
                        def fun(x):
                            y = x ** 2 + x
                            return y
        :param x_min: x의 최소 범위
        :param x_max: x의 최대 범위
        :param err: error 범위
        """
        # init part
        self._get_fun = fun
        self._get_x_min = x_min
        self._get_x_max = x_max
        self._get_error = err

        self._x_min = float(x_min)             # _step 진행 시 업데이트
        self._x_max = float(x_max)             # _step 진행 시 업데이트
        self._x_mid = 0

        self._info = {'x_start_min': self._get_x_min,       'x_min_list': [],
                      'x_start_max': self._get_x_max,       'x_max_list': [],
                      'x_start_mid': self._x_mid,           'x_mid_list': [],
                      'iter': 0,                            'iter_list': [],
                      'root': 0,}

        # assert part
        assert not x_min >= x_max, 'x_min 값은 x_max 보다 커야합니다.'
        assert fun(x_min) * fun(x_max) < 0, f'[{x_min}~{x_max}] 구간 사이에 근이 없습니다.'

        self._run()

    def _log(self):
        self._info['x_min_list'].append(self._x_min)
        self._info['x_max_list'].append(self._x_max)
        self._info['x_mid_list'].append(self._x_mid)
        self._info['iter_list'].append(self._info['iter'])
        self._info['root'] = self._x_mid
        self._info['iter'] += 1

    def _run(self):
        while True:
            # 1. 중간 값 도출
            self._x_mid = (self._x_min + self._x_max) / 2
            # 2. Search 시작
            if self._get_fun(self._x_min) * self._get_fun(self._x_mid) < 0:
                self._x_max = self._x_mid
            else:
                self._x_min = self._x_mid

            # -. logger
            self._log()

            # 3. err 보다 작으면 종료
            if abs(self._get_fun(self._x_mid)) < self._get_error: break

        print('Done!')

    def get_info(self):
        print(f"Root {self._info['root']} | Iter {self._info['iter']} |")
        return 0

    def plot(self):
        plt.plot(self._info['x_min_list'], label='Min')
        plt.plot(self._info['x_mid_list'], label='Mid')
        plt.plot(self._info['x_max_list'], label='Max')
        plt.legend()
        plt.grid()
        plt.show()


parser = argparse.ArgumentParser(description='이분법 사용한 근 계산기 (by Daeil Lee)')
parser.add_argument('--fun', type=str, required=True, help="함수식 f(x)")
parser.add_argument('--xmin', type=float, required=True, help="x min")
parser.add_argument('--xmax', type=float, required=True, help="x max")
parser.add_argument('--err', type=float, required=True, help="error")
args = parser.parse_args()

# 문자열 식을 함수로 변환
def fun_(eq=str): return lambda x: eval(eq)

bisec = BisectionFun(fun=fun_(args.fun), x_min=args.xmin, x_max=args.xmax, err=args.err)
bisec.get_info()
bisec.plot()
