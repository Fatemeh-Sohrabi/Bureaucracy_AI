# ==========================================
# task_planner.py
# Bureaucracy AI Task Planning Agent
# ==========================================


from datetime import datetime, timedelta

from database import cursor, conn



# ==========================================
# TIME
# ==========================================

def now():

    return datetime.now().isoformat()



# ==========================================
# CONSEQUENCE KNOWLEDGE
# ==========================================

CONSEQUENCES = {


    "Visa":
    {
        "risk":
        "Residence or visa process may be delayed",

        "impact":
        "Critical"
    },


    "Insurance":
    {
        "risk":
        "Insurance approval may be delayed",

        "impact":
        "High"
    },


    "University":
    {
        "risk":
        "Application process may stop",

        "impact":
        "High"
    },


    "Finance":
    {
        "risk":
        "Late payment penalty may occur",

        "impact":
        "Medium"
    },


    "Tax":
    {
        "risk":
        "Tax filing problems may occur",

        "impact":
        "High"
    },


    "General":
    {
        "risk":
        "Unknown administrative risk",

        "impact":
        "Low"
    }

}





# ==========================================
# NORMALIZE TASK
# ==========================================

def normalize_task(
        task,
        category
):


    task=task.lower()



    if category=="Insurance":

        return "Submit insurance documents"



    if category=="Visa":

        return "Submit visa documents"



    if category=="University":

        return "Complete university application"



    if category=="Finance":

        return "Complete payment"



    if category=="Tax":

        return "Review tax documents"



    return task.capitalize()





# ==========================================
# PRIORITY ENGINE
# ==========================================

def calculate_priority(
        category,
        deadline
):


    score=0



    if deadline:

        score+=2



    if category=="Visa":

        score+=4



    elif category=="University":

        score+=3



    elif category=="Insurance":

        score+=2



    elif category=="Tax":

        score+=2



    elif category=="Finance":

        score+=1




    if score>=5:

        return "Critical"


    elif score>=3:

        return "High"


    else:

        return "Normal"





# ==========================================
# DUPLICATE CHECK
# ==========================================

def task_exists(task):


    rows=cursor.execute(
    """

    SELECT id,task

    FROM tasks_v03

    WHERE status!='DONE'

    """
    ).fetchall()



    for row in rows:


        if task.lower() in row[1].lower():

            return row[0]



    return None





# ==========================================
# CREATE TASK
# ==========================================

def create_task(context):


    category=context["category"]


    task=normalize_task(

        context["task"],

        category

    )



    deadline=context["deadline"]



    priority=calculate_priority(

        category,

        deadline

    )



    consequence=CONSEQUENCES.get(

        category,

        CONSEQUENCES["General"]

    )



    existing=task_exists(
        task
    )



    if existing:


        return {


            "task_id":existing,

            "status":"EXISTING"

        }





    explanation=f"""

AI TASK ANALYSIS

Category:
{category}


Task:
{task}


Deadline:
{deadline}


Risk:
{consequence['risk']}


Impact:
{consequence['impact']}

"""



    cursor.execute(
    """

    INSERT INTO tasks_v03

    (

    email_id,

    category,

    task,

    deadline,

    priority,

    risk,

    explanation,

    status,

    created_at

    )

    VALUES (?,?,?,?,?,?,?,?,?)

    """,

    (

    context.get("email_id",0),

    category,

    task,

    deadline,

    priority,

    consequence["risk"],

    explanation,

    "ACTIVE",

    now()

    )

    )


    conn.commit()



    return {


        "task_id":cursor.lastrowid,

        "task":task,

        "category":category,

        "priority":priority,

        "deadline":deadline,

        "risk":consequence["risk"],

        "status":"CREATED"

    }





# ==========================================
# REMINDER CREATION
# ==========================================

def create_reminder(
        task_id,
        deadline
):


    if deadline is None:

        return False



    try:

        date=datetime.strptime(

            deadline,

            "%d %B %Y"

        )


    except:

        return False



    reminder_date=date-timedelta(
        days=7
    )



    cursor.execute(
    """

    INSERT INTO reminders

    (

    task_id,

    reminder_date,

    reminder_type,

    status

    )

    VALUES(?,?,?,?)

    """,

    (

    task_id,

    reminder_date.strftime("%Y-%m-%d"),

    "7_DAYS_BEFORE",

    "PENDING"

    )

    )


    conn.commit()


    return True





# ==========================================
# SHOW TASKS
# ==========================================

def show_tasks():


    rows=cursor.execute(
    """

    SELECT

    id,

    category,

    task,

    deadline,

    priority,

    status


    FROM tasks_v03


    ORDER BY id DESC


    """
    ).fetchall()



    for row in rows:

        print(row)





if __name__=="__main__":


    from database import init_database

    init_database()


    test={

        "email_id":1,

        "category":"Insurance",

        "task":"submit documents",

        "deadline":"15 September 2026"

    }



    print(
        create_task(test)
    )


    show_tasks()