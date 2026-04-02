import re
from users.models import Account

def sanitize_existing_phones():
    users = Account.objects.all()
    updated_count = 0
    deleted_count = 0

    for user in users:
        raw_phone = user.phone
        if not raw_phone:
            continue

        # split multiple numbers and take first
        raw_phone = raw_phone.split('/')[0].strip()

        # remove non-digit characters
        phone = re.sub(r'\D', '', raw_phone)

        # convert +251XXXXXXXXX to 09XXXXXXXX
        if phone.startswith('251') and len(phone) == 12:
            phone = '0' + phone[3:]

        # fix missing leading zero
        if len(phone) == 9 and phone.startswith('9'):
            phone = '0' + phone

        # only update if it’s a valid Ethiopian phone
        if len(phone) == 10 and phone.startswith('09'):
            # check if another user already has this phone
            existing = Account.objects.filter(phone=phone).exclude(id=user.id).first()
            if existing:
                print(f"Deleting duplicate user {existing.id} with phone {phone}")
                existing.delete()
                deleted_count += 1

            if phone != user.phone:
                user.phone = phone
                user.save(update_fields=['phone'])
                updated_count += 1
        else:
            print(f"Skipping invalid phone for user {user.id}: {raw_phone}")

    print(f"Sanitized {updated_count} phone numbers.")
    print(f"Deleted {deleted_count} duplicate users.")