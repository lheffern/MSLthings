KPL/MK

    This is the meta-kernel used in the solution of the
    "figuring out MAVEN's orbit over MSL"

    File name Contents
    -------------------------- -----------------------------
    naif0008.tls                Generic LSK
    mar085s.bsp                 Mars Ephemeris different dates
    mar097s.bsp                 Mars Ephemeris different dates
    msl_ls_ops120808_iau2000_v1.bsp Mars IAU thing
    msl_surf_rover_loc.bsp      MSL SPK
    maven_orb.bsp               MAVEN Ephemeris
    de430s.bsp                  SBC
    maven_orb_rec.bsp           More MAVEN SPK
    maven_struct_v01.bsp        More MAVEN SPK
    maven_orb_rec_170101_170401_v1.bsp
    maven_orb_rec_170401_170701_v1.bsp
    maven_orb_rec_170701_171001_v1.bsp
    naif.jpl.nasa.gov_pub_naif_MSL_kernels_pck_pck00008.tpc.txt
                                PCK for MSL

    \begindata
    PATH_VALUES     = ('/Users/lheffern/PycharmProjects/SPICEworkshop/kernels')
    PATH_SYMBOLS    = ('KERNELS'    )
    KERNELS_TO_LOAD = ( '$KERNELS/lsk/naif0008.tls',
                        '$KERNELS/spk/mar085s.bsp',
                        '$KERNELS/spk/mar097s.bsp',
                        '$KERNELS/spk/msl_ls_ops120808_iau2000_v1.bsp'
                        '$KERNELS/spk/msl_surf_rover_loc.bsp',
                        '$KERNELS/spk/maven_orb.bsp',
                        '$KERNELS/spk/maven_orb_rec_170101_170401_v1.bsp',
                        '$KERNELS/spk/maven_orb_rec_170401_170701_v1.bsp',
                        '$KERNELS/spk/maven_orb_rec_170701_171001_v1.bsp',
                        '$KERNELS/spk/de430s.bsp' ,
                        '$KERNELS/spk/maven_orb_rec.bsp'
                        '$KERNELS/spk/maven_struct_v01.bsp'
                        '$KERNELS/pck/+',
                        'naif.jpl.nasa.gov_pub_naif_MSL_kernels_pck_pck00008.tpc.txt')

    \begintext
