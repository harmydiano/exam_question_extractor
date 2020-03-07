import psycopg2


class Db:

    def __init__(self):

        self.conn = psycopg2.connect("host=localhost dbname=exam user=test password=test")
        self.cur = self.conn.cursor()

    def create_db(self):

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS m_database(
        uid serial primary key not null,
        text varchar(500),
        option_one varchar(500),
        option_two varchar(500),
        option_three varchar(500),
        option_four varchar(500),
        answer varchar(500),
        exam_id integer,
        class_id integer,
        subject_id integer,
        instruction varchar(500),
        num_views integer,
        exam_year integer,
        exam_number integer
        )
        """)
        self.conn.commit()

        #postgres_insert_query = """ INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)"""
        #record_to_insert = (5, 'One Plus 6', 950)
        #cursor.execute(postgres_insert_query, record_to_insert)

    def insert_db(self, text, ans, op_one, op_two, op_three, op_four, ex_id, cls_id,sub_id,inst, nm_v, ex_year, ex_num):
        self.create_db()
        cls_id = int(cls_id)
        sub_id = int(sub_id)
        nm_v = int(nm_v)
        ex_year = int(ex_year)

        print(text, ans)
        postgres_insert_query = """ 
        INSERT INTO m_database (uid,text,answer, option_one, option_two, option_three,
        option_four, exam_id, class_id, subject_id, instruction, num_views, exam_year, exam_number) 
        VALUES (DEFAULT,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s)"""
        record_to_insert = (text, ans, op_one, op_two, op_three, op_four, ex_id, cls_id,sub_id,inst, nm_v, ex_year, ex_num)
        self.cur.execute(postgres_insert_query, record_to_insert)
        self.conn.commit()