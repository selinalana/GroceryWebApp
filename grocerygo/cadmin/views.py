from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import IntegrityError

def home(request):
    return render(request, 'home.html')

def navigation(request):
    return render(request, 'navigation.html')

def about(request):
    return render(request, 'about.html')

def index(request):
    if request.user.is_staff:
        return redirect('admindashboard')
    data = Carousel.objects.all()
    dict = {'data' :data}
    return render(request, 'index.html',dict)

def contact(request):
    if request.method == 'POST':
        # Get the form data from the POST request
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        contact_number = request.POST['contact_number']
        message = request.POST['message']

        # Create a new Contact object and save it to the database
        contact = Contact(
            first_name=first_name,
            last_name=last_name,
            email=email,
            contact_number=contact_number,
            message=message
        )
        contact.save()  # Save the contact form data to the database
        return redirect(index)
    return render(request, 'contact.html')

def adminLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('admindashboard')
            else:
                messages.success(request, "Invalid Credentials!")
        except:
            messages.success(request, "Invalid Credentials!")
    return render(request, 'admin_login.html')

def adminHome(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    return render(request, 'admin_base.html')

def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    user = UserProfile.objects.filter()
    category = Category.objects.filter()
    product = Product.objects.filter()
    new_order = Booking.objects.filter(status=1)
    dispatch_order = Booking.objects.filter(status=2)
    way_order = Booking.objects.filter(status=3)
    deliver_order = Booking.objects.filter(status=4)
    cancel_order = Booking.objects.filter(status=5)
    return_order = Booking.objects.filter(status=6)
    order = Booking.objects.filter()
    read_feedback = Feedback.objects.filter(status=1)
    unread_feedback = Feedback.objects.filter(status=2)
    read_messages = Contact.objects.filter(status=1)
    unread_messages = Contact.objects.filter(status=2)
    return render(request, 'admin_dashboard.html', locals())

def add_category(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    if request.method == "POST":
        name = request.POST['name']
        Category.objects.create(name=name)
        messages.success(request, "Category added")
        return redirect('view_category')
    return render(request, 'add_category.html', locals())

def view_category(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    category = Category.objects.all()
    return render(request, 'view_category.html', locals())

def edit_category(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    category = Category.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        messages.success(request, "Category updated")
        return redirect('view_category')
    return render(request, 'edit_category.html', locals())

def delete_category(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    category = Category.objects.get(id=pid)
    category.delete()
    messages.success(request, "Category deleted")
    return redirect('view_category')

def add_product(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        image = request.FILES['image']
        catobj = Category.objects.get(id=cat)
        Product.objects.create(name=name, price=price, discount=discount, category=catobj, description=desc, image=image)
        messages.success(request, "Product added")
    return render(request, 'add_product.html', locals())

def view_product(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    product = Product.objects.all()
    return render(request, 'view_product.html', locals())

def edit_product(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    product = Product.objects.get(id=pid)
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        try:
            image = request.FILES['image']
            product.image = image
            product.save()
        except:
            pass
        catobj = Category.objects.get(id=cat)
        Product.objects.filter(id=pid).update(name=name, price=price, discount=discount, category=catobj, description=desc)
        messages.success(request, "Product Updated")
        return redirect('view_product')
    return render(request, 'edit_product.html', locals())

def delete_product(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect('view_product')

# def registration(request):
#     if request.method == "POST":
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         password = request.POST['password']
#         address = request.POST['address']
#         mobile = request.POST['mobile']
#         image = request.FILES['image']
#         user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password)
#         UserProfile.objects.create(user=user, mobile=mobile, address=address, image=image)
#         messages.success(request, "Registration Successful")
#     return render(request, 'registration.html', locals())


def registration(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        mobile = request.POST['mobile']
        image = request.FILES['image']
        
        try:
            # Attempt to create the user
            user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password)
            UserProfile.objects.create(user=user, mobile=mobile, address=address, image=image)
            messages.success(request, "Registration Successful!")
            return redirect('userlogin')  # Redirect to login page after success
        except IntegrityError:
            # If the email is already used
            messages.error(request, "This email is already registered. Please use a different one.")
    
    return render(request, 'registration.html', locals())

def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "User login successfully")
            return redirect('index')
        else:
            messages.success(request,"Invalid Credentials")
    return render(request, 'login.html', locals())

def profile(request):
    if not request.user.is_authenticated:
        return redirect ('userlogin')
    user = User.objects.get(id=request.user.id)
    data = UserProfile.objects.filter(user=user)
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email'] 
        address = request.POST['address']
        mobile = request.POST['mobile']
        try:
            image = request.FILES['image']
            data.image = image
            data.save()
        except:
            pass
        user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname)
        UserProfile.objects.filter(id=data.id).update(mobile=mobile, address=address)
        messages.success(request, "Profile updated")
        return redirect('profile')
    return render(request, 'profile.html', locals())

def logoutuser(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('index')

def change_password(request):
    if not request.user.is_authenticated:
        return redirect ('userlogin')
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('index')
            else:
                messages.success(request, "Password not matching")
                return redirect('change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('change_password')
    return render(request, 'change_password.html')

def user_product(request,pid):
    if pid == 0:
        product = Product.objects.all()
    else:
        category = Category.objects.get(id=pid)
        product = Product.objects.filter(category=category)
    allcategory = Category.objects.all()
    return render(request, "user-product.html", locals())

def product_detail(request, pid):
    product = Product.objects.get(id=pid)
    latest_product = Product.objects.filter().exclude(id=pid).order_by('-id')[:10]
    return render(request, "product_detail.html", locals())

def addToCart(request, pid):
    if not request.user.is_authenticated:
        return redirect ('userlogin')
    myli = {"objects":[]}
    try:
        cart = Cart.objects.get(user=request.user)
        myli = json.loads((str(cart.product)).replace("'", '"'))
        try:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
        except:
            myli['objects'].append({str(pid):1})
        cart.product = myli
        cart.save()
    except:
        myli['objects'].append({str(pid): 1})
        cart = Cart.objects.create(user=request.user, product=myli)
    return redirect('cart')

def incredecre(request, pid):
    if not request.user.is_authenticated:
        return redirect ('userlogin')
    cart = Cart.objects.get(user=request.user)
    if request.GET.get('action') == "incre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
    if request.GET.get('action') == "decre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        if myli['objects'][0][str(pid)] == 1:
            del myli['objects'][0][str(pid)]
        else:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) - 1
    cart.product = myli
    cart.save()
    return redirect('cart')

def cart(request):
    if not request.user.is_authenticated:
        return redirect ('userlogin')
    try:
        cart = Cart.objects.get(user=request.user)
        product = (cart.product).replace("'", '"')
        myli = json.loads(str(product))
        product = myli['objects'][0]
    except:
        product = []
    lengthpro = len(product)
    return render(request, 'cart.html', locals())

def deletecart(request, pid):
    if not request.user.is_authenticated:
        return redirect ('userlogin')
    cart = Cart.objects.get(user=request.user)
    product = (cart.product).replace("'", '"')
    myli = json.loads(str(product))
    del myli['objects'][0][str(pid)]
    cart.product = myli
    cart.save()
    messages.success(request, "Delete Successfully")
    return redirect('cart')

# def booking(request):
#     if not request.user.is_authenticated:
#         return redirect ('userlogin')
#     user = UserProfile.objects.get(user=request.user)
#     cart = Cart.objects.get(user=request.user)
#     total = 0
#     discounted =0
#     deduction = 0
#     productid = (cart.product).replace("'", '"')
#     productid = json.loads(str(productid))
#     try:
#         productid = productid['objects'][0]
#     except:
#         messages.success(request, "Cart is empty, Please add product in cart.")
#         return redirect('cart')
#     for i,j in productid.items():
#         product = Product.objects.get(id=i)
#         total += int(j) * float(product.price)
#         price = float(product.price) * (100 - float(product.discount)) / 100
#         discounted += int(j) * price
#     deduction = total - discounted
#     if request.method == "POST":
#         return redirect('/payment/?total='+str(total)+'&discounted='+str(discounted)+'&deduction='+str(deduction))
#     return render(request, "booking.html", locals())

def booking(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')

    user = UserProfile.objects.get(user=request.user)
    cart = Cart.objects.get(user=request.user)

    total = 0
    discounted = 0
    deduction = 0

    # Load cart product data
    productid = (cart.product).replace("'", '"')
    productid = json.loads(str(productid))

    try:
        productid = productid['objects'][0]  # Access first product
    except:
        messages.success(request, "Cart is empty, Please add product in cart.")
        return redirect('cart')

    # Loop through cart items and calculate total and discounted price
    for i, j in productid.items():
        product = Product.objects.get(id=i)

        # Validate product price and discount
        try:
            product_price = float(product.price) if product.price else 0.0
            product_discount = float(product.discount) if product.discount else 0.0

            # Calculate total price and discounted price
            total += int(j) * product_price
            price_after_discount = product_price * (100 - product_discount) / 100
            discounted += int(j) * price_after_discount

        except ValueError as e:
            # Handle case where conversion fails
            messages.error(request, f"Invalid price or discount for product {product.name}.")
            return redirect('cart')

    # Calculate deduction
    deduction = total - discounted

    # Handle POST request for payment
    if request.method == "POST":
        return redirect(f'/payment/?total={total}&discounted={discounted}&deduction={deduction}')

    return render(request, "booking.html", locals())

def myOrder(request):
    if not request.user.is_authenticated:
        return redirect ('userlogin')
    order = Booking.objects.filter(user=request.user)
    return render(request, "my-order.html", locals())

def user_order_track(request, pid):
    if not request.user.is_authenticated:
        return redirect ('userlogin')
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    return render(request, "user-order-track.html", locals())

def change_order_status(request, pid):
    if not request.user.is_authenticated:
        return redirect ('userlogin')
    order = Booking.objects.get(id=pid)
    status = request.GET.get('status')
    if status:
        order.status = status
        order.save()
        messages.success(request, "Order status changed.")
    return redirect('myorder')

def user_feedback(request):
    if not request.user.is_authenticated:
        return redirect ('userlogin')
    user = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        Feedback.objects.create(user=request.user, message=request.POST['feedback'])
        messages.success(request, "Feedback sent successfully")
    return render(request, "feedback-form.html", locals())

def manage_feedback(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    action = request.GET.get('action', 0)
    feedback = Feedback.objects.filter(status=int(action))
    return render(request, 'manage_feedback.html', locals())

def delete_feedback(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    feedback = Feedback.objects.get(id=pid)
    feedback.delete()
    messages.success(request, "Deleted successfully")
    return redirect('/manage_feedback/?action=1')

def read_feedback(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    feedback = Feedback.objects.get(id=pid)
    feedback.status = 1
    feedback.save()
    return HttpResponse(json.dumps({'id':1, 'status':'success'}), content_type="application/json")

def payment(request):
    if not request.user.is_authenticated:
        return redirect ('userlogin')
    total = request.GET.get('total')
    discounted = request.GET.get('discounted')
    cart = Cart.objects.get(user=request.user)
    if request.method == "POST":
        book = Booking.objects.create(user=request.user, product=cart.product, total=discounted)
        cart.product = {'objects': []}
        cart.save()
        messages.success(request, "Book Order Successfully")
        return redirect('myorder')
    return render(request, 'payment.html', locals())

def manage_order(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    action = request.GET.get('action', 0)
    order = Booking.objects.filter(status=int(action))
    order_status = ORDERSTATUS[int(action)-1][1]
    if int(action) == 0:
        order = Booking.objects.filter()
        order_status = 'All'
    return render(request, 'manage_order.html', locals()) 

def delete_order(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    order = Booking.objects.get(id=pid)
    order.delete()
    messages.success(request, 'Order Deleted')
    return redirect('/manage-order/?action='+request.GET.get('action'))

def admin_order_track(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    status = int(request.GET.get('status',0))
    if status:
        order.status = status
        order.save()
        return redirect('admin_order_track', pid)
    return render(request, 'admin-order-track.html', locals())

def manage_user(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    userprofile = UserProfile.objects.all()
    return render(request, 'manage_user.html', locals()) 

def delete_user(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    user = User.objects.get(id=pid)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect('manage_user') 

def admin_change_password(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('index')
            else:
                messages.success(request, "Password not matching")
                return redirect('admin_change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('admin_change_password')
    return render(request, 'admin_change_password.html')

def manage_messages(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    action = request.GET.get('action', 0)
    msg = Contact.objects.filter(status=int(action))
    return render(request, 'manage_messages.html', locals())

# def delete_messages(request):
#     if not request.user.is_staff:
#         return redirect('admin_login')
#     msg = Contact.objects.get(id)
#     msg.delete()
#     messages.success(request, "Deleted successfully")
#     return redirect('/manage_messages/?action=1')

# def read_messages(request, pid):
#     if not request.user.is_staff:
#         return redirect('admin_login')
#     msg = Contact.objects.get(id=pid)
#     msg.status = 1
#     msg.save()
#     return HttpResponse(json.dumps({'id':1, 'status':'success'}), content_type="application/json")

def read_messages(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    
    # Get the specific message and mark it as read
    msg = get_object_or_404(Contact, id=pid)
    msg.status = 1  # Mark as read
    msg.save()

    return JsonResponse({'id': pid, 'status': 'success'})

def delete_messages(request, pid):
    if not request.user.is_staff:
        return redirect('admin_login')
    
    # Fetch and delete the message
    msg = get_object_or_404(Contact, id=pid)
    msg.delete()
    
    # Success message for the admin
    messages.success(request, "Message deleted successfully")
    return redirect('/admin_dashboard/')  # Redirect to the admin dashboard
