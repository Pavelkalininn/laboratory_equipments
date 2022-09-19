from django.core.paginator import Paginator

COUNT_OF_EQUIPMENT = 100


def pagination(posts, request):
    paginator = Paginator(posts, COUNT_OF_EQUIPMENT)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
