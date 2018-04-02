#
# CoCoFunctionHaveRhs.py
#
# This file is part of NEST.
#
# Copyright (C) 2004 The NEST Initiative
#
# NEST is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# NEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NEST.  If not, see <http://www.gnu.org/licenses/>.
from pynestml.modelprocessor.CoCo import CoCo
from pynestml.modelprocessor.ASTNeuron import ASTNeuron
from pynestml.modelprocessor.ASTVisitor import ASTVisitor
from pynestml.utils.Logger import LOGGING_LEVEL, Logger
from pynestml.utils.Messages import Messages


class CoCoFunctionHaveRhs(CoCo):
    """
    This coco ensures that all function declarations, e.g., function V_rest mV = V_m - 55mV, have a rhs.
    """

    @classmethod
    def check_co_co(cls, node=None):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ASTNeuron
        """
        assert (node is not None and isinstance(node, ASTNeuron)), \
            '(PyNestML.CoCo.FunctionWithRhs) No or wrong type of neuron provided (%s)!' % type(node)
        node.accept(FunctionRhsVisitor())
        return


class FunctionRhsVisitor(ASTVisitor):
    """
    This visitor ensures that everything declared as function has a rhs.
    """

    def visit_declaration(self, node):
        """
        Checks if the coco applies.
        :param node: a single declaration.
        :type node: ASTDeclaration.
        """
        if node.is_function() and not node.has_expression():
            code, message = Messages.getNoRhs(node.get_variables()[0].get_name())
            Logger.logMessage(_errorPosition=node.get_source_position(), _logLevel=LOGGING_LEVEL.ERROR,
                              _code=code, _message=message)
        return
