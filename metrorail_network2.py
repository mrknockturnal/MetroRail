import metrorail2
import random

# instantiating train lines
central_BLV = metrorail2.Line("Bellville via Lavistown", "blue", "90")
central_KPT = metrorail2.Line("Kapteinsklip via Pinelands", "blue", "95")
central_CHN = metrorail2.Line("Chris Hani via Esplanade", "blue", "99")
northern_MTV = metrorail2.Line("Bellville via Monte Vista", "green", "2")
northern_MUT = metrorail2.Line("Bellville via Mutual", "green", "3")
cape_flats = metrorail2.Line("Retreat via Athlone", "brown", "05")
southern = metrorail2.Line("Simonstown", "red", "02")

# global variable containing all the lines in a list:
network_lines = [central_BLV, central_KPT, central_CHN, northern_MUT, northern_MTV, cape_flats, southern]

# instantiating (creating) train stations
########################################################
file = open('stations.dat','r')
current = []
while True:
    line = file.readline()
    line = line.rstrip('\n')
    current.append(line.split(','))
    if len(line) == 0:
        break

for i in range(len(current)-1):
    code = current[i][2]
    station = current[i][1]
    codes = code.lower()
    exec("%s = metrorail2.Station(station,code)" % (codes))

file.close()

##########################################################
# populating lines with their stations (IN PROPER ORDER, outbound from Cape Town to the other end of the line)

central_BLV.set_stations([cpt, esp, yst, mut, lng, btw, lvs, blh, uni, pen, srp, blv])
northern_MUT.set_stations([cpt, wsk, slt, koe, mai, wol, mut, ttn, gdw, vas, els, prw, tyg, blv]) 
central_KPT.set_stations([cpt, wsk, slt, koe, mai, ndb, pnl, lng, btw, net, hdv, nya, ppi, ltg, mpl, kpt])
central_CHN.set_stations([cpt, esp, yst, mut, lng, btw, net, hdv, nya, ppi, sto, man, nol, nkq, khy, kuy, chn])
northern_MTV.set_stations([cpt, esp, yst, ken, ctc, aka, mtv, dgd, avo, ooz, blv])
cape_flats.set_stations([cpt, wsk, slt, koe, mai, ndb, pnl, haz, ath, crw, lnd, wet, ott, stf, htf, ret])
southern.set_stations([cpt, wsk, slt, obs, mow, rsb, rdb, new, clr, har, knw, wyn, wit, plm, sth, dpr, htf, ret, stb, lks, fsb, mzb, stj, kkb, fsh, snc, glc, sim])


# creating the travel times between stations (in this version 2 of the prac)
random_generator = random.Random()
for myline in network_lines:
		myline.set_random_travel_times(random_generator)


# and then generating random interconnection times for Mutual:
nb_lines = mut.get_num_lines()
mut.interconnect_time = []
for i in range(nb_lines):
		mut.interconnect_time.append([]) # start with an empty list for this row of the matrix
		for j in range(nb_lines):
				if i == j:
						mut.interconnect_time[i].append(0) # doesn't make sense to change from line x to line x
				else:
						mut.interconnect_time[i].append(random_generator.randint(20,80)) # between 20 and 80 seconds to realize a line interchange

