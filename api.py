import status
from datetime import date
from tornado import web, escape, ioloop, httpclient, gen
from drone import Altimeter, Drone, Hexacopter, LightEmittingDiode


drone = Drone

class HexacopterHandler(web.RequestHandler):
    """docstring for HexacopterHandler."""
    SUPORTED_METHODS = ("GET", "PATCH")
    HEXACOPTER_ID = 1

    def get(self, id):
        if int(id) is not self.__class__.HEXACOPTER_ID:
            self.set_status(status.HTTP_404_NOT_FOUND)
            return
        print("I've started retrieving hexacopter's status" )
        hexacopter_status = drone.hexacopter.get_hexacopter_status()
        print("I've finished retrieving hexacopter's status")
        responce = {
        'speed': hexacopter_status.motor_speed,
        'turned_on': hexacopter_status.turned_on,
        }
        self.set_status(status.HTTP_200_OK)
        self.write(responce)
    def patch(self, id):
        if int(id) is not self.__class__.HEXACOPTER_ID:
            self.set_status(status.HTTP_404_NOT_FOUND)
            return
        request_data = escape.json_decode(self.request.body)
        if ('motor_speed' not in request_data.keys()) or \
            (request_data['motor_speed'] is not None):
            self.set_status(status.HTTP_400_BAD_REQUEST)
            return
        try:
            motor_speed = int(request_data['motor_speed'])
            print("I've started setting the hexacopter's motor speed")
            hexacopter_status = drone.hexacopter.set_motor_speed(motor_speed)
            print("I've finished setting the hexacopter's motor speed")
            responce = {
            'speed': hexacopter_status.motor_speed,
            'turned_on': hexacopter_status.turned_on,
            }
            self.set_status(status.HTTP_200_OK)
            self.write(responce)
        except ValueError as e:
            print("I've failed setting the hexacopter's motor speed")
            self.set_status(status.HTTP_400_BAD_REQUEST)
            responce = {
            'error': e.args[0]
            }
            self.write(responce)


class LedHandler(web.RequestHandler):
    SUPPORTED_METHODS = ("GET", "PATCH")

    def get(self, id):
        int_id = int(id)
        if int_id not in drone.leds.keys():
            self.status(status.HTTP_404_NOT_FOUND)
            return
        led = drone.leds[int_id]
        print("I've started retrieving {0}'s status".format(led.description))
        brightness_level = led.get_brightness_level()
        print("I've finished retrieving {0}'s status".format(led.description))
        responce = {
        'id': led.identifier,
        'description': led.description,
        'brightness_level': brightness_level,
        }
        self.set_status(status.HTTP_200_OK)
        self.write(responce)

    def patch(self, id):
        int_id = int(id)
        if int_id not in drone.leds.keys():
            self.set_status(status.HTTP_404_NOT_FOUND)
            return
        led = drone.leds[int_id]
        request_data = escape.json_decode(self.request.body)
        if ('brightness_level' not in request_data.keys()) or \
            (request_data['brightness_level'] is None):
            self.set_status(status.HTTP_400_BAD_REQUEST)
            return
        try:
            brightness_level = int(request_data['brightness_level'])
            print("I've started setting the {0}'s brightness level".format(led.description))
            led.set_brightness_level(brightness_level)
            print("I've finished setting the {0}'s brightness level".format(led.description))
            responce = {
            'id': led.identifier,
            'description': led.description,
            'brightness_level': brightness_level
            }
            self.set_status(status.HTTP_200_OK)
            self.write(responce)
        except ValueError as e:
            print("I've failed setting the {0}'s brightness level".format(led.description))
            self.set_status(status.HTTP_400_BAD_REQUEST)
            responce = {
            'error': e.args[0]
            }
            self.write(responce)


class AltimeterHandler(web.RequestHandler):
    SUPPORTED_METHODS = ("GET")
    ALTIMETER_ID = 1

    def get(self, id):
        if int(id) is not self.__class__.ALTIMETER_ID:
            self.set_status(status.HTTP_404_NOT_FOUND)
            return
        print("I've started retrieving the altitude")
        altimeter = drone.altimeter.get_altitude()
        print("I've finished retrieving the altitude")
        responce = {
        'altitude': altitude
        }
        self.set_status(status.HTTP_200_OK)
        self.write(responce)

application = web.Application([
    (r"/hexacopters/([0-9]+)", HexacopterHandler),
    (r"/leds/([0-9]+)", LedHandler),
    (r"/altimeters/([0-9]+)", AltimeterHandler),
], debug=True)

if __name__ == "__main__":
    port = 8888
    print("Listening at port {0}".format(port))
    application.listen(port)
    ioloop.IOLoop.instance().start()
