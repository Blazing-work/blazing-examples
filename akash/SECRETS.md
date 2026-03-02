# Akash Template Secrets Reference

This document lists all secrets used across Akash SDL templates in this library, along with the corresponding DigitalFrontier (DF) secret names needed to provision them.

| Secret Ref | Description | DF API Key | Env Var | Used In | Count |
|------------|-------------|------------|---------|---------|-------|
| `admin_password` | Admin password | `admin_password` | `ADMIN_PASSWORD` | machine-learning/doccano | 1 |
| `admin_token` | Admin token | `admin_token` | `ADMIN_TOKEN` | tools/vaultwarden | 1 |
| `allow_empty_password` | Allow empty password | `allow_empty_password` | `ALLOW_EMPTY_PASSWORD` | databases-and-administration/redis, social/discourse | 2 |
| `anon_key` | Anon key | `anon_key` | `ANON_KEY` | databases-and-administration/supabase | 1 |
| `arbitrage_private_key` | Arbitrage private key | `arbitrage_private_key` | `ARBITRAGE_PRIVATE_KEY` | _uncategorized/sovryn-node | 1 |
| `authorise_command_key` | Authorise command key | `authorise_command_key` | `AUTHORISE_COMMAND_KEY` | ai-cpu/auto-gpt | 1 |
| `aws_secret_access_key` | Aws secret access key | `aws_secret_access_key` | `AWS_SECRET_ACCESS_KEY` | _uncategorized/minio, cicd-devops/micro-services-example | 2 |
| `azp_token` | Azp token | `azp_token` | `AZP_TOKEN` | cicd-devops/azure-devops-agent | 1 |
| `backup_encryption_password` | Backup encryption password | `backup_encryption_password` | `BACKUP_ENCRYPTION_PASSWORD` | blogging/ghost-filebase-backup | 1 |
| `backup_key` | Backup key | `backup_key` | `BACKUP_KEY` | _uncategorized/postgres-restore | 1 |
| `backup_secret` | Backup secret | `backup_secret` | `BACKUP_SECRET` | _uncategorized/postgres-restore | 1 |
| `couchdb_password` | Couchdb password | `couchdb_password` | `COUCHDB_PASSWORD` | databases-and-administration/couchdb | 1 |
| `deepseek_api_key` | Deepseek api key | `deepseek_api_key` | `DEEPSEEK_API_KEY` | ai-cpu/Elizaos-ai_Agents | 1 |
| `discourse_database_password` | Discourse database password | `discourse_database_password` | `DISCOURSE_DATABASE_PASSWORD` | social/discourse | 1 |
| `dkn_wallet_secret_key` | Dkn wallet secret key | `dkn_wallet_secret_key` | `DKN_WALLET_SECRET_KEY` | ai-gpu/dria | 1 |
| `elevenlabs_api_key` | Elevenlabs api key | `elevenlabs_api_key` | `ELEVENLABS_API_KEY` | ai-cpu/auto-gpt | 1 |
| `eth_private_key` | Eth private key | `eth_private_key` | `ETH_PRIVATE_KEY` | decentralized-storage/codex | 1 |
| `exit_key` | Exit key | `exit_key` | `EXIT_KEY` | ai-cpu/auto-gpt | 1 |
| `filebase_secret_access_key` | Filebase secret access key | `filebase_secret_access_key` | `FILEBASE_SECRET_ACCESS_KEY` | blogging/ghost-filebase-backup | 1 |
| `flock_api_key` | Flock api key | `flock_api_key` | `FLOCK_API_KEY` | ai-gpu/FLock-training-node, ai-gpu/FLock-validator | 2 |
| `github_api_key` | Github api key | `github_api_key` | `GITHUB_API_KEY` | ai-cpu/auto-gpt | 1 |
| `google_api_key` | Google api key | `google_api_key` | `GOOGLE_API_KEY` | ai-cpu/auto-gpt | 1 |
| `gotrue_jwt_secret` | Gotrue jwt secret | `gotrue_jwt_secret` | `GOTRUE_JWT_SECRET` | databases-and-administration/supabase | 1 |
| `gpustack_token` | Gpustack token | `gpustack_token` | `GPUSTACK_TOKEN` | ai-gpu/gpustack-worker | 1 |
| `hf_token` | Hf token | `hf_token` | `HF_TOKEN` | ai-gpu/FLock-training-node, ai-gpu/FLock-validator, ai-gpu/Llama-3-70B, +14 more | 17 |
| `huggingface_api_token` | Huggingface api token | `huggingface_api_token` | `HUGGINGFACE_API_TOKEN` | ai-cpu/auto-gpt | 1 |
| `influxdb_admin_password` | Influxdb admin password | `influxdb_admin_password` | `INFLUXDB_ADMIN_PASSWORD` | databases-and-administration/influxdb | 1 |
| `jicofo_auth_password` | Jicofo auth password | `jicofo_auth_password` | `JICOFO_AUTH_PASSWORD` | video-conferencing/jitsi-meet | 1 |
| `jupyter_token` | Jupyter token | `jupyter_token` | `JUPYTER_TOKEN` | ai-gpu/axolotlai | 1 |
| `jvb_auth_password` | Jvb auth password | `jvb_auth_password` | `JVB_AUTH_PASSWORD` | video-conferencing/jitsi-meet | 1 |
| `kay_api_key` | Kay api key | `kay_api_key` | `KAY_API_KEY` | ai-gpu/open-gpt | 1 |
| `keycloak_admin_password` | Keycloak admin password | `keycloak_admin_password` | `KEYCLOAK_ADMIN_PASSWORD` | tools/keycloak-iam | 1 |
| `liquidator_private_key` | Liquidator private key | `liquidator_private_key` | `LIQUIDATOR_PRIVATE_KEY` | _uncategorized/sovryn-node | 1 |
| `lt_api_key` | Lt api key | `lt_api_key` | `LT_API_KEY` | tools/libretranslate | 1 |
| `mariadb_password` | Mariadb password | `mariadb_password` | `MARIADB_PASSWORD` | tools/nextcloud | 1 |
| `mariadb_random_root_password` | Mariadb random root password | `mariadb_random_root_password` | `MARIADB_RANDOM_ROOT_PASSWORD` | tools/nextcloud | 1 |
| `minio_access_key` | Minio access key | `minio_access_key` | `MINIO_ACCESS_KEY` | _uncategorized/minio | 1 |
| `minio_secret_key` | Minio secret key | `minio_secret_key` | `MINIO_SECRET_KEY` | _uncategorized/minio | 1 |
| `mongo_initdb_root_password` | Mongo initdb root password | `mongo_initdb_root_password` | `MONGO_INITDB_ROOT_PASSWORD` | business/RAIR-Dapp, databases-and-administration/mongoDB | 2 |
| `mysql_allow_empty_password` | Mysql allow empty password | `mysql_allow_empty_password` | `MYSQL_ALLOW_EMPTY_PASSWORD` | cicd-devops/micro-services-example | 1 |
| `mysql_password` | Mysql password | `mysql_password` | `MYSQL_PASSWORD` | blogging/wordpress, cicd-devops/micro-services-example, tools/matomo, +1 more | 4 |
| `mysql_random_root_password` | Mysql random root password | `mysql_random_root_password` | `MYSQL_RANDOM_ROOT_PASSWORD` | blogging/wordpress | 1 |
| `mysql_root_password` | Mysql root password | `mysql_root_password` | `MYSQL_ROOT_PASSWORD` | cicd-devops/micro-services-example, databases-and-administration/MySQL, project-management/redmine, +1 more | 4 |
| `n8n_encryption_key` | N8n encryption key | `n8n_encryption_key` | `N8N_ENCRYPTION_KEY` | business/n8n | 1 |
| `next_public_use_user_api_key` | Next public use user api key | `next_public_use_user_api_key` | `NEXT_PUBLIC_USE_USER_API_KEY` | ai-cpu/babyagi-ui | 1 |
| `nextauth_secret` | Nextauth secret | `nextauth_secret` | `NEXTAUTH_SECRET` | ai-cpu/chatchat | 1 |
| `np_auth_iron_password` | Np auth iron password | `np_auth_iron_password` | `NP_AUTH_IRON_PASSWORD` | blogging/nitropage | 1 |
| `openai_api_key` | Openai api key | `openai_api_key` | `OPENAI_API_KEY` | ai-cpu/auto-gpt, ai-cpu/babyagi, ai-cpu/babyagi-ui, +3 more | 6 |
| `openrouter_api_key` | Openrouter api key | `openrouter_api_key` | `OPENROUTER_API_KEY` | ai-gpu/dria | 1 |
| `pg_meta_db_password` | Pg meta db password | `pg_meta_db_password` | `PG_META_DB_PASSWORD` | databases-and-administration/supabase | 1 |
| `pgadmin_default_password` | Pgadmin default password | `pgadmin_default_password` | `PGADMIN_DEFAULT_PASSWORD` | databases-and-administration/pgadmin4 | 1 |
| `pgrst_jwt_secret` | Pgrst jwt secret | `pgrst_jwt_secret` | `PGRST_JWT_SECRET` | databases-and-administration/supabase | 1 |
| `pinecone_api_key` | Pinecone api key | `pinecone_api_key` | `PINECONE_API_KEY` | ai-cpu/babyagi-ui | 1 |
| `postgres_password` | Postgres password | `postgres_password` | `POSTGRES_PASSWORD` | _uncategorized/postgres-restore, ai-cpu/botpress, ai-cpu/chatchat, +9 more | 12 |
| `private_key` | Private key | `private_key` | `PRIVATE_KEY` | mining-pools/kawpow-pool-meowcoin, mining-pools/kawpow-pool-neoxa, mining-pools/kawpow-pool-ravencoin | 3 |
| `redash_cookie_secret` | Redash cookie secret | `redash_cookie_secret` | `REDASH_COOKIE_SECRET` | data-visualization/Redash | 1 |
| `redash_secret_key` | Redash secret key | `redash_secret_key` | `REDASH_SECRET_KEY` | data-visualization/Redash | 1 |
| `redis_password` | Redis password | `redis_password` | `REDIS_PASSWORD` | ai-cpu/auto-gpt, databases-and-administration/redis | 2 |
| `redmine_db_password` | Redmine db password | `redmine_db_password` | `REDMINE_DB_PASSWORD` | project-management/redmine | 1 |
| `retail_catalog_persistence_password` | Retail catalog persistence password | `retail_catalog_persistence_password` | `RETAIL_CATALOG_PERSISTENCE_PASSWORD` | cicd-devops/micro-services-example | 1 |
| `retail_orders_messaging_rabbitmq_password` | Retail orders messaging rabbitmq password | `retail_orders_messaging_rabbitmq_password` | `RETAIL_ORDERS_MESSAGING_RABBITMQ_PASSWORD` | cicd-devops/micro-services-example | 1 |
| `retail_orders_persistence_password` | Retail orders persistence password | `retail_orders_persistence_password` | `RETAIL_ORDERS_PERSISTENCE_PASSWORD` | cicd-devops/micro-services-example | 1 |
| `rln_relay_cred_password` | Rln relay cred password | `rln_relay_cred_password` | `RLN_RELAY_CRED_PASSWORD` | social/waku | 1 |
| `rollover_private_key` | Rollover private key | `rollover_private_key` | `ROLLOVER_PRIVATE_KEY` | _uncategorized/sovryn-node | 1 |
| `runner_token` | Runner token | `runner_token` | `RUNNER_TOKEN` | cicd-devops/ghrunner | 1 |
| `searp_api_key` | Searp api key | `searp_api_key` | `SEARP_API_KEY` | ai-cpu/babyagi-ui | 1 |
| `service_key` | Service key | `service_key` | `SERVICE_KEY` | databases-and-administration/supabase | 1 |
| `session_secret` | Session secret | `session_secret` | `SESSION_SECRET` | business/RAIR-Dapp | 1 |
| `setup_password` | Setup password | `setup_password` | `SETUP_PASSWORD` | ai-cpu/openclaw | 1 |
| `shiori_http_secret_key` | Shiori http secret key | `shiori_http_secret_key` | `SHIORI_HTTP_SECRET_KEY` | tools/shiori | 1 |
| `srcds_token` | Srcds token | `srcds_token` | `SRCDS_TOKEN` | game-servers/csgo, game-servers/tf2 | 2 |
| `sudo_password` | Sudo password | `sudo_password` | `SUDO_PASSWORD` | tools/code-server | 1 |
| `supabase_anon_key` | Supabase anon key | `supabase_anon_key` | `SUPABASE_ANON_KEY` | databases-and-administration/supabase | 1 |
| `supabase_service_key` | Supabase service key | `supabase_service_key` | `SUPABASE_SERVICE_KEY` | databases-and-administration/supabase | 1 |
| `tavily_api_key` | Tavily api key | `tavily_api_key` | `TAVILY_API_KEY` | ai-gpu/open-gpt | 1 |
| `telegram_bot_key` | Telegram bot key | `telegram_bot_key` | `TELEGRAM_BOT_KEY` | _uncategorized/sovryn-node | 1 |
| `tw_access_token` | Tw access token | `tw_access_token` | `TW_ACCESS_TOKEN` | ai-cpu/auto-gpt | 1 |
| `tw_access_token_secret` | Tw access token secret | `tw_access_token_secret` | `TW_ACCESS_TOKEN_SECRET` | ai-cpu/auto-gpt | 1 |
| `tw_consumer_key` | Tw consumer key | `tw_consumer_key` | `TW_CONSUMER_KEY` | ai-cpu/auto-gpt | 1 |
| `tw_consumer_secret` | Tw consumer secret | `tw_consumer_secret` | `TW_CONSUMER_SECRET` | ai-cpu/auto-gpt | 1 |
| `twitter_password` | Twitter password | `twitter_password` | `TWITTER_PASSWORD` | ai-cpu/Venice-ElizaOS | 1 |
| `venice_api_key` | Venice api key | `venice_api_key` | `VENICE_API_KEY` | ai-cpu/Venice-ElizaOS | 1 |
| `wallet_private_key` | Wallet private key | `wallet_private_key` | `WALLET_PRIVATE_KEY` | ai-cpu/morpheus-lumerin-node | 1 |
| `wandb_api_key` | Wandb api key | `wandb_api_key` | `WANDB_API_KEY` | ai-gpu/axolotlai | 1 |
| `webui_secret_key` | Webui secret key | `webui_secret_key` | `WEBUI_SECRET_KEY` | ai-cpu/open-webui-cpu, ai-gpu/open-webui-gpu | 2 |
| `wordpress_db_password` | Wordpress db password | `wordpress_db_password` | `WORDPRESS_DB_PASSWORD` | blogging/wordpress | 1 |
| `ydc_api_key` | Ydc api key | `ydc_api_key` | `YDC_API_KEY` | ai-gpu/open-gpt | 1 |

## Provisioning in DF

To provision secrets in your DigitalFrontier organization before deploying a template:

1. In your DF organization, go to **Settings → Secrets**
2. Click **Add Secret**
3. Enter the **DF API Key** name from the table above
4. Paste your credential value
5. Save

Each template's Core Compose YAML will automatically receive the secret value at deploy time when the secret_ref matches the API key name.
