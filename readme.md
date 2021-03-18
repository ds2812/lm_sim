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