package airflow.gcloud.transform;

import com.google.cloud.dataflow.sdk.transforms.DoFn;
import airflow.gcloud.model.EmailEvent;

public class NoopFn extends DoFn<EmailEvent, EmailEvent> {
    private static final long serialVersionUID = 0;

    @Override
    public void processElement(ProcessContext c) throws Exception {
        EmailEvent element = c.element();
        c.output(element);
    }
}

