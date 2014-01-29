
from pyretic.lib.corelib import *
from pyretic.lib.std import *

from pyretic.pyresonance.fsm_policy import *
from pyretic.pyresonance.drivers.json_event import JSONEvent
from pyretic.pyresonance.smv.translate import *


class ids(DynamicPolicy):
    def __init__(self):

       ### DEFINE THE FLEC FUNCTION

        def flec_fn(f):
            return match(srcip=f['srcip'])

        ## SET UP TRANSITION FUNCTIONS

        def infected_next(event):
            return event

        def policy_next(state):
            if state['infected']:
                return drop
            else:
                return identity

        ### SET UP THE FSM DESCRIPTION

        self.fsm_description = { 
            'infected' : (bool, 
                          False, 
                          NextFns(event_fn=infected_next)), 
            'policy'   : ([drop,identity],
                          identity,
                          NextFns(state_fn=policy_next)) }

        ### SET UP POLICY AND EVENT STREAMS

        fsm_pol = FSMPolicy(flec_fn,self.fsm_description)
        json_event = JSONEvent()
        json_event.register_callback(fsm_pol.event_handler)

        super(ids,self).__init__(fsm_pol)


def main():
    pol = ids()

    # For NuSMV
    mc = ModelChecker(pol)  

    return pol >> flood()
