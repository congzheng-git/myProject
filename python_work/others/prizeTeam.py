import random

with open('prizeTeam.txt', 'w') as tes:
	empty = "    "
	name = "\"playertest\","
	# icon = "\"5,\""
	for i in range(100, 150):
		if i == 100:
			print("\"" + str(i) + "\" : " + "{", file=tes)
		else:
			print("\t" + "\"" + str(i) + "\" : " + "{", file=tes)
		print("\t" + empty +"\"" + "a" + "\" : " + name, file=tes)
		print("\t" + empty +"\"" + "b" + "\" : " + "\"" + str(random.randint(1,6)) + "\",", file=tes)
		print("\t" + empty +"\"" + "c" + "\" : " + str(i * random.randint(10,20) + random.randint(1,100)) + ",", file=tes)
		print("\t" + empty +"\"" + "d" + "\" : " + "-1", file=tes)
		if i == 149:
			print("\t" + "}", file=tes)
		else:
			print("\t" + "},", file=tes)	
		
		

