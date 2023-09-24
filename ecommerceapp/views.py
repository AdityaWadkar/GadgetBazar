from django.shortcuts import render,redirect
from ecommerceapp.models import Contact,Product,Orders,OrderUpdate
from django.contrib import messages
from math import ceil
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.template.loader import render_to_string
from django.core.mail import send_mail
def home(request):

    prods =[]
    cat_prod = Product.objects.values('subcategory','id')
    cats = {item['subcategory'] for item in cat_prod}
    for cat in cats:
        prod = Product.objects.filter(subcategory=cat)
        n = len(prod)
        nSlides = n // 4 +ceil((n/4) - (n//4))
        prods.append([prod, range(1,nSlides),nSlides])
    params = {'allProds':prods}

    return render(request,"index.html",params)


def about(request):
    return render(request,"about.html")


def contact(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        desc = request.POST["desc"]
        number = request.POST["number"]
        myquery = Contact(name=name,email=email,description=desc,number=number)
        myquery.save()
        messages.info(request,"Request sent! We Will Contact You soon !!")
        return render(request,"contact.html")
    return render(request,"contact.html")


def checkout(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    
    return render(request,"checkout.html")


@csrf_exempt
def success(request):
    if request.method=="POST":
        item_json = request.POST["itemsJson"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        amount = request.POST["amt"]
        mobile_no = request.POST["phone"]
        pin_code = request.POST["zip_code"]
        email = request.POST["email"]
        address1 = request.POST["address1"]
        address2 = request.POST["address2"]
        landmark = request.POST["landmark"]
        city = request.POST["city"]
        state = request.POST["state"]
        Order = Orders(item_json=item_json,fname = fname,lname = lname,amount=amount,mobile_no=mobile_no,
                       pin_code=pin_code,email=email,address1=address1,address2=address2,
                       landmark=landmark,city=city,state=state)
        Order.save()
        # update =OrderUpdate(update_desc = "your order has been placed")

        # update.save()
        client = razorpay.Client(auth=(settings.MID, settings.MK))   
    
        payment = client.order.create(
            {'amount':int(amount)*100,
                'currency':"INR",
                'payment_capture':"1",
                })
        # print(f"************ {payment} *******")
        Order.razor_pay_order_id=payment['id']
        Order.save()
        context = {'amount': amount,
                   'api_key': settings.MID,
                   'order_id': payment['id'],
                   'name': fname+" "+lname,
                   'email': email,
                   'mobile':mobile_no,
                   }
        return render(request,'success.html',context)

       
    # print("int success.html but outside post condition")
    return render(request,'success.html')


@csrf_exempt
def paymentstatus(request):
    if request.method=="POST":
        # print("IN paymentstatus METHOD OF POST")
        a = request.POST
        order_id=""
        payment_id=""
        signature=""
        for key,val in a.items():
            if key == 'razorpay_order_id':
                order_id=val
            if key == 'razorpay_payment_id':
                payment_id=val
            if key == 'razorpay_signature':
                signature=val

        save_trascation = Orders.objects.filter(razor_pay_order_id=order_id).first()
        save_trascation.paymentstatus="PAID"
        save_trascation.razor_pay_payment_id=payment_id
        save_trascation.razor_pay_payment_signature=signature
        save_trascation.save()

        save_Update = OrderUpdate(order_id=order_id,update_desc = "Order placed !")
        save_Update.save()
        # print(f"#######\n paymentID = {payment_id}\n signature={signature}")

        dict = {
            'order_id' : order_id,
            'payment_id' : payment_id
        }
        
        msg_plain = render_to_string('email.txt')
        msg_html = render_to_string("email.html")
        currentuser = request.user.username
        send_mail(
            "Your Ordered has been received",
            msg_plain,
            settings.EMAIL_HOST_USER,
            [currentuser],
            html_message=msg_html
        )

        return render(request,'paymentstatus.html',dict)
    return render(request,'paymentstatus.html')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    currentuser = request.user.username
    name = request.user.first_name+" "+request.user.last_name
    items = Orders.objects.filter(email=currentuser)
    rid = ""
    for i in items:
        # print(i.razor_pay_order_id)
        rid = i.razor_pay_order_id
    
    
    status = OrderUpdate.objects.filter(order_id=rid)
    context = {"items":items,
               "status":status,
               "email":currentuser,
               "name" : name
               }
    
    
    return render(request,"profile.html",context)

