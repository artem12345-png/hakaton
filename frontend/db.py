import psycopg2
import psycopg2.extras

conn = psycopg2.connect("""
    host=rc1b-7dcuebkqzirwnxee.mdb.yandexcloud.net
    port=6432
    sslmode=verify-full
    dbname=db
    user=user
    password=MfjQkR6zh6aCG7q4
""")
q = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def all_regions():
    query = """
    select * from regions;
    """
    q.execute(query)
    regions = [region['name'] for region in q.fetchall()]

    return regions


def get_region(region='район Внуково'):
    query = f"""
    select * from regions
    where name='{region}';
    """
    q.execute(query)

    return q.fetchall()[0].get('district_id', '')



