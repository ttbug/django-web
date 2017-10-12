from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
# from .models import Comment
from .forms import CommentForm

# Create your views here.


def post_comment(request, post_pk):
    # 获取被评论的文章
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        # 用户提交的数据存储在request.POST中,这是一个类字典对象
        form = CommentForm(request.POST)
        print('here')

        # 检查表单数据是否符合格式要求
        if form.is_valid():
            # 检查到数据是合法的，将数据保存到数据库
            # commit=False的作用是利用表单数据生成Comment类的实例,但是还不保存到数据库
            comment = form.save(commit=False)

            # 将评论和文章关联起来
            comment.post = post
            # 最终将实例保存到数据库
            comment.save()
            print('there')
            print(comment.name)
            '''
            重定向到post的详情页，实际上当redirect函数接受一个模型的实例时，他会调用这个模型实例的get_absolute_url，然后重定向到get_absolute_url返回的url
            '''
            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            context = {
                    'post': post,
                    'form': form,
                    'comment_list': comment_list,
            }
            return render(request, 'blog/detail.html', context=context)
    # 如果是非POST请求，说明用户没有提交数据，重定向到文章详情页
    return redirect(post)
