# defining the class for train lines
class Line:
		def __init__(self, long_name, colour, train_num_prefix):
				self.long_name = long_name
				self.colour = colour
				self.train_num_prefix = train_num_prefix
				self.stations = [] # advisable in order not to run into errors of the type "no such attribute"
				self.nb_stations = 0 # consistent with the previous line
				self.endpoints = [] # also consistent with the above
				self.travel_times = [ [], [] ] # a list of two lists, empty for the moment

		def set_stations(self, stations):
				self.stations = stations
				self.endpoints = [ stations[0], stations[len(stations)-1] ]
				self.nb_stations = len(stations)
				# and then for all the Station objects listed in the parameter called "stations",
				# we update the corresponding attribute called "lines":
				for stn in stations:
						if self not in stn.lines: # if the station doesn't know yet that it's on the line being "self" here
								stn.lines.append(self)
								# and be careful, in this implementation we then also have to change the "is_interchange" attribute of that station
								if len(stn.lines) >= 2:
										stn.is_interchange = True


		def get_stations(self):
				return self.stations

		def has_station(self, stn):
				for station in self.stations:
						if stn == station:
								return True
				return False
		
		def index_station(self, stn):
				# returns the index of the station in the list self.stations, -1 if stn is not found in the list
				for i in range(self.nb_stations):
					if self.stations[i] == stn:
							return i
				return -1

		def number_stops_and_direction(self, origin, destination):
				# This function returns a list of THREE elements:
				# (1) the number of stops (>= 0) between one station and another on the line.
				# (2) the direction (endpoint station) in which to go in order to go from station_from to station_to
				# (3) the corresponding travel time in seconds (an integer)
				# The first two arguments are instances of the class Station. It returns [-1, None] if at least one
				# of the given stations is not on the line.
				if origin == destination:
						return [0, None, 0]
				index_orig = -1
				index_dest = -1
				num_found = 0 # to break later as soon as we have found the two stations, using only one loop
				for i in range(self.nb_stations): # preparing to loop on the list of stations on the line
						if self.stations[i] == origin:
								index_orig = i
								num_found += 1
						elif self.stations[i] == destination:
								index_dest = i
								num_found += 1
						else:
								continue # we haven't incremented num_found
						if num_found == 2:
								break
				if num_found < 2:
						return [-1, None, 0]
				if index_orig > index_dest:
						# we have to go towards the "beginning" of the line
						# we use a slice of self.travel_times[1] (inbound direction)
						# and the built-in function sum to sum the travel times between stations
						return [ index_orig - index_dest, self.stations[0], sum(self.travel_times[1][index_dest:index_orig]) ]
				else:
						# we have to go towards the "end" of the line (outbound direction)
						# we use a slice of self.travel_times[0] (outbound direction)
						# and the built-in function sum to sum the travel times between stations
						return [ index_dest - index_orig, self.stations[-1], sum(self.travel_times[0][index_orig:index_dest]) ] 



		def set_random_travel_times(self, rng): # the second argument is a random number generator, object of class random.Random
				self.travel_times = [[],[]] # resetting any existing travel times
				for i in [0,1]:
						for j in range(self.nb_stations-1): # to create the appropriate number of iterations
								self.travel_times[i].append(rng.randint(10,120)) # random number generation




class Station:
		
		default_interchange_time = 60 # a class variable

		def __init__(self, name, code): #only two parameters to the constructor in this implementation
				self.name = name
				self.code = code
				self.lines = []
				self.is_interchange = False

		def get_lines(self):
				return self.lines

		def get_num_lines(self):
				return len(self.lines)

		def is_on_line(self, line):
				# returns True if the station is on the line (given as an object of type Line).
				# moreover, checks that the line definition is consistent with that information
				found = False
				for l in self.lines:
						if l == line:
								found = True
								break
				if not found:
						return False
				else:
						if self not in line.get_stations(): # another way to test for membership of an element in a list
								print("Warning! Inconsistent situation: station {0} claims it is on line {1}, but that line fails to list it as one of its stations!".format(self.name, line.long_name))
						return True


		def find_interchange(self, line_on, line_to):
				# this method returns a Station object being an interchange station on line_on (which contains the station self), 
				# where it is possible to change to line_to.
				# If there is no such interchange, the method returns None.
				if not self.is_on_line(line_on):
						print("Error in closest_interchange: object self is not on the first line given as argument.")
						return
				if line_on == line_to:
						print("Error in closest_interchange: line_on is the same as line_to.")
						return
				for stn in line_on.stations:
						if stn == self:
								continue # this is not an interchange, but the source station
						if line_to in stn.lines:
								return stn
				print("In closest_interchange: line \"{0}\" is not reachable with one change only from station {1} using line \"{2}\".".format(line_to.long_name, self.name, line_on.long_name))


		def find_all_interchanges(self, line_on, line_to):
				# useful to find all the possible routes from one station to another,
				# this method returns a list of Station objects:
				# all the interchange stations on line_on (which contains the station self) 
				# where it is possible to change to line_to.
				# If there is no such interchange, the method returns an empty list.
				if not self.is_on_line(line_on):
						print("Error in closest_interchange: object self is not on the first line given as argument.")
						return []
				if line_on == line_to:
						print("Error in closest_interchange: line_on is the same as line_to.")
						return []
				interchanges = []
				for stn in line_on.stations:
						if stn == self:
								continue # this is not an interchange, but the source station
						if line_to in stn.lines:
								interchanges.append(stn)
				return interchanges


		# a helper function to return a duration in hours, minutes, seconds (in a string) from an argument given in seconds (int)
		def hr_min_sec_string(self, number):
				hours = number // 3600
				if hours > 0:
						number -= hours * 3600
				minutes = number // 60
				if minutes > 0:
						number -= minutes * 60
				seconds = number
				# then we create the string:
				if hours == 0:
						hours_substring = ""
				else:
						hours_substring = str(hours) + "hr "
				if minutes == 0:
						minutes_substring = ""
				else:
						minutes_substring = str(minutes) + "min "
				if seconds == 0:
						seconds_substring = ""
				else:
						seconds_substring = str(seconds) + "s"

				almost_ready = hours_substring + minutes_substring + seconds_substring
				# and then we remove the trailing spaces if necessary (for instance if almost_ready == "1min ", using a builtin function:
				return almost_ready.rstrip()


		def get_connecting_time(self, line1, line2):
				# the arguments are two objects of class Line
				# the return value is an integer (number of seconds)
				# we first try and get the two indices corresponding to the two lines 
				l = self.lines
				try:
						index1 = l.index(line1)
						index2 = l.index(line2)
				except ValueError: # raised by the built-in function index in case one of the lines is not found in l
						raise InvalidLine("object self is not on one of the lines given as arguments to get_connecting_time()")
				# at this point we know the two indices index1 and index2 are properly set
				try:
						return self.interconnect_time[index1][index2]
				except (AttributeError, IndexError):
						return Station.default_interchange_time







		# another helper function to print a direct route to the screen
		def print_direct_route(self, destination, line, direction, num_stops, travel_time):
				if num_stops > 1:
						plural = "s"
				else:
						plural = ""
				print("Route from {0} to {1}:".format(self.name, destination.name))
				print("From {0} to {1} on line \"{2}\", direction {3} ({4} stop{5}, {6})\n".format(self.name, destination.name, line.long_name, direction.name, num_stops, plural, self.hr_min_sec_string(travel_time)))


		# helper function to print a route involving one interchange
		def print_indirect_route(self, destination, line1, direction1, num_stops1, travel_time1, change_stn, interconnect_time, line2, direction2, num_stops2, travel_time2):
				print("Route from {0} to {1}:".format(self.name, destination.name))
				if num_stops1 > 1:
						plural = "s"
				else:
						plural = ""
				print("From {0} to {1} on line \"{2}\", direction {3} ({4} stop{5}, {6})".format(self.name, change_stn.name, line1.long_name, direction1.name, num_stops1, plural, self.hr_min_sec_string(travel_time1)))
				print("Change lines in {0} to line \"{1}\" ({2})".format(change_stn.name, line2.long_name, self.hr_min_sec_string(interconnect_time)))
				if num_stops2 > 1:
						plural = "s"
				else:
						plural = ""
				print("From {0} to {1} on line \"{2}\", direction {3} ({4} stop{5}, {6})\n".format(change_stn.name, destination.name, line2.long_name, direction2.name, num_stops2, plural, self.hr_min_sec_string(travel_time2)))


		# to get a route from one station to another, the first solution is to get for each station (origin and destination)
		# the list of lines they are on, and try to see if there is one line common to both stations. Then we have a path involving no
		# train change. If there is no common line, we will have to change once. We try and find a suitable interchange station going from
		# the origin station by increasing distance.
		def route_to(self, destination):
				# first try and find a route with no train change: try to find a common line
				for line1 in self.lines:
						for line2 in destination.lines:
								if line1 == line2:
										# we found a direct connection, to be preferred to any other route:
										path = line1.number_stops_and_direction(self, destination)
										self.print_direct_route(destination, line1, path[1], path[0], path[2])
										return

				# at this point we know the two stations are not on the same line. We need to find an interchange
				# from the station of origin to catch a line on which the other station is:
				for line_from_self in self.lines:
						for line_where_to_go in destination.lines:
								# find a possible interchange:
								station0 = self.find_interchange(line_from_self, line_where_to_go)
								if station0 != None:
										# we have a solution involving only one change, through station0.

										# First segment:
										first_trip = line_from_self.number_stops_and_direction(self, station0)
										# Connecting time:
										interconnect = station0.get_connecting_time(line_from_self, line_where_to_go)
										# Second segment:
										second_trip = line_where_to_go.number_stops_and_direction(station0, destination)

										self.print_indirect_route(destination, line_from_self, first_trip[1], first_trip[0], first_trip[2], station0, interconnect, line_where_to_go, second_trip[1], second_trip[0], second_trip[2]) 
										return
				print("No route found between {0} and {1} involving at most one interchange.".format(self.name, destination.name))




		# Below, "best_route_to" is a reimplementation of "route_to"
		# finding the route giving the minimum number of stops.
		# We store in a local variable the list of all solutions found so far,
		# and at the end of the function we select the one giving the minimum number of stops.
		# Our list of solutions contain solutions described as:
		# [ first_line, direction, nb_stops_trip1, time_trip1, interchange_station, interchange_time, second_line, direction, nb_stops_trip2, time_trip2 ]
		# ([ first_line, direction, nb_stops, trip_time ] in case of a direct trip)
		# and we have three additional variables that we store:
		# (1) current_index -> the next index to be populated in the list
		# (2) minimum_stops -> the number of stops in the shortest solution
		# (3) index_in_list -> the position in the list of the shortest solution
		def best_route_to(self, destination):
				solutions = []
				current_index = 0
				minimum_time = 100000 # seconds
				index_in_list = -1

				# first try and find a route with no train change: try to find a common line
				for line1 in self.lines:
						for line2 in destination.lines:
								if line1 == line2:
										# we found a direct connection:
										path = line1.number_stops_and_direction(self, destination)
										solutions.append([line1, path[1], path[0], path[2]]) # we append one object that is a list
										trip_time = path[2]
										if trip_time < minimum_time: # the solution we just found is the best so far
												minimum_time = trip_time
												index_in_list = current_index
										# we now increment the current index because we have added a solution in the list
										current_index += 1
								else:
										# the two lines are different: find all their common interchange stations
										stations0 = self.find_all_interchanges(line1, line2)
										for connecting_station in stations0: # no iteration if stations0 is empty
												first_trip = line1.number_stops_and_direction(self, connecting_station)
												# Connecting time:
												interconnect = connecting_station.get_connecting_time(line1, line2)
												second_trip = line2.number_stops_and_direction(connecting_station, destination)
												solutions.append([line1, first_trip[1], first_trip[0], first_trip[2], connecting_station, interconnect, line2, second_trip[1], second_trip[0], second_trip[2]])
												trip_time = first_trip[2] + interconnect  + second_trip[2]
												if trip_time < minimum_time: # the solution we just found is the best so far
														minimum_time = trip_time
														index_in_list = current_index
												# we now increment the current index because we have added a solution in the list
												current_index += 1
				
				# ultimately, we return the best route (that can involve 0 or one change):
				if index_in_list == -1: # should never happen because there is always at least one solution going through Cape Town
						print("Error: no route found!")
						return

				best = solutions[index_in_list]
				print('Best ', end='') # prefix to form "Best Route to..."
				# best is a solution: this is a list of length 4 in case the best solution is a direct route,
				# or a list of length 9 in case it involves changing trains
				if len(best) == 4: # no changing trains
						self.print_direct_route(destination, best[0], best[1], best[2], best[3])
				else:
						self.print_indirect_route(destination, best[0], best[1], best[2], best[3], best[4], best[5], best[6], best[7], best[8], best[9])
						# to avoid print all these individual arguments instead of "print_indirect_route(destination, best)",
						# we would have to rewrite the definition of print_indirect_route so that it takes only two arguments


# we also define two exceptions: InvalidLine and InvalidStation

class InvalidLine(Exception):
		pass

class InvalidStation(Exception):
		pass
