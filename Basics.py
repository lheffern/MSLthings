import spiceypy as spice
import numpy as np
import matplotlib.pyplot as plt
import spiceypy
from mpl_toolkits.mplot3d import art3d
import seaborn as sn
from __future__ import print_function
from builtins import input
import spiceypy.utils.support_types as stypes
from spiceypy.utils.support_types import SpiceyError


# Find the toolkit in terminal: find / -name cspice 2>/dev/null

'''
Check the proper library is loaded
'''
spice.tkvrsn("TOOLKIT")


'''
Extra Functions
'''

# check number of loaded kernels
kernel_count = spice.ktotal('ALL')
print("Total kernels loaded:", kernel_count)

# find nacid names
def namecode(name='MARS SCIENCE LABORATORY'):
    try:
        nacid = spiceypy.bodn2c(name) #Body name to ID code translation
    except SpiceyError:
    #
    # Stop the program if the code was not found.
    #
        print('Unable to locate the ID code for '
          + str(name))
        raise
    return nacid


'''
Use to clear all kernels
'''
spice.unload('ALL')



'''
Lesson 1 - convtm
Write a program that prompts the user for an input UTC time string, converts it to the following time systems and output
formats:
1. Ephemeris Time (ET) in seconds past J2000
2. Calendar Ephemeris Time
3. Spacecraft Clock Time
and displays the results. Use the program to convert “2004 jun 11 19:32:00” UTC into these alternate systems.
'''

def convtm():
    #
    # Local Parameters
    #
    METAKR = 'convtm.tm'
    SCLKID = -82

    spiceypy.furnsh(METAKR)

    #
    # Prompt the user for the input time string.
    #
    utctim = input('Input UTC Time: ')

    print('Converting UTC Time: {:s}'.format(utctim))

    #
    # Convert utctim to ET.
    #
    et = spiceypy.str2et(utctim)

    print('   ET Seconds Past J2000: {:16.3f}'.format(et))

    #
    # Now convert ET to a calendar time string.
    # This can be accomplished in two ways.
    #
    calet = spiceypy.etcal(et)

    print('   Calendar ET (etcal):   {:s}'.format(calet))

    #
    # Or use timout for finer control over the
    # output format. The picture below was built
    # by examining the header of timout.
    #
    calet = spiceypy.timout(et, 'YYYY-MON-DDTHR:MN:SC ::TDB')

    print('   Calendar ET (timout):  {:s}'.format(calet))

    #
    # Convert ET to spacecraft clock time.
    #
    sclkst = spiceypy.sce2s(SCLKID, et)

    print('   Spacecraft Clock Time: {:s}'.format(sclkst))

    #
    # Convert UTC to Julien Date
    #
    pictur = "Wkd Mon DD HR:MN ::UTC-7 YYYY (JULIAND.#### JDUTC)"

    utcjul = spiceypy.timout(et,pictur)

    print('   TBD Julien Date: {:s}'.format(utcjul))

    spiceypy.unload(METAKR)



if __name__ == '__main__':
    convtm()

# 2004 jun 11 19:32:00

'''
Lesson 2 - getsta
Write a program that prompts the user for an input UTC time string, computes the following quantities at that epoch:
1. The apparent state of Phoebe as seen from CASSINI in the J2000
frame, in kilometers and kilometers/second. This vector itself
is not of any particular interest, but it is a useful
intermediate quantity in some geometry calculations.
2. The apparent position of the Earth as seen from CASSINI in the
J2000 frame, in kilometers.
3. The one-way light time between CASSINI and the apparent position of Earth, in seconds.
4. The apparent position of the Sun as seen from Phoebe in the
J2000 frame (J2000), in kilometers.
5. The actual (geometric) distance between the Sun and Phoebe, in
astronomical units.
and displays the results. Use the program to compute these quantities at “2004 jun 11 19:32:00” UTC.
'''
def getsta():
    #
    # Local parameters
    #
    METAKR = 'getsta.tm'
    #
    # Load the kernels that this program requires. We
    # will need a leapseconds kernel to convert input
    # UTC time strings into ET. We also will need the
    # necessary SPK files with coverage for the bodies
    # in which we are interested.
    #
    spiceypy.furnsh( METAKR )
    #
    #Prompt the user for the input time string.
    #
    utctim = input( 'Input UTC Time: ' )
    print( 'Converting UTC Time: {:s}'.format(utctim) )
    #
    #Convert utctim to ET.
    #
    et = spiceypy.str2et( utctim )
    print( ' ET seconds past J2000: {:16.3f}'.format(et) )
    #
    # Compute the apparent state of Phoebe as seen from
    # CASSINI in the J2000 frame. All of the ephemeris
    # readers return states in units of kilometers and
    # kilometers per second.
    #
    [state, ltime] = spiceypy.spkezr( 'PHOEBE', et,'J2000', 'LT+S', 'CASSINI' )
    print( ' Apparent state of Phoebe as seen '
    'from CASSINI in the J2000\n'
    ' frame (km, km/s):' )
    print( ' X = {:16.3f}'.format(state[0]) )
    print( ' Y = {:16.3f}'.format(state[1]) )
    print( ' Z = {:16.3f}'.format(state[2]) )
    print( ' VX = {:16.3f}'.format(state[3]) )
    print( ' VY = {:16.3f}'.format(state[4]) )
    print( ' VZ = {:16.3f}'.format(state[5]) )
    #
    # Compute the apparent position of Earth as seen from
    # CASSINI in the J2000 frame. Note: We could have
    # continued using spkezr and simply ignored the
    # velocity components.
    #
    [pos, ltime] = spiceypy.spkpos( 'EARTH', et, 'J2000',
    'LT+S', 'CASSINI', )
    print( ' Apparent position of Earth as '
    'seen from CASSINI in the J2000\n'
    ' frame (km):' )
    print(' X = {:16.3f}'.format(pos[0]))
    print(' Y = {:16.3f}'.format(pos[1]))
    print(' Z = {:16.3f}'.format(pos[2]))
    #
    # We need only display LTIME, as it is precisely the
    # light time in which we are interested.
    #
    print(' One way light time between CASSINI and '
          'the apparent position\n'
          ' of Earth (seconds):'
          ' {:16.3f}'.format(ltime))
    #
    # Compute the apparent position of the Sun as seen from
    # PHOEBE in the J2000 frame.
    #
    [pos, ltime] = spiceypy.spkpos('SUN', et, 'J2000',
                                   'LT+S', 'PHOEBE', )
    print(' Apparent position of Sun as '
          'seen from Phoebe in the\n'
          ' J2000 frame (km):')
    print(' X = {:16.3f}'.format(pos[0]))
    print(' Y = {:16.3f}'.format(pos[1]))
    print(' Z = {:16.3f}'.format(pos[2]))
    #
    # Now we need to compute the actual distance between
    # the Sun and Phoebe. The above spkpos call gives us
    # the apparent distance, so we need to adjust our
    # aberration correction appropriately.
    #
    [pos, ltime] = spiceypy.spkpos('SUN', et, 'J2000',
                                   'NONE', 'PHOEBE')
    #
    # Compute the distance between the body centers in
    # kilometers.
    #
    dist = spiceypy.vnorm(pos)
    #
    # Convert this value to AU using convrt.
    #
    dist = spiceypy.convrt(dist, 'KM', 'AU')
    print(' Actual distance between Sun and '
          'Phoebe body centers:\n'
          ' (AU): {:16.3f}'.format(dist))
    spiceypy.unload(METAKR)

if __name__ == '__main__':
    getsta()


'''
Lesson 3 - xform
The solution to the problem can be broken down into a series of simple steps:
-- Decide which SPICE kernels are necessary. Prepare a meta-kernel
listing the kernels and load it into the program.
-- Prompt the user for an input time string.
-- Convert the input time string into ephemeris time expressed as
seconds past J2000 TDB.
-- Compute the state of Phoebe relative to CASSINI in the J2000
reference frame, corrected for aberrations.
-- Compute the state transformation matrix from J2000 to
IAU_PHOEBE at the epoch, adjusted for light time.
-- Multiply the state of Phoebe relative to CASSINI in the J2000
reference frame by the state transformation matrix computed in
the previous step.
-- Compute the position of Earth relative to CASSINI in the J2000
reference frame, corrected for aberrations.
-- Determine what the nominal boresight of the CASSINI high gain
antenna is by examining the frame kernel's content.
-- Compute the rotation matrix from the CASSINI high gain antenna
frame to J2000.
-- Multiply the nominal boresight expressed in the CASSINI high
gain antenna frame by the rotation matrix from the previous
step.
-- Compute the separation between the result of the previous step
and the apparent position of the Earth relative to CASSINI in
the J2000 frame.
'''

def xform():
    #
    # Local parameters
    #
    METAKR = 'MetaKernels/xform.tm'
    #
    # Load the kernels that this program requires. We
    # will need a leapseconds kernel to convert input
    # UTC time strings into ET. We also will need the
    # necessary SPK files with coverage for the bodies
    # in which we are interested.
    #
    spiceypy.furnsh( METAKR )
    #
    #Prompt the user for the input time string.
    #
    utctim = input( 'Input UTC Time: ' )
    print( 'Converting UTC Time: {:s}'.format(utctim) )
    #
    #Convert utctim to ET.
    #
    et = spiceypy.str2et( utctim )
    print( ' ET seconds past J2000: {:16.3f}'.format(et) )
    #
    #
    # Compute the apparent state (spkezr) of Phoebe as seen from
    # CASSINI in the J2000 frame.
    #
    [state, ltime] = spiceypy.spkezr('PHOEBE', et, 'J2000',
                                     'LT+S', 'CASSINI')
    #
    # Now obtain the transformation (sxform) from the inertial
    # J2000 frame to the non-inertial body-fixed IAU_PHOEBE
    # frame. Since we want the apparent position, we
    # need to subtract ltime from et.
    #
    sform = spiceypy.sxform('J2000', 'IAU_PHOEBE', et - ltime)
    #
    # Now rotate (mxvg) the apparent J2000 state into IAU_PHOEBE
    # with the following matrix multiplication:
    #
    bfixst = spiceypy.mxvg(sform, state)
    #
    # Display the results.
    #
    print(' Apparent state of Phoebe as seen '
          'from CASSINI in the IAU_PHOEBE\n'
          ' body-fixed frame (km, km/s):')
    print(' X = {:19.6f}'.format(bfixst[0]))
    print(' Y = {:19.6f}'.format(bfixst[1]))
    print(' Z = {:19.6f}'.format(bfixst[2]))
    print(' VX = {:19.6f}'.format(bfixst[3]))
    print(' VY = {:19.6f}'.format(bfixst[4]))
    print(' VZ = {:19.6f}'.format(bfixst[5]))
    #
    # It is worth pointing out, all of the above could
    # have been done with a single use of spkezr:
    #
    [state, ltime] = spiceypy.spkezr(
        'PHOEBE', et, 'IAU_PHOEBE',
        'LT+S', 'CASSINI')
    #
    # Display the results.
    #
    print(' Apparent state of Phoebe as seen '
          'from CASSINI in the IAU_PHOEBE\n'
          ' body-fixed frame (km, km/s) '
          'obtained using spkezr directly:')
    print(' X = {:19.6f}'.format(state[0]))
    print(' Y = {:19.6f}'.format(state[1]))
    print(' Z = {:19.6f}'.format(state[2]))
    print(' VX = {:19.6f}'.format(state[3]))
    print(' VY = {:19.6f}'.format(state[4]))
    print(' VZ = {:19.6f}'.format(state[5]))
    #
    # Note that the velocity found by using spkezr
    # to compute the state in the IAU_PHOEBE frame differs
    # at the few mm/second level from that found previously
    # by calling spkezr and then sxform. Computing
    # velocity via a single call to spkezr as we've
    # done immediately above is slightly more accurate because
    # it accounts for the effect of the rate of change of
    # light time on the apparent angular velocity of the
    # target's body-fixed reference frame.
    #
    # Now we are to compute the angular separation between
    # the apparent position of the Earth as seen from the
    # orbiter and the nominal boresight of the high gain
    # antenna. First, compute the apparent position of
    # the Earth as seen from CASSINI in the J2000 frame.
    #
    [pos, ltime] = spiceypy.spkpos('EARTH', et, 'J2000',
                                   'LT+S', 'CASSINI')
    #
    # Now compute the location of the antenna boresight
    # at this same epoch. From reading the frame kernel
    # we know that the antenna boresight is nominally the
    # +Z axis of the CASSINI_HGA frame defined there.
    #
    bsight = [0.0, 0.0, 1.0]
    #
    # Now compute the rotation matrix (pxform) from CASSINI_HGA into
    # J2000.
    #
    pform = spiceypy.pxform('CASSINI_HGA', 'J2000', et)
    #
    # And multiply (mvx) the result to obtain the nominal
    # antenna boresight in the J2000 reference frame.
    #
    bsight = spiceypy.mxv(pform, bsight)
    #
    # Lastly compute the angular separation (convrt).
    #
    sep = spiceypy.convrt(spiceypy.vsep(bsight, pos),
                          'RADIANS', 'DEGREES')
    print(' Angular separation between the '
          'apparent position of\n'
          ' Earth and the CASSINI high '
          'gain antenna boresight (degrees):\n'
          ' {:16.3f}'.format(sep))
    #
    # Or alternatively we can work in the antenna
    # frame directly (spkpos).
    #
    [pos, ltime] = spiceypy.spkpos(
        'EARTH', et, 'CASSINI_HGA',
        'LT+S', 'CASSINI')
    #
    # The antenna boresight is the Z-axis in the
    # CASSINI_HGA frame.
    #
    bsight = [0.0, 0.0, 1.0]
    #
    # Lastly compute the angular separation.
    #
    sep = spiceypy.convrt(spiceypy.vsep(bsight, pos),
                          'RADIANS', 'DEGREES')
    print(' Angular separation between the '
          'apparent position of\n'
          ' Earth and the CASSINI high '
          'gain antenna boresight computed\n'
          ' using vectors in the CASSINI_HGA '
          'frame (degrees):\n'
          ' {:16.3f}'.format(sep))
    spiceypy.unload(METAKR)

if __name__ == '__main__':
    xform()



'''
Find the difference b/t dates
'''
step = 4000
# we are going to get positions between these two dates
utc = ['Jun 20, 2004', 'Dec 1, 2005']

# get et values one and two, we could vectorize str2et
etOne = spice.str2et(utc[0])
etTwo = spice.str2et(utc[1])
print("ET One: {}, ET Two: {}".format(etOne, etTwo))





'''
Lesson 4 - subpts
Write a program that prompts the user for an input UTC time string and computes the following quantities at that epoch:
1. The apparent sub-observer point of CASSINI on Phoebe, in the
body fixed frame IAU_PHOEBE, in kilometers.
2. The apparent sub-solar point on Phoebe, as seen from CASSINI in
the body fixed frame IAU_PHOEBE, in kilometers.
The program computes each point twice: once using an ellipsoidal shape model and the
near point/ellipsoid
definition, and once using a DSK shape model and the
nadir/dsk/unprioritized
definition.
The program displays the results. Use the program to compute these quantities at “2004 jun 11 19:32:00” UTC.
'''

def subpts():
    #
    # Local parameters
    #
    METAKR = 'MetaKernels/subpts.tm'
    #
    # Load the kernels that this program requires. We
    # will need:
    #
    # A leapseconds kernel
    # The necessary ephemerides
    # A planetary constants file (PCK)
    # A DSK file containing Phoebe shape data
    #
    spiceypy.furnsh(METAKR)
    #
    # Prompt the user for the input time string.
    #
    utctim = input('Input UTC Time: ')
    print(' Converting UTC Time: {:s}'.format(utctim))
    #
    # Convert utctim to ET.
    #
    et = spiceypy.str2et(utctim)
    print(' ET seconds past J2000: {:16.3f}'.format(et))
    for i in range(2):
        if i == 0:
            #
            # Use the "near point" sub-point definition
            # and an ellipsoidal model.
            #
            method = 'NEAR POINT/Ellipsoid'
        else:
            #
            # Use the "nadir" sub-point definition
            # and a DSK model.
            #
            method = 'NADIR/DSK/Unprioritized'
    print('\n Sub-point/target shape model: {:s}\n'.format(
        method))
    #
    # Compute the apparent sub-observer point of CASSINI
    # on Phoebe.
    #
    [spoint, trgepc, srfvec] = spiceypy.subpnt(method, 'PHOEBE', et,'IAU_PHOEBE', 'LT+S', 'CASSINI' )
    #
    print(' Apparent sub-observer point of CASSINI '
          'on Phoebe in the\n'
          ' IAU_PHOEBE frame (km):')
    print(' X = {:16.3f}'.format(spoint[0]))
    print(' Y = {:16.3f}'.format(spoint[1]))
    print(' Z = {:16.3f}'.format(spoint[2]))
    print(' ALT = {:16.3f}'.format(spiceypy.vnorm(srfvec))) # vnorm computes the vector magnitude
    #
    # Compute the apparent sub-solar point on Phoebe
    # as seen from CASSINI.
    #
    [spoint, trgepc, srfvec] = spiceypy.subslr(method, 'PHOEBE', et,'IAU_PHOEBE', 'LT+S', 'CASSINI')
    print(' Apparent sub-solar point on Phoebe '
          'as seen from CASSINI in\n'
          ' the IAU_PHOEBE frame (km):')
    print(' X = {:16.3f}'.format(spoint[0]))
    print(' Y = {:16.3f}'.format(spoint[1]))
    print(' Z = {:16.3f}'.format(spoint[2]))
    #
    # End of computation block for "method"
    #
    print("")
    spiceypy.unload(METAKR)

if __name__ == '__main__':
    subpts()


'''
Lesson 5 - fovint
Write a program that prompts the user for an input UTC time string and, for that time, 
computes the intersection of the CASSINI ISS NAC camera boresight 
and field of view (FOV) boundary vectors with the surface of Phoebe. 
Compute each intercept twice: once with Phoebe’s shape modeled as an ellipsoid, 
and once with Phoebe’s shape modeled by DSK data. 
The program presents each point of intersection as
1. A Cartesian vector in the IAU_PHOEBE frame
2. Planetocentric (latitudinal) coordinates in the IAU_PHOEBE
frame.
For each of the camera FOV boundary and boresight vectors, if an intersection is found, the program displays the results
of the above computations, otherwise it indicates no intersection exists.
At each point of intersection compute the following:
3. Phase angle
4. Solar incidence angle
5. Emission angle
These angles should be computed using both ellipsoidal and DSK shape models.
Additionally compute the local solar time at the intercept of the camera boresight with the surface of Phoebe, using
both ellipsoidal and DSK shape models.
Use this program to compute values at the epoch:
"2004 jun 11 19:32:00" UTC
'''

def fovint():
    #
    # Local parameters
    #
    METAKR = 'MetaKernels/fovint.tm'
    #
    # Load the kernels that this program requires. We
    # will need:
    #
    # A leapseconds kernel
    # The necessary ephemerides
    # A planetary constants file (PCK)
    # A DSK file containing Phoebe shape data
    #
    spiceypy.furnsh(METAKR)
    ROOM = 4 #square - 4 corners?
    #
    # Prompt the user for the input time string.
    #
    utctim = input('Input UTC Time: ')
    print(' Converting UTC Time: {:s}'.format(utctim))
    #
    # Convert utctim to ET.
    #
    et = spiceypy.str2et(utctim)
    print(' ET seconds past J2000: {:16.3f}'.format(et))
    #
    #
    # Now we need to obtain the FOV configuration of
    # the ISS NAC camera. To do this we will need the
    # ID code for CASSINI_ISS_NAC.
    #
    nacid = namecode('CASSINI_ISS_NAC')
    #nacid = -82360 # can hardcode this one if the function didn't work
    #
    # Now retrieve the field of view parameters.
    #
    [shape, insfrm, bsight, n, bounds] = spiceypy.getfov(nacid, ROOM)
    #
    # `bounds' is a numpy array. We'll convert it to a list.
    #
    # Rather than treat BSIGHT as a separate vector,
    # copy it into the last slot of BOUNDS.
    #
    bounds = bounds.tolist()
    bounds.append(bsight)
    #
    # Set vector names to be used for output.
    #
    vecnam = ['Boundary Corner 1',
              'Boundary Corner 2',
              'Boundary Corner 3',
              'Boundary Corner 4',
              'Cassini NAC Boresight']
    #
    # Set values of "method" string that specify use of
    # ellipsoidal and DSK (topographic) shape models.
    #
    # In this case, we can use the same methods for calls to both
    # spiceypy.sincpt and spiceypy.ilumin. Note that some SPICE
    # routines require different "method" inputs from those
    # shown here. See the API documentation of each routine
    # for details.
    #
    method = ['Ellipsoid', 'DSK/Unprioritized']
    #
    # Get ID code of Phoebe. We'll use this ID code later, when we
    # compute local solar time.
    #
    phoeid = int(namecode('PHOEBE'))
    #
    # Now perform the same set of calculations for each
    # vector listed in the BOUNDS array. Use both
    # ellipsoidal and detailed (DSK) shape models.
    #
    for i in range(5):
        #
        # Call sincpt to determine coordinates of the
        # intersection of this vector with the surface
        # of Phoebe.
        #
        print('Vector: {:s}\n'.format(vecnam[i])) # vecnam = array above, 4 corners + boresight = 5
        for j in range(2):
            print(' Target shape model: {:s}\n'.format(method[j])) # try ellipse & DSK = 2
            try:
                [point, trgepc, srfvec] = spiceypy.sincpt(method[j], 'PHOEBE', et,
                'IAU_PHOEBE', 'LT+S', 'CASSINI',insfrm, bounds[i])
                # sincpt = Surface intercept
                #
                # Now, we have discovered a point of intersection.
                # Start by displaying the position vector in the
                # IAU_PHOEBE frame of the intersection.
                #
                print(' Position vector of surface intercept '
                      'in the IAU_PHOEBE frame (km):')
                print(' X = {:16.3f}'.format(point[0]))
                print(' Y = {:16.3f}'.format(point[1]))
                print(' Z = {:16.3f}'.format(point[2]))
                #
                # Display the planetocentric latitude and longitude
                # of the intercept.
                #
                [radius, lon, lat] = spiceypy.reclat(point)
                # reclat = Rectangular to latitudinal coordinates
                print(' Planetocentric coordinates of '
                      'the intercept (degrees):')
                print(' LAT = {:16.3f}'.format(
                    lat * spiceypy.dpr()))
                print(' LON = {:16.3f}'.format(
                    lon * spiceypy.dpr()))
                # dpr = Degrees per radian
                #
                #
                # Compute the illumination angles at this
                # point.
                #
                # illumf = Illumination angles, general source, return flags
                #
                [trgepc, srfvec, phase, solar, emissn, visibl, lit] = \
                    spiceypy.illumf(
                        method[j], 'PHOEBE', 'SUN', et,
                        'IAU_PHOEBE', 'LT+S', 'CASSINI', point)
                print(' Phase angle (degrees): '
                      '{:16.3f}'.format(phase * spiceypy.dpr()))
                print(' Solar incidence angle (degrees): '
                      '{:16.3f}'.format(solar * spiceypy.dpr()))
                print(' Emission angle (degrees): '
                      '{:16.3f}'.format(emissn * spiceypy.dpr()))
                print(' Observer visible: {:s}'.format(
                    str(visibl)))
                print(' Sun visible: {:s}'.format(
                    str(lit)))
                if i == 4:
                    #
                    # Compute local solar time corresponding
                    # to the light time corrected TDB epoch
                    # at the boresight intercept.
                    #
                    [hr, mn, sc, time, ampm] = spiceypy.et2lst(trgepc,phoeid,lon,'PLANETOCENTRIC')
                    print('\n Local Solar Time at boresight intercept (24 Hour Clock):\n'
                      ' {:s}'.format(time))
                #
                # End of LST computation block.
                #
            except SpiceyError as exc:
                #
                # Display a message if an exception was thrown.
                # For simplicity, we treat this as an indication
                # that the point of intersection was not found,
                # although it could be due to other errors.
                # Otherwise, continue with the calculations.
                #
                print('Exception message is: {:s}'.format(exc.value))
            #
            # End of SpiceyError try-catch block.
            #
            print('')
        #
        # End of target shape model loop.
        #
    #
    # End of vector loop.
    #
    spiceypy.unload(METAKR)

if __name__ == '__main__':
    fovint()

# Now repeat for MAVEN/Mars!




'''
Last Lesson - Geometric Event Finding Hands-On Lesson, using MEX
In this lesson the student is asked to construct a program that finds the time intervals, within a specified time range,
when the Mars Express Orbiter (MEX) is visible from the DSN station DSS-14. Possible occultation of the spacecraft
by Mars is to be considered.

Write a program that finds the set of time intervals, within the time range
2004 MAY 2 TDB
2004 MAY 6 TDB
when the Mars Express Orbiter (MEX) is visible from the DSN station DSS-14. These time intervals are frequently
called “view periods.”

The spacecraft is considered visible if its apparent position (that is, its position corrected for light time and stellar
aberration) has elevation of at least 6 degrees in the topocentric reference frame DSS-14_TOPO. In this exercise, we
ignore the possibility of occultation of the spacecraft by Mars.

Use a search step size that ensures that no view periods of duration 5 minutes or longer will be missed by the search.
Display the start and stop times of these intervals using TDB calendar dates and millisecond precision.
'''

def viewpr():
    METAKR = 'MetaKernels/viewpr.tm'
    #
    spiceypy.furnsh(METAKR)
    TDBFMT = 'YYYY MON DD HR:MN:SC.### (TDB) ::TDB'
    MAXIVL = 1000
    MAXWIN = 2 * MAXIVL
    #
    # Assign the inputs for our search.
    #
    # Since we're interested in the apparent location of the
    # target, we use light time and stellar aberration
    # corrections. We use the "converged Newtonian" form
    # of the light time correction because this choice may
    # increase the accuracy of the occultation times we'll
    # compute using gfoclt.
    #
    srfpt = 'DSS-14' # ground station
    obsfrm = 'DSS-14_TOPO'
    target = 'MEX' # MEX spacecraft
    abcorr = 'CN+S'
    start = '2004 MAY 2 TDB'
    stop = '2004 MAY 6 TDB'
    elvlim = 6.0
    #
    # The elevation limit above has units of degrees; we convert
    # this value to radians for computation using SPICE routines.
    # We'll store the equivalent value in radians in revlim.
    #
    revlim = spiceypy.rpd() * elvlim #Radians per degree
    #
    # Since SPICE doesn't directly support the AZ/EL coordinate
    # system, we use the equivalent constraint
    #
    # latitude > revlim
    #
    # in the latitudinal coordinate system, where the reference
    # frame is topocentric and is centered at the viewing location.
    #
    crdsys = 'LATITUDINAL'
    coord = 'LATITUDE'
    relate = '>'
    #
    # The adjustment value only applies to absolute extrema
    # searches; simply give it an initial value of zero
    # for this inequality search.
    #
    adjust = 0.0
    #
    # stepsz is the step size, measured in seconds, used to search
    # for times bracketing a state transition. Since we don't expect
    # any events of interest to be shorter than five minutes, and
    # since the separation between events is well over 5 minutes,
    # we'll use this value as our step size. Units are seconds.
    #
    stepsz = 300.0
    #
    # Display a banner for the output report:
    #
    print('\n{:s}\n'.format(
        'Inputs for target visibility search:'))
    print(' Target = '
          '{:s}'.format(target))
    print(' Observation surface location = '
          '{:s}'.format(srfpt))
    print(' Observer\'s reference frame = '
          '{:s}'.format(obsfrm))
    print(' Elevation limit (degrees) = '
          '{:f}'.format(elvlim))
    print(' Aberration correction = '
          '{:s}'.format(abcorr))
    print(' Step size (seconds) = '
          '{:f}'.format(stepsz))
    #
    # Convert the start and stop times to ET.
    #
    etbeg = spiceypy.str2et(start)
    etend = spiceypy.str2et(stop)
    #
    # Display the search interval start and stop times
    # using the format shown below.
    #
    # 2004 MAY 06 20:15:00.000 (TDB)
    #
    timstr = spiceypy.timout(etbeg, TDBFMT)
    print(' Start time = '
          '{:s}'.format(timstr))
    timstr = spiceypy.timout(etend, TDBFMT)
    print(' Stop time = '
          '{:s}'.format(timstr))
    print(' ')
    #
    # Initialize the "confinement" window with the interval
    # over which we'll conduct the search.
    #
    cnfine = stypes.SPICEDOUBLE_CELL(2)
    spiceypy.wninsd(etbeg, etend, cnfine) #Insert an interval into a DP window
    #
    # In the call below, the maximum number of window
    # intervals gfposc can store internally is set to MAXIVL.
    # We set the cell size to MAXWIN to achieve this.
    #
    riswin = stypes.SPICEDOUBLE_CELL(MAXWIN)
    #
    # Now search for the time period, within our confinement
    # window, during which the apparent target has elevation
    # at least equal to the elevation limit.
    #
    spiceypy.gfposc(target, obsfrm, abcorr, srfpt,
                    crdsys, coord, relate, revlim,
                    adjust, stepsz, MAXIVL, cnfine, riswin)
    # gfposc = observer-target vector coordinate search
    #
    # The function wncard returns the number of intervals
    # in a SPICE window.
    #
    winsiz = spiceypy.wncard(riswin)
    if winsiz == 0:
        print('No events were found.')
    else:
        print('Visibility times of {0:s} '
              'as seen from {1:s}:\n'.format(
            target, srfpt))
        for i in range(winsiz):
            [intbeg, intend] = spiceypy.wnfetd(riswin, i)
            # wnfetd = Fetch an interval from a DP window
            #
            # Convert the rise time to a TDB calendar string.
            #
            timstr = spiceypy.timout(intbeg, TDBFMT)
            #
            # Write the string to standard output.
            #
            if i == 0:
                print('Visibility or window start time:'
                      ' {:s}'.format(timstr))
            else:
                print('Visibility start time: '
                      ' {:s}'.format(timstr))
            #
            # Convert the set time to a TDB calendar string.
            #
            timstr = spiceypy.timout(intend, TDBFMT)
            if i == (winsiz - 1):
                print('Visibility or window stop time: '
                      ' {:s}'.format(timstr))
            else:
                print('Visibility stop time: '
                      ' {:s}'.format(timstr))
            print(' ')
    spiceypy.unload(METAKR)


if __name__ == '__main__':
    viewpr()


'''
Be sure to quit each program properly
'''
spice.kclear()
spiceypy.unload('ALL')