#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
# import jinja2
import os
import datetime

import logging
import webapp2
import json

# from webapp2_extras import jinja2

# os.environ['DJANGO_SETTINGS_MODULE'] = 'memartlbuy.settings'
# import django.core.handlers.wsgi
# from google.appengine.dist import use_library
# use_library('django', '1.2')

# from django.utils import simplejson
# from webapp2_extras import users
# import users
from google.appengine.api import users
# from google.appengine.api import memcache
# from google.appengine.ext import db
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.api.datastore_types import PhoneNumber


# import gdata.docs.service

# from google.appengine.ext.webapp2 import util
# from google.appengine.ext.webapp.util import run_wsgi_app
# from google.appengine.ext.webapp2.util import login_required

# #import sys
# #from pyasn1_modules.rfc2459 import StreetAddress
# sys.path.insert(0, 'reportlab.zip')
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.units import mm
# from reportlab.lib.colors import pink, black, red, blue, green
# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import *
# from reportlab.pdfgen.canvas import Canvas
# from reportlab.lib.pagesizes import letter, A4
# #from django.http import HttpResponse
# #from reportlab.pdfbase import pdfmetrics
# ##import reportlab

# jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)

class Audit(ndb.Model):
    author = ndb.UserProperty()
    date_added = ndb.DateTimeProperty(auto_now_add=True)
    date_changed = ndb.DateTimeProperty(auto_now=True)   


class Address(ndb.Model):
    # ===========================================================================
    # add_type = ndb.StringProperty(
    #     choices=('home', 'work', 'postal')) 
    # ===========================================================================
    street = ndb.StringProperty()
    suburb = ndb.StringProperty() 
    town = ndb.StringProperty()
    province = ndb.StringProperty()
    postal_code = ndb.StringProperty()


class PhoneNum(ndb.Model):
    """A model representing a phone number."""
    # ===========================================================================
    # phone_type = ndb.StringProperty(
    #     choices=('home', 'work', 'mobile', 'other'))
    # ===========================================================================
    country_code = ndb.StringProperty()
    number = ndb.StringProperty()

class Customer(ndb.Model):
    customer_name = ndb.StringProperty(required=True)  
    customer_code = ndb.StringProperty(required=False)        
    customer_id = ndb.StringProperty(required=True)    
    customer_address = ndb.StructuredProperty(Address, repeated=False)
    customer_cellphone = ndb.StructuredProperty(PhoneNum, repeated=False)   
    customer_email = ndb.StringProperty(required=True) 


class Contract(ndb.Model):

    contract_number = ndb.StringProperty(required=True, indexed=True)
    date_start = ndb.DateProperty(required=True)
    date_end = ndb.DateProperty(required=True)
    branchname = ndb.StringProperty(required=True)  
    methodofpayment = ndb.StringProperty(required=False) 
     
    customer = ndb.StructuredProperty(Customer)  # Todo - Save Customer as seperate list
    
    letters = ndb.StringProperty(required=False)    
    comments = ndb.StringProperty(required=False)    
    date_rear = ndb.DateProperty(required=False)    
    rear_place = ndb.StringProperty(required=False)    
    gravenumber = ndb.StringProperty(required=False)   
    
    planfees_comment = ndb.StringProperty(required=False)
    planfees_price = ndb.FloatProperty(required=False)
    transport_comment = ndb.StringProperty(required=False)
    transport_price = ndb.FloatProperty(required=False)

    letter_count = ndb.IntegerProperty(required=False)
    letter_cost = ndb.FloatProperty(required=False)
    letter_price = ndb.FloatProperty(required=False)
     
    status = ndb.StringProperty(required=True, choices=('Active', 'Complete', 'Cancel'))  # new contract
    date_invoiced = ndb.DateProperty()
    invoice_number = ndb.StringProperty()
    
    # -- Auto Added
    audit = ndb.StructuredProperty(Audit)   
    

class ContractSundries(ndb.Model):
    # contract = ndb.ReferenceProperty(Contract, collection_name='cnsundries')
    contract = ndb.StructuredProperty(Contract)
    sundries_comment = ndb.StringProperty(required=False)
    sundries_price = ndb.FloatProperty(required=False)
           
    # -- Auto Added
    audit = ndb.StructuredProperty(Audit)       


class ContractItem(ndb.Model):
    # contract = ndb.ReferenceProperty(Contract, collection_name='cnitems')
    contract = ndb.StructuredProperty(Contract)
    item = ndb.StringProperty(required=False)        
    description = ndb.StringProperty(required=False)        
    code = ndb.StringProperty()        
    quantity = ndb.IntegerProperty()    # ??? Just create Duplicate Items
    price = ndb.FloatProperty()    
    price_cat = ndb.StringProperty()    # Price Category
    comments = ndb.StringProperty()        

    # -- Auto Added
    audit = ndb.StructuredProperty(Audit)      


class ContractPayment(ndb.Model):
    # contract = ndb.ReferenceProperty(Contract, collection_name='payments')
    contract = ndb.StructuredProperty(Contract)
    amount = ndb.FloatProperty()
    comments = ndb.StringProperty()    
    receipt = ndb.IntegerProperty()    
    date_received = ndb.DateProperty(auto_now_add=False)
    
    # -- Auto Added
    audit = ndb.StructuredProperty(Audit)   


class Item(ndb.Model):
    item = ndb.StringProperty(required=True)  
    itemcat = ndb.StringProperty()  # E Vir Enkel
    itemno = ndb.IntegerProperty()  # Numeriese nommer 1 vir E1
    description = ndb.StringProperty()
    code = ndb.StringProperty()    
    comment = ndb.StringProperty()
    remarks = ndb.StringProperty()
    price1 = ndb.FloatProperty()
    price2 = ndb.FloatProperty()
    price3 = ndb.FloatProperty()
    price4 = ndb.FloatProperty()
    price5 = ndb.FloatProperty()
    price6 = ndb.FloatProperty()
    price7 = ndb.FloatProperty()
    price8 = ndb.FloatProperty()
    price9 = ndb.FloatProperty()
    defcat = ndb.StringProperty()    
    bper = ndb.DateTimeProperty()
    eper = ndb.DateTimeProperty()
    
    # -- Auto Added
    audit = ndb.StructuredProperty(Audit)   


class PriceCat(ndb.Model):
    catcode = ndb.StringProperty(required=False)        
    catdesc = ndb.StringProperty(required=False) 
    catprice = ndb.IntegerProperty()
    
    # -- Auto Added
    audit = ndb.StructuredProperty(Audit)


class Branch(ndb.Model):
    # branchname = ndb.StringProperty(name="key")
    branchname = ndb.StringProperty(required=False)        
    description = ndb.StringProperty(required=False)
    
    # -- Auto Added
    audit = ndb.StructuredProperty(Audit)

    
class MethodOfPayment(ndb.Model):
    mop = ndb.StringProperty(required=False)   
         
    # -- Auto Added
    audit = ndb.StructuredProperty(Audit)


class UserPriv(ndb.Model):
    user_name = ndb.StringProperty(required=True, indexed=True)
    user_branch = ndb.StringProperty(required=True)        
    user_rights = ndb.IntegerProperty(required=True)
    
    # -- Auto Added
    audit = ndb.StructuredProperty(Audit)

    
class Housekeeping(ndb.Model):     
    hktype = ndb.StringProperty(required=True, choices=('MAIN', 'DEF'))
    lettercost = ndb.FloatProperty(required=False)
    mainheading = ndb.StringProperty(required=False)   
    company_name = ndb.StringProperty(required=False)   
    company_regno = ndb.StringProperty(required=False)   
    company_vatno = ndb.StringProperty(required=False)  
    contract_period = ndb.IntegerProperty()  # Number of days
    
    # -- Auto Added
    audit = ndb.StructuredProperty(Audit)


# --------------------------------
# Create global contract variable
# contracts_query = Contract.all()
# contract = contracts_query.fetch(1)
# branch = Branch(branchname="NewBranch", author=users.get_current_user())
# branch = Branch()

# textout = 'txt'


class MainPage(webapp2.RequestHandler):

    # @login_required
    # @users.login_required
    def get(self):
        # users.create_login_url("foo")
           
        url, url_linktext = get_url()
                
        mjk = UserPriv.query(UserPriv.user_name == 'marjo@memart.co.za').get()
        # import pdb; pdb.set_trace();
        if mjk is None: 
            usersmnew = UserPriv()
            if users.get_current_user():
                usersmnew.author = users.get_current_user()
                
            usersmnew.user_name = 'marjo@memart.co.za'
            usersmnew.user_branch = ''
            usersmnew.user_rights = int('5')
            usersmnew.put()
                                                  
        # logging.info('User Logged on is: ' + users.nickname())  # Todo - Fix this
        # Verify if the user has MEMART rights and build the menu to display
        usermenu, userr = build_menu('laybuy')
        mainheading = get_heading()

        # verify again, user might not be present in User_priv table...
        if userr is None:   
            url = users.create_login_url(self.request.uri)
            # url_linktext = 'Login'
            template_values = {'url': url,
                               'mainheading': mainheading,                               
                               'url_linktext': url_linktext}
            path = os.path.join(os.path.dirname(__file__), 'usernopriv.html')
            self.response.write(template.render(path, template_values))  
        else:
            mainheading = get_heading()                     
                                           
            template_values = {'url': url,
                               'url_linktext': url_linktext,
                               'mainheading': mainheading,
                               'userr': userr,
                               'usermenu': usermenu}

            # path = os.path.join(os.path.dirname(__file__), 'laybuy.html')
            # self.response.out.write(template.render(path, template_values))
            
            path = os.path.join(os.path.dirname(__file__), 'laybuy.html')
            self.response.out.write(template.render(path, template_values))    


class ContractSave(webapp2.RequestHandler):

    def post(self):
        cn = Contract(key_name=str(self.request.get('ckey')))

        cn.contract_number = self.request.get('ckey')
        cn.date_start = datetime.datetime.strptime(self.request.get('date_start'), '%d/%m/%Y').date() 
        cn.date_end = datetime.datetime.strptime(self.request.get('date_end'), '%d/%m/%Y').date() 
        cn.branchname = self.request.get('branchname')
        cn.methodofpayment = self.request.get('methodofpayment')
        # logging.info(self.request.get('customer_name'))
        cn.customer_name = self.request.get('customer_name')
        # logging.info('||' + str(cn.customer_name))
        cn.customer_code = self.request.get('customer_code')
        cn.customer_id = self.request.get('customer_id')        
        cn.customer_address = self.request.get('customer_address')
        cn.customer_cellphone = self.request.get('customer_cellphone')
        cn.customer_landline = self.request.get('customer_landline')
        cn.customer_email = self.request.get('customer_email')
        cn.letters = self.request.get('letters')
        cn.comments = self.request.get('comments')
        cn.rear_place = self.request.get('rearplace')
        cn.gravenumber = self.request.get('gravenumber')
        cn.date_rear = datetime.datetime.strptime(self.request.get('date_rear'), '%d/%m/%Y').date()
        
        cn.planfees_comment = self.request.get('planfeescomment')
        cn.planfees_price = float(self.request.get('planfeesprice'))
        cn.transport_comment = self.request.get('transportcomment')
        cn.transport_price = float(self.request.get('transportprice'))
        # cn.sundries_comment = self.request.get('sundriescomment')
        # cn.sundries_price = float(self.request.get('sundriesprice'))
        cn.letter_count = int(self.request.get('lettercount'))
        cn.letter_cost = float(self.request.get('lettercost'))
        cn.letter_price = float(self.request.get('letterprice'))
            
        cn.status = 'Active'
        cn.author = users.get_current_user()    
        try:    
            cn.put()
        except:
            logging.error("NEW Contract: Unable to add Contract" + self.request.get('ckey') + str(users.get_current_user()))            
        else:
            logging.info("NEW Contract added:" + self.request.get('ckey') + str(users.get_current_user()))
                    
            # Create iterative variables to hold multiple ITEMS/PAYMENTS
            citems = []
            cpayms = []
            csundries = []

            # Fetch Multiple Sundry Items from HTML POST
            all_sp = self.request.get_all('sundriesprice')
            all_sc = self.request.get_all('sundriescomment')

            i = 0
            while i < len(all_sp):
                if len(all_sp[i].strip()) > 0:
                    cns = ContractSundries(contract = cn)
                    cns.sundries_comment = all_sc[i]
                    cns.sundries_price = float(all_sp[i])
                    cns.author = users.get_current_user()

                    try:
                        cns.put()
                    except:
                        logging.error("NEW Contract, New Sundries: Unable to add Sundries ITEM" + str(all_sc[i]) + ' ' + str(all_sp[i]) + ' ' + str(users.get_current_user()))
                    else:
                        logging.info("NEW Contract, New Sundries:" + str(all_sc[i]) + ' ' + str(all_sp[i]) + ' ' + str(users.get_current_user()))
                        csundries.append(cns)
                i += 1

            # Fetch Multiple Items/Desc/Price from HTML POST
            all_i = self.request.get_all('item')
            all_d = self.request.get_all('itemdesc')
            all_pc = self.request.get_all('pricecat')
            all_p = self.request.get_all('price')
            all_c = self.request.get_all('comment')

            i = 0
            while i < len(all_i):
                # cni = Contract_item(contract = cn, key_name = str(self.request.get('ckey')) + str(i))
                if len(all_i[i].strip()) > 0:
                    cni = ContractItem(contract = cn)
                    cni.item = all_i[i]
                    cni.description = all_d[i]
                    cni.price_cat = all_pc[i]
                    cni.price = float(all_p[i])
                    cni.comments = all_c[i]
                    cni.author = users.get_current_user()

                    try:
                        cni.put()
                    except:
                        logging.error("NEW Contract, New Item: Unable to add ITEM" + str(all_i[i]) + ' ' + str(all_pc[i]) + ' ' + str(all_p[i]) + ' ' + str(all_c[i]) + ' ' + str(users.get_current_user()))
                    else:
                        logging.info("NEW Contract, New Item:" + str(all_i[i]) + ' ' + str(all_pc[i]) + ' ' + str(all_p[i]) + ' ' + str(all_c[i]) + ' ' + str(users.get_current_user()))
                        citems.append(cni)
                i += 1

            all_pm = self.request.get_all('payment')
            all_pmc = self.request.get_all('paycomment')
            all_pmd = self.request.get_all('paydatereceived')
            i = 0
            while i < len(all_pm):
                # cnp = Contract_payment(contract=cn, key_name=str(self.request.get('ckey')) + str(i))
                if len(all_pm[i].strip()) > 0:
                    cnp = ContractPayment(contract=cn)
                    cnp.amount = float(all_pm[i])
                    cnp.comments = all_pmc[i]
                    cnp.date_received = datetime.datetime.strptime(all_pmd[i], '%d/%m/%Y').date()
                    cnp.receipt = 999999
                    cnp.author = users.get_current_user()
                    try:
                        cnp.put()
                    except:
                        logging.error("NEW Contract, Unable to add new PAYM" + str(all_pm[i]) + ' ' + str(all_pmc[i]) + ' ' + str(all_pmd[i]) + ' ' + str(users.get_current_user()))
                    else:
                        logging.error("NEW Contract, new PAYM" + str(all_pm[i]) + ' ' + str(all_pmc[i]) + ' ' + str(all_pmd[i]) + ' ' + str(users.get_current_user()))
                        cpayms.append(cnp)
                i += 1

            self.redirect('/dispc')


class ContractChange(webapp2.RequestHandler):

    def post(self):
        contract_key = self.request.get('ckey')      
        cchange = self.request.get('contract_change')           
        if cchange == 'ContractChanged':
            logging.info("ContractChanged - Ok something changed...Key:" + contract_key)             
            # Fetch from datastore - want to make sure that we have the latest records
            contract = Contract.get_by_id(contract_key)
            
            c_sundries = ContractSundries.get_by_id(contract.key())
            # ndb.GqlQuery("SELECT * FROM Contract_sundries WHERE contract = :1", contract.key())
            c_items = ContractPayment.get_by_id(contract.Key())
            # ndb.GqlQuery("SELECT * FROM Contract_item WHERE contract = :1", contract.key())
            c_payms = ContractPayment.get_by_id(contract.key())
            # ndb.GqlQuery("SELECT * FROM Contract_payment where contract = :1", contract.key())
            
            # Fetch Multiple Sundry Items from HTML POST
            all_sp = self.request.get_all('sundriesprice')
            all_sc = self.request.get_all('sundriescomment')
            all_sk = self.request.get_all('sundrieskey')
            
            # Fetch Items from web first
            all_i = self.request.get_all('item')
            all_d = self.request.get_all('itemdesc')
            all_pc = self.request.get_all('pricecat')
            all_p = self.request.get_all('price')
            all_c = self.request.get_all('comment')
            all_ik = self.request.get_all('itemkey')
            
            all_pm = self.request.get_all('payment')
            all_pmc = self.request.get_all('paycomment')
            all_pmd = self.request.get_all('paydatereceived')
            all_pmk = self.request.get_all('paymkey')
                        
            # Verify if any Sundries item has been deleted. Delete if not found...
            for osi in c_sundries: 
                drop_item = 'Y'
                i = 0
                while i < len(all_sc):
                    if str(osi.key()).strip() == all_sk[i].strip():
                        drop_item = 'N'
                        break
                    i += 1  
                    
                if drop_item == 'Y':
                    try:
                        osi.delete()
                    except:
                        logging.error("Sundries ITEMS: Unable to DELETE Existing record:" + osi.sundries_comment + ' ' + str(osi.sundries_price) + ' ' + str(users.get_current_user()))
                    else:
                        logging.info("Sundries ITEMS: DELETE Existing record:" + osi.sundries_comment + ' ' + str(osi.sundries_price) + ' ' + str(users.get_current_user()))

            # Verify if any item has been deleted. Delete if not found...
            for oitem in c_items: 
                drop_item = 'Y'
                i = 0
                while i < len(all_i):
                    if str(oitem.key()).strip() == all_ik[i].strip():
                        drop_item = 'N'
                        break
                    i += 1  
                    
                if drop_item == 'Y':
                    try:
                        oitem.delete()
                    except:
                        logging.error("ITEMS: Unable to DELETE Existing record:" + oitem.item + ' ' + oitem.price_cat + ' ' + str(oitem.price) + ' ' + oitem.comments + ' ' + str(users.get_current_user()))
                    else:
                        logging.info("ITEMS: DELETE Existing record:" + oitem.item + ' ' + oitem.price_cat + ' ' + str(oitem.price) + ' ' + oitem.comments + ' ' + str(users.get_current_user()))

            # Verify if any PAYMENT has been deleted. Delete if not found...
            for opaym in c_payms: 
                drop_pm = 'Y'
                i = 0
                while i < len(all_pm):
                    if str(opaym.key()).strip() == all_pmk[i].strip():
                        drop_pm = 'N'
                        break
                    i += 1  
                if drop_pm == 'Y':
                    try:
                        opaym.delete()
                    except:
                        logging.error("PAYMENTS - Unable to DELETE Existing record:" + str(opaym.amount) + ' ' + opaym.comments + ' ' + str(opaym.date_received) + ' ' + str(users.get_current_user()))
                    else:
                        logging.info("PAYMENTS - DELETE Existing record:" + str(opaym.amount) + ' ' + opaym.comments + ' ' + str(opaym.date_received) + ' ' + str(users.get_current_user()))

            # We re-save all fields. Not checking which one changed...
            contract.contract_number = self.request.get('ckey')
            contract.date_start = datetime.datetime.strptime(self.request.get('date_start'), '%d/%m/%Y').date()
            contract.date_end = datetime.datetime.strptime(self.request.get('date_end'), '%d/%m/%Y').date()
            contract.branchname = self.request.get('branchname')
            contract.customer_name = self.request.get('customer_name')
            contract.customer_code = self.request.get('customer_code')
            contract.customer_id = self.request.get('customer_id')
            contract.customer_address = self.request.get('customer_address')
            contract.customer_cellphone = self.request.get('customer_cellphone')
            contract.customer_landline = self.request.get('customer_landline')
            contract.customer_email = self.request.get('customer_email')
            contract.letters = self.request.get('letters')
            contract.comments = self.request.get('comments')
            contract.date_rear = datetime.datetime.strptime(self.request.get('date_rear'), '%d/%m/%Y').date()            
            contract.rear_place = self.request.get('rearplace')
            contract.gravenumber = self.request.get('gravenumber')
            contract.status = self.request.get('status')
            
            contract.planfees_comment = self.request.get('planfeescomment')
            contract.planfees_price = float(self.request.get('planfeesprice'))
            contract.transport_comment = self.request.get('transportcomment')
            contract.transport_price = float(self.request.get('transportprice'))
            # contract.sundries_comment = self.request.get('sundriescomment')
            # contract.sundries_price = float(self.request.get('sundriesprice'))
            contract.letter_count = int(self.request.get('lettercount'))
            contract.letter_cost = float(self.request.get('lettercost'))
            contract.letter_price = float(self.request.get('letterprice'))
                    
            if users.get_current_user():
                contract.author = users.get_current_user()            
            
            # Update the current Contract
            try:
                contract.put()
            except:
                logging.error("Contract: Unable to UPDATE:" + str(contract.contract_number) + ' ' + str(users.get_current_user()))                                                                                        
            else:
                logging.info("Contract: UPDATED!:" + str(contract.contract_number) + ' ' + str(users.get_current_user()))                                                        
                                
            # Verify if any of the Sundries items changed. Fetch Sundries Items from web first
            i = 0
            while i < len(all_sc):
                # Only do this where the Sundries ITEM number is available
                if len(all_sc[i].strip()) > 0:
                    # For Existing Sundries ITEMS only
                    if len(all_sk[i].strip()) > 0:
                        # Find the Sundries item, then update it
                        for osi in c_sundries:                      
                            if str(osi.key()).strip() == all_sk[i].strip():
                                break
                         
                        # Just make sure the current osi is the record to be changed
                        if str(osi.key()).strip() == all_sk[i].strip():
                            if (str(osi.sundries_comment).strip() != str(all_sc[i]).strip()) or (str(osi.sundries_price).strip() != str(all_sp[i]).strip()):
                                logging.info("Sundries ITEMS: Change before:" + osi.sundries_comment + ' ' + str(osi.sundries_price) + ' ' + str(users.get_current_user()))                                                        
                                osi.sundries_comment = all_sc[i]
                                osi.sundries_price = float(all_sp[i])
                               
                                try:
                                    osi.put()
                                except:
                                    logging.error("Sundries ITEMS: Unable to update record:" + all_sc[i] + ' ' + all_sp[i] + str(users.get_current_user()))
                                else:
                                    logging.info("Sundries ITEMS: Change  after:" + all_sc[i] + ' ' + all_sp[i] + str(users.get_current_user()))
                        else:
                            logging.error("Sundries ITEMS - Unable to find record to update???:" + all_sc[i] + 'Key:' + all_sk[i].strip() + str(users.get_current_user()))
                    else:
                        # This is a new Sundries item, so add it
                        cnsund = ContractSundries(contract = contract)
                        cnsund.sundries_comment = all_sc[i]
                        cnsund.sundries_price = float(all_sp[i])
                        cnsund.author = users.get_current_user()
                        
                        try:
                            cnsund.put()
                        except:
                            logging.error("Sundries ITEMS: Unable to add NEW record:" + all_sc[i] + ' ' + all_sp[i].strip() + ' ' + str(users.get_current_user()))
                        else:    
                            logging.info("Sundries ITEMS: NEW record Added:" + all_sc[i] + ' ' + all_sp[i].strip() + ' ' + str(users.get_current_user()))

                i += 1

            # Verify if any of the items changed. Fetch Items from web first
            i = 0
            while i < len(all_i):
                # Only do this where the ITEM number is available
                if len(all_i[i].strip()) > 0:
                    # For Existing ITEMS only
                    if len(all_ik[i].strip()) > 0:
                        # Find the item, then update it
                        for oitem in c_items:                      
                            if str(oitem.key()).strip() == all_ik[i].strip():
                                break
                         
                        # Just make sure the current oitem is the record to be changed
                        if str(oitem.key()).strip() == all_ik[i].strip():
                            if (str(oitem.item).strip() != str(all_i[i]).strip()) or (str(oitem.description).strip() != str(all_d[i]).strip()) or (str(oitem.price_cat).strip() != str(all_pc[i]).strip()) or (str(oitem.price).strip() != str(all_p[i]).strip()) or (str(oitem.comments).strip() != str(all_c[i]).strip()):
                                logging.info("ITEMS: Change before:" + oitem.item + ' ' + oitem.description + ' ' + oitem.price_cat + ' ' + str(oitem.price) + ' ' + oitem.comments + all_ik[i] + ' ' + str(users.get_current_user()))
                                oitem.item = all_i[i]
                                oitem.description = all_d[i]
                                oitem.price_cat = all_pc[i]
                                oitem.price = float(all_p[i])
                                oitem.comments = all_c[i]
                                
                                try:
                                    oitem.put()
                                except:
                                    logging.error("ITEMS: Unable to update record:" + all_i[i] + ' ' + all_d[i] + ' ' + all_pc[i] + ' ' + all_p[i] + ' ' + all_c[i] + ' ' + all_ik[i] + str(users.get_current_user()))
                                else:
                                    logging.info("ITEMS: Change  after:" + all_i[i] + ' ' + all_d[i] + ' ' + all_pc[i] + ' ' + all_p[i] + ' ' + all_c[i] + ' ' + all_ik[i] + str(users.get_current_user()))
                        else:
                            logging.error("ITEMS - Unable to find record to update???:" + all_i[i] + 'Key:' + all_ik[i].strip() + str(users.get_current_user()))
                    else:
                        # This is a new item, so add it
                        # cni = Contract_item(contract = contract, key_name = str(self.request.get('ckey')) + str(i))
                        cni = ContractItem(contract = contract)
                        cni.item = all_i[i]
                        cni.description = all_d[i]
                        cni.price_cat = all_pc[i]
                        cni.price = float(all_p[i])
                        cni.comments = all_c[i]
                        cni.author = users.get_current_user()
                        
                        try:
                            cni.put()
                        except:
                            logging.error("ITEMS: Unable to add NEW record:" + all_i[i] + ' ' + all_d[i].strip() + ' ' + all_pc[i] + ' ' + all_p[i] + ' ' + all_c[i].strip() + ' ' + str(users.get_current_user()))
                        else:    
                            logging.info("ITEMS: NEW record Added:" + all_i[i] + ' ' + all_d[i].strip() + ' ' + all_pc[i] + ' ' + all_p[i] + ' ' + all_c[i].strip() + ' ' + str(users.get_current_user()))

                i += 1
                
            # Verify if any of the Payments changed
            i = 0
            while i < len(all_pm):
                if len(all_pm[i].strip()) > 0:
                    # Just verify if this is an existing record... remember we stored the key in the HTML...
                    if len(all_pmk[i].strip()) > 0:
                        # Find the item, then update it
                        for opaym in c_payms:
                            if str(opaym.key()).strip() == all_pmk[i].strip():
                                break
                 
                        # Just make sure the current Payment is the record to be changed
                        if str(opaym.key()).strip() == all_pmk[i].strip():
                            # Only update the record where some of the fields changed
                            if (str(opaym.amount).strip() != str(all_pm[i]).strip()) or (opaym.comments.strip() != all_pmc[i].strip()) or (opaym.date_received.strftime('%d/%m/%Y').strip() != str(all_pmd[i]).strip()):
                                logging.info("PAYM: Change before:" + str(opaym.amount) + ' ' + str(opaym.date_received) + ' ' + opaym.comments.strip() + ' Key:' + all_pmk[i].strip() + ' ' + str(users.get_current_user()))
                                opaym.amount = float(all_pm[i])
                                opaym.comments = all_pmc[i]
                                opaym.date_received = datetime.datetime.strptime(all_pmd[i], '%d/%m/%Y').date()
                                opaym.author = users.get_current_user()
                                
                                try:
                                    opaym.put()
                                except:
                                    logging.error("PAYM: Unable to update!:" + all_pm[i].strip() + ' ' + str(all_pmd[i]) + ' ' + all_pmc[i].strip() + ' Key:' + str(all_pmk[i]) + ' ' + str(users.get_current_user()))
                                else:  
                                    logging.info("PAYM: Change  after:" + all_pm[i].strip() + ' ' + str(all_pmd[i]) + ' ' + all_pmc[i].strip() + ' Key:' + str(all_pmk[i]) + ' ' + str(users.get_current_user()))
                        else:
                            logging.error("PAYM - Unable to find record to update???:" + all_pm[i] + ' ' + str(all_pmd[i]) + ' Key:' + all_pmk[i] + ' ' + str(users.get_current_user()))
                                
                    else:
                        # This is a new item, so add it
                        # cnp = Contract_payment(contract = contract, key_name = str(self.request.get('ckey')) + str(i))
                        cnp = ContractPayment(contract = contract)
                        cnp.amount = float(all_pm[i])
                        cnp.comments = all_pmc[i]
                        cnp.date_received = datetime.datetime.strptime(all_pmd[i], '%d/%m/%Y').date()
                        cnp.receipt = 999999
                        cnp.author = users.get_current_user()
                        
                        try:
                            cnp.put()
                        except:
                            logging.error("PAYM - Unable to Add new Record:" + all_pm[i] + ' ' + str(all_pmd[i]) + all_pmc[i] + ' ' + str(all_pmk[i]) + ' ' + str(users.get_current_user()))
                        else:
                            logging.info("PAYM - NEW record added:" + all_pm[i] + ' ' + str(all_pmd[i]) + all_pmc[i] + ' ' + str(all_pmk[i]) + ' ' + str(users.get_current_user()))
                i += 1     

        self.redirect('/dispc')


class ContractEdit(webapp2.RequestHandler):

    def get(self):
        
        url, url_linktext = get_url()
                    
#       Verify if the user has MEMART rights and build the menu to display            
        usermenu, userr = build_menu('contract_change')
        
        mainheading = get_heading()   
                
#       verify again, user might not be present in User_priv table...    
        if userr is None:            
            template_values = {'mainheading': mainheading}
            path = os.path.join(os.path.dirname(__file__), 'usernopriv.html')
            self.response.out.write(template.render(path, template_values))  
        else:
            contract_key = self.request.get('ckey')
            logging.info("contract_key__edit = " + contract_key)  # ToDo - Required?

            # Fetch the latest values
            contract, c_sundries, c_items, c_paym, ret_message = get_contract_detail(contract_key)
            
            if ret_message != 'NoMessage':  # Contract not found
                exit  # ToDo ? Not sure
                
            branches = Branch.query().fetch()
            if branches is None:
                logging.error("Unable to select any Branches. From Contractedit")

            items = Item.query().fetch()
            if items is None:
                logging.info("Unable to select Items. From Contractedit")
                    
            pricecats = PriceCat.query().Fetch()
            if pricecats is None:
                logging.error("Unable to select Price Cat. From Contractedit")
                        
            mop = MethodOfPayment.query().fetch()
            if mop is None:
                logging.error("Unable to select MOP. From Contractedit")       

            # ===================================================================
            # hk = memcache.get("hk" + str(users.get_current_user()))
            # ===================================================================
            hk = Housekeeping.get_by_id('MAIN')
            if hk is None:
                logging.error("Unable to select HouseKeeping. From Contractedit")                             
                # ===============================================================

            # mainheading = get_heading()
                                    
            template_values = {'url': url,
                               'url_linktext': url_linktext,
                               'mainheading': mainheading,
                               'userr': userr,
                               'usermenu': usermenu,
                               'contract': contract,
                               'c_sundries': c_sundries,
                               'c_items': c_items,
                               'c_paym': c_paym,
                               'branches': branches,
                               'pricecats': pricecats,
                               'items': items,
                               'mop': mop,
                               'hk': hk}

            path = os.path.join(os.path.dirname(__file__), 'contract_change.html')
            self.response.out.write(template.render(path, template_values))


class ContractDisplay(webapp2.RequestHandler):
    def get(self):
        
        url, url_linktext = get_url()
                    
        # Verify if the user has MEMART rights and build the menu to display
        usermenu, userr = build_menu('contract_display')
        
        mainheading = get_heading()   
        
        # verify again, user might not be present in User_priv table...
        if userr is None:            
            template_values = {'mainheading': mainheading}
            path = os.path.join(os.path.dirname(__file__), 'usernopriv.html')
            self.response.out.write(template.render(path, template_values))  
        else:        
            contract_key = self.request.get('ckey') 
            logging.info("contract_key_disp = " + contract_key)

            # mainheading = get_heading()
            
            # Fetch the latest values
            contract, c_sundries, c_items, c_paym, ret_message = get_contract_detail(contract_key)
            
            if ret_message != 'NoMessage':  # Contract not found
                heading = 'Contract search'                  
                template_values = {'url': url,
                                   'url_linktext': url_linktext,
                                   'mainheading': mainheading,                                   
                                   'message': ret_message,
                                   'userr': userr,
                                   'usermenu': usermenu,
                                   'heading': heading}                
                path = os.path.join(os.path.dirname(__file__), 'contract_invalid_key.html')
                self.response.out.write(template.render(path, template_values))
            else:    
                heading = 'Display Contract'                                           
                template_values = {'url': url,
                                   'url_linktext': url_linktext,
                                   'mainheading': mainheading,                                   
                                   'userr': userr,
                                   'usermenu': usermenu,
                                   'contract': contract, 
                                   'c_sundries': c_sundries,
                                   'c_items': c_items, 
                                   'c_paym': c_paym, 
                                   'heading': heading}

                path = os.path.join(os.path.dirname(__file__), 'contract_display.html')
                self.response.out.write(template.render(path, template_values))


class ContractNew(webapp2.RequestHandler):

    def get(self):
        mainheading = get_heading()           
        url, url_linktext = get_url()

        logging.info("ContractNew")
#         logging.info("url_linktext", url_linktext)

        # Verify if the user has MEMART rights and build the menu to display
        usermenu, userr = build_menu('contract_new')
        
        # verify again, user might not be present in User_priv table...
        if userr is None:        
            logging.info("User is None")    
            template_values = {'mainheading': mainheading}
            path = os.path.join(os.path.dirname(__file__), 'usernopriv.html')
            self.response.out.write(template.render(path, template_values))  
        else:
            logging.info("User Ok")
            if userr.user_branch == '':
                branches = Branch.query().fetch()
            else:
                branches = Branch.query(Branch.branchname == userr.user_branch)          
                
            items = Item.query().fetch()  # Fetch all Items - Memcache?
    
                # pricecats = memcache.get("pricecats" + str(users.get_current_user()))
                # if pricecats is None:
                # pricecat_query = Price_cat.query().fetch()
                # pricecats = pricecat_query.order('catprice')
                # pricecats = pricecat_query.fetch(100)
    
            pricecats = PriceCat.query().fetch()
            mop = MethodOfPayment.query().fetch()
            
            
            hk = Housekeeping.query(Housekeeping.hktype == 'MAIN').fetch()
            if hk is None:
                logging.info("HK is None") 
            else:
                logging.info('HK Extracted')
                
                for h1 in hk:
                    logging.info('HK Extracted:')
                
            for b in branches:
                logging.info('Branch:')
                
#             hk = Housekeeping.query(Housekeeping.hktype == 'MAIN').fetch()
#             hk = Housekeeping.get_by_id('MAIN')
                             
            logging.info("Template Next")           
            template_values = {'url': url,
                               'url_linktext': url_linktext,
                               'mainheading': mainheading,
                               'branches': branches,
                               'items': items,
                               'pricecats': pricecats,
                               'userr': userr,
                               'usermenu': usermenu,
                               'mop': mop,
                               'hk': hk}

            path = os.path.join(os.path.dirname(__file__), 'contract_new.html')
            self.response.out.write(template.render(path, template_values))


class ContractPaymentsAdd(webapp2.RequestHandler):

    def get(self):
        url, url_linktext = get_url()
                    
        # Verify if the user has MEMART rights and build the menu to display
        usermenu, userr = build_menu('add_payment')
        
        mainheading = get_heading()   
                
        # verify again, user might not be present in User_priv table...
        if userr is None:            
            template_values = {'mainheading': mainheading}
            path = os.path.join(os.path.dirname(__file__), 'usernopriv.html')
            self.response.out.write(template.render(path, template_values))  
        else:        
            contract_key = self.request.get('ckey') 
                
            # Fetch the latest values
            # ??? Process RET_MESSAGE...
            contract, c_sundries, c_items, c_paym, ret_message = get_contract_detail(contract_key)
            
            if ret_message != 'NoMessage':
                exit
                
            heading = 'Add Payment'         
            # mainheading = get_heading()
            template_values = {'url': url,
                               'url_linktext': url_linktext,
                               'mainheading': mainheading,                               
                               'userr': userr,
                               'usermenu': usermenu,
                               'contract': contract, 
                               'c_sundries': c_sundries,                               
                               'c_items': c_items, 
                               'c_paym': c_paym,
                               'heading': heading,                           
                               'f_paym': 'X',
                               'f_item': ''}
            path = os.path.join(os.path.dirname(__file__), 'contract_display.html')
            self.response.out.write(template.render(path, template_values))        


class ContractItemsAdd(webapp2.RequestHandler):

    def get(self):
        url, url_linktext = get_url()
                    
        # Verify if the user has MEMART rights and build the menu to display
        usermenu, userr = build_menu('add_item')
        
        mainheading = get_heading()   
                
        # verify again, user might not be present in User_priv table...
        if userr is None:            
            template_values = {'mainheading': mainheading}
            path = os.path.join(os.path.dirname(__file__), 'usernopriv.html')
            self.response.out.write(template.render(path, template_values))  
        else:         
            contract_key = self.request.get('ckey') 
            # Fetch the latest values
            #  ??? Process RET_MESSAGE...
            contract, c_sundries, c_items, c_paym, ret_message = get_contract_detail(contract_key)
            
            if ret_message != 'NoMessage':
                exit
                
            items = Item.query()
            pricecats = PriceCat.query()
            heading = 'Add Item'     
            # mainheading = get_heading()
            template_values = {'url': url,
                               'url_linktext': url_linktext,
                               'mainheading': mainheading,                               
                               'userr': userr,
                               'usermenu': usermenu,
                               'contract': contract, 
                               'c_sundries': c_sundries,                               
                               'c_items': c_items, 
                               'c_paym': c_paym,
                               'items': items, 
                               'pricecats': pricecats,
                               'heading': heading, 
                               'f_paym': '',
                               'f_item': 'X'}

            path = os.path.join(os.path.dirname(__file__), 'contract_display.html')
            self.response.out.write(template.render(path, template_values))    


class AdditionalItemSave(webapp2.RequestHandler):

    def post(self):
        contract_key = self.request.get('ckey')
        logging.info("ContractItemAdd - key=" + contract_key)
        contract = Contract.get_by_id(contract_key)             
           
        # Verify if any of the items changed
        all_i = self.request.get_all('itemAdd')
        all_d = self.request.get_all('itemdescAdd')
        all_pc = self.request.get_all('pricecatAdd')  # PriceCat
        all_p = self.request.get_all('priceAdd')
        all_c = self.request.get_all('commentAdd')

        i = 0
        while i < len(all_i):
            if len(all_i[i].strip()) > 0:
                # This is a new item, so add it
                # cni = Contract_item(contract = contract, key_name = str(self.request.get('ckey')) + str(i))
                cni = ContractItem(contract = contract)
                cni.item = all_i[i]
                cni.description = all_d[i]
                cni.price_cat = all_pc[i]
                cni.price = float(all_p[i])
                cni.comments = all_c[i]
                cni.author = users.get_current_user()
                try:
                    cni.put()
                except:
                    logging.error("ContractItemAdd: Unable to add new Item:" + str(all_i[i]) + ' ' + str(all_pc[i]) + ' ' + str(all_p[i]) + ' ' + str(all_c[i]) + ' ' + str(users.get_current_user()))
                else:       
                    logging.info("ContractItemAdd New Item added:" + str(all_i[i]) + ' ' + str(all_pc[i]) + ' ' + str(all_p[i]) + ' ' + str(all_c[i]) + ' ' + str(users.get_current_user()))
            i += 1
        
        self.redirect('/dispc') 


class AdditionalPaymSave(webapp2.RequestHandler):

    def post(self):
        contract_key = self.request.get('ckey')
        logging.info("ContractPAYMAdd - key=" + contract_key)           
        contract = Contract.get_by_id(contract_key)              
      
        # Verify if any of the Payments changed
        all_pm = self.request.get_all('paymentAdd')
        all_pmc = self.request.get_all('paycommentAdd')
        all_pmd = self.request.get_all('paydatereceivedAdd')

        i = 0
        while i < len(all_pm):
            # Just verify if any Paym have been captured
            if len(all_pm[i].strip()) > 0:
                # This is a new item, so add it
                # cnp = Contract_payment(contract = contract, key_name = str(contract_key) + str(i))
                cnp = ContractPayment(contract = contract)
                cnp.amount = float(all_pm[i])
                cnp.comments = all_pmc[i]
                cnp.date_received = datetime.datetime.strptime(all_pmd[i], '%d/%m/%Y').date()
                cnp.receipt = 999999
                cnp.author = users.get_current_user()
                try:
                    cnp.put()
                except:
                    logging.error("ContractPAYMAdd: UNABLE to add NEW payment:" + str(all_pm[i]) + ' ' + str(all_pmc[i]) + ' ' + str(all_pmd[i]) + ' ' + str(users.get_current_user()))
                else:
                    logging.info("ContractPAYMAdd: NEW payment:" + str(all_pm[i]) + ' ' + str(all_pmc[i]) + ' ' + str(all_pmd[i]) + ' ' + str(users.get_current_user()))
            i += 1     

        self.redirect('/dispc')                      


class BranchNew(webapp2.RequestHandler):

    def get(self):
        url, url_linktext = get_url()
        mainheading = get_heading()   
                    
        # Verify if the user has MEMART rights and build the menu to display
        usermenu, userr = build_menu('branch_new')
        
        # verify again, user might not be present in User_priv table...
        if userr is None:            
            template_values = {'mainheading': mainheading}
            path = os.path.join(os.path.dirname(__file__), 'usernopriv.html')
            self.response.out.write(template.render(path, template_values))  
        else:
            branches = Branch.query().fetch()
                       
            template_values = {'url': url,
                               'url_linktext': url_linktext, 
                               'mainheading': mainheading,                               
                               'branches': branches,                               
                               'userr': userr,
                               'usermenu': usermenu}
        
            path = os.path.join(os.path.dirname(__file__), 'branch_new.html')
            self.response.out.write(template.render(path, template_values))


class MOPnew(webapp2.RequestHandler):

    def get(self):
        url, url_linktext = get_url()
                    
        # Verify if the user has MEMART rights and build the menu to display
        usermenu, userr = build_menu('mop')
        
        mainheading = get_heading()   
                
        # verify again, user might not be present in User_priv table...
        if userr is None:            
            template_values = {'mainheading': mainheading}
            path = os.path.join(os.path.dirname(__file__), 'usernopriv.html')
            self.response.out.write(template.render(path, template_values))  
        else:
            mop = MethodOfPayment.query()

            # ===================================================================
            # print('laybuy_import ubit', mop)     
            # import pdb; pdb.set_trace();  
            # ===================================================================
                          
            template_values = {'url': url,
                               'url_linktext': url_linktext,
                               'mainheading': mainheading,
                               'userr': userr,
                               'mop': mop,
                               'usermenu': usermenu}
                        
            path = os.path.join(os.path.dirname(__file__), 'methodofpayment.html')
            self.response.out.write(template.render(path, template_values))     


class HousekeepingNew(webapp2.RequestHandler):

    def get(self):
        url, url_linktext = get_url()
                    
        # Verify if the user has MEMART rights and build the menu to display
        usermenu, userr = build_menu('housekeeping')
        
        mainheading = get_heading()     
        # verify again, user might not be present in User_priv table...
        if userr is None:            
            template_values = {'mainheading': mainheading}
            path = os.path.join(os.path.dirname(__file__), 'usernopriv.html')
            self.response.out.write(template.render(path, template_values))  
        else:
            hk = Housekeeping.query(Housekeeping.hktype == 'MAIN').get()
            
            template_values = {'url': url,
                               'url_linktext': url_linktext,
                               'mainheading': mainheading,
                               'userr': userr,
                               'usermenu': usermenu,
                               'hk': hk}
                        
            path = os.path.join(os.path.dirname(__file__), 'housekeeping.html')
            self.response.out.write(template.render(path, template_values))                       


class BranchSave(webapp2.RequestHandler):

    def post(self):
        br = Branch.query(Branch.branchname == str(self.request.get('branchname').strip())).get()
        
        if br is None:
            brnew = Branch()
            brnew.branchname = self.request.get('branchname')
            brnew.description = self.request.get('description')
        
            if users.get_current_user():
                brnew.author = users.get_current_user()
                
            try:
                brnew.put()
            except:
                logging.error("Branchsave: UNABLE to add NEW branch:" + str(self.request.get('branchname')) + ' ' + str(self.request.get('description')) + ' ' + str(users.get_current_user()))            
            else:
                logging.info("Branchsave: NEW branch:" + str(self.request.get('branchname')) + ' ' + str(self.request.get('description')) + ' ' + str(users.get_current_user()))            
   
        else:
            # br.branchname = self.request.get('branchname')
            br.description = self.request.get('description')
            if users.get_current_user():
                br.author = users.get_current_user()
            # br.date_changed = datetime.datetime.now()
            try:
                br.put()
            except:
                logging.error("Branchsave: UNABLE to Update branch:" + str(self.request.get('branchname')) + ' ' + str(self.request.get('description')) + ' ' + str(users.get_current_user()))            
            else:
                logging.info("Branchsave: Update branch:" + str(self.request.get('branchname')) + ' ' + str(self.request.get('description')) + ' ' + str(users.get_current_user()))            

        self.redirect('/newb')


class BranchDisplay(webapp2.RequestHandler):

    def get(self):
        mainheading = get_heading()           
        # textout = self.request.get('branch') # Not realy required
        branches = Branch.query().fetch()
        template_values = {'branch': branches,
                           'mainheading': mainheading}
        path = os.path.join(os.path.dirname(__file__), 'branch_display.html')
        self.response.out.write(template.render(path, template_values))


class PricecatNew(webapp2.RequestHandler):

    def get(self):
        mainheading = get_heading()          
        url, url_linktext = get_url()
                    
        # Verify if the user has MEMART rights and build the menu to display
        usermenu, userr = build_menu('pricecat_new')
        
        # verify again, user might not be present in User_priv table...
        if userr is None:            
            template_values = {'mainheading': mainheading}
            path = os.path.join(os.path.dirname(__file__), 'usernopriv.html')
            self.response.out.write(template.render(path, template_values))  
        else:       
            pricecats = PriceCat.query().fetch()
            template_values = {'url': url,
                               'url_linktext': url_linktext,
                               'mainheading': mainheading,                               
                               'pricecats': pricecats,
                               'userr': userr,
                               'usermenu': usermenu}
        
            path = os.path.join(os.path.dirname(__file__), 'pricecat_new.html')
            self.response.out.write(template.render(path, template_values))


class PricecatSave(webapp2.RequestHandler):

    def post(self):
        pc = PriceCat.query(PriceCat.catcode == str(self.request.get('catcode').strip())).get()

        if pc is None:
            pcnew = PriceCat()
            pcnew.catcode = self.request.get('catcode')
            pcnew.catdesc = self.request.get('catdesc')
            pcnew.catprice = int(self.request.get('catprice'))        
            # br.date_changed = datetime.datetime.now()
            if users.get_current_user():
                pcnew.author = users.get_current_user()
            
            try:
                pcnew.put()
            except:
                logging.error("Pricecatsave: UNABLE to add NEW record:" + str(self.request.get('catcode')) + ' ' + str(self.request.get('catdesc')) + ' ' + str(self.request.get('catprice')) + ' ' + str(users.get_current_user()))
            else:
                logging.info("Pricecatsave: NEW record:" + str(self.request.get('catcode')) + ' ' + str(self.request.get('catdesc')) + ' ' + str(self.request.get('catprice')) + ' ' + str(users.get_current_user()))                  

        else:
            pc.catdesc = self.request.get('catdesc')
            pc.catprice = int(self.request.get('catprice'))        
            # br.date_changed = datetime.datetime.now()
            if users.get_current_user():
                pc.author = users.get_current_user()
            
            try:
                pc.put()
            except:
                logging.error("Pricecatsave: UNABLE to update record:" + str(self.request.get('catcode')) + ' ' + str(self.request.get('catdesc')) + ' ' + str(self.request.get('catprice')) + ' ' + str(users.get_current_user()))
            else:
                logging.info("Pricecatsave: NEW record:" + str(self.request.get('catcode')) + ' ' + str(self.request.get('catdesc')) + ' ' + str(self.request.get('catprice')) + ' ' + str(users.get_current_user()))                  

        self.redirect('/newpc')
        

class PricecatDisplay(webapp2.RequestHandler):

    def get(self):
        # textout = self.request.get('catcode') # Not realy required
        mainheading = get_heading()   
        pc = PriceCat.query().fetch()
        template_values = {'pc': pc,
                           'mainheading': mainheading}
        path = os.path.join(os.path.dirname(__file__), 'pricecat_display.html')
        self.response.out.write(template.render(path, template_values))        


class ItemNew(webapp2.RequestHandler):

    def get(self):
        url, url_linktext = get_url()
                    
        # Verify if the user has MEMART rights and build the menu to display
        usermenu, userr = build_menu('Item_new')
        mainheading = get_heading()   
        # verify again, user might not be present in User_priv table...
        if userr is None:            
            template_values = {'mainheading': mainheading}
            path = os.path.join(os.path.dirname(__file__), 'usernopriv.html')
            self.response.out.write(template.render(path, template_values))  
        else:
            pricecats = PriceCat.query().fetch()
            if pricecats is None:
                logging.error("Unable to select Price Cat All - Itemnew")
                        
            items = Item.query().fetch()
            if items is None:
                logging.error("Unable to select Items All - Itemnew")
            
            # mainheading = get_heading()
            template_values = {'url': url,
                               'url_linktext': url_linktext, 
                               'mainheading': mainheading,                               
                               'userr': userr,
                               'items': items,
                               'usermenu': usermenu,
                               'pricecats': pricecats}
        
            path = os.path.join(os.path.dirname(__file__), 'item_new.html')
            self.response.out.write(template.render(path, template_values))


class ItemSave(webapp2.RequestHandler):

    def post(self):
                
        itemnew = Item.query(Item.item == str(self.request.get('item').strip())).get()
        
        if itemnew is None:
            itemnew = Item()
            if users.get_current_user():
                itemnew.author = users.get_current_user()

            itemnew.item = str(self.request.get('item'))
            itemnew.itemcat = self.request.get('itemcat')
            itemnew.itemno = int(self.request.get('itemno'))
            itemnew.description = self.request.get('description')
            itemnew.code = self.request.get('code')
            itemnew.defcat = self.request.get('pricecat')       
            itemnew.comment = self.request.get('comment')
            itemnew.price1 = float(self.request.get('p1'))   
            itemnew.price2 = float(self.request.get('p2'))
            itemnew.price3 = float(self.request.get('p3'))
            itemnew.price4 = float(self.request.get('p4'))
            itemnew.price5 = float(self.request.get('p5'))
            # itemnew.price6 = float(self.request.get('p6'))
            # itemnew.price7 = float(self.request.get('p7'))
            # itemnew.price8 = float(self.request.get('p8'))
            # itemnew.price9 = float(self.request.get('p9'))
            # itemnew.date_changed = datetime.datetime.now()
            try:
                itemnew.put()
            except:
                logging.error("Itemsave: UNABLE to add NEW record:" + str(self.request.get('item')) + ' ' + str(self.request.get('description')) + ' ' + str(self.request.get('code')) + ' ' + str(self.request.get('pricecat')) + ' ' + str(self.request.get('comment')) + ' ' + str(self.request.get('p1')) + ' ' + str(self.request.get('p2')) + ' ' + str(self.request.get('p3')) + ' ' + str(self.request.get('p4')) + ' ' + str(self.request.get('p5')) + ' ' + str(self.request.get('p6')) + ' ' + str(self.request.get('p7')) + ' ' + str(self.request.get('p8')) + ' ' + str(self.request.get('p9')) + ' ' + str(users.get_current_user()))
            else:
                logging.info("Itemsave: NEW record:" + str(self.request.get('item')) + ' ' + str(self.request.get('description')) + ' ' + str(self.request.get('code')) + ' ' + str(self.request.get('pricecat')) + ' ' + str(self.request.get('comment')) + ' ' + str(self.request.get('p1')) + ' ' + str(self.request.get('p2')) + ' ' + str(self.request.get('p3')) + ' ' + str(self.request.get('p4')) + ' ' + str(self.request.get('p5')) + ' ' + str(self.request.get('p6')) + ' ' + str(self.request.get('p7')) + ' ' + str(self.request.get('p8')) + ' ' + str(self.request.get('p9')) + ' ' + str(users.get_current_user()))            
                    
            self.redirect('/newi')
            
        else:
            if users.get_current_user():
                itemnew.author = users.get_current_user()

            # itemnew.item = str(self.request.get('item'))
            itemnew.itemcat = self.request.get('itemcat')
            itemnew.itemno = int(self.request.get('itemno'))
            itemnew.description = self.request.get('description')
            itemnew.code = self.request.get('code')
            itemnew.defcat = self.request.get('pricecat')       
            itemnew.comment = self.request.get('comment')
            itemnew.price1 = float(self.request.get('p1'))   
            itemnew.price2 = float(self.request.get('p2'))
            itemnew.price3 = float(self.request.get('p3'))
            itemnew.price4 = float(self.request.get('p4'))
            itemnew.price5 = float(self.request.get('p5'))
            # itemnew.price6 = float(self.request.get('p6'))
            # itemnew.price7 = float(self.request.get('p7'))
            # itemnew.price8 = float(self.request.get('p8'))
            # itemnew.price9 = float(self.request.get('p9'))
            # itemnew.date_changed = datetime.datetime.now()
            
            try:
                itemnew.put()
            except:
                logging.error("Itemsave: UNABLE to update NEW record:" + str(self.request.get('item')) + ' ' + str(self.request.get('description')) + ' ' + str(self.request.get('code')) + ' ' + str(self.request.get('pricecat')) + ' ' + str(self.request.get('comment')) + ' ' + str(self.request.get('p1')) + ' ' + str(self.request.get('p2')) + ' ' + str(self.request.get('p3')) + ' ' + str(self.request.get('p4')) + ' ' + str(self.request.get('p5')) + ' ' + str(self.request.get('p6')) + ' ' + str(self.request.get('p7')) + ' ' + str(self.request.get('p8')) + ' ' + str(self.request.get('p9')) + ' ' + str(users.get_current_user()))
            else:
                logging.info("Itemsave: Update record:" + str(self.request.get('item')) + ' ' + str(self.request.get('description')) + ' ' + str(self.request.get('code')) + ' ' + str(self.request.get('pricecat')) + ' ' + str(self.request.get('comment')) + ' ' + str(self.request.get('p1')) + ' ' + str(self.request.get('p2')) + ' ' + str(self.request.get('p3')) + ' ' + str(self.request.get('p4')) + ' ' + str(self.request.get('p5')) + ' ' + str(self.request.get('p6')) + ' ' + str(self.request.get('p7')) + ' ' + str(self.request.get('p8')) + ' ' + str(self.request.get('p9')) + ' ' + str(users.get_current_user()))            
                    
        self.redirect('/newi')


class ItemDisplay(webapp2.RequestHandler):

    def get(self):
        # textout = self.request.get('item') #todo: No BRANCH when called from new?
        mainheading = get_heading()  
        item = Item.query().fetch()
        template_values = {'item': item,
                           'mainheading': mainheading}

        path = os.path.join(os.path.dirname(__file__), 'item_display.html')
        self.response.out.write(template.render(path, template_values))


class UserManage(webapp2.RequestHandler):

    def get(self):
        url, url_linktext = get_url()
                    
        # Verify if the user has MEMART rights and build the menu to display
        usermenu, userr = build_menu('usermanage')
        mainheading = get_heading()   
                
        # verify again, user might not be present in User_priv table...
        if userr is None:            
            template_values = {'mainheading': mainheading}
            path = os.path.join(os.path.dirname(__file__), 'usernopriv.html')
            self.response.out.write(template.render(path, template_values))  
        else:        
            branches = Branch.query().fetch()
            if branches is None:
                logging.error("Unable to select Branches - Usermanage")

            usersm = UserPriv.query().fetch()
            if usersm is None:
                logging.error("Unable to select User_Priv - Usermanage")
                    
            # In the future we get the different rights available...???
            # for uu in usersm:
            # logging.info("Usermanage" + str(uu.user_name) + str(uu.user_branch) + str(uu.user_rights))
                       
            # mainheading = get_heading()
            template_values = {'url': url,
                               'url_linktext': url_linktext,
                               'mainheading': mainheading,
                               'userr': userr,
                               'usermenu': usermenu,
                               'branches': branches,
                               'usersm': usersm}
        
            path = os.path.join(os.path.dirname(__file__), 'usermanage.html')
            self.response.out.write(template.render(path, template_values))     


class UserManageSave(webapp2.RequestHandler):

    def post(self):
        up = UserPriv.query(UserPriv.user_name == str(self.request.get('user_name')).strip()).get()
        if up is None:      
            usersmnew = UserPriv()
            if users.get_current_user():
                usersmnew.author = users.get_current_user()
    
            usersmnew.user_name = str(self.request.get('user_name')).strip()
            usersmnew.user_branch = self.request.get('user_branch')
            usersmnew.user_rights = int(self.request.get('user_rights'))
                                                                       
            # itemnew.date_changed = datetime.datetime.now()
            try:
                usersmnew.put()
            except:
                logging.error("UsermanageSave: UNABLE to add NEW record:" + str(self.request.get('user_name')) + ' ' + str(self.request.get('user_branch')) + ' ' + str(self.request.get('user_rights')) + ' ' + str(users.get_current_user()))
            else:
                logging.info("UsermanageSave: NEW record:" + str(self.request.get('user_name')) + ' ' + str(self.request.get('user_branch')) + ' ' + str(self.request.get('user_rights')) + ' ' + str(users.get_current_user()))            
        else:
            # up.user_name = self.request.get('user_name')
            up.user_branch = self.request.get('user_branch')
            up.user_rights = int(self.request.get('user_rights'))
            up.author = users.get_current_user()            

            try:
                up.put()
            except:
                logging.error("UsermanageSave: UNABLE to update record:" + str(self.request.get('user_name')) + ' ' + str(self.request.get('user_branch')) + ' ' + str(self.request.get('user_rights')) + ' ' + str(users.get_current_user()))
            else:
                logging.info("UsermanageSave: Update record:" + str(self.request.get('user_name')) + ' ' + str(self.request.get('user_branch')) + ' ' + str(self.request.get('user_rights')) + ' ' + str(users.get_current_user())) 
                                    
        self.redirect('/newu')           


class MOPsave(webapp2.RequestHandler):

    def post(self):
        mop = MethodOfPayment.query(MethodOfPayment.mop == self.request.get('mopnew')).get()
        
        # =======================================================================
        # print('laybuy_import', mop)
        # import pdb; pdb.set_trace();
        # =======================================================================
        
        if mop is None:
            mopnew = MethodOfPayment()
            mopnew.mop = self.request.get('mopnew')
            if users.get_current_user():
                mopnew.author = users.get_current_user()
                
            # Todo - Audit...
                                                     
            # itemnew.date_changed = datetime.datetime.now()
            try:
                mopnew.put()
            except:
                    logging.error("mopnew: UNABLE to add NEW record:" + str(self.request.get('mopnew')))
            else:
                    logging.info("mopnew: NEW record:" + str(self.request.get('mopnew')) + ' ' + str(users.get_current_user()))            
                            
        else:
            logging.warning("mopnew: ADD record (Exist already):" + str(self.request.get('mopnew')) + ' ' + str(users.get_current_user()))            
        
        self.redirect('/newmop')      


class HousekeepingSave(webapp2.RequestHandler):

    def post(self):
        hk = Housekeeping.query(Housekeeping.hktype == 'MAIN').get()
        # =======================================================================
        # print('laybuy_import HK', hkl)     
        # import pdb; pdb.set_trace();  
        # =======================================================================
            
        if hk is None:
            hknew = Housekeeping()
            hknew.hktype = 'MAIN'
            hknew.mainheading = self.request.get('hkmainheading')
            hknew.company_name = self.request.get('hkcompany_name')
            hknew.company_regno = self.request.get('hkcompany_regno')
            hknew.company_vatno = self.request.get('hkcompany_vatno')
            hknew.lettercost = float(self.request.get('hklettercost'))            
            hknew.contract_period = int(self.request.get('hkContractPeriod'))                
            # Todo - Audit...
                        
            if users.get_current_user():
                hknew.author = users.get_current_user()        
                                                                       
            # itemnew.date_changed = datetime.datetime.now()
            try:
                hknew.put()
            except:
                logging.error("hknew: UNABLE to add NEW record:" + str(self.request.get('hklettercost')))
            else:
                logging.info("hknew: NEW record:" + str(self.request.get('hklettercost')) + ' ' + str(users.get_current_user()))            

        else:
            hk.mainheading = self.request.get('hkmainheading')
            hk.company_name = self.request.get('hkcompany_name')
            hk.company_regno = self.request.get('hkcompany_regno')
            hk.company_vatno = self.request.get('hkcompany_vatno')            
            hk.lettercost = float(self.request.get('hklettercost'))
            hk.contract_period = int(self.request.get('hkContractPeriod'))               
            hk.author = users.get_current_user()        
            # Todo - Audit...
                                                              
            # itemnew.date_changed = datetime.datetime.now()
            try:
                hk.put()
            except:
                logging.error("hk: UNABLE to Update record:" + str(self.request.get('hklettercost')))
            else:
                logging.info("hk: UPDATE record:" + str(self.request.get('hklettercost')) + ' ' + str(users.get_current_user()))
                                            
        self.redirect('/newhk')         


def get_contract_detail(contract_no):

    ret_message = "NoMessage"
    
    contract = Contract.query(Contract.contract_number == contract_no)
            
    if contract is None:
        ret_message = "Unable to retrieve Contract from datastore"
        logging.warning("Unable to retrieve Contract from datastore: " + contract_no)                 
        return ret_message  # ToDo - I that correct
    else:
        logging.info("Retrieve Contract from datastore: " + contract_no)
                
        c_sundries = ContractSundries.query(ContractSundries.contract == contract_no)
        c_items = ContractItem.query(ContractItem.contract == contract_no)
        c_payms = ContractPayment.query(ContractPayment.contract == contract_no)
                
    if c_sundries is None:
        # Create Empty Sundries item
        cns = ContractSundries()
        cns.sundries_comment = ""
        cns.sundries_price = ""
        cns.author = ""
        c_sundries.append(cns) 

    if c_items is None:     
        # Create Empty item
        cni = ContractItem()
        cni.item = ""
        cni.description = ""
        cni.price = ""
        cni.author = ""
        c_items.append(cni) 
        
    if c_payms is None:    
        cnp = ContractPayment()
        cnp.amount = ""
        cnp.comments = ""
        cnp.receipt = ""
        cnp.author = ""
        c_payms.append(cnp)

    # Return the calculated values...
    return contract, c_sundries, c_items, c_payms, ret_message


def build_menu(page_name):

    li = []
    userrdummy = None
    userr = None

    # logging.info("---1123 " + " " + str(users.get_current_user()))

    if str(users.get_current_user()).strip() == "marjo":
        # logging.info("---1124 " + " " + str(users.get_current_user()))
        userr = UserPriv(key_name="marjo")
        
        userr.author = users.get_current_user()
        userr.user_name = str(users.get_current_user()).strip()
        userr.user_branch = ''
        userr.user_rights = 5   

    # userr = memcache.get("userr" + str(users.get_current_user()))
    if userr is None:
        # Fetch ALL the Users
        usersm = UserPriv.query()
            
        # Fetch the current users record
        for ur in usersm:
            if ur.user_name.strip() == str(users.get_current_user()).strip():
                logging.info("MainPage: userr " + str(ur.user_name) + " " + str(users.get_current_user()))                
                userr = ur
                # Store current user rigts in Memcache
                # ===============================================================
                # if not memcache.set("userr" + str(users.get_current_user()), userr):
                #     if not memcache.add("userr" + str(users.get_current_user()), userr):
                #         logging.error("Memcache User_Priv add failed - for: " + str(users.get_current_user())) 
                # ===============================================================
                break

    if userr is None:
        logging.error("MainPage: userr None, user not in User_priv")         
        # user not current, return empty strings...
        return li, userrdummy       
    else:                    
        # Ok User is current, now build the page menu
        if page_name == 'laybuy':
            if int(userr.user_rights) > 1:            
                li.append({'href': '/newc', 'htext': 'Add new Contract'})
                
            if int(userr.user_rights) > 4:                 
                li.append({'href': '/newi', 'htext': 'Add new Item'})
                li.append({'href': '/newpc', 'htext': 'Price Category'})
                li.append({'href': '/newb', 'htext': 'Add new Branch'})
                li.append({'href': '/newu', 'htext': 'User Rights'})
                li.append({'href': '/newmop', 'htext': 'Method of Payment'})
                li.append({'href': '/newhk', 'htext': 'Housekeeping'})
        
        if page_name == 'contract_new':
            if int(userr.user_rights) > 0:  # 1 and more...
                li.append({'href': '/', 'htext': 'Find Contract'})
              
        if page_name == 'branch_new':
            if int(userr.user_rights) > 0:  # 1 and more...
                li.append({'href': '/', 'htext': 'Find Contract'})
                            
            if int(userr.user_rights) > 1:                 
                li.append({'href': '/newc', 'htext': 'Add new Contract'})
                       
        if page_name == 'Item_new':
            if int(userr.user_rights) > 0:  # and more...
                li.append({'href': '/', 'htext': 'Find Contract'})
                            
            if int(userr.user_rights) > 1:
                li.append({'href': '/newc', 'htext': 'Add new Contract'})
                
        if page_name == 'pricecat_new':
            if int(userr.user_rights) > 0:  # 1 and more...
                li.append({'href': '/', 'htext': 'Find Contract'})
                            
            if int(userr.user_rights) > 1:
                li.append({'href': '/newc', 'htext': 'Add new Contract'})
                           
        if page_name == 'usermanage':
            if int(userr.user_rights) > 0:  # and more...
                li.append({'href': '/', 'htext': 'Find Contract'})
                            
            if int(userr.user_rights) > 1:
                li.append({'href': '/newc', 'htext': 'Add new Contract'})
                                          
        if page_name == 'contract_change':
            if int(userr.user_rights) > 0:  # 1 and more...
                li.append({'href': '/', 'htext': 'Find Contract'})
                            
            if int(userr.user_rights) > 1:
                li.append({'href': '/newc', 'htext': 'Add new Contract'})
                      
        if page_name == 'contract_display': 
            if int(userr.user_rights) > 0:  # and more...
                li.append({'href': '/', 'htext': 'Find Contract'})
                            
            if int(userr.user_rights) > 2:            
                li.append({'href': '/addcp', 'htext': 'Add Payments'})
                
            if int(userr.user_rights) > 3:            
                li.append({'href': '/addci', 'htext': 'Add Items'})
               
            if int(userr.user_rights) > 4:                 
                li.append({'href': '/editc', 'htext': 'Edit Contract'})
                
            if int(userr.user_rights) > 1:            
                li.append({'href': '/newc', 'htext': 'Add new Contract'})

            if int(userr.user_rights) > 0:  # 1 and more...
                li.append({'href': '/cp', 'htext': 'Print Contract'})
                            
        if page_name == 'add_payment':
            if int(userr.user_rights) > 0:  # 1 and more...
                li.append({'href': '/', 'htext': 'Find Contract'})
                            
            if int(userr.user_rights) > 1:
                li.append({'href': '/newc', 'htext': 'Add new Contract'})
                
        if page_name == 'add_item':
            if int(userr.user_rights) > 0:  # 1 and more...
                li.append({'href': '/', 'htext': 'Find Contract'})
                            
            if int(userr.user_rights) > 1:
                li.append({'href': '/newc', 'htext': 'Add new Contract'})

        if page_name == 'mop':
            if int(userr.user_rights) > 0:  # 1 and more...
                li.append({'href': '/', 'htext': 'Find Contract'})
                            
            if int(userr.user_rights) > 1:                 
                li.append({'href': '/newc', 'htext': 'Add new Contract'})
                   
        if page_name == 'housekeeping':
            if int(userr.user_rights) > 0:  # 1 and more...
                li.append({'href': '/', 'htext': 'Find Contract'})
                            
            if int(userr.user_rights) > 1:                 
                li.append({'href': '/newc', 'htext': 'Add new Contract'})

        #        if page_name == '???':
        #            if int(userr.user_rights) == 5:
        #                li.append({'href':'/cp', 'htext':'Contract Print'})
               
        #   Global return
    return li, userr


def get_heading():

    mainheading = 'Laybuy'     
    
    hk = Housekeeping.query(Housekeeping.hktype == 'MAIN').get()
         
    # hk = Housekeeping.get_by_id('MAIN')
    if hk is not None:
        mainheading = hk.mainheading         
        
    return mainheading 
# 
#     mainheading = 'Laybuy'          
#     hk = memcache.get("hk" + str(users.get_current_user()))
#     if hk is None:
#         hk = Housekeeping.get_by_id('MAIN')      
#         if hk is not None:
#             mainheading = hk.mainheading     
#     else:
#         mainheading = hk.mainheading   
#         
#     if not memcache.set("hk" + str(users.get_current_user()), hk):
#         if not memcache.add("hk" + str(users.get_current_user()), hk):
#             logging.error("Memcache HK add failed - get_heading")        
#         
#     return mainheading 
# ===============================================================================


def get_url():
    
    if users.get_current_user():
        url = users.create_logout_url('/')
        url_linktext = 'Logout'
    else:
        url = users.create_login_url('/')
        url_linktext = 'Login'      
        
    return url, url_linktext


class RPCHandler(webapp2.RequestHandler):
    """ Allows the functions defined in the RPCMethods class to be RPCed."""

    def __init__(self, request, response):
        webapp2.RequestHandler.__init__(self, request, response)
        self.methods = RPCMethods()

    def get(self):
        func = None

        action = self.request.get('action')
        if action:
            if action[0] == '_':
                self.error(403)  # access denied
                return
            else:
                func = getattr(self.methods, action, None)

        if not func:
            self.error(404)  # file not found
            return

        args = ()
        while True:
            key = 'arg%d' % len(args)
            val = self.request.get(key)
            if val:
                args += (json.loads(val),)
            else:
                break
        result = func(*args)
        self.response.out.write(json.dumps(result))


class RPCMethods:

    """ Defines the methods that can be RPCed.
    NOTE: Do not allow remote callers access to private/protected "_*" methods.
    """

    def ItemDesc(self, *args):
        # The JSON encoding may have encoded integers as strings.
        # Be sure to convert args to any mandatory type(s).
        items = Item.query()
        if items is None:
            logging.error("Unable to select Items - ItemDesc RPCMethods")   
                    
        pricecats = PriceCat.query()
        if pricecats is None:                    
            logging.error("Unable to select Pricecats - ItemDesc RPCMethods") 
                      
        for item in items:            
            if item.item == args[0]:                     
                pricecol = ''
                if item.defcat is not None:
                    pricecol = 'price1'  # Set the default
                    for pcat in pricecats: 
                        # logging.info(pcat.catcode)
                        if pcat.catcode == item.defcat:  # Find the Finish Code
                            pricecol = 'price' + str(pcat.catprice)
                            # exit
                
                return item.description, item.defcat, getattr(item, pricecol)
                # exit  # first record only
                                             
#        ints = [int(arg) for arg in args]
#        return sum(ints) + 2000

    def ItemPrice(self, *args):
        items = Item.query()
        if items is None:
            logging.error("Unable to select Items - ItemPrice RPCMethods")          
                
        pricecats = PriceCat.query()
        if pricecats is None:                    
            logging.error("Unable to select Pricecats - ItemPrice RPCMethods")
                    
        # logging.info("??? About to loop")
        for item in items:            
            if item.item == args[0]:  # Stop at selected item
                # logging.info("??? Ok Got the ITEM")
                logging.info(args[1])   
                pricecol = 'price1'  # Set the default
                for pcat in pricecats:            
                    if pcat.catcode == args[1]:  # Find the Finish Code
                        # logging.info("??? Ok Got the CATEGORY")
                        pricecol = 'price' + str(pcat.catprice)
                        # logging.info("Aboyt to RET")
                        # logging.info(getattr(item, pricecol))
                        return getattr(item, pricecol)

# class pdf_view(webapp2.RequestHandler):
#    def get(self):   
#        contract_key = self.request.get('ckey') 
#        logging.info("contract_key_print = " + contract_key)
#
#        #Fetch the latest values
#        contract, c_sundries, c_items, c_paym, ret_message = get_contract_detail(contract_key)
#        
#        if ret_message == 'NoMessage':  
#            logging.info(ret_message)                      
#            self.response.headers['Content-Type'] = 'application/pdf'
#            self.response.headers['Content-Disposition'] = 'filename=testpdf.pdf'
#            
#            # Our container for 'Flowable' objects
#            elements = []
#            
#            # A basic document for us to write to 'rl_hello_platypus.pdf'
#            doc = SimpleDocTemplate(self.response.out, 
#                                    pagesize=A4,
#                                    rightMargin=10*mm,
#                                    leftMargin=10*mm,
#                                    topMargin=5*mm,
#                                    bottomMargin=15*mm)
#            
#            elements.append(pdf_header())   
#            elements.append(pdf_header2())   
#            elements.append(pdf_branches())   
#            elements.append(pdf_customer(contract))   
#    
#            # Show the PDF Doc
#            doc.build(elements)
#        else:
#            logging.info(ret_message)
#            template_values = {'mainheading': mainheading}
#            path = os.path.join(os.path.dirname(__file__), 'usernopriv.html')
#            self.response.out.write(template.render(path, template_values))             
        
# def pdf_header():
#    I = Image('laybuy.jpg')
#    I.drawHeight = 35*mm*I.drawHeight / I.drawWidth
#    I.drawWidth = 45*mm
#
#    data= [[I, 'ORDER', ''],
#           ['', 'Memorial Art (PTY) LTD.', ''],
#           ['', 'Reg.No: 1983/013124/07'],
#           ['', 'Vat No: 4420110092']
#           ]
#    
#    t=Table(data,colWidths=(50*mm,110*mm, 40*mm),
#                 rowHeights=(10*mm),
#                 style=[('SPAN',(0,0),(0,1)),
#                        ('ALIGN',(0,0),(0,1),'LEFT'), 
#                        ('ALIGN',(1,0),(1, -1),'CENTER'), 
#                        ('VALIGN',(0,0),(0, 1),'TOP'), 
#                        ('VALIGN',(1,0),(1, 0),'TOP'), 
#                            ('BOTTOMPADDING',(1,0),(1, 0),6),
#                        ('FONTSIZE',(1,0),(1, 0),20), 
#                        ('FONTNAME',(1,0),(1, 0),'Times-Bold'), 
#                        ('VALIGN',(1,1),(1, -1),'TOP'),                             
#                        ('FONTSIZE',(1,1),(1, 1),26), 
#                        ('FONTNAME',(1,1),(1, 1),'Times-BoldItalic'), 
#                        ('TOPPADDING',(1,0),(1,0),0), 
#                        
#                        ('BOX', (0,0), (-1,-1),1,black),
#                        ('GRID', (0,0), (-1,-1),1,black),
#                        ])    
#    return t   
 
# def pdf_header2():
#    data= [['', 'Reg.No: 1983/013124/07 \n Vat No: 4420110092', ''],              
#           ['', '']
#           ]
#    
#    t=Table(data,colWidths=(50*mm,110*mm, 40*mm),
#                 rowHeights=(5*mm),
#                 style=[('ALIGN',(0,0),(-1,-1),'CENTER'),
#                        ('VALIGN',(0,0),(-1,-1),'BOTTOM'),                        
#                        ('FONTNAME',(0,0),(-1,-1),'Times-Bold'),                        
#                        ('FONTSIZE',(0,0),(-1,-1),5), 
#                        ('BOX', (0,0), (-1,-1),1,black),
#                        ('GRID', (0,0), (-1,-1),1,black),
#                        ])    
#    return t   

# def pdf_branches():

#    data= [['Factory & Head Ofice', '', 'Rustenburg', 'Zeerust', 'Mamelodi Crossing'],
#           ['91 van Belkum Str', 'Tel: (014) 596 7533', 'Cnr. Berg &', 'Cnr. Kerk & Cilliers Str.', 'Centre'],
#           ['P.O. Box 2890', 'Fax: (014) 596 7539', 'Oliver Tambo Dr.', 'Zeerust', 'Shop F8B Mamelodi'],
#           ['Rustenburg, 0300', 'Reg No: 1983/013124/07', 'Rustenburg, 0300', 'Tel (018) 642 2502', 'Tel: (012) 805 9818'],
#           ['', 'Vat. No: 4420110092', 'Tel: (014) 592 8111', '', ''],
#           ]
#    
#    t=Table(data,style=[ ('ALIGN',(0,0),(-1,-1),'LEFT'), 
#                         ('FONTNAME',(0,0),(4,0),'Courier-Bold'), 
#                         ('FONTNAME',(4,1),(4,1),'Courier-Bold'), 
#                         ('FONTSIZE',(1,3),(1,4),6),  
#                         ('VALIGN',(1,3),(1,3),'BOTTOM'), 
#                         ('VALIGN',(1,4),(1,4),'TOP'), 
#                         ('LINEBELOW',(0,4),(4,4),2,black), 
#                        ('ALIGN',(1,0),(1, -1),'CENTER'),
#                        ('VALIGN',(0,0),(0, 1),'TOP'),
#
#                            ('BOTTOMPADDING',(1,0),(1, 0),6),
# 
#                        ('FONTNAME',(1,0),(1, 0),'Times-Bold'),
#                        ('VALIGN',(1,1),(1, -1),'TOP'),
#                        ('FONTSIZE',(1,1),(1, 1),24),
#                        ('FONTNAME',(1,1),(1, 1),'Times-BoldItalic'),
#                        ('BOX', (0,0), (-1,-1),.5,black),
#                        ('GRID', (0,0), (-1,-1),.5,black),
#                        ])    
#    return t    

# def pdf_customer(lbc):
#    data= [['Customer:', lbc.customer_name, 'THIS AGREEMENT WILL \n BE VALID FOR 6 MONTHS \n ONLY AS FROM DATE', lbc.contract_number ],              
#           ['', '', 'Date:', lbc.date_start],               
#           ['Cellphone Number:', lbc.customer_cellphone, 'REPRESENTED BY:', lbc.author] ,              
#           ]
#    
#    t=Table(data,
#            colWidths=(50*mm,110*mm, 40*mm),
#                 rowHeights=(5*mm),
#                 style=[('ALIGN',(0,0),(-1,-1),'CENTER'),
#                        ('VALIGN',(0,0),(-1,-1),'BOTTOM'),                        
#                        ('FONTNAME',(0,0),(-1,-1),'Times-Bold'),                        
#                        ('FONTSIZE',(0,0),(-1,-1),5), 
#                       ('BOX', (0,0), (-1,-1),1,black),
#                       ('GRID', (0,0), (-1,-1),1,black),
#                        ])    
#    return t  


# def main():
application = webapp2.WSGIApplication([('/', MainPage),
                                       ('/addcp', ContractPaymentsAdd),
                                       ('/addci', ContractItemsAdd),
                                       ('/editc', ContractEdit),
                                       ('/newc', ContractNew),
                                       ('/newb', BranchNew),
                                       ('/newi', ItemNew),
                                       ('/newpc', PricecatNew),
                                       ('/newmop', MOPnew),           
                                       ('/newu', UserManage),
                                       ('/newhk', HousekeepingNew),
                                       ('/savee', ContractChange),
                                       ('/savec', ContractSave),
                                       ('/saveb', BranchSave),
                                       ('/savei', ItemSave),
                                       ('/savepc', PricecatSave),
                                       ('/saveai', AdditionalItemSave),
                                       ('/saveap', AdditionalPaymSave),
                                       ('/saveu', UserManageSave),
                                       ('/savemop', MOPsave),
                                       ('/savehk', HousekeepingSave),
                                       ('/dispc', ContractDisplay),
                                       ('/dispb', BranchDisplay),
                                       ('/dispi', ItemDisplay),
                                       ('/disppc', PricecatDisplay),
#                                      ('/cp', pdf_view),
                                       ('/rpc', RPCHandler)], 
                                      debug=True)
    
#    application.run()
#
# if __name__ == "__main__":
#    main()

# appcfg.py create_bulkloader_config --application=memartlbuy --url=http://memartlbuy.appspot.com/_ah/remote_api --filename=C:\Users\marjo\workspace\LayBuy\src\mal_bl.yaml
# appcfg.py download_data --application=memartlbuy --url=http://memartlbuy.appspot.com/_ah/remote_api --filename=C:\Users\marjo\workspace\LayBuy\src\memart_data
# appcfg.py download_data --application=memartlbuy --kind=Branch --url=http://memartlbuy.appspot.com/_ah/remote_api --filename=C:\Users\marjo\workspace\LayBuy\src\memart_data
# appcfg.py download_data --config_file=C:\Users\marjo\workspace\LayBuy\src\mal_bl.yaml --filename=C:\Users\marjo\workspace\LayBuy\src\branch.csv --kind=Branch --url=http://memartlbuy.appspot.com/_ah/remote_api
# appcfg.py upload_data --config_file=C:\Users\marjo\workspace\LayBuy\src\mal_bul_item.yaml --filename=C:\Users\marjo\workspace\LayBuy\src\Items_bulk_upload.csv --kind=Item --url=http://memartlbuy.appspot.com/_ah/remote_api
#      import_transform: transform.import_date_time('%Y-%m-%d') 
#      export_transform: transform.export_date_time('%Y-%m-%d') 