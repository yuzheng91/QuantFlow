from rest_framework import serializers
from .models import Article
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ArticleSerializer(serializers.ModelSerializer):
    summary = serializers.SerializerMethodField()
    category = CategorySerializer()
    
    class Meta:
        model = Article
        fields = '__all__'

    def get_summary(self, obj):
        return obj.summary()
