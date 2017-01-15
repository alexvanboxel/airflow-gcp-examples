from datetime import timedelta, datetime

from airflow import DAG
from airflow.contrib.sensors.gcs_sensor import GoogleCloudStorageObjectSensor, \
    GoogleCloudStorageObjectUpdatedSensor

seven_days_ago = datetime.combine(datetime.today() - timedelta(7),
                                  datetime.min.time())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': seven_days_ago,
    'email': ['alex@vanboxel.be'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}

with DAG('v1_8_cloud_storage', schedule_interval=timedelta(days=1),
         default_args=default_args) as dag:
    sens_object_create = GoogleCloudStorageObjectSensor(
        task_id='sens_object_create',
        bucket='{{var.value.gcs_bucket}}',
        object='{{var.value.gcs_root}}/gcp_smoke_bq/bq_to_gcp_avro/{{ ds_nodash }}/part-000000000000.avro',
        google_cloud_conn_id='gcp_smoke'
    )

    sens_object_update = GoogleCloudStorageObjectUpdatedSensor(
        task_id='sens_object_update',
        bucket='{{var.value.gcs_bucket}}',
        object='{{var.value.gcs_root}}/gcp_smoke_bq/bq_to_gcp_avro/99999999/part-000000000000.avro',
        google_cloud_conn_id='gcp_smoke'
    )
