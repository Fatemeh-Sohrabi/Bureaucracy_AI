# ==========================================
# main.py
# Bureaucracy AI Main Orchestrator
# ==========================================


from database import init_database

from rag_engine import initialize_rag

from supervisor_agent import supervisor_agent

from task_planner import show_tasks




# ==========================================
# SYSTEM STARTUP
# ==========================================

def startup():


    print("""

====================================

        Bureaucracy AI

     Multi-Agent Assistant

====================================

Starting system...

""")


    init_database()


    initialize_rag()


    print(
        "System Ready\n"
    )





# ==========================================
# PROCESS USER MESSAGE
# ==========================================

def process_request(message):


    print(
        "\nAnalyzing request...\n"
    )


    result = supervisor_agent(
        message
    )


    print(
        "\n===== AI RESULT =====\n"
    )


    print(result)



    return result





# ==========================================
# DEMO
# ==========================================

if __name__=="__main__":


    startup()



    examples=[



        """
        ABC Insurance GmbH requires my
        insurance documents before
        15 September 2026.

        Policy number INS-458921.
        """,



        """
        Electricity bill from Stadtwerke München.

        Amount 85.50 €.

        Customer number 458921.

        """,



        """
        Finanzamt sent my
        Steuererklärung request
        for 2025.
        """,



        """
        Ausländerbehörde requested
        my residence permit documents.
        """

    ]



    for item in examples:


        print(
            "\n=============================="
        )


        process_request(
            item
        )



    print(
        "\n===== CURRENT TASKS ====="
    )


    show_tasks()
