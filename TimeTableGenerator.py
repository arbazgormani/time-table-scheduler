import xlrd
import random
import pandas as pd
import numpy as np
class TimeTableGenerator:
	
	def __init__(self, filename,worksheetname):

		self.fileName = filename
		self.workSheetName = worksheetname
		self.timeTableDetails = []
		self.timeTable = []
		self.dictionary = {}
		self.preferences = {}

	def readFile(self):
		dictionary = {}		#Dictionary of timeTable
		pref = {}				# Preference Soft Constraints
		df = pd.read_csv(self.fileName)
		writer = pd.ExcelWriter('test.xlsx')
		df.to_excel(writer, index = False)
		writer.save()
		workbook = xlrd.open_workbook('test.xlsx')
		# print workbook.sheet_names()
		worksheet = workbook.sheet_by_name(self.workSheetName)
		self.timeTableDetails.append(worksheet.cell(0,1).value)
		self.timeTableDetails.append(worksheet.cell(1,1).value)
		self.timeTableDetails.append(worksheet.cell(2,1).value)
		self.timeTableDetails.append(worksheet.cell(3,1).value)
		i = 6
		while (i < worksheet.nrows):
			group = worksheet.cell(i,0).value
			if (group == "Preferences"):
				i += 1
				group = worksheet.cell(i,0).value
				while (i < worksheet.nrows):
					pref[worksheet.cell(i,0).value] = worksheet.cell(i,1).value
					i += 1
			else:
				classDetails = []
				for column in range(1,7):
					# print worksheet.cell(i, column).value
					temp = []
					temp.append(worksheet.cell(i, column).value)
					temp.append(worksheet.cell(i+1, column).value)
					classDetails.append(tuple(temp))
					# classDetails.append(tuple(temp))
					
				dictionary[group] = classDetails
				i += 2
		# print dictionary
		self.dictionary = dictionary
		self.preferences = pref	
		pass

	def makeGroupsFortimeTable(self):
		dictionary = self.dictionary
		groupsList = []
		keys = dictionary.keys()
		for k in keys:
			values = dictionary[k]
			# print values
			for num,val in enumerate(values):
				groupDetails = []
				key = k
				course = "C"+str(num+1)		## Course number
				teacher = val[0]
				groupDetails.append(key)
				groupDetails.append(course)
				groupDetails.append(teacher)

				if (float(val[1]) == 1):				## if have 3 classes of 1 hour in a week
					numClasses = 3
					groupDetails.append(2)
					for i in range(numClasses):
						groupsList.append(tuple(groupDetails))
				elif (float(val[1]) == 1.5):		## if have 2 classes of 1.5 hour in a week
					numClasses = 2
					groupDetails.append(3)
					for i in range(numClasses):
						groupsList.append(tuple(groupDetails))
		return groupsList
		pass
		## Make a random Population(in this case making 1 timeTable) of timeTable giving random values to genes

	def generateChromosome(self,groupsList):		# making 1 chromosome
		chromosome = []
		# i = 0
		for group in groupsList:
	# 		# print group
			day = random.randint(0,4)	# 5 days
			room = random.randint(0,int(self.timeTableDetails[2])-1)
			timeSlot = -1	# if no slot append -1
	# 		## 0 to 6 slots of 1 hour classes and 7 to 14 for 1.5 hour classes
			if (group[3] == 2):		# 1 hour class
				timeSlot = random.randint(7,14)
			else:	# 1.5 hour class
				timeSlot = random.randint(0,6)
	# 		# print "hello"
			sectionClassDetails = []	# Details of classes of each section in each slot
			sectionClassDetails.append(str(day))
			sectionClassDetails.append(str(timeSlot))
			# sectionClassDetails.append(str(timeSlot)
			sectionClassDetails.append(str(room))
			sectionClassDetails.append(list(group))
			chromosome.append(sectionClassDetails)
	# 		# print ("he           llo")
	# 	    # print timeTable[i]
			# i += 1
	# 	# print timeTable
		# print chromosome
		return chromosome
		pass

	def evaluateSoftConstraints(self,chromosome):
		clashes = []
		cost = 0
		i = 0
		length = len(chromosome)
		# print length,len((chromosome))
		while i < length:    
			hasClash = False		## If chromosome of each slot has clash or not
			# for key in self.preferences.keys():
			# 	if chromosome[i][3][2] == key and self.preferences[key] == "m":
			# 		if (int(chromosome[i][1]) > 7 ):
			# 			cost += 20
			# 			hasClash = True
			# 	elif chromosome[i][3][2] == key and self.preferences[key] == "e":
			# 		if (int(chromosome[i][1]) < 7 ):
			# 			cost += 20
			# 			hasClash = True  
			# start time for 1 hour classes
			courseInd = chromosome[i][3][3]
			timeSlot = chromosome[i][1]
			if courseInd == 2 and timeSlot == "15":
				cost += 20
				hasClash = True
			# start time for 1.5 hour classes
			courseInd = chromosome[i][3][3]
			timeSlot = chromosome[i][1]
			if courseInd == 3 and (timeSlot == "14" or timeSlot == "15"):
				cost += 20
				hasClash = True       
			if hasClash == True:
				clashes.append(chromosome[i])
				chromosome.remove(chromosome[i])
			length = len(chromosome)
			i+=1
		return cost, clashes, chromosome

	def evaluateHardConstraints(self,chromosome):
		clashes = []
		cost = 0
		i = 0
		length = len(chromosome)
		# print length,len((chromosome))
		while i < len(chromosome):
			j = i + 1     
			while j < len(chromosome):

				# print i," i] j ",j," arbaz ",len(chromosome)
				hasClash = False		## If chromosome of each slot has clash or not
				# Classroom cannot be shared by two or more classes at a time.
				day = chromosome[i][0]
				timeSlot = chromosome[i][1]
				room = chromosome[i][2]
				if day == chromosome[j][0] and timeSlot == chromosome[j][1] and room == chromosome[j][2]:
					cost += 100
					hasClash = True
				# #consecutive slots for 1 hour classes
				# courseInd = chromosome[j][3][3]
				# day = chromosome[i][0]
				# timeSlot = chromosome[i][1]
				# if courseInd == 2 and day == chromosome[j][0] and (int(timeSlot)+1==int(chromosome[j][1])):
				# 	hasClash = True
				# 	cost += 1
				# # #consecutive slots for 1.5 hour classes
				# courseInd = chromosome[j][3][3]
				# day = chromosome[i][0]
				# timeSlot = chromosome[i][1]
				# if courseInd == 3 and day == chromosome[j][0] and (int(timeSlot)+1 == int(chromosome[j][1]) or int(timeSlot) + 2 == int(chromosome[j][1])):
				# 	hasClash = True
				# 	cost += 1 
				#Friday Constraints
				day = chromosome[j][0]
				timeSlot = chromosome[j][1]
				course = chromosome[j][3][3]
				if course == 2 and day == "4" and (timeSlot =="7" or timeSlot == "8" or timeSlot =="9"):
					cost += 50
					hasClash = True
				elif course == 3 and day == "4" and (timeSlot == "6" or timeSlot =="7" or timeSlot == "8" or timeSlot =="9"):
					cost += 50
					hasClash = True
				# A teacher cannot teach more than one class at a time.
				room = chromosome[i][3][2]
				day = chromosome[i][0]
				timeSlot = chromosome[i][1]
				if room == chromosome[j][3][2] and day == chromosome[j][0] and timeSlot == chromosome[j][1]:
					cost += 100
					hasClash = True
				#A group or Batch Section has no two classes of same course in one day
				# print i,j,chromosome[j]
				course = chromosome[i][3][1]
				batch = chromosome[i][3][0]
				day = chromosome[i][0]
				if course == chromosome[j][3][1] and batch == chromosome[j][3][0] and day == chromosome[j][0]:
					cost += 100
					hasClash = True 
				if hasClash == True:
					clashes.append(chromosome[j])
					chromosome.remove(chromosome[j])
				j+=1
				length = len(chromosome)
			i+=1
		return cost, clashes, chromosome
	def calculateFitness(self,chromosome):
		cost = 20000
		count = 0
		while cost > 100:
			if count == 500:		## Repopulattion and Generate New Chromosome
				count = 0
				chromosome = self.generateChromosome(self.makeGroupsFortimeTable())
			print (cost)
			costHard,clashes,chromosome = self.evaluateHardConstraints(chromosome)
			costSoft,clashesSoft,chromosome = self.evaluateSoftConstraints(chromosome)
			cost = costHard + costSoft
			newGenes = self.mutation(clashes)
			for ng in newGenes:
				chromosome.append(ng)
			newGenes = self.mutation(clashesSoft)
			for ng in newGenes:
				chromosome.append(ng)
			count += 1
		self.timeTable = chromosome
	def mutation(self,genes):
		newGenes = []
		for gene in genes:
			day = random.randint(0,4)	# 5 days
			room = random.randint(0,int(self.timeTableDetails[2])-1)
			timeSlot = -1	# if no slot append -1
	# 		## 0 to 6 slots of 1 hour classes and 7 to 14 for 1.5 hour classes
			# print gene
			if (gene[3][3] == 3):		# 1.5 hour class
				timeSlot = random.randint(0,6)
			else:	# 1 hour class
				timeSlot = random.randint(7,14)
	# 		# print "hello"
			sectionClassDetails = []	# Details of classes of each section in each slot
			sectionClassDetails.append(str(day))
			sectionClassDetails.append(str(timeSlot))
			# sectionClassDetails.append(str(timeSlot)
			sectionClassDetails.append(str(room))
			sectionClassDetails.append(gene[3])
			# print sectionClassDetails
			newGenes.append(sectionClassDetails)
		return newGenes
		pass
	# def crossOver(self,chromosome):
	# 	splitPoint  = random.randint(0,len(chromosome)-1)
	# 	crossOver = chromosome[splitPoint]