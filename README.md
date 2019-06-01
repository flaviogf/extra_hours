# Extra Hours

## Deploy azure webapp

```shell
export APP_NAME=dev-extra-hours \
export RESOURCE_GROUP=appsvc_rg_Linux_centralus \
export PLAN=appsvc_asp_Linux_centralus
```

```shell
az webapp up \
--name $APP_NAME \
--location centralus \
--resource-group $RESOURCE_GROUP \
--plan $PLAN \
--sku F1
```

```shell
az webapp config set \
--resource-group $RESOURCE_GROUP \
--name $APP_NAME \
--startup-file "gunicorn --bind=0.0.0.0 --timeout 600 wsgi:app"
```
