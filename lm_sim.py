from scipy import stats
import numpy as np
import datetime
import time
import random


class lm_sim():
    """
    lmstat -a output data.
    https://media.3ds.com/support/simulia/public/flexlm108/EndUser/chap7.htm#wp895655
    :returns user, user_host, display, version, server_host, port, handle, checkout_time
    """

    def __init__(self, engine_mode, person):
        self.engine_mode = engine_mode
        self.person = person
        self.min_sim_time = 60
        self.sim_time_mu = 1
        self.sim_time_sigma = 1
        self.checkout_time = None
        self.sim_duration = None
        self.checkin_time = None
        self.valid = False

        self._engine_mode()
        self._sim_checkout_time()
        self._sim_checkin_time()

    def _engine_mode(self):
        if self.engine_mode == 'pre':
            self.sim_time_mu = 300
            self.sim_time_sigma = 600
        if self.engine_mode == 'design':
            self.sim_time_mu = 300
            self.sim_time_sigma = 600
        if self.engine_mode == 'pg':
            self.sim_time_mu = 7200
            self.sim_time_sigma = 600

    def _sim_host(self):
        pass

    def _sim_display(self):
        pass

    def _sim_version(self):
        pass

    def _sim_port(self):
        pass

    def _sim_handle(self):
        pass

    def _lic_type(self):
        pass

    def _sim_checkout_time(self):
        """
        In seconds, generate a checkout time of the license.
        :return: a checkout time in second if lucky, -1 if unlucky.
        """
        # 9am to 6pm
        # 6pm to 12am
        # 12am to 9am
        rand_checkout_time = random.randint(0, 24 * 60 * 60)  # Random time during the 24 hour day
        if 9 * 60 * 60 < rand_checkout_time <= 18 * 60 * 60:  # 9am to 6pm, not doing anything
            self.valid = True
        elif 18 * 60 * 60 < rand_checkout_time <= 24 * 60 * 60:  # 6pm to 12am, randomly drop 75% of value
            if random.randint(0, 3) == 1:
                self.valid = True
        elif 0 < rand_checkout_time <= 9 * 60 * 60:  # 12am to 9am, randomly drop 90% of value
            if random.randint(0, 20) == 1:
                self.valid = True
        if self.valid:
            # If data is valid, it will update the class variable.
            self.checkout_time = rand_checkout_time
            return rand_checkout_time
        else:
            return -1

    def _sim_duration(self):
        """
        In seconds, generate how long the simulation is going to take
        :return: random seconds of license taken
        """
        rand_sec = np.random.normal(self.sim_time_mu, self.sim_time_sigma)
        if rand_sec < self.min_sim_time:
            rand_sec = self.min_sim_time  # Force simulation to minimum time if random value is less than random
        self.sim_duration = rand_sec
        return rand_sec

    def _sim_checkin_time(self):
        if self.valid:
            self._sim_duration()
            self.checkin_time = self.checkout_time + self.sim_duration
        # Check if it goes to next day


if __name__ == '__main__':
    pass
