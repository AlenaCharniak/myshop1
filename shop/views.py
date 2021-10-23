from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Comment
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    object_list = Product.objects.filter(category=category).filter(available=True).order_by('created')
    paginator = Paginator(object_list, 2)
    page = request.GET.get('page', 1)
    try:
        products = paginator.get_page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop/product/list.html', context={'category': category,
                   'categories': categories,
                   'products': products})



def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    comments = product.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'shop/product/detail.html', context={'product': product,
               'cart_product_form': cart_product_form,
               'comments': comments,
               'comment_form': comment_form})

