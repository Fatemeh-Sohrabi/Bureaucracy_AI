# ==========================================
# bill_agent.py
# Bureaucracy AI Bill Agent
# v1.1
# ==========================================


import re
from datetime import datetime


# ==========================================
# DETECT BILL
# ==========================================

def detect_bill(text):

    keywords = [

        "bill",
        "invoice",
        "electricity",
        "internet",
        "rent",
        "rechnung",
        "payment",
        "zahlung",
        "miete"

    ]


    text = text.lower()


    for word in keywords:

        if word in text:

            return True


    return False




# ==========================================
# EXTRACT BILL TYPE
# ==========================================

def extract_bill_type(text):


    text=text.lower()


    if "electricity" in text or "strom" in text:

        return "Electricity"


    if "internet" in text:

        return "Internet"


    if "rent" in text or "miete" in text:

        return "Rent"


    if "insurance" in text:

        return "Insurance"


    return "General Bill"




# ==========================================
# EXTRACT AMOUNT
# ==========================================

def extract_amount(text):


    patterns=[

        r"\d+[,.]?\d*\s?(€|eur)",

        r"(€|eur)\s?\d+[,.]?\d*",

        r"\b\d+[,.]\d{2}\b"

    ]


    for p in patterns:


        result=re.search(

            p,

            text.lower()

        )


        if result:

            return result.group()



    return None




# ==========================================
# EXTRACT CUSTOMER NUMBER
# ==========================================

def extract_customer_number(text):


    patterns=[

        r"customer number[:\s]+(\d+)",

        r"customer[:\s]+(\d+)",

        r"kundennummer[:\s]+(\d+)"

    ]


    for p in patterns:


        result=re.search(

            p,

            text.lower()

        )


        if result:

            return result.group(1)



    return None




# ==========================================
# EXTRACT DEADLINE
# ==========================================

def extract_deadline(text):


    patterns=[


        r"\d{1,2}\s[A-Z][a-z]+\s\d{4}",


        r"\d{1,2}\.\d{1,2}\.\d{4}"

    ]



    for p in patterns:


        result=re.search(

            p,

            text

        )


        if result:

            return result.group()



    return None




# ==========================================
# ANALYZE BILL
# ==========================================

def analyze_bill(text):


    if not detect_bill(text):

        return None



    bill={


        "type":

        extract_bill_type(text),



        "amount":

        extract_amount(text),



        "customer_number":

        extract_customer_number(text),



        "deadline":

        extract_deadline(text),



        "status":

        "UNPAID"


    }



    return bill




# ==========================================
# CREATE TASK CONTEXT
# ==========================================

def bill_to_task_context(bill):


    priority="Normal"


    if bill["deadline"]:

        priority="High"



    return {


        "email_id":0,


        "category":"Finance",


        "task":

        "Complete payment",


        "deadline":

        bill["deadline"],


        "priority":

        priority,


        "bill":

        bill

    }




# ==========================================
# TEST
# ==========================================

if __name__=="__main__":


    text="""

    Your electricity bill from Stadtwerke München
    is 85.50 €.

    Please pay before 20 August 2026.

    Customer number: 458921

    """



    result=analyze_bill(text)



    print(result)