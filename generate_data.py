import random
from datetime import timedelta
from django.contrib.auth.models import User
from twitt_app.models import Post, Comment, Like
from faker import Faker

fake = Faker('en_US')
fake.unique.clear()

users = []
for i in range(60):
    while True:
        try:
            username = fake.unique.user_name()
            if not User.objects.filter(username=username).exists():
                new_user = User.objects.create_user(
                    username=username,
                    password='password'
                )
                users.append(new_user)
                break
        except Exception as e:
            print(f"خطا در ایجاد کاربر: {e}")

if len(users) < 50:
    raise Exception("تعداد کاربران ایجاد شده کمتر از 50 است!")

posts = []
for i in range(10):
    new_post = Post.objects.create(
        author=random.choice(users),
        text=fake.text(max_nb_chars=100),
        created_at=fake.date_this_year(before_today=True),
    )
    posts.append(new_post)

for post in posts:
    num_likes = random.randint(50, len(users))
    likers = random.sample(users, num_likes)
    for liker in likers:
        Like.objects.create(
            post=post,
            author=liker,
            created_at=fake.date_this_year(before_today=False),
        )

    num_comments = random.randint(25, len(users))
    commenters = random.sample(users, num_comments)
    for commenter in commenters:
        random_days = random.randint(1, 5)  # کامنت‌ها حداکثر 5 روز بعد از پست ایجاد شوند
        end_date = post.created_at + timedelta(days=random_days)

        Comment.objects.create(
            post=post,
            author=commenter,
            text=fake.text(),
            created_at=fake.date_time_between(start_date=post.created_at, end_date=end_date)
        )

print("داده‌های نمونه با موفقیت ایجاد شدند!")