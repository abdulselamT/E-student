from django.shortcuts import render,redirect
from .forms import *
from django.forms import inlineformset_factory
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.forms import inlineformset_factory
# Create your views here.
def generatetranscript():
	students=Student.objects.all()
	for k in students:
		semister=Semister.objects.get(active=True)
		section=Assesment.objects.filter(student=k).first().section
		Transcript.objects.create(student=k,grade=k.enroll_year,semister=semister,section=section)



def generatetotal():
	students=Student.objects.all()
	semister=Semister.objects.get(active=True)
	
	for k in students:
		tot=0
		c=1
		transcript=Transcript.objects.filter(student=k,semister=semister).first()
		asses=Assesment.objects.filter(student=k,semister=semister.semister)
		a=0
		b=1
		for j in asses :
			if not j.result:
				transcript.total=None
				transcript.complete=False
				transcript.save()
				c=0
				break
			else:
				if j.result >= 50:
					j.status='green'
				elif j.result>=40:
					j.status='yellow'
					a+=1
				else:
					j.status='red'
					transcript.complete=False
					transcript.save()
					a+=1
				j.save()
				tot+=j.result
		asses=Assesment.objects.filter(student=k,semister=semister.semister)
		if (c==1 and  a>=4) or ( a==3 and tot/len(asses)<55) or ( a==2 and tot/len(asses)<53) or ( a==1 and tot/len(asses)<51):
			transcript.total=tot
			transcript.complete=False
			transcript.avg=tot/len(asses)
			transcript.save()
		elif c==1:
			transcript.total=tot
			transcript.avg=tot/len(asses)
			transcript.complete=True
			transcript.save()

def generatecourseallstanding():
	
	semister=Semister.objects.get(active=True)
	grades=Grade.objects.all()
	for j in grades:
	
		courses=Course.objects.filter(grade=j)
		for m in courses:
			sturank =Assesment.objects.filter(semister=semister.semister).filter(section__grade=j).filter(course=m).order_by('-result')
			cval=-1
			s=1
			jum=0
			for k in  sturank:
				if not k.result:
					continue
				if k.result == cval:
					
					k.standing_all=s
					cval=k.result
					jum+=1
					k.save()
				else:
					s+=jum
					cval=k.result
					k.standing_all=s
					jum=1
					k.save()
				k.save()






def generatecoursesectionstanding():
	
	semister=Semister.objects.get(active=True)
	sections=Section.objects.all()
	for j in sections:
		courses=Course.objects.filter(grade=j.grade)
		for m in courses:
			sturank=Assesment.objects.filter(semister=semister.semister).filter(section=j).filter(course=m).order_by('-result')
			cval=-1
			s=1
			jum=0
			for k in  sturank:
				if not k.result:
					continue
				if k.result == cval:
					
					k.standing_sec=s
					cval=k.result
					jum+=1
					k.save()
				else:
					s+=jum
					cval=k.result
					k.standing_sec=s
					jum=1
					k.save()
				k.save()


def generatesectionstanding():
	semister=Semister.objects.get(active=True)
	sections=Section.objects.all()
	for j in sections:
		sturank=Transcript.objects.filter(complete=True,semister=semister,section=j).order_by('-total')
		cval=-1
		s=1
		jum=0
		for k in  sturank:
			if k.total == cval:
				
				k.standing_sec=s
				cval=k.total
				jum+=1
				k.save()
			else:
				s+=jum
				cval=k.total
				k.standing_sec=s
				jum=1
				k.save()
			k.save()

def generateallstanding():
	semister=Semister.objects.get(active=True)
	grades=Grade.objects.all()
	for j in grades:
		sturank=Transcript.objects.filter(complete=True,semister=semister,grade=j).order_by('-total')
		cval=-1
		s=1
		jum=0
		for k in  sturank:
			if k.total == cval:
				
				k.standing_all=s
				cval=k.total
				jum+=1
				k.save()
			else:
				s+=jum
				cval=k.total
				k.standing_all=s
				jum=1
				k.save()
			k.save()






def generateteacher():
	x="teacher"
	gradelist=Grade.objects.all()
	n=len(gradelist)
	sectionlist=Section.objects.all()
	m=len(sectionlist)
	for j in range(25):
		group=Group.objects.get(name='teacher')
		User.objects.create(username=x+str(j)).groups.add(group)
		y=User.objects.last()
		print(y.id)
		y.set_password(2*(x+str(j)))
		user=y.save()
		y=User.objects.last()
		#user.groups.add(group)
		dep=Department.objects.all()
		teacher=Teacher.objects.create(user=y,first_name=x+str(j),last_name="myfa",department=dep[j%len(dep)])
def generate():
	x="student"
	gradelist=Grade.objects.all()
	n=len(gradelist)
	for j in range(300):
		group=Group.objects.get(name='student')
		User.objects.create(username=x+str(j)).groups.add(group)
		y=User.objects.last()
		y.set_password(2*(x+str(j)))
		user=y.save()
		y=User.objects.last()
		#user.groups.add(group)
		std=Student.objects.create(user=y,first_name=x+str(j),last_name="myfa",ministry_result=85,matric_result=6.9,emergency_contact_name="emer",emergency_phone_number="gjj",enroll_year=gradelist[j%n])
		l=Course.objects.all().filter(grade=std.enroll_year)
		sectionlist=Section.objects.filter(grade=std.enroll_year)
		m=len(sectionlist)
		std.section = sectionlist[j%m]
		std.save()
		for k in l:
			Assesment.objects.create(course=k,student=std,section=std.section,semister='semisterI')
			Assesment.objects.create(course=k,student=std,section=std.section,semister='semisterII')
@login_required(login_url='login')
@allowed_users(['student'])
def registerstud(request):

	customerform=CustomerForm(instance=request.user.student)
	if request.method=="POST":
		customerform=CustomerForm(request.POST,request.FILES,instance=request.user.student)
		if  customerform.is_valid():
			customerform.save()
			messages.success(request,"registered successfully")
			return redirect('home')
	context={"customerform":customerform}
	return render(request,'student/registerrr.html',context)

def teacher(request):
	form=CreateUserForm()
	customerform=TeacherForm()
	if request.method=="POST":
		form=CreateUserForm(request.POST)
		customerform=TeacherForm(request.POST)
		if form.is_valid() and customerform.is_valid():
			group=Group.objects.get(name='teacher')
			user=form.save()
			user.groups.add(group)
			customer=customerform.save(commit=False)
			customer.user=user
			customer.save()
			messages.success(request,"registered successfully" + str(user))
			return redirect('home')
	context={"form":form,"customerform":customerform}
	return render(request,'student/registerrr.html',context)

def arrangment(request):
	customerform=ArrangementForm()
	if request.method=="POST":
		customerform=ArrangementForm(request.POST)
		if customerform.is_valid():
			customer=customerform.save()
			messages.success(request,"registered successfully" )
			l=customer.section.all()
			for k in l:
				students=Student.objects.filter(section=k)
				for j in students:
					temp=Assesment.objects.get(student=j,course=customer.course)
					temp.teacher=customer.teacher
					temp.save()
			return redirect('home')
	context={"customerform":customerform}
	return render(request,'student/arrange.html',context)
@unauthenticated_user
def loginpage(request):
	if request.method=="POST":
		username=request.POST.get('username')
		password=request.POST.get('password')
		user = authenticate(username=username,password=password)
		if user is not None:
			login(request ,user)
			return redirect('home')
	return render(request,'student/login.html')


def logoutpage(request):
	logout(request)
	return redirect('login')

def studentslist(request):
	students =Student.objects.all()
	context={'object_list':students}
	return render(request,'student/student_list.html',context)

@login_required(login_url='login')
@student_only
def studenthome(request):
	context={}
	return render(request,'student/homepage.html',context)
def teacherhome(request):
	context={}
	return render(request,'student/teacherhomepage.html',context)


@login_required(login_url='login')
@allowed_users(['teacher'])
def teacherpage(request):
	arr=TeacherArrangment.objects.filter(teacher=request.user.teacher)
	l=[]
	for k in arr:
		print(k.section.all())
		l+=k.section.all()

	context={'arr':arr,'sectionlist':l}
	return render(request,'student/teacherview.html',context)
@login_required(login_url='login')
@allowed_users(['student'])
def assesmentresult(request):
	assesments=Assesment.objects.filter(student=request.user.student).filter(asgt__contains = 'assesmenttype').filter(semister='semisterI')
	context={'assesments':assesments}
	if request.method=='POST':
		c=request.POST.get('asm')
		print(c)
		print("yess")
		result=Assesment.objects.get(id=c)
		tt=0
		tot=0
		xy=result.asgt
		for z in xy:
			if xy[z]['result']!='':
				tt+=float(xy[z]['result'])
			tot+=float(xy[z]['maximummark'])
		result.total=tt
					
	
		context={'assesments':assesments,'result':result,'total':tot}
		return render(request,'student/assesmentresult.html',context)
	return render(request,'student/assesmentresult.html',context)


def registeruser(request):
	if request.method=='POST':
		for n in range(8):
			mn=request.POST.get('user'+str(n))
	extras=[i for i in range(8)]
	context={'extra':extras}
	return render(request,'student/reg.html',context)

@login_required(login_url='login')
@allowed_users(['teacher'])
def assesmenttype(request):
	tar=TeacherArrangment.objects.filter(teacher=request.user.teacher)
	if request.method=='POST':
		z=request.POST.get('asm')
		x=request.POST.get('name')
		y=request.POST.get('maxmark')
		astpe=request.POST.get('tpe')
		print(z,x,y)
		ta=TeacherArrangment.objects.get(id=z)
		assesment=Assesment.objects.filter(teacher=ta.teacher,course=ta.course).filter(semister='semisterI')
		for k in assesment:
			if x in k.asgt :
				return HttpResponse("2 names must not be the same ")
			k.asgt[x]={'assesmenttype':astpe,'maximummark':y,'result':''}
			
			k.save()
	context={'asm':tar}
	return render(request,'student/type.html',context)

@allowed_users(['teacher'])
def fillmark(request,pk):
	y=Section.objects.get(id=pk)
	z=Assesment.objects.filter(semister='semisterI').filter(teacher=request.user.teacher).filter(finished=False).filter(section=y)
	
	if z:
		tt=z[0].asgt
		
	else:
		return HttpResponse('<h1>you have submitted the form to change you should goto administrator<h1/>')
	x=z.filter(student__section=y)
	print("here is working" )
	if request.method=='POST':
		calctot=request.POST.get('calculatetotal')
		fin=request.POST.get('finished')
		
		
		for j in x:
			tot=0
			for m in tt:
				asde=request.POST.get(str(j.student)+str(m))
				if calctot !='None':
					if asde != '':
						tot+=float(asde)
				j.asgt[m]['result']=asde
				
				j.save()
			fin = str(fin)	
			if fin !='None':
				j.result=tot
				print('finished')
				if tot<40:
					j.status='red'
				if tot<50:
					j.status='yellow'
				else:
					j.status='green'
				
				j.save()
		if fin !='None':
			print(x)
			sturank=x.order_by('-result')
			print(sturank)
			print('student rank ',len(sturank))
			cval=-1
			s=1
			jum=0
			for k in  sturank:
				k.finished=True
				k.save()
				print(k.student,'['+str(k.result) +','+str(k.standing)+'],')
				if not k.result:
					continue
				if k.result == cval:
					
					k.standing=s
					cval=k.result
					jum+=1
					k.save()
				else:
					s+=jum
					cval=k.result
					k.standing=s
					jum=1
					k.save()
				k.save()

	context={'students':x,'tt':tt}
	return render(request,'student/fill.html',context)



@login_required(login_url='login')
@allowed_users(['department'])
def arrangetea(request):
	depart=Department.objects.get(id=request.user.department.id)
	arranges=TeacherArrangment.objects.filter(course__department=depart)
	courses=Course.objects.filter(department=depart)
	teachers=Teacher.objects.filter(department=depart)
	if request.method=='POST':
		tchr=Teacher.objects.get(id=request.POST.get('tr'))
		crse=Course.objects.get(id=request.POST.get('cr'))
		semister=request.POST.get('semr')
		#arran=TeacherArrangment.objects.filter(teacher=tchr,course=crse)
		TeacherArrangment.objects.create(teacher=tchr,course=crse,semister=semister)
	context={'courses':courses,'teachers':teachers,'course':'Course:-','teacher':'Teacher:-','arranges':arranges,'semister':'s'}
	return render(request,'student/registerrr.html',context)

@login_required(login_url='login')
@allowed_users(['department'])
def sectioning(request,pk):
	tar=TeacherArrangment.objects.get(id=pk)
	cour=tar.course.grade
	cid=tar.course

	cid=cid.course_id
	
	mysection=set({})
	m=Section.objects.filter(grade=cour)
	for k in m:
		if not k.withcourse[cid]:
			mysection.add(k)
	courses=tar.course
	teachers=tar.teacher
	se=TeacherArrangment.objects.all()
	allocatedsection=TeacherArrangment.objects.filter(teacher=teachers).filter(course__course_id=cid)[0].section.all()
	
	if request.method=='POST':
		checkedlis=request.POST.getlist('check')
		for j in checkedlis:
			se=Section.objects.get(id=j)
			se.withcourse[cid]=1
			se.save()
			tar.section.add(se)
			tar.save()
			asesmentss=Assesment.objects.filter(course=tar.course).filter(section=Section.objects.get(id=j))
			for asm in asesmentss:
				asm.teacher=teachers
				asm.save()

	context={'courses':courses,'teachers':teachers,'sections':mysection,'course':'Course:-','section':'unallocated Sections:-','teacher':'Teacher:-','allocatedsection':allocatedsection}
	return render(request,'student/sectioning.html',context)
@login_required(login_url='login')
@allowed_users(['department'])
def teacherarrange(request):
	depart=Department.objects.get(id=request.user.department.id)
	
	courses=Course.objects.filter(department=depart)
	teachers=Teacher.objects.filter(department=depart)
	sections=Section.objects.all()
	if request.method=='POST':
		tchr=Teacher.objects.get(id=request.POST.get('tr'))
		crse=Course.objects.get(id=request.POST.get('cr'))
		checkedlis=request.POST.getlist('check')
		arran=TeacherArrangment.objects.filter(teacher=tchr,course=crse)
		x=TeacherArrangment.objects.create(teacher=tchr,course=crse)
		for j in checkedlis:
			x.section.add(Section.objects.get(id=j))
			x.save()
			asesmentss=Assesment.objects.filter(course=x.course).filter(section=Section.objects.get(id=j))
			for asm in asesmentss:
				asm.teacher=tchr
				asm.save()


	context={'courses':courses,'teachers':teachers,'sections':sections,'course':'Course:-','section':'Sections:-','teacher':'Teacher:-'}
	return render(request,'student/registerrr.html',context)

def registercourse(request):
	#generatecoursesectionstanding()
	#generatecourseallstanding()
	#generatesectionstanding()
	#generateallstanding()
	#generatetranscript()
	generatetotal()
	#generate()
	#generateteacher()
	depts=Department.objects.all()
	grades=Grade.objects.all()
	if request.method=='POST':
		x=request.POST.get('crid')
		y=request.POST.get('crn')
		t=request.POST.get('dp')
		u=request.POST.get('gr')
		c=Course.objects.create(course_id=x,course_name=y,department=Department.objects.get(id=t),grade=Grade.objects.get(id=u))
		sec=Section.objects.filter(grade=u)
		for j in sec:
			j.withcourse[c.course_id]=0
			j.save()
	context={'depts':depts,'grades':grades}
	return render(request,'student/regcourse.html',context)



@login_required(login_url='login')
@allowed_users(['teacher'])
def teacherupdate(request):
	tear=request.user.teacher
	customerform=TeacherForm(instance=tear)
	if request.method=="POST":
		customerform=TeacherForm(request.POST,request.FILES,instance=tear)
		if   customerform.is_valid():
			customer=customerform.save()
			messages.success(request,"registered successfully")
			
	context={"customerform":customerform}
	return render(request,'student/registerrr.html',context)

@login_required(login_url='login')
@allowed_users(['department'])
def departmenthomepage(request):
	context={}
	return render(request,'student/departmenthomepage.html',context)
def transcript(request):
	print('yessssssssssss')
	semister=Semister.objects.get(active=True)
	print(type(semister.semister))
	x=Assesment.objects.filter(student=request.user.student).filter(semister=semister.semister)
	print("I ti sokay")
	y=Transcript.objects.filter(student=request.user.student).filter(semister=semister).filter(grade=request.user.student.enroll_year).first()
	context={'assesments':x,'totaltr':y}
	return render(request,'student/transcript.html',context)

