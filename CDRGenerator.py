__author__ = "Kübra Yıkılmaz"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "kubra.yikilmaz@turkcell.com.tr"
__status__ = "Production"
#pip install Faker
#pip install xlrd
#pip install networkx
#pip install scipy
from faker import Faker
fake = Faker()
import random
from random import randrange
import datetime 
from dateutil.relativedelta import *
import networkx as nx
import matplotlib.pyplot as plt

CustomerNumber=100
OperatorNumber = 3
max_call_number = 5

class Operator:
    def __init__(self,name,marketshare):
        self.name = name
        self.marketshare = marketshare
        self.customers = []
        
    def info(self):
        print(self.name)
        
def CreateOperator(OperatorNumber = OperatorNumber):
    operators = []
    last_marketshare = 0
    
    for i in range(OperatorNumber):
        if i==0:
            ms = random.randint(0,100)
            last_marketshare += ms
            o = Operator(fake.company(),(ms/100))
            operators.append(o)
        elif i==OperatorNumber-1:
            o = Operator(fake.company(),((100-last_marketshare)/100))
            operators.append(o)    
        
        else:
            ms = random.randint(0,(100-last_marketshare))
            o = Operator(fake.company(),(ms/100))
            operators.append(o)
            last_marketshare += ms
    return operators

class Customer:
    def __init__(self,customerid,msisdn):
        self.customerid = customerid
        self.msisdn = msisdn
        self.operator = ""
        self.contacts = []
        self.call_records = []
        
    def info(self):
        print(self.customerid+"\n"+self.msisdn)
       
    
def CreatCustomer(CustomerNumber = CustomerNumber):
    if CustomerNumber % 100 != 0:
        print("""Lütfen 100 ve katları olacak şekilde müşteri sayısı giriniz...""")
    else:
        customers = []
        for i in range(CustomerNumber):
            while True:
                msisdn = fake.msisdn()
                customerid = fake.isbn10(separator="")
                if int(msisdn[0])!=0 and int(customerid[0])!=0:
                    break
            #print(msisdn,customerid)
            c = Customer(customerid,msisdn)
            customers.append(c)
        return customers
    
operators = CreateOperator()
created_customers = CreatCustomer()
customers_4_operators = created_customers.copy()
for i in range(len(operators)):
    for j in range(int(operators[i].marketshare*100)):
        c = customers_4_operators.pop()
        c.operator = operators[i]
        operators[i].customers.append(c)
        
        
for c in created_customers:
    for i in range(random.randint(0,CustomerNumber)):
        possible_contact = random.choice(created_customers)
        if possible_contact not in c.contacts:
            c.contacts.append(possible_contact)
            
class CallRecord():
    def __init__(self,caller,called,timestamp,duration):
        self.CDRNo = "".join(fake.itin().split("-"))
        self.caller = caller
        self.called = called
        self.timestamp = timestamp
        self.duration = duration #Second
        
    def info(self):
        print(self.CDRNo)
        
        
def random_date():
    start = datetime.datetime(2013, 9, 20,13,0)
    start += datetime.timedelta(minutes=randrange(1000))
    start += datetime.timedelta(days=randrange(0,30))
    start += relativedelta(months=randrange(2,12))
    return start

CDR = []
for c in created_customers:
    for contact in c.contacts:
        for i in range(1,random.randint(1,max_call_number)):
            cdr = CallRecord(caller=c,called=contact,timestamp=random_date().strftime("%d-%m-%y %H:%M"),duration=random.randint(0,120*60))
            c.call_records.append(cdr)
            CDR.append(cdr)
            #print(c.msisdn,contact.msisdn,random_date().strftime("%d-%m-%y %H:%M"),random.randint(0,120*60))
            
            
            
network_dict = {}
for cdr in CDR:
    connection = cdr.caller.msisdn+"->"+cdr.called.msisdn
    if connection not in network_dict:
        network_dict[connection]=1
    else:
        network_dict[connection]+=1
        
G_weighted = nx.Graph()
for c in network_dict:
    G_weighted.add_edge(c.split("->")[0],c.split("->")[1], weight=network_dict[c])
    
print(nx.info(G_weighted))


pos = nx.spectral_layout(G_weighted)
betCent = nx.betweenness_centrality(G_weighted, normalized=True, endpoints=True)
node_color = [20000.0 * G_weighted.degree(v) for v in G_weighted]
node_size =  [v * 1000 for v in betCent.values()]
plt.figure(figsize=(20,20))
nx.draw_networkx(G_weighted, pos=pos, with_labels=False,
                 node_color=node_color,
                 node_size=node_size )