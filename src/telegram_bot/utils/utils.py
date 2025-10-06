def get_email_list_to_text(email_list: list[dict]) -> str:
    email_list_to_text = ""
    if not email_list:
        return "Нет подключенных почт"
    for i in range(len(email_list)):
        email_list_to_text += f"{i + 1}: {email_list[i]["email"]}\n"
    return email_list_to_text
