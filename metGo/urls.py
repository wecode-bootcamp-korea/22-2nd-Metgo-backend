from django.urls    import path, include

from services.views import ServicesView, CategoryView

urlpatterns = [
    path('/categories', CategoryView.as_view()),
    path('/catergories/<int:category_id>', ServicesView.as_view()),
    path('services', include('services.urls')),
    path('users', include('users.urls')),
    path('masters', include('masters.urls')),
    path('reviews', include('reviews.urls')),
    path('quotations', include('quotations.urls')),
    path('applications', include('applications.urls'))
]
