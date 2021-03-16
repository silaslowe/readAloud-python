DELETE
FROM auth_user
WHERE id = 3; 

DELETE
FROM readAloudapi_topic
WHERE id = 9; 

DELETE
FROM readAloudapi_booktopic
WHERE id = 5; INSERT INTO readAloudapi_book (
    id,
    title,
    author,
    publish_year,
    notes,
    cover_url,
    rating,
    location,
    synopsis,
    profile_id
  )
VALUES (
    id:integer,
    'title:varchar(75)',
    'author:varchar(75)',
    publish_year:integer,
    'notes:text',
    'cover_url:varchar(125)',
    rating:real,
    'location:varchar(50)',
    'synopsis:text',
    profile_id:integer
  );