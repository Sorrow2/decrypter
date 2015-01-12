# coding=utf-8
__author__ = 'm_messiah'


class Coordinates(object):
    def __init__(self, coords):
        self.type_coords = ["BadInput", "DegDec", "MinDec", "DMS"]
        self.type, self.coords = self.parse(coords)
        self.all_coords = {"DegDec": "", "MinDec": "", "DMS": ""}
        self.convert()

    def parse(self, coords):
        type_coord = 0
        result = [0, [[], []]]
        for i, lat in enumerate(coords):
            lat = lat.split()
            count = len(lat)
            if count > type_coord:
                type_coord = count
            result[1][i] = lat
        result[0] = self.type_coords[type_coord]
        return result

    def deg_dec2min_dec(self):
        result = []
        for i, lat in enumerate(self.coords):
            lat = float(lat[0])
            d = int(lat)
            m = round(abs((lat - d) * 60), 3)
            result.append("%s %s" % (abs(d), m))
        return ", ".join(result)

    def deg_dec2dms(self):
        result = []
        for i, lat in enumerate(self.coords):
            lat = float(lat[0])
            d = int(lat)
            ms = abs((lat - d) * 60)
            m = int(ms)
            s = round((ms - m) * 60, 2)
            result.append("%s %s %s" % (abs(d), m, s))
        return ", ".join(result)

    def min_dec2deg_dec(self):
        result = []
        for lat in self.coords:
            d, m = map(float, lat[:2])
            result.append(str(round(d + m / 60 * (-1 if d < 0 else 1), 6)))
        return ", ".join(result)

    def min_dec2dms(self):
        result = []
        for lat in self.coords:
            d, ms = map(float, lat[:2])
            m = int(ms)
            s = round((ms - m) * 60, 2)
            result.append("%s %s %s" % (int(d), m, s))
        return ", ".join(result)

    def dms2deg_dec(self):
        result = []
        for lat in self.coords:
            d, m, s = map(float, lat[:3])
            result.append(str(round(d + (m * 60 + s)
                                    / 3600 * (-1 if d < 0 else 1), 6)))
        return ", ".join(result)

    def dms2min_dec(self):
        result = []
        for lat in self.coords:
            d, m, s = map(float, lat[:3])
            result.append("%s %s" % (int(d), round(m + s / 60, 3)))
        return ", ".join(result)

    def dms(self, i):
        d, m, s = self.coords[i][:3]
        s = round(float(s), 2)
        return "%s %s %s" % (d, m, s)

    def min_dec(self, i):
        d, m = self.coords[i][:2]
        m = round(float(m), 3)
        return "%s %s" % (d, m)

    def convert(self):
        if self.type == "DMS":
            self.all_coords["DMS"] = "%s, %s" % (self.dms(0), self.dms(1))
            self.all_coords["MinDec"] = self.dms2min_dec()
            self.all_coords["DegDec"] = self.dms2deg_dec()
        elif self.type == "MinDec":
            self.all_coords["MinDec"] = "%s, %s" % (self.min_dec(0),
                                                    self.min_dec(1))
            self.all_coords["DMS"] = self.min_dec2dms()
            self.all_coords["DegDec"] = self.min_dec2deg_dec()
        elif self.type == "DegDec":
            self.all_coords["DegDec"] = "%s, %s" % tuple(
                map(lambda x: round(float(x[0]), 6), self.coords)
            )
            self.all_coords["MinDec"] = self.deg_dec2min_dec()
            self.all_coords["DMS"] = self.deg_dec2dms()
        else:
            self.all_coords["BadInput"] = 0

        dms = self.all_coords["DMS"].split(",")
        link = [u"<a href=\"http://google.com/maps/place/"]
        coords = []
        for cor in dms:
            d, m, s = cor.strip().split()[:3]
            coords.append(u"%s°%s'%s%%22" % (d, m, s))

        link.append(u"+".join(coords))
        link.append(u"\" class='btn' target='_blank'>GoogleMaps</a>")
        self.all_coords["~ Maps"] = u"".join(link)

    def __str__(self):
        res = ["------"]
        for k, v in self.all_coords.items():
            res.append("%s : %s" % (k, v))
        return "\n".join(res)


if __name__ == "__main__":
    from sys import argv

    print(Coordinates((argv[1], argv[2])))
