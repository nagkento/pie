import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="your_db",
    user="user",
    password="password"
)

cur = conn.cursor()

table = "table_a"

query = """
SELECT
    rid,
    uid,
    shape_mng_rid,
    shape_mng_uid,
    encode(coordinate,'hex') as coordinate,
    t_represent_rid,
    t_contents_id,
    t_box_hbr::text,
    t_llx_hbr,
    t_lly_hbr,
    t_urx_hbr,
    t_ury_hbr,
    create_stime,
    update_stime,
    sdiff_start_stime,
    sdiff_project_start_stime,
    sdiff_project_end_stime,
    sdiff_start_process,
    sdiff_end_process,
    sdiff_start_project,
    sdiff_end_project,
    sdiff_update_status
FROM table_a
"""

cur.execute(query)

columns = [d[0] for d in cur.description]
rows = cur.fetchall()

values_sql = []

timestamp_cols = {
    "create_stime",
    "update_stime",
    "sdiff_start_stime",
    "sdiff_project_start_stime",
    "sdiff_project_end_stime"
}

for row in rows:

    vals = []

    for col, val in zip(columns, row):

        if val is None:
            vals.append("NULL")

        elif col == "coordinate":
            vals.append(f"'\\\\x{val}'::bytea")

        elif col == "t_box_hbr":
            vals.append(f"'{val}'::box")

        elif col in timestamp_cols:
            vals.append(f"'{val}'::timestamp")

        elif isinstance(val, str):
            vals.append("'" + val.replace("'", "''") + "'")

        else:
            vals.append(str(val))

    values_sql.append("(" + ",".join(vals) + ")")

insert_sql = f"""
INSERT INTO {table} (
{",".join(columns)}
)
VALUES
{",\n".join(values_sql)};
"""

with open("insert.sql", "w") as f:
    f.write(insert_sql)

cur.close()
conn.close()
