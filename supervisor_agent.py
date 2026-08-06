# ==========================================
# supervisor_agent.py
# Bureaucracy AI Multi-Agent Supervisor
# ==========================================


from email_agent import email_agent
from bill_agent import analyze_bill
from task_planner import create_task



# ==========================================
# ROUTING KEYWORDS
# ==========================================

ROUTES = {


    "Bill Agent":[

        "bill",
        "invoice",
        "rechnung",
        "electricity",
        "strom",
        "internet",
        "rent",
        "miete",
        "payment"

    ],



    "Tax Agent":[

        "tax",
        "steuer",
        "finanzamt",
        "elster"

    ],



    "Visa Agent":[

        "visa",
        "residence",
        "aufenthalt",
        "immigration",
        "permit"

    ],



    "Insurance Agent":[

        "insurance",
        "versicherung",
        "krankenkasse"

    ],



    "Email Agent":[

        "email",
        "message",
        "letter"

    ]

}




# ==========================================
# DETECT AGENT
# ==========================================

def detect_agent(text):


    text=text.lower()


    scores={}



    for agent, keywords in ROUTES.items():


        score=0


        for word in keywords:


            if word in text:

                score += 1



        scores[agent]=score




    selected=max(

        scores,

        key=scores.get

    )



    if scores[selected]==0:

        return "Email Agent"



    return selected





# ==========================================
# SUPERVISOR
# ==========================================

def supervisor_agent(request):


    agent = detect_agent(
        request
    )



    print(
        "Supervisor selected:",
        agent
    )



    # =========================
    # BILL
    # =========================

    if agent=="Bill Agent":


        bill=analyze_bill(
            request
        )


        if bill:


            context={

            "email_id":0,

            "category":"Finance",

            "task":
            "Complete payment",

            "deadline":
            bill["deadline"],

            "bill":
            bill,

            "email":
            request

            }


            return create_task(
                context
            )



        return {

            "agent":
            "Bill Agent",

            "status":
            "Bill detected but analysis failed"

        }




    # =========================
    # EMAIL
    # =========================

    elif agent=="Email Agent":


        return email_agent(
            request
        )




    # =========================
    # FUTURE AGENTS
    # =========================

    elif agent=="Tax Agent":


        return {

            "agent":
            "Tax Agent",

            "status":
            "Waiting for tax_agent implementation"

        }




    elif agent=="Visa Agent":


        return {

            "agent":
            "Visa Agent",

            "status":
            "Waiting for visa_agent implementation"

        }




    elif agent=="Insurance Agent":


        return {

            "agent":
            "Insurance Agent",

            "status":
            "Insurance workflow available through email_agent"

        }




    return {

        "agent":
        agent,

        "status":
        "Completed"

    }





# ==========================================
# TEST
# ==========================================

if __name__=="__main__":


    examples=[


        """
        Electricity bill from Stadtwerke München
        Amount 85.50 €
        Customer number 458921
        """,


        """
        Finanzamt sent tax declaration request
        """,


        """
        I need to extend my residence permit
        """

    ]



    for e in examples:


        print(
            "----------------"
        )


        print(
            supervisor_agent(e)
        )