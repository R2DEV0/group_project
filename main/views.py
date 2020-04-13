from django.shortcuts import render, HttpResponse, redirect
from random import randint
import time
from time import localtime, strftime

def index(request):
    print(request.session)
    if 'gold' not in request.session:
        request.session['gold'] = 0
    if 'activity_log' not in request.session:
        request.session['activity_log']=[]
    print(request.session['gold'])
    print(request.session['activity_log'])
    
    context={
        "gold":request.session['gold'],
        "activity_log":request.session['activity_log']
    }
    
    return render(request,"index.html", context)

def process_money(request):
    
    loc=request.POST["location"]
    # print(loc)
    
    locations = {
        'farm':randint(10,20),
        'cave':randint(5,10),
        'house':randint(2,5),
        'casino':randint(-50,50)
    }
    context={
        'gain':f"Earned a whopping {locations[loc]} golds from the {loc}! - {strftime('%H:%M %p %Y-%m-%d', localtime())}",
        'loss':f"You entered a casino and lost! {locations[loc]} from the {loc} ...Ouch, you suck. - {strftime('%H:%M %p %Y-%m-%d', localtime())}",
        # The real friends were the debts we gained along the way-Josh
        'even':f"Whew, you left the casino and didn't lose anything. Not bad for a day at the casino!  - {strftime('%H:%M %p %Y-%m-%d', localtime())}"
    }
    
    if locations[loc]>0:
        request.session['activity_log'].append(context['gain'])
    elif locations[loc]<0:
        request.session['activity_log'].append(context['loss'])
    else:
        request.session['activity_log'].append(context['even'])
    request.session['gold'] += locations[loc]
    print(request.session['activity_log'])
    return redirect("/")
    
def reset(request):
    request.session.flush()
    return redirect('/')