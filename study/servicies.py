def get_email_subscribes(course):
    """ Получаем email всех подписчиков """
    active_subscriptions = course.subscription_course.filter(is_active=True)
    subscribers_emails = []
    for subscription in active_subscriptions:
        subscribers_emails.append(subscription.user.email)

    return subscribers_emails
