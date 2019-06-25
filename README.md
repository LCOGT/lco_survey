# LCO Survey

Django app to collect feedback on our education programme.

## Configuration

Environment variables needed for production:

`SECRET_KEY` - Django secret key
`DEBUG` - Debug flag `True/False`
`DB_NAME` - database name
`DB_USER` - database username
`DB_PASS` - database user's password
`DB_HOST` - database host

## Build

This project is built automatically by the [LCO Jenkins Server](http://jenkins.lco.gtn/).
Please see the [Jenkinsfile](Jenkinsfile) for details.

## Production Deployment

This project is deployed on the LCO Kubernetes Cluster. Please see the
[LCO Helm Charts Repository](https://github.com/LCOGT/helm-charts) for details.

## License

This project is licensed under the MIT License. Please see the
[LICENSE](LICENSE) file for details.
