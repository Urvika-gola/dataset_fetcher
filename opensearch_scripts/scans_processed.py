import sys
from opensearchpy import OpenSearch, helpers
from datetime import datetime

"""
Script to find unique scans in Level 0, 1 and 2
Usage python scans_processed.py <season> <crop>
"""

def run_query(client, index, query):
    """
    Run the Query on OpenSearch server
    """
    response = client.search(index=index, body=query)
    return response

def convert_date_format(date_str):
    """
    Convert date from (eg) 20230308T012740.989Z to 2023-03-08__01-27-40-989
    """
    original_format = '%Y%m%dT%H%M%S.%fZ'
    dt = datetime.strptime(date_str, original_format)
    # Reformat to the format used in phytooracle project
    new_format = '%Y-%m-%d__%H-%M-%S-%f'
    return dt.strftime(new_format)[:-3]  # Remove the last three digits of microseconds

def create_query(level, crop, season):
    """
    Create JSON Query to get the unique scan dates for a given level, crop, and season
    """
    return {
    "size": 0,
    "query": {
        "bool": {
            "must": [
                {"match": {"level": level}},
                {"match": {"crop_type": crop}},
                {"match": {"season": season}}
            ]
        }
    },
    "aggs": {
        "unique_scan_dates": {
            "terms": {
                "field": "scan_date",
                "size": 100
            }
        }
    }
}
if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python scans_processed.py <season> <crop>")
        sys.exit(1)

    # Extract season and crop from command line arguments
    season = int(sys.argv[1])
    crop = sys.argv[2]

    host = 'localhost'
    port = 9200
    auth = ('admin', 'admin') # For testing only.
    
    # Create the client with SSL/TLS and hostname verification disabled.
    client = OpenSearch(
        hosts = [{'host': host, 'port': port, 'scheme': 'https'}],
        http_compress = True, # enables gzip compression for request bodies
        http_auth = auth,
        use_ssl = True,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False
    )

    # Executing the queries
    # Get key_as_string as an alias for scan_date because due to aggregative above, the key used to aggregate is the epoch time

    response_level_0 = run_query(client, "phytooracle-index", create_query(level=0, crop=crop, season=season))
    dates_level_0 = set([bucket['key_as_string'] for bucket in response_level_0['aggregations']['unique_scan_dates']['buckets']])

    response_level_1 = run_query(client, "phytooracle-index", create_query(level=1, crop=crop, season=season))
    dates_level_1 = set([bucket['key_as_string'] for bucket in response_level_0['aggregations']['unique_scan_dates']['buckets']])

    response_level_2 = run_query(client, "phytooracle-index", create_query(level=2, crop=crop, season=season))
    dates_level_2 = set([bucket['key_as_string'] for bucket in response_level_2['aggregations']['unique_scan_dates']['buckets']])

    unique_dates = dates_level_0 - dates_level_2
    diff = dates_level_2 - dates_level_0

    formatted_dates = [convert_date_format(date) for date in unique_dates]

    print("Number of Scans that processed to level 0:", len(dates_level_0))
    print("Number of Scans that processed to level 1:", len(dates_level_1))
    print("Number of Scans that processed to level 2:", len(dates_level_2))
    print("\nScans that did not process to level 2 from level 0:", formatted_dates)
