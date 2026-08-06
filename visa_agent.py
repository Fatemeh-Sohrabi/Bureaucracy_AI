# ==========================================
# visa_agent.py
# Bureaucracy AI Visa Agent
# ==========================================


import re

from memory_engine import save_entity



# ==========================================
# VISA KEYWORDS
# ==========================================

VISA_KEYWORDS = [

    "visa",
    "residence",
    "aufenthalt",
    "aufenthaltstitel",
    "immigration",
    "permit",
    "ausländerbehörde",
    "embassy",
    "consulate"

]





# ==========================================
# DETECT VISA REQUEST
# ==========================================

def detect_visa(text):


    text=text.lower()


    for word in VISA_KEYWORDS:

        if word in text:

            return True



    return False





# ==========================================
# DETECT VISA TYPE
# ==========================================

def detect_visa_type(text):


    text=text.lower()



    if "student" in text or "study" in text:

        return "Student Visa"



    if "family" in text or "spouse" in text:

        return "Family Reunion Visa"



    if "work" in text or "employment" in text:

        return "Work Visa"



    if "residence" in text or "aufenthalt" in text:

        return "Residence Permit"



    return "General Immigration Request"






# ==========================================
# EXTRACT REFERENCES
# ==========================================

def extract_reference(text):


    refs=re.findall(

        r"[A-Z]{2,}-\d+",

        text

    )


    return refs






# ==========================================
# DOCUMENT CHECKLIST
# ==========================================

def required_documents(visa_type):


    documents={


        "Student Visa":[

            "Passport",

            "Admission letter",

            "Financial proof",

            "Health insurance",

            "Language certificate"

        ],



        "Family Reunion Visa":[

            "Marriage certificate",

            "Passport",

            "Residence documents",

            "Health insurance"

        ],



        "Work Visa":[

            "Employment contract",

            "Passport",

            "Qualification documents"

        ],



        "Residence Permit":[

            "Passport",

            "Residence application",

            "Proof of address"

        ]

    }



    return documents.get(

        visa_type,

        [

        "Passport",

        "Application form",

        "Supporting documents"

        ]

    )






# ==========================================
# SAVE VISA MEMORY
# ==========================================

def save_visa_memory(data):


    save_entity(

        "visa",

        data["type"],

        str(data),

        None

    )


    return True






# ==========================================
# VISA WORKFLOW
# ==========================================

def analyze_visa_request(document):


    if not detect_visa(document):

        return {

            "status":
            "Not a visa request"

        }




    visa_type = detect_visa_type(
        document
    )



    result={


        "agent":
        "Visa Agent",


        "type":
        visa_type,


        "references":
        extract_reference(document),


        "required_documents":
        required_documents(visa_type),


        "next_steps":[


            "Check document completeness",

            "Prepare application package",

            "Submit to authority",

            "Track application status"

        ]

    }



    save_visa_memory(
        result
    )



    return result






# ==========================================
# TEST
# ==========================================

if __name__=="__main__":


    text="""

    Ausländerbehörde requested my
    residence permit documents.

    Reference: VISA-458921

    """


    print(
        analyze_visa_request(text)
    )