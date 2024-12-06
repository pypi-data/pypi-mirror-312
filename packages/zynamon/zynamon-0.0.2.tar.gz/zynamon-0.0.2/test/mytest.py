import numpy as np
from scipy import signal    ### DEBUG ## checkt this for replace sigproc!

from zdev.plot import qplot
from zynamon.tscore import TimeSeries, ts_convert_time


FILE = r'../data/TimeDefined.json'

N = 20
N2 = 5
DEV_VAL = 333
DEV_TIME = 60
JUMP_TIME = 500
START = '1970-01-01 00:00:50'
# START = '2023-12-01 00:00:00'
START_stamp = ts_convert_time(START, float)

def demo():

    # stack times
    tmp = np.linspace(0.0, 1.0, (N+N2))
    t_fluct = signal.sawtooth(2*np.pi*1.0 * tmp, 0.5)
    t_base = np.ones(N) * START_stamp
    t_jump = np.ones(N2) * (START_stamp + N*DEV_TIME + JUMP_TIME)

    t_def = np.zeros_like( np.concatenate((t_base, t_jump)) )
    for n, item in enumerate(t_base):
        t_def[n] = item + n*DEV_TIME + np.abs(t_fluct[n]*DEV_TIME)
    for n, item in enumerate(t_jump):
        t_def[len(t_base)+n] = item + n*DEV_TIME + np.abs(t_fluct[n]*DEV_TIME)


    # create values
    x_def = 1000 + t_fluct*DEV_VAL

    # show times & values
    t_def_iso = ts_convert_time(t_def, str)
    for n, item in enumerate(t_def_iso):
        print(item)
    fh = qplot(t_base)
    qplot(t_def, info='time (defined)', fig=fh)
    qplot(x_def, info='values', fig=fh, newplot=True)

    return


# # create time-seris & export
# ts = TimeSeries('time_defined')
# ts.samples_add({'t': t_def, 'x': x_def})
# ts.export_to_file(FILE, overwrite=True)

# qplot(ts, time_iso=True)