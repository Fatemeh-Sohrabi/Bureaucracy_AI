# ==========================================
# bill_manager.py
# Bureaucracy AI Bill Manager
# ==========================================


from datetime import datetime

from database import cursor, conn



# ==========================================
# SAVE BILL
# ==========================================

def save_bill(
        task_id,
        bill
):


    cursor.execute(
    """
    INSERT INTO bills
    (
        task_id,
        bill_type,
        provider,
        amount,
        customer_number,
        deadline,
        status,
        created_at
    )

    VALUES (?,?,?,?,?,?,?,?)

    """,

    (

        task_id,

        bill.get(
            "type"
        ),


        bill.get(
            "provider"
        ),


        bill.get(
            "amount"
        ),


        bill.get(
            "customer_number"
        ),


        bill.get(
            "deadline"
        ),


        bill.get(
            "status",
            "UNPAID"
        ),


        datetime.now().isoformat()

    )

    )


    conn.commit()


    return cursor.lastrowid





# ==========================================
# GET BILLS
# ==========================================

def get_bills():


    rows = cursor.execute(
    """
    SELECT

        id,
        task_id,
        bill_type,
        amount,
        customer_number,
        deadline,
        status


    FROM bills


    ORDER BY id DESC

    """
    ).fetchall()


    return rows





# ==========================================
# UPDATE BILL STATUS
# ==========================================

def update_bill_status(
        bill_id,
        status
):


    cursor.execute(
    """
    UPDATE bills

    SET status=?

    WHERE id=?

    """,

    (
        status,
        bill_id
    )

    )


    conn.commit()



    return True





# ==========================================
# TEST
# ==========================================

if __name__=="__main__":


    from bill_agent import analyze_bill



    email="""

    Electricity bill

    Amount: 85.50 €

    Customer number: 458921

    Pay before 20 August 2026

    """



    bill=analyze_bill(email)



    if bill:


        bill_id=save_bill(

            1,

            bill

        )


        print(
            "Saved bill:",
            bill_id
        )



        print(
            get_bills()
        )