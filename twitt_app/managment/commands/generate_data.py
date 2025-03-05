import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from twitt_app.models import Post, Comment, Like
from faker import Faker

class Command(BaseCommand):
    help = "Generate sample data for the project"

    def handle(self, *args, **kwargs):
        fake = Faker('en_US')
        fake.unique.clear()

        # ایجاد 60 کاربر نمونه
        users = []
        for i in range(60):
            try:
                new_user = User.objects.create_user(
                    username=fake.unique.user_name(),
                    password='password'
                )
                users.append(new_user)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating user: {e}"))

        if len(users) < 50:
            self.stdout.write(self.style.ERROR("Not enough users created!"))
            return

        # ایجاد 10 پست نمونه با تاریخ‌های گذشته
        posts = []
        for i in range(10):
            new_post = Post.objects.create(
                author=random.choice(users),
                text=fake.text(max_nb_chars=100),
                created_at=fake.date_time_between(start_date="-1y", end_date="now")
            )
            posts.append(new_post)

        # ایجاد لایک‌ها و کامنت‌ها برای هر پست
        for post in posts:
            # ایجاد لایک‌ها
            num_likes = random.randint(50, len(users))
            likers = random.sample(users, num_likes)
            for liker in likers:
                Like.objects.create(
                    post=post,
                    author=liker,  # فرض می‌کنیم در مدل Like فیلد مربوط به کاربر 'author' است.
                    created_at=fake.date_time_between(start_date=post.created_at, end_date="now")
                )

            # ایجاد کامنت‌ها
            num_comments = random.randint(25, len(users))
            commenters = random.sample(users, num_comments)
            for commenter in commenters:
                # پاکسازی کاراکترهای مشکل‌دار
                safe_text = fake.text(max_nb_chars=70).encode('utf-8', 'replace').decode('utf-8')
                Comment.objects.create(
                    post=post,
                    author=commenter,
                    text=safe_text,
                    created_at=fake.date_time_between(start_date=post.created_at, end_date="now")
                )

        self.stdout.write(self.style.SUCCESS("Sample data generated successfully!"))
