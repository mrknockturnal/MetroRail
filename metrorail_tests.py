# just comment out one of the two lines below to switch between the two implementations (prac1 and prac2)
#from metrorail_network1 import *
from metrorail_network2 import *

route_on_single_line = central_BLV.number_stops_and_direction(uni, esp)
print("Unibell to Esplanade on central_BLV: direction {0}, {1} stops\n".format(route_on_single_line[1].name, route_on_single_line[0]))

uni.route_to(esp)
ooz.route_to(cpt)
uni.route_to(pen)
cpt.route_to(blv)
yst.route_to(chn)

uni.route_to(sto)
uni.route_to(slt)

# the test below is very inefficient with the first version of the function (going through Cape Town, total of 30 stops)
kuy.route_to(kpt)

# now best routes (you can see that the output differs between different runs when using the second version of the prac):
kuy.best_route_to(kpt)
uni.best_route_to(slt)
clr.best_route_to(haz)

print(clr.get_connecting_time(southern, central_BLV)) # raises one of our user-defined exceptions


