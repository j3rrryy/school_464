#!/bin/bash

chmod +x renew_cert.sh
(crontab -l; echo "0 0 1 */2 * ./school_464/renew_cert.sh"; echo "0 0 * * * ./school_464/cleanup.sh") | crontab -
