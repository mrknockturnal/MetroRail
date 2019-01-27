###### 1 Using Exec Built in Functions ############################
alphabet = "abcdefghijklmnopqrstuvwxyz"
position = 1
for i in range(len(alphabet)):
    exec("%s = %d" % (alphabet[i],position))
    position += 1

print(a)
print(b)
print(c)
print(z)

####################################################################

###### 2 Built-in functions on strings #############################

sentence = str(input("Please enter sentence"))
words = list(sentence)
char = "!?:;.,"

for i in range(len(words)):
    if words[i] in char:
        words[i] = ' '

new = "".join(words)

count = new.split()

print(len(count))

#######################################################################

########### 3 Using it all to instantiate stations from..... ##########
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

########################################################################   
