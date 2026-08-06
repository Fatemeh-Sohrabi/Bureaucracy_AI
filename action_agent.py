# ==========================================
# action_agent.py
# Bureaucracy AI Action Agent
# ==========================================


from database import cursor, conn

from memory_engine import save_episode

from datetime import datetime



# ==========================================
# TIME
# ==========================================

def now():

    return datetime.now().isoformat()




# ==========================================
# GET TASK
# ==========================================

def get_task(task_id):


    task = cursor.execute(
    """
    SELECT

    id,
    category,
    task,
    deadline,
    priority,
    status,
    explanation

    FROM tasks_v03

    WHERE id=?

    """,

    (task_id,)

    ).fetchone()



    return task




# ==========================================
# REPLY GENERATOR
# ==========================================

def generate_reply(category):


    replies={


    "Insurance":

"""
Sehr geehrte Damen und Herren,

vielen Dank für Ihre Nachricht.

Ich bestätige den Erhalt Ihrer Anfrage.
Die angeforderten Unterlagen werde ich
fristgerecht einreichen.

Mit freundlichen Grüßen

Fatemeh Sohrabi
""",



    "Visa":

"""
Sehr geehrte Damen und Herren,

vielen Dank für Ihre Nachricht.

Ich werde die erforderlichen Dokumente
schnellstmöglich übermitteln.

Mit freundlichen Grüßen

Fatemeh Sohrabi
""",



    "University":

"""
Dear Sir/Madam,

Thank you for your message.

I have received your request and will
provide the required documents.

Best regards,

Fatemeh Sohrabi
""",



    "Tax":

"""
Sehr geehrte Damen und Herren,

vielen Dank für Ihre Nachricht.

Ich werde die angeforderten
Steuerunterlagen prüfen.

Mit freundlichen Grüßen

Fatemeh Sohrabi
"""



    }



    return replies.get(

        category,

        "Thank you for your message. I will review it."

    )





# ==========================================
# COMPLETE TASK
# ==========================================

def complete_task(task_id):


    cursor.execute(
    """

    UPDATE tasks_v03

    SET status='DONE'

    WHERE id=?

    """,

    (task_id,)

    )


    conn.commit()



    save_episode(

        task_id,

        "complete",

        "Task completed"

    )



    return {

        "status":"DONE",

        "message":
        "Task completed successfully"

    }





# ==========================================
# SNOOZE TASK
# ==========================================

def snooze_task(task_id):


    cursor.execute(
    """

    UPDATE tasks_v03

    SET status='SNOOZED'

    WHERE id=?

    """,

    (task_id,)

    )


    conn.commit()



    save_episode(

        task_id,

        "snooze",

        "Task postponed"

    )



    return {

        "status":"SNOOZED",

        "message":
        "Task postponed"

    }





# ==========================================
# DELETE TASK
# ==========================================

def delete_task(
        task_id,
        confirm=False
):


    if not confirm:


        return {

            "status":
            "WAITING_CONFIRMATION",

            "message":
            "Confirmation required"

        }




    task=get_task(task_id)



    if task is None:


        return {

            "status":
            "ERROR",

            "message":
            "Task not found"

        }




    cursor.execute(
    """

    UPDATE tasks_v03

    SET status='DELETED'

    WHERE id=?

    """,

    (task_id,)

    )


    conn.commit()



    save_episode(

        task_id,

        "delete",

        "Task deleted"

    )



    return {


        "status":
        "DELETED",

        "message":
        f"Task {task_id} deleted"

    }





# ==========================================
# EXPLAIN TASK
# ==========================================

def explain_task(task_id):


    task=get_task(task_id)



    if task is None:

        return "Task not found"




    return f"""

========== AI TASK EXPLANATION ==========


Category:
{task[1]}


Task:
{task[2]}


Deadline:
{task[3]}


Priority:
{task[4]}


Status:
{task[5]}


Explanation:

{task[6]}


=========================================

"""





# ==========================================
# MAIN ACTION
# ==========================================

def execute_action(
        task_id,
        action,
        confirm=False
):


    if action=="complete":

        return complete_task(task_id)



    elif action=="snooze":

        return snooze_task(task_id)



    elif action=="delete":

        return delete_task(
            task_id,
            confirm
        )



    elif action=="explain":

        return explain_task(task_id)



    elif action=="reply":


        task=get_task(task_id)



        if task is None:

            return "Task not found"



        return generate_reply(
            task[1]
        )



    else:

        return {

            "status":"ERROR",

            "message":
            "Unknown action"

        }





if __name__=="__main__":


    from database import init_database


    init_database()


    print(
        execute_action(
            1,
            "explain"
        )
    )