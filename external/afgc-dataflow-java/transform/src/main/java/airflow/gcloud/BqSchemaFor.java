package airflow.gcloud;

import com.google.api.services.bigquery.model.TableFieldSchema;
import com.google.api.services.bigquery.model.TableSchema;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by alexvanboxel on 24/12/16.
 */
public class BqSchemaFor {

    public static TableSchema gsob() throws IOException {
        List<TableFieldSchema> fields = new ArrayList<>();
        fields.add(new TableFieldSchema().setName("partition_date").setType("DATE").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("temperature_mean").setType("FLOAT").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("temperature_min").setType("FLOAT").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("temperature_max").setType("FLOAT").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("dew_point_mean").setType("FLOAT").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("pressure_sea_level_mean").setType("FLOAT").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("pressure_station_level_mean").setType("FLOAT").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("visibility_mean").setType("FLOAT").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("wind_speed_mean").setType("FLOAT").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("wind_speed_sustained_max").setType("FLOAT").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("precipitation").setType("FLOAT").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("snow_depth").setType("FLOAT").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("fog").setType("BOOLEAN").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("rain_drizzle").setType("BOOLEAN").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("snow_ice_pellets").setType("BOOLEAN").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("hail").setType("BOOLEAN").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("thunder").setType("BOOLEAN").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("tornado_funnel_cloud").setType("BOOLEAN").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("usaf").setType("INTEGER").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("wban").setType("INTEGER").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("station_name").setType("STRING").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("station_country").setType("STRING").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("station_state").setType("STRING").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("station_latitude").setType("FLOAT").setMode("NULLABLE"));
        fields.add(new TableFieldSchema().setName("station_longitude").setType("FLOAT").setMode("NULLABLE"));
        return new TableSchema().setFields(fields);
    }
}


