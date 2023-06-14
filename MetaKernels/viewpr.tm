KPL/MK

   Example meta-kernel for geometric event finding hands-on
   coding lesson.

   The names and contents of the kernels referenced by this
   meta-kernel are as follows:

   File name                   Contents
   --------------------------  -----------------------------
   de405xs.bsp                    Planetary ephemeris SPK,
                                  subsetted to cover only
                                  time range of interest.
   earthstns_itrf93_050714.bsp    DSN station SPK.
   earth_topo_050714.tf           DSN station frame definitions.
   earth_000101_060525_060303.bpc Binary PCK for Earth.
   naif0008.tls                   Generic LSK.
   ORMM__040501000000_00076XS.BSP MEX Orbiter trajectory SPK,
                                  subsetted to cover only
                                  time range of interest.
                                  pck00008.tpc Generic PCK.

   \begindata
   PATH_VALUES     = ('/Users/lheffern/PycharmProjects/SPICEworkshop/MEXkernels')
   PATH_SYMBOLS    = ('KERNELS'    )
   KERNELS_TO_LOAD = ( '$KERNELS/spk/de405xs.bsp',
   '$KERNELS/spk/earthstns_itrf93_050714.bsp',
   '$KERNELS/fk/earth_topo_050714.tf',
   '$KERNELS/pck/earth_000101_060525_060303.bpc',
   '$KERNELS/lsk/naif0008.tls',
   '$KERNELS/spk/ORMM__040501000000_00076XS.BSP',
   '$KERNELS/pck/pck00008.tpc' )

   \begintext