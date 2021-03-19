from scipy import stats
import numpy as np
import datetime
import time


class lm_sim():
    """
    lmstat -a output data.
    https://media.3ds.com/support/simulia/public/flexlm108/EndUser/chap7.htm#wp895655
    :returns user, user_host, display, version, server_host, port, handle, checkout_time
    """

    def __init__(self, engine_mode, person):
        self.engine_mode = engine_mode
        self.person = person
        self.min_sim_time = 30
        self.sim_time_mu = 1
        self.sim_time_sigma = 1
        self._engine_mode()

    def _convert_time_to_sec(self, timt_to_convert):
        x = time.strptime(str(timt_to_convert).split(',')[0],'%H:%M:%S')
        sec_out = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
        print(sec_out)

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
        """
        # 9am to 6pm
        # 6pm to 12am
        # 12am to 9am

        

    def _sim_duration(self):
        """
        In seconds, generate how long the simulation is going to take
        :return: random seconds of license taken
        """
        rand_sec = np.random.normal(self.sim_time_mu, self.sim_time_sigma)
        if (rand_sec < self.min_sim_time):
            rand_sec = self.min_sim_time  # Force simulation to minimum time if random value is less than random
        return rand_sec

    def _sim_checkin_time(self):
        pass


if __name__ == '__main__':
    pass
