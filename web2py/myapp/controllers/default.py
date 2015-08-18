# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
from temp_humi_co2 import *

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    session.which_task = 1
    response.flash = T("Hi everyone!")
    return dict(message=T('Welcome to ChanMin\'s blog'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

def project_temp_humi_co2():
    r_temp = reading(1)
    r_humi = reading(2)
    r_value = calc(r_temp, r_humi)
    r_co2 = getCO2()
    return dict(temp = "%.7s"%(r_value[0]), humi = "%.7s"%(r_value[1]), co2 = r_co2)

def project_tablebar_setting():
    form = SQLFORM(db.tablebar_schedules, deletable=True)
    if form.accepts(request,session):
        response.flash = 'Thanks! The form has been submitted.'
    elif form.errors:
        response.flash = 'Please correct the error(s).'
    else:
        response.flash = 'Try again - no fields can be empty.'
    
    rows = db(db.tablebar_schedules.id>0).select()
    
    form2 = SQLFORM(db.tablebar_user_location)
    if form2.accepts(request,session):
        response.flash = 'Good! Your location is set.'
    elif form2.errors:
        response.flash = 'Please check your location.'
    else:
        response.flash = 'Enter your location.'
        
    rows2 = db(db.tablebar_user_location.id>0).select()
        
    return dict(form=form, rows=rows, form2=form2, rows2=rows2)

def database_update_delete():
    if request.args(0) == 'tablebar_schedules':
        if request.args(1) == 'update':
            update = db.tablebar_schedules(request.args(2))
            form = SQLFORM(db.tablebar_schedules, update, deletable=True)
            if form.accepts(request,session):
                return dict(form=redirect(URL('myapp','default','project_tablebar_setting')))
            elif form.errors:
                response.flash = 'Please correct the error(s).'
            else:
                response.flash = 'Try again - no fields can be empty.'
            return dict(form=form, table='tablebar_schedules', state='update')
            
        if request.args(1) == 'delete':
            db(db.tablebar_schedules.id == request.args(2)).delete()
            return dict(form=redirect(URL('myapp','default','project_tablebar_setting')))
    elif request.args(0) == 'tablebar_user_location':
        if request.args(1) == 'delete':
            db(db.tablebar_user_location.id == request.args(2)).delete()
            return dict(form=redirect(URL('myapp','default','project_tablebar_setting')))

def profile():
    return dict()

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
