import pandas as pd
from lm_sim import lm_sim
import numpy as np
import yaml
import datetime
from datetime import datetime as dt
import time
import calendar
import random


def _convert_time_to_sec(time_to_convert):
    x = time.strptime(str(time_to_convert).split(',')[0], '%H:%M:%S')
    sec_out = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
    return sec_out

def _convert_date_to_day_month(date_to_convert):
    my_date = dt.strptime(date_to_convert, "%Y_%m_%d")
    rtn_string = []
    rtn_string.append(calendar.day_abbr[my_date.weekday()])
    return rtn_string[0], my_date


class lm_sim_mgr():
    def __init__(self, checkout_per_day, engine_mode, person, time_slice, lic_to_assign):
        self.checkout_per_day = checkout_per_day
        self.engine_mode = engine_mode
        self.engine_person = person
        self.lic = {}
        self.user = []
        self.time_slice = time_slice
        self.lic_to_assign = lic_to_assign
        self.df_one_day = pd.DataFrame(
            columns=['user',
                     'user_host',
                     'display',
                     'version',
                     'server_host',
                     'port',
                     'handle',
                     'lic_type',
                     'checkout_time',
                     'checkin_time',
                     'sim_duration',
                     'approved',
                     'processed'])

    def _resource_readin(self, yaml_file):
        """
        This is to read in the .yaml file as a part of config.
        :return:
        """
        with open(yaml_file) as file:
            documents = yaml.full_load(file)
            for item, dict in documents.items():
                if item == 'lic_type':
                    self.lic = dict
                elif item == 'user':
                    self.user = dict.split()
                # Iterate out the yaml file
                pass

    def _update_df_inplace(self, df_candidate, col_name):
        row_to_update = []
        for i, row in df_candidate.iterrows():
            row_to_update.append(i)
        # print(f'Row to update: {row_to_update}')
        self.df_one_day.loc[self.df_one_day.index.isin(row_to_update), col_name] = True

    def _lic_alloc_by_time_slice(self):
        """
        This is to slice time into second of time_slice slices (for now)
        :return:
        """
        # Use 24 hrs for now, can be updated in the future.
        curr_slice = 0 * 3600
        max_sec = 24 * 3600

        while curr_slice < max_sec:
            # Only process data with 'processed = False'
            mask = (self.df_one_day['checkout_time'] >= curr_slice) & (
                    self.df_one_day['checkout_time'] < curr_slice + self.time_slice)

            df_mask = self.df_one_day[mask]
            self._update_df_inplace(df_candidate=df_mask, col_name='processed')
            df_temp = self.df_one_day[mask].head(self.lic[self.lic_to_assign])
            self._update_df_inplace(df_candidate=df_temp, col_name='approved')
            curr_slice += self.time_slice

    def _run_one_day(self):
        """
        Generates one day of simulated checkouts.
        :return: Update self.df_one_day with a simulated database
        """
        one_day_db = []
        self._resource_readin(yaml_file='sim_mgr_user.yaml')
        l_lictype = self.lic_to_assign
        [l_user,
         l_user_host,
         l_display,
         l_version,
         l_server_host,
         l_port,
         l_handle] = ['default',
                      'user_host1',
                      '1',
                      '1.0',
                      'sever_host1',
                      '3721',
                      '40301']
        for i in range(self.checkout_per_day):
            random_idx = random.randint(0, len(self.user) - 1)
            l_user = self.user[random_idx]
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
                                          l_lictype,
                                          lm_sim_inst.checkout_time,
                                          lm_sim_inst.checkin_time,
                                          lm_sim_inst.sim_duration,
                                          False,
                                          False]

    def lmstat_query(self, date, time):
        """
        date: need to be in format %Y_%M_%D
        time: %H:%M:%S
        t_int: The length of reporting in seconds
        Function to return a simulated lmstat -a query
        :return:
        """
        sec = _convert_time_to_sec(time)
        # Time interval to report, in seconds
        df_to_response = pd.read_csv(f"checkout_summary_{date}.csv", index_col=0)

        mask = (df_to_response['checkout_time'] >= sec) & (df_to_response['checkout_time'] < sec + self.time_slice)
        df_to_response_masked = df_to_response[mask]
        # Count how many 'approved = True' rows to calculate how many license current in use
        lic_in_use_during_time_interval = len(df_to_response_masked[df_to_response_masked['approved'] == True])
        print(df_to_response_masked)
        day, date_converted = _convert_date_to_day_month(date)
        for index, row in df_to_response_masked.iterrows():
            time_report = datetime.timedelta(seconds=row['checkout_time'])
            print(f"License server system status: {row['port']}@{row['server_host']}")
            print(f"License files(s) on {row['server_host']}: ...")
            print(f"{row['server_host']}: license server system UP\n")
            print(f"demo: UP v9.3")
            print(f"Feature usage info:")
            print(
                f"Users of {row['lic_type']}: (Total of {self.lic[self.lic_to_assign]} issued, Total of {lic_in_use_during_time_interval} license in use)")
            print(f" \"{row['lic_type']}\" v1.0, vendor: demo")
            print(f"floating license")
            print(
                f"{row['user']} {row['user_host']}, user_ip (v1.0) ({row['user_host']}/{row['port']} {row['handle']}), start {day} {date_converted.month}/{date_converted.day} {time_report}\n")

# if __name__ == '__main__':
    # Example usage of the code
    # lsm = lm_sim_mgr(checkout_per_day=1000, engine_mode='design', person='design', lic_to_assign='vmms', time_slice=60)
    # lsm._run_one_day()
    # lsm._resource_readin(yaml_file='sim_mgr_config.yaml')
    # lsm._lic_alloc_by_time_slice()
    # lsm.df_one_day.to_csv('checkout_summary_1970_01_01.csv')
    # lsm.lmstat_query(date='1970_01_01', time='09:45:00')
