#!/bin/bash

sudo chmod +x renew_cert.sh cleanup.sh
(crontab -l; echo "0 0 1 */2 * bash ./school_464/renew_cert.sh"; echo "0 0 * * * bash ./school_464/cleanup.sh") | crontab -
