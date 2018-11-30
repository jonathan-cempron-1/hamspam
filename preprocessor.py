import re
#import pydot
import datetime
import sys
import csv

# returns
# FALSE if character is expected in input language
# TRUE if character is not allowed
def isCharNotExpected(inch):
	acceptable = "?+*|[]()-"
	for ch in acceptable:
		if(inch==ch):
			return False
	if(inch.isalpha()):
		return False
	if(inch.isdigit()):
		return False
	return True

# returns
# TRUE if inpt is a valid regex whose
# FALSE if invalid
# we restricted our valid regex		
def isValidRegEx(inpt):
	is_valid = True
	#for letter in inpt:
	#	if(isCharNotExpected(letter)):
	#		return False
	#try:
	#	re.compile(inpt)
	#	is_valid = True
	#except re.error:
	#	is_valid = False
	return is_valid

# initializes the data structure
# grouping elemnts () [] are stored as a list
# nested groups are nested list
# example input: ab(cd(ef))gh
# output: ['a', 'b', ['(', 'c', 'd', ['(', 'e', 'f', ')'], ')'], 'g', 'h']
indx = 0
def datStructPass1(inpt, oupt):
	global indx
	#print(indx)
	if(len(inpt)):
		temp = inpt[0]
		if temp=="(" or temp=="[":
			d1 = []
			d1.append(temp)
			inpt2, d2 = datStructPass1(inpt[1:], d1)
			oupt.append(d2)
			datStructPass1(inpt2[indx:], oupt)
		elif temp==")" or temp=="]":
			oupt.append(temp)
			indx = indx + 1
			return inpt[:], oupt
		else:
			oupt.append(temp)
			datStructPass1(inpt[1:], oupt)
		indx = indx + 1
	return inpt, oupt

i1a = 0
def datStructPass1a(inpt, oupt, lengt):
	global i1a
	while i1a < lengt:
		if inpt[i1a] == "(" or inpt[i1a] == "[":
			fndchr = inpt[i1a]
			i1a += 1
			noupt = datStructPass1a(inpt, [fndchr], lengt)
			oupt.append(noupt)
		elif inpt[i1a] == ")" or inpt[i1a] == "]":
			fndchr = inpt[i1a]
			oupt.append(fndchr)
			return oupt
		else:
			oupt.append(inpt[i1a])
		i1a += 1
	return oupt

# groups * + ? and elements on its left together
# unifies ranges a-z A-Z 0-1, detects if - usage is for range or as character, inside a []
# sample pass1 input (a|b)*-ab[a-z]
# output [[['(', 'a', '|', 'b', ')'], '*'], '-', 'a', 'b', ['[', 'a-z', ']']]
def datStructPass2(datstruct):
	datstruct2 = []
	for i, thing in enumerate(datstruct):
		if type(thing) == list:
			datstruct2.append(datStructPass2(thing))
		# group * + ? with left
		elif thing == "?" or thing == "*" or thing == "+":
			temp = [datstruct2.pop(),thing]
			datstruct2.append(temp)
		# unify ranges 0-1 a-z A-Z, check if inside a []
		elif i>1 and i<len(datstruct) and datstruct[i-1]=="-" and datstruct[0]=="[":
			lft = datstruct[i-2]
			dsh = datstruct[i-1]
			rht = datstruct[i]
			# make sure left and right are char/str data type
			if type(lft) is str and type(rht) is str:
				# for number range
				if lft.isdigit() and rht.isdigit():
					dsh = datstruct2.pop()
					lft = datstruct2.pop()
					temp = "%s%s%s"%(lft, dsh, rht)
					datstruct2.append(temp)
				# for uppercase character ranges
				elif lft.isalpha() and lft.isupper() and rht.isalpha() and rht.isupper():
					dsh = datstruct2.pop()
					lft = datstruct2.pop()
					temp = "%s%s%s"%(lft, dsh, rht)
					datstruct2.append(temp)
				# lower case
				elif lft.isalpha() and lft.islower() and rht.isalpha() and rht.islower():
					dsh = datstruct2.pop()
					lft = datstruct2.pop()
					temp = "%s%s%s"%(lft, dsh, rht)
					datstruct2.append(temp)
		else:
			datstruct2.append(thing)
	return datstruct2

def datStructPass3(datstruct):
	datstruct2 = []
	temp = ["("]
	for thing in datstruct:
		if thing == "|":
			temp.append(")")
			datstruct2.append(temp)
			temp = ["("]
			datstruct2.append(thing)
			temp.append
		elif type(thing) is list and thing[0] == "(":
			thing2 = thing[1:len(thing)-1]
			temp2 = datStructPass3(thing2)
			temp.append(["("] + temp2 +[")"])
		else:
			temp.append(thing)
	temp.append(")")
	datstruct2.append(temp)
	return datstruct2

def getValueRange(valArg):
	lb = valArg[0]
	ub = valArg[2]
	rangVals = ["("]
	for i in range(ord(lb), ord(ub)+1):
		rangVals.append("%c"%chr(i))
		rangVals.append("|")
	del rangVals[-1]
	rangVals.append(")")
	return rangVals

# converts [a-zA-z] into (a-z|A-Z)
# then a-z into (a|b|c|d|e...)
def datStructPass4(datstruct):
	datstruct2 = []
	for thing in datstruct:
		if type(thing) is list and thing[0] == "[":
			temp = []
			for i, ch in enumerate(thing):
				if i == 0 and ch == "[":
					temp.append("(")
				elif i == len(thing)-1 and ch == "]":
					temp.append(")")
				elif type(ch) is list:
					temp.append(datStructPass4(thing))
				elif len(ch) == 3 and ch[1] == "-":
					temp.append(getValueRange(ch))
				else:
					temp.append(ch)
				if 0 < i and i < len(thing)-2:
					temp.append("|")
			datstruct2.append(temp)
		# all below maintains the datastructure
		elif type(thing) is list:
			datstruct2.append(datStructPass4(thing))
		else:
			datstruct2.append(thing)
	return datstruct2
	

# generates a list of input alphabet
# ranges are taken as a single unit
# returns inptAlpha and tableHEader
# sample input: (a-z)*abb  
# inptAlpha output ["a-z", "a", "b"]
# tableHeader output  ["state", "a-z", "a", "b", "epsilon"]
def getInptAlpha(datstruct):
	listAlpha = []
	acceptable = "?+*|[]()"
	for thing in datstruct:
		# recurse if list
		if type(thing) is list:
			temp, tempTable = getInptAlpha(thing)
			for nth in temp:
				listAlpha.append(nth)
		else:
			# exclude operators
			incl = True
			for ch in acceptable:
				if thing == ch:
					incl = False
					break
			if incl:
				listAlpha.append(thing)
	# remove redundancy in characters
	listAlpha2 = []
	for symbol in listAlpha:
		includeInAlpha2 = True
		for symbol2 in listAlpha2:
			if symbol == symbol2:
				includeInAlpha2 = False
				break
		if includeInAlpha2:
			listAlpha2.append(symbol)
	# prepare return and for table header
	listAlpha = listAlpha2[:]
	listAlpha2.append("epsilon")
	listAlpha2.insert(0, "state")
	tableHeader = listAlpha2
	return listAlpha, tableHeader
	
def isThingAlpha(thing, listAlpha):
	for elmnt in listAlpha:
		if elmnt == thing:
			return True
	return False

def getSymbolColumn(symbl, tableHeader):
	for i, tsymbl in enumerate(tableHeader):
		if tsymbl == symbl:
			return i
	return -1


sst1 = []
statecounter = 2
def cvtRegexToNfa(datstruct, listAlpha, table, startstate, endstate):
	global statecounter
	rowrstart = [None] * len(table[0])
	rowrend = [None] * len(table[0])
	table.append(rowrstart)
	table.append(rowrend)
	rowrstart[0] = startstate
	rowrend[0] = endstate
	prevrowrstart = rowrstart
	prevrowrend = rowrstart
	prevprevrowrstart = prevrowrstart
	prevprevrowrend = prevrowrend
	i = 0
	while(i < len(datstruct)):
		thing = datstruct[i]
		if type(thing) is list:
			# if thing is () grouped
			if thing[len(thing)-1] == ")":
				# remove grouping symbols
				thing = thing[1:len(thing)-1]
				# create 2 new states enclosing
				nstrt = statecounter
				nend = statecounter+1
				statecounter += 2
				# recurse for elements inner ()
				table, nrstrt, nrend = cvtRegexToNfa(thing, listAlpha, table, nstrt, nend)
				# relate to outer
				prevprevrowrstart = prevrowrstart
				prevprevrowrend = prevrowrend
				prevrowrend[len(prevrowrend)-1] = [nrstrt[0]]
				prevrowrend = nrend
				prevrowrstart = nrstrt
			# if thing is star *
			elif thing[len(thing)-1] == "*" or thing[len(thing)-1] == "?" or thing[len(thing)-1] == "+":
				# create 4 new states enclosing
				sst1 = statecounter
				sst2 = statecounter+1
				sst3 = statecounter+2
				sst4 = statecounter+3
				statecounter += 4
				srst1 = [None] * len(table[0])
				srst4 = [None] * len(table[0])
				srst1[0] = sst1
				srst4[0] = sst4
				table.append(srst1)
				table.append(srst4)
				# recurse for thing(s) on left
				thing2 = thing[len(thing)-2]
				nstrt = sst2
				nend = sst3
				table, srst2, srst3 = cvtRegexToNfa(thing2, listAlpha, table, nstrt, nend)
				# * for 4 states: 0orMany
				if thing[len(thing)-1] == "*":
					srst1[len(srst1)-1] = [sst2, sst4]
					srst3[len(srst1)-1] = [sst2, sst4]
				# ? for 4 states: 0or1
				elif thing[len(thing)-1] == "?":
					srst1[len(srst1)-1] = [sst2, sst4]
					srst3[len(srst1)-1] = [sst4]
				# + for 4 states 1orMany
				elif thing[len(thing)-1] == "+":
					srst1[len(srst1)-1] = [sst2]
					srst3[len(srst1)-1] = [sst2, sst4]
				# relate to outer
				prevprevrowrstart = prevrowrstart
				prevprevrowrend = prevrowrend
				prevrowrend[len(prevrowrend)-1] = [sst1]
				prevrowrend = srst4
				prevrowrstart = srst1
		# if thing is atomic symbol
		elif isThingAlpha(thing, listAlpha):
			# create rows
			nstrt = statecounter
			nend = statecounter+1
			statecounter += 2
			nrstrt = [None] * len(table[0])
			nrend = [None] * len(table[0])
			nrstrt[0] = nstrt
			nrend[0] = nend
			# add rows to table
			table.append(nrstrt)
			table.append(nrend)
			# connect rows to outside
			prevprevrowrstart = prevrowrstart
			prevprevrowrend = prevrowrend
			prevrowrend[len(prevrowrend)-1] = [nrstrt[0]]
			prevrowrend = nrend
			prevrowrstart = nrstrt
			# connect rows within
			nrstrt[getSymbolColumn(thing, table[0])] = nrend[0]
		elif thing == "|":
			# create new rows
			tst1 = statecounter
			tst2 = statecounter+1
			statecounter += 2
			trst1 = [None] * len(table[0])
			trst2 = [None] * len(table[0])
			trst1[0] = tst1
			trst2[0] = tst2
			table.append(trst1)
			table.append(trst2)
			# upper element to be or ed
			start1 = prevrowrstart
			end1 = prevrowrend
			start1c = start1[0]
			end1c = end1[0]
			# lower element to be or ed
			start2c = statecounter
			end2c = statecounter+1
			statecounter += 2
			i += 1
			thing2 = [datstruct[i]]
			#?????
			table, start2, end2 = cvtRegexToNfa(thing2, listAlpha, table, start2c, end2c)
			# connect upper and lower element to oring states trstx
			trst1[len(trst1)-1] = [start1c, start2c]
			end1[len(end1)-1] = [tst2]
			end2[len(end2)-1] = [tst2]
			# connectible to outside
			prevprevrowrstart[-1] = [tst1]
			prevrowrstart = trst1
			prevrowrend = trst2
		i += 1
	prevrowrend[len(prevrowrend)-1] = [rowrend[0]]
	return table, rowrstart, rowrend
	

def epsilonReduction(table):
	epsColNum = len(table[0])-1
	deletablestates = []
	table2 = table[:]
	i = 0
	while i < len(table2):
		targetStateRow = table[i]
		targetStateNum = table[i][0]
		targetStateEpsOut = table[i][epsColNum]
		#print "==="
		#print targetStateRow
		#print targetStateNum
		#print targetStateEpsOut
		# count epsilon going in
		cntEpsilonIn = 0
		j = 0
		while j < len(table2):
			epsIn = table2[j][epsColNum]			
			if type(epsIn) is list and targetStateNum in epsIn:
				cntEpsilonIn += 1
			j += 1
		# count epsilon going out
		cntEpsilonOut = 0
		if type(targetStateEpsOut) is list:
			cntEpsilonOut = len(targetStateEpsOut)
		#print "inout " + str(cntEpsilonIn) + " " + str(cntEpsilonOut)
		# check if state is deletable: i.e. one epsilon in, one epsilon out
		if cntEpsilonIn == 1 and cntEpsilonOut == 1:
			#print "state " + str(targetStateNum) + " is deletable "
			# new destination state
			newDestState = targetStateEpsOut[0]
			#print newDestState
			# ingoing state
			j = 0
			while j < len(table2):
				epsIn = table2[j][epsColNum]			
				if type(epsIn) is list and targetStateNum in epsIn:
					#point the ingoing state's epsilon to its new dest
					for qqindex, qqitem in enumerate(epsIn):
						if qqitem == targetStateNum:
							table2[j][epsColNum][qqindex] = newDestState
					#print table2[j]
				j += 1
			# add in list of deleteable states
			deletablestates.append(targetStateNum)
			# RECURSE LATER FOR OTHER DELETABLE STATES : UGLY BUGFIX
			break
		i += 1
	# delete deletable states
	for x in deletablestates:
		for t2indx, t2row in enumerate(table2):
			t2rowstate = t2row[0]
			if x == t2rowstate:
				del table2[t2indx]
	# repeat till no states can be deleted
	if(len(table) != len(table2)):
		table2 = epsilonReduction(table2)
	return table2
	
dfaTable = []#final answer
eclosureTable = [] #where eclosures are stored

def calculateEclosure(table, stateName): 
#store output at eclosure table;
# for startState= output of this is dfaTable firstState1
# eclosure table usually has spare column of none
	stateList = []
	stateList.append(stateName)
	for a in table:
		if a[0] == stateName:
			if a[-1] is not None:
				stateList += a[-1] #add the transition
			temp = [None] * 2
			temp[0] = stateName
			temp[1] = stateList
			stateList.sort() #first layer
			
	return stateList

def calculateEclosureSet(table, stateList, eclosureTable, inputPosition, rowCounter):
# finds eclosure of each state output in findEclosureWithInput, fetch data from eclosure table; removes duplicates and sorts; 
# check if output is already added at dfaTable as state, if not add the output of this to dfa table state
# add output of this to dfa transition table
	outputStateList = []
	# print str(type(stateList))
	# print stateList
	for a in stateList:
		for b in range(1, len(eclosureTable)):
			# print "state" + str(a)
			if a == eclosureTable[b][0]:
				temp = eclosureTable[b][-1] #gets eclosure of currentState
				# print "eclsoure of all " + str(temp)
				for c in temp: 
					if c not in outputStateList: #check if state is not listed
						outputStateList.append(c)
						outputStateList.sort()
				# calculateEclosureSet(table, stateList, eclosureTable, inputPosition, rowCounter)

	for c in range(0,len(dfaTable)):
		if c == rowCounter:
			dfaTable[c][inputPosition] = outputStateList


	isContained = False
	for x in dfaTable:
		if x[0] == outputStateList: #if it is already stored at dfaTable
			isContained = True
	if isContained is False:
		temp = [None] * (len(table[0])-1)
		temp[0] = outputStateList
		dfaTable.append(temp)

				
def findEclosureWithInput(table, stateList, stateInputPos): #check table for each state given input
# remove duplicates and sorts;
# Traverses with dfa table (row), input pos (column)
	newStateList = [] 

	for a in stateList: #traverse each state in listed states
		for b in range(1, len(table)): # find state it goes to given input and current state
			# print "StateList: " + str(a) + "|" + str(table[b][stateInputPos])
			if a == table[b][0]:
				temp = table[b]
				if temp[stateInputPos] != None:
					newStateList.append(temp[stateInputPos])
	return newStateList

def markStartState(dfaTable, startStateName):
	startStates = []
	for x in range(0, len(dfaTable)):
		if startStateName in dfaTable[x][0]:
			startStates.append(dfaTable[x][0])
	return startStates

def markEndState(dfaTable, endStateName):
	endStates = []
	for x in range(0, len(dfaTable)):
		if endStateName in dfaTable[x][0]:
			endStates.append(dfaTable[x][0])
	return endStates

# main loop ish
def populateDFATable(table, startState, endState):
	print()
	path = []
	for a in range(1,len(table)):
		output = calculateEclosure(table, table[a][0])
		while True:
			for b in output: #[0,4]#check each member of discovered path
				# print "output" + str(output)
				innerOutput = calculateEclosure(table, b) #findEclosure(4)
				for x in innerOutput: 
					if x not in path: #new member (5,7)
					 path.append(x)
					 output.append(x)
			break;
		temp = [None] * 2
		temp[0] = table[a][0]
		path.sort()
		temp[1] = path
		eclosureTable.append(temp)
		if table[a][0] == 0:
			temp = [None] * (len(table[0])-1)
			temp[0] = path
			dfaTable.append(temp)
			maxCol = len(table[a])
		output = []
		path = []

	rowCounter = 0
	#row
	while True:
		#column; assumes epsilon yung dulo so minus 1, and starts at 1st column
		for inputPosition in range(1, maxCol-1):
			if rowCounter == 0:
				stateList = dfaTable[rowCounter][0]
			else:
				stateList = dfaTable[rowCounter][0] #replace stateList to check if there are new states 
			# print "stateList " + str(stateList)
			moveOutput = findEclosureWithInput(table, stateList, inputPosition)			
			# print "moveOutput after with input" + str(moveOutput)
			calculateEclosureSet(table, moveOutput, eclosureTable, inputPosition, rowCounter)
		rowCounter +=1
		if rowCounter == len(dfaTable):
			break;

def getNewStateName(oldState, tempDfaTable):
	#print "--- GETTING NEW STATE NAME"
	#print "OLDSTATE: " + str(oldState)
	for i, row in enumerate(tempDfaTable):
		#print "CURRENTSTATE: " + str(row[0])
		if ( row[0] == oldState ):
			return i
	#print "--- GETTING NEW STATE NAME"

def isStateStart(state, startStates):
	#print "-- IS STATE START"
	#print "STATE: " + str(state)
	for startState in startStates:
		#print "LOOPSTATE: " + str(row[0])
		if ( str(startState) == str(state)):
			#"-- STATE IS START"
			return True
	#print "-- STATE IS NOT START"
	return False

def isStateEnd(state, endStates):
	#print "-- IS STATE END"
	#print "STATE: " + str(state)
	#print "ENDSTATES: " + str(endStates)
	for endState in endStates:
		#print "LOOPSTATE: " + str(endState)
		if ( int(endState) == int(state) ):
			#print "-- STATE IS END"
			return True
	#print "-- STATE IS NOT END"
	return False

def getInputIndex(inpt, alphabet):
	#print "--- GETTING INPUT INDEX"
	for i, item in enumerate(alphabet):
		if ( item == inpt ):
			#print "INDEX: " + str(i)
			#print "--- GETTING INPUT INDEX"
			return i
	

def getAlphabet(tableHeader):
	return tableHeader[1:]

def traverseDfa(inpts, alphabet, dfaTable, finalEndStates):
	#print "--- TRAVERSING DFA"
	#print "INPUTS: " + str(inpts)
	currentState = -1
	#initialize CurrentState
	for i, row in enumerate(dfaTable):
		if ( i == 0 ):
			currentState = row[0]

	for inpt in inpts:
		#print "Single INPUT: '" + str(inpt) + "'"
		#print "isThingAlpha" + str(isThingAlpha(inpt, alphabet))
		if ( isThingAlpha(inpt, alphabet) ):
			#print "INPUT TO DFA: " + str(inpt)
			#print "CURRENTSTATE: " + str(currentState)
			inputIndex = getInputIndex(inpt, alphabet)
			for row in dfaTable:
				state = row[0]
				transitions = row[1:]
				if ( int(state) == int(currentState) ):
					#print "CURRENT LOOP STATE: " + str(state)
					#print "ALPHABET: " + str(alphabet)
					#print "TRANSITIONS: " + str(transitions)
					currentState = transitions[inputIndex]
					break
		else:
			#print "--- TRAVERSING DFA STOP NOT INPUT OF DFA"
			return False
	#print "CURRENTSTATE: " + str(currentState)
	#print "finalEndStates" + str(finalEndStates)
	#print "--- DFA TRAVERSED"

	if ( isStateEnd(currentState, finalEndStates) ):
		return True
	else:
		return False

def traverseInput(qstr, alphabet, dfaTable, finalEndStates):
	#print "--- TRAVERSING INPUT"
	accepted = []
	i = 0
	while len(qstr) - i:
		n = len(qstr)
		while n > i:
			#print "I: " + str(i)
			#print "CURRENTSTRING: '" + str(qstr[i:n]) + "'"
			if ( traverseDfa(qstr[i:n], alphabet, dfaTable, finalEndStates) ):
				#print "accepted: substr(%d,%d): '%s'"%(i, n, qstr[i:n])
				accepted.append([i,n-1])
				i = n-1
			n -= 1
		i += 1
	#print "--- TRAVERSING INPUT"
	return accepted

# Highlight - highlights text in shell. Returns plain if colour doesn't exist.
def highlight(colour, text):
    if colour == "black":
        return "\033[1;40m" + str(text) + "\033[1;m"
    if colour == "red":
        return "\033[1;41m" + str(text) + "\033[1;m"
    if colour == "green":
        return "\033[1;42m" + str(text) + "\033[1;m"
    if colour == "yellow":
        return "\033[1;43m" + str(text) + "\033[1;m"
    if colour == "blue":
        return "\033[1;44m" + str(text) + "\033[1;m"
    if colour == "magenta":
        return "\033[1;45m" + str(text) + "\033[1;m"
    if colour == "cyan":
        return "\033[1;46m" + str(text) + "\033[1;m"
    if colour == "gray":
        return "\033[1;47m" + str(text) + "\033[1;m"
    return str(text)

def isIndexAccepted(index, acceptedIndices):
	for acceptedIndex in acceptedIndices:
		if ( index >= acceptedIndex[0] and index <= acceptedIndex[1] ):
			return True
	return False

def constructGraph(finalDfaTable, finalEndStates, finalStartStates, alphabet):
	# Graph Construction Start Time
	graphStartTime = datetime.datetime.now()
	print "CONSTRUCTING GRAPH"
	graph = pydot.Dot(graph_type='digraph')
	nodeStart = pydot.Node("Start")
	graph.add_node(nodeStart)
	nodes = []
	for i, row in enumerate(finalDfaTable):
		state = row[0]
		#print "STATE: " + str(state)
		#print "END STATE: " + str(isStateEnd(state, finalEndStates))
		nodeColor="red"
		if ( isStateEnd(state, finalEndStates) ):
			# state is end state
			nodeColor = "green"
		nodes.append([state ,pydot.Node(state, style="filled", fillcolor=nodeColor)])

	for node in nodes:
		graph.add_node(node[-1])

	edges = []
	for i, row in enumerate(finalDfaTable):
		state = row[0]
		transitions = row[1:]
		currentNode = None

		# get currentNode
		for node in nodes:
			if ( node[0] == state ):
				currentNode = node

		# start node to state
		if ( isStateStart(state, finalStartStates)):
			edges.append(pydot.Edge(nodeStart, currentNode[-1]))

		#get all transitions of state
		for i, inpt in enumerate(alphabet):
			nextState = transitions[i]
			if (nextState is not None):
				for node in nodes:
					if ( node[0] == nextState ):
						edges.append(pydot.Edge(currentNode[-1], node[-1], label=inpt))

	for edge in edges:
		graph.add_edge(edge)


	graph.write_png('dfa.png')
	print "GRAPH CONSTRUCTED"
	# Graph Construction End Time
	graphEndTime = datetime.datetime.now()

	graphElapsedTime = graphEndTime - graphStartTime

	print " Graph Construction Elapsed Time: " + str(graphElapsedTime.total_seconds())


	
def countAccepted(queryString, alphabet, finalDfaTable, finalEndStates):
	ret = 0
	accepted = traverseInput(queryString, alphabet, finalDfaTable, finalEndStates)
	print "ACCEPTED: " + str(accepted)
	ret += len(accepted)
	return ret
	

def getDFA(regex):	
	inpt = regex
	ret = 0
	if isValidRegEx(inpt):
		# NFA Generation Start Time
		nfaStartTime = datetime.datetime.now()

		#inpt, datastructed = datStructPass1(inpt, [])
		datastructed = datStructPass1a(inpt, [], len(inpt))
		#print datastructed
		datastructed = datStructPass2(datastructed)
		#print datastructed
		datastructed = datStructPass3(datastructed)
		#print datastructed
		datastructed = datStructPass4(datastructed)
		#print datastructed
		listAlpha, tableHeader = getInptAlpha(datastructed)
		#print "ALPHABET"
		#print listAlpha
		#print tableHeader
		table = []
		table.append(tableHeader)
		table, rowrstart, rowrend = cvtRegexToNfa(datastructed, listAlpha, table, 0, 1)
		#for row in table:
		#	print row
		table = epsilonReduction(table)
		#print "START STATE : 0"
		#print "END STATE : 1"

		# NFA Generation End Time
		nfaEndTime = datetime.datetime.now()

		nfaElapsedTime = nfaEndTime - nfaStartTime

		print "" #extra line when using the operator '<' in running python
		print "NFA TABLE"
		for row in table:
			print row
		#print "NFA TABLE"
		print "NFA Elapsed Time in seconds: " + str(nfaElapsedTime.total_seconds())

		# DFA Generation Start Time
		dfaStartTime = datetime.datetime.now()

		populateDFATable(table, 0, 1)

		#print "ECLOSURE TABLE"

		#for a in eclosureTable:
		#	print a

		#print "DFA TABLE"
		tableHeader.pop(-1)
		#print tableHeader
		#for a in dfaTable:
		#	print a
		#print "DFA TABLE"

		startState = markStartState(dfaTable, 0)
		#print "START STATE: \n" + str(startState)
		endState = markEndState(dfaTable, 1)
		#print "END STATES: \n" + str(endState)

		#print "RENAMING STATES"
		tempDfaTable = []
		for i, row in enumerate(dfaTable):
			newRow = []
			newRow.extend(row)
			newRow.append(i)
			tempDfaTable.append(newRow)
		
		#for row in tempDfaTable:
			#print row

		finalDfaTable = []
		for i, row in enumerate(dfaTable):
			newRow = []
			for item in row:
				newState = str(getNewStateName(item, tempDfaTable))
				#print " OLD STATE: " + str(item)
				#print " NEW STATE: " + str(newState)
				newRow.append(newState)
			finalDfaTable.append(newRow)
		#print "RENAMING STATES"
		
		# DFA Generation End time
		dfaEndTime = datetime.datetime.now()

		dfaElapsedTime = dfaEndTime - dfaStartTime
		
		print "DFA"
		print tableHeader
		for row in finalDfaTable:
			print row
		#print "DFA"
		print "DFA Elapsed Time in seconds: " + str(dfaElapsedTime.total_seconds())

		finalStartStates = []
		for state in startState:
			finalStartStates.append(getNewStateName(state, tempDfaTable))
		#print "START STATES: " + str(finalStartStates)

		finalEndStates = []
		for state in endState:
			finalEndStates.append(getNewStateName(state, tempDfaTable))
		#print "END STATES: " + str(finalEndStates)

		alphabet = getAlphabet(tableHeader)
		#print "ALPHABET: " + str(alphabet)

		#constructGraph(finalDfaTable, finalEndStates, finalStartStates, alphabet)
	#reset everything
	global sst1
	global statecounter
	global i1a
	global indx
	global dfaTable
	global eclosureTable
	sst1 = []
	statecounter = 2
	i1a = 0
	indx = 0
	dfaTable = []#final answer
	eclosureTable = [] #where eclosures are stored
		
	return alphabet, finalDfaTable, finalEndStates


	
'''	
inputFile = raw_input("input filename: ")
countCapitalWords = countAccepted("[A-Z][A-Z]+ |[A-Z][A-Z]+,|[A-Z][A-Z]+." ,inputFile)
countDollarSign = countAccepted("$+" ,inputFile)
countWordYou = countAccepted("you|YOU" ,inputFile)
countWordMillion = countAccepted("(M|m)illion" ,inputFile)
countWordWeightLoss = countAccepted("(L|l)ose *(W|w)eight|(W|w)eight *(L|l)oss" ,inputFile)
countWordFree = countAccepted("FREE|free" ,inputFile)
countTotalWords = countAccepted(" *" ,inputFile)
threshCapitalWords = 0
threshDollarSign = 0
threshWordYou = 0
threshWordMillion = 0
threshWeightLoss = 0
threshWordFree = 0
print "SPAM DETECTOR FEATURE REPORT %s"%(inputFile)
print "    capital word count: " + str(countCapitalWords) + " trhesh: " + str(threshCapitalWords)
print "     dollar sign count: " + str(countDollarSign) + " trhesh: " + str(threshDollarSign)
print "        word you count: " + str(countWordYou) + " trhesh: " + str(threshWordYou)
print "    word million count: " + str(countWordMillion) + " trhesh: " + str(threshWordMillion)
print "word weight loss count: " + str(countWordWeightLoss) + " trhesh: " + str(threshWeightLoss)
print "       word free count: " + str(countWordFree) + " trhesh: " + str(threshWordFree)
print "mail1 total word count: " + str(countTotalWords) 
'''
inptfl = "rawdata.csv"
spamreader = []
processed = []
alphabet1, finalDfaTable1, finalEndStates1 = getDFA("[A-Z][A-Z]+ |[A-Z][A-Z]+,|[A-Z][A-Z]+.")
alphabet2, finalDfaTable2, finalEndStates2 = getDFA("$+")
alphabet3, finalDfaTable3, finalEndStates3 = getDFA("(y|Y)ou|YOU")
alphabet4, finalDfaTable4, finalEndStates4 = getDFA("(M|m)illion")
alphabet5, finalDfaTable5, finalEndStates5 = getDFA("(L|l)ose *(W|w)eight|(W|w)eight *(L|l)oss")
alphabet6, finalDfaTable6, finalEndStates6 = getDFA("FREE|(f|F)ree")
alphabet7, finalDfaTable7, finalEndStates7 = getDFA("(W|w)(i|o)n|W(I|O)N")
alphabet8, finalDfaTable8, finalEndStates8 = getDFA("(P|p)orn|PORN")
alphabet9, finalDfaTable9, finalEndStates9 = getDFA("(S|s)ex|SEX")
alphabet10, finalDfaTable10, finalEndStates10 = getDFA("(N|n)ude|NUDE")
alphabet11, finalDfaTable11, finalEndStates11 = getDFA("(J|j)ackpot|JACKPOT")
alphabet12, finalDfaTable12, finalEndStates12 = getDFA("(P|p)rize|PRIZE")
alphabet13, finalDfaTable13, finalEndStates13 = getDFA("(D|d)iscount|DISCOUNT")
alphabet14, finalDfaTable14, finalEndStates14 = getDFA("(S|s)ale|SALE")
alphabet15, finalDfaTable15, finalEndStates15 = getDFA("(V|v)irus|VIRUS")
alphabet16, finalDfaTable16, finalEndStates16 = getDFA("(C|c)ongratulations|(C|c)ongrats|CONGRATULATIONS|CONGRATS")
alphabet17, finalDfaTable17, finalEndStates17 = getDFA("(re|a|RE|A)ward|(RE|A)WARD")
alphabet18, finalDfaTable18, finalEndStates18 = getDFA("(U|u)rgent|URGENT")
alphabet19, finalDfaTable19, finalEndStates19 = getDFA("(C|c)lient|CLIENT")
alphabet20, finalDfaTable20, finalEndStates20 = getDFA("(C|c)ustomer|CUSTOMER")
alphabet21, finalDfaTable21, finalEndStates21 = getDFA("(C|c)ash|CASH")
alphabet22, finalDfaTable22, finalEndStates22 = getDFA("[0-9]+")
alphabet23, finalDfaTable23, finalEndStates23 = getDFA("(C|c)laim|CLAIM")
alphabet24, finalDfaTable24, finalEndStates24 = getDFA("(P|p)rivate|PRIVATE")
alphabet25, finalDfaTable25, finalEndStates25 = getDFA("(E|e)xclusive|EXCLUSIVE")
alphabet26, finalDfaTable26, finalEndStates26 = getDFA("(G|g)uarantee|GUARANTEE")
alphabet27, finalDfaTable27, finalEndStates27 = getDFA("(A|a)pply|APPLY")
alphabet28, finalDfaTable28, finalEndStates28 = getDFA("(A|a)sap|ASAP")
alphabet29, finalDfaTable29, finalEndStates29 = getDFA("(M|m)oney|MONEY")
alphabet30, finalDfaTable30, finalEndStates30 = getDFA("(S|s)ubscribe|SUBSCRIBE")
alphabet999, finalDfaTable999, finalEndStates999 = getDFA(" *")
totalCount = 5573.0 
trainingEndIndex = int(totalCount * 0.7)
testingStartIndex = trainingEndIndex
with open(inptfl, 'rb') as csvfile:
	spamreader = csv.reader(csvfile)
	for i, row in enumerate(spamreader):
		cnt1 = countAccepted(row[1], alphabet1, finalDfaTable1, finalEndStates1)
		cnt2 = countAccepted(row[1], alphabet2, finalDfaTable2, finalEndStates2)
		cnt3 = countAccepted(row[1], alphabet3, finalDfaTable3, finalEndStates3)
		cnt4 = countAccepted(row[1], alphabet4, finalDfaTable4, finalEndStates4)
		cnt5 = countAccepted(row[1], alphabet5, finalDfaTable5, finalEndStates5)
		cnt6 = countAccepted(row[1], alphabet6, finalDfaTable6, finalEndStates6)
		cnt7 = countAccepted(row[1], alphabet7, finalDfaTable7, finalEndStates7)
		cnt8 = countAccepted(row[1], alphabet8, finalDfaTable8, finalEndStates8)
		cnt9 = countAccepted(row[1], alphabet9, finalDfaTable9, finalEndStates9)
		cnt10 = countAccepted(row[1], alphabet10, finalDfaTable10, finalEndStates10)
		cnt11 = countAccepted(row[1], alphabet11, finalDfaTable11, finalEndStates11)
		cnt12 = countAccepted(row[1], alphabet12, finalDfaTable12, finalEndStates12)
		cnt13 = countAccepted(row[1], alphabet13, finalDfaTable13, finalEndStates13)
		cnt14 = countAccepted(row[1], alphabet14, finalDfaTable14, finalEndStates14)
		cnt15 = countAccepted(row[1], alphabet15, finalDfaTable15, finalEndStates15)
		cnt16 = countAccepted(row[1], alphabet16, finalDfaTable16, finalEndStates16)
		cnt17 = countAccepted(row[1], alphabet17, finalDfaTable17, finalEndStates17)
		cnt18 = countAccepted(row[1], alphabet18, finalDfaTable18, finalEndStates18)
		cnt19 = countAccepted(row[1], alphabet19, finalDfaTable19, finalEndStates19)
		cnt20 = countAccepted(row[1], alphabet20, finalDfaTable20, finalEndStates20)
		cnt21 = countAccepted(row[1], alphabet21, finalDfaTable21, finalEndStates21)
		cnt22 = countAccepted(row[1], alphabet22, finalDfaTable22, finalEndStates22)
		cnt23 = countAccepted(row[1], alphabet23, finalDfaTable23, finalEndStates23)
		cnt24 = countAccepted(row[1], alphabet24, finalDfaTable24, finalEndStates24)
		cnt25 = countAccepted(row[1], alphabet25, finalDfaTable25, finalEndStates25)
		cnt26 = countAccepted(row[1], alphabet26, finalDfaTable26, finalEndStates26)
		cnt27 = countAccepted(row[1], alphabet27, finalDfaTable27, finalEndStates27)
		cnt28 = countAccepted(row[1], alphabet28, finalDfaTable28, finalEndStates28)
		cnt29 = countAccepted(row[1], alphabet29, finalDfaTable29, finalEndStates29)
		cnt30 = countAccepted(row[1], alphabet30, finalDfaTable30, finalEndStates30)
		cnt999 = countAccepted(row[1], alphabet999, finalDfaTable999, finalEndStates999)
		row.append(str(cnt1)) 
		row.append(str(cnt2)) 
		row.append(str(cnt3)) 
		row.append(str(cnt4)) 
		row.append(str(cnt5)) 
		row.append(str(cnt6)) 
		row.append(str(cnt7)) 
		row.append(str(cnt8))  
		row.append(str(cnt9))  
		row.append(str(cnt10))  
		row.append(str(cnt11))  
		row.append(str(cnt12))  
		row.append(str(cnt13))  
		row.append(str(cnt14))
		row.append(str(cnt15)) 
		row.append(str(cnt16)) 
		row.append(str(cnt17)) 
		row.append(str(cnt18))  
		row.append(str(cnt19))  
		row.append(str(cnt20)) 
		row.append(str(cnt21)) 
		row.append(str(cnt22)) 
		row.append(str(cnt23)) 
		row.append(str(cnt24)) 
		row.append(str(cnt25)) 
		row.append(str(cnt26)) 
		row.append(str(cnt27)) 
		row.append(str(cnt28))  
		row.append(str(cnt29))  
		row.append(str(cnt30))   
		row.append(str(cnt999)) 
		processed.append(row)
		print i
for row in processed:
	print row

with open('preprocessed.csv', mode='w') as pp2:
    pp2 = csv.writer(pp2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in processed:
		pp2.writerow(row)
