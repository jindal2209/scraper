# coun = 0
def CreateExcel(path,filename):
	import pdfplumber
	import re

	pdf = pdfplumber.open(path)
	data = pdf.pages

	# global coun
	# coun = 0

	outputPDf = str('D:\\Shubham\\Shubham\\BPIT\\Results\\scraper\\generated_excels\\'+filename + '' + '.csv')
	resultantFile = open(outputPDf,'a')

	def subjectList():
		page = data[0].extract_text()			## all subjects info is present on page 1
		subject_list = {}
		match = re.compile(r'^(\d{2}) (\d+) \w+ \w+.*')
		for line in page.split('\n'):
			if match.match(line.strip()):
				sno,sid,scode,*sname,credit,typeofexam,exam,mode,kind,minor,major,maxmarks,passmarks = line.split()
				subject_list[int(sid.strip())] = [scode.strip(),' '.join(sname)]

		return subject_list


	def instituteList():
		## returning variables
		institute_list = {}
		branch_list = {}
		semester = ''

		## regex matchers
		matchInstitute = re.compile(r'\AInstitution Code')
		matchBranch = re.compile(r'\AScheme of Programme Code')
		matchResult = re.compile(r'\AResult of Programme Code:')
		matchCurrInstitute = re.compile(r'\AS.No. photo.',flags=re.IGNORECASE)
		matchRollNumber = re.compile(r'^\d{11}')

		## helper variables
		currBranch = ''
		currBatch = ''
		currExaminationType = ''
		currInstitute = ''
		checkStudentResult = False

		for p in data:
			page = p.extract_text().split('\n')
			page = iter(page)
			for line in page :
				if checkStudentResult == True :
					if matchRollNumber.match(line):
						internal_list = []
						external_list = []
						total_list = []
						grade_list = []
						
						rollnumber = line.split()[0]
						subject_id_list = re.findall(r'([0-9]+)\(', line, re.IGNORECASE)
						subject_id_list = [int(i) for i in subject_id_list]
						name = next(page,None).strip()

						internal_external_marks = next(page,None)
						internal_external_marks = internal_external_marks.split()[2:]
						internal_external_marks = iter(internal_external_marks)
						for i in internal_external_marks :
							internal_list.append(i)
							external_list.append(next(internal_external_marks,None))

						next(page,None)
						
						total_marks = next(page,None).strip()
						# total_marks = '1  69(A) 69(A) 75(A+) 65(A) 79(A+) 69(A) 84(A+) 75(A+) 73(A) 75(A+) 81(A+) 78(A+)'
						total_marks = total_marks.split()[1:]
						for i in total_marks:
							if i.upper() in ['A','C','D','RL','AP','A(F)']:
								total_list.append('A')
								grade_list.append('F')
								continue
							grade_search = re.search(r'\(([A-Za-z\+]+)\)', i, re.IGNORECASE)
							marks_search = re.search(r'([0-9]+)\(', i, re.IGNORECASE)
							total_list.append(marks_search.group(1))
							grade_list.append(grade_search.group(1))

						res = []
						res.append(rollnumber)
						res.append(name)	
						res.append(semester)
						res.append(currBatch)
						res.append(currInstitute)
						res.append(institute_list[currInstitute])  ##institute code
						res.append(currBranch)
						res.append(branch_list[currBranch])
						
						for i in range(len(subject_id_list)) :
							res.append(subject_list[subject_id_list[i]][0])
							res.append(subject_list[subject_id_list[i]][1])
							try:
								s = int(internal_list[i])
								res.append(internal_list[i])
							except ValueError:
								res.append('0')
							res.append(external_list[i])
							res.append(total_list[i])
							res.append(grade_list[i])

						res = ','.join(res)
						
						## writing final result to file
						resultantFile.write('\n')
						resultantFile.write(res)
						# global coun
						# coun += 1

					else:
						checkStudentResult = False
				elif matchInstitute.match(line):
					checkStudentResult = False
					ins,co,code,nameinit,*name = line.split()
					code = code.strip()
					institute_list[code] = ' '.join(name).replace(',','')
				elif matchBranch.match(line):
					checkStudentResult = False
					a,b,c,d,branchCode,e,f,*branchName,g,h,i,semnumber,j = line.split()
					branchCode = branchCode.strip()
					branch_list[branchCode] = ' '.join(branchName)
					semester = semnumber
				elif matchResult.match(line):
					checkStudentResult = False
					currBranch = re.search('Code: (.*) Programme', line, re.IGNORECASE).group(1).strip()
					currBatch = re.search('Batch: (.*) E', line, re.IGNORECASE).group(1).strip()
					currExaminationType = re.search('Examination: (.*) [A-Z]', line, re.IGNORECASE).group(1).strip()
					# row_data = line.split()
					# currBranch = row_data[4]
					# currBatch = row_data[18]
					# currExaminationType = row_data[20]
				elif matchCurrInstitute.match(line):
					title_search = re.search('Institution Code: (.*) Institution:', line, re.IGNORECASE)
					if title_search:
						currInstitute = title_search.group(1).strip()
						checkStudentResult = True			## now from next line we will have data


		# return (institute_list,branch_list,semester)
			
			

	subject_list = subjectList() 			# key will be subjectID value will be [code,name]

	st = ['enrollment_number', 'student_name', 'semester', 'batch', 'college_code', 'college_name', 'branch_code', 'branch_name']
	for i in range(len(subject_list)):
		st.append('subjectcode{i}'.format(i=i))
		st.append('subjectname{i}'.format(i=i))
		st.append('internalmark{i}'.format(i=i))
		st.append('externalmark{i}'.format(i=i))
		st.append('total{i}'.format(i=i))
		st.append('obtainedcredit{i}'.format(i=i))

	st = ','.join(st)
	resultantFile.write(st)


	instituteList() 		# key will be code value will be name
	# print('Parsed {coun} records'.format(coun=coun))

	resultantFile.close()
import os
path = 'D:\\Shubham\\Shubham\\BPIT\\Results\\scraper\\generated_pdfs\\'
files_list = os.listdir(path)
for fi in files_list:
	CreateExcel(path=path+fi , filename=fi)
