# latest-indonesia-earthquake
this package will get the latest earthquake from BMKG -Meteorology, Climatology, and Geophysics Agency

## HOW IT WORKS ?

This package uses beautifllsoup4 and a request which will produce a jSON file output that is ready to be used for web 
or mobile applications


import gempaterkini

if __name__ == '__main__' :

    print('Aplikasi utama')

    result = gempaterkini.ekstraksi_data()

    gempaterkini.tampilkan_data(result)