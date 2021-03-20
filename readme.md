LM_SIM
==========
A simulator attempt to model user activity for difference license in an organization

Engine
----------
This is a generator for a job_request based on different modes.

### Engine Mode

- engine_mode_pre: Feasibility studies, MATLAB/Simulink mostly used
- engine_mode_design: Design phase, vmms etc. mostly used
- engine_mode_verif: P&R tools, AMS used
- engine_mode_pre_pg: calibre tools, LVS/DRC/XOR tools
- engine_mode_future: To be added

### Person role

- design
- verification
- physical_design
- layout

### License type

Need to be assigned using a distributed amount + person role

- cal_*
- ciw
- jasper_*
- verdi
- voltus
- xsc_*

### Checkout time

Should be a distribution at 9-17, another distribution 17-23.59, another one 0-9 The start time should be bounded by
argument sent when instianting the an object.

### Duration

Should be a normal normal distribution, perhaps left skwed because more sims should be shorter sims

### Exit Type

This is an optional argument where it directs the engine to regenerate a same token if user terminated the process.

## job_request

Everything described above would combine into a job_request type for as 1 output result.

LM_SIM_MGR
===========
This is the simulator manager for lm_sim. It will do further database processing and also running simulations.

Initial idea is to run 1 day of sim and do processing. If more days are required, just call this inst multiple times and
combine them together.

Dataframe Structure
----------

- 'user': user checking out
- 'user_host': host checking out (handled by lm_sim_mgr, using .yaml)
- 'display': (handled by lm_sim_mgr, using .yaml)
- 'version': (handled by lm_sim_mgr, using .yaml)
- 'server_host': (handled by lm_sim_mgr, using .yaml)
- 'port': (handled by lm_sim_mgr, using .yaml)
- 'handle': (handled by lm_sim_mgr, using .yaml)
- 'lic_type': License type, defined in sim_mgr_config.yaml
- 'checkout_time': time checking out
- 'approved': Time slice algorithm is used to decide if a checkout is successful (handled by lm_sim_mgr)
- 'processed': A flag suggesting that this row has already been processed regarding approve/reject license.

Methods
---------

### lm_sim_mgr.__init__()

```python
lsm = lm_sim_mgr(checkout_per_day=1000, engine_mode='design', person='design', lic_to_assign='vmms', time_slice=60)
```

- checkout_per_day: Number of simulations to be run
- lic_to_assign: Need to mach with the sim_mgr_config.yaml
- time_slice: Sampling time of the simulator, it will be used as a time window to allocate license, and also be used to
  report license usage. A potential issue will be if lmstat_query time is not at 'o clock, it probably report
  allocated > max license due to simulator limitation.

Refer to [here](#LM_SIM) for other parameters

### lm_sim_mgr._run_one_day()

This starts the simulator engine (lm_sim) with parameters given in the init. It will run a full day (24 hrs) of data and
save in an internal DF: lm_sim_mgr.df_one_day

### lm_sim_mgr.lsm._resource_readin()

This reads resource in the config file: sim_mgr_config.yaml

```yaml
lic_type:
  cal_pex: 300
  vmms: 5
  xsc: 300
  ciw: 200

```

### lm_sim_mgr.lsm._lic_alloc_by_time_slice()

This function runs an algorithm to divide the generated database into time slices, lenth = self.time_slice set before. Then it will
assign license based on maximum number of license on hand.

```python
Example: lm_sim_mgr._lic_alloc_by_time_slice()
```

This slices the result into time slices of 3600 secs. In a full 3600 second period, it will assign license to top X
number of users where X=total license available.

### lm_sim_mgr.lmstat_query(date, time, t_int)

This function generates a short report with the time interval given. Detailed info at the top of the function.

```python
Example: lm_sim_mgr.lmstat_query(date='1970_01_01', time='09:45:00')
```
- date will be used to identify .csv to load (checkout_summary_{date}.csv)
- time will be used to put a window in the .csv file to generate a lmstat -a response.

Output Example (One line)

```log
License server system status: 3721@sever_host1
License files(s) on sever_host1: ...
sever_host1: license server system UP

demo: UP v9.3
Feature usage info:
Users of vmms: (Total of 5 issued, Total of 1 license in use)
 "vmms" v1.0, vendor: demo
floating license
daniel user_host1, user_ip (v1.0) (user_host1/3721 40301), start Thu 1/1 9:45:58
```

