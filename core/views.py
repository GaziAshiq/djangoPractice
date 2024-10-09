from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q, F, Value, Func, Count, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from store.models import Product, OrderItem, Customer


def index(request):
    context = {
        "title": "Django example",
        "name": "Ashiq"
    }
    return render(request, "index.html", context)


def say_hello(request):
    query_set = Product.objects.filter(inventory=F('collection__id'))
    return render(request, 'index.html', {"name": query_set.count(), 'products': list(query_set)})


def about(request):
    return HttpResponse("About Django")


# in this function, I will try all the query set
def objects__retrieve_filter(request):
    # region Get all products...
    products = Product.objects.all()
    # endregion it will evaluate when we use it

    # region retrieve single product...
    product = Product.objects.filter(id=0).first()  # it will return None if not found
    product = Product.objects.get(id=1)  # we can also use pk=1. return error if not found
    # pk benefit is, if we change the primary key name, it will still work.
    # endregion it's return single object, not a queryset

    # region Filter products...
    products = Product.objects.filter(price__gt=20)  # price greater than 20
    products = Product.objects.filter(price__lt=20)  # price less than 20
    products = Product.objects.filter(price__gte=20)  # price greater than or equal to 20
    products = Product.objects.filter(price__lte=20)  # price less than or equal to 20
    products = Product.objects.filter(price__range=(10, 20))  # price between 10 and 20
    products = Product.objects.filter(price__isnull=True)  # price is null
    products = Product.objects.filter(title__icontains='noodles')  # title contains coffee
    # endregion products = Product.objects.filter(updated_at__year=2021) # title contains coffee

    # region complex lookups using Q objects...
    # inventory < 10 AND price < 20
    queryset = Product.objects.filter(inventory__lt=10, price__lt=20)  # using multiple kwargs
    queryset = Product.objects.filter(inventory__lt=10).filter(
        price__lt=20)  # using multiple filter, it will use AND condition
    # if we want to use or condition, we can use Q objects
    # inventory < 10 OR price < 20
    queryset = Product.objects.filter(Q(inventory__lt=10) | Q(price__lt=20))
    # can also use AND here, but best practice is to use multiple kwargs in filter
    queryset = Product.objects.filter(Q(inventory__lt=10) | ~Q(price__lt=200))  # ~ is for not
    # endregion

    # region Referencing fields using F objects...
    # inventory is equal to collection id
    refer_query = Product.objects.filter(inventory=F('collection__id'))  # it will compare inventory with collection id
    # endregion

    # region Order by...
    order_by = Product.objects.order_by('price')  # ascending order
    order_by = Product.objects.order_by('-price')  # descending order
    order_by = Product.objects.order_by('price', '-title')  # price ascending, title descending
    order_by = Product.objects.order_by('price', '-title').reverse()  # Reverse the order
    order_by = Product.objects.filter(price__gt=95).order_by('price')  # filter and order by
    # order_by = Product.objects.earliest('price')  # earliest
    # order_by = Product.objects.latest('price')  # latest
    # endregion

    # region limiting query set
    limit_query = Product.objects.all()[:10]  # first 10
    limit_query = Product.objects.values('title', 'id')  # selecting fields only
    limit_query = Product.objects.values('title', 'id', 'collection__title')[1]  # now it'll use inner join
    # note: if we use values, it'll return dictionary, not object

    limit_query = Product.objects.values_list('title', 'id')[1]  # This return tuple instead of dictionary

    # select products that have been ordered
    limit_query = OrderItem.objects.values('product_id').distinct()  # distinct is used to remove duplicate
    # sort the list by id
    limit_query = Product.objects.filter(id__in=limit_query).order_by('id')

    # only versus values: only is used to select fields, values is used to select fields and return dictionary
    limit_query = Product.objects.only('title', 'price')  # only select title and price
    # be careful, if we use only, it won't return id, so we can't use it in filter, end up with many queries

    limit_query = Product.objects.defer('title', 'price')  # defer is the opposite of only
    # defer is used to exclude fields, so it'll return id, but not title and price
    # endregion

    # region select_related and prefetch_related...
    # when we use product.objects.all(), it only load product table, not related table (like - collection)
    # so, when we use product.collection.title, it will make another query to get collection title. so, it will make n+1 queries
    # to avoid this, we can use select_related. it will join the tables and return collection title
    limit_query = Product.objects.select_related('collection')  # it will return collection object, not collection id.
    # it preloads the related table, so it will not make another query to get collection title
    limit_query = Product.objects.select_related(
        'collection__featured_product')  # we can also use nested select_related

    # select_related is used for many-to-one relationship
    # prefetch_related is used for many-to-many relationship
    limit_query = Product.objects.prefetch_related(
        'promotions').all()  # it will return all promotions related to product
    # here, it will make 2 queries, one for product and one for promotions (n+1 queries)

    limit_query = Product.objects.prefetch_related('promotions').select_related(
        'collection')  # if we use both, it will reduce multiple queries
    # endregion

    # region Annotating objects
    # annotate is used to add extra fields to the queryset
    # lets add is_new field to the queryset
    limit_query = Product.objects.annotate(is_new=Value(True))  # django will add is_new field to the queryset
    # let's add new_id +1 with id field reference
    limit_query = Product.objects.annotate(new_id=F('id') + 1)  # it'll add new_id field to the queryset

    # calling database function using annotate and Func
    limit_query = Customer.objects.annotate(
        # Concatenate first_name and last_name with space in between
        full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT'))
    # this doesn't work in sqlite, but work in postgresql

    # alternatively, we can use Concat function
    limit_query = Customer.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name'))  # this will work in sqlite

    # lest find the total number of orders for each customer
    limit_query = Customer.objects.annotate(total_orders=Count('order'))  # it'll add total_orders field to the queryset

    # expression wrapper is used to perform arithmetic operations
    limit_query = Product.objects.annotate(
        discounted_price=ExpressionWrapper(F('price') * 0.9, output_field=DecimalField()))

    # endregion

    context = {
        'single_product': product,
        'products': products,
        'queryset': queryset,
        'refer_queryset': refer_query,
        'order_by': order_by,
        'limit_query': list(limit_query)
    }
    return render(request, 'objects.html', context)
