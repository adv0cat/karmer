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

GET_ALL_KARMA_SQL = '''
SELECT R.to_user_id           AS user_id,
       SUM(RC.cost * R.count) AS total_karma
FROM Reactions R
         JOIN
     ReactionCost RC ON R.emoticon = RC.emoticon
WHERE R.channel_id = $1
GROUP BY R.to_user_id
HAVING SUM(RC.cost * R.count) <> 0
ORDER BY total_karma DESC;
    '''

GET_MY_KARMA_SQL = '''
SELECT SUM(RC.cost * R.count) AS total_karma
FROM Reactions R
         JOIN
     ReactionCost RC ON R.emoticon = RC.emoticon
WHERE R.channel_id = $1
  AND R.to_user_id = $2;
    '''
