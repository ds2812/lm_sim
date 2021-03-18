from scipy import stats
import numpy as np


class lm_sim():

    def __init__(self, engine_mode, person):
        self.engine_mode = engine_mode
        self.person = person
        self.min_sim_time = 0.5
        self.sim_time_mu = 1
        self.sim_time_sigma = 1
        self._engine_mode()

    def _engine_mode(self):
        if self.engine_mode == 'pre':
            self.sim_time_mu = 5
            self.sim_time_sigma = 10
        if self.engine_mode == 'design':
            self.sim_time_mu = 5
            self.sim_time_sigma = 10
        if self.engine_mode == 'pg':
            self.sim_time_mu = 120
            self.sim_time_sigma = 10

    def _lic_type(self):
        pass

    def _sim_start_time(self):
        pass

    def _sim_duration(self):
        """
        In minutes, generate how long the simulation is going to take
        :return:
        """
        rand_min = np.random.normal(self.sim_time_mu, self.sim_time_sigma)
        if (rand_min < self.min_sim_time):
            rand_min = self.min_sim_time  # Force simulation to minimum time if random value is less than random
        return rand_min


if __name__ == '__main__':
    pass
