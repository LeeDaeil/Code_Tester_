"""
이분법 사용한 근 계산기 (by Daeil Lee)

Ref
    1. https://stackoverflow.com/questions/14392208/how-to-do-the-bisection-method-in-python
    2. https://github.com/rursvd/pynumerical2/blob/master/8_2.py
"""
import matplotlib.pylab as plt


class BisecFun:
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
                      'iter': 0,                            'iter_list': [],}

        # assert part
        assert not x_min >= x_max, 'x_min 값은 x_max 보다 커야합니다.'
        assert fun(x_min) * fun(x_max) < 0, f'[{x_min}~{x_max}] 구간 사이에 근이 없습니다.'

        self._run()

    def _log(self):
        self._info['x_min_list'].append(self._x_min)
        self._info['x_max_list'].append(self._x_max)
        self._info['x_mid_list'].append(self._x_mid)
        self._info['iter_list'].append(self._info['iter'])
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
        return print(self._info)

    def plot(self):
        plt.plot(self._info['x_min_list'], label='Min')
        plt.plot(self._info['x_mid_list'], label='Mid')
        plt.plot(self._info['x_max_list'], label='Max')
        plt.legend()
        plt.grid()
        plt.show()


if __name__ == '__main__':
    bisec = BisecFun(fun=lambda x: x + 1, x_min=-10, x_max=10, err=0.0001)
    bisec.get_info()
    bisec.plot()
