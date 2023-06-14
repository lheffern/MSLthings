KPL/MK
     This is the meta-kernel used in the solution of the
     "Intersecting Vectors with a Triaxial Ellipsoid" task
     in the Remote Sensing Hands On Lesson.

     The names and contents of the kernels referenced by this
     meta-kernel are as follows:

     File name Contents
     -------------------------- -----------------------------
     naif0008.tls                Generic LSK - leapseconds
     cas00084.tsc                Cassini SCLK - spacecraft clock
     981005_PLTEPH-DE405S.bsp    Solar System Ephemeris - SPK
     020514_SE_SAT105.bsp        Saturnian Satellite Ephemeris - SPK
     030201AP_SK_SM546_T45.bsp   Cassini Spacecraft Ephemeris - SPK
     cas_v37.tf                  Cassini FK - frame
     04135_04171pc_psiv2.bc      Cassini Spacecraft CK - orientation/camera
     cpck05Mar2004.tpc           Cassini Project PCK - constants (size, shape)
     cas_iss_v09.ti              ISS Instrument Kernel - IK
     phoebe_64q.bds              Phoebe DSK - digital shape kernel

     \begindata
     PATH_VALUES     = ('/Users/lheffern/PycharmProjects/SPICEworkshop/kernels')
     PATH_SYMBOLS    = ('KERNELS'    )
     KERNELS_TO_LOAD = ( '$KERNELS/lsk/naif0008.tls',
                         '$KERNELS/sclk/cas00084.tsc',
                         '$KERNELS/spk/981005_PLTEPH-DE405S.bsp',
                         '$KERNELS/spk/020514_SE_SAT105.bsp',
                         '$KERNELS/spk/030201AP_SK_SM546_T45.bsp',
                         '$KERNELS/fk/cas_v37.tf',
                         '$KERNELS/ck/04135_04171pc_psiv2.bc',
                         '$KERNELS/pck/cpck05Mar2004.tpc',
                         '$KERNELS/ik/cas_iss_v09.ti'
                         '$KERNELS/dsk/phoebe_64q.bds' )
     \begintext