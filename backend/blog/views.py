from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from .models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer

class ArticleListCreateView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        queryset = Article.objects.all().order_by('-created_at')
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset
    
class ArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer