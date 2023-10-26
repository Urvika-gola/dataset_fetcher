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
          "type": "keyword"
        },
        "id": {
          "type": "keyword"
        },
        "files": {
          "type": "nested",
          "properties": {
            "block": {
              "type": "integer"
            },
            "file_size": {
              "type": "integer"
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
    