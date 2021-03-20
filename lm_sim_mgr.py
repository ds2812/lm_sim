import pandas as pd
from lm_sim import lm_sim
import numpy as np
import yaml



class lm_sim_mgr():
    def __init__(self, checkout_per_day, engine_mode, person, time_slice):
        self.checkout_per_day = checkout_per_day
        self.engine_mode = engine_mode
        self.engine_person = person
        self.time_slice = time_slice
        self.lic = {}
        self.df_one_day = pd.DataFrame(
            columns=['user',
                     'user_host',
                     'display',
                     'version',
                     'server_host',
                     'port',
                     'handle',
                     'checkout_time',
                     'checkin_time',
                     'sim_duration',
                     'approved',
                     'processed'])

    def _resource_readin(self):
        """
        This is to read in the .yaml file as a part of config.
        :return:
        """
        with open(r'sim_mgr_config.yaml') as file:
            documents = yaml.full_load(file)
            for item, self.lic in documents.items():
                # Iterate out the yaml file
                pass
        print(self.lic['vmms'], self.lic['ciw'])

    def _update_df_inplace(self, df_candidate, col_name):
        row_to_update = []
        for i, row in df_candidate.iterrows():
            row_to_update.append(i)
        print(f'Row to update: {row_to_update}')
        self.df_one_day.loc[self.df_one_day.index.isin(row_to_update), col_name] = True

    def _lic_alloc_by_time_slice(self):
        """
        This is to slice time into second of time_slice slices (for now)
        :return:
        """
        # Use 24 hrs for now, can be updated in the future.
        curr_slice = 0 * 3600
        max_sec = 24 * 3600
        slice_step = 3600
        while curr_slice < max_sec:
            # Only process data with 'processed = False'
            mask = (self.df_one_day['checkout_time'] >= curr_slice) & (
                    self.df_one_day['checkout_time'] < curr_slice + slice_step)

            df_mask = self.df_one_day[mask]
            self._update_df_inplace(df_candidate=df_mask, col_name='processed')
            df_temp = self.df_one_day[mask].head(self.lic['vmms'])
            self._update_df_inplace(df_candidate=df_temp, col_name='approved')
            curr_slice += slice_step

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
                self.df_one_day.loc[i] = [l_user,
                                          l_user_host,
                                          l_display,
                                          l_version,
                                          l_server_host,
                                          l_port,
                                          l_handle,
                                          lm_sim_inst.checkout_time,
                                          lm_sim_inst.checkin_time,
                                          lm_sim_inst.sim_duration,
                                          False,
                                          False]

    def lmstat_query(self):
        pass
