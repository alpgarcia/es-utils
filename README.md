# es-utils
Set of scripts related to ES

[Troubleshooting](#troubleshooting)

# Troubleshooting

1. [Connection Problems](#1-connection-problems-timeouts)

#### 1. Connection problems (timeouts)
Take care when specifying ES host. If you don't add the corresponding HTTP port and it is not the default ES one, connection will fail.

For instance, if you are connecting through port 80, you should literally write `your_host:80` as ES default port is 9200.

