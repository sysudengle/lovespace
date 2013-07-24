#coding=utf-8
from loveSpace.public import *
from users.models import *
from models import *
import datetime
import Image
import math
import pytz
import os
from random import randint
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
# Create your views here.


def album(request, lid, pid):
    errors = []
    if request.method == 'POST':
        errors = albumAddValid(request)
        if not errors:
            # add new album to db
            newAlbum = Album(
                loversId = lid,
                name = request.POST['name'],
                desc = request.POST['desc'],
                time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
             )
            newAlbum.save()
            request.session['aid'] = str(Album.objects.get(name = request.POST['name']).id)
            # mkdir for new album
            uploadFolder = os.path.join('/home/dengle/web/loveSpace/static/pic', str(lid))
            if not os.path.exists(uploadFolder):
                os.mkdir(uploadFolder)
            uploadFolder = os.path.join(uploadFolder, str(request.session['aid']))
            if not os.path.exists(uploadFolder):
                os.mkdir(uploadFolder)

            return HttpResponseRedirect('/lovers/album/' + lid + '/' + request.session['aid'] + '/page1/')
    albums = Album.objects.filter(loversId = lid)
    for album in albums:
        tmp = album.photo_set.all()
        album.num = len(tmp)
        if tmp:
            album.cover = 'c' + tmp[0].name
        else:
            album.cover = '../../default_cover.jpg'
    pageNum = int(math.ceil(len(albums) / 6.))  # 6张图片为一页，有pageNum页
    notFirst, notLast, haveAlbum = True, True, True
    if int(pid) == 1:
        notFirst = False
    elif int(pid) == pageNum:
        notLast = False
    page = [[] for i in range(pageNum)]
    if len(albums) == 0:
        page = [[]]
        haveAlbum = False
    for i in range(len(albums)):
        page[i / 6].append(albums[i])
    pageIndex = range(1,pageNum + 1)

    data = {
        'errors': errors,
        'albums': page[int(pid) - 1],
        'lid': lid,
        'pagepost': str(int(pid) + 1),
        'pagepre': str(int(pid) - 1),
        'pageindex': pageIndex,
        'havealbum': haveAlbum,
        'notfirst': notFirst,
        'notlast': notLast,
    }
    data['lovers'] = get_lovers_info(lid)
    return render_to_response('album.html', data ,context_instance=RequestContext(request))

# def albumAdd(request, lid):
#     errors = []
#     if request.method == 'POST':
#         errors = albumAddValid(request)
#         if not errors:
#             # add new album to db
#             newAlbum = Album(
#                 loversId = lid,
#                 name = request.POST['name'],
#                 desc = request.POST['desc'],
#                 time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
#              )
#             newAlbum.save()
#             request.session['aid'] = str(Album.objects.get(name = request.POST['name']).id)
#             # mkdir for new album
#             uploadFolder = os.path.join('/home/zhyin/workspace/loveSpace/static/pic', str(lid))
#             if not os.path.exists(uploadFolder):
#                 os.mkdir(uploadFolder)
#             uploadFolder = os.path.join(uploadFolder, str(request.session['aid']))
#             if not os.path.exists(uploadFolder):
#                 os.mkdir(uploadFolder)
#
#             return HttpResponseRedirect('/lovers/album/' + lid + '/' + request.session['aid'] + '/page1/')
#     return render_to_response('albumAdd.html', {'errors': errors},context_instance=RequestContext(request))

@csrf_exempt
def albumPhoto(request, lid, aid, pid):
    theAlbum = Album.objects.get(id = aid)
    errors = []
    if theAlbum:
        photos = theAlbum.photo_set.all()
        if request.method == 'POST':
            # if request.POST.get('comment', ''):
            #     photoid = int(request.POST.get('photoid', ''))
            #     thephoto = Photo.objects.get(id = photoid)
            #     userid = int(request.session['uid'])
            #     theuser = U
            #     newPhoto = Photo(
            #         photo = thephoto,
            #         user = models.IntegerField(max_length = 11)
            #         content = models.CharField(max_length = 200, null = True)
            #         time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc),

            #         album = theAlbum,
            #         name = photoName + '.jpg',
            #         desc = '',
            #     )
            #     newPhoto.save()

            photo = request.FILES['Filedata']
            if photoAddValid(photo, errors):
                # upload photo
                photoExt = str(photo.name.split('.')[-1])
                photoName = randomstr(16)
                uploadFolder = os.path.join('/home/dengle/web/loveSpace/static/pic', str(lid), str(aid))
                if not os.path.exists(uploadFolder):
                    os.mkdir(uploadFolder)
                photoPath = os.path.join(uploadFolder, photoName + '.' + photoExt)
                uploadPhoto = open(photoPath, 'w')
                uploadPhoto.write(request.FILES['Filedata'].read())
                uploadPhoto.close()
                # valid photo
                im = Image.open(photoPath)
                photoWidth, photoHeight = im.size
                # if photoWidth < 100 or photoHeight < 100:
                #     return HttpResponse(0)
                # original
                photoSPath = os.path.join(uploadFolder, 'o' + photoName + '.jpg')
                im.save(photoSPath, 'jpeg')
                # show
                if photoWidth > photoHeight:
                    tmp = int((photoWidth-photoHeight)*1.0/2)
                    box = (tmp, 0, tmp+photoHeight, photoHeight)
                else :
                    tmp = int((photoHeight-photoWidth)*1.0/2)
                    box = (0, tmp, photoWidth, tmp+photoWidth)
                region = im.crop(box)
                imS = region.resize((400, 400))
                photoSPath = os.path.join(uploadFolder, 's' + photoName + '.jpg')
                imS.save(photoSPath, 'jpeg')
                # cover
                if photoWidth > photoHeight:
                    tmp = int((photoWidth-photoHeight)*1.0/2)
                    box = (tmp, 0, tmp+photoHeight, photoHeight)
                else :
                    tmp = int((photoHeight-photoWidth)*1.0/2)
                    box = (0, tmp, photoWidth, tmp+photoWidth)
                region = im.crop(box)
                imS = region.resize((120, 120))
                photoSPath = os.path.join(uploadFolder, 'c' + photoName + '.jpg')
                imS.save(photoSPath, 'jpeg')

                # os.remove(photoPath)
                newPhoto = Photo(
                    album = theAlbum,
                    name = photoName + '.jpg',
                    desc = '',
                    time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc),
                )
                newPhoto.save()
                thePhoto = Photo.objects.get(name = photoName + '.jpg')
                print '~~~~', thePhoto.name
                return HttpResponse(str(thePhoto.id) + ' ' + str(thePhoto.name))
    else:
        errors.append(u'该相册不存在')

    pageNum = int(math.ceil(len(photos) / 16.))  # 16张图片为一页，有pageNum页
    notFirst, notLast, havePhoto = True, True, True
    if int(pid) == 1:
        notFirst = False
    elif int(pid) == pageNum:
        notLast = False
    page = [[] for i in range(pageNum)]
    if len(photos) == 0:
        page = [[]]
        havePhoto = False
    for i in range(len(photos)):
        page[i / 16].append(photos[i])
    pageIndex = range(1,pageNum + 1)
    data = {
        'lid': lid,
        'aid': aid,
        'pagepost': str(int(pid) + 1),
        'pagepre': str(int(pid) - 1),
        'pageindex': pageIndex,
        'havephoto': havePhoto,
        'notfirst': notFirst,
        'notlast': notLast,
        'album': theAlbum,
        'photos': page[int(pid) - 1]
    }
    data['lovers'] = get_lovers_info(lid)
    return render_to_response('albumPhoto.html', data, context_instance=RequestContext(request))

# def albumPhoto(request, lid, aid, pid):
#     theAlbum = Album.objects.get(id = aid)
#     thePhoto = Photo.objects.get(id = pid)
#     return render_to_response('albumPhoto.html', data, context_instance=RequestContext(request))

def albumAddValid(request):
    errors = []
    if not request.POST.get('name', ''):
        errors.append(u'缺少相册名称')
    if not request.POST.get('desc', ''):
        errors.append(u'缺少相册描述')
    return errors

def photoAddValid(photo, errors):
    if not photo:
        errors.append(u'请选择图片上传')
        return False
    # print 'value: ', photo.name
    # print 'type: ', type(photo.name)
    photoExt = str(photo.name.split('.')[-1])
    # print 'ext: ', photoExt
    if not photoExt in ['jpg', 'jpeg', 'png', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF']:
        errors.append(u'图片格式错误')
        return False
    print 'true'
    return True



def randomstr(n):
    wholeStr = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    subStr = ''
    for i in range(n) :
        subStr += wholeStr[randint(0, 61)]
    return subStr

#     http://localhost:8000/lovers/home/6/
# http://localhost:8000/9/user/
# 匿名用户，用户访问自己空间，用户有情侣访问别人空间，用户没情侣访问别人空间四种
