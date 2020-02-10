
from rest_framework import serializers
from blog.models import Post


class BlogPostSerializer(serializers.ModelSerializer):

    # username = serializers.SerializerMethodField('get_username_from_author')
    # image 	 = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'overview', 'thumbnail', 'timestamp']


"""
	def get_username_from_author(self, blog_post):
		username = blog_post.author.username
		return username

	def validate_image_url(self, blog_post):
		image = blog_post.image
		new_url = image.url
		if "?" in new_url:
			new_url = image.url[:image.url.rfind("?")]
		return new_url
"""
