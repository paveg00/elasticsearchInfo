# Поднимем докер и кибану(OpenSearch)

```bash
docker-compose -f demo/elk_docker_compose.yaml up -d
```

# Поработаем клиентом эластика

```bash
# Создаем темплейты
python3 demo/app/load.py create_templates

# Создаем индекс аэропортов
python3 demo/app/load.py create_index

# Проверим, что индекс создался
python3 demo/app/load.py list_indexes

green open airport-2023-05-17-22-53-13  JDOLRoCDTryqwL9WioIB4A 1 1   0 0    416b    208b
green open security-auditlog-2023.05.17 kmXDkwhHRIe3yvlk8xvMDQ 1 1 323 0   1.3mb 697.9kb
green open .opensearch-observability    lqwdNBqZQ3CF0iUAK3Iyow 1 1   0 0    416b    208b
green open airport-2023-05-17-23-45-23  K5c1KPfbT6qBZGCLDd_LNQ 1 1   0 0    416b    208b
green open .kibana_92668751_admin_1     ZqlRtMuSR6G7dopDzspyWg 1 1   2 0  22.8kb  11.4kb
green open .kibana_1                    xCrqy4t7Q66JC2Wbv6CuRQ 1 1   0 0    416b    208b
green open .opendistro_security         _TizowA1QO6SAZ_1oCrk0Q 1 1  10 0 145.9kb  72.9kb


# Заливаем данные в индекс аэропортов
python3 demo/app/load.py load_data
```

Посмотрим: данные в кибане появились

![Пример kibana на данных аэропортов](/images/example_airport.png)


```bash

// Время полнотекстового поиска по полю "name"
python3 demo/app/load.py search_airport vnukovo
{
    "took": 6,
    "timed_out": false,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 1,
            "relation": "eq"
        },
        "max_score": 10.609816,
        "hits": [
            {
                "_index": "airport",
                "_id": "3a0b364a-ae24-4930-a6b2-641be3f7d480",
                "_score": 10.609816,
                "_source": {
                    "ident": "UUWW",
                    "type": "large_airport",
                    "name": "Vnukovo International Airport",
                    "elevation_ft": "685",
                    "continent": "EU",
                    "iso_country": "RU",
                    "iso_region": "RU-MOS",
                    "municipality": "Moscow",
                    "gps_code": "UUWW",
                    "iata_code": "VKO",
                    "local_code": "",
                    "coordinates": "55.5914993286, 37.2615013123"
                }
            }
        ]
    }
}
```



```
// Удаляем индекс
python3 demo/app/load.py load_data delete_index

```