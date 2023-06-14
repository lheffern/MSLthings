import spiceypy as spice
import numpy as np
import matplotlib.pyplot as plt
import spiceypy
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sn


# Find the toolkit in terminal: find / -name cspice 2>/dev/null

'''
Check the proper library is loaded
'''
spice.tkvrsn("TOOLKIT")




'''
Write a program to track MAVEN's location from MSL
'''

def getmaven():
    #
    # Load the metakernal
    #
    METAKRM = '/Users/lheffern/PycharmProjects/SPICEworkshop/MetaKernels/findmaven.tm'
    #
    # Load the kernels that this program requires. We
    # will need a leapseconds kernel to convert input
    # UTC time strings into ET. We also will need the
    # necessary SPK and PCK files with coverage for the bodies
    # in which we are interested.
    #
    spiceypy.furnsh( METAKRM )
    # furnish loads the kernels that are in the metakernal
    #
    # Orbital dates for SEPs in 2017
    start_et = spice.utc2et('2017-07-01')
    end_et = spice.utc2et('2017-10-01')
    # we convet the UTC dates to ET for computations
    #
    interval = 3600  # Time interval in seconds (1 hour)
    et = start_et
    postion=[]
    while et <= end_et:
        maven_pos, _ = spice.spkpos('-202', et, 'J2000', 'NONE', '-76')
        # calculates the position of MAVEN (-202) based on MSL (-76)
        postion.append(maven_pos)
        # Process the position data as needed
        # ...
        et += interval
    return(postion)
    spice.unload('ALL')
    # unloads the spice kernels, helps with RAM use


if __name__ == '__main__':
    output=np.rot90(getmaven())


x=output[0]
y=output[1]
z=output[2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the data points
ax.scatter(x, y, z, c='b', marker='.',linestyle='dotted')

# Set labels for the x, y, and z axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set title for the plot
ax.set_title('3D Plot')

mars_radius = 3390  # Mars radius in kilometers
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x_sphere = mars_radius * np.outer(np.cos(u), np.sin(v))
y_sphere = mars_radius * np.outer(np.sin(u), np.sin(v))
z_sphere = mars_radius * np.outer(np.ones(np.size(u)), np.cos(v))

ax.plot_surface(x_sphere, y_sphere, z_sphere, color='r', alpha=0.3)

# Show the plot
plt.show()



'''
Determine the angular separation between Earth and Mars for any given date
'''
def getMarsEarthAngle(inputdate='2022 feb 15 12:00:00'):
    #
    # Load the metakernal
    #
    METAKRM = 'MetaKernels/MarsKernels.tm'
    #
    # Load the kernels that this program requires. We
    # will need a leapseconds kernel to convert input
    # UTC time strings into ET. We also will need the
    # necessary SPK and PCK files with coverage for the bodies
    # in which we are interested.
    #
    spiceypy.furnsh( METAKRM )
    # furnish loads the kernels that are in the metakernal
    #
    # Orbital dates for the Feb 22 SEP event
    utctim = str(inputdate)
    et = spiceypy.str2et(utctim)
    # Compute the angular positions
    earth_state, _ = spice.spkpos('EARTH', et, 'J2000', 'NONE', 'SUN')
    mars_state, _ = spice.spkpos('MARS', et, 'J2000', 'NONE', 'SUN')
    #
    angular_position = spice.vsep(earth_state, mars_state)
    #
    print(f"Angular Position between Mars and Earth on {utctim}:")
    print(f"{np.degrees(angular_position):.2f} degrees")
    #
    spice.unload('MetaKernels/MarsKernels.tm')

if __name__ == '__main__':
    getMarsEarthAngle()


'''
Mars landing date
'''
# 2012 JUL 02 00:01:06.183

'''
Determine MSL's position on Mars
'''

def getMSLtracks(start_time_utc='2021 dec 01 12:00:00',end_time_utc='2021 dec 30 12:00:00'):
    #
    # Load the metakernal
    #
    METAKRM = 'MetaKernels/MarsKernels.tm'
    #
    # Load the kernels that this program requires. We
    # will need a leapseconds kernel to convert input
    # UTC time strings into ET. We also will need the
    # necessary SPK and PCK files with coverage for the bodies
    # in which we are interested.
    #
    spiceypy.furnsh( METAKRM )
    # furnish loads the kernels that are in the metakernal
    #
    # Orbital dates for the Feb 22 SEP event
    start_et = spice.utc2et(start_time_utc)
    end_et = spice.utc2et(end_time_utc)
    # Compute the angular positions
    step_size = 3600  # Time step in seconds
    times = range(int(start_et), int(end_et + step_size), step_size)
    rover_positions = []
    rover_altitudes = []
    rover_latitudes = []
    rover_longitudes = []
    rover_radius=[]
    #
    for et in times:
        rover_state, _ = spice.spkpos('-76', et, 'IAU_MARS', 'NONE', 'MARS')
        rover_positions.append(rover_state)
        # Obtain the altitude by subtracting the radius of Mars from the distance
        mars_radius = spice.bodvrd('MARS', 'RADII', 3)[1][0]  # Fetch Mars radius in kilometers
        rover_altitude = spice.vnorm(rover_state) - mars_radius
        rover_altitudes.append(rover_altitude)
        # Convert the Cartesian coordinates to latitude, longitude, and altitude
        radius, longitude, latitude = spice.reclat(rover_state)
        rover_latitudes.append(np.degrees(latitude))
        rover_longitudes.append(np.degrees(longitude))
        rover_radius.append(radius)
    return rover_positions, rover_altitudes, rover_latitudes, rover_longitudes, radius, times
    #
    spice.unload('MetaKernels/MarsKernels.tm')

if __name__ == '__main__':
    rover_positions1, rover_altitudes1, rover_latitudes1,rover_longitudes1, rover_radius1, times1=getMSLtracks()

rover_positions=np.rot90(rover_positions1)

x=rover_positions[0]
y=rover_positions[1]
z=rover_positions[2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# make a Mars

mars_radius = spice.bodvrd('MARS', 'RADII', 3)[1][0]
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x_sphere = mars_radius * np.outer(np.cos(u), np.sin(v))
y_sphere = mars_radius * np.outer(np.sin(u), np.sin(v))
z_sphere = mars_radius * np.outer(np.ones(np.size(u)), np.cos(v))

ax.plot_wireframe(x_sphere, y_sphere, z_sphere, color='red', linewidth=0.5, label='Mars')


# Plot the data points
ax.plot(x, y, z, c='b', marker='o',linestyle='dotted')

# Set labels for the x, y, and z axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set title for the plot
ax.set_title('3D Plot')

# Show the plot
plt.show()


# Latitude/Longitude Plot w/ Altitude colored

fig, ax = plt.subplots()

# Scatter plot of latitude vs longitude with altitude as color
sc = ax.scatter(rover_longitudes1, rover_latitudes1, c=rover_altitudes1, cmap='cool', s=30)

# Set labels for the x and y axes
ax.set_xlabel('Longitude (degrees)')
ax.set_ylabel('Latitude (degrees)')

# Set title for the plot
ax.set_title('Latitude vs Longitude - Mars Rover')

# Add a color bar
cbar = plt.colorbar(sc)
cbar.set_label('Altitude (km)')
plt.grid()
# Show the plot
plt.show()



fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(times1,rover_altitudes1,'ro-')
ax.set_xlabel('SCLK')
ax.set_ylabel('Rover Altitude (km)')
plt.grid()
plt.show()
