# دیتاست کامل کشورها (نمونه - می‌تونی کامل‌ترش کنی)
COUNTRIES_DATA = {
    'canada': {
        'name': 'Canada',
        'capital': 'Ottawa',
        'region': 'Americas',
        'population': 38246108,
        'area': 9984670,
        'languages': ['English', 'French'],
        'currency': 'Canadian Dollar (CAD)',
        'flag': '🇨🇦',
        'immigration_score': 9,
    },
    'australia': {
        'name': 'Australia',
        'capital': 'Canberra',
        'region': 'Oceania',
        'population': 26439111,
        'area': 7692024,
        'languages': ['English'],
        'currency': 'Australian Dollar (AUD)',
        'flag': '🇦🇺',
        'immigration_score': 10,
    },
    'germany': {
        'name': 'Germany',
        'capital': 'Berlin',
        'region': 'Europe',
        'population': 83240525,
        'area': 357022,
        'languages': ['German'],
        'currency': 'Euro (EUR)',
        'flag': '🇩🇪',
        'immigration_score': 7,
    },
    'japan': {
        'name': 'Japan',
        'capital': 'Tokyo',
        'region': 'Asia',
        'population': 125681593,
        'area': 377975,
        'languages': ['Japanese'],
        'currency': 'Yen (JPY)',
        'flag': '🇯🇵',
        'immigration_score': 5,
    },
    'netherlands': {
        'name': 'Netherlands',
        'capital': 'Amsterdam',
        'region': 'Europe',
        'population': 17646358,
        'area': 41850,
        'languages': ['Dutch', 'English'],
        'currency': 'Euro (EUR)',
        'flag': '🇳🇱',
        'immigration_score': 8,
    },
    'sweden': {
        'name': 'Sweden',
        'capital': 'Stockholm',
        'region': 'Europe',
        'population': 10415811,
        'area': 450295,
        'languages': ['Swedish', 'English'],
        'currency': 'Swedish Krona (SEK)',
        'flag': '🇸🇪',
        'immigration_score': 9,
    },
    'norway': {
        'name': 'Norway',
        'capital': 'Oslo',
        'region': 'Europe',
        'population': 5457127,
        'area': 385207,
        'languages': ['Norwegian', 'English'],
        'currency': 'Norwegian Krone (NOK)',
        'flag': '🇳🇴',
        'immigration_score': 9,
    },
    'newzealand': {
        'name': 'New Zealand',
        'capital': 'Wellington',
        'region': 'Oceania',
        'population': 5124100,
        'area': 268021,
        'languages': ['English', 'Maori'],
        'currency': 'New Zealand Dollar (NZD)',
        'flag': '🇳🇿',
        'immigration_score': 9,
    },
}


def search_country(name):
    """Search for a country in our dataset"""
    name = name.lower().strip()

    if name in COUNTRIES_DATA:
        return COUNTRIES_DATA[name]

    # جستجوی جزئی
    for key, data in COUNTRIES_DATA.items():
        if name in key or name in data['name'].lower():
            return data

    return None


def show_country(country):
    """Display country information"""
    if not country:
        print('❌ Country not found!')
        return

    print('\n' + '=' * 60)
    print(f'{country["flag"]}  {country["name"].upper()}')
    print('=' * 60)
    print(f'🏛️  Capital: {country["capital"]}')
    print(f'🌍 Region: {country["region"]}')
    print(f'👥 Population: {country["population"]:,}')
    print(f'📐 Area: {country["area"]:,} km²')
    print(f'🗣️  Languages: {", ".join(country["languages"])}')
    print(f'💰 Currency: {country["currency"]}')
    print(f'⭐ Immigration Score: {country["immigration_score"]}/10')
    print('=' * 60)


def compare_countries(c1, c2):
    """Compare two countries"""
    if not c1 or not c2:
        print('❌ One or both countries not found!')
        return

    print('\n' + '=' * 60)
    print(f'📊 {c1["name"]} vs {c2["name"]}')
    print('=' * 60)

    print(f'\n👥 Population:')
    print(f'   {c1["flag"]} {c1["name"]}: {c1["population"]:,}')
    print(f'   {c2["flag"]} {c2["name"]}: {c2["population"]:,}')

    print(f'\n📐 Area:')
    print(f'   {c1["flag"]} {c1["name"]}: {c1["area"]:,} km²')
    print(f'   {c2["flag"]} {c2["name"]}: {c2["area"]:,} km²')

    print(f'\n⭐ Immigration Score:')
    print(f'   {c1["flag"]} {c1["name"]}: {c1["immigration_score"]}/10')
    print(f'   {c2["flag"]} {c2["name"]}: {c2["immigration_score"]}/10')

    if c1['immigration_score'] > c2['immigration_score']:
        print(f'\n🏆 {c1["name"]} is better for immigration!')
    elif c2['immigration_score'] > c1['immigration_score']:
        print(f'\n🏆 {c2["name"]} is better for immigration!')
    else:
        print(f'\n🤝 Both are equal!')


def list_all_countries():
    """List all countries in dataset"""
    print('\n' + '=' * 60)
    print(f'🌍 Available Countries ({len(COUNTRIES_DATA)})')
    print('=' * 60)

    for key, data in COUNTRIES_DATA.items():
        print(
            f'{data["flag"]}  {data["name"]:15} | Region: {data["region"]:10} | Score: {data["immigration_score"]}/10')


def main():
    """Main program"""
    print('=' * 60)
    print('🌍 Country Info (Offline Dataset)')
    print('=' * 60)

    while True:
        print('\n📋 Menu:')
        print('1. 🔍 Search country')
        print('2. 📋 List all countries')
        print('3. 📊 Compare two countries')
        print('4. 🚪 Quit')

        choice = input('\nEnter choice (1-4): ').strip()

        if choice == '1':
            name = input('Enter country name: ').strip()
            country = search_country(name)
            show_country(country)

        elif choice == '2':
            list_all_countries()

        elif choice == '3':
            c1_name = input('First country: ').strip()
            c2_name = input('Second country: ').strip()
            c1 = search_country(c1_name)
            c2 = search_country(c2_name)
            compare_countries(c1, c2)

        elif choice == '4':
            print('👋 Goodbye!')
            break
        else:
            print('❌ Invalid choice!')


if __name__ == '__main__':
    main()