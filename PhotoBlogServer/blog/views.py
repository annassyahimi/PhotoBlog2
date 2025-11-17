import os
import torch
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib.auth.models import User

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import CreateAPIView, ListAPIView

from .models import Post
from .forms import PostForm
from .serializers import PostSerializers


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

YOLO_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'yolov5'))
YOLO_WEIGHTS = os.path.join(YOLO_DIR, 'yolov5s.pt')

model = torch.hub.load(
    YOLO_DIR,
    'custom',
    path=YOLO_WEIGHTS,
    source='local'
)

class blogImage(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers


class UploadView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # debug logs
        print("DEBUG request.data:", request.data)
        print("DEBUG request.FILES:", request.FILES)
        print("Serializer errors:", serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PhotoListView(ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializers


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@csrf_exempt
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            author_id = request.POST.get("author")
            try:
                post.author = User.objects.get(id=author_id)
            except User.DoesNotExist:
                return render(request, "blog/post_edit.html", {
                    "form": form,
                    "error": "User not found.",
                })

            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.author = request.user
            updated_post.published_date = timezone.now()
            updated_post.save()
            return redirect('post_detail', pk=updated_post.pk)

    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})


def js_test(request):
    return render(request, 'blog/js_test.html', {})


def upload(request):
    if request.method == 'POST':
        img = request.FILES['image']

        # Save temporarily before feeding YOLO
        temp_path = default_storage.save('temp.jpg', img)

        # Run YOLO
        results = model(temp_path)
        labels = results.pandas().xyxy[0]['name'].tolist()

        # Save as Post
        Post.objects.create(
            title=labels[0] if labels else "Unknown",
            text=", ".join(labels),
            image=img,
        )

        return redirect('post_list')

    return render(request, 'blog/post_edit.html')
