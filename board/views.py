from django.shortcuts import render, get_object_or_404, redirect
# Query Set은 모델의 디폴트 매니저를 통해 실행된다
from .models import Document
# Create your views here.


# query set 설정
# 1. 객체 선택
# 2. 객체 생성
# 3. 객체 필터링
# 4. 객체 삭제
def document_list(request):
    # 모델의 디폴트 매니저(오브젝트와 혼동 주의!!)
    # 1. 모델의 전체 데이터 불러오기

    # 복수 객체 던지고 -> 컨텍스트 밸류로 받음
    documents = Document.objects.all()
    return render(request, 'board/document_list.html', {'object_list':documents})

from .forms import DocumentForm
#로그인을 한사람만 접근
from django.contrib.auth.decorators import login_required
from django.urls import reverse
@login_required()
def document_create(request):
    #Document.objects.create() - 실행과 동시에 DB에 삽입(올바른 데이터가 있어야 함)
    # 분기 필요!! - post, get
    if request.method == "POST":
        # 처리
        # request.POST : 폼에서 입력한 텍스트 데이터
        # request.Files : 파일
        form = DocumentForm(request.POST, request.FILES)
        form.instance.author_id = request.user.id
        if form.is_valid():
            document = form.save()
            return redirect(document)
            #return redirect(reverse('board:detail', args=[document.id]))
    else:
        # 입력창
        # Form 사용
        form = DocumentForm()

    return render(request, 'board/document_create.html', {'form':form})

def document_update(request):
    # 객체 불러와서, 데이터 수정
    if request.method == "POST":
        '''
        id가 없으면 새로 저장 됨
        document = Document.objects.get(pk=1)
        document.id = None
        document.save()
        '''
        document = Document.objects.get(pk=document_id)
        # 모델 폼을 사용 할 때는 instance를 넘겨주면, 해당 인스턴스값으로 초기화 되고
        # 만약 pk가 있는 instance라면 update를 수행한다
        # request.POST와 instance가 같이 전달되면, POST 데이터가 우선순위가 높다
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            document = form.save()
            return redirect(document)
    else:
        document = Document.objects.get(pk=document_id)
        # 검색할 때 modelform init with instance(model object)
        form = DocumentForm(instance=document)
    return render(request, 'board/document_update.html', {'form':form})

def document_detail(request, document_id):
    #단일 객체 던지고 -> 컨텍스트 밸류로 받음
    document = Document.objects.get(pk=document_id)
    return render(request, 'board/document_detail.html', {'object':document})

def document_delete(request):
    # 객체 불러와서, delete만 호출
    return render(request, 'board/document_delete.html')

# 20190513
# 과제1 delete view 구현하기
# - get object or 404, get list or 404, paging
# 과제2 bootstrap 디자인, 템플릿, 확장