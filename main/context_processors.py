from main.models import News


def latest_news(request):
    latest_posts = News.objects.all().order_by('-publish_time')[:5]
    context = {
        'latest_posts':latest_posts,
    }
    return context