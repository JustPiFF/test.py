import telebot
from math import ceil

# Создание экземпляра бота
bot = telebot.TeleBot('TOKEN')

# Коэффициенты для расчетов
coefficient_d = 6.43 # Коэффициент электричества
coefficient_e = 50.93 # Коэффициент ХВС
coefficient_f = 243.16 # Коэффициент ГВС
coefficient_sum = 39.97 # Коэффициент водоотвода


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я рассчитываю оплату счётчиков! Сначала вводим показания за прошлый месяц, а затем текущие.')
    bot.send_message(message.chat.id, 'Напиши показания счётчика Эл.энергии в "кВт/ч" за прошлый месяц.')

# Обработчик ввода числа A
@bot.message_handler(func=lambda message: True)
def process_number_a(message):
    try:
        a = float(message.text)
        bot.send_message(message.chat.id, 'Напиши показания счётчика ХВС в "м3" (холодная вода) за прошлый месяц.')
        bot.register_next_step_handler(message, process_number_b, a)
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректный ввод. Введите число.')

# Обработчик ввода числа B
def process_number_b(message, a):
    try:
        b = float(message.text)
        bot.send_message(message.chat.id, 'Напиши показания счётчика ГВС в "м3" (горячая вода) за прошлый месяц.')
        bot.register_next_step_handler(message, process_number_c, a, b)
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректный ввод. Введите число.')

# Обработчик ввода числа C
def process_number_c(message, a, b):
    try:
        c = float(message.text)
        bot.send_message(message.chat.id, 'Отлично! Ты ввёл показания за прошлый месяц. Что у нас в этом месяце по счётчикам?')
        bot.send_message(message.chat.id, 'Напиши показания счётчика Эл.энергии в "кВт/ч" в этом месяце.')
        bot.register_next_step_handler(message, process_number_d, a, b, c)
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректный ввод. Введите число.')

# Обработчик ввода числа D
def process_number_d(message, a, b, c):
    try:
        d = float(message.text)
        result_d = (d - a)
        bot.send_message(message.chat.id, 'Напиши показания счётчика ХВС в "м3" (холодная вода) в этом месяце.')
        bot.register_next_step_handler(message, process_number_e, a, b, c, result_d)
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректный ввод. Введите число.')

# Обработчик ввода числа E
def process_number_e(message, a, b, c, result_d):
    try:
        e = float(message.text)
        result_e = (e - b)
        bot.send_message(message.chat.id, 'Напиши показания счётчика ГВС в "м3" (горячая вода) в этом месяце.')
        bot.register_next_step_handler(message, process_number_f, a, b, c, result_d, result_e)
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректный ввод. Введите число.')

# Обработчик ввода числа F
def process_number_f(message, a, b, c, result_d, result_e):
    try:
        f = float(message.text)
        result_f = (f - c)
        result_sum_ef = result_e + result_f
        result = (result_d, result_e, result_f, result_sum_ef)
        bot.send_message(message.chat.id, f'Итого израсходовали (Эл. энергия, ХВС, ГВС, водоотвод): {result}')
        result_with_coefficient = (
            result_d * coefficient_d,
            result_e * coefficient_e,
            result_f * coefficient_f,
            result_sum_ef * coefficient_sum
        )
        bot.send_message(message.chat.id, f'К оплате (Эл. энергия, ХВС, ГВС, водоотвод): {result_with_coefficient}')
        result_sum = sum(result_with_coefficient)
        result_sum_rounded = ceil(result_sum * 100) / 100  # Округление до сотых
        bot.send_message(message.chat.id, f'Сумма оплате: {result_sum_rounded}')
        bot.send_message(message.chat.id, 'Готово! Введите /start для начала сначала.')
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректный ввод. Введите число.')

# Запуск бота
bot.polling()
