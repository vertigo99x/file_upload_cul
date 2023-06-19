from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages

from .models import Files, Folders, Activities, Allusers, Students

from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required

from django.db.models import Q

imgs=['jpg','jpeg','png','gif']
audios = ['mp3','m4a']
videos=['avi','mp4','mkv']



@register.filter
def strip(value):
    value = str(value)
    if len(value)>15:
        return f"{value[:15]}..."
    return value

@register.filter
def strip_longer(value):
    value = str(value)
    if len(value)>40:
        return f"{value[:40]}..."
    return value




def addActivity(data):
    activity = Activities.objects.create(
        recipient = data['recipient'],
        message = data['message']
    )
    
    activity.save();


@login_required
def dashboard(request):
    user = request.user
    context={}
    
    userdata = Allusers.objects.filter(user=user)[0]
    
    if userdata.usercat == 'student':
        name = Students.objects.filter(user = user).values()[0]['fullname']
        
        if len(name.split(' ')) >= 2:
            firstname = name.split(' ')[1]
        else:
            firstname = name.split(' ')[0]
        
        files = Files.objects.filter(user=user).filter(Q(status=1) | Q(status=0))
        folders = Folders.objects.filter(user=user)
        context['files'] = files
        context['folders'] = folders
        context['recent_files'] = files[:5]
        
        context['total_files'] = files.count()
        context['approved_files'] = files.filter(status=1).count()
        context['approved_percentage'] = int((context['approved_files'] / context['total_files'])*100)
    
    elif userdata.usercat == 'admin':
        context['files'] = Files.objects.filter(status=0)
    
    context['userData'] = userdata
    
    
    return render(request, 'dashboard.html', context)


@login_required
def approve(request, pk):
    Files.objects.filter(id=pk).update(status=1)
    user_file = Files.objects.filter(id=pk)[0].user
    addActivity({
            "recipient":"admin",
            "message":f"You Approved a File Approval Request From {user_file}",
        })
    return redirect('dashboard')


@login_required
def reject(request, pk):
    Files.objects.filter(id=pk).update(status=1)
    user_file = Files.objects.filter(id=pk)[0].user
    addActivity({
            "recipient":"admin",
            "message":f"You Declined a File Approval Request From {user_file}",
        })
    return redirect('dashboard')





@login_required
def history(request):
    user = request.user
    context={}
    context['userData'] = Allusers.objects.filter(user=user)[0]
    
    if context['userData'].usercat == 'admin':
        files = Files.objects.all()
        context['files'] = files
        return render(request,"history.html",context)
    
    return redirect('dashboard')


@login_required
def students(request):
    user = request.user
    context={}
    context['userData'] = Allusers.objects.filter(user=user)[0]
    
    if context['userData'].usercat == 'admin':
        students = Students.objects.all().values()
        
        context['students'] = students
        print(students)
        return render(request,"students.html",context)
    
    return redirect('dashboard')




@login_required
def notifications(request):
    user = request.user
    context={}
    
    files = Files.objects.filter(user=user)
    folders = Folders.objects.filter(user=user)
    context['files'] = files
    context['folders'] = folders
    context['total_files'] = files.count()
    context['approved_files'] = files.filter(status=1).count()
    context['approved_percentage'] = int((context['approved_files'] / context['total_files'])*100)
    context['userData'] = Allusers.objects.filter(user=user)[0]
    
   
    return render(request, 'notifications.html', context)


@login_required
def folderSort(request, folder_id):
    user = request.user
    context={}
    
    folder_name = Folders.objects.filter(id=folder_id).values()[0]['folder_name']
    
    filtered_files = Files.objects.filter(user=user, folder_name=folder_name)
    print(filtered_files)
    
    files = Files.objects.filter(user=user)
    print(files.values())
    folders = Folders.objects.filter(user=user)
    
    context['files'] = filtered_files
    context['folda_sort'] = folder_name
    context['folders'] = folders
    context['recent_files'] = files.filter(folder_name=folder_name)[:5]
    
    context['total_files'] = files.count()
    context['approved_files'] = files.filter(status=1).count()
    context['approved_percentage'] = int((context['approved_files'] / context['total_files'])*100)
    context['userData'] = Allusers.objects.filter(user=user)[0]
    
   
    return render(request, 'dashboard.html', context)




@login_required
def upload_file(request):
    if request.method == "POST":
        folder_name = request.POST['folder_name']
        file_name = request.POST['file_name']
        file_size = request.POST['file_size']
        file = request.FILES['file']
        
        file_str = f"{file}".split('.')[-1]
        
        try:
            file_size = float(file_size)
            
            print(file_size)
            if float(file_size) > 1048576:
                file_size = f"{file_size / 1048576}".split('.')[0] + '.' + f"{file_size / 1048576}".split('.')[1][:2] + "MB"
            elif float(file_size) > 1024:
                file_size = f"{file_size / 1024}".split('.')[0] + '.' + f"{file_size / 1024}"[1][:2] + "KB"
            else:
                file_size = f"{file_size}B"   
        
        except Exception:
            pass
        
        if file_str.lower().strip() in imgs:file_type="image"
        elif file_str.lower().strip() in audios:file_type="audio"
        elif file_str.lower().strip() in videos:file_type="video"
        else:file_type="document"
        
        user = request.user
        
        file = Files.objects.create(
            user=user,
            file_name = file_name,
            folder_name = folder_name,
            file = file,
            file_type = file_type,
            file_size = file_size,
        )
        
        file.save();
        
        student = Students.objects.filter(user = user).values()[0]
        mat_no = student['matric_no']
        fullname = student['fullname']
        
        
        addActivity({
            "recipient":"admin",
            "message":f"{fullname} with Matric No: {mat_no} Uploaded a file for Approval",
        })
        
        
    return redirect('dashboard')


@login_required
def createFolder(request):
    if request.method == "POST":
    
        folder_name = request.POST['folder_name'].upper()
        
        folder = Folders.objects.create(
            user = request.user,
            folder_name =folder_name
        )
        
        folder.save();

    return redirect('dashboard')






def login(request):
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']
        user = auth.authenticate(username = username, password = password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        
        messages.error(request, 'User Does Not Exist!!')
        return redirect('login')
    
    return render(request, 'login.html')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        
    return redirect('login')