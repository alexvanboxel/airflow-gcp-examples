from datetime import timedelta, datetime

from airflow import DAG
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.operators.bigquery_to_gcs import BigQueryToCloudStorageOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator

from dags.support import schemas

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

with DAG('v1_8_bigquery', schedule_interval=timedelta(days=1),
         default_args=default_args) as dag:
    bq_extract_one_day = BigQueryOperator(
        task_id='bq_extract_one_day',
        bql='gcp_smoke/gsob_extract_day.sql',
        destination_dataset_table=
        '{{var.value.gcq_dataset}}.gsod_partition{{ ds_nodash }}',
        write_disposition='WRITE_TRUNCATE',
        bigquery_conn_id='gcp_smoke',
        use_legacy_sql=False
    )

    bq2gcp_avro = BigQueryToCloudStorageOperator(
        task_id='bq2gcp_avro',
        source_project_dataset_table='{{var.value.gcq_dataset}}.gsod_partition{{ ds_nodash }}',
        destination_cloud_storage_uris=[
            'gs://{{var.value.gcs_bucket}}/{{var.value.gcs_root}}/gcp_smoke_bq/bq_to_gcp_avro/{{ ds_nodash }}/part-*.avro'
        ],
        export_format='AVRO',
        bigquery_conn_id='gcp_smoke',
    )

    bq2gcp_override = BigQueryToCloudStorageOperator(
        task_id='bq2gcp_override',
        source_project_dataset_table='{{var.value.gcq_dataset}}.gsod_partition{{ ds_nodash }}',
        destination_cloud_storage_uris=[
            'gs://{{var.value.gcs_bucket}}/{{var.value.gcs_root}}/gcp_smoke_bq/bq_to_gcp_avro/99999999/part-*.avro'
        ],
        export_format='AVRO',
        bigquery_conn_id='gcp_smoke',
    )

    gcs2bq_avro_auto_schema = GoogleCloudStorageToBigQueryOperator(
        task_id='gcs2bq_avro_auto_schema',
        bucket='{{var.value.gcs_bucket}}',
        source_objects=[
            '{{var.value.gcs_root}}/gcp_smoke_bq/bq_to_gcp_avro/{{ ds_nodash }}/part-*'
        ],
        destination_project_dataset_table='{{var.value.gcq_tempset}}.avro_auto_schema{{ ds_nodash }}',
        source_format='AVRO',
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_TRUNCATE',
        google_cloud_storage_conn_id='gcp_smoke',
        bigquery_conn_id='gcp_smoke'
    )

    gcs2bq_avro_with_schema = GoogleCloudStorageToBigQueryOperator(
        task_id='gcs2bq_avro_with_schema',
        bucket='{{var.value.gcs_bucket}}',
        source_objects=[
            '{{var.value.gcs_root}}/gcp_smoke_bq/bq_to_gcp_avro/{{ ds_nodash }}/part-*'
        ],
        destination_project_dataset_table='{{var.value.gcq_tempset}}.avro_with_schema{{ ds_nodash }}',
        source_format='AVRO',
        schema_fields=schemas.gsob(),
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_TRUNCATE',
        google_cloud_storage_conn_id='gcp_smoke',
        bigquery_conn_id='gcp_smoke'
    )

    bq_extract_one_day >> bq2gcp_avro >> bq2gcp_override
    bq2gcp_avro >> gcs2bq_avro_auto_schema
    bq2gcp_avro >> gcs2bq_avro_with_schema
