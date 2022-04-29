from system import System
from step2 import Step2

system = System()
system.run()
best_container = system.get_best_container()

print(best_container)

FILE = "test250.txt"
layout = Step2(FILE, best_container)
layout.create_containers_matrix()
layout.print_matrix()
layout.prepare_plata()
layout.run()
print('Q = ', layout.get_q())
