from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact, Orders, OrderUpdate
from math import ceil
import json

# Create your views here.
def index(request):
    # product = Product.objects.all()
    # n = len(product)
    # nSlides = n//4 + ceil(n/4 - n//4)
    # # params = {'product':product,'no_of_slides':nSlides,'range_obj':range(1,nSlides) }
    # m_products = [[product, range(nSlides),nSlides],
    #               [product, range(nSlides),nSlides]]
    
    m_products = []
    cat_products = Product.objects.values('category', 'id') #category haru k k hun ta with id, dictionary ma dinxa, id matlab items 4 ota xa vane teslai 1,2,3,4 dine as per the items in database
    cats = {item['category'] for item in cat_products} # {yesle chai tyo mathi aako category lai list,set ma rakxa}
    
    for cat in cats:
        product = Product.objects.filter(category=cat)
        n = len(product)
        nSlides = n//4 + ceil(n/4 - n//4)
        m_products.append([product, range(1, nSlides), nSlides])


    params = {'m_products':m_products}
    return render(request, 'dokan/index.html',params)

def about(request):
    return render(request, 'dokan/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'dokan/contact.html')

def tracker(request):
    if request.method == 'POST':
        orderId = request.POST.get('orderId','')
        email = request.POST.get('email','')

        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []

                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')

        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'dokan/tracker.html')

def prodview(request,pid):
    # product = Product.objects.get(id=pid)#for single object
    product = Product.objects.filter(id=pid)
    # print(product.p_name)
    # context = {'product':product}
    return render(request, 'dokan/prodview.html',{'product':product[0]})

def checkout(request):
    if request.method == 'POST':
        jsonItems = request.POST.get('jsonItems','')
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        address = request.POST.get('address1') + " " + request.POST.get('address2')
        phone = request.POST.get('phone','')
        state = request.POST.get('state','')
        city = request.POST.get('city','')
        zip_code = request.POST.get('zip_code','')
        order = Orders( items_json=jsonItems, name=name, email=email, address=address, phone=phone, state=state, city=city, zip_code=zip_code)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request,'dokan/checkout.html', {'thank':thank, 'id':id})
    return render(request, 'dokan/checkout.html')



# def search(request):
#     return HttpResponse("Hello from dokan ko search")