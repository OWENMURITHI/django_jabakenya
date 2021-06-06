import operator
import random
from functools import reduce
from django.contrib import messages
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..models import Product, Chat
from ..decorators import seller_required



@method_decorator([login_required, seller_required], name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    fields = ('title', 'description', 'price', 'image', 'locations')
    template_name = "jaba/add_product.html"

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        messages.success(self.request, 'The product is now under REVIEW!!!')
        return redirect('home')


class ProductView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = "jaba/home.html"
    paginate_by = 20

    def get_queryset(self):
        queryset = Product.objects.filter(is_approved=True).order_by(
            '-created')  # Order by the last to be created
        return queryset


# Takes care of the search functionality
def search(request):
    if request.method == 'GET':
        queries = request.GET.get('q').split()
        submitbutton = request.GET.get('submit')

        if queries is not None:
            # Look for the query in the following fields
            initial = Product.objects.all()
            lookups = reduce(operator.or_, [Q(title__icontains=query) | Q(
                description__icontains=query) | Q(owner__username__icontains=query) | Q(owner__first_name__icontains=query) | Q(owner__last_name__icontains=query) for query in queries])

            results = Product.objects.filter(lookups).distinct()

            context = {'results': results,
                       'submitbutton': submitbutton}

            return render(request, 'jaba/search.html', context)

        else:
            products = Product.objects.all()
            return render(request, 'jaba/search.html', products)

    else:
        return render(request, 'jaba/search.html')


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'products'
    template_name = "jaba/product_page.html"

    def products(request):

       
        context = {
            'items': Product.objects.all()
        }

        return render(request, 'jaba/product_page.html', context)

    def get_context_data(self, *args, **kwargs):
        # Get the existing context dictionary, then add
        # your custom object to it before returning it
        ctx = super(ProductDetail, self).get_context_data(*args, **kwargs)
        ctx['related_products'] = random.sample(list(Product.objects.all()), 6)

        return ctx

    def get_queryset(self):
        query = Product.objects.all()
        return query
