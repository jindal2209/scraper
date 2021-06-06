import PyPDF2
import numpy as np
import pandas as pd
from PyPDF2 import PdfFileReader, PdfFileWriter

def CREATEXLSFROMPDF(path, filename):

	## return raw text from parsed pdf
	def FindAllRawTextfromPDF(PdfPath):
		rawText = ''
		pdf = PyPDF2.PdfFileReader(open(PdfPath, 'rb'))
		for page in pdf.pages:
			rawText += page.extractText()
		# rawText = pdf.getPage(15).extractText()
		return rawText

	D1 = FindAllRawTextfromPDF(path).split('\n')

	def IndexexofStudentsData(D1):
		ans = []
		for i in range(len(D1)):
			if D1[i].find('(SCHEME OF EXAMINATIONS)') > -1:
				ans.append(i)
		ans.append(len(D1) - 1)
		return ans

	LLforIndexesSD = IndexexofStudentsData(D1)


	## returns semester number
	def FindSemesterNumberformFirstRow(L):
		SemNumber = 0
		for i in range(len(L)):
			if L[i].find('SEMESTER') > -1:
				L2 = L[i].split(' ')
				if len(L2) > 1:
					for o in range(len(L2)):
						if L2[o].find('SEMESTER') > -1:
							if o > 0:
								SemNumber = L2[o - 1]
								break
			if L[i].find('Sem./Year:') > -1:
				L3 = L[i].split(' ')
				if len(L3) > 1 and i < len(L3) - 1:
					for e in range(len(L3)):
						if L3[e].find('Sem./Year:') > -1:
							if e > 0:
								SemNumber = L3[e + 1]
								break
		return SemNumber

	def FindDeclaredDate(L):
		ans = ''
		for i in range(len(L)):
			if L[i].find('RTSID:') > -1:
				ans = (L[i])[7:15]
				break
		return ans

	## this will return whether the exam was for regular,reappear or rechecking
	def FindExaminationStatus(L):
		ans = ''
		for i in range(len(L)):
			if L[i].find('Examination:') > -1:
				NL = L[i].split(' ')
				for j in range(len(NL)):
					if NL[j].find('Examination:') > -1:
						ans = NL[j + 1]
						break
		if len(ans) == 0:
			for i in range(len(L)):
				if L[i].find('Examinat') > -1:
					NL = L[i + 1].split(' ')
					for j in range(len(NL)):
						if NL[j].find('ion:') > -1:
							ans = NL[j + 1]
							break
		if len(ans) == 0:
			for i in range(len(L)):
				if L[i].find('Examination:') > -1:
					NL = L[i + 1].split(' ')
					ans = NL[0]
					break

		if ans.find('REG') > -1:
			ans = 'REGULAR'

		if ans.find('REC') > -1:
			ans = 'RECHECKING'

		if ans.find('REV') > -1:
			ans = 'REVISED'

		if ans.find('REA') > -1:
			ans = 'REAPPEAR'

		return ans


	def EvaluatePCPN(L):
		PC = ''
		PN = ''
		i1 = 0
		i2 = 0
		L1 = []
		L2 = []
		for i in range(len(L)):
			if L[i].find('Scheme of Programme Code:') > -1 \
				or L[i].find('Programme Code:') > -1:
				L1 = L[i].split(' ')
				i1 = i
				break
		for i in range(len(L1)):
			if L1[i].find('Code:') > -1:
				PC = L1[i + 1]
				break
		for i in range(len(L1)):
			if L1[i].find('Name:') > -1:
				for j in L1[i + 1:]:
					PN = PN + j
				break

		for i in range(len(L)):
			if L[i].find('SchemeID:') > -1 or L[i].find('Sem./Year:') \
				> -1:
				L2 = L[i].split(' ')
				i2 = i
				break

		for i in range(i1 + 1, i2):
			PN = PN + L[i]

		for i in range(len(L2)):
			if L2[i].find(')') > -1:
				PN = PN + L2[i]
				break
			PN = PN + L2[i] + ' '

		return (PC, PN)


	def FindALLDetailsUsingCode(L, code):
		for i in L:
			if code.find(i[0]) > -1:
				return i


	def CreateUniqueElementListforProgram(L):
		output1 = []
		for x in L:
			if x[0] not in output1:
				output1.append(x[0])
		ans = []
		for i in output1:
			ans.append(FindALLDetailsUsingCode(L, i))
		return ans

	def CreateActualBranchName(L):
		ans = []
		ans.append(L[0])
		branchname = ''
		x = 0

		for i in range(len(L[1])):
			if L[1][i].find(')') > -1:
				x = i
				break

		for i in range(0, x + 1):
			branchname += L[1][i]

		ans.append(branchname)
		return ans


	def ISGetCredit(L):
		L1 = L.split(' ')
		ans = False
		L2 = ''
		for i in L1:
			if i.isdigit():
				L2 += i
				break
		if len(L2) == 1:
			ans = True
		return ans


	## returns list of all subjects and their details
	def FindALLPeperID(L):
		pid = []
		pcode = []
		pname = []
		Ans = []
		tp = []
		for i in range(len(L)):
			if len(L[i]) == 5 or len(L[i]) == 6:
				if L[i].isdigit():
					L1 = []
					pid.append(L[i])
					pcode.append(L[i + 1])
					L1.append(L[i])
					L1.append(L[i + 1])

					if ISGetCredit(L[i + 3]):
						pname.append(L[i + 2])
						L1.append(L[i + 2])
						L1.append(L[i + 3])
						L1.append(L[i + 4])
						L1.append(L[i + 7])
					else:
						pname.append(L[i + 2] + L[i + 3])
						L1.append(L[i + 2] + L[i + 3])
						L1.append(L[i + 4])
						L1.append(L[i + 5])
						L1.append(L[i + 8])

					Ans.append(L1)
		return (Ans, pid, pname, pcode)


	## returns list of subject code
	def CreateUniqueElementListforsubject(L):
		output1 = []
		for x in L:
			if x[1] not in output1:
				output1.append(x[1])
		return output1


	## returns details of subject whose subject-code is passed as parameter
	def FindALLDetailsUsingCode(L, code):
		for i in L:
			if code.find(i[1]) > -1:
				return i


	## returns Institute Code and Institute Name
	def EvaluateICIN(L):
		IC = ''
		IN = ''
		i1 = 0
		i2 = 0
		L1 = []
		L2 = []
		for i in range(len(L)):
			if L[i].find('Institution Code:') > -1 \
				or L[i].find('Institution:') > -1:
				L1 = L[i].split(' ')
				i1 = i
				break
		for i in range(len(L1)):
			if L1[i].find('Code:') > -1:
				IC = L1[i + 1]
				break
		for i in range(len(L1)):
			if L1[i].find('Institution:') > -1:
				for j in L1[i + 1:]:
					IN = IN + j + ' '
				break
		IN = IN[:-1]

		endIndexforIN = 0
		for i in range(len(L)):
			if L[i].find('S.No.') > -1:
				endIndexforIN = i
				break

		for i in range(i1 + 1, endIndexforIN):
			IN = IN + L[i]
		return (IC, IN)


	## returns student id from the string
	def RemoveSID(s1):
		return s1[s1.index(':', 0, len(s1)) + 2:len(s1)]


	## returns scheme id from the string
	def RemoveSchemaID(s2):
		return s2[s2.index(':', 0, len(s2)) + 2:len(s2)]


	## returns subject id and maximum credits that can be obtained
	def RemoveBrakets(S):
		A = []
		i1 = S.find('(')
		i2 = S.find(')')
		A.append(S[0:i1])
		A.append(S[i1 + 1:i2])
		return A


	## returns internal and external marks
	def RemoveSpaces(S):
		if S.find(' ') < 0:
			return S
		else:
			A = []
			S1 = S.split(' ')
			for i in range(len(S1)):
				if len(S1[i]) > 0:
					A.append(S1[i])
			return A


	## returns student data in the format [enrollment number , name , studentID , schemeID , then subjects details in following format , credits , 00]
	## [subject code , max credits , internal marks , external marks , total marks , grade , ... then for next subject]
	def CreateEfficientDatafromRawofStudent(i1, i2, L1):
		EfL = []
		L = []
		while i1 < i2:
			L.append(L1[i1])
			i1 += 1

		EfL.append(L[0])
		EfL.append(L[2])
		if L[4].find('SID:') > -1:
			EfL.append(RemoveSID(L[4]))
		else:
			EfL.append(L[4])
		if L[6].find('SchemeID:') > -1:
			EfL.append(RemoveSchemaID(L[6]))
		else:
			EfL.append(L[6])

		for i in range(7, len(L)):
			L[i] = L[i].strip()
			if L[i].find('AA') > -1 or L[i].find('DD') > -1 or L[i].find('CC') > -1:
				for i in range(4):
					EfL.append('A')
				continue
			if L[i].find('(') > -1:
				if 'A' in L[i] or 'D' in L[i] or 'C' in L[i] or 'L' in L[i]:
					L[i] = (L[i])[1:]
				BL = RemoveBrakets(L[i])
				for k2 in range(len(BL)):
					EfL.append(BL[k2])
				continue
			if L[i].find(' ') > -1:
				SL = RemoveSpaces(L[i])
				for k1 in range(len(SL)):
					EfL.append(SL[k1])
				continue
		EfL.append('00')
		return EfL


	def FindTotalSubject(L):
		TotalSIndexes = []
		for i in range(4, len(L)):
			if len(L[i]) == 5 or len(L[i]) == 6 or len(L[i]) == 7:
				if L[i].isdigit():
					TotalSIndexes.append(i)
		return TotalSIndexes


	## return a list of [subject id,max credits,internalmarks , external marks] // total marks need to be added
	def FillAllIE(L, i1, i2):
		Ans = []
		diff = i2 - i1
		Ans.append(L[i1])			## subject id
		Ans.append(L[i1 + 1])		## max credits
		if diff >= 5:
			if L[i1 + 2].isdigit():	## internal marks
				Ans.append(L[i1 + 2])
			else:
				Ans.append('A')

			if L[i1 + 3].isdigit():	## external marks
				Ans.append(L[i1 + 3])
			else:
				Ans.append('A')

			if L[i1 + 4].isdigit():	## total marks
				Ans.append(L[i1 + 4])
			else:
				Ans.append('A')

		else:
			if diff < 3:
				Ans.append('A')			## internal
				Ans.append('A')			## external
				Ans.append('A')			## total
			if diff >= 4:
				if L[i1 + 2].isdigit():	## internal
					Ans.append(L[i1 + 2])
				else:
					Ans.append('A')

				if L[i1 + 3].isdigit():	## external
					Ans.append(L[i1 + 3])
				else:
					Ans.append('A')

				if L[i1 + 4].isdigit():	## total marks
					Ans.append(L[i1 + 4])
				else:
					Ans.append('A')
		return Ans


	## return list of list where each list contains data of individual subject
	def AddPidIE(L):
		NumberofSubjectL = FindTotalSubject(L)
		TotalSubject = len(NumberofSubjectL)
		ans = []
		for i in range(len(NumberofSubjectL) - 1):
			ans.append(FillAllIE(L, NumberofSubjectL[i],NumberofSubjectL[i + 1]))
		ans.append(FillAllIE(L, NumberofSubjectL[len(NumberofSubjectL)- 1], len(L)))

		return ans


	## returns list with all details of student
	def ExtractOnlyMainFeatures(L, SemNumber, DeclaredDateofPDF):
		A = []
		A.append(L[0])
		A.append(L[1])
		A.append(L[2])
		A.append(L[3])
		A.append(SemNumber)
		A.append(DeclaredDateofPDF)
		A.append(AddPidIE(L))

		return A

	def CreateSubjectIDIEStringFinal2(L):
		Ans = []

		for i in range(len(L)):
			Ans.append(L[i][0])		## subject id
			Ans.append(L[i][1])		## max credits
			Ans.append(L[i][2])		## internal marks
			Ans.append('0')
			Ans.append('0')
			Ans.append('0')
			Ans.append(L[i][3])		## external marks
			Ans.append(L[i][4])		## total marks
		return Ans

	def CreateFinal2(L):
		LS = []
		LS.append(L[0])
		LS.append(L[1])
		LS.append(L[2])
		LS.append(L[3])
		LS.append(L[4])
		LS.append(L[5])
		ANSL = CreateSubjectIDIEStringFinal2(L[6])
		for i in range(len(ANSL)):
			LS.append(ANSL[i])
		return LS

	def CreateListforSubject(ML, i1, i2):
		Ans = []
		while i1 < i2:
			Ans.append(ML[i1])
			i1 += 1
		return Ans


	## return list containing details of student
	def CreateCommonInformation(L):
		Ans = []
		for i in range(6):
			Ans.append(L[i])
		return Ans

	def CreateSubjectRow(L):
		ans = []
		# TotalSubject = int((len(L) - 6) / 7)
		TotalSubject = int((len(L) - 6) / 8)		## dong 8 due to total marks also
		Indexes = []

		for i in range(TotalSubject):
			Indexes.append(6 + 8 * i)
		Indexes.append(Indexes[-1] + 8)

		for i in range(len(Indexes) - 1):
			li = CreateListforSubject(L, Indexes[i], Indexes[i + 1])
			ans.append(li)

		return ans


	def CreateAllLabaledData(L):
		ans = []
		ans.append(CreateCommonInformation(L))
		ans.append(CreateSubjectRow(L))

		return ans


	def EvaluateProgrammeInstituteName(x, L):
		ans = 'LATERAL ENTRY'
		for i in L:
			if i[0].find(x) > -1:
				ans = i[-1]
				break
		return ans


	def CreateCommonFeatureofStudent(L,NewAccuratePCPN,NewAccurateICIN,Examinationstatus,):
		Batch = '20' + (L[0])[9:11]
		RollNumber = (L[0])[0:3]
		InstituteCode = (L[0])[3:6]
		ProgrammeCode = (L[0])[6:9]
		ProgrammeName = ''
		InstituteName = ''
		NewAccurateICIN = list(NewAccurateICIN)

		if len(NewAccuratePCPN) == 2:
			ProgrammeName = NewAccuratePCPN[1]

		if len(NewAccurateICIN) == 2:
			InstituteName = NewAccurateICIN[1]

		ans = []

		for i in L:
			ans.append(i)

		ans.append(Batch)
		ans.append(RollNumber)
		ans.append(Examinationstatus)
		ans.append(InstituteCode)
		ans.append(InstituteName)
		ans.append(ProgrammeCode)
		ans.append(ProgrammeName)

		return ans


	def EvaluateSubjectNameList(x, L):
		ans = []
		for i in L:
			if i[0].find(x) > -1:
				ans = i[1:]
		return ans


	def FillSubjectNameCode(L, SubjectList):  # # f=getting individual subject marks list
		ansSNC = []
		ansSNC = EvaluateSubjectNameList(L[0], SubjectList)
		SubjectName = ''
		SubjectCode = ''
		SubjectType = ''
		SubjectTotalredit = ''
		SubjectKind = ''
		SubjectName = ansSNC[1]
		SubjectCode = ansSNC[0]
		SubjectTotalredit = ansSNC[2]
		SubjectKind = ansSNC[-1]
		SubjectType = ansSNC[-2]

		ans = []
		ans.append(L[0])
		ans.append(SubjectCode)
		ans.append(SubjectName)
		ans.append(SubjectType)
		ans.append(SubjectTotalredit)
		ans.append(SubjectKind)
		ans.append(L[1])		## credits obtained
		ans.append(L[2])		## internal marks
		ans.append(L[-2])		## external marks
		ans.append(L[-1])		## total marks

		return ans


	def CreateCommonFeatureofStudentSubject(L, SubjectList):
		ans = []
		for i in L:
			ans.append(FillSubjectNameCode(i, SubjectList))
		return ans


	def CreateLLforXLS(L,SubjectList,NewAccuratePCPN,NewAccurateICIN,Examinationstatus,) :
		ans1 = CreateCommonFeatureofStudent(L[0], NewAccuratePCPN,NewAccurateICIN, Examinationstatus)
		ans2 = CreateCommonFeatureofStudentSubject(L[-1], SubjectList)
		ans = []
		for i in ans1:
			ans.append(i)
		for i in ans2:
			for j in i:
				ans.append(j)

		return ans

	def CREATELLFORDATAFRAME(i1, i2, D):
		ans = []
		L1 = []

		while i1 < i2:
			L1.append(D[i1])
			i1 += 1

		SemNumber = FindSemesterNumberformFirstRow(L1)
		DeclaredDate = FindDeclaredDate(L1)
		Examinationstatus = FindExaminationStatus(L1)
		LforPCPN = EvaluatePCPN(L1)
		LforPCPN2 = []
		LforPCPN2.append(LforPCPN[0])
		LforPCPN2.append(LforPCPN[1])
		NewAccuratePCPN = CreateActualBranchName(LforPCPN2)
		ALLSubjectCodeNameID = FindALLPeperID(L1)
		output1 = CreateUniqueElementListforsubject(ALLSubjectCodeNameID[0])
		SubjectList = []
		for i in output1:
			SubjectList.append(FindALLDetailsUsingCode(ALLSubjectCodeNameID[0],i))

		NewAccurateICIN = EvaluateICIN(L1)

		EnrollmentNumbers = []
		EnrollmentNumbersIndexes = []
		for i in range(len(L1)):
			if len(L1[i]) == 11:
				if L1[i].isdigit():
					EnrollmentNumbersIndexes.append(i)
					EnrollmentNumbers.append(L1[i])

		EnrollmentNumbersIndexes.append(len(L1))

		LLforDSDB = []
		for i in range(len(EnrollmentNumbersIndexes) - 1):
			LLforDSDB.append(CreateEfficientDatafromRawofStudent(EnrollmentNumbersIndexes[i],EnrollmentNumbersIndexes[i + 1], L1))

		Final1LL = []
		for i in range(len(LLforDSDB)):
			Final1LL.append(ExtractOnlyMainFeatures(LLforDSDB[i],SemNumber, DeclaredDate))

		Datafram3dL = []
		for i in range(len(Final1LL)):
			Datafram3dL.append(CreateFinal2(Final1LL[i]))

		AfterLabelingCreateL = []
		for i in range(len(Datafram3dL)):
			AfterLabelingCreateL.append(CreateAllLabaledData(Datafram3dL[i]))

		LLforDataFrame = []
		for i in AfterLabelingCreateL:
			ans.append(CreateLLforXLS(i, SubjectList, NewAccuratePCPN,NewAccurateICIN, Examinationstatus))

		studentinformation = []
		subjectinformation = []

		return (ans, Final1LL)



	def CreateMainLLforDF(L, L1):
		for i in L1:
			L.append(i)
		return L

	NewLLforDF = []
	for i in range(len(LLforIndexesSD) - 1):
		CreateMainLLforDF(NewLLforDF,CREATELLFORDATAFRAME(LLforIndexesSD[i],LLforIndexesSD[i + 1], D1)[0])


	def CreateMainFinal1LL(L, L1):
		for i in L1:
			L.append(i)
		return L

	NewLLFinal1LL = []
	for i in range(len(LLforIndexesSD) - 1):
		CreateMainFinal1LL(NewLLFinal1LL,CREATELLFORDATAFRAME(LLforIndexesSD[i],LLforIndexesSD[i + 1], D1)[1])


	DataFrameS = pd.DataFrame(NewLLforDF)

	def CreateSubjectIDIEString(L):
		Ans = []

		for i in range(len(L)):
			Ans.append('subjectid' + str(i + 1))
			Ans.append('subjectcode' + str(i + 1))
			Ans.append('subjectname' + str(i + 1))
			Ans.append('subjecttype' + str(i + 1))
			Ans.append('subjecttotalcredit' + str(i + 1))
			Ans.append('subjectkind' + str(i + 1))
			Ans.append('obtainedcredit' + str(i + 1))
			Ans.append('internalmark' + str(i + 1))
			Ans.append('externalmark' + str(i + 1))
			Ans.append('totalmark' + str(i + 1))

		return Ans


	def CreateStringKeys(L):
		LS = []
		LS = [
			'enrollmentnumber',
			'name',
			'sid',
			'schemaid',
			'semester',
			'declareddate',
			'batch',
			'classrollnumber',
			'examinationtype',
			'institutecode',
			'institutename',
			'programmecode',
			'programmename',
			]
		ANSL = CreateSubjectIDIEString(L[6])
		for i in range(len(ANSL)):
			LS.append(ANSL[i])

		return LS

	MaxL = list()
	for i in range(len(NewLLFinal1LL)):
		MaxL.append(len(NewLLFinal1LL[i][6]))
	MaxL.sort()
	MAxNumberforKays = MaxL[-1]
	FinalIndexKeys = 0
	for i in range(len(NewLLFinal1LL)):
		if len(NewLLFinal1LL[i][6]) == MAxNumberforKays:
			FinalIndexKeys = i
			break

	KeysDF = CreateStringKeys(NewLLFinal1LL[FinalIndexKeys])
	DataFrameS.columns = KeysDF

	# outputPDf = str(filename + '' + '.csv')
	outputPDf = str('generated_excels//' + filename + '' + '.csv')

	DataFrameS.to_csv(outputPDf)

	return outputPDf



# path = 'D:\Shubham\Shubham\Results\ABCD.pdf'
# CREATEXLSFROMPDF(path, 'ABCD.pdf')