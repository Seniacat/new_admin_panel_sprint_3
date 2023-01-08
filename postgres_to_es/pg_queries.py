def get_movies_updates(start_time):
    return (f"""
    SELECT
        fw.id,
        fw.title,
        fw.description,
        fw.rating as imdb_rating,
        fw.updated_at,
        ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'director') AS director,
        ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'actor') AS actors,
        ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'writer') AS writers,
        ARRAY_AGG(DISTINCT g.name) as genre
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p ON p.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE fw.updated_at > '{start_time}'::timestamp
    GROUP BY fw.id
    ORDER BY fw.updated_at;
    """)


def get_person_updates(start_time):
    return (f"""
    WITH person AS (
        SELECT id, updated_at, full_name
        FROM content.person as p
        WHERE p.updated_at > '{start_time}'::timestamp
        ORDER BY p.updated_at
    )
    SELECT
        fw.id,
        fw.title,
        fw.description,
        fw.rating as imdb_rating,
        person.updated_at,
        ARRAY_AGG(DISTINCT jsonb_build_object('id', person.id, 'name', person.full_name)) FILTER (WHERE pfw.role = 'director') AS director,
        ARRAY_AGG(DISTINCT jsonb_build_object('id', person.id, 'name', person.full_name)) FILTER (WHERE pfw.role = 'actor') AS actors,
        ARRAY_AGG(DISTINCT jsonb_build_object('id', person.id, 'name', person.full_name)) FILTER (WHERE pfw.role = 'writer') AS writers,
        ARRAY_AGG(DISTINCT g.name) as genre
    FROM content.film_work as fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    JOIN person ON person.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    GROUP BY (person.updated_at, fw.id)
    ORDER BY person.updated_at;
    """)


def get_genre_updates(start_time):
    return (f"""
    WITH genres AS (
        SELECT id, updated_at, name
        FROM content.genre as g
        WHERE g.updated_at > '{start_time}'::timestamp
        ORDER BY g.updated_at
    )
    SELECT
        fw.id,
        fw.title,
        fw.description,
        fw.rating as imdb_rating,
        genres.updated_at,
        ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'director') AS director,
        ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'actor') AS actors,
        ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'writer') AS writers,
        ARRAY_AGG(DISTINCT genres.name) as genre
    FROM content.film_work as fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p ON p.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    JOIN genres ON genres.id = gfw.genre_id
    GROUP BY (genres.updated_at, fw.id)
    ORDER BY genres.updated_at;
    """)
