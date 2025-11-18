def cartCount(request):
    if request.user.is_authenticated:
        count=request.user.basket.all().count()
        return {"cartcount":count}
    else:
        return{"cartcount":0}
