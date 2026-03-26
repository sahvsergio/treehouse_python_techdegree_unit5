# 🔹 Create table in MySQL (drop first if exists)
with engine.connect() as conn:
    conn.execute("DROP TABLE IF EXISTS my_projects;")
metadata.create_all(engine)

# 🔹 Insert rows inside transaction
with engine.begin() as conn:  # ensures commit
    for row in rows:
        id_, title, date_str, description, skills, github = row
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except:
            date = datetime.datetime.now()
        conn.execute(projects_table.insert().values(
            id=id_,
            title=title,
            date=date,
            description=description,
            skills_practiced=skills,
            url=github
        ))
