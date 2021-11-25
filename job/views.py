from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
from .models import *


# Function For Home Page (For All)
def index(request):
	return render(request,'index.html')

# Admin Login Function
def admin_login(request):
	error = ""
	if request.method == 'POST':
		uname = request.POST['username']
		pwd = request.POST['pwd']
			
		user = authenticate(username=uname,password=pwd)
		try:
			if user.is_staff:
				login(request,user)
				error = "no"
			else:
				error = "yes"
		except:
			error = "yes"
	context = {
		"error":error
	}
	return render(request,'admin_login.html',context)

# User(Job Seeker) Function
def user_login(request):
	error = ""
	if request.method == 'POST':
		email = request.POST['email']
		pwd = request.POST['pwd']
			
		user = authenticate(username=email,password=pwd)
		if user:
			try:
				user1 = StudentUser.objects.get(user=user)
				if user1.usertype == "student":
					login(request,user)
					error = "no"
				else:
					error = "yes"
			except:
				error = "yes"
		else:
			error = "yes"
	context = {
		"error":error
	}
	return render(request,'user_login.html',context)

# Recruiter (Company Owner) Function
def recruiter_login(request):
	error = ""
	if request.method == 'POST':
		email = request.POST['email']
		pwd = request.POST['pwd']
			
		user = authenticate(username=email,password=pwd)
		if user:
			try:
				user1 = Recruiter.objects.get(user=user)
				if user1.usertype == "recruiter" and user1.status != "pending" and user1.status != "Reject":
					login(request,user)
					error = "no"
				else:
					error = "not"
			except:
				error = "yes"
		else:
			error = "yes"
	context = {
		"error":error
	}
	return render(request,'recruiter_login.html',context)

# User (Job Seeker) Registeration Function
def user_signup(request):
	error = ""
	if request.method == 'POST':
		fname = request.POST['fname']
		lname = request.POST['lname']
		contact = request.POST['contact']
		email = request.POST['email']
		pwd = request.POST['pwd']
		gender = request.POST['gender']
		img = request.FILES['image']

		if User.objects.filter(username=email):
			error = "same_user"
		else:
			try:
				user = User.objects.create_user(first_name=fname,last_name=lname,username=email,password=pwd)
				StudentUser.objects.create(user=user,mobile=contact,image=img,gender=gender,usertype="student")
				error="no"
			except:
				error="yes"
	context = {
		"error":error
	}
	return render(request,'user_signup.html',context)

# User (Job Seeker) Home Page Function. For Users Only
def user_home(request):
	if not request.user.is_authenticated:
		return redirect('user_login')
	user = request.user
	stduser = StudentUser.objects.get(user=user)
	error = ""
	if request.method == 'POST':
		fname = request.POST['fname']
		lname = request.POST['lname']
		contact = request.POST['contact']
		gender = request.POST['gender']

		stduser.user.first_name = fname
		stduser.user.last_name = lname
		stduser.mobile = contact
		stduser.gender = gender

		try:
			stduser.save()
			stduser.user.save()
			error="no"
		except:
			error="yes"

		try:
			img = request.FILES['image']
			stduser.image = img
			stduser.save()
			error="no"
		except:
			pass
	context = {
		"stduser":stduser,
		"error":error
	}
	return render(request,'user_home.html',context)	

# Persons Logout Function. For All Type of Users
def person_logout(request):
	logout(request)
	return redirect('/')

# Recruiter (Company Owner) Registeration Function
def recruiter_signup(request):
	error = ""
	if request.method == 'POST':
		fname = request.POST['fname']
		lname = request.POST['lname']
		contact = request.POST['contact']
		email = request.POST['email']
		pwd = request.POST['pwd']
		gender = request.POST['gender']
		img = request.FILES['image']
		company = request.POST['company']

		if User.objects.filter(username=email):
			error = "same_user"
		else:	
			try:
				user = User.objects.create_user(first_name=fname,last_name=lname,username=email,password=pwd)
				Recruiter.objects.create(user=user,mobile=contact,image=img,gender=gender,company=company,usertype="recruiter",status="pending")
				error="no"
			except:
				error="yes"
	context = {
		"error":error
	}
	return render(request,'recruiter_signup.html',context)

# Recruiter (Company Owner) Home Page Funtion. For Recruiter Only
def recruiter_home(request):
	if not request.user.is_authenticated:
		return redirect('recruiter_login')
	user = request.user
	recruiter = Recruiter.objects.get(user=user)
	error = ""
	if request.method == 'POST':
		fname = request.POST['fname']
		lname = request.POST['lname']
		contact = request.POST['contact']
		gender = request.POST['gender']

		recruiter.user.first_name = fname
		recruiter.user.last_name = lname
		recruiter.mobile = contact
		recruiter.gender = gender

		try:
			recruiter.save()
			recruiter.user.save()
			error="no"
		except:
			error="yes"

		try:
			img = request.FILES['image']
			recruiter.image = img
			recruiter.save()
			error="no"
		except:
			pass
	context = {
		"recruiter":recruiter,
		"error":error
	}
	return render(request,'recruiter_home.html',context)

# Admin Home Page Function. For Admin Only
def admin_home(request):
	if not request.user.is_staff:
		return redirect('admin_login')
	stduser = StudentUser.objects.all().count()
	recuser = Recruiter.objects.all().count()
	jobs = Jobs.objects.all().count()
	res = UserApply.objects.all().count()
	msg = Contact.objects.all().count()
	context = {
		"stduser":stduser,
		"recuser":recuser,
		"jobs":jobs,
		"res":res,
		"msg":msg
	}
	return render(request,'admin_home.html',context)	

# Users View Function. For Admin Only
def view_users(request):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	users_data = StudentUser.objects.all()
	context = {
		"users_data":users_data
	}
	return render(request,'view_users.html',context)

# Delete Users Function. For Admin Only
def delete_user(request,id):
	users_data = User.objects.get(id=id)
	users_data.delete()
	return redirect('view_users')		

# Recruiter's (Company Owner) Status View Function. For Admin Only
def recruiter_pending(request):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	recruiters_data = Recruiter.objects.filter(status="pending")
	context = {
		"recruiters_data":recruiters_data
	}
	return render(request,'recruiter_pending.html',context)

# Recruiter's (Company Owner) Status Change Function. For admin only
def change_status(request,id):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	error = ""
	recruiters_data = Recruiter.objects.get(id=id)
	if request.method == "POST":
		status = request.POST['status']
		recruiters_data.status = status
		try:
			recruiters_data.save()
			error = "no"
		except:
			error = "yes"
	context = {
		"recruiters_data":recruiters_data,
		"error":error
	}
	return render(request,'change_status.html',context)

# Recruiter's (Company Owner) Accept View Function. For Admin Only
def recruiter_accepted(request):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	recruiters_data = Recruiter.objects.filter(status="Accept")
	context = {
		"recruiters_data":recruiters_data
	}
	return render(request,'recruiter_accepted.html',context)

# Recruiter's (Company Owner) Rejection View Function. For Admin Only
def recruiter_rejected(request):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	recruiters_data = Recruiter.objects.filter(status="Reject")
	context = {
		"recruiters_data":recruiters_data
	}
	return render(request,'recruiter_rejected.html',context)

# All Recruiters (Company Owner) View Function. For Admin only
def all_recruiters(request):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	recruiters_data = Recruiter.objects.all()
	context = {
		"recruiters_data":recruiters_data
	}
	return render(request,'all_recruiters.html',context)

# Recruiter (Company Owner) Deletion Function. For Admin Only
def delete_recruiter(request,id):
	recruiter_data = User.objects.get(id=id)
	recruiter_data.delete()
	return redirect('all_recruiters')

# Change Password Function. For Admin Only
def change_passwordadmin(request):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	error = ""
	if request.method == "POST":
		crntpwd = request.POST['crntpwd']
		newpwd = request.POST['newpwd']
		try:
			user = User.objects.get(id=request.user.id)
			if user.check_password(crntpwd):
				user.set_password(newpwd)
				user.save()
				error = "no"
			else:
				error = "not"
		except:
			error = "yes"
	context = {
		"error":error
	}
	return render(request,'change_passwordadmin.html',context)

# Change Password Function. For User (Job Seeker) only
def change_passworduser(request):
	if not request.user.is_authenticated:
		return redirect('user_login')
	error = ""
	if request.method == "POST":
		crntpwd = request.POST['crntpwd']
		newpwd = request.POST['newpwd']
		try:
			user = User.objects.get(id=request.user.id)
			if user.check_password(crntpwd):
				user.set_password(newpwd)
				user.save()
				error = "no"
			else:
				error = "not"
		except:
			error = "yes"
	context = {
		"error":error
	}
	return render(request,'change_passworduser.html',context)

# Password Changing Function. For Recruiter (Company Owner) Only
def change_passwordrecruiter(request):
	if not request.user.is_authenticated:
		return redirect('recruiter_login')
	error = ""
	if request.method == "POST":
		crntpwd = request.POST['crntpwd']
		newpwd = request.POST['newpwd']
		try:
			user = User.objects.get(id=request.user.id)
			if user.check_password(crntpwd):
				user.set_password(newpwd)
				user.save()
				error = "no"
			else:
				error = "not"
		except:
			error = "yes"
	context = {
		"error":error
	}
	return render(request,'change_passwordrecruiter.html',context)

# Add New Job Function. For Recruiter (Company Owner) Only
def add_job(request):
	if not request.user.is_authenticated:
		return redirect('recruiter_login')
	error = ""
	if request.method == 'POST':
		jtitle = request.POST['jtitle']
		sdate = request.POST['sdate']
		edate = request.POST['edate']
		salary = request.POST['salary']
		clogo = request.FILES['clogo']
		experience = request.POST['experience']
		skills = request.POST['skills']
		location = request.POST['location']
		description = request.POST['description']
		
		user = request.user
		recruiter = Recruiter.objects.get(user=user)

		try:
			Jobs.objects.create(recruiter=recruiter,title=jtitle,description=description,
				salary=salary,experience=experience,location=location,skills=skills,
				image=clogo,start_date=sdate,end_date=edate,creation_date=date.today())
			error="no"
		except:
			error="yes"
	context = {
		"error":error
	}
	return render(request,'add_job.html',context)

# View All Added Jobs Function. For Recruiter (Company Owner) only
def job_list(request):
	if not request.user.is_authenticated:
		return redirect('recruiter_login')
	user = request.user
	recruiter = Recruiter.objects.get(user=user)
	recruiters_data = Jobs.objects.filter(recruiter=recruiter)
	context = {
		"recruiters_data":recruiters_data
	}
	return render(request,'job_list.html',context)

# Added Job Updation Function. For Recruiter (Company Owner) Only
def edit_jobdetail(request,id):
	if not request.user.is_authenticated:
		return redirect('recruiter_login')
	error = ""
	job = Jobs.objects.get(id=id)
	if request.method == 'POST':
		jtitle = request.POST['jtitle']
		sdate = request.POST['sdate']
		edate = request.POST['edate']
		salary = request.POST['salary']
		experience = request.POST['experience']
		skills = request.POST['skills']
		location = request.POST['location']
		description = request.POST['description']
		
		job.title = jtitle
		job.salary = salary
		job.experience = experience
		job.location = location
		job.skills = skills
		job.description = description

		try:
			job.save()
			error="no"
		except:
			error="yes"
		if sdate:
			try:
				job.start_date = sdate
				job.save()
			except:
				pass
		else:
			pass

		if edate:
			try:
				job.end_date = edate
				job.save()
			except:
				pass
		else:
			pass
	context = {
		"error":error,
		"job":job
	}
	return render(request,'edit_jobdetail.html',context)

# Company Logo Changing Function. For Recruiter (Company Owner) only
def change_companylogo(request,id):
	if not request.user.is_authenticated:
		return redirect('recruiter_login')
	error = ""
	job = Jobs.objects.get(id=id)
	if request.method == 'POST':
		clogo = request.FILES['clogo']
		
		job.image = clogo

		try:
			job.save()
			error="no"
		except:
			error="yes"
	context = {
		"error":error,
		"job":job
	}
	return render(request,'change_companylogo.html',context)

# Delete Added Job Function. For Recruiter (Company Onwer) only
def delete_job(request,id):
	users_data = Jobs.objects.get(id=id)
	users_data.delete()
	return redirect('job_list')	

# Latest Job Function. For All Users
def latest_jobs(request):
	jobs = Jobs.objects.all().order_by('-start_date')
	context = {
		"jobs":jobs
	}
	return render(request,'latest_jobs.html',context)

# Job List Function. For User (Job seeker) only
def user_joblist(request):
	jobs = Jobs.objects.all().order_by('-start_date')
	user = request.user
	student = StudentUser.objects.get(user=user)
	data = UserApply.objects.filter(user=student)
	li = []
	for i in data:
		li.append(i.job.id)
	context = {
		"jobs":jobs,
		"li":li
	}
	return render(request,'user_joblist.html',context)

# Added Job detail Function. For User (Job Seeker) only
def job_applydetail(request,id):
	job = Jobs.objects.get(id=id)
	context = {
		"job":job
	}
	return render(request,'job_applydetail.html',context)	

# Resume Upload Function. For User (Job Seeker) only
def apply_resume(request,jid):
	if not request.user.is_authenticated:
		return redirect('user_login')
	error = ""
	user = request.user
	user1 = StudentUser.objects.get(user=user)
	job = Jobs.objects.get(id=jid)
	date1 = date.today()
	if job.end_date < date1:
		error = "close"
	elif job.start_date > date1:
		error = "notopen"
	else:
		if request.method == "POST":
			res = request.FILES['resume']
			try:
				UserApply.objects.create(user=user1,job=job,resume=res)
				error = "no"
			except:
				error = "yes"
	context = {
		"error":error
	}
	return render(request,'apply_resume.html',context)

# List of applied candidates Function. For Recruiters (Company Owner) only
def applied_candidates(request):
	res = UserApply.objects.all()
	context = {
		"resume":res
	}
	return render(request,'applied_candidates.html',context)

# Contact Form Function. For All Users
def contact_form(request):
	error = ""
	if request.method == "POST":
		name = request.POST['name']
		email = request.POST['email']
		msg = request.POST['message']

		try:
			Contact.objects.create(name=name,email=email,message=msg)
			error = "no"
		except:
			error = "yes"
	context = {
		"error":error
	}
	return render(request,'contact_form.html',context)

# Messages View function. For Admin Only
def messages(request):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	msg = Contact.objects.all().order_by("-name")
	context = {
		"messages":msg
	}
	return render(request,'messages.html',context)

# Delete Message Function. For Admin Only
def delete_msgs(request,id):
	users_data = Contact.objects.get(id=id)
	users_data.delete()
	return redirect('messages')	

# # Search Messages Function By Sender Name, For Admin Only
# def search_msgs(request):
# 	if request.method == "POST":

# 		smsgs = request.POST.get('srMsgs')
# 		query = Contact.objects.filter(name__icontains=smsgs)

# 	context = {
# 		"srmsgs":query
# 	}
# 	return render(request,'search_messages.html',context)