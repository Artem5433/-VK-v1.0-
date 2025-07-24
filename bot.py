import vk_api
import time

# === НАСТРОЙКИ ===
TOKEN = 'ВАШ_ТОКЕН'
SOURCE_GROUP_ID = -123456789  # ID паблика-источника (со знаком минус!)
TARGET_GROUP_ID = -987654321  # ID вашей группы (со знаком минус!)

# ================

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
POSTED_IDS = set()

def get_latest_post(group_id):
    posts = vk.wall.get(owner_id=group_id, count=1)['items']
    return posts[0] if posts else None

def repost_to_group(post):
    attachments = []

    if 'attachments' in post:
        for att in post['attachments']:
            if att['type'] == 'photo':
                attachments.append(f"photo{att['photo']['owner_id']}_{att['photo']['id']}")
            elif att['type'] == 'video':
                attachments.append(f"video{att['video']['owner_id']}_{att['video']['id']}")

    vk.wall.post(
        owner_id=TARGET_GROUP_ID,
        from_group=1,
        message=post.get('text', ''),
        attachments=','.join(attachments)
    )

print("Бот запущен...")

while True:
    try:
        latest_post = get_latest_post(SOURCE_GROUP_ID)
        if latest_post and latest_post['id'] not in POSTED_IDS:
            repost_to_group(latest_post)
            POSTED_IDS.add(latest_post['id'])
            print(f"Новый пост опубликован: ID {latest_post['id']}")
        time.sleep(300)  # Проверка каждые 5 минут
    except Exception as e:
        print("Ошибка:", e)
        time.sleep(60)
