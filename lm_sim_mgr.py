import pandas as pd
from lm_sim import lm_sim
import numpy as np
import yaml


class lm_sim_mgr():
    def __init__(self, checkout_per_day):
        self.checkout_per_day = checkout_per_day
        self.df_one_day = pd.DataFrame(
            columns=['user', 'user_host', 'display', 'version', 'server_host', 'port', 'handle', 'checkout_time', 'checkin_time', 'sim_duration',
                     'approved'])


    def _run_one_day(self):
        """
        Generates one day of simulated checkouts.
        :return:
        """
        one_day_db = []
        [l_user, l_user_host, l_display, l_version, l_server_host, l_port, l_handle] = np.ones(7)
        for i in range(self.checkout_per_day):
            lm_sim_inst = lm_sim(engine_mode='design', person='design')
            if lm_sim_inst.valid:
                one_day_db.append(lm_sim_inst.checkin_time / 3600)
            if lm_sim_inst.valid:
                self.df_one_day.loc[i] = [l_user, l_user_host, l_display, l_version, l_server_host, l_port, l_handle, lm_sim_inst.checkout_time, lm_sim_inst.checkin_time, lm_sim_inst.sim_duration, True]