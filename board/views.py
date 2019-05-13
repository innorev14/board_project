from django.shortcuts import render, get_object_or_404
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

def document_create(request):
    #Document.objects.create() - 실행과 동시에 DB에 삽입(올바른 데이터가 있어야 함)
    return render(request, 'board/document_create.html')

def document_update(request):
    # 객체 불러와서, 데이터 수정
    return render(request, 'board/document_update.html')

def document_detail(request, document_id):
    #단일 객체 던지고 -> 컨텍스트 밸류로 받음
    document = Document.objects.get(pk=document_id)
    return render(request, 'board/document_detail.html', {'object':document})

def document_delete(request):
    # 객체 불러와서, delete만 호출
    return render(request, 'board/document_delete.html')
