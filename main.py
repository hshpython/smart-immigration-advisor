# خوش آمدگویی به سبک حرفه‌ای
# print("=" * 50)
# print("🌟 به سامانه‌ی شبیه‌سازی مصاحبه‌ی مهاجرتی خوش آمدی!")
# print("=" * 50)
#
# # 1. دریافت اطلاعات از کاربر (ورودی)
# اسم = input("اسم خودت را وارد کن: ")
# سن = int(input("سن خودت را وارد کن (عدد): "))
# کشور_مقصد = input("کشور مورد نظرت برای مهاجرت رو بنویس: ")
#
# # 2. پردازش اطلاعات (یک منطق ساده و انگیزشی)
# if سن < 30:
#     امتیاز_سن = "عالی 🌟"
# elif 30 <= سن <= 45:
#     امتیاز_سن = "خیلی خوب (شما در بازه‌ی طلایی هستید) 💪"
# else:
#     امتیاز_سن = "با تجربه‌ترین افراد! (با سابقه کار جبران می‌شود) 😎"
#
# # 3. خروجی نهایی (چاپ با فرمت زیبا)
# print("\n" + "-" * 50)
# print("📋 خلاصه اطلاعات شما:")
# print(f"✅ نام: {اسم}")
# print(f"✅ سن: {سن} سال")
# print(f"✅ مقصد: {کشور_مقصد}")
# print(f"✅ وضعیت سنی: {امتیاز_سن}")
# print("-" * 50)
#
# # یه آرزوی قشنگ برای آخر کار
# print(f"🙏 {اسم} جان! قدم اول رو برداشتی. مسیر پایتون و مهاجرت از همینجا شروع شد!")


# print('*' * 50)
# print('🌟 سیستم ارزیابی اولیه مهاجرت به کانادا (بر اساس سن)')
# print('*' * 50)
# # گرفتن اطلاعات
# name = input('نام و نام خانوادگی: ')
# age = int(input('سن: '))
# education = input('مدرک تحصیلی (دیپلم/کاردانی/کارشناسی/ارشد): ')
# country = input('کشور مقصد: ')
# years_experience = input('سابقه کار : ')
# print('-' * 50)
# # منطق هوشمند ارزیابی سن (مشابه سیستم اکسپرس اینتری کانادا)
# if age < 18:
#     status = '🔴 متاسفانه سن شما کمتر از حداقل پذیرش است'
# elif 18 <= age <= 30:
#     status = '🟢 عالی! حداکثر امتیاز سن (۱۲ امتیاز)'
# elif 31 <= age <= 45:
#     status = '🟡 خوب! امتیاز سن متوسط (بازه طلایی شما)'
# elif 46 <= age <= 50:
#     status = '🟠 قابل قبول، نیاز به جبران با سابقه کار بالا'
# else:
#     status = '🔴 بالای ۵۰ سال، نیاز به بررسی ویژه دارد'
#
# # چاپ کارت خلاصه اطلاعات
# print('📋 کارت اطلاعات مهاجرتی شما:')
# print(f'   نام: {name}')
# print(f'   سن: {age} سال')
# print(f'   مدرک: {education}')
# print(f'   کشور مقصد: {country}')
# print(f'   وضعیت سنی: {status}')
# print(f'سابقه کار {years_experience}')
# print('*' * 50)
#
# # یه پیام انگیزشی خاص برای سن ۴۳ خودت
# if age == 43:
#     print(f'🔥 {name} عزیز! سن ۴۳ در کانادا "Golden Age" محسوب میشه، دقیقاً در اوج تجربه و انرژی!')


# print('Your Information Mohajerati : ')
# print('*' * 50)
#
# name = input('Name & Family : ')
# age = int(input('Age : '))
# education = input('Education : ')
# maghsadCountry = input('MaghsadCountry : ')
# sabeghehWork = input('SabeghehWork : ')
# job = input('Job : ')
#
# if age < 18:
#     resultage = 'سن شما از محدوده سن قانونی کمتر مییباشد......'
# elif 18 <= age <= 30:
#     resultage = 'سن شما دارای امتیاز طلایی هست......'
# elif 30 < age <= 40:
#     resultage = 'سن شما امتیاز فوق و العاده داره'
# elif 40 < age <= 50:
#     resultage = 'امتیاز شما خوب اما نیاز به سابقه و تجربه دارد'
# else:
#     resultage = 'سن شما از حداکثر سن مجاز بیشتره و باید بررسی کن'
#
# print(f'Name : {name}')
# print(f'Age : {age}')
# print(f'Education : {education}')
# print(f'MaghsadCountry : {maghsadCountry}')
# print(f'SabeghehWork : {sabeghehWork}')
# print(f'Job : {job}')
# print(f'Resultage : {resultage}')
#
# if age == 43:
#     print('شما با سن 43 میتوانید به کانادا بروید')


# print('*' * 50)
# print('🌟 سیستم ارزیابی اولیه مهاجرت به کانادا (بر اساس سن و سابقه کار)')
# print('*' * 50)
#
# # دریافت اطلاعات کاربر
# name = input('نام و نام خانوادگی: ')
# age = int(input('سن: '))
# education = input('مدرک تحصیلی (دیپلم/کاردانی/کارشناسی/ارشد): ')
# country = input('کشور مقصد: ')
# experience = input('سال‌های سابقه کار (عدد): ')
#
# # تبدیل سابقه کار به عدد
# try:
#     exp_years = int(experience)
# except:
#     exp_years = 0
#     print('⚠️ مقدار وارد شده برای سابقه کار معتبر نیست، صفر در نظر گرفته شد.')
#
# print('-' * 50)
#
# # ارزیابی سن (بر اساس سیستم امتیازدهی کانادا)
# if age < 18:
#     age_status = '🔴 کمتر از حداقل سن پذیرش'
#     age_score = 0
# elif 18 <= age <= 30:
#     age_status = '🟢 عالی! حداکثر امتیاز سن (۱۲ امتیاز)'
#     age_score = 12
# elif 31 <= age <= 45:
#     age_status = '🟡 خوب! امتیاز سن متوسط (بازه طلایی)'
#     age_score = 8
# elif 46 <= age <= 50:
#     age_status = '🟠 قابل قبول، نیاز به جبران با سابقه کار بالا'
#     age_score = 5
# else:
#     age_status = '🔴 بالای ۵۰ سال، نیاز به بررسی ویژه دارد'
#     age_score = 0
#
# # ارزیابی سابقه کار (امتیازدهی ساده)
# if exp_years >= 5:
#     exp_status = '💪 عالی! سابقه کار بالا (حداکثر امتیاز)'
#     exp_score = 15
# elif 3 <= exp_years < 5:
#     exp_status = '👍 خوب، نیاز به تقویت با پروژه‌های شخصی'
#     exp_score = 10
# elif 1 <= exp_years < 3:
#     exp_status = '🟡 متوسط، پیشنهاد می‌شود پروژه‌های عملی بیشتری انجام دهید'
#     exp_score = 5
# else:
#     exp_status = '🟠 کم، تمرکز بر روی ساختن پورتفولیوی قوی'
#     exp_score = 0
#
# if education == 'ارشد':
#     edu_status = "شما در رتبه ارشد هستید ، پس صاحب علم و تجربه بالایی هستید و دارای امتیاز طلایی هستسد"
#     edu_score = 8
# elif education == 'کارشناسی' :
#     edu_status = 'شما صاحب مدرک کارشناسی هستید پس بر اساس عمل و تجربه صاحب امتیاز خوبی هستید'
#     edu_score = 6
# elif education == 'کاردانی' :
#     edu_status = 'شما صاحب مدرک کاردانی هستید پس باید بخاطر سطح مدرک پایین دارای تجربه و عمل بالایی باشید'
#     edu_score = 4
# elif education == 'دیپلم' :
#     edu_status = 'مدرک فعلی شما دیپلم است پس با سابقه و تجربه فراوان مورد بررسی قرار خواهد گرفت'
#     edu_score = 2
# else:
#     edu_status = 'باید به صورت کامل مورد بررسی قرار گیرد'
#
# # جمع کل امتیازات (شبیه‌سازی ساده)
# total_score = age_score + exp_score + edu_score
#
# # چاپ کارت اطلاعات
# print('📋 کارت اطلاعات مهاجرتی شما:')
# print(f'   👤 نام: {name}')
# print(f'   📅 سن: {age} سال')
# print(f'   🎓 مدرک: {education}')
# print(f'   🌍 کشور مقصد: {country}')
# print(f'   💼 سابقه کار: {exp_years} سال')
# print(f'   📊 وضعیت سن: {age_status}')
# print(f'   📊 وضعیت سابقه: {exp_status}')
# print(f'وضعیت مدرک تحصیلی : {edu_status}')
# print(f'   ⭐ امتیاز کل (تقریبی): {total_score} از ۲۷')
# print('*' * 50)
#
# # پیام انگیزشی اختصاصی برای سن ۴۳
# if age == 43:
#     print(f'🔥 {name} عزیز! سن ۴۳ در کانادا "Golden Age" محسوب میشه، دقیقاً در اوج تجربه و انرژی!')
#     print(f'💡 با {experience} سال سابقه، شما در مسیر درستی هستید. همین الان شروع به ساخت پروژه‌های عملی کنید.')
# elif age >= 30 and age <= 45:
#     print(f'🌟 {name} جان! شما در بهترین بازه‌ی سنی برای مهاجرت هستید. روی تقویت مهارت‌های عملی تمرکز کن.')
# else:
#     print(f'🙏 {name} عزیز! هر سنی جایگاه خودش را دارد. با تلاش و برنامه‌ریزی، هدف دست‌یافتنی است.')
#
# print('*' * 50)
# print('✅ قدم اول برداشته شد! فردا میریم سراغ حلقه‌ها و لیست‌ها.')


# print('*' * 50)
# print('نمایش مشخصات کارت مهاجرتی...... ')
# print('*' * 50)
#
# name = input('نام و نام خانوادگی : ')
# age = (input('سن : '))
# education = input('تحصیلات : ')
# address = input('آدرس محل سکونت : ')
# job = input('شغل : ')
# sabegheh_work = input('سابقه کار : ')
# country_place = input('کشور مقصد : ')
#
# try:
#     age = int(age)
#     sabegheh_work = int(sabegheh_work)
# except:
#     age = 'سن خود را استاندارد وارد نکردید...!!'
#     sabegheh_work = 'سابقه کار را استاندارد وارد نکردید...!!'
#
# if sabegheh_work >= 10:
#     sab_years = 'شما سابقه کار طلایی دارید......'
#     sab_score = 20
# elif 5 <= sabegheh_work < 10:
#     sab_years = 'شما سابقه کار خوبی دارید......'
#     sab_score = 10
# elif 3 <= sabegheh_work < 5:
#     sab_years = 'شما سابقه کار متوسطی دارید......'
#     sab_score = 5
# else:
#     sab_years = 'سابقه کار شما کم است و باید مورد بررسی قرار گیرد......!!'
#     sab_score = 0
#
#
# if age < 18:
#     age_comment = 'سن شما برای مهاجرت پذیرفته نیست......!!'
#     age_score = 0
# elif 18 <= age <= 30:
#     age_comment = 'شما دارای سن طلایی برای مهاجرت هستید......'
#     age_score = 20
# elif  31 <= age <= 40:
#     age_comment = 'شما دارای سن خوبی برای مهاجرت هستید با توجه به تحصیلات و سابقه کار'
#     age_score = 15
# elif 41 <= age <= 50:
#     age_comment = 'شما دارای سن بالایی هستید و مهاجرت شما وابسته به تحصیلات و سابقه کار بالا هست......'
#     age_score = 10
# else:
#     age_comment = 'شما دارای سن بالایی نسبت به حد مجاز هستید بنابراین باید سابقه کار و تحصیلات شما مورد بررسی قرار گیرد......!! '
#     age_score = 5
#
#
# if education == 'دکترا' :
#     edu_comment = 'شما دارای مدرک طلایی برای مهاجرت هستید......'
#     edu_score = 30
# elif education == 'کارشناسی ارشد'  :
#     edu_comment = 'شما دارای مدرک خوبی برای مهاجرت هستید......'
#     edu_score = 20
# elif education == 'کارشناسی'  :
#     edu_comment = 'شما دارای مدرک خوبی به شرط سابقه کار برای مهاجرت هستید......'
#     edu_score = 15
# elif education == 'کاردانی' :
#     edu_comment = 'شما دارای مدرک پایینی هستید اما داشتن سابقه کار بالا به شما کمک میکند......'
#     edu_score = 10
# else:
#     edu_comment = 'شما دارای حداقل مدرک برای مهاجرت هستید. بنابراین سن و سابقه کار بالا به شما کمک میکند......'
#     edu_score = 5
#
#
# total_score = edu_score + age_score + sab_score
#
#
# print(f'نام و نام خانوادگی : {name}')
# print(f'سن : {age}')
# print(f'تحصیلات : {education}')
# print(f'آدرس محل سکونت : {address}')
# print(f'شغل : {job}')
# print(f'سابقه کار : {sabegheh_work}')
# print(f'کشور مقصد : {country_place}')
# print(f'وضعیت سن : {age_comment}')
# print(f'وضعیت تحصیلات : {edu_comment}')
# print(f'وضعیت سابقه کار : {sab_years}')
# print(f'امتیاز مهاجرتی شما از نمره 70 شد {total_score}')
# print('موفق و پیروز باشید......$$')



# print('*' * 50)
# print('🌟 سیستم مقایسه هوشمند کشورها برای مهاجرت (با وزن‌های اختصاصی)')
# print('*' * 50)
#
# # دریافت اطلاعات پایه کاربر
# name = input('نام و نام خانوادگی: ')
# age = int(input('سن: '))
# education = input('مدرک تحصیلی (دیپلم/کاردانی/کارشناسی/ارشد): ')
# experience = int(input('سال‌های سابقه کار (عدد): '))
#
# # --- گرفتن لیست کشورها از کاربر ---
# countries_input = input('کشورهای مد نظر خود را با کاما (,) جدا کنید (مثلاً کانادا, استرالیا, هلند, آلمان): ')
# countries = [c.strip() for c in countries_input.split(',')]
#
# scores = {}  # دیکشنری برای ذخیره امتیازها
#
# # --- حلقه برای محاسبه امتیاز هر کشور ---
# for country in countries:
#     # ۱. محاسبه امتیاز سن
#     if age < 18:
#         age_score = 0
#     elif 18 <= age <= 30:
#         age_score = 12
#     elif 31 <= age <= 45:
#         age_score = 8
#     else:
#         age_score = 5
#
#     # ۲. محاسبه امتیاز سابقه کار
#     if experience >= 5:
#         exp_score = 15
#     elif 3 <= experience < 5:
#         exp_score = 10
#     else:
#         exp_score = 5
#
#     # ۳. محاسبه امتیاز تحصیلات
#     if education == 'ارشد':
#         edu_score = 8
#     elif education == 'کارشناسی':
#         edu_score = 6
#     elif education == 'کاردانی':
#         edu_score = 4
#     else:
#         edu_score = 2
#
#     # امتیاز پایه
#     base_score = age_score + exp_score + edu_score
#
#     # --- اعمال امتیاز ویژه (وزن کشور) ---
#     bonus = 0
#     if country == 'فرانسه' and 30 <= age <= 50:
#         bonus = 2
#     elif country == 'سوئد' and age <= 30:
#         bonus = 1
#     elif country == 'ژاپن' and education == 'ارشد':
#         bonus = 5
#     elif country == 'نیوزلند' and experience >= 5:
#         bonus = 1
#     elif country == 'انگلستان' and age >= 31:
#         bonus = 4
#
#
#
#     total_score = base_score + bonus
#     scores[country] = total_score
#     print(f'   {country}: سن={age_score}, سابقه={exp_score}, تحصیلات={edu_score}, بونوس={bonus} → مجموع={total_score}')
#
# # --- پیدا کردن بهترین کشور ---
# best_country = max(scores, key=scores.get)
#
# # --- نمایش نتایج ---
# print('\n' + '-' * 50)
# print('📊 نتایج امتیازدهی نهایی (شامل امتیازات ویژه):')
# for country, score in scores.items():
#     print(f'   {country}: {score} امتیاز')
# print('-' * 50)
# print(f'🎯 بهترین کشور برای شما: {best_country} با {scores[best_country]} امتیاز!')
# print(f'🔥 {name} جان! همین الان شروع کن به یادگیری مهارت‌های مورد نیاز برای {best_country}.')
#
# print('*' * 50)



# print('Identify Card Hooshmand......')
# name_family = input('Enter your name: ')
# age = input('Enter your age: ')
# exprience = input('Enter your exprience: ')
# education = input('Enter your education: ')
# country = input('Enter your country: ')
#
# try:
#     age = int(age)
#     exprience = int(exprience)
# except:
#     age = 0
#     exprience = 0
#     print('Invalid Input, please enter again Age AND Exprience Correct...!!')
#
# countries = [c.strip() for c in country.split(',')]
# scores = {}
#
# for country_place in countries:
#     if age < 18:
#         age_score = 0
#     elif 18 <= age <= 30:
#         age_score = 12
#     elif 31 <= age <= 40:
#         age_score = 8
#     elif 41 <= age <= 60:
#         age_score = 6
#     else:
#         age_score = 2
#
#     if exprience >= 10:
#         exp_score = 30
#     elif 5 <= exprience < 10:
#         exp_score = 20
#     elif 3 <= exprience < 5:
#         exp_score = 10
#     else:
#         exp_score = 2
#
#     if education == 'doctora':
#         edu_score = 30
#     elif education == 'arshad':
#         edu_score = 20
#     elif education == 'karshenasi':
#         edu_score = 10
#     elif education == 'kardani':
#         edu_score = 5
#     else:
#         edu_score = 2
#
#     base_score = age_score + exp_score + edu_score
#
#     bonus = 0
#     if country_place == 'canada' and age >= 30:
#         bonus = 6
#     elif country_place == 'china' and exprience >= 10:
#         bonus = 5
#     elif country_place == 'japan' and education == 'arshad':
#         bonus = 6
#     elif country_place == 'india' and education == 'doctora':
#         bonus = 10
#     elif country_place == 'germany' and ( education == 'arshad' or education == 'doctora' ):
#         bonus = 8
#     elif country_place == 'germany' and 30 <= age <= 40:
#         bonus = 3
#
#     total_score = base_score + bonus
#     scores[country_place] = total_score
#     print(f'Country : {country_place}, Age : {age_score}, Exprience : {exp_score}, Education : {edu_score}, Bonus : {bonus}, Total Score : {total_score}')
#
# best_country = max(scores, key=scores.get)
# sorted_countries = sorted(scores.items(), key=lambda x: x[1], reverse=True)
# second_best_country = sorted_countries[1][0]
# print('Result Finally : ')
# for country, score in scores.items():
#     print(f'Country : {country} : To Emtiyase {score}')
# print('Because : ')
# print(f'Country : Best Bountry : {best_country} To Emtiyase {scores[best_country]} ')
# print(f'Then {name_family} your programming journey continues in  {best_country} ')
# print(f'Second Best Country : {second_best_country} To Emtiyaze {sorted_countries[1][1]}')
# print('END......$$$')



while True:  # حلقه‌ی تکرار
    print('\n' + '=' * 60)
    print('🌟 سیستم ارزیابی هوشمند مهاجرت (نسخه ۳.۰)')
    print('=' * 60)

    # دریافت اطلاعات
    name = input('نام و نام خانوادگی: ')
    age = int(input('سن: '))
    education = input('مدرک تحصیلی (doctora/arshad/karshenasi/kardani): ')
    experience = int(input('سال‌های سابقه کار: '))
    english_level = input('سطح زبان انگلیسی (مبتدی/متوسط/پیشرفته): ')

    # دیکشنری کشورها
    countries_data = {
        'canada': {'language': 'انگلیسی/فرانسوی', 'language_difficulty': 3, 'python_jobs': 9, 'culture_fit': 8, 'living_cost': 7, 'security': 9, 'weather': 4, 'immigration_score': 0},
        'germany': {'language': 'آلمانی', 'language_difficulty': 7, 'python_jobs': 8, 'culture_fit': 6, 'living_cost': 6, 'security': 9, 'weather': 5, 'immigration_score': 0},
        'japan': {'language': 'ژاپنی', 'language_difficulty': 9, 'python_jobs': 7, 'culture_fit': 5, 'living_cost': 8, 'security': 10, 'weather': 6, 'immigration_score': 0},
        'australia': {'language': 'انگلیسی', 'language_difficulty': 2, 'python_jobs': 8, 'culture_fit': 9, 'living_cost': 7, 'security': 9, 'weather': 9, 'immigration_score': 0}
    }

    # محاسبه امتیاز مهاجرتی
    for country in countries_data:
        if age < 18:
            age_score = 0
        elif 18 <= age <= 30:
            age_score = 12
        elif 31 <= age <= 40:
            age_score = 8
        elif 41 <= age <= 60:
            age_score = 6
        else:
            age_score = 2

        if experience >= 10:
            exp_score = 30
        elif 5 <= experience < 10:
            exp_score = 20
        elif 3 <= experience < 5:
            exp_score = 10
        else:
            exp_score = 2

        if education == 'doctora':
            edu_score = 30
        elif education == 'arshad':
            edu_score = 20
        elif education == 'karshenasi':
            edu_score = 10
        elif education == 'kardani':
            edu_score = 5
        else:
            edu_score = 2

        bonus = 0
        if country == 'canada' and age >= 30:
            bonus = 6
        elif country == 'canada' and english_level == 'پیشرفته':
            bonus = 5
        elif country == 'germany' and (education == 'arshad' or education == 'doctora'):
            bonus = 8
        elif country == 'australia' and english_level == 'پیشرفته':
            bonus = 5

        immigration_score = age_score + exp_score + edu_score + bonus
        countries_data[country]['immigration_score'] = immigration_score

    # محاسبه امتیاز نهایی
    final_scores = {}
    for country, data in countries_data.items():
        language_score = (10 - data['language_difficulty']) * 2
        job_score = data['python_jobs'] * 2
        culture_score = data['culture_fit'] * 2
        cost_score = data['living_cost']
        security_score = data['security']
        weather_score = data['weather']
        immigration_normalized = (data['immigration_score'] / 100) * 10

        total = (language_score + job_score + culture_score +
                 cost_score + security_score + weather_score +
                 immigration_normalized)
        final_scores[country] = round(total, 1)

    # نمایش نتایج
    best_country = max(final_scores, key=final_scores.get)

    print('\n' + '-' * 60)
    print('📊 نتایج ارزیابی هوشمند (از ۱۰۰):')
    print('-' * 60)

    for country, score in final_scores.items():
        data = countries_data[country]
        print(f'\n🌍 {country.upper()}')
        print(f'   📝 امتیاز مهاجرتی: {data["immigration_score"]}')
        print(f'   🗣️ زبان: {data["language"]} (سختی: {data["language_difficulty"]}/۱۰)')
        print(f'   💼 بازار کار پایتون: {data["python_jobs"]}/۱۰')
        print(f'   🌏 سازگاری فرهنگی: {data["culture_fit"]}/۱۰')
        print(f'   💰 هزینه زندگی: {data["living_cost"]}/۱۰')
        print(f'   🔒 امنیت: {data["security"]}/۱۰')
        print(f'   ☀️ آب و هوا: {data["weather"]}/۱۰')
        print(f'   ⭐ امتیاز نهایی: {score} از ۱۰۰')

    print('\n' + '=' * 60)
    print(f'🎯 بهترین کشور: {best_country.upper()} با {final_scores[best_country]} امتیاز!')
    print(f'🔥 {name} عزیز! {best_country.upper()} بهترین گزینه برای شماست.')
    print('=' * 60)

    # ذخیره در فایل
    with open('immigration_results.txt', 'w', encoding='utf-8') as file:
        file.write('=' * 50 + '\n')
        file.write('📋 گزارش ارزیابی مهاجرت\n')
        file.write('=' * 50 + '\n')
        file.write(f'👤 نام: {name}\n')
        file.write(f'📅 سن: {age} سال\n')
        file.write(f'🎓 مدرک: {education}\n')
        file.write(f'💼 سابقه کار: {experience} سال\n')
        file.write(f'🗣️ سطح زبان: {english_level}\n')
        file.write('-' * 50 + '\n')
        file.write('📊 امتیاز کشورها:\n')
        for country, score in final_scores.items():
            file.write(f'   {country.upper()}: {score} امتیاز\n')
        file.write('-' * 50 + '\n')
        file.write(f'🥇 بهترین کشور: {best_country.upper()}\n')
        file.write(f'⭐ امتیاز نهایی: {final_scores[best_country]}\n')
        file.write('=' * 50 + '\n')

    print('✅ نتایج در فایل immigration_results.txt ذخیره شد!')

    # پرسیدن برای اجرای مجدد
    again = input('\n🔄 آیا می‌خواهی دوباره اجرا کنی؟ (بله/خیر): ')
    if again != 'بله':
        print('👋 خداحافظ! موفق باشی!')
        break