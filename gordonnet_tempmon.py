#!/usr/bin/env python
import LCD1602
import time
import datetime
import smbus
import Adafruit_DHT as DHT
import RPi.GPIO as GPIO

strdoorstatus = 'X'
maxtemp = 24
maxhumidity = 24
webpage = 1

Sensor = 11     # address of screen on i2c bus
humiture = 17   # temp / humidity sensor

ReedPin = 12    # magnetic door switch

BuzzerPin = 16  # buzzer

# ------------------
led1 = 15
led2 = 13

pins = [led1, led2]
#-------------------


#----------------------------------------------------------

#----------------------------------------------------------
def init():

    #print ('Setting up, please wait...')
    
    LCD_Width = 16
    # Configure LCD
    LCD1602.init(0x27, 1)   # init(slave address, background light)
    LCD1602.write(0, 0, 'Greetings!!')
    LCD1602.write(0, 1, 'from GordonNet Temp Monitor')
    time.sleep(5)
    LCD1602.clear()


# -------------------------------------------------------------
# Main Routine
# --------------------------------------------------------------
def main():
    GPIO.setmode(GPIO.BOARD)        # Numbers GPIOs by physical location
    GPIO.setwarnings(False)

    GPIO.setup(ReedPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set BtnPin's mode is input, and pull up to high level(3.3V)
    GPIO.add_event_detect(ReedPin, GPIO.BOTH, callback=detect, bouncetime=200)

    GPIO.setup(BuzzerPin, GPIO.OUT, initial=GPIO.LOW)   #Default State Off.
    

    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)   # Set all pins' mode is output

    strdoorstatus = ' '

    # Initialise display
    init()
    
    #buzzertest()
    Led(0)
    
    #Start main Routine
    while True:
        localtime = time.asctime( time.localtime(time.time()) )
        strlocaltime = 'Local Time: ', localtime
        

        # -------------------------------------------------------------------------------
        #check door sensor status
        # -------------------------------------------------------------------------------
        Led(GPIO.input(ReedPin))
    

        # --------------------------------------------------------------------------------
        # Temperature Sensor
        # --------------------------------------------------------------------------------
        humidity, temperature = DHT.read_retry(Sensor, humiture)    #built in 2sec delay
        
        if humidity is not None and temperature is not None:
            #strtemp = str(Temp={0:0.1f}*C).format(temperature)
            
            temperature = str(temperature)
            humidity = str(humidity)
            strdoorstatus = str(strdoorstatus)


            # ------------------------
            #strtemp = 'Temp: ' + str(temperature) + ' ' + chr(223) + 'C' #add degree symbol
            #strhumidity = 'Humidity: ' + str(humidity) + '%'
            # ------------------------
            
            
            # ----------------------------------------------------------------------
            # print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
            # strdisplay = str('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
            # print strdisplay #print on console window

            ###########################################################
            #
            #
            displayonlcd(temperature, humidity, strdoorstatus)  
            
            if webpage ==1:
                updatewebpage(temperature, humidity, strdoorstatus)
            #
            ###########################################################

        
        else:
            print ('Failed to get reading')

            #tmp = greetings
            #for i in range(0, len(greetings)):
                #LCD1602.write(1, 1, strtemp)
                #tmp = tmp[1:]
                #time.sleep(0.8)
                #LCD1602.clear()

# ---------------------------------------------------------------------
# Write to LCD screen
# ---------------------------------------------------------------------
def displayonlcd(temperature, humidity, strdoorstatus):
    # LCD1602.write(0, 0, 'ABCDEFGHIJKLMNOPQURSTUVWXYZ')
    # LCD1602.write(1, 1, 'abcdefghighijklmnopqurstuvwxyz')
    #
    line1 = 'Temp: ' + str(temperature) + ' ' + chr(223) + 'C' + ' ' + str(strdoorstatus)#add degree symbol
    line2 = 'Humidity: ' + str(humidity) + '%'
    #      
    #
    LCD1602.write(0, 0, line1)      #line 1 
    LCD1602.write(0, 1, line2)      #line 2
    # ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Print to Console
# ---------------------------------------------------------------------
def Print(x):
    if x == 0:
        print ('    ***********************************')
        print ('    *   Door Closed!   *')
        print ('    ***********************************')
        strdoorstatus = str('Closed')


    if x == 1:
        print ('    ***********************************')
        print ('    *   Door Open!   *') 
        print ('    ***********************************')
        strdoorstatus = str('Open')

   
# ---------------------------------------------------------------------
# Buzzer Test
# ---------------------------------------------------------------------
def buzzertest():
    GPIO.output(BuzzerPin, GPIO.HIGH)
    time.sleep(.1)

# ---------------------------------------------------------------------
# Check Temp.
# --------------------------------------------------------------------
def checktemp(temperature):
    if temperature > maxtemp:
        #flash light
        GPIO.output(led1, 1)
        time.sleep(1)
        GPIO.output(led1, 0)
        time.sleep(1)
        
    else:
        #do nothing 
        print ("ok")
    

#----------------------------------------------------------------------
# Update Web Page.
# ---------------------------------------------------------------------
def updatewebpage(temperature,humidity,strdoorstatus):
    #filename = "/var/www/html/index.html"
    filename = "/home/pi/gordonnet/tempmon/www/index.html"
    f = open(filename,"w") 
    localtime = time.asctime( time.localtime(time.time()) )
    message = """<!DOCTYPE HTML><html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta http-equiv="refresh" content="10">
            <!-- JQuery -->
            <script src="scripts/jquery/jquery.min.js" type="text/javascript"></script>
            <!-- Bootstrap core JavaScript -->
            <script src="scripts/twitter-bootstrap/js/bootstrap.bundle.min.js" type="text/javascript"></script>
            <!-- Bootstrap core CSS -->
            <link href="scripts/twitter-bootstrap/css/bootstrap.min.css" rel="stylesheet">
        <!-- Popper -->
            <!-- <script src="scripts/popper.js/umd/popper.min.js"></script> -->
            <!-- GordonNet Theme-->
         <link href="gordonnet/css/gordonnet-theme.css" rel="stylesheet">
            <!-- Animate -->
            <link href="css/animate/animate.min.css" rel="stylesheet">

            <!-- Font Awesome-->
            <script src="scripts/font-awesome/js/all.min.js"></script>
            <link href="scripts/font-awesome/css/all.min.css" rel="stylesheet">
  
        <style>
                html {
                font-family: Roboto;
                display: inline-block;
                margin: 30px auto;
                text-align: center;
             }
                h2 { font-size: 3.0rem; }
                p { font-size: 3.0rem; }
                .units { font-size: 1.5rem; }
                .dht-labels{
                font-size: 1.5rem;
                vertical-align:middle;
                padding-bottom: 20px;
                }
        </style>
        <Title>RP-TempMon</Title>

    </head>
    <body>
        <p>
                <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
                <span class="dht-labels">Temperature:</span> 
                <span>"""+str(temperature)+"""</span>
                <sup class="units">&deg;C</sup>
        </p>
        <p>
                <i class="fas fa-tint" style="color:#00add6;"></i> 
                <span class="dht-labels">Humidity:</span>
                <span>"""+str(humidity)+"""</span>
                <sup class="units">%</sup>
        </p>
        <p>
                <i class="fas fa-door-closed" style="color:#00add6;"></i> 
                <span class="dht-labels">Door:</span>
                <span>"""+str(strdoorstatus)+"""</span>
        </p>

    </body>
    </html>"""

    f.write(message)
    f.close()

# ---------------------------------------------------------------------
# Morse Code !
# ---------------------------------------------------------------------
def morsecode():
    #Dot Dot Dot
    GPIO.output(BuzzerPin, GPIO.HIGH)
    time.sleep(.1)
    GPIO.output(BuzzerPin, GPIO.LOW)
    time.sleep(.1)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    time.sleep(.1)
    GPIO.output(BuzzerPin, GPIO.LOW)
    time.sleep(.1)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    time.sleep(.1)

    #Dash Dash Dash
    GPIO.output(BuzzerPin, GPIO.LOW)
    time.sleep(.2)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    time.sleep(.2)
    GPIO.output(BuzzerPin, GPIO.LOW)
    time.sleep(.2)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    time.sleep(.2)
    GPIO.output(BuzzerPin, GPIO.LOW)
    time.sleep(.2)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    time.sleep(.2)
    GPIO.output(BuzzerPin, GPIO.LOW)
    time.sleep(.2)

    #Dot Dot Dot
    GPIO.output(BuzzerPin, GPIO.HIGH)
    time.sleep(.1)
    GPIO.output(BuzzerPin, GPIO.LOW)
    time.sleep(.1)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    time.sleep(.1)
    GPIO.output(BuzzerPin, GPIO.LOW)
    time.sleep(.1)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    time.sleep(.1)


# ---------------------------------------------------------------------
# Write to LCD screen
# ---------------------------------------------------------------------
def Led(x):
    #RED
    if x == 0:
        GPIO.output(led1, 1)
        GPIO.output(led2, 0)
        morsecode()
        strdoorstatus = str('Closed')
        
    
    #GREEN
    if x == 1:
        GPIO.output(led1, 0)
        GPIO.output(led2, 1)
        strdoorstatus = str('Open')
        

# ---------------------------------------------------------------------
# Detect Change
# ---------------------------------------------------------------------
def detect(chn):
    Led(GPIO.input(ReedPin))
    Print(GPIO.input(ReedPin))
    
    x = GPIO.input(ReedPin)
    if x == 0:
        strdoorstatus = 'Closed'
    if x == 1:
        strdoorstatus = 'Open'
# ---------------------------------------------------------------------
# Exit
# ---------------------------------------------------------------------
def destroy():
    GPIO.output(BuzzerPin, GPIO.LOW)    #Turn off buzzer

    for pin in pins:
        GPIO.output(pin, GPIO.LOW)      #Turn off all leds
    
    
    GPIO.cleanup()  
    LCD1602.clear()

if __name__ == "__main__":
    try:
        main()
        while True:
            pass
    except KeyboardInterrupt:
        destroy()
