{
    "mappings": {
      "properties": {
        "plant_name": {
          "type": "text"
        },
        "genotype": {
          "type": "keyword"
        },
        "season": {
          "type": "integer"
        },
        "crop_type": {
          "type": "keyword"
        },
        "year_of_planting": {
          "type": "integer"
        },
        "level": {
          "type": "integer"
        },
        "instrument": {
          "type": "keyword"
        },
        "scan_date": {
          "type": "date",
          "format": "basic_date_time"
        },
        "id": {
          "type": "keyword"
        },
        "files": {
          "type": "nested",
          "properties": {
            "block": {
              "type": "text"
            },
            "file_size": {
              "type": "text"
            },
            "path": {
              "type": "text"
            },
            "filename": {
              "type": "text"
            }
          }
        }
      }
    }
  }
    