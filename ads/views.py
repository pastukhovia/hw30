import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, CreateView, ListView
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from categories.models import Category
from hw28.settings import TOTAL_ON_PAGE
from users.models import User
from .models import Ad
from .permissions import IsOwner, IsAdminOrModerator
from .serializers import AdRetrieveSerializer, AdUpdateSerializer, AdDestroySerializer


class AdListView(ListView):
    model = Ad
    queryset = Ad.objects.order_by('-price')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        cat = request.GET.get('cat', None)
        if cat:
            self.queryset = self.queryset.filter(category=cat)

        text = request.GET.get('text', None)
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get('location', None)
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get('price_from', None)
        price_to = request.GET.get('price_to', None)
        if price_from and price_to:
            price_q = Q(price__gte=price_from) & Q(price__lte=price_to)
            self.queryset = self.queryset.filter(price_q)

        paginator = Paginator(self.queryset, TOTAL_ON_PAGE)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        items = [{
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author.id,
            "price": ad.price
        }
            for ad in page_obj
        ]

        response = {
            'total': paginator.count,
            'num_pages': paginator.num_pages,
            'items': items
        }

        return JsonResponse(response, safe=False)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdRetrieveSerializer
    permission_classes = [IsAuthenticated, ]


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'author', 'price', 'desc', 'category', 'is_published']

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)

        ad = Ad.objects.create(
            name=json_data['name'],
            author=User.objects.get(pk=json_data['author']),
            price=json_data['price'],
            desc=json_data['desc'],
            category=Category.objects.get(pk=json_data['category']),
            is_published=json_data['is_published']
        )

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author.id,
            "price": ad.price,
            "desc": ad.desc,
            "category_id": ad.category.id,
            'is_published': ad.is_published
        })


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrModerator | IsOwner, ]


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ['name', 'image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author.id,
            'author': self.object.name,
            'price': self.object.price,
            'desc': self.object.desc,
            'is_published': self.object.is_published,
            'category_id': self.object.category.id,
            'image': self.object.image.name
        })


class AdDestroyView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDestroySerializer
    permission_classes = [IsAuthenticated, IsAdminOrModerator | IsOwner, ]
