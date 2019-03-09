geolite2_city_url = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz"
geolite2_city_md5_url = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz.md5"
geolite2_city_name = "GeoLite2-City.mmdb"
geolite2_city_archive_name = "GeoLite2-City.tar.gz"

geolite2_country_url = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz"
geolite2_country_md5_url = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz.md5"
geolite2_country_name = "GeoLite2-Country.mmdb"
geolite2_country_archive_name = "GeoLite2-Country.tar.gz"

geolite2_asn_url = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN.tar.gz"
geolite2_asn_md5_url = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN.tar.gz.md5"
geolite2_asn_name = "GeoLite2-ASN.mmdb"
geolite2_asn_archive_name = "GeoLite2-ASN.tar.gz"

geolite2_databases_urls = [geolite2_city_url, geolite2_country_url, geolite2_asn_url]
geolite2_databases_url_md5 = {
    geolite2_city_url: geolite2_city_md5_url,
    geolite2_country_url: geolite2_country_md5_url,
    geolite2_asn_url: geolite2_asn_md5_url
}
geolite2_databases_name_url = {
    geolite2_city_name: geolite2_city_url,
    geolite2_country_name: geolite2_country_url,
    geolite2_asn_name: geolite2_asn_url
}
geolite2_databases_url_name = {
    geolite2_city_url: geolite2_city_name,
    geolite2_country_url: geolite2_country_name,
    geolite2_asn_url: geolite2_asn_name
}
geolite2_databases_archive_name = {
    geolite2_city_archive_name: geolite2_city_name,
    geolite2_country_archive_name: geolite2_country_name,
    geolite2_asn_archive_name: geolite2_asn_name
}

database_location = ""
