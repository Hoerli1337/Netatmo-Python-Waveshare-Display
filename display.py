#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, os, json, time, logging, traceback
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_epd import epd7in5b_V3
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("Waveshare epd7in5b_V3 Netatmo Display")

    epd = epd7in5b_V3.EPD()
    logging.info("init and Clear")
    epd.init()
    # Clear weg lassen, reduziert Arbeitszeit um 50%
    #epd.Clear()
    
    try:
        json_file = open("/home/pi/netatmo-api-python/weather.json", "r")
        weather_json = json_file.read()
        weather_json = json.loads(weather_json)
        json_file.close() 
    except:
        print("Die Datei konnste nicht eingelesen werden!")
        quit(1)
    
    # num to string
    #number = 20
    
    ##
    # Erfassen der Daten
    ##
    logging.info("Hole Daten aus der JSON-Datei ...")
   
    weather_stationname = weather_json['4']['mainstation']
    weather_sensor1_name = weather_json['4']['stationname']
    weather_sensor1_temp = str(weather_json['4']['Temperature'])
    weather_sensor1_humidity = str(weather_json['4']['Humidity'])
    weather_sensor1_ppm = str(weather_json['4']['CO2'])
    weather_sensor1_signal = str(weather_json['4']['rf_status'])
    weather_sensor1_accu = str(weather_json['4']['Temperature'])
    
    #Schlafzimmer
    weather_sensor2_name = weather_json['1']['stationname']
    weather_sensor2_temp = str(weather_json['1']['Temperature'])
    weather_sensor2_humidity = str(weather_json['1']['Humidity'])
    weather_sensor2_ppm = str(weather_json['1']['CO2'])
    weather_sensor2_signal = str(weather_json['1']['wifi_status'])
    
    weather_outdoor_name = weather_json['2']['stationname']
    weather_outdoor_temp = str(weather_json['2']['Temperature'])
    weather_outdoor_humidity = str(weather_json['2']['Humidity'])
    weather_outdoor_min = str(weather_json['2']['min_temp'])
    weather_outdoor_max = str(weather_json['2']['max_temp'])
    weather_outdoor_signal = str(weather_json['2']['rf_status'])
    weather_outdoor_accu = str(weather_json['2']['battery_percent'])
    
    weather_wind_name = weather_json['5']['stationname']
    weather_wind_current = str(weather_json['5']['WindStrength'])
    weather_wind_max = str(weather_json['5']['max_wind_str'])
    weather_wind_angle = int(weather_json['5']['WindAngle'])
    weather_wind_signal = str(weather_json['5']['rf_status'])
    weather_wind_accu = str(weather_json['5']['battery_percent'])
    
    weather_rain_name = weather_json['3']['stationname']
    weather_rain_hour = str(weather_json['3']['sum_rain_1'])
    weather_rain_today = str(weather_json['3']['sum_rain_24'])
    weather_rain_signal = str(weather_json['3']['rf_status'])
    weather_rain_accu = str(weather_json['3']['battery_percent'])
    
    last_update = weather_json['1']['When']
    
    ##
    # Schriftarten / Schriftgrößen setzen
    ##
    logging.info("Erstelle Schriftartengroessen ...")
    font72 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 72)
    font60 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 60)
    font50 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 50)
    font40 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 40)
    font32 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 32)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

# Drawing on the Vertical image
    logging.info("Erfasse nun die Daten fuer das Bild")
    Limage = Image.new('1', (epd.height, epd.width), 255)
    Limage_Other = Image.new('1', (epd.height, epd.width), 255)
    draw_Himage = ImageDraw.Draw(Limage)
    draw_Himage_Other = ImageDraw.Draw(Limage_Other)

    ##
    # Grundaufbau des Gerüsts (Linien) zeichnen
    ##
    logging.info("Zeichne das Grundgeruest ...")
    
    # Header-Linie
    draw_Himage.line((0, 60, 528, 60), fill = 0)
    # Trenner für Innen-Temperaturen Vertikale Linie
    draw_Himage.line((260, 60, 260, 280), fill = 0)
    # Horizontale Linie zwischen Innen und Außentemperatur 
    draw_Himage.line((0, 280, 528, 280), fill = 0)
    # Horizontale Linie zwischen Außentemperatur und Wind 
    draw_Himage.line((0, 490, 528, 490), fill = 0)
    # Horizontale Linie zwischen Wind und Regen
    draw_Himage.line((0, 680, 528, 680), fill = 0)
    # Letzte Horizontale Linie zwischen Regen und Update
    draw_Himage.line((0, 855, 528, 855), fill = 0)

# Titel - Stationname zeichnen
    draw_Himage.text((50, 0), weather_stationname, font = font50, fill = 0)

# Wohnzimmer-Temperatur - Angaben des 2. Innensensors zeichnen
    draw_Himage.text((5, 70), weather_sensor1_name, font = font24, fill = 0)
    draw_Himage.text((20, 90), weather_sensor1_temp+'°C', font = font72, fill = 0)
    draw_Himage.text((20, 170), weather_sensor1_humidity+'%', font = font32, fill = 0)
    draw_Himage.text((20, 200), weather_sensor1_ppm+'ppm', font = font32, fill = 0)
    draw_Himage.text((160, 240), 'Signal: '+weather_sensor1_signal+'%', font = font18, fill = 0)
    draw_Himage.text((160, 260), 'Akku: '+weather_sensor1_accu+'%', font = font18, fill = 0)

# Schlafzimmer-Temperatur - Hauptstation zeichnen
    draw_Himage.text((270, 70), weather_sensor2_name, font = font24, fill = 0)
    draw_Himage.text((280, 90), weather_sensor2_temp+' °C', font = font72, fill = 0)
    draw_Himage.text((280, 170), weather_sensor2_humidity+'%', font = font32, fill = 0)
    draw_Himage.text((280, 200), weather_sensor2_ppm+'ppm', font = font32, fill = 0)
    draw_Himage.text((430, 240), 'Signal: '+weather_sensor2_signal+ '%', font = font18, fill = 0)


# Außentemperatur - Angaben zur Außentemperatur zeichnen
    draw_Himage.text((5, 290), weather_outdoor_name, font = font24, fill = 0)
    draw_Himage.text((20, 320), weather_outdoor_temp+' °C', font = font72, fill = 0)
    draw_Himage.text((50, 400), weather_outdoor_humidity+'%', font = font60, fill = 0)
#    draw_Himage.text((320, 310), 'WETTER', font = font40, fill = 0)
#    draw_Himage.text((320, 355), 'SYMBOL', font = font40, fill = 0)
    draw_Himage.text((220, 405), 'Min. '+weather_outdoor_min+' °C', font = font32, fill = 0)
    draw_Himage.text((220, 435), 'Max. '+weather_outdoor_max+' °C', font = font32, fill = 0)
    draw_Himage.text((430, 450), 'Signal: '+weather_outdoor_signal+'%', font = font18, fill = 0)
    draw_Himage.text((430, 470), 'Akku: '+weather_outdoor_accu+'%', font = font18, fill = 0)

# Windmesser - Angaben zum Wind zeichnen
    draw_Himage.text((5, 500), weather_wind_name, font = font24, fill = 0)
    draw_Himage.text((20, 540), weather_wind_current+'km/h', font = font60, fill = 0)
    draw_Himage.text((20, 600), weather_wind_max+'km/h', font = font60, fill = 0)

# Windrichtung-Pfeil
    logging.info("Windrichtung malen ...")
    bmp = Image.open(os.path.join(picdir, 'Arrow.bmp'))
    angle = weather_wind_angle
    out = bmp.rotate(angle)
    out.save('Arrow-rotate.bmp')
    out.paste(out, (320,500))

# Windrichtung anzeigen
#    Arrow = Image.new('1', (epd.height, epd.width), 255)
#    bmp = Image.open(os.path.join('rotate-arrow.bmp'))
#    Arrow.paste(bmp, (320,500))
   # epd.display(epd.getbuffer(Arrow))
    
    
# Windrichtrung-Text
#    draw_Himage.text((320, 500), 'WIND', font = font40, fill = 0)
#    draw_Himage.text((320, 540), 'RICHTUNG', font = font40, fill = 0)


# Info
    draw_Himage.text((430, 630), 'Signal: '+weather_wind_signal+'%', font = font18, fill = 0)
    draw_Himage.text((430, 650), 'Akku: '+weather_wind_accu+'%', font = font18, fill = 0)

# Regen - Angaben zum Regenmesser zeichnen
    logging.info("Regeninfos malen ...")
    draw_Himage.text((5, 690), weather_rain_name, font = font24, fill = 0)
    draw_Himage.text((20, 730), 'Letzte', font = font18, fill = 0)
    draw_Himage.text((20, 750), 'Stunde', font = font18, fill = 0)
    draw_Himage.text((100, 720), weather_rain_hour+'mm', font = font60, fill = 0)
    draw_Himage.text((20, 800), 'Heute:', font = font18, fill = 0)
    draw_Himage.text((100, 780), weather_rain_today+'mm', font = font60, fill = 0)
    draw_Himage.text((430, 810), 'Signal: '+weather_rain_signal+'%', font = font18, fill = 0)
    draw_Himage.text((430, 830), 'Akku: '+weather_rain_accu+'%', font = font18, fill = 0)

# Letztes Update laut Netatmo-API der Wetterstation
    draw_Himage.text((10, 860), 'Letztes Update: '+last_update, font = font18, fill = 0)

    logging.info("Ab zum rendern ... das dauert ...")

# Bild rendern lassen ...
# Das Display kann nur zwei buffer-Dinge annehmen. Drei gehen nicht. Das zweite ist aktuell irgendwie ungenutzt
    epd.display(epd.getbuffer(Limage), epd.getbuffer(Limage_Other))
except Exception:
    print("#------")
    traceback.print_exc()
