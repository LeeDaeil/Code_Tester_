"""
Newton Raphson 법을 사용한 근 계산기 (by Daeil Lee)

Ref
    1. https://www.codesansar.com/numerical-methods/newton-raphson-method-python-program.htm
    2. https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.newton.html
"""
import matplotlib.pylab as plt
import argparse
import numpy as np
import time

from random import randint
from sympy import *
from math import *


class NonLinearNewtonFun:
    def __init__(self, fun_list=str, x_r=str, omega=float, err=float, max_iter=int):
        """
        Non_linear Newton Raphson 법을 사용한 근 계산기

        :param fun_list: 'f1:x_1... , f2:x_3'
        :param x_r: 'x_1:1:1, x_2:3'
        :param omega:
        :param err:
        """
        # init part
        self._check_x_nub = self._find_x_nub(fun_list)
        self._x_range_info = self._find_x_range(x_r)
        self._x_fun_info = self._find_fun(fun_list)
        self._jacobian_info = self._find_jacobian()
        self._omega = omega
        self._error = err
        self._max_iter = max_iter

        self._run()

    def _find_x_nub(self, fun_list) -> int:
        """
        x_ 인자의 갯수를 파악

        :param fun_list:
        :return: x_ 인자의 갯수 e.x) return 2는 x_1, x_2 가 있다는 의미
        """
        count = 0
        while True:
            if f'x_{count + 1}' in fun_list:
                count += 1
            else:
                break
        return count

    def _find_x_range(self, x_r) -> dict:
        """
        x_r 정보를 받아서 x_ 인수로 분해 및 범위 내에서 Random으로 값을 추출

        :param x_r: 'x_1:1:1, x_2:3'
        :return: {'x_1': {'InitVal': False, 'InitXMin': '1', 'InitXMax': '3', 'FinVal:': 1, 'FinVal_list': []},
                 'x_2': {'InitVal': True, 'InitXMin': None, 'InitXMax': None, 'FinVal:': '3', 'FinVal_list': []}}
        """
        # 1. 식과 x_r의 x_ 인자가 동일하게 있는지 확인
        x_r_nun = self._find_x_nub(x_r)
        assert not self._check_x_nub != x_r_nun, f'함수내의 x_인자와 x_r의 x_ 인자가 동일하지 않습니다. ' \
                                                 f'fun:{self._check_x_nub} | x_r:{x_r_nun}'
        # 2. x_ 인자의 table 구성
        x_r_info = {}
        x_r_ = x_r.replace(' ', '').split(',')      # ['x_1:1:1', 'x_2:1:2']
        for _ in range(len(x_r_)):
            one_x_r_ = x_r_[_].split(':')
            if len(one_x_r_) == 2:                  # ['x_1:1'] 범위 없음, 초기값 세팅됨
                x_r_info[f'x_{_ + 1}'] = {'InitVal': True,  'InitXMin': None, 'InitXMax': None,
                                          'FinVal': int(one_x_r_[1]),
                                          'FinVal_list': []}
            if len(one_x_r_) == 3:                  # ['x_1:1:2'] 범위 존재
                assert not int(one_x_r_[1]) >= int(one_x_r_[2]), f'x_min {one_x_r_[1]} 값은 ' \
                                                                 f'x_max {one_x_r_[2]} 보다 커야합니다.'
                x_r_info[f'x_{_ + 1}'] = {'InitVal': False, 'InitXMin': int(one_x_r_[1]), 'InitXMax': int(one_x_r_[2]),
                                          'FinVal': randint(int(one_x_r_[1]), int(one_x_r_[2])),
                                          'FinVal_list': []}
            x_r_info[f'x_{_ + 1}']['FinVal_list'].append(x_r_info[f'x_{_ + 1}']['FinVal'])
        return x_r_info

    def _find_fun(self, fun_list) -> dict:
        """
        입력된 fun을 dict로 변환하여, 'Eq'와 Lambda 함수로 반환

        :param fun_list:
        :return: {'f1': {'Eq': 'x_1*3+x_2*2', 'F': 3*x_1 + 2*x_2}, 'f2': {'Eq': 'x_2**2', 'F': x_2**2}}
                 ** 'F'의 타입은 spmpify.
        """
        # 1. 함수 분할
        fun_list_ = fun_list.replace(' ', '').split(',')    # 공백 제거 후 f1, f2 로 분할
                                                            # {'f1': 'x_1*3+x_2*2', 'f2': 'x_2**2'}
        fun_list_ = {f'{f.split(":")[0]}': f.split(":")[1] for f in fun_list_}
        # 2. warp
        for key in fun_list_.keys():
            fun_list_[key] = {'Eq': fun_list_[key], 'F': sympify(fun_list_[key]) }
        print(fun_list_)
        return fun_list_

    def _find_jacobian(self) -> list:
        """
        Jacobian table을 작성함.

        :return: {'f1': 'x_1*3+x_2*2', 'f2': 'x_2**2'} --> [[3, 2], [0, 2*x_2]]
        """
        J_table = []
        for Eq in self._x_fun_info.keys():          # 함수의 수
            J_table_row = []
            for x_ in range(self._check_x_nub):     # 인자의 수
                dif_eq = diff(self._x_fun_info[Eq]['Eq'], f'x_{x_ + 1}')    # 인자에 대한 함수를 미분
                J_table_row.append(dif_eq)
            J_table.append(J_table_row)
        return J_table

    def _cal_jacobinan_table(self) -> np.array:
        """
        현재 x_ 인자의 FinVal 값을 통해 Table의 값을 계산

        :return: [[3. 2.] [0. 6.]]
        """
        J_cal_table = []
        get_x_val = [(Val_name, self._x_range_info[Val_name]['FinVal']) for Val_name in self._x_range_info.keys()]
        for Eq, j in zip(self._x_fun_info.keys(), range(len(self._x_fun_info.keys()))):  # 함수의 수
            J_cal_table_row = []
            for x_ in range(self._check_x_nub):  # 인자의 수
                J_cal_table_row.append(float(self._jacobian_info[j][x_].subs(get_x_val)))
            J_cal_table.append(J_cal_table_row)
        print(np.array(J_cal_table))
        return np.array(J_cal_table)

    def _cal_fun_table(self) -> np.array:
        """
        현재 x_ 인자에 대한 fun 함수의 y 값 계산

        :return: [12 9]
        """
        get_x_val = [(Val_name, self._x_range_info[Val_name]['FinVal']) for Val_name in self._x_range_info.keys()]
        get_y = [self._x_fun_info[_]['F'].subs(get_x_val) for _ in self._x_fun_info.keys()]
        return np.array(get_y)

    def _run(self):
        while True:
            # 1. 초기 값에 계산
            f = self._cal_fun_table()       # [12 9 ...]
            out_ = - self._omega * np.dot(np.linalg.inv(self._cal_jacobinan_table()), f)
            # 2. x_ 인자 값 업데이트
            for i in range(len(out_)):
                self._x_range_info[f'x_{i + 1}']['FinVal'] += out_[i]
                self._x_range_info[f'x_{i + 1}']['FinVal_list'].append(self._x_range_info[f'x_{i + 1}']['FinVal'])
            print([self._x_range_info[f'x_{i + 1}']['FinVal'] for i in range(len(out_))])

            # 3. 종료
            if len(self._x_range_info[f'x_1']['FinVal_list']) > 2:
                Trig = False
                # Error 기반
                Trig_count = 0
                for i in range(len(out_)):
                    if abs(self._x_range_info[f'x_{i + 1}']['FinVal_list'][-1] -
                           self._x_range_info[f'x_{i + 1}']['FinVal_list'][-2]) < self._error: Trig_count += 1
                if Trig_count == len(out_): break

                # Max iter 선택시
                if self._max_iter != 0 and len(self._x_range_info[f'x_1']['FinVal_list']) > self._max_iter:
                    Trig = True

                if Trig:
                    break

    def plot(self):
        for i in range(self._check_x_nub):
            plt.plot(self._x_range_info[f'x_{i + 1}']['FinVal_list'], label=f'x_{i + 1}')
        plt.legend()
        plt.grid()
        plt.show()


parser = argparse.ArgumentParser(description='Newton Raphson법 사용한 근 계산기 (by Daeil Lee)')
parser.add_argument('-f', '--f', required=True,
                    help="함수식 List f(x) e.x) 'f1:x_1*2+x_2+3, f2:x_1**2'")
parser.add_argument('-r', '--xr', required=True,
                    help="x_range e.x) 범위시 'x_1:1:3', 초기값 Set-up시 'x_1:1'")
parser.add_argument('-o', '--o', type=float, required=True, help="omega")
parser.add_argument('-e', '--e', type=float, required=True, help="error")
parser.add_argument('-maxiter', '--maxiter', type=int, default=0, required=False, help="maxiter")
args = parser.parse_args()

out = NonLinearNewtonFun(fun_list=args.f, x_r=args.xr, omega=args.o, err=args.e, max_iter=args.maxiter)
out.plot()

