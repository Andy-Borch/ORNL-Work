from evalys.jobset import JobSet
from evalys import visu
import matplotlib.pyplot as plt

js = JobSet .from_csv("/home/er3/ORNL-Work/Simulators/batsim/out_jobs.csv")
js.plot(with_details=True)

plt.show()

