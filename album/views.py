#coding=utf-8
from loveSpace.public import *
from users.models import *
from models import *
import datetime
import Image
import math
import pytz
import os
import shutil
from random import randint
from django.db import connection, transaction
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def album_show(request, *args, **kwargs):
    print 'kwargs1: ', kwargs
    if request.method == 'POST':
		print 'kjsakdja'
		album_add(request, *args, **kwargs)
    data = {}
    cursor = connection.cursor()
    cursor.execute("select * from Album where loversId = " + kwargs['lid'] + " order by Album.id desc")
    albums_info = cursor.fetchall()
    albums_info_new = []
    for one_album_info in albums_info:
        if one_album_info[5] != 0:
            cursor2 = connection.cursor()
            cursor2.execute("select Photo.name from Photo where album_id = " + str(one_album_info[0]))
            cover_name = cursor2.fetchone()
            cover_path = 'c' + cover_name[0]
        else:
            cover_path = '../../default_cover.jpg'
        albums_info_new.append({
            'id' : one_album_info[0],
            'name' : one_album_info[2],
            'desc' : one_album_info[3],
            'time' : one_album_info[4],
            'photonum' :  one_album_info[5],
            'cover': cover_path,
        })
    pageNum = int(math.ceil(len(albums_info_new) / 6.))  # 6张图片为一页，有pageNum页
    notFirst, notLast, haveAlbum = True, True, True
    if int(kwargs['pid']) == 1:
        notFirst = False
    elif int(kwargs['pid']) == pageNum:
        notLast = False
    page = [[] for i in range(pageNum)]
    if len(albums_info_new) <= 6:
        page = [[]]
        haveAlbum = False
    for i in range(len(albums_info_new)):
        page[i / 6].append(albums_info_new[i])
    pageIndex = range(1, pageNum + 1)

    data = {
        'albums': page[int(kwargs['pid']) - 1],
        'pagepost': str(int(kwargs['pid']) + 1),
        'pagepre': str(int(kwargs['pid']) - 1),
        'pageindex': pageIndex,
        'havealbum': haveAlbum,
        'notfirst': notFirst,
        'notlast': notLast,
    }
    return data


def album_add(request, *args, **kwargs):
    print 'kwargs: ', kwargs
    errors = albumAddValid(request)
    aid = 0
    if not errors:
		newAlbum = Album(
            loversId = kwargs['lovers']['lid'],
            name = request.POST['name'],
            descri = request.POST['desc'],
            time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc),
            photonum = 0,
        )
		newAlbum.save()
		
		cursor = connection.cursor()
		aid = cursor.execute('select max(id) from Album')
		aid = str(cursor.fetchone()[0])
        # mkdir for new album
		uploadFolder = os.path.join('/home/dengle/web/loveSpace/static/pic', str(kwargs['lovers']['lid']))
		if not os.path.exists(uploadFolder):
			os.mkdir(uploadFolder)
		uploadFolder = os.path.join(uploadFolder, aid)
		if not os.path.exists(uploadFolder):
			os.mkdir(uploadFolder)

    else:
		for e in errors:
			print e
    return HttpResponseRedirect('/lovers/album/' + str(kwargs['lovers']['lid']) + '/' + aid + '/page' + kwargs['pid'] +'/')


#def album(request, lid, pid):
#    errors = []
#    if request.method == 'POST':
#        errors = albumAddValid(request)
#        if not errors:
#            # add new album to db
#            newAlbum = Album(
#                loversId = lid,
#                name = request.POST['name'],
#                descri = request.POST['desc'],
#                time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
#             )
#            newAlbum.save()
#            request.session['aid'] = str(Album.objects.get(name = request.POST['name']).id)
#            # mkdir for new album
#            uploadFolder = os.path.join('/home/dengle/web/loveSpace/static/pic', str(lid))
#            if not os.path.exists(uploadFolder):
#                os.mkdir(uploadFolder)
#            uploadFolder = os.path.join(uploadFolder, str(request.session['aid']))
#            if not os.path.exists(uploadFolder):
#                os.mkdir(uploadFolder)
#
#            return HttpResponseRedirect('/lovers/album/' + lid + '/' + request.session['aid'] + '/page1/')
#    albums = Album.objects.filter(loversId = lid)
#    for album in albums:
#        tmp = album.photo_set.all()
#        album.num = len(tmp)
#        if tmp:
#            album.cover = 'c' + tmp[0].name
#        else:
#            album.cover = '../../default_cover.jpg'
#    pageNum = int(math.ceil(len(albums) / 6.))  # 6张图片为一页，有pageNum页
#    notFirst, notLast, haveAlbum = True, True, True
#    if int(pid) == 1:
#        notFirst = False
#    elif int(pid) == pageNum:
#        notLast = False
#    page = [[] for i in range(pageNum)]
#    if len(albums) == 0:
#        page = [[]]
#        haveAlbum = False
#    for i in range(len(albums)):
#        page[i / 6].append(albums[i])
#    pageIndex = range(1,pageNum + 1)
#
#    data = {
#        'errors': errors,
#        'albums': page[int(pid) - 1],
#        'lid': lid,
#        'pagepost': str(int(pid) + 1),
#        'pagepre': str(int(pid) - 1),
#        'pageindex': pageIndex,
#        'havealbum': haveAlbum,
#        'notfirst': notFirst,
#        'notlast': notLast,
#    }
#    data['lovers'] = get_lovers_info(lid)
#    return render_to_response('album.html', data ,context_instance=RequestContext(request))

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


def photos_show(request, *args, **kwargs):
    cursor = connection.cursor()
    cursor.execute("select * from Album where id = " + kwargs['aid'])
    theAlbum = cursor.fetchone()
    album_info = {
			'id':theAlbum[0],
			'name':theAlbum[2],
			'desc':theAlbum[3],
			'time':theAlbum[4],
			'photonum':theAlbum[5]}
	
    cursor.execute("select * from Photo where album_id = " + str(album_info['id']))
    photos = cursor.fetchall()
    photos_info = []
    for each_photo in photos:
		photos_info.append({
			'id':each_photo[0],
			'name':each_photo[2],
			'time':each_photo[4],
		})
    
    pageNum = int(math.ceil(len(photos_info) / 12.))  # 12张图片为一页，有pageNum页
    notFirst, notLast, havePhoto = True, True, True
    if int(kwargs['pid']) == 1:
        notFirst = False
    elif int(kwargs['pid']) == pageNum:
        notLast = False
    page = [[] for i in range(pageNum)]
    print '~~~~~', len(photos_info)
    if len(photos_info) <= 12:
        page = [[]]
        havePhoto = False
    print havePhoto
    for i in range(len(photos_info)):
        page[i / 12].append(photos_info[i])
    pageIndex = range(1,pageNum + 1)
    data = {
        'album': album_info,
        'pagepost': str(int(kwargs['pid']) + 1),
        'pagepre': str(int(kwargs['pid']) - 1),
        'pageindex': pageIndex,
        'havephoto': havePhoto,
        'notfirst': notFirst,
        'notlast': notLast,
        'photos': page[int(kwargs['pid']) - 1]
    }
    return data


@csrf_exempt
def photos_add(request, *args, **kwargs):
	errors = []
	if request.method == 'POST':
		photo = request.FILES['Filedata']
		if photoAddValid(photo, errors):
			# upload photo
			photoExt = str(photo.name.split('.')[-1])
			photoName = randomstr(16)
			uploadFolder = os.path.join(settings.MEDIA_ROOT, request.POST['lid'], request.POST['aid'])

			if not os.path.exists(uploadFolder):
				os.mkdir(uploadFolder)
			photoPath = os.path.join(uploadFolder, photoName + '.' + photoExt)
			uploadPhoto = open(photoPath, 'w')
			uploadPhoto.write(request.FILES['Filedata'].read())
			uploadPhoto.close()
			# valid photo
			im = Image.open(photoPath)
			photoWidth, photoHeight = im.size
			if photoWidth < 100 or photoHeight < 100:
				return HttpResponse('0')
			# cover
			if photoWidth > photoHeight:
				tmp = int((photoWidth-photoHeight)*1.0/2)
				box = (tmp, 0, tmp+photoHeight, photoHeight)
			else :
				tmp = int((photoHeight-photoWidth)*1.0/2)
				box = (0, tmp, photoWidth, tmp+photoWidth)
			region = im.crop(box)
			imS = region.resize((180, 180))
			photoSPath = os.path.join(uploadFolder, 'c' + photoName + '.jpg')
			imS.save(photoSPath, 'jpeg')

			# os.remove(photoPath)
			newPhoto = Photo(
				album_id = request.POST['aid'],
				name = photoName + '.jpg',
				descri = '',
				time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc),
			)
			newPhoto.save()
			print 'why?!: ', request.POST['aid']
			cursor = connection.cursor()
			cursor.execute('update Album set photonum=photonum+1 where id=' + request.POST['aid'])
			transaction.commit_unless_managed()
			print 'update Album set photonum=photonum+1 where id=' + request.POST['aid']
			return HttpResponse(photoName + '.jpg')
	return HttpResponse('0')


#@csrf_exempt
#def albumPhoto(request, lid, aid, pid):
#    theAlbum = Album.objects.get(id = aid)
#    errors = []
#    if theAlbum:
#        photos = theAlbum.photo_set.all()
#        if request.method == 'POST':
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

#            photo = request.FILES['Filedata']
#            if photoAddValid(photo, errors):
#                # upload photo
#                photoExt = str(photo.name.split('.')[-1])
#                photoName = randomstr(16)
#                uploadFolder = os.path.join('/home/dengle/web/loveSpace/static/pic', str(lid), str(aid))
#                if not os.path.exists(uploadFolder):
#                    os.mkdir(uploadFolder)
#                photoPath = os.path.join(uploadFolder, photoName + '.' + photoExt)
#                uploadPhoto = open(photoPath, 'w')
#                uploadPhoto.write(request.FILES['Filedata'].read())
#                uploadPhoto.close()
#                # valid photo
#                im = Image.open(photoPath)
#                photoWidth, photoHeight = im.size
#                # if photoWidth < 100 or photoHeight < 100:
#                #     return HttpResponse(0)
                # original
#                photoSPath = os.path.join(uploadFolder, 'o' + photoName + '.jpg')
#                im.save(photoSPath, 'jpeg')
                # show
#                if photoWidth > photoHeight:
#                    tmp = int((photoWidth-photoHeight)*1.0/2)
#                    box = (tmp, 0, tmp+photoHeight, photoHeight)
#                else :
#                    tmp = int((photoHeight-photoWidth)*1.0/2)
#                    box = (0, tmp, photoWidth, tmp+photoWidth)
#                region = im.crop(box)
#                imS = region.resize((400, 400))
#                photoSPath = os.path.join(uploadFolder, 's' + photoName + '.jpg')
#                imS.save(photoSPath, 'jpeg')
#                # cover
#                if photoWidth > photoHeight:
#                    tmp = int((photoWidth-photoHeight)*1.0/2)
#                    box = (tmp, 0, tmp+photoHeight, photoHeight)
#                else :
#                    tmp = int((photoHeight-photoWidth)*1.0/2)
#                    box = (0, tmp, photoWidth, tmp+photoWidth)
#                region = im.crop(box)
#                imS = region.resize((120, 120))
#                photoSPath = os.path.join(uploadFolder, 'c' + photoName + '.jpg')
#                imS.save(photoSPath, 'jpeg')
#
#                # os.remove(photoPath)
#                newPhoto = Photo(
#                    album = theAlbum,
#                    name = photoName + '.jpg',
#                    descri = ' ',
#                    time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc),
#                )
#                newPhoto.save()
#                thePhoto = Photo.objects.get(name = photoName + '.jpg')
#                print 'thePhoto.name', thePhoto.name
#                return HttpResponse(str(thePhoto.id) + ' ' + str(thePhoto.name))
#    else:
#        errors.append(u'该相册不存在')

 #   pageNum = int(math.ceil(len(photos) / 16.))  # 16张图片为一页，有pageNum页
 #   notFirst, notLast, havePhoto = True, True, True
 #   if int(pid) == 1:
 #       notFirst = False
 #   elif int(pid) == pageNum:
 #       notLast = False
 #   page = [[] for i in range(pageNum)]
 #   if len(photos) == 0:
 #       page = [[]]
 #       havePhoto = False
 #   for i in range(len(photos)):
 #       page[i / 16].append(photos[i])
 #   pageIndex = range(1,pageNum + 1)
 #   data = {
 #       'lid': lid,
 #       'aid': aid,
 #       'pagepost': str(int(pid) + 1),
 #       'pagepre': str(int(pid) - 1),
 #       'pageindex': pageIndex,
 #       'havephoto': havePhoto,
 #       'notfirst': notFirst,
 #       'notlast': notLast,
 #       'album': theAlbum,
 #       'photos': page[int(pid) - 1]
 #   }
 #   data['lovers'] = get_lovers_info(lid)
 #   return render_to_response('albumPhoto.html', data, context_instance=RequestContext(request))

# def albumPhoto(request, lid, aid, pid):
#     theAlbum = Album.objects.get(id = aid)
#     thePhoto = Photo.objects.get(id = pid)
#     return render_to_response('albumPhoto.html', data, context_instance=RequestContext(request))


def delete_album(request, *args, **kwargs):
	print '???????'
	result = '0'
	print request.method
	print request.session.get('uid', None)
	print request.POST['uid']
	if request.method == 'POST' and request.session.get('uid', None) == request.POST['uid']:
		aid = request.POST['aid']
		print aid
		lid = request.POST['lid']
		print lid
		cursor = connection.cursor()
		print '1'
		cursor.execute('delete from Photo where album_id=' + str(aid))
		print '2'
		cursor.execute('delete from Album where id=' + str(aid))
		transaction.commit_unless_managed()
		album_path = settings.MEDIA_ROOT + '/' + lid + '/' + aid
		if os.path.exists(album_path):
			shutil.rmtree(album_path)
		result = '1'
	return HttpResponse(result)


def delete_photo(request, *args, **kwargs):
	print '~~~~~~~~~~'
	result = '0'
	if request.method == 'POST' and request.session.get('uid', None) == request.POST['uid']:
		photo_name = request.POST['photo_name']
		print photo_name
		lid = request.POST['lid']
		print lid
		aid = request.POST['aid']
		print aid
		cursor = connection.cursor()
		print '1'
		print 'delete from Photo where name=' + str(photo_name) + ' and album_id =' + aid
		cursor.execute("delete from Photo where name='" + str(photo_name) + "'")
		print '2'
		cursor.execute('update Album set photonum=photonum-1 where id=' + aid)
		transaction.commit_unless_managed()
		print '3'
		photo_path1 = settings.MEDIA_ROOT + '/' + lid + '/' + aid + '/' + photo_name
		print photo_path1
		photo_path2 = settings.MEDIA_ROOT + '/' + lid + '/' + aid + '/c' + photo_name
		print photo_path2
		if os.path.isfile(photo_path1):
			os.remove(photo_path1)
		print '4'
		if os.path.isfile(photo_path2):
			os.remove(photo_path2)
		print '5'
		result = '1'
	return HttpResponse(result)


def albumAddValid(request):
    errors = []
    if not request.POST.get('name', ''):
        errors.append(u'缺少相册名称')
    if not request.POST.get('desc', ''):
        errors.append(u'缺少相册描述')
    return errors


def photoAddValid(photo, errors):
    if not photo:
        print 'no photo'
        errors.append(u'请选择图片上传')
        return False
    photoExt = str(photo.name.split('.')[-1])
    if not photoExt in ['jpg', 'jpeg', 'png', 'gif', 'JPG', 'JPEG', 'PNG']:
        errors.append(u'图片格式错误')
        return False
    return True


def randomstr(n):
    wholeStr = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    subStr = ''
    for i in range(n) :
        subStr += wholeStr[randint(0, 61)]
    return subStr

# 匿名用户，用户访问自己空间，用户有情侣访问别人空间，用户没情侣访问别人空间四种
