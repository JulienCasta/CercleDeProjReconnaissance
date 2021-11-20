x = range(100)
f = open("nombres.txt", "w")
f.write('[')
for chiffre in x:
	f.write("'{}',".format(chiffre))
f.write(']')

