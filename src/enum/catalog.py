from enum import Enum


class Catalog(Enum):
    """
    A Enum that represents all earthquake data Catalogs. Use this enum in EarthquakeQuery class to set its parameters
    related to catalogs.
    """
    CATALOG_AACSE = "aacse"
    """
    AACSE - Alaska Amphibious Community Seismic Experiment 
    """

    CATALOG_AK = "ak"
    """
    AK - Alaska Earthquake Center
    """

    CATALOG_AT = "at"
    """
    AT - National Tsunami Warning Center
    """

    CATALOG_ATLAS = "atlas"
    """
    ATLAS - ShakeMap Atlas
    """

    CATALOG_AV = "av"
    """
    AV - Alaska Volcano Observatory
    """

    CATALOG_CDMG = "cdmg"
    """
    CDMG - California Division of Mines and Geology
    """

    CATALOG_CGS = "cgs"
    """
    California Geological Survey
    """

    CATALOG_CHOY = "choy"
    """
    CHOY - Energy Magnitude and Broadband Depth
    """

    CATALOG_CI = "ci"
    """
    CI - California Integrated Seismic Network: Southern, California Seismic Network (Caltech/USGS Pasadena and Partners) 
    and Southern California Earthquake Data Center
    """

    CATALOG_CIDEV = "cidev"
    """
    CIDEV - CIDEV database
    """

    CATALOG_DR = "dr"
    """
    DR = DR database
    """

    CATALOG_DUPUTEL = "duputel"
    """
    DUPUTEL - Duputel et al. W phase catalog
    """

    CATALOG_EQH = "eqh"
    """
    EQH - Coffman, von Hake and Stover, Earthquake History of the United States
    """

    CATALOG_EW = "ew"
    """
    EW - EW database
    """

    CATALOG_EW_DM = "ew_dm"
    """
    EW_DM - EW_DM database
    """

    CATALOG_GCMT = "gcmt"
    """
    GCMT - Lamont-Doherty Earth Observatory Global CMT project, New York, USA
    """

    CATALOG_GSC = "gsc"
    """
    Geological Survey of Canada
    """

    CATALOG_HV = "hv"
    """
    HV - Hawaii Volcano Observatory
    """

    CATALOG_ID = "id"
    """
    ID - ID database
    """

    CATALOG_IS = "is"
    """
    IS - IS database
    """

    CATALOG_ISCGEM = "iscgem"
    """
    ISCGEM - ISC-GEM Main Catalog
    """

    CATALOG_ISCGEMSUP = "iscgemsup"
    """
    ISCGEMSUP - ISC-GEM Supplementary Catalog
    """

    CATALOG_ISMPKANSAS = "ismpkansas"
    """
    ISMPKANSAS - USGS Induced Seismicity Project (Kansas)
    """

    CATALOG_LD = "ld"
    """
    LD - Lamont-Doherty Cooperative Seismographic Network
    """

    CATALOG_MB = "mb"
    """
    MB - Montana Bureau of Mines and Geology
    """

    CATALOG_NC = "nc"
    """
    NC - California Integrated Seismic Network: Northern California Seismic System 
    (UC Berkeley, USGS Menlo Park, and Partners)
    """

    CATALOG_NE = "ne"
    """
    NE - New England Seismic Network
    """

    CATALOG_NM = "nm"
    """
    NM - New Madrid Seismic Network
    """

    CATALOG_NN = "nn"
    """
    NN - Nevada Seismological Laboratory
    """

    CATALOG_OFFICIAL = "official"
    """
    OFFICIAL - USGS Earthquake Magnitude Working Group
    """

    CATALOG_OFFICIAL19631013051759_30 = "official19631013051759_30"
    """
    OFFICIAL - USGS Earthquake Magnitude Working Group
    """

    CATALOG_OK = "ok"
    """
    OK - Oklahoma Geological Survey Statewide Network, Norman, USA (aka TUL, OGS)
    """

    CATALOG_OTT = "ott"
    """
    Geological Survey of Canada, Ottawa, Canada
    """

    CATALOG_PR = "pr"
    """
    PR - Puerto Rico Seismic Network
    """

    CATALOG_PT = "pt"
    """
    PT - Pacific Tsunami Warning Center
    """

    CATALOG_SC = "sc"
    """
    SC - SC database
    """

    CATALOG_SE = "se"
    """
    SE - Center for Earthquake Research and Information
    """

    CATALOG_TX = "tx"
    """
    TX - Texas Seismological Network (TexNet) (aka TEXNET, BEG)
    """

    CATALOG_UNKNOWN = "unknown"
    """
    UNKNOWN = Unknown database
    """

    CATALOG_US = "us"
    """
    US - USGS National Earthquake Information Center, PDE
    """

    CATALOG_USAUTO = "usauto"
    """
    USAUTO - USAUTO database
    """

    CATALOG_USHIS = "ushis"
    """
    USHIS - Stover and Coffman, Seismicity of the United States, 1568-1989
    """

    CATALOG_UU = "uu"
    """
    UU - University of Utah Seismograph Stations
    """

    CATALOG_UW = "uw"
    """
    UW - Pacific Northwest Seismic Network
    """

    CATALOG_EQUALC = "=c"
    """
    =C - =C Database
    """

    CATALOG_38457511 = "38457511"
    """
    38457511 - 38457511 Database
    """