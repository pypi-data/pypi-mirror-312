#    ControLib. A Python package for advanced control systems design and deployment.
#    Copyright (C) 2024  Miguel Loureiro

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
This module contains the base class for state estimators.

Classes
-------
StateEstimator
    State estimator base class.
"""

from abc import ABC, abstractmethod
import numpy as np

class StateEstimator(ABC):

    def __init__(self, sampling_time: int | float, n_inputs: int | float, n_outputs: int | float) -> None:

        super().__init__();
        self._Ts = sampling_time;
        self._input_dim = n_inputs;
        self._output_dim = n_outputs;

        return;

    @abstractmethod
    def compute(self) -> np.ndarray:

        pass

    @abstractmethod
    def info(self) -> None:

        pass