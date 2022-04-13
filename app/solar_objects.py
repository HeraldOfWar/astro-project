import sqlite3

DATA = sqlite3.connect('solar_objects_db.db').cursor().execute("""SELECT * FROM SolarObjects""")
DATA = [list(i) for i in DATA] # загружаем все данные из БД
SOLAR_IMAGES = ['images/sun.png', 'images/mercury.png', 'images/venerus.png', 'images/earth.png',
                'images/mars.png', 'images/jupiter.png', 'images/saturn.png', 'images/uran.png',
                'images/neptun.png', 'images/pluton.png']   # список изображений
SOLAR_OBJECTS, CLICKED_SOLAR_OBJECT, START_POSITION = [], None, []  # необходимые константы


class SolarObject:

    def __init__(self, objName, view, image, *args):
        self.objName = objName
        self.view = view
        self.image = image
        self.info = args[0]
        self.name = self.info[1]

    # возвращает основную информацию об объекте Солнечной системы
    def to_main_info(self):
        main_data = [i for i in self.info[2:11]]
        return f'Тип: {main_data[0]}\n\nРасстояние от Солнца: {main_data[1]} а.е.\n\n' \
               f'Период обращения (в земных годах): {main_data[2]}\n\nЭксцентриситет: {main_data[3]}\n\n' \
               f'Орбитальная скорость: {main_data[4]} км/с\n\nПлотность: {main_data[5]}x10^3 кг/м^3\n\n' \
               f'Ускорение свободного падения: {main_data[6]} м/с^2\n\n' \
               f'Масса (в массах Земли): {main_data[7]}\n\nКоличество спутников: {main_data[8]}\n\n' \

    # возвращает второстепенную информацию об объекте Солнечной системы
    def to_other_info(self):
        d, atmosphere, description = 0, [], []
        for i in range(1, len(self.info[11])):
            if len(self.info[11]) < 124:
                atmosphere.append(self.info[11])
                break
            if i % 124 == 0:
                atmosphere.append(self.info[11][d:i + 1])
                d = i + 1
                if len(self.info[11][i + 1:]) < 124:
                    atmosphere.append(self.info[11][i + 1:])
                    break
        d = 0
        for i in range(1, len(self.info[12])):
            if len(self.info[12]) < 124:
                description.append(self.info[12].strip())
                break
            if i % 124 == 0:
                description.append(self.info[12][d:i + 1].strip())
                d = i + 1
                if len(self.info[12][i + 1:]) < 124:
                    description.append(self.info[12][i + 1:].strip())
                    break
        atmosphere, description = '\n'.join(atmosphere), '\n'.join(description)
        return f'Состав атмосферы:\n{atmosphere}\n\nОписание:\n{description}'


# создаём объекты Солнечной системы
for i in range(10):
    SOLAR_OBJECTS.append(SolarObject(None, None, SOLAR_IMAGES[i], DATA[i]))

