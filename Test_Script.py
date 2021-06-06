# -*- coding: utf-8 -*-
"""
This script reports a bug in the total derivatives computation (or a
misunderstanding of the author's part)

@author: g.fiorello
"""
#### Imports

from openmdao.api import ExplicitComponent, Group, Problem, ScipyOptimizeDriver

#### Components definition

ref = 1

class comp_1(ExplicitComponent):

    def setup(self):
        self.add_input('a1')
        self.add_input('a2')
        self.add_output('b', ref = ref)
        self.declare_partials(['b'], ['a1', 'a2'])

    def compute(self, inputs, outputs):
        a1 = inputs['a1']
        a2 = inputs['a2']
        b = 2*a1*a2
        outputs['b'] = b

    def compute_partials(self, inputs, partials):
        a1 = inputs['a1']
        a2 = inputs['a2']
        partials['b', 'a1'] = 2*a2
        partials['b', 'a2'] = 2*a1



class comp_2(ExplicitComponent):

    def setup(self):
        self.add_input('b')
        self.add_output('c')
        self.declare_partials(['c'], ['b'])

    def compute(self, inputs, outputs):
        b = inputs['b']
        c = 2*b
        outputs['c'] = c

    def compute_partials(self, inputs, partials):
        partials['c', 'b'] = 2

#### Model construction

model = Group()
model.add_subsystem('comp_1', comp_1(), promotes = ['*'])
model.add_subsystem('comp_2', comp_2(), promotes = ['*'])

model.add_design_var('a1', lower = 0.5, upper = 1.5)
model.add_design_var('a2', lower = 0.5, upper = 1.5)

model.set_input_defaults('a1', val = 1.)
model.set_input_defaults('a2', val = 1.)

model.add_objective('c')

#### Test script

problem = Problem()
problem.model = model

problem.driver = ScipyOptimizeDriver()
problem.driver.options['optimizer'] = 'SLSQP'

problem.setup()
problem.set_solver_print(level=0)
problem.run_driver()

problem.check_totals()

