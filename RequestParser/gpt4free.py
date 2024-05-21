from g4f.client import Client

clientGPT = Client()

prompt = ("Выступи в роли фрилансера в сфере смм/маркетинг, "
          "тебе нужно определять заказы относящиеся к твоей работе. "
          "2. Контекст: я предоставлю вам текст беседы. "
          "3. Ваша задача: определить, содержит ли текст информацию о поиске сотрудника "
          "(обязанности, оплату, время, график и т.д.) и относится ли этот текст "
          "к SMM/маркетингу? 4. Формат: Если текст содержит поиск сотрудника(обязанности,"
          " оплату, время, график и т.д.) и соответствует SMM/маркетингу/, "
          "укажите только  #маркетинг/#smm; если текст содержит рекламу "
          "(призыв к действию, услуги, ссылки и т.д.) - ответьте только 'нет'. Текст:")
async def check_message(message):
    response = clientGPT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": str(prompt + message)}]
    )
    #print(message)
    #print("Ответ ГПТ: " + response.choices[0].message.content)
    if ( 'маркетинг'in response.choices[0].message.content
            or 'смм' in response.choices[0].message.content
            or 'smm' in response.choices[0].message.content
            or 'marketing' in response.choices[0].message.content):
        print(message)
        print("Ответ ГПТ: " + response.choices[0].message.content)
        return True
