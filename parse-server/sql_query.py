INSERT_REACTIONS_SQL = '''
INSERT INTO reactions (channel_id, msg_id, from_user_id, to_user_id, emoticon, count, created_at)
VALUES ($1, $2, $3, $4, $5, $6, $7)
ON CONFLICT (channel_id, msg_id, from_user_id, emoticon)
    DO UPDATE SET count      = EXCLUDED.count,
                  created_at = EXCLUDED.created_at;
    '''

DELETE_REACTIONS_SQL = '''
DELETE
FROM Reactions
WHERE channel_id = $1
  AND msg_id IN (SELECT * FROM unnest($2::integer[]))
  AND (channel_id, msg_id, from_user_id, emoticon)
    NOT IN (SELECT * FROM unnest($3::PKeyReaction[]));
    '''
