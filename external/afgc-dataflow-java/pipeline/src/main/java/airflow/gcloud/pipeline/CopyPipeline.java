package airflow.gcloud.pipeline;

import com.google.cloud.dataflow.sdk.Pipeline;
import com.google.cloud.dataflow.sdk.io.TextIO;
import com.google.cloud.dataflow.sdk.options.Description;
import com.google.cloud.dataflow.sdk.options.PipelineOptions;
import com.google.cloud.dataflow.sdk.options.PipelineOptionsFactory;

import java.io.IOException;


public class CopyPipeline {

    private interface Options extends PipelineOptions {
        @Description("Path of the file to read from")
        String getIn();

        void setIn(String value);

        @Description("Path of the file to write to")
        String getOut();

        void setOut(String value);
    }

    public static void main(String[] args) throws IOException {
        Options options = PipelineOptionsFactory.fromArgs(args).withValidation().as(Options.class);
        Pipeline pipeline = Pipeline.create(options);

        pipeline.apply(TextIO.Read.from(options.getIn()))
                .apply(TextIO.Write.to(options.getOut()));

        pipeline.run();
    }

}
