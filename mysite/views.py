# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, render_to_response
from django.forms import ModelForm
from django.core.context_processors import csrf
from mysite.models import Dutyreg, Extraworkreg, Holidutyreg, Variable
# Create your views here.
import time
import os
import datetime
import random
import string
import csv


def digits_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def str_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def init(request):
    return HttpResponse(os.path.abspath(os.path.join(os.path.dirname(__file__))))
    try:
        Variable.objects.all().delete()
        Variable(varname="adminpass", varval="123456").save()
        Variable(varname="defaultmoney", varval='0').save()
        return HttpResponse("Finished!")
    except:
        return HttpResponse("Error!")


def chgpass(request):
    newpass = request.POST.get('password', None)
    if newpass:
        # try:
        var = Variable.objects.all().filter(varname='adminpass')[0]
        var.varval = (newpass)
        var.save()
        return response_spcinf(request, '修改成功！新密码为:' + newpass.encode('utf8'), 'dj:admin')
        # except:
        #    return response_spcinf(request,'未知错误','dj:admin')
    else:
        return render_to_response('mysite/chgpass.html', context_instance=RequestContext(request))


def makedutyreg(request):
    queryresults = Dutyreg.objects.all().filter(date=datetime.date.today())
    if len(queryresults) > 0:
        duty = queryresults[0]
    else:
        duty = Dutyreg()
        duty.save()
    c = {'duty': duty,
         }
    return render_to_response(
        'mysite/duty.html', c, context_instance=RequestContext(request))


def generate_data(request):
    pass
    """
    # try:
    Dutyreg.objects.all().delete()
    Extraworkreg.objects.all().delete()
    curdate = datetime.date(2014, 1, 1)
    delta = datetime.timedelta(days=1)
    while curdate <= datetime.date(2015, 3, 12):
        duty = Dutyreg(date=curdate, amname=str_generator(), amamount=digits_generator(), pmname=str_generator(
        ), pmamount=digits_generator(), evename=str_generator(), eveamount=digits_generator(), remark=str_generator(size=50))
        duty.save()
        extrawork = Extraworkreg(date=curdate, amname=str_generator(), amamount=digits_generator(), amtext=str_generator(size=50), pmname=str_generator(), pmtext=str_generator(
            size=50), pmamount=digits_generator(), evename=str_generator(), evetext=str_generator(size=50), eveamount=digits_generator(), remark=str_generator(size=50))
        extrawork.save()
        holiduty = Holidutyreg(date=curdate,
                               emergencyteamname=str_generator(),
                               emergencyteamamount=digits_generator(),
                               servicecentername=str_generator(),
                               servicecenteramount=digits_generator(),
                               generaldutyname=str_generator(),
                               generaldutyamount=digits_generator(),
                               amphonedutyname=str_generator(),
                               amphonedutyamount=digits_generator(),
                               amengineername=str_generator(),
                               amengineeramount=digits_generator(),
                               pmphonedutyname=str_generator(),
                               pmphonedutyamount=digits_generator(),
                               pmengineername=str_generator(),
                               pmengineeramount=digits_generator(),
                               evedutyname=str_generator(),
                               evedutyamount=digits_generator(),
                               remark=str_generator(size=50))
        holiduty.save()
        curdate += delta
    return HttpResponse('Finished!')
    # except:
    #    return HttpResponse('Error!')
    """

def makeextraworkreg(request):
    queryresults = Extraworkreg.objects.all().filter(
        date=datetime.date.today())
    if len(queryresults) > 0:
        extrawork = queryresults[0]
    else:
        extrawork = Extraworkreg()
        extrawork.save()
    c = {'extrawork': extrawork,
         }
    return render_to_response(
        'mysite/extrawork.html', c, context_instance=RequestContext(request))


def makeholidutyreg(request):
    queryresults = Holidutyreg.objects.all().filter(
        date=datetime.date.today())
    if len(queryresults) > 0:
        holiduty = queryresults[0]
    else:
        holiduty = Holidutyreg()
        holiduty.save()
    c = {'holiduty': holiduty,
         }
    return render_to_response('mysite/holiduty.html', c, context_instance=RequestContext(request))


def response_success(request, retlink):
    msgtext = "提交成功!"
    c = {"msgtext": msgtext,
         "retlink": retlink,
         }
    return render_to_response('mysite/msgbox.html', c, context_instance=RequestContext(request))


def response_wrong(request, retlink):
    msgtext = "未知错误，请按格式填写。"
    c = {"msgtext": msgtext,
         "retlink": retlink,
         }
    return render_to_response('mysite/msgbox.html', c, context_instance=RequestContext(request))


def response_spcinf(request, msgtext, retlink):
    c = {"msgtext": msgtext,
         "retlink": retlink,
         }
    return render_to_response('mysite/msgbox.html', c, context_instance=RequestContext(request))


def handleduty(request):
    queryresults = Dutyreg.objects.all().filter(date=datetime.date.today())
    msgtext = ""
    if len(queryresults) > 0:
        try:
            cur_duty = queryresults[0]
            cur_duty.amname = request.POST['amname']
            cur_duty.amamount = int(request.POST['amamount'])
            cur_duty.pmname = request.POST['pmname']
            cur_duty.pmamount = int(request.POST['pmamount'])
            cur_duty.evename = request.POST['evename']
            cur_duty.eveamount = int(request.POST['eveamount'])
            if request.POST['remark'].strip() != "":
                if cur_duty.remark == ' ':
                    cur_duty.remark += (request.POST['remark'])
                else:
                    cur_duty.remark += ' | ' + (request.POST['remark'])
            cur_duty.save()
        except:
            return response_wrong(request, 'dj:duty')
    else:
        return response_wrong(request, 'dj:duty')
    return response_success(request, 'dj:duty')


def handleholiduty(request):
    queryresults = Holidutyreg.objects.all().filter(date=datetime.date.today())
    msgtext = ""
    if len(queryresults) > 0:
        try:
            cur_holiduty = queryresults[0]
            cur_holiduty.emergencyteamname = request.POST['emergencyteamname']
            cur_holiduty.emergencyteamamount = request.POST[
                'emergencyteamamount']
            cur_holiduty.servicecentername = request.POST['servicecentername']
            cur_holiduty.servicecenteramount = request.POST[
                'servicecenteramount']
            cur_holiduty.generaldutyname = request.POST['generaldutyname']
            cur_holiduty.generaldutyamount = request.POST['generaldutyamount']
            cur_holiduty.amphonedutyname = request.POST['amphonedutyname']
            cur_holiduty.amphonedutyamount = request.POST['amphonedutyamount']
            cur_holiduty.amengineername = request.POST['amengineername']
            cur_holiduty.amengineeramount = request.POST['amengineeramount']
            cur_holiduty.pmphonedutyname = request.POST['pmphonedutyname']
            cur_holiduty.pmphonedutyamount = request.POST['pmphonedutyamount']
            cur_holiduty.pmengineername = request.POST['pmengineername']
            cur_holiduty.pmengineeramount = request.POST['pmengineeramount']
            cur_holiduty.evedutyname = request.POST['evedutyname']
            cur_holiduty.evedutyamount = request.POST['evedutyamount']
            if request.POST['remark'].strip() != "":
                if cur_holiduty.remark == ' ':
                    cur_holiduty.remark += (request.POST['remark'])
                else:
                    cur_holiduty.remark += ' | ' + (request.POST['remark'])
            cur_holiduty.save()
        except:
            return response_wrong(request, 'dj:holiduty')
    else:
        return response_wrong(request, 'dj:holiduty')
    return response_success(request, 'dj:holiduty')


def handleextrawork(request):
    queryresults = Extraworkreg.objects.all().filter(
        date=datetime.date.today())
    msgtext = ""
    if len(queryresults) > 0:
        try:
            cur_extrawork = queryresults[0]
            cur_extrawork.amname = request.POST['amname']
            cur_extrawork.amtext = request.POST['amtext']
            cur_extrawork.amamount = int(request.POST['amamount'])
            cur_extrawork.pmname = request.POST['pmname']
            cur_extrawork.pmtext = request.POST['pmtext']
            cur_extrawork.pmamount = int(request.POST['pmamount'])
            cur_extrawork.evename = request.POST['evename']
            cur_extrawork.evetext = request.POST['evetext']
            cur_extrawork.eveamount = int(request.POST['eveamount'])
            if request.POST['remark'].strip() != "":
                if cur_extrawork.remark == ' ':
                    cur_extrawork.remark += (request.POST['remark'])
                else:
                    cur_extrawork.remark += ' | ' + (request.POST['remark'])
            cur_extrawork.save()
        except:
            return response_wrong(request, 'dj:extrawork')
    else:
        return response_wrong(request, 'dj:extrawork')
    return response_success(request, 'dj:extrawork')


def index(request):
    return render_to_response('mysite/index.html', context_instance=RequestContext(request))
    # return render_to_response('mysite/duty.html',
    # context_instance=RequestContext(request))


def login(request):
    return render_to_response('mysite/login.html', context_instance=RequestContext(request))


def gettable(request):
    # try:
    savetype = request.POST.get('savetype', None)
    savedate = request.POST.get('savedate', None)
    if savedate:
        savedate_list = savedate.split('-')
        savedate = datetime.date(
            int(savedate_list[0]), int(savedate_list[1]), int(savedate_list[2]))
    if savetype:
        if savetype == "extrawork":
            spc_extrawork = Extraworkreg.objects.all().filter(
                date=savedate)[0]
            spc_extrawork.amname = request.POST['amname']
            spc_extrawork.amtext = request.POST['amtext']
            spc_extrawork.amamount = request.POST['amamount']
            spc_extrawork.pmname = request.POST['pmname']
            spc_extrawork.pmtext = request.POST['pmtext']
            spc_extrawork.pmamount = request.POST['pmamount']
            spc_extrawork.evename = request.POST['evename']
            spc_extrawork.evetext = request.POST['evetext']
            spc_extrawork.eveamount = request.POST['eveamount']
            spc_extrawork.remark = request.POST['remark']
            spc_extrawork.save()
        elif savetype == "duty":
            spc_duty = Dutyreg.objects.all().filter(date=savedate)[0]
            spc_duty.amname = request.POST['amname']
            spc_duty.amamount = request.POST['amamount']
            spc_duty.pmname = request.POST['pmname']
            spc_duty.pmamount = request.POST['pmamount']
            spc_duty.evename = request.POST['evename']
            spc_duty.eveamount = request.POST['eveamount']
            spc_duty.remark = request.POST['remark']
            spc_duty.save()
        elif savetype == "holiduty":
            spc_holiduty = Holidutyreg.objects.all().filter(
                date=savedate)[0]
            spc_holiduty.emergencyteamname = request.POST[
                'emergencyteamname']
            spc_holiduty.emergencyteamamount = request.POST[
                'emergencyteamamount']
            spc_holiduty.servicecentername = request.POST[
                'servicecentername']
            spc_holiduty.servicecenteramount = request.POST[
                'servicecenteramount']
            spc_holiduty.generaldutyname = request.POST['generaldutyname']
            spc_holiduty.generaldutyamount = request.POST[
                'generaldutyamount']
            spc_holiduty.amphonedutyname = request.POST['amphonedutyname']
            spc_holiduty.amphonedutyamount = request.POST[
                'amphonedutyamount']
            spc_holiduty.amengineername = request.POST['amengineername']
            spc_holiduty.amengineeramount = request.POST[
                'amengineeramount']
            spc_holiduty.pmphonedutyname = request.POST['pmphonedutyname']
            spc_holiduty.pmphonedutyamount = request.POST[
                'pmphonedutyamount']
            spc_holiduty.pmengineername = request.POST['pmengineername']
            spc_holiduty.pmengineeramount = request.POST[
                'pmengineeramount']
            spc_holiduty.evedutyname = request.POST['evedutyname']
            spc_holiduty.evedutyamount = request.POST['evedutyamount']
            spc_holiduty.remark = request.POST['remark']
            spc_holiduty.save()
        else:
            pass

    sdate_str = request.POST['sdate']
    tdate_str = request.POST['tdate']
    sdate_list = sdate_str.split('-')
    tdate_list = tdate_str.split('-')
    sdate = datetime.date(
        int(sdate_list[0]), int(sdate_list[1]), int(sdate_list[2]))
    tdate = datetime.date(
        int(tdate_list[0]), int(tdate_list[1]), int(tdate_list[2]))
    cxtype = request.POST['cxtype']
    if cxtype == 'extrawork':
        rst_list = Extraworkreg.objects.all().filter(
            date__gte=sdate, date__lte=tdate).order_by('date')
        c = {
            'extrawork_list': rst_list,
            'selectfg': 'extrawork',
            'lstsdate': sdate_str,
            'lsttdate': tdate_str,
        }
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__))) + '/static/mysite/down.csv', 'wb') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(
                ["日期", "上午名字", "加班内容", "金额", "下午名字", "加班内容", "金额", "晚上名字", "加班内容", "金额", "备注"])
            for extrawork in rst_list:
                writer.writerow([str((extrawork.date).isoformat()), unicode(extrawork.amname).encode('utf8'), unicode(extrawork.amtext).encode('utf8'), str(extrawork.amamount), unicode(extrawork.pmname).encode('utf8'), unicode(
                    extrawork.pmtext).encode('utf8'), str(extrawork.pmamount), unicode(extrawork.evename).encode('utf8'), unicode(extrawork.evetext).encode('utf8'), str(extrawork.eveamount), unicode(extrawork.remark).encode('utf8')])
        return render_to_response('mysite/admin.html', c, context_instance=RequestContext(request))
    elif cxtype == 'duty':
        rst_list = Dutyreg.objects.all().filter(
            date__gte=sdate, date__lte=tdate).order_by('date')
        c = {
            'duty_list': rst_list,
            'selectfg': 'duty',
            'lstsdate': sdate_str,
            'lsttdate': tdate_str,
        }
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__))) + '/static/mysite/down.csv', 'wb') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(
                ["日期", "上午名字", "金额", "下午名字", "金额", "晚上名字", "金额", "备注"])
            for extrawork in rst_list:
                writer.writerow([str((extrawork.date).isoformat()), unicode(extrawork.amname).encode('utf8'), str(extrawork.amamount), unicode(extrawork.pmname).encode(
                    'utf8'), str(extrawork.pmamount), unicode(extrawork.evename).encode('utf8'), str(extrawork.eveamount), unicode(extrawork.remark).encode('utf8')])

        return render_to_response('mysite/admin.html', c, context_instance=RequestContext(request))
    elif cxtype == 'holiduty':
        rst_list = Holidutyreg.objects.all().filter(
            date__gte=sdate, date__lte=tdate).order_by('date')
        c = {
            'holiduty_list': rst_list,
            'selectfg': 'holiduty',
            'lstsdate': sdate_str,
            'lsttdate': tdate_str,
        }
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__))) + '/static/mysite/down.csv', 'wb') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(
                ["日期", "应急小组", "金额", "客服中心收费人", "金额", "总值班人", "金额", "上午电话值班人", "金额", "上午工程值班人", "金额", "下午电话值班人", "金额", "下午工程值班人", "金额", "晚上值班人", "金额", "备注"])
            for holiduty in rst_list:
                writer.writerow([str((holiduty.date).isoformat()),
                                 unicode(holiduty.emergencyteamname).encode(
                                     'utf8'),
                                 unicode(holiduty.emergencyteamamount).encode(
                                     'utf8'),
                                 unicode(holiduty.servicecentername).encode(
                                     'utf8'),
                                 unicode(holiduty.servicecenteramount).encode(
                                     'utf8'),
                                 unicode(holiduty.generaldutyname).encode(
                                     'utf8'),
                                 unicode(holiduty.generaldutyamount).encode(
                                     'utf8'),
                                 unicode(holiduty.amphonedutyname).encode(
                                     'utf8'),
                                 unicode(holiduty.amphonedutyamount).encode(
                                     'utf8'),
                                 unicode(holiduty.amengineername).encode(
                                     'utf8'),
                                 unicode(holiduty.amengineeramount).encode(
                                     'utf8'),
                                 unicode(holiduty.pmphonedutyname).encode(
                                     'utf8'),
                                 unicode(holiduty.pmphonedutyamount).encode(
                                     'utf8'),
                                 unicode(holiduty.pmengineername).encode(
                                     'utf8'),
                                 unicode(holiduty.pmengineeramount).encode(
                                     'utf8'),
                                 unicode(holiduty.evedutyname).encode('utf8'),
                                 unicode(holiduty.evedutyamount).encode(
                                     'utf8'),
                                 unicode(holiduty.remark).encode('utf8'), ]
                                )
        return render_to_response('mysite/admin.html', c, context_instance=RequestContext(request))
    else:
        return response_spcinf(request, "Failed to query!", 'dj:admin')
    # except:
    #    return response_spcinf(request, "Error!", 'dj:admin')


def down(request):
    import os
    import tempfile
    import zipfile
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes
    filename = os.path.abspath(
        os.path.join(os.path.dirname(__file__))) + "/static/mysite/down.csv"
    download_name = "down.csv"
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = "attachment; filename=%s" % download_name
    return response


def handlelogin(request):
    try:
        if request.POST['password'] == Variable.objects.all().filter(varname='adminpass')[0].varval:
            request.session['password'] = request.POST['password']
            return admin(request)
        else:
            return response_spcinf(request, "Failed to login!", 'dj:login')
    except:
        return response_spcinf(request, "Error!", 'dj:login')


def duty(request):
    return makedutyreg(request)


def extrawork(request):
    return makeextraworkreg(request)


def holiduty(request):
    return makeholidutyreg(request)


def admin(request):
    try:
        if request.session['password'] == Variable.objects.all().filter(varname='adminpass')[0].varval:
            return render_to_response('mysite/admin.html', context_instance=RequestContext(request))
        else:
            return response_spcinf(request, "Failed to login!", 'dj:login')
    except:
        return response_spcinf(request, "Error!", 'dj:login')
