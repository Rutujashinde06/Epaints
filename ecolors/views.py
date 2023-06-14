from django.shortcuts import render,redirect
from django.http import HttpResponse
from ecolors.models import Paints
from django.contrib.auth.models import User
from ecolors.models import Paints,Cart,Order,OrderHistory
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth  import authenticate,logout,login
from ecolors.forms import EmpForm,ProductModelForm,UserForm
import random

from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def index(request):
    data=Paints.objects.filter(status=1)
    content={}
    content['paints']=data
    return render(request,'index.html',content)



def user_register(request):
     content={}
     regobj=UserForm()
     print(regobj)
     content['userform']=regobj
     if request.method=="POST":
           regobj=UserForm(request.POST)
           if regobj.is_valid():
            regobj.save()
            content['success']="User Created Successfully"
            return render(request,'user_register.html',content)

     else:
         return render(request,'user_register.html',content)


def user_login(request):
     if request.method=="POST":
           dataobj=AuthenticationForm(request=request,data=request.POST)
           #print(dataobj)
           if dataobj.is_valid():
                uname=dataobj.cleaned_data['username']
                upass=dataobj.cleaned_data['password']
                #print(uname)
                #print(upass)
                u=authenticate(username=uname,password=upass)
                #print(u)
                if u:
                     login(request,u)
                     return redirect('/')
     else:
          obj=AuthenticationForm()
          content={}
          content['loginform']=obj
          return render(request,'user_login.html',content)
     
def user_logout(request):
    logout(request)
    return redirect('/login')     

def addshade(request):
    if request.method== "POST":
        n=request.POST['name']
        c=request.POST['cat']
        amt=request.POST['price']
        s=request.POST['status']
        p=Paints.objects.create(name=n,cat=c,price=amt,status=s)
        p.save()
        return redirect('/addshade')
    else:    
        p=Paints.objects.all()
        content={}
        content['paints']=p
        return render(request,'addshade.html',content) 
        user_id=request.user.id
        print("Id of the logged in User:",user_id)
    if user_id:
        print("Id of the logged in User:",user_id)
    else:
        return redirect('/login')    
    
    
def editshade(request,rid):
    print('Id to be edited:',rid)
    
    if request.method=="POST":
        upname=request.POST['name']
        ucat=request.POST['cat']
        uprice=request.POST['price']
        ustatus=request.POST['status']

        print(upname)
        print(ucat)
        print(uprice)
        print(ustatus)
        p=Paints.objects.filter(id=rid)
        p.update(name=upname,cat=ucat,price=uprice,status=ustatus)
        return redirect('/addshade')


    else:
        p=Paints.objects.filter(id=rid)
        content={}
        content['paints']=p
        return render(request,'editshade.html',content)

def sort(request,sv):
    if sv=='0':
        param="price"
    else:    
         param="-price"
    data=Paints.objects.order_by(param).filter(status=1)
    content={}
    content['paints']=data
    return render(request,'index.html',content)   


def catfilter(request,catv):
    q1=Q(cat=catv)
    q2=Q(status=1)
    data=Paints.objects.filter(q1 & q2)
    content={}
    content['paints']=data
    return render(request,'index.html',content)


def pricefilter(request,pv):
    q1=Q(status=1)
    if pv=='0':
        q2=Q(price__lt=5000)
    else:
        q2=Q(price__gte=5000)

    data=Paints.objects.filter(q1 & q2)
    content={}
    content['paints']=data
    return render(request,'index.html',content)

def pricerange(request):
    low=request.GET['min']
    high=request.GET['max']
    # print(low)
    # print(high)
    q1=Q(status=1)
    q2=Q(price__gte=low)
    q3=Q(price__lte=high)
    q4=Q(price__gt=0)
    data=Paints.objects.filter(q1 & q2 & q3)
    content={}
    content['paints']=data
    return render(request,'index.html',content)

def delshade(request,rid): 
   p=Paints.objects.filter(id=rid)
   p.delete()
   return redirect('/addshade')



def color_details(request,pid):
   # print("Id of the product:",pid)
    data=Paints.objects.filter(id=pid)
    content={}
    content['paints']=data
    return render(request,'color_details.html',content)

def addtocart(request,pid):
    
    if request.user.is_authenticated:
        userid=request.user.id
        #print("User ID:",uid)
        #print("Product Id",pid)
        q1=Q(pid=pid)
        q2=Q(uid=userid)
        
        c=Cart.objects.filter(q1 & q2)
        # u=User.objects.filter(id=userid)
       # print(u[0])
        p=Paints.objects.filter(id=pid)
        content={}
        content['paints']=p
        if c:
            content['msg']="product Already Exist in the cart"
            return render(request,'color_details.html',content)
        else:
            u=User.objects.filter(id=userid)
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            content['success']="Product Added in cart"
            return render(request,"color_details.html",content)
    else:
        return redirect('/login')
    

def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
   # print(c)
   # print(c[0])
   # print(c[0].pid)
   # print(c[0].uid)
    sum=0 
    for x in c:
   #  print(type(x.qty))
    # print(type(x.pid.price))
     sum=sum+(x.qty*x.pid.price)
    print("Total Product Price:",sum)
    content={}
    content['paints']=c
    content['nitems']=len(c)
    content['total']=sum
    print(len(c))
    return render(request,'viewcart.html',content)    


def changeqty(request,pid,f):
    content={}
    c=Cart.objects.filter(pid=pid)
    if f=='1':
        x=c[0].qty+1
    else:
        x=c[0].qty-1

    if x>0:
        c.update(qty=x)
    return redirect('/viewcart') 




def placeorder(request):
    oid=random.randrange(1000,9999)
   # print(oid)
    user_id=request.user.id
    c=Cart.objects.filter(uid=user_id)
   # print(c)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    o=Order.objects.filter(uid=user_id)
    sum=0     
    for x in o:
         sum=sum+(x.qty*x.pid.price)
    content={}
    content['products']=o
    content['nitems']=len(o)
    content['total']=sum

    return render(request,'placeorder.html',content)

'''
def makepayment(request):
    print("In make payment function")
    userid=request.user.id
    client = razorpay.Client(auth=("rzp_test_0J3OWLUUsNXvYg", "7Ha7uEedHfUpMxIZY7FunB7L"))
    o=Order.objects.filter(uid=userid)
    oid=str(o[0].id)
    sum=0
    for x in o:
        sum=sum+(x.qty*x.pid.price)
    sum=sum*100 #conversion of RS into Paise    
    data = { "amount": sum, "currency": "INR", "receipt":oid }
    payment = client.order.create(data=data)
    print(payment)
    content={}
    content['payment']=payment
    return render(request,'pay.html',content)

def storedetails(request):
    pay_id=request.GET['pid']
    order_id=request.GET['oid']
    sign=request.GET['sign']
    userid=request.user.id
    u=User.objects.filter(id=userid)
  #  print(pay_id)
  #  print(order_id)
  #  print(sign)
    email=u[0].email
    msg="Order Placed Successfully. Details are Payment ID:"+pay_id+" and OrderId is:"+order_id
    send_mail(
        "Order Status-Ekart",
        msg,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    oh=OrderHistory.objects.create(order_id=order_id,pay_id=pay_id,sign=sign,uid=u[0])
    return render(request,'finalpage.html')

  '''