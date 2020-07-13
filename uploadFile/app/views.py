from django.http import HttpResponse
from django.shortcuts import render
import string
import os

#html自动转义案例
def htmlTest(request):
    return render(request, 'html_test.html')

def upload_check(request):
    md5 = request.GET.get('md5')    # 获取文件的md5值
    file_name = request.GET.get('name')     # 获取文件名
    cwd = os.getcwd()
    upload_folder = os.path.join(cwd, 'upload/%s' % md5)    # md5拼接出文件夹
    if not os.path.exists(upload_folder):   # 如果该文件夹不存在，该文件没有上传过
        os.makedirs(upload_folder)
        return HttpResponse('success')
    else:       # 文件夹存在，判断文件是否上传成功或文件已上传的文件块数
        return HttpResponse(get_max_chunk(upload_folder, file_name))

def get_max_chunk(path, file_name):
    files = []
    list_ = os.listdir(path)
    if len(list_) == 1 and list_[0] == file_name:   # 文件上传成功
        return 'complete'
    return len(list_) - 1

def upload_file_m(request): 
    if request.method == 'POST':
        task = request.GET.get('md5')       # 不同的文件的md5值
        chunk = request.GET.get('chunk', 0)     # 该文件的chunk号，第几块数据
        filename = '%s/%s' % (task, chunk)      # file path： md5/chunk
        b = request.read()      # 获取二进制流
        cwd = os.getcwd()
        file_wrap = os.path.join(cwd, 'upload/%s' % filename)   #获取文件的绝对路径
        if os.path.exists(file_wrap):
            os.remove(file_wrap)

        # 写文件块  
        f = open(file_wrap,'wb+')
        f.write(b)
        f.close()

    return HttpResponse('success')

def upload_success(request):
    target_filename = request.GET.get('filename')   # 获取文件名
    task = request.GET.get('md5')       # 获取文件的md5值
    cwd = os.getcwd()
    chunk = 0
    # 把所有的文件块写入到一个文件中
    if not os.path.exists(os.path.join(cwd, 'upload/%s/%s' % (task, target_filename))):
        with open(os.path.join(cwd, 'upload/%s/%s' % (task, target_filename)), 'wb+') as target_file:
            while True:
                try:
                    filename = os.path.join(cwd, 'upload/%s/%d' % (task, chunk))
                    source_file = open(filename, 'rb')
                    target_file.write(source_file.read())
                    source_file.close()
                except IOError:
                    break
                chunk += 1
                os.remove(filename)      
    return HttpResponse('success')

