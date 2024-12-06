### Python CLI (name : nufictl) for CRD npudeploy 

```bash
poetry shell
poetry install
```

* set context
```bash

# add api url with context_name and url
nufictl config set [context_name] https://nufi.nufi.me:31500/api/deployments 

# set config (change config)
nufictl config set_current_context [context_name]

# get config list
nufictl config ls
+---------+-------------+----------------------------------------------+
| Context | Config Name |                     URL                      |
+---------+-------------+----------------------------------------------+
|    *    |   default   | https://nufi.nufi.me:31500/api/deployments |
+---------+-------------+----------------------------------------------+

# get current context
nufictl config get_current_context                                                                                               2 ↵
Current context: default (https://nufi.nufi.me:31500/api/deployments)

# reset
nufictl config reset # reset config to default 

# help
nufictl config help # see command list

```


* nufictl exmaple
```bash

nufictl help # show command and explanation

nufictl ls
+---------------------------+---------------------------+----------+---------------------+------------------+-------------------+---------------------------------------+
|           Name            |         Namespace         | Replicas |       Created       | Accelerator Type | Accelerator Count |               Endpoint URL            |
+---------------------------+---------------------------+----------+---------------------+------------------+-------------------+---------------------------------------+
|      example-foo-002      | kubeflow-user-example-com |   2/2    | 2024-08-08 06:09:46 |       none       |         1         |      https://example-foo-002-kube     |
|      example-foo-003      | kubeflow-user-example-com |   1/1    | 2024-08-09 04:24:25 |       none       |         1         |      https://example-foo-003-kube     |
| npu-deploy-nginx-hxyvjbwr | kubeflow-user-example-com |   1/1    | 2024-08-05 06:48:04 |  skt.com/aix_v1  |         1         | https://npu-deploy-nginx-hxyvjbwr-    |
+---------------------------+---------------------------+----------+---------------------+------------------+-------------------+---------------------------------------+

nufictl create

Name [npu-deploy-example]: nufictl-test
Image [nginx]: 
CPU [1]: 
Memory [1]: 
Replicas [1]: 
Accelerator Type [npu]: 
Accelerator Count [1]: 
Successfully created nufictl-test with image: nginx


nufictl run --image=nginx                                                        
Successfully created npu-deploy-nginx-70w2c8yt with image: nginx


nufictl delete npu-deploy-example                                           
Successfully deleted npu-deploy-example
```