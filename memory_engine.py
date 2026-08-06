# ==========================================
# memory_engine.py
# Bureaucracy AI Memory Engine
# ==========================================


from datetime import datetime

from database import cursor, conn



# ==========================================
# TIME
# ==========================================

def now():

    return datetime.now().isoformat()



# ==========================================
# ADD MEMORY
# ==========================================

def add_memory(
        memory_type,
        entity,
        content,
        importance=0.5,
        source_id=None
):


    cursor.execute(
    """
    INSERT INTO memories
    (
        memory_type,
        entity,
        content,
        importance,
        source_id,
        created_at
    )

    VALUES (?,?,?,?,?,?)

    """,
    (
        memory_type,
        entity,
        content,
        importance,
        source_id,
        now()
    )
    )


    conn.commit()




# ==========================================
# ENTITY MEMORY
# ==========================================

def save_entity(
        entity_type,
        name,
        description,
        source_id=None
):


    add_memory(

        entity_type,

        name,

        description,

        0.8,

        source_id

    )




# ==========================================
# WORKING MEMORY
# ==========================================

def save_working_memory(
        task_id,
        context
):


    add_memory(

        "working",

        f"task_{task_id}",

        context,

        0.9,

        task_id

    )




# ==========================================
# EPISODIC MEMORY
# ==========================================

def save_episode(
        task_id,
        action,
        result
):


    add_memory(

        "episode",

        action,

        f"""
Action:
{action}

Result:
{result}
""",

        0.7,

        task_id

    )




# ==========================================
# SEMANTIC MEMORY
# ==========================================

def save_semantic_memory(
        topic,
        knowledge
):


    add_memory(

        "semantic",

        topic,

        knowledge,

        1.0,

        None

    )




# ==========================================
# RETRIEVE MEMORY
# ==========================================

def retrieve_memories(
        keyword,
        memory_type=None
):


    if memory_type:


        rows = cursor.execute(
        """
        SELECT

        memory_type,
        entity,
        content,
        importance


        FROM memories


        WHERE

        (
        entity LIKE ?
        OR
        content LIKE ?
        )

        AND memory_type=?


        ORDER BY importance DESC

        """,

        (
            f"%{keyword}%",
            f"%{keyword}%",
            memory_type
        )

        ).fetchall()



    else:


        rows = cursor.execute(
        """
        SELECT

        memory_type,
        entity,
        content,
        importance


        FROM memories


        WHERE

        entity LIKE ?

        OR

        content LIKE ?


        ORDER BY importance DESC

        """,

        (
            f"%{keyword}%",
            f"%{keyword}%"
        )

        ).fetchall()



    return rows




# ==========================================
# MEMORY SUMMARY
# ==========================================

def memory_summary():


    rows = cursor.execute(
    """
    SELECT

    memory_type,
    COUNT(*)

    FROM memories

    GROUP BY memory_type

    """
    ).fetchall()


    return rows




# ==========================================
# BUILD CONTEXT
# ==========================================

def build_memory_context(keyword):


    memories = retrieve_memories(
        keyword
    )


    context=""


    for m in memories:


        context += f"""

TYPE:
{m[0]}

ENTITY:
{m[1]}

CONTENT:
{m[2]}

IMPORTANCE:
{m[3]}

--------------------

"""


    return context




if __name__=="__main__":


    from database import init_database

    init_database()


    save_entity(

        "organization",

        "ABC Insurance GmbH",

        "German health insurance company"

    )


    print(
        retrieve_memories(
            "ABC"
        )
    )