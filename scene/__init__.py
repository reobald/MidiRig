def generateList():
	list = ["default", "midirigconstants", "roland_sysex","customunits"]
	for i in range(1,257):
		s = "scene_"
		if i>99: 
			list.append("scene"   + `i`)
		elif i>9: 
			list.append("scene0"  + `i`)
		else:
			list.append("scene00" + `i`)
	return list

__all__ = generateList()
