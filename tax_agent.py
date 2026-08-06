# ==========================================
# tax_agent.py
# Bureaucracy AI German Tax Agent
# ==========================================


import re
from datetime import datetime


# ==========================================
# TAX KEYWORDS
# ==========================================

TAX_KEYWORDS = [

    "tax",
    "steuer",
    "steuererklärung",
    "finanzamt",
    "elster",
    "einkommensteuer",
    "income tax"

]



# ==========================================
# DETECT TAX REQUEST
# ==========================================

def detect_tax(text):

    text=text.lower()


    for word in TAX_KEYWORDS:

        if word in text:

            return True


    return False




# ==========================================
# EXTRACT TAX YEAR
# ==========================================

def extract_tax_year(text):


    years=re.findall(

        r"20\d{2}",

        text

    )


    if years:

        return years[0]


    return None





# ==========================================
# EXTRACT DEADLINE
# ==========================================

def extract_deadline(text):


    pattern = r"\d{1,2}\s[A-Z][a-z]+\s\d{4}"


    result=re.search(

        pattern,

        text

    )


    if result:

        return result.group()


    return None





# ==========================================
# EXTRACT AMOUNT
# ==========================================

def extract_amount(text):


    result=re.findall(

        r"\d+[,.]?\d*\s?€",

        text

    )


    if result:

        return result[0]


    return None





# ==========================================
# TAX ANALYSIS
# ==========================================

def analyze_tax(document):


    if not detect_tax(document):

        return None



    result={


        "agent":

        "Tax Agent",



        "category":

        "Tax",



        "tax_year":

        extract_tax_year(document),



        "deadline":

        extract_deadline(document),



        "amount":

        extract_amount(document),



        "task":

        "Prepare tax declaration",



        "priority":

        "High",



        "status":

        "REVIEW_REQUIRED"



    }


    return result





# ==========================================
# TAX WORKFLOW
# ==========================================

def tax_workflow(document):


    result=analyze_tax(document)



    if result is None:


        return {


            "agent":

            "Tax Agent",


            "status":

            "Not a tax document"

        }



    return result





# ==========================================
# TEST
# ==========================================

if __name__=="__main__":


    text="""

    Finanzamt München

    Please submit your Einkommensteuererklärung
    for 2025 before 30 September 2026.

    Tax amount: 450 €

    """


    print(
        tax_workflow(text)
    )