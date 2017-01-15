from datetime import timedelta, datetime

from airflow import DAG
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator, \
    DataprocClusterDeleteOperator
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator

yesterday = datetime.combine(datetime.today() - timedelta(1),
                             datetime.min.time())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': yesterday,
    'email': ['alex@vanboxel.be'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}

with DAG('v1_8_dataproc', schedule_interval=timedelta(days=1),
         default_args=default_args) as dag:
    def should_run(ds, **kwargs):

        if datetime.now() < kwargs['execution_date'] + timedelta(days=2):
            return "start_cluster"
        else:
            return "no_run"


    start = BranchPythonOperator(
        task_id='start',
        provide_context=True,
        python_callable=should_run,
    )

    start_cluster = DataprocClusterCreateOperator(
        task_id='start_cluster',
        cluster_name='smoke-cluster-{{ ds_nodash }}',
        project_id=Variable.get('gc_project'),
        num_workers=2,
        num_preemptible_workers=1,
        properties={
            'spark:spark.executorEnv.PYTHONHASHSEED': '0',
            'spark:spark.yarn.am.memory': '1024m',
            'spark:spark.sql.avro.compression.codec': 'deflate'
        },
        worker_disk_size=50,
        master_disk_size=50,
        labels={
            'example': 'label'
        },
        zone=Variable.get('gc_zone'),
        google_cloud_conn_id='gcp_smoke'
    )

    stop_cluster = DataprocClusterDeleteOperator(
        task_id='stop_cluster',
        cluster_name='smoke-cluster-{{ ds_nodash }}',
        project_id=Variable.get('gc_project'),
        google_cloud_conn_id='gcp_smoke'
    )

    no_run = DummyOperator(task_id='no_run')

    end = DummyOperator(
        trigger_rule='one_success',
        task_id='end')

    start >> start_cluster >> stop_cluster >> end
    start >> no_run >> end
