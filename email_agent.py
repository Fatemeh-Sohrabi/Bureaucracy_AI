# ==========================================
# email_agent.py
# Bureaucracy AI Email Understanding Agent
# ==========================================


import re
from datetime import datetime


from database import cursor, conn


from memory_engine import (
    save_entity,
    save_working_memory,
    retrieve_memories
)


from rag_engine import (
    build_rag_context
)



# ==========================================
# SAVE EMAIL
# ==========================================

def save_email(
        email,
        sender="Unknown",
        subject="No Subject"
):


    cursor.execute(
    """
    INSERT INTO emails
    (
        sender,
        subject,
        body,
        language,
        created_at
    )

    VALUES (?,?,?,?,?)

    """,

    (
        sender,
        subject,
        email,
        "English",
        datetime.now().isoformat()
    )

    )


    conn.commit()


    return cursor.lastrowid




# ==========================================
# EMAIL CATEGORY
# ==========================================


CATEGORIES = {


    "Insurance":[

        "insurance",
        "versicherung",
        "krankenkasse",
        "documents",
        "unterlagen"

    ],


    "Visa":[

        "visa",
        "residence",
        "aufenthalt",
        "immigration",
        "passport"

    ],


    "University":[

        "university",
        "admission",
        "application",
        "professor"

    ],


    "Finance":[

        "bill",
        "invoice",
        "payment",
        "rechnung"

    ],


    "Tax":[

        "tax",
        "steuer",
        "finanzamt",
        "elster"

    ]

}




def classify_email(email):


    text=email.lower()


    scores={}


    for category,words in CATEGORIES.items():


        score=0


        for word in words:


            if word in text:

                score+=1



        scores[category]=score



    result=max(
        scores,
        key=scores.get
    )



    if scores[result]==0:

        return "General"



    return result




# ==========================================
# ENTITY EXTRACTION
# ==========================================

def extract_entities(email):


    entities={

        "organizations":[],
        "references":[],
        "dates":[]

    }



    organizations=re.findall(

        r"[A-Z][A-Za-z]+\s[A-Z][A-Za-z]+\s(?:GmbH|AG)",

        email

    )


    entities["organizations"]=organizations



    references=re.findall(

        r"[A-Z]{2,}-\d+",

        email

    )


    entities["references"]=references



    dates=re.findall(

        r"\d{1,2}\s[A-Z][a-z]+\s\d{4}",

        email

    )


    entities["dates"]=dates



    return entities




# ==========================================
# TASK EXTRACTION
# ==========================================

def extract_task(email):


    text=email.lower()



    if "submit" in text:

        return "Submit requested documents"



    if "provide" in text:

        return "Provide requested information"



    if "pay" in text:

        return "Complete payment"



    if "register" in text:

        return "Complete registration"



    return "Review email"





# ==========================================
# DEADLINE
# ==========================================

def extract_deadline(email):


    result=re.search(

        r"\d{1,2}\s[A-Z][a-z]+\s\d{4}",

        email

    )


    if result:

        return result.group()


    return None




# ==========================================
# MAIN EMAIL AGENT
# ==========================================

def email_agent(email):


    email_id=save_email(
        email
    )



    category=classify_email(
        email
    )



    entities=extract_entities(
        email
    )



    task=extract_task(
        email
    )



    deadline=extract_deadline(
        email
    )



    # Save organization memory

    for org in entities["organizations"]:


        save_entity(

            "organization",

            org,

            "Detected from email",

            email_id

        )



    # Save references

    for ref in entities["references"]:


        save_entity(

            "reference",

            ref,

            "Detected reference number",

            email_id

        )



    previous_memory=[]


    for org in entities["organizations"]:


        previous_memory.extend(

            retrieve_memories(
                org
            )

        )



    knowledge=build_rag_context(
        category
    )



    context={


        "email_id":email_id,


        "category":category,


        "task":task,


        "deadline":deadline,


        "entities":entities,


        "previous_memory":previous_memory,


        "knowledge":knowledge


    }



    save_working_memory(

        email_id,

        str(context)

    )



    return context




# ==========================================
# TEST
# ==========================================

if __name__=="__main__":


    from database import init_database
    from rag_engine import initialize_rag


    init_database()

    initialize_rag()



    email="""

Dear Fatemeh,

ABC Insurance GmbH requires you to submit
your insurance documents before 15 September 2026.

Policy number INS-458921.

"""


    result=email_agent(email)


    print(result)