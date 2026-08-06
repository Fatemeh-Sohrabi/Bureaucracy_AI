# ==========================================
# rag_engine.py
# Bureaucracy AI RAG Engine
# ==========================================


from database import cursor, conn



# ==========================================
# ADD KNOWLEDGE
# ==========================================

def add_knowledge(
        source,
        topic,
        content
):


    cursor.execute(
    """
    INSERT INTO knowledge_base
    (
        source,
        topic,
        content
    )

    VALUES (?,?,?)

    """,

    (
        source,
        topic,
        content
    )

    )


    conn.commit()




# ==========================================
# SEARCH KNOWLEDGE
# ==========================================

def rag_search(topic):


    rows = cursor.execute(
    """
    SELECT

    source,
    topic,
    content


    FROM knowledge_base


    WHERE

    topic LIKE ?

    OR

    content LIKE ?

    """,

    (
        f"%{topic}%",
        f"%{topic}%"
    )

    ).fetchall()



    results=[]


    for row in rows:


        results.append(

            {

            "source":row[0],

            "topic":row[1],

            "content":row[2]

            }

        )


    return results




# ==========================================
# BUILD CONTEXT
# ==========================================

def build_rag_context(topic):


    documents = rag_search(topic)



    if not documents:


        return "No relevant knowledge found"



    context=""


    for doc in documents:


        context += f"""

SOURCE:
{doc['source']}


TOPIC:
{doc['topic']}


KNOWLEDGE:

{doc['content']}


----------------------

"""


    return context




# ==========================================
# INITIAL KNOWLEDGE
# ==========================================

def initialize_rag():


    documents=[


        (

        "German Insurance Rules",

        "Insurance",

        """
Health insurance companies may request
documents before activation.

Missing documents can delay approval.

"""

        ),



        (

        "German Immigration Rules",

        "Visa",

        """
Foreign residents may need to provide
additional documents.

Late responses can delay residence procedures.

"""

        ),



        (

        "German University Rules",

        "University",

        """
Universities require complete documents
before admission processing.

"""

        ),



        (

        "German Tax Rules",

        "Tax",

        """
Tax documents should be reviewed before
submission to Finanzamt.

"""

        )



    ]




    for doc in documents:


        exists = cursor.execute(
        """
        SELECT id

        FROM knowledge_base

        WHERE source=?

        """,

        (doc[0],)

        ).fetchone()



        if exists is None:


            add_knowledge(

                doc[0],

                doc[1],

                doc[2]

            )



    print(
        "RAG Knowledge Initialized"
    )




if __name__=="__main__":


    from database import init_database


    init_database()


    initialize_rag()


    print(
        build_rag_context(
            "Insurance"
        )
    )