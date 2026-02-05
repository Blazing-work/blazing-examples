# Blazing Examples Extraction Summary

**Date:** 2026-02-05
**Total Examples:** 108
**Extraction Status:** Complete

## Summary By Product

- blazing-core: 1
- blazing-flow: 75
- blazing-flow-endpoint: 18
- blazing-flow-sandbox: 16

## Summary By Category

- API Patterns: 8
- Advanced: 14
- Async & Parallel: 4
- Data Processing: 10
- Deployment & Packaging: 9
- GPU & Agents: 3
- Getting Started: 9
- Integrations: 9
- Machine Learning: 1
- Platform Integrations: 7
- Runtime & Routing: 10
- Sandbox & Isolation: 6
- Web Endpoints: 7
- Web Endpoints Advanced: 11

## Lexicon

All examples are written for the v2.0 lexicon and include `@app.step`, `@app.workflow`, and `@app.service` where appropriate. `services=None` is used consistently for dependency injection.

## Structure

Each example directory includes:
- `flow.py`
- `meta.json`
- `EXPECTED_OUTPUT.md`

## Index

### API Patterns
- API Execution Patterns (`07_api_patterns/api_execution_patterns/flow.py`)
- Callable Workflows (`07_api_patterns/callable_workflows/flow.py`)
- Decorators and Context Manager (`07_api_patterns/decorators_and_context/flow.py`)
- run_sync by Name (`07_api_patterns/run_sync_by_name/flow.py`)
- SyncBlazing Quickstart (`07_api_patterns/syncblazing_quickstart/flow.py`)
- wait_result_sync Helper (`07_api_patterns/wait_result_sync/flow.py`)
- Workflow Handle wait()/cancel() (`07_api_patterns/workflow_handle_wait_cancel/flow.py`)
- Workflow Version Pins (`07_api_patterns/workflow_version_pins/flow.py`)

### Advanced
- Batch Stock Processing (`06_advanced/batch_stock_processing/flow.py`)
- Cleanup Expired Records (`06_advanced/cleanup_expired_records/flow.py`)
- Daily Report Generation (`06_advanced/daily_reports/flow.py`)
- Event Stream Processor (`06_advanced/event_stream_processor/flow.py`)
- Health Check Workflow (`06_advanced/health_check_workflow/flow.py`)
- Modular Registration Pattern (`06_advanced/modular_registration/flow.py`)
- Sandbox: Async Service Calls (`06_advanced/sandbox_async_service_calls/flow.py`)
- Sandbox: Basic User-Provided Transform (`06_advanced/sandbox_basic_transform/flow.py`)
- Sandbox: Service Bridge with Database (`06_advanced/sandbox_database_service/flow.py`)
- Sandbox: Multi-Tenant Data Processing (`06_advanced/sandbox_multi_tenant/flow.py`)
- Sandbox: Service Bridge with REST APIs (`06_advanced/sandbox_rest_api_service/flow.py`)
- Sandbox: Security Validation (`06_advanced/sandbox_security_validation/flow.py`)
- Sandboxed Step Execution (`06_advanced/sandboxed_step_execution/flow.py`)
- Trading Strategy Sandbox (`06_advanced/trading_strategy_sandbox/flow.py`)

### Async & Parallel
- CPU vs I/O Optimization with Worker Types (`04_async_parallel/cpu_vs_io_optimization/flow.py`)
- Fan-Out / Fan-In Pattern (`04_async_parallel/fan_out_fan_in/flow.py`)
- Parallel Data Processing (`04_async_parallel/parallel_processing/flow.py`)
- Rate-Limited API Calls (`04_async_parallel/rate_limited_api/flow.py`)

### Data Processing
- Aggregating Results (`03_data_processing/aggregating_results/flow.py`)
- CSV Import Pipeline (`03_data_processing/csv_import/flow.py`)
- ETL Pipeline (`03_data_processing/etl_pipeline/flow.py`)
- Event Processing Pipeline (`03_data_processing/event_processing/flow.py`)
- Large DataFrame Processing with Arrow Flight (`03_data_processing/large_dataframe_processing/flow.py`)
- Map-Reduce Pattern (`03_data_processing/map_reduce/flow.py`)
- PDF Generation Workflow (`03_data_processing/pdf_generation/flow.py`)
- Retry Logic with Exponential Backoff (`03_data_processing/retry_logic/flow.py`)
- Timeout Handling (`03_data_processing/timeout_handling/flow.py`)
- Validation & Error Handling (`03_data_processing/validation_error_handling/flow.py`)

### Deployment & Packaging
- Build a Wheel for Sandbox (`13_deployment_packaging/build_wheel/flow.py`)
- Custom Image Workflow (`13_deployment_packaging/custom_image_workflow/flow.py`)
- Dockerfile Image (`13_deployment_packaging/dockerfile_image/flow.py`)
- Executor Base Image (`13_deployment_packaging/executor_base_image/flow.py`)
- Image Environment Variables (`13_deployment_packaging/image_env_vars/flow.py`)
- Image with Run Commands (`13_deployment_packaging/image_with_run_commands/flow.py`)
- Model Cache in Image (`13_deployment_packaging/model_cache_in_image/flow.py`)
- Multiple Images in One App (`13_deployment_packaging/multiple_images/flow.py`)
- Secrets via Environment (`13_deployment_packaging/secrets_via_env/flow.py`)

### GPU & Agents
- Agent Checkpointing Service (`12_gpu_ai_agents/agent_checkpointing_service/flow.py`)
- GPU Matrix Multiplication (`12_gpu_ai_agents/gpu_matrix_multiplication/flow.py`)
- Sandbox Dependencies for Agents (`12_gpu_ai_agents/sandbox_dependencies_langgraph/flow.py`)

### Getting Started
- Basic Task Execution (`01_getting_started/basic_task/flow.py`)
- Basic Workflow (`01_getting_started/basic_workflow/flow.py`)
- Data Processing Step (`01_getting_started/data_processing_step/flow.py`)
- Data Transformation Workflow (`01_getting_started/data_transformation_workflow/flow.py`)
- Hello World (`01_getting_started/hello_world/flow.py`)
- Multi-Branch Workflow (`01_getting_started/multi_branch_workflow/flow.py`)
- Parallel Execution (`01_getting_started/parallel_execution/flow.py`)
- Simple Step (`01_getting_started/simple_step/flow.py`)
- Step with Math (`01_getting_started/step_with_math/flow.py`)

### Integrations
- Cache Service (`05_integrations/cache_service/flow.py`)
- Connector Integration Patterns (`05_integrations/connector_integration/flow.py`)
- Database Service (`05_integrations/database_service/flow.py`)
- Email Queue Processor (`05_integrations/email_queue/flow.py`)
- Email Service (`05_integrations/email_service/flow.py`)
- GitHub Webhook Handler (`05_integrations/github_webhook/flow.py`)
- Multi-Channel Notification (`05_integrations/multi_channel_notification/flow.py`)
- REST API Service (`05_integrations/rest_api_service/flow.py`)
- Stripe Payment Webhook (`05_integrations/stripe_webhook/flow.py`)

### Machine Learning
- ML Inference Pipeline (`01_getting_started/ml_inference_pipeline/flow.py`)

### Platform Integrations
- Local Dict Connector (`11_integrations_platform/local_dict_connector/flow.py`)
- Local Multiple Services (`11_integrations_platform/local_multiple_services/flow.py`)
- Local Service Multistep (`11_integrations_platform/local_service_multistep/flow.py`)
- Publish with Retry (`11_integrations_platform/publish_with_retry/flow.py`)
- Redis Completion Polling (`11_integrations_platform/redis_completion_polling/flow.py`)
- Remote Control Plane Connection (`11_integrations_platform/remote_control_plane_connection/flow.py`)
- Service Composition Pipeline (`11_integrations_platform/service_composition_pipeline/flow.py`)

### Runtime & Routing
- Depth Across Boundaries (`08_runtime_routing/depth_cross_boundary/flow.py`)
- Depth Metrics API (`08_runtime_routing/depth_metrics_api/flow.py`)
- Depth Statistics Metrics (`08_runtime_routing/depth_statistics_metrics/flow.py`)
- Depth Tracking Basics (`08_runtime_routing/depth_tracking_basic/flow.py`)
- Depth Tracking Chain (`08_runtime_routing/depth_tracking_chain/flow.py`)
- Mixed Executor Routing (`08_runtime_routing/executor_routing_mixed/flow.py`)
- Mixed Load Profile (`08_runtime_routing/mixed_load_profile/flow.py`)
- State Machine Loop (`08_runtime_routing/state_machine_loop/flow.py`)
- Worker Type Isolation (`08_runtime_routing/worker_type_isolation/flow.py`)
- Worker Types Overview (`08_runtime_routing/worker_types_overview/flow.py`)

### Sandbox & Isolation
- Dynamic Code Execution (Sandboxed) (`09_sandbox_isolation/dynamic_code_execution/flow.py`)
- Isolated Execution (`09_sandbox_isolation/isolated_execution/flow.py`)
- Isolated Execution with Retry (`09_sandbox_isolation/isolated_retry/flow.py`)
- Pyodide Sandbox Dependencies (`09_sandbox_isolation/pyodide_dependencies/flow.py`)
- Pyodide Parallel Stress (`09_sandbox_isolation/pyodide_parallel_stress/flow.py`)
- Sandboxed Step Basics (`09_sandbox_isolation/sandboxed_step_basic/flow.py`)

### Web Endpoints
- API with Authentication (`02_web_endpoints/authenticated_api/flow.py`)
- Basic Calculator API (`02_web_endpoints/basic_calculator_api/flow.py`)
- Batch Processing API (`02_web_endpoints/batch_processing_api/flow.py`)
- Error Handling in APIs (`02_web_endpoints/error_handling_api/flow.py`)
- Multi-Step Data Pipeline API (`02_web_endpoints/multi_step_pipeline_api/flow.py`)
- Multiple Endpoints with Different Paths (`02_web_endpoints/multiple_endpoints/flow.py`)
- WebSocket Real-Time Updates (`02_web_endpoints/websocket_realtime/flow.py`)

### Web Endpoints Advanced
- API Key Middleware (`10_web_endpoints_advanced/api_key_middleware/flow.py`)
- ASGI Server Integration (`10_web_endpoints_advanced/asgi_server_integration/flow.py`)
- Custom Exception Handler (`10_web_endpoints_advanced/custom_exception_handler/flow.py`)
- Framework Endpoints (ASGI) (`10_web_endpoints_advanced/framework_endpoints_multi/flow.py`)
- GET Endpoint with Query Params (`10_web_endpoints_advanced/get_endpoint_query/flow.py`)
- Mount Blazing in FastAPI (`10_web_endpoints_advanced/mount_blazing_asgi/flow.py`)
- Multiple HTTP Methods (`10_web_endpoints_advanced/multiple_methods/flow.py`)
- Real HTTP Endpoints (`10_web_endpoints_advanced/real_http_endpoints/flow.py`)
- Streaming Progress Bar (`10_web_endpoints_advanced/streaming_progress_bar/flow.py`)
- Streaming Sidecar Route (`10_web_endpoints_advanced/streaming_sidecar_route/flow.py`)
- Streaming Workflow Progress (`10_web_endpoints_advanced/streaming_workflow_progress/flow.py`)

