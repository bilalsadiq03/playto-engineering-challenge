from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return f'Post by {self.author.username} at {self.created_at}'
    
class Comment(models.Model):
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} by {self.author.username}"
    
class Like(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    post = models.ForeignKey(
        Posts, 
        null=True, 
        blank=True,
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    comment = models.ForeignKey(
        Comment, 
        null=True, 
        blank=True,
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_user_post_like"
            ),
            models.UniqueConstraint(
                fields=["user", "comment"],
                name="unique_user_comment_like"
            ),
        ]

    def __str__(self):
        return f'Like by {self.user.username}'
    
class KarmaTransaction(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='karma_transactions'
    )
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.points}"