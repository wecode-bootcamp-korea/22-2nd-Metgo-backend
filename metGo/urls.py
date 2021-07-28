from django.urls    import path, include

from services.views import ServicesView, CategoryView

urlpatterns = [
    path('', CategoryView.as_view()),
    path('<int:category_id>', ServicesView.as_view()),
    path('services', include('services.urls')),
    path('users', include('users.urls')),
    path('masters', include('masters.urls')),
    path('reviews', include('reviews.urls'))
]
