KPL/MK

     This is the meta-kernel used in the solution of the
     "Computing Sub-spacecraft and Sub-solar Points" task
     in the Remote Sensing Hands On Lesson.

     The names and contents of the kernels referenced by this
     meta-kernel are as follows:

     File name                   Contents
     -------------------------- -----------------------------
     naif0008.tls                Generic LSK
     981005_PLTEPH-DE405S.bsp    Solar System Ephemeris
     020514_SE_SAT105.bsp        Saturnian Satellite Ephemeris
     030201AP_SK_SM546_T45.bsp   Cassini Spacecraft SPK
     cpck05Mar2004.tpc           Cassini Project PCK
     phoebe_64q.bds              Phoebe DSK

     \begindata
     PATH_VALUES     = ('/Users/lheffern/PycharmProjects/SPICEworkshop/kernels')
     PATH_SYMBOLS    = ('KERNELS'    )
     KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls',
                         '$KERNELS/spk/981005_PLTEPH-DE405S.bsp',
                         '$KERNELS/spk/020514_SE_SAT105.bsp',
                         '$KERNELS/spk/030201AP_SK_SM546_T45.bsp',
                         '$KERNELS/pck/cpck05Mar2004.tpc'
                         '$KERNELS/dsk/phoebe_64q.bds' )

     \begintext