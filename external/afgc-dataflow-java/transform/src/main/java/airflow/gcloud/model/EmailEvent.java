package airflow.gcloud.model;

import java.io.Serializable;


public class EmailEvent implements Serializable {

    String timestamp;
    String event;
    String email;
    String campaign;
    String id;

}
