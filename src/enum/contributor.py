from enum import Enum


class Contributor(Enum):
    """
    A Enum that represents all earthquake data contributors. Use this enum in EarthquakeQuery class to set its
    parameters related to contributors.
    """
    CONTRIBUTOR_ADMIN = "admin"
    """
    Admin - Administrator
    """

    CONTRIBUTOR_AK = "ak"
    """
    AK - Alaska Earthquake Center
    """

    CONTRIBUTOR_AT = "at"
    """
    AT - National Tsunami Warning Center
    """

    CONTRIBUTOR_ATLAS = "atlas"
    """
    ATLAS - ShakeMap Atlas
    """

    CONTRIBUTOR_AV = "av"
    """
    AV - Alaska Volcano Observatory
    """

    CONTRIBUTOR_CGS = "cgs"
    """
    California Geological Survey
    """

    CONTRIBUTOR_CI = "ci"
    """
    CI - California Integrated Seismic Network: Southern, California Seismic Network (Caltech/USGS Pasadena and Partners) 
    and Southern California Earthquake Data Center
    """

    CONTRIBUTOR_EW = "ew"
    """
    EW - EW database
    """

    CONTRIBUTOR_HV = "hv"
    """
    HV - Hawaii Volcano Observatory
    """

    CONTRIBUTOR_ISMP = "ismp"
    """
    ISMP - USGS Induced Seismicity Project
    """

    CONTRIBUTOR_LD = "ld"
    """
    LD - Lamont-Doherty Cooperative Seismographic Network
    """

    CONTRIBUTOR_MB = "mb"
    """
    MB - Montana Bureau of Mines and Geology
    """

    CONTRIBUTOR_NC = "nc"
    """
    NC - California Integrated Seismic Network: Northern California Seismic System 
    (UC Berkeley, USGS Menlo Park, and Partners)
    """

    CONTRIBUTOR_NM = "nm"
    """
    NM - New Madrid Seismic Network
    """

    CONTRIBUTOR_NN = "nn"
    """
    NN - Nevada Seismological Laboratory
    """

    CONTRIBUTOR_NP = "np"
    """
    NP - NP Contributor
    """

    CONTRIBUTOR_OFFICIAL = "official"
    """
    Official - United States Geological Survey
    """

    CONTRIBUTOR_OK = "ok"
    """
    OK - Oklahoma Geological Survey Statewide Network, Norman, USA (aka TUL, OGS)
    """

    CONTRIBUTOR_PR = "pr"
    """
    PR - Puerto Rico Seismic Network
    """

    CONTRIBUTOR_PT = "pt"
    """
    PT - Pacific Tsunami Warning Center
    """

    CONTRIBUTOR_SE = "se"
    """
    SE - Center for Earthquake Research and Information
    """

    CONTRIBUTOR_TX = "tx"
    """
    TX - Texas Seismological Network (TexNet) (aka TEXNET, BEG)
    """

    CONTRIBUTOR_US = "us"
    """
    US - USGS National Earthquake Information Center, PDE (aka GS, NEIC)
    """

    CONTRIBUTOR_UU = "uu"
    """
    UU - University of Utah Seismograph Stations
    """

    CONTRIBUTOR_UW = "uw"
    """
    UW - Pacific Northwest Seismic Network
    """