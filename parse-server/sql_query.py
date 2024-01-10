INSERT_REACTIONS_SQL = '''
    INSERT INTO reactions (channel_id, msg_id, from_user_id, to_user_id, emoticon, count, created_at)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    ON CONFLICT (channel_id, msg_id, from_user_id, emoticon)
        DO UPDATE SET count = EXCLUDED.count;
    '''
