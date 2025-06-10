UPDATE user_info
SET
    accessed = 'Y'
WHERE
    email = %s;