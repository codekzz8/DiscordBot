from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import Counter

groups1 = ['I1A1', 'I1A2', 'I1A3', 'I1A4', 'I1A5', 'I1A6',
           'I1B1', 'I1B2', 'I1B3', 'I1B4', 'I1B5',
           'I1E1', 'I1E2', 'I1E3', 'I1E4',
           'I1X', 'I1X1', 'I1X2', 'I1X3', 'I1X4', 'I1X5']
groups2 = ['I2A1', 'I2A2', 'I2A3', 'I2A4', 'I2A5', 'I2A6',
           'I2B1', 'I2B2', 'I2B3', 'I2B4', 'I2B5',
           'I2E1', 'I2E2', 'I2E3', 'I2E4',
           'I2X1', 'I2X2', 'I2X3', 'I2X4', 'I2X5', 'I2X6']
groups3 = ['I3A1', 'I3A2', 'I3A3', 'I3A4', 'I3A5', 'I3A6', 'I3A7',
           'I3B1', 'I3B2', 'I3B3', 'I3B4', 'I3B5', 'I3B6',
           'I3E1', 'I3E2',
           'I3X1', 'I3X2', 'I3X3', 'I3X4', 'I3X5']
saved_killers = []
saved_killer_images = []
saved_killer_urls = []


def get_groups():
    groups = []
    groups.extend(groups1)
    groups.extend(groups2)
    groups.extend(groups3)
    return groups


def get_timetable(group):
    if not (group in groups1 or group in groups2 or group in groups3):
        return 'Grupa nu exista!'

    url = "https://profs.info.uaic.ro/~orar/participanti/orar_" + group + ".html"
    html_code = urlopen(url).read().decode("utf-8")
    soup = BeautifulSoup(html_code, 'lxml')

    tabel_orar = soup.find('table')
    rows = tabel_orar.find_all('tr')[1:]
    coursesByDays = []

    for row in rows:
        try:
            data = row.find_all("b")
            day = data[0].get_text()
        except:
            pass
        try:
            columns = row.find_all("td")
            if columns[0].get_text().startswith(' '):
                coursesByDays.append((day, columns[0].get_text()[1:], columns[1].get_text()[1:],
                                      columns[2].find('a').get_text(), columns[3].get_text()[1:]))
        except:
            pass

    nrOfCourses = Counter(day[0] for day in coursesByDays)
    nrOfCoursesPerDay = []
    for elem in nrOfCourses.items():
        nrOfCoursesPerDay.append(elem[1])
    nrOfCoursesPerDay.sort()

    alreadyPrinted = {'Luni': False, 'Marti': False, 'Miercuri': False, 'Joi': False, 'Vineri': False}

    dataAsString = ''
    for day in coursesByDays:
        if not alreadyPrinted[day[0]]:
            dataAsString += day[0] + '\n'
            alreadyPrinted[day[0]] = True

        dataAsString += '{line:{fill}{align}{width}}'.format(line=f'\t\t{day[1]} - {day[2]} | {day[3]}',
                                                             fill=' ',
                                                             align='<',
                                                             width=40)
        dataAsString += ' | ' + day[4] + '\n'
    return dataAsString


def get_killers():
    url = "https://deadbydaylight.fandom.com/wiki/Killers#List_of_Killers"
    html_code = urlopen(url).read().decode("utf-8")
    soup = BeautifulSoup(html_code, 'lxml')

    killers_result = soup.find_all('div', attrs={'style': 'display: inline-block; text-align:center; margin: 10px'})
    # killers = tuples of strings where first element in the name of the killer
    #           and the second element is the in-game name of the killer
    killers = []
    killer_images = []
    killer_urls = []
    # killers and killer_images are ordered
    for killer in killers_result:
        killer_atr = [elem.strip() for elem in killer.text.split(' - ')]
        killers.append((killer_atr[0], killer_atr[1]))

    for killer in killers_result:
        killers_images = killer.findChildren('img')
        for image in killers_images:
            killer_images.append(image['data-src'])

    killer_urls = [killer.find_next('a')['href'] for killer in killers_result]

    return killers, killer_images, killer_urls


def get_info_about_killers(killers, killer_images):
    result = []

    for killer in killers:
        result.append(f'**{killer[0]} - {killer[1]}**\n{killer_images[killers.index((killer[0], killer[1]))]}\n')

    return result


def get_killer_info(url: str):
    url = f"https://deadbydaylight.fandom.com{url}"
    html_code = urlopen(url).read().decode("utf-8")
    soup = BeautifulSoup(html_code, 'lxml')

    first_paragraph = soup.find('span', attrs={'id': 'Overview'}).findNext('p')
    details_rs = first_paragraph.find_next_siblings('p')
    all_info = [first_paragraph.text]
    for tag in details_rs:
        if 'difficulty rating' in tag.text.lower():
            break
        all_info.append(tag.text)

    all_info.append(url)

    return all_info
