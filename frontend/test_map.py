import psycopg2
import psycopg2.extras
import pandas as pd
import plotly.express as px
import geopandas as gpd


conn = psycopg2.connect("""
    host=rc1b-7dcuebkqzirwnxee.mdb.yandexcloud.net
    port=6432
    sslmode=verify-full
    dbname=db
    user=user
    password=MfjQkR6zh6aCG7q4
""")
q = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def show_all_camers(district_id):
    detectors_query = """
    select 
        lat, lon, regions.name as region_name, det_coords.address, distric_points.district_id
    from distric_points 
        join regions 
        on regions.district_id = distric_points.district_id

        join det_coords
        on distric_points.device_id = det_coords.device_id::text;
    """

    q.execute(detectors_query)
    detectors_coords = pd.DataFrame(q.fetchall())
    detectors_coords['device_type'] = 'detector'

    cameras_query = """
    select 
        lat, lon, regions.name as region_name, cameras.address, distric_points.district_id
    from distric_points 
        join regions 
        on regions.district_id = distric_points.district_id

        join cameras
        on distric_points.device_id = cameras.device_id;
    """

    q.execute(cameras_query)
    cameras_coords = pd.DataFrame(q.fetchall())
    cameras_coords['device_type'] = 'camera'

    invalid_grz_detector_cameras_query = """
    select 
        lat, lon, regions.name as region_name, cameras.address, distric_points.district_id
    from distric_points 
        join regions 
        on regions.district_id = distric_points.district_id

        join cameras
        on distric_points.device_id = cameras.device_id

        join disable_cameras_grz
        on disable_cameras_grz.camera = cameras.device_id;
    """

    q.execute(invalid_grz_detector_cameras_query)
    invalid_grz_detector_cameras_coords = pd.DataFrame(q.fetchall())
    invalid_grz_detector_cameras_coords['device_type'] = 'not confident camera'
    invalid_grz_detector_cameras_coords['reason'] = 'mistakes in grz detection'

    invalid_speed_detector_cameras_query = """
    select 
        lat, lon, regions.name as region_name, cameras.address, distric_points.district_id
    from distric_points 
        join regions 
        on regions.district_id = distric_points.district_id

        join cameras
        on distric_points.device_id = cameras.device_id

        join disable_cameras_speed
        on disable_cameras_speed.camera = cameras.device_id;
    """
    q.execute(invalid_speed_detector_cameras_query)
    invalid_speed_detector_cameras_coords = pd.DataFrame(q.fetchall())
    invalid_speed_detector_cameras_coords['device_type'] = 'not confident camera'
    invalid_speed_detector_cameras_coords['reason'] = 'mistakes in speed detection'

    invalid_devices = pd.concat(
        [
            invalid_speed_detector_cameras_coords,
            invalid_grz_detector_cameras_coords
        ]
    )


    print(detectors_coords.columns)
    devices_df = pd.concat([detectors_coords[detectors_coords['district_id']==district_id], cameras_coords[cameras_coords['district_id']==district_id], invalid_devices[invalid_devices['district_id']==district_id]])
    geo_df = gpd.GeoDataFrame(devices_df,
                              geometry=gpd.points_from_xy(
                                  x=devices_df['lon'],
                                  y=devices_df['lat']
                              ))

    fig = px.scatter_mapbox(geo_df,
                            lat='lat',
                            lon='lon',
                            hover_data=[
                                "region_name", "device_type", "reason"
                            ],
                            color='device_type',
                            mapbox_style="open-street-map",
                            width=1000,
                            height=800
                            )

    return fig
