# Configuration
Clickhouse configuration 설정할 부분

## Changes
- **config.xml**
    - `<path>/data/clickhouse</path>`
    - `<tmp_path>/data/clickhouse/tmp</tmp_path>`
    - `<user_files_path>/data/clickhouse/user_files</user_files_path>`
    - `<format_schema_path>/data/clickhouse/format_schemas</format_schema_path>`
    - uncomment `<listen_host>0.0.0.0</listen_host>` : allow external access
- **config.d/data-paths.xml**
    ```
    <path>/data/clickhouse</path>
    <tmp_path>/data/clickhouse/tmp</tmp_path>
    <user_files_path>/data/clickhouse/user_files</user_files_path>
    <format_schema_path>/data/clickhouse/format_schemas</format_schema_path>
    ```