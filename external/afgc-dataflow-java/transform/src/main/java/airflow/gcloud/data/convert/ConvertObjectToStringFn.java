package airflow.gcloud.data.convert;

import com.google.cloud.dataflow.sdk.transforms.DoFn;

public class ConvertObjectToStringFn extends DoFn<Object, String> {
    @Override
    public void processElement(ProcessContext c) throws Exception {
        c.output(c.element().toString());
    }
}
