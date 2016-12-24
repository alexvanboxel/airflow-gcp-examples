package airflow.gcloud.pipeline;

import airflow.gcloud.BqSchemaFor;
import com.google.cloud.dataflow.sdk.Pipeline;
import com.google.cloud.dataflow.sdk.io.BigQueryIO;
import com.google.cloud.dataflow.sdk.options.DataflowPipelineOptions;
import com.google.cloud.dataflow.sdk.options.Description;
import com.google.cloud.dataflow.sdk.options.PipelineOptionsFactory;
import com.google.cloud.dataflow.sdk.options.ValueProvider;

import java.io.IOException;


public class Bq2BqPipeline {

    private interface Options extends DataflowPipelineOptions {
        @Description("Path of the file to read from")
        ValueProvider<String> getIn();

        void setIn(ValueProvider<String> value);

        @Description("Path of the file to write to")
        ValueProvider<String> getOut();

        void setOut(ValueProvider<String> value);
    }

    public static void main(String[] args) throws IOException {
        Options options = PipelineOptionsFactory.fromArgs(args).withValidation().as(Options.class);
        Pipeline pipeline = Pipeline.create(options);

        pipeline.apply(BigQueryIO.Read.from(options.getIn()))
                .apply(BigQueryIO.Write.to(options.getOut()).withSchema(BqSchemaFor.gsob()));

        pipeline.run();
    }

}
