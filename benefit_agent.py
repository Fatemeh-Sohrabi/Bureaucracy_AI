# ==========================================
# benefit_agent.py
# Bureaucracy AI Benefit Agent
# ==========================================


import re

from memory_engine import save_entity



# ==========================================
# BENEFIT KEYWORDS
# ==========================================

BENEFIT_KEYWORDS = {


    "Bürgergeld":[

        "bürgergeld",
        "jobcenter",
        "arbeitslosengeld"

    ],


    "Child Benefit":[

        "kindergeld",
        "child benefit",
        "familienkasse"

    ],


    "Housing Benefit":[

        "wohngeld",
        "housing benefit",
        "miete"

    ],


    "Social Support":[

        "social",
        "hilfe",
        "sozialamt"

    ]

}





# ==========================================
# DETECT BENEFIT TYPE
# ==========================================

def detect_benefit(text):


    text=text.lower()



    for benefit, keywords in BENEFIT_KEYWORDS.items():


        for word in keywords:


            if word in text:

                return benefit



    return None





# ==========================================
# EXTRACT AMOUNT
# ==========================================

def extract_amount(text):


    result=re.findall(

        r"\d+[,.]?\d*\s?€",

        text

    )


    return result






# ==========================================
# EXTRACT REFERENCE
# ==========================================

def extract_reference(text):


    return re.findall(

        r"[A-Z]{2,}-\d+",

        text

    )






# ==========================================
# DOCUMENT CHECKLIST
# ==========================================

def required_documents(benefit_type):


    documents={


        "Bürgergeld":[

            "Identity document",

            "Income proof",

            "Housing contract",

            "Bank information"

        ],



        "Child Benefit":[

            "Birth certificate",

            "Residence documents",

            "Bank details"

        ],



        "Housing Benefit":[

            "Rental contract",

            "Income proof",

            "Residence certificate"

        ],



        "Social Support":[

            "Identity document",

            "Financial documents"

        ]

    }



    return documents.get(

        benefit_type,

        [

        "Identity document",

        "Application documents"

        ]

    )






# ==========================================
# SAVE MEMORY
# ==========================================

def save_benefit_memory(data):


    save_entity(

        "benefit",

        data["type"],

        str(data),

        None

    )


    return True





# ==========================================
# BENEFIT WORKFLOW
# ==========================================

def analyze_benefit_request(document):


    benefit_type = detect_benefit(
        document
    )



    if benefit_type is None:


        return {

            "status":
            "Not a benefit request"

        }





    result={


        "agent":
        "Benefit Agent",


        "type":
        benefit_type,


        "amounts":
        extract_amount(document),


        "references":
        extract_reference(document),


        "required_documents":
        required_documents(
            benefit_type
        ),


        "next_steps":[


            "Check eligibility",

            "Collect documents",

            "Submit application",

            "Track response"

        ]

    }




    save_benefit_memory(
        result
    )



    return result






# ==========================================
# TEST
# ==========================================

if __name__=="__main__":


    text="""

    Jobcenter requests documents
    for Bürgergeld application.

    Amount 563 €.

    Reference BG-458921

    """



    print(
        analyze_benefit_request(text)
    )