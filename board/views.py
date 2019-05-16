from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
# Query Set은 모델의 디폴트 매니저를 통해 실행된다
import math
from .models import Document
# Create your views here.


# query set 설정
# 1. 객체 선택
# 2. 객체 생성
# 3. 객체 필터링
# 4. 객체 삭제
from django.db.models import Q
def document_list(request):
    # request.POST.get('')
    # 현재 페이지 번호
    page = int(request.GET.get('page', 1))  # -> get으로 query를 가져올 수 있다.

    paginated_by = 3  # 한 페이지에 띄울 리스트 개수
    # request.METHOD.get -> 아이템 1개
    # request.METHOD.getlist -> 여러개 리스트형태로
    search_type = request.GET.getlist('search_type', None)
    if not search_type:
        # not인 경우 : search_type = None, search_type = []
        search_type = ['title']
        """
        search_type?
        username => Q(author__username__icontains=search_key)
        title => Q(title__icontains=search_key)
        text => Q(text__icontains=search_key)
        search_q = q1 | q2 | q3
        if search_key and search_type:
            documents = get_list_or_404(Documen, title__icontains='11')
            documents = get_list_or_404(Document, search_q)
        """
    print(search_type)
    search_key = request.GET.get('search_key', None)

    # username = Q(author__username__icontains=search_key)
    # title = Q(title__icontains=search_key)
    # print(title)
    # author = Q(author__icontains=search_key)
    # print(author)
    search_q = None
    # F : 컬럼 참조
    # Join
    # select_related -> DB에 부담을 줄 것이냐? 아니면 서버에 부담을 줄 것이냐?
    # prefetch_related
    if search_key:
        if 'title' in search_type:
            temp_q = Q(title__icontains=search_key)
            search_q = search_q | temp_q if search_q else temp_q
        if 'author' in search_type:
            temp_q = Q(author__icontains=search_key)
            search_q = search_q | temp_q if search_q else temp_q
        documents = get_list_or_404(Document, search_q)
    else:
        documents = get_list_or_404(Document)
    # QuerySet 객체를 슬라이싱 할 때 [시작번호:끝번호]
    # 1 - 0 ====== page*paginated_by
    # 2 - paginated_by*(page-1) ==== 6
    # 3 - paginated_by*(page-1) ==== 9

    total_count = len(documents)  # 전체 페이지 수
    total_page = math.ceil(total_count / paginated_by)
    page_range = range(1, total_page + 1)
    # 전체 갯수 -> 전체 페이지 수
    start_index = paginated_by * (page - 1)
    end_index = paginated_by * page

    documents = documents[start_index:end_index]  # slicing을 이용해 객체를 수집
    """
     필드명 = "값" 매칭
     필드명__exact = "값" 매칭
     필드명__iexact = "값" 대소문자 구분없이 매칭

     __startswith, __istartswith 값으로 시작
     __endswith, __iendswith 값으로 끝
     __continas, __icontains 값을 포함하느냐

     ForeignKey 매칭
     필드명__해당모델의필드명 매칭
     필드명__해당모델의필드명__옵션 위와 동일하게 동작

     __gt=값, __gte=값 크다, 크거나 같다. 
     ex) created__gt = 오늘 => 작성일이 오늘보다 크다. 
     __lt=값, __lte=값 작다, 작거나 같다.
     ex) created__lt = 오늘 => 작성일이 오늘보다 이전
     ex) 판매시작일__lte = 오늘 => 판매시작일 설정값이 오늘보다 작거나 같으면 판매 시작

    objects.filter() : filter 메서드에 들어가는 매개변수들은 항상 and 연산을 한다.
    or 연산을 하고 싶어서 Q 객체를 사용한다.
    사용법은 filter에 들어가는 매개변수의 작성법과 똑같다.

    Q() | Q() or
    Q() & Q() and
    ~Q() not
    """

    """
    from django.db.models import F
    Document.objects.fillter(text icontains=title) 
    """
    return render(request, 'board/document_list.html',
                  {'object_list': documents, 'total_page': total_page, 'page_range': page_range})
    # 모델의 디폴트 매니저(오브젝트와 혼동 주의!!)
    # 1. 모델의 전체 데이터 불러오기

    # 복수 객체 던지고 -> 컨텍스트 밸류로 받음
    #documents = Document.objects.all()
    #return render(request, 'board/document_list.html', {'object_list':documents})

from .forms import DocumentForm
#로그인을 한사람만 접근
from django.contrib.auth.decorators import login_required
from django.urls import reverse
@login_required # -> login이 되었을 경우에만 document_create 실행됨
def document_create(request):
    #Document.objects.create() - 실행과 동시에 DB에 삽입(올바른 데이터가 있어야 함)
    # 분기 필요!! - post, get
    if request.method == "POST":
        # 처리
        # request.POST : 폼에서 입력한 텍스트 데이터
        # request.Files : 파일
        form = DocumentForm(request.POST, request.FILES)
        form.instance.author_id = request.user.id # login 되어있다는 가정
        if form.is_valid():
            document = form.save()
            return redirect(document)
            #return redirect(reverse('board:detail', args=[document_id]))
    else:
        # 입력창
        # Form 사용
        form = DocumentForm() # empty page

    return render(request, 'board/document_create.html', {'form':form})

def document_update(request, document_id):
    # 객체 불러와서, 데이터 수정
    if request.method == "POST":
        #document = Document.objects.get(pk=document_id)
        # 모델 폼을 사용 할 때는 instance를 넘겨주면, 해당 인스턴스값으로 초기화 되고
        # 만약 pk가 있는 instance라면 update를 수행한다
        # request.POST와 instance가 같이 전달되면, POST 데이터가 우선순위가 높다
        document = get_object_or_404(Document, pk=document_id)  # -> 페이지를 찾지 못할 경우 404 페이지 출력
        '''
        id가 없으면 새로 저장 됨
        document = Document.objects.get(pk=1)
        document.id = None
        document.save()
        '''
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            document = form.save() # 저장된 이후 Document 객체(instance) 생성하여 documet변수에 할당
            return redirect(document)
    else:
        #document = Document.objects.get(pk=document_id)
        document = get_object_or_404(Document, pk=document_id)
        # 검색할 때 modelform init with instance(model object)
        form = DocumentForm(instance=document) # 위 과정을 거치면 instance.title, instance.text.... 등으로 채워진다
    return render(request, 'board/document_update.html', {'form':form})

# def document_update(request, document_id):
#     # 객체 불러와서, 데이터를 수정
#     if request.method == "POST":
#         # 처리
#         # request.POST : 폼에서 입력한 텍스트 데이터
#         # request.FILES : 파일
#         document = Document.objects.get(pk=document_id)
#         form = DocumentForm(request.POST, request.FILES or None, instance=document)
#         if form.is_valid():
#             document = form.save()
#             return redirect(document)
#     else:
#         # 입력 창
#         document = Document.objects.get(pk=document_id)
#         form = DocumentForm(instance=document)
#     return render(request, 'board/document_update.html',{'form':form})

def document_detail(request, document_id):
    #단일 객체 던지고 -> 컨텍스트 밸류로 받음
    #document = Document.objects.get(pk=document_id)
    document = get_object_or_404(Document, pk=document_id)
    # 만약 post일 때만 댓글 입력에 관한 처리를 한다

    # if request.method == "POST":
    #     comment_form = CommentForm(request.POST)
    #     comment_form.instance.author_id = request.user.id
    #     comment_form.instance.document_id = document_id
    #     if comment_form.is_valid():
    #         comment = comment_form.save()
    comment_form = CommentForm()
    comments = document.comments.all()
    return render(request, 'board/document_detail.html', {'object':document, 'comments':comments, 'comment_form':comment_form})

'''
form = CommentForm()
self.instance = Comment()
self.instance.text = 
'''
from .forms import CommentForm
# ajax사용해서 댓글 달기
def comment_create(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    comment_form = CommentForm(request.POST)
    comment_form.instance.author_id = request.user.id
    comment_form.instance.document_id = document_id
    if comment_form.is_valid():
        comment = comment_form.save()
    # redirect(reverse('board:detail', args=[document_id]))
    # reverse -> url pattern을 가지고 주소를 만들어 주는 함수
    # reverse_lazy -> url pattern을 가지고 주소를 만들어주지만 평가가 나중에 일어남
    # 실제 호출 될 때 평가한다
    # redirect는 HTTPResposeRedirect를 포함한다
    return redirect(document)

"""
페이지에 접근했을 때 구동되는 로직들
함수형 뷰
1) 해당 객체가 있는지 확인 - get_object_or_404, objects.get, objects.filter.exists
2) 객체에 대한 권한 체크 - 작성자, 관리자
3-1) get -> 해당 페이지에 필요한 값 입력받기
3-2) post -> 입력받는 값에 대한 처리 -> 삭제, 업데이트
4) 처리 후 페이지 이동

클래스형 뷰
def dispatch(self, request, *args, **kwargs):
    object = self.get_object()
    #권한체크
    # supper().dispath(request, *args, **kwargs)
    # 만약 분기한다면 아래코드로!
    if request.method == "POST":
        # supper().post(request, *args, **kwargs)
    else:
        # supper().get(request, *args, **kwargs)
1) 해당 객체가 있는지 확인 - dispatch
2) 해당 객체가 있는지 확인 - get_object, get_queryset
2) 객체에 대한 권한 체크 - 작성자, 관리자
3-1) get -> 해당 페이지에 필요한 값 입력받기 - def get
3-2) post -> 입력받는 값에 대한 처리 -> 삭제, 업데이트 - def post
4) 처리 후 페이지 이동
"""
from django.contrib import messages
from .models import Comment
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    document = get_object_or_404(Document, pk=comment.document.id)
    # user.is_staff
    # user.is_superuser
    if request.user != comment.author:
        messages.warning(request, "권한없음")
        return redirect(document)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(document)
    else:
        form = CommentForm(instance=comment)
        return render(request, 'board/comment/comment_update.html', {'form':form})

def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    document = get_object_or_404(Document, pk=comment.document.id)

    if request.user != comment.author and not request.user.is_staff and request.user != document.author:
        message.warning(request, "권한 없음")
        return redirect(document)

    if request.method == "POST":
        comment.delete()
        return redirect(document)
    else:
        return render(request, 'board/comment/comment_delete.html', {'object':comment})


def document_delete(request, document_id):
    # 객체 불러와서, delete만 호출
    return render(request, 'board/document_delete.html')

# 20190513
# 과제1 delete view 구현하기
# - get object or 404, get list or 404, paging
# 과제2 bootstrap 디자인, 템플릿, 확장

# 20190514
# 과제1: Document, Category, Board 모델까지 확장
# Category - board = models.ForeignKey(Board)
# 게시판에서의 category - 질문, 답변, 판매, 구매
# 쇼핑몰에서의 category - 상의, 하의, -> 상위 카테고리 - 하위코테고리
# category에 depth를 어떻게 구현할 것이냐? 고민!
# 과제2: 검색 페이지 구현, Board?, Category?, Document?
# ex) 검색시 programming이라는 이름을 가진 1) 게시판, 2) 카테고리, 3) 게시글
# 과제3: 전화번호부
# 구현 - 이름, 전화번호, 메모 + 검색

from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
# 과제 : 페이스북으로 소셜 로그인 - heroku 업로드
# 시그널이 발생했을 때 실행 될 함수
def naver_signup(request, user, **kwargs):
    social_user = SocialAccount.objects.filter(user=user)
    if social_user.exists():
        user.last_name = social_user[0].extra_data['name']
        user.save()
# 시그널과 해당 함수 connect
# 시그널 연결방법 2가지 receiver 쓰는 방법, connect 쓰는 방법
user_signed_up.connect(naver_signup)


