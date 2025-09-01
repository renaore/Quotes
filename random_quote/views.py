from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import F
from .models import Quote
from .forms import UserForm
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random


def index(request):
    try:
        total_weight = Quote.objects.aggregate(Sum('weight'))['weight__sum']
        random_point = random.randint(1, total_weight)
        current_sum = 0
        quotes = Quote.objects.order_by('id')
        for quote in quotes:
            current_sum += quote.weight
            if current_sum >= random_point:
                Quote.objects.filter(id=quote.id).update(shows=F('shows') + 1)
                quote.refresh_from_db()
                return render(request, "index.html", {"quote": quote})

    except Exception as e:
        return render(request, "index.html", {"quote": None})

def edit(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            source, text, weight = (userform.cleaned_data[field] for field in ("source", "text", "weight"))
            source = source.strip().capitalize()
            text = text.strip().capitalize()

            exists = Quote.objects.filter(source=source, text=text).update(weight=weight)
            if exists:
                messages.success(request, f'Обновлен вес ({weight}) для цитаты \n «{text}» \
                                \n из источника «{source}».')
                return redirect('edit')

            cnt = Quote.objects.filter(source=source).count()
            if cnt >= 3:
                messages.success(request, f'Из источника «{source}» уже хватает цитат :) \
                                \n Попробуйте ввести другой источник.')
                return redirect('edit')
            quote = Quote()
            quote.source = source
            quote.text = text
            quote.weight = weight
            quote.save()
            messages.success(request, f'Успешно добавлена цитата \n «{text}» \
                            \n из источника «{source}».')
            return redirect('edit')

    userform = UserForm()
    return render(request, "edit.html", {"form": userform})

@csrf_exempt
def vote(request, quote_id):
    if request.method == "POST":
        action = request.POST.get("action")
        quote = get_object_or_404(Quote, id=quote_id)

        if action == "like":
            Quote.objects.filter(id=quote_id).update(likes=F('likes') + 1)
            quote.refresh_from_db()
            return JsonResponse({"status": "success", "likes": quote.likes})
        elif action == "dislike":
            Quote.objects.filter(id=quote_id).update(dislikes=F('dislikes') + 1)
            quote.refresh_from_db()
            return JsonResponse({"status": "success", "dislikes": quote.dislikes})

def top(request):
    quotes = Quote.objects.order_by('-likes')[:10]
    return render(request, "top.html", {"quotes": quotes})
