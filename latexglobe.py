####
# Create LaTeX pstricks code to draw a globe, with meridians and parallels
# pstricks may work only if you use 'dvips' on the .dvi file, and then 'ps2pdf' on the .ps file.
#
# Axis of globe is specified with:
#  -- a tilt (0:North is at top, 90:North is in front center of globe, -90:North is back center)
#  -- a rotation (rotates at the end the final picture)
####

NORTH = (90, 0)
SOUTH = (-90, 0)
EARTH_INCLINATION = 23.4

# constants to specify which part of the parallels or meridians to draw
VISIBLE = 1
INVISIBLE = 2
ALL = VISIBLE + INVISIBLE

# Functions are :
### OUTPUT DOCUMENT LATEX CODE ###
#   documentStart()
#   pictureStart(unit='10mm', size='(-11, -11)(11, 11)', crop=True)
#   pictureEnd()
#   documentEnd()

### OUTPUT GLOBE LATEX CODE ###
#   meridian(longitude=0, tilt=DEFAULT_TILT, rot=DEFAULT_ROT, radius=1, show=ALL, comment='')
#   parallel(latitude=0, tilt=DEFAULT_TILT, rot=DEFAULT_ROT, radius=1, show=ALL, comment='')
#   equator(tilt=DEFAULT_TILT, rot=DEFAULT_ROT, radius=1, show=ALL)
#   globe(tilt=DEFAULT_TILT, rot=DEFAULT_ROT, radius=1, hollow=False, diff_longitude=30, diff_latitude=15, longitude_start=0)
#   shortPathEllipse(latitude1, longitude1, latitude2, longitude2, tilt=DEFAULT_TILT, radius=1, rot=0, show=ALL, onlyPath=True, drawPoints=True)

### COMPUTE TILT AND ROT FROM ROTATIONS AROUND OX-OY-OZ AXIS, OR FROM POLAR COORDINATES OF NORTH POLE ###
### (NO OZ ROTATION FIRST, AS IT IS THE SAME AS SHIFTING THE LONGITUDES AFTERWARDS)
#   tiltRotOxOy(angleOx, angleOy)
#   tiltRotOyOx(angleOy, angleOx)
#   tiltRotOxOz(angleOx, angleOz)
#   tiltRotOyOz(angleOy, angleOz)
#   tiltRotPolar(theta, phi)

### OTHER COMPUTING FUNCTIONS ###
#   getXYZPosition(latitude, longitude, tilt=DEFAULT_TILT, radius=1)
#   getPointPosition(latitude, longitude, tilt=DEFAULT_TILT, radius=1)
#   isPointVisible(latitude, longitude, tilt=DEFAULT_TILT)

### TEST OUTPUT ###
#   test()


from math import sin, cos, tan, atan, atan2, acos, asin, pi, sqrt

# Function to test output and to give some examples of usage
def test():
    documentStart()

    print('\n\n\n%%%%%  lots of differents axis  %%%%%')
    pictureStart(unit='8mm', size='(-1,0)(24,30)', crop=False)
    for x in range(8):
        az = -30 + x * 30
        for y in range(9):
          ax = -30 + y * 30
          (tilt, rot) = tiltRotOxOz(ax, az)
          print('\\rput(%d, %d){ %s ax=%d, az=%d' % (x*3, y*3, '%', ax, az))
          print('\\rput[t](0,%.1f){\\tiny ox=%d,oz=%d }' % (-1.1, ax, az))
          print('\\rput[t](0,%.1f){\\tiny t=%.2f,r=%.2f }' % (-1.3, tilt, rot))
          print('% tilt rot:', tilt, rot)
          globe(tilt, rot, hollow=True, longitude_start = 10)
          print('}')
    pictureEnd()

    print('\\newpage')
    print('\\begin{center}')

    print('\n\n\n%%%%%  Standard globe with labels  %%%%%')
    pictureStart(unit='50mm', size='(-1,-1)(1,1.2)', crop=False)
    rot = -EARTH_INCLINATION
    tilt = 28
    mmPerPt = .352778
    axeWidth = 6 / 2 * mmPerPt / 50
    print('  \\psline[linewidth=6pt,linecolor=darkgray](%.3f;%.3f)(%.3f;%.3f)' % (1, 90+rot+180, cosd(tilt), 90+rot+180))
    print('  \\psline[linewidth=1pt,linecolor=darkgray,linestyle=dashed](1;%.3f)(1;%.3f)' % (rot, rot+180))
    print('  \\psdot[dotsize=4pt 1,linecolor=darkgray](0,0)')
    print('  \\rput{%.3f}{\\psellipse[linecolor=darkgray,fillstyle=solid,fillcolor=gray](0,%.3f)(%.3f,%.3f)}' %  (rot, -cosd(tilt), axeWidth, axeWidth*sind(tilt)))
    print('\\psset{linestyle=dashed,linecolor=blue}')
    shortPathEllipse(45, 25, -60, 115, tilt=tilt, rot=rot, drawPoints=True, onlyPath=True, show=INVISIBLE)
    globe(tilt=tilt, rot=rot, hollow=True, diff_longitude=15, longitude_start=10)
    print('\\psset{linestyle=solid,linecolor=blue}')
    shortPathEllipse(45, 25, -60, 115, tilt=tilt, rot=rot, drawPoints=True, onlyPath=True, show=VISIBLE)
    print('\\rput(1.2;%.3f){North}' % (90 + rot))
    print('\\rput(1.2;%.3f){South}' % (90 + rot + 180))
    print('\\rput{%.3f}{' % (rot))
    print('  \\psset{linecolor=black}')
    print('  \\psline[linewidth=3pt,linecolor=darkgray,linestyle=dashed](0,%.3f)(0,%.3f)  %% internal axis' % (cosd(tilt), -cosd(tilt)))
    print('  \\psline[linewidth=6pt](0,%.3f)(0,%.3f)' % (cosd(tilt), cosd(tilt)*1.3))
    print('  \\psline[linewidth=6pt](0,%.3f)(0,%.3f)' % (-1, -cosd(tilt)*1.3))
    print('  \\psline[linewidth=6pt](0,%.3f)(0,%.3f)' % (-1, -cosd(tilt)*1.3))
    print('  \\psellipse[linecolor=lightgray,linewidth=0.3pt,fillstyle=solid,fillcolor=black](0,%.3f)(%.3f,%.3f)' %  (cosd(tilt)*1.3, axeWidth, axeWidth*sind(tilt)))
    print('  \\psellipse[fillstyle=solid,fillcolor=black](0,%.3f)(%.3f,%.3f)' %  (cosd(tilt), axeWidth, axeWidth*sind(tilt)))
    print('  \\psellipse[fillstyle=solid,fillcolor=black](0,%.3f)(%.3f,%.3f)' % (-cosd(tilt)*1.3, axeWidth, axeWidth*sind(tilt)))
    print('}')
    pictureEnd()


    print('\n\n\\vspace{7mm}\n\n')

    print('\n\n\n%%%%%  Cropped with lots of longitude but no latitudes  %%%%%')
    pictureStart(unit='5mm', size='(-7,-7)(7,7)', crop=True)
    globe(hollow=False, longitude_start=1, radius=8, diff_latitude=0, diff_longitude=3)
    shortPathEllipse(45, 25, -60, 115, radius=8, rot=DEFAULT_ROT, drawPoints=False, onlyPath=False, show=VISIBLE)
    pictureEnd()

    print('%%%%%  Wireframe (no edge)  %%%%%')
    pictureStart(unit='40mm', size='(-1,-1)(1,1)', crop=False)
    print('\\psset{linewidth=2pt}')
    for longitude in range(5,185, 30):
        meridian(longitude=longitude, show=ALL)
    print('\\psset{linewidth=0.1pt}')
    parallel(latitude=70)
    parallel(latitude=-70)
    equator()
    pictureEnd()

    print('\n\n\\vspace{5mm}\n\n')
    print('\n\n\n%%%%%  No edge but only visible  %%%%%')
    pictureStart(unit='40mm', size='(-1,-1)(1,1)', crop=False)
    print('\\psset{linewidth=1pt}')
    for longitude in range(15,185, 180):
        meridian(longitude=longitude, show=VISIBLE)
    for latitude in range(-85, 86, 25):
        parallel(latitude=latitude, show=VISIBLE)
    pictureEnd()

    print('%%%%%  One globe in another one  %%%%%')
    pictureStart(unit='20mm', size='(-2,-2)(2,2)', crop=False)
    print('\\psset{linewidth=1pt}')
    (tilt, rot) = tiltRotOxOy(90 - EARTH_INCLINATION, 45)
    decal = EARTH_INCLINATION
    smallRad = 1.4
    globe(radius=2, hollow=True, longitude_start=decal, diff_latitude=0)
    print('\\psset{linewidth=1pt, linestyle=dashed}')
    equator(radius=2, show=INVISIBLE)
    meridian(radius=2, show=INVISIBLE, longitude=decal)
    print('\\psset{linecolor=orange, linestyle=solid}')
    print('\\pscircle[fillstyle=solid,fillcolor=yellow](0,0){' + str(smallRad) + '}')
    globe(radius=smallRad, tilt=tilt, rot=rot, hollow=False, diff_latitude=0, diff_longitude=0)
    for longitude in range(28, 180, 30):
        meridian(radius=smallRad, tilt=tilt, rot=rot, show=VISIBLE, longitude=longitude)
    equator(radius=smallRad, tilt=tilt, rot=rot, show=VISIBLE)
    print('\\psset{linewidth=2pt, linecolor=black}')
    globe(radius=2, hollow=False, longitude_start=decal, diff_latitude=0)
    meridian(radius=2, show=VISIBLE, longitude=decal)
    equator(radius=2, show=VISIBLE)
    pictureEnd()

    print('\\end{center}')

    documentEnd()


def sind(angle):
    return sin(angle*pi/180)
def cosd(angle):
    return cos(angle*pi/180)
def tand(angle):
    return tan(angle*pi/180)
def asind(r):
    return asin(r)*180/pi
def acosd(r):
    return acos(r)*180/pi
def atand(r):
    return atan(r)*180/pi
def atan2d(x,y):
    return atan2(x,y)*180/pi



# gives tilt and final rotation when axe is rotated along Ox and then Oy
def tiltRotOxOy(angleOx, angleOy):
    if angleOx == 0 or angleOy == 0:
        return (angleOy, angleOx)
    if angleOx % 180 == 90:
        return (0, angleOx)
    if angleOy % 180 == 90:
        tilt = 90 - angleOx
        rot = 90
        if sind(angleOy) < 0:
          #rot += 180
          tilt *= -1
    else:
        tilt = asind(cosd(angleOx)*sind(angleOy))
        rot = atand(tand(angleOx)/cosd(angleOy))
        if cosd(angleOy) < 0:
          rot += 180
    return (tilt, rot)

# gives tilt and final rotation when axe is rotated along Oy and then Ox
def tiltRotOyOx(angleOy, angleOx):
    return (angleOy, angleOx)

# gives tilt and final rotation when axe is rotated along Ox and then Oz
def tiltRotOxOz(angleOx, angleOz):
    if angleOz % 180 == 90:
        return ((-1)**((angleOz-90) // 180) * angleOx, 0)
    if angleOx % 180 == 0 or angleOz % 180 == 0:
        return (0, (-1)**(angleOz // 180) * angleOx)
    if angleOx % 180 == 90:
        if sind(angleOx) > 0:
            return (angleOz, angleOx)
        else:
            return (-angleOz, angleOx)
    tilt = asind(sind(angleOx)*sind(angleOz))
    rot = atand(tand(angleOx)*cosd(angleOz))
    if cosd(angleOx) < 0:
        rot += 180
    return (tilt, rot)

# gives tilt and final rotation when axe is rotated along Oy and then Oz
def tiltRotOyOz(angleOy, angleOz):
    return tiltRotOxOz(-angleOy, angleOz - 90)

# gives tilt and final rotation when North is at given polar coordinates
def tiltRotPolar(theta, phi):
    return tiltRotOyOz(90 - phi, theta)

(DEFAULT_TILT, DEFAULT_ROT) = tiltRotOxOy(-EARTH_INCLINATION, 45)

# return x-y-z coords from latitude and longitude when axis has tilt:
def getXYZPosition(latitude, longitude, tilt=DEFAULT_TILT, radius=1):
    return (radius * (cosd(tilt) * cosd(latitude) * cosd(longitude) + sind(tilt) * sind(latitude)),
            radius * cosd(latitude) * sind(longitude),
            radius * (cosd(tilt) * sind(latitude) - sind(tilt) * cosd(latitude) * cosd(longitude)))
# return x-y coords from latitude and longitude, with rot supposed 0 (use \rput{rot} to place on the right spot)
def getPointPosition(latitude, longitude, tilt=DEFAULT_TILT, radius=1):
    return getXYZPosition(latitude=latitude, longitude=longitude, tilt=tilt, radius=radius)[1:]
def isPointVisible(latitude, longitude, tilt=DEFAULT_TILT):
    return getXYZPosition(latitude=latitude, longitude=longitude, tilt=tilt)[0] >= 0

def shortPathEllipse(latitude1, longitude1, latitude2, longitude2, tilt=DEFAULT_TILT, radius=1, rot=0, show=ALL, onlyPath=True, drawPoints=True):
    if latitude1 == latitude2 and longitude1 == longitude2:
        return
    (x1,y1,z1) = getXYZPosition(latitude=latitude1, longitude=longitude1, tilt=tilt, radius=radius)
    (x2,y2,z2) = getXYZPosition(latitude=latitude2, longitude=longitude2, tilt=tilt, radius=radius)
    (a,b,c) = (y1*z2 - z1*y2, z1*x2 - x1*z2, x1*y2 - y1*x2)
    print("%% short path: x1,y1,z1, x2,y2,z2, a,b,c:", x1, y1, z1, ' ', x2, y2, z2, ' ', a, b, c)
    n = a*a + b*b + c*c
    if n == 0:
        return
    if c == 0:
        delta = 90
    else:
        delta = atand(-b / c)
    semiMajorAxis = radius
    semiMinorAxis = abs(a/sqrt(n))*radius
    comment = "short path ellipse"
    if rot:
        print('\\rput{%.3f}(0,0){' % rot)
    if drawPoints:
        if show==ALL or ((show==VISIBLE) == (x1>=0)):
            print('  \\psdot[linecolor=%s](%.3f,%.3f)  %% %s' % (((x1>=0) and 'black' or 'gray'), y1, z1, 'Point 1'))
        if show==ALL or ((show==VISIBLE) == (x2>=0)):
            print('  \\psdot[linecolor=%s](%.3f,%.3f)  %% %s' % (((x2>=0) and 'black' or 'gray'), y2, z2, 'Point 2'))
    if onlyPath:
        angle1 = (atan2d(z1, y1) - delta) % 360
        angle2 = (atan2d(z2, y2) - delta) % 360
        if (angle2 - angle1) % 360 > 180:
            (angle1, angle2, x1, y1, z1, x2, y2, z2) = (angle2, angle1, x2, y2, z2, x1, y1, z1)
        if (show == VISIBLE)  ==  ((sind(angle1) >= 0) == (x1>=0)):
            startAngle = 0
            endAngle = 180
        else:
            startAngle = 180
            endAngle = 360
        if show == ALL  or  (angle1 >= startAngle and angle2 <= endAngle and angle1 <= angle2):
            print("      \\rput{%.3f}(0,0){\\psellipticarc(0,0)(%.3f,%.3f){%.3f}{%.3f}}  %% %s" % (delta, semiMajorAxis, semiMinorAxis, angle1, angle2, comment))
        else:
            if angle1 >= startAngle and angle1 <= endAngle:
                print("      \\rput{%.3f}(0,0){\\psellipticarc(0,0)(%.3f,%.3f){%.3f}{%.3f}}  %% %s" % (delta, semiMajorAxis, semiMinorAxis, angle1, endAngle%360, comment))
            elif angle2 >= startAngle and angle2 <= endAngle:
                print("      \\rput{%.3f}(0,0){\\psellipticarc(0,0)(%.3f,%.3f){%.3f}{%.3f}}  %% %s" % (delta, semiMajorAxis, semiMinorAxis, startAngle, angle2%360, comment))
    else:
        if show == ALL  or  semiMinorAxis == 0:
            if semiMinorAxis == 0:
                print("      \\psline(%.3f;%.3f)(%.3f;%.3f)  %% %s" % (radius, delta, radius, delta + 180, comment))
            else:
                print(' \\rput{%.3f}(0,0){\\psellipse(0,0)(%.3f,%.3f)}  %% %s' % (delta, semiMajorAxis, semiMinorAxis, comment))
        else:
            angle1 = (atan2d(z1, y1) - delta) % 360
            if (show == VISIBLE)  ==  ((sind(angle1) >= 0) == (x1>=0)):
                startAngle = 0
                endAngle = 180
            else:
                startAngle = 180
                endAngle = 0
            print("      \\rput{%.3f}(0,0){\\psellipticarc(0,0)(%.3f,%.3f){%.3f}{%.3f}}  %% %s" % (delta, semiMajorAxis, semiMinorAxis, startAngle, endAngle, comment))

    if rot:
        print('}')


def documentStart():
    print('%%% Generated by latexglobe.py. Needs pstricks: use dvips+ps2pdf to convert dvi file to pdf.')
    print('\\documentclass{report}')
    print('\\usepackage{pstricks, pstricks-add, pst-grad}')
    print('\\usepackage[a4paper]{geometry}')
    print('\\geometry{tmargin=5mm,bmargin=5mm,lmargin=5mm,rmargin=5mm}')
    print('\\begin{document}')
    print('\\SpecialCoor  % use polar coords (r, theta)')

def documentEnd():
    print('\\end{document}')

star = ''
def pictureStart(unit='10mm', size='(-11, -11)(11, 11)', crop=True):
    global star
    print('\\psset{xunit=' + unit + ', yunit=' + unit + '}')
    print('\\setlength{\\unitlength}{' + unit + '}')
    star = (crop and '*' or '')
    print('\\begin{pspicture' + star + '}' + size)
    print('\\setlength{\\unitlength}{' + unit + '}')

def pictureEnd():
    global star
    print('\\end{pspicture' + star + '}')

def globe(tilt=DEFAULT_TILT, rot=DEFAULT_ROT, radius=1, hollow=False, diff_longitude=30, diff_latitude=15, longitude_start=0):
    if rot != 0:
        print('  \\rput{%.3f}(0,0){' % (rot))

    # north and south poles
    if hollow or sind(tilt) >= 0:
        print('    \\psdot[dotsize=1pt 1, dotstyle=*, linecolor=%s](%.3f,%.3f)  %% North' % ((sind(tilt) >= 0 and 'red' or 'darkgray'), 0, cosd(tilt)*radius) )
    if (abs(cosd(tilt)) > 0.01  or  sind(tilt) < 0) and (hollow or sind(tilt) < 0):
        print('    \\psdot[dotsize=1pt 1, dotstyle=*, linecolor=%s](%.3f,%.3f)  %% South' % ((sind(tilt) < 0  and 'blue' or 'darkgray'), 0, -cosd(tilt)*radius) )

    # axis
    yNorth = cosd(tilt) * radius
    yNorthAxis = yNorth * 1.25
    yNorthEdge = radius * (yNorth > 0 and 1 or -1)
    if hollow:
        if sind(tilt) > 0:
            if abs(yNorthAxis) >= radius:
                print('  \\psline[linecolor=darkgray, linewidth=2pt, linestyle=solid](0,%.3f)(0,%.3f)  %% south axis' % (-yNorth, -yNorthEdge))
            else:
                print('  \\psline[linecolor=darkgray, linewidth=2pt, linestyle=solid](0,%.3f)(0,%.3f)  %% south axis' % (-yNorth, -yNorthAxis))
        else:
            if abs(yNorthAxis) >= radius:
                print('  \\psline[linecolor=darkgray, linewidth=2pt, linestyle=solid](0,%.3f)(0,%.3f)  %% north axis' % (yNorth, yNorthEdge))
            else:
                print('  \\psline[linecolor=darkgray, linewidth=2pt, linestyle=solid](0,%.3f)(0,%.3f)  %% north axis' % (yNorth, yNorthAxis))

    # masked parallels and meridians
    if hollow:
        # parallels and equator
        if diff_latitude > 0:
            #print('    \\psset{linecolor=darkgray, linestyle=dashed, linewidth=.3pt}    % masked parallels')
            print('    \\psset{linecolor=darkgray, linestyle=dashed, linewidth=.2pt}    % masked parallels')
            latitude = -90 + diff_latitude
            while latitude < 90:
                parallel(latitude=latitude, tilt=tilt, rot=0, radius=radius, show=INVISIBLE)  # rot=0 because it is already in rput{rot}
                latitude += diff_latitude
            print('    \\psset{linecolor=darkgray, linestyle=dashed, linewidth=1.pt}')
            equator(tilt=tilt, rot=0, radius=radius, show=INVISIBLE)

        # meridians
        if diff_longitude:
            print('    \\psset{linecolor=darkgray, linestyle=dashed, linewidth=.2pt}    % masked meridians')
            longitude = 0
            while longitude < 180:
                meridian(longitude=longitude + longitude_start, tilt=tilt, rot=0, radius=radius, show=INVISIBLE)  # rot=0 because it is already in rput{rot}
                longitude += diff_longitude

    if hollow:
        print('  \\psline[linecolor=darkgray, linewidth=1pt, linestyle=dashed](0,%.3f)(0,%.3f)  %% earth axis inside' % (yNorth, -yNorth))
        print('  \\psdot[dotsize=2pt 1,linecolor=darkgray](0,0)  % center')

    # visible parallels and meridians
    #    parallels and equator
    if diff_latitude > 0:
        print('    \\psset{linecolor=black, linestyle=solid, linewidth=.5pt}    % visible parallels')
        latitude = -90 + diff_latitude
        while latitude < 90:
            parallel(latitude=latitude, tilt=tilt, rot=0, radius=radius, show=VISIBLE)        # rot=0 because it is already in rput{rot}
            latitude += diff_latitude
        print('    \\psset{linecolor=black, linestyle=solid, linewidth=1.5pt}')
        equator(tilt=tilt, rot=0, radius=radius, show=VISIBLE)

    #   meridians
    if diff_longitude:
        print('    \\psset{linecolor=black, linestyle=solid, linewidth=.5pt}    % visible meridians')
        longitude = 0
        while longitude < 180:
            meridian(longitude=longitude + longitude_start, tilt=tilt, rot=0, radius=radius, show=VISIBLE)  # rot=0 because it is already in rput{rot}
            longitude += diff_longitude

    # globe
    print('    \\pscircle[linewidth=1.5pt, linecolor=black](0,0){' + str(radius) + '} % globe limit')

    # visible axis
    if sind(tilt) > 0:
        print('  \\psline[linecolor=red, linewidth=2pt, linestyle=solid](0,%.3f)(0,%.3f)  %% north axis' % (yNorth, yNorthAxis))
        if abs(yNorthAxis) >= radius:
            print('  \\psline[linecolor=blue, linewidth=2pt, linestyle=solid](0,%.3f)(0,%.3f)  %% south' % (-yNorthEdge, -yNorthAxis))
    else:
        print('  \\psline[linecolor=blue, linewidth=2pt, linestyle=solid](0,%.3f)(0,%.3f)  %% south axis' % (-yNorth, -yNorthAxis))
        if abs(yNorthAxis) >= radius:
            print('  \\psline[linecolor=red, linewidth=2pt, linestyle=solid](0,%.3f)(0,%.3f)  %% north axis' % (yNorthEdge, yNorthAxis))


    if rot != 0:
        print('  } % end final rotation')

def parallel(latitude=0, tilt=DEFAULT_TILT, rot=DEFAULT_ROT, radius=1, show=ALL, comment=''):
    global VISIBLE, INVISIBLE, ALL
    if rot != 0:
        print('  \\rput{%.3f}(0,0){' % (rot))

    center_y = radius * cosd(tilt) * sind(latitude)
    semiMajorAxis = abs(radius * cosd(latitude))
    semiMinorAxis = abs(radius * cosd(latitude) * sind(tilt))
    if (latitude % 180 == 90 or tilt % 180 == 0):
        semiMinorAxis = 0
    if (tilt % 180 == 90):
        semiMinorAxis = semiMajorAxis
    if comment == '':
        comment = 'parallel %d°' % latitude

    if show == ALL:
        if semiMinorAxis == 0:
            #print("      \\psline(%.3f,%.3f)(%.3f,%.3f)  %% %s" % (-semiMajorAxis, center_y, semiMajorAxis, center_y, comment))
            print("      \\psline(%.3f;%.3f)(%.3f;%.3f)  %% %s" % (radius, latitude, radius, 180 - latitude, comment))
        elif semiMinorAxis == semiMajorAxis:
            print("      \\pscircle(0,%.3f){%.3f}  %% %s" % (center_y, semiMajorAxis, comment))
        else:
            print("      \\psellipse(0,%.3f)(%.3f,%.3f)  %% %s" % (center_y, semiMajorAxis, semiMinorAxis, comment))
    else:
        # gamma = ellipse parametrical angle from where it is visible
        # beta = ellipse real angle
        if (latitude + tilt) % 180 == 90:  # or round value of sinGamma to 3 decimals
            sinGamma = (-1)**((latitude + tilt - 90) // 180)
        else:
            sinGamma = tand(latitude) * tand(tilt)
        #print("% kkk  lat, tilt, rot, cent, semMaj, semMin, beta:", latitude, tilt, rot, center_y, semiMajorAxis, semiMinorAxis, sinGamma)
        if (abs(sinGamma) < 0.99999999):
            beta = atand(abs(sind(tilt)) * tand(asind(sinGamma)))
            if (sind(tilt) < 0):
                beta += 180
            if (show == VISIBLE) == (cosd(tilt) >= 0):
                startAngle = 180 - beta
                if beta < 0:
                    endAngle = beta + 360
                else:
                    endAngle   = beta
            else:
                startAngle = beta
                endAngle   = 180 - beta
            if semiMinorAxis == 0:
                #print("      \\psline(%.3f,%.3f)(%.3f,%.3f)  %% %s" % (-semiMajorAxis, center_y, semiMajorAxis, center_y, comment))
                print("      \\psline(%.3f;%.3f)(%.3f;%.3f)  %% %s" % (radius, latitude, radius, 180 - latitude, comment))
            elif semiMinorAxis == semiMajorAxis:
                print("      \\psarc(0,%.3f){%.3f}{%.3f}{%.3f}  %% %s" % (center_y, semiMajorAxis, startAngle, endAngle, comment))
            else:
                print("      \\psellipticarc(0,%.3f)(%.3f,%.3f){%.3f}{%.3f}  %% %s" % (center_y, semiMajorAxis, semiMinorAxis, startAngle, endAngle, comment))
        elif (sind(tilt) * latitude > 0) == (show == VISIBLE):
            if semiMinorAxis == 0:
                #print("      \\psline(%.3f,%.3f)(%.3f,%.3f)  %% %s" % (-semiMajorAxis, center_y, semiMajorAxis, center_y, comment))
                print("      \\psline(%.3f;%.3f)(%.3f;%.3f)  %% %s" % (radius, latitude, radius, 180 - latitude, comment))
            elif semiMinorAxis == semiMajorAxis:
                print("      \\pscircle(0,%.3f){%.3f}  %% %s" % (center_y, semiMajorAxis, comment))
            else:
                print("      \\psellipse(0,%.3f)(%.3f,%.3f)  %% %s" % (center_y, semiMajorAxis, semiMinorAxis, comment))

    if rot != 0:
        print('  } % end final rotation')

def equator(tilt=DEFAULT_TILT, rot=DEFAULT_ROT, radius=1, show=ALL):
    parallel(latitude=0, tilt=tilt, rot=rot, radius=radius, show=show, comment='equator')


# draw the whole circle, that is with opposite meridian (e.g. 30°E + 150°W), which is much simpler
def meridian(longitude=0, tilt=DEFAULT_TILT, rot=DEFAULT_ROT, radius=1, show=ALL, comment=''):
    global VISIBLE, INVISIBLE, ALL
    if rot != 0:
        print('  \\rput{%.3f}(0,0){' % (rot))

    # delta is angle of major Axis
    delta = 90 + atand(sind(tilt) * tand(longitude))
    semiMajorAxis = radius
    semiMinorAxis = abs(radius * cosd(tilt) * sind(longitude))

    if (longitude % 180 == 0 or tilt % 180 == 90):
        semiMinorAxis = 0
    if comment == '':
        comment = 'meridian %d°' % longitude

    if show == ALL  or  semiMinorAxis == semiMajorAxis  or  semiMinorAxis == 0:
        if semiMinorAxis == 0:
            print("      \\psline(%.3f;%.3f)(%.3f;%.3f)  %% %s" % (radius, delta, radius, delta + 180, comment))
        elif semiMinorAxis == semiMajorAxis:
            # same as globe limit
            print("      \\pscircle(0,0){%.3f}  %% %s" % (semiMajorAxis, comment))
        else:
            print("      \\rput{%.3f}(0,0){\\psellipse(0,0)(%.3f,%.3f)}  %% %s" % (delta, semiMajorAxis, semiMinorAxis, comment))
    else:
        if (show == VISIBLE)  ==  (cosd(tilt) * cosd(longitude) > 0):
            startAngle = 180
            endAngle = 0
        else:
            startAngle = 0
            endAngle = 180
        print("      \\rput{%.3f}(0,0){\\psellipticarc(0,0)(%.3f,%.3f){%.3f}{%.3f}}  %% %s" % (delta, semiMajorAxis, semiMinorAxis, startAngle, endAngle, comment))

    if rot != 0:
        print('  } % end final rotation')


if __name__ == '__main__':
    test()
