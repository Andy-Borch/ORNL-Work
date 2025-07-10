from evalys.jobset import JobSet
from evalys import visu
import matplotlib.pyplot as plt

js = JobSet.from_csv("/home/er3/ORNL-Work/Simulators/batsim/out_jobs.csv")


visu.gantt.plot_gantt(js)

plt.savefig("./gantt_chart.png", dpi=3000, bbox_inches='tight')

plt.show()

# coding: utf-8
import matplotlib.pyplot as plt
from evalys.jobset import JobSet

#matplotlib.use('WX')

js = JobSet.from_csv("/home/er3/ORNL-Work/Simulators/batsim/out_jobs.csv")
print(js.df.describe())

js.df.hist()

#fig, axe = plt.subplots()
js.gantt()
plt.show()
