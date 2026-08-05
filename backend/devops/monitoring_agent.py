import yaml
import json
from typing import Dict, List

class MonitoringAgent:
    def generate_prometheus_config(self, services: List[Dict]) -> str:
        scrape_configs = []
        for svc in services:
            scrape_configs.append({
                "job_name": svc.get("name", "app"),
                "metrics_path": svc.get("path", "/metrics"),
                "static_configs": [{"targets": [f"localhost:{svc.get('port', 8000)}"]}]
            })
            
        config = {
            "global": {"scrape_interval": "15s"},
            "scrape_configs": scrape_configs
        }
        return yaml.dump(config, sort_keys=False)

    def generate_grafana_dashboard(self, app_name: str, metrics: List[str]) -> Dict:
        panels = []
        for i, metric in enumerate(metrics):
            panels.append({
                "id": i+1,
                "title": f"{app_name} - {metric}",
                "type": "timeseries",
                "targets": [{"expr": metric, "refId": "A"}],
                "gridPos": {"h": 8, "w": 12, "x": (i%2)*12, "y": (i//2)*8}
            })
            
        dashboard = {
            "title": f"{app_name} Dashboard",
            "uid": f"{app_name.lower()}-dash",
            "panels": panels,
            "schemaVersion": 30
        }
        return dashboard

    def generate_alertmanager_config(self, slack_webhook: str = None, pagerduty_key: str = None) -> str:
        receivers = [{"name": "default"}]
        
        if slack_webhook:
            receivers.append({
                "name": "slack",
                "slack_configs": [{"api_url": slack_webhook, "channel": "#alerts"}]
            })
            
        if pagerduty_key:
            receivers.append({
                "name": "pagerduty",
                "pagerduty_configs": [{"service_key": pagerduty_key}]
            })
            
        config = {
            "global": {"resolve_timeout": "5m"},
            "route": {
                "group_by": ["alertname", "job"],
                "group_wait": "30s",
                "group_interval": "5m",
                "repeat_interval": "4h",
                "receiver": receivers[-1]["name"] if len(receivers) > 1 else "default"
            },
            "receivers": receivers
        }
        return yaml.dump(config, sort_keys=False)

    def generate_alert_rules(self, app_name: str, sla_uptime: float = 99.9) -> str:
        rules = {
            "groups": [{
                "name": f"{app_name}_alerts",
                "rules": [
                    {
                        "alert": "InstanceDown",
                        "expr": "up == 0",
                        "for": "1m",
                        "labels": {"severity": "critical"},
                        "annotations": {
                            "summary": "Instance {{ $labels.instance }} down",
                            "description": f"{app_name} instance has been down for more than 1 minute."
                        }
                    },
                    {
                        "alert": "HighErrorRate",
                        "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) > 0.05",
                        "for": "5m",
                        "labels": {"severity": "warning"},
                        "annotations": {
                            "summary": "High error rate detected",
                            "description": "Error rate is above 5% for the last 5 minutes."
                        }
                    }
                ]
            }]
        }
        return yaml.dump(rules, sort_keys=False)

    def generate_opentelemetry_config(self, language: str, service_name: str) -> str:
        config = {
            "receivers": {"otlp": {"protocols": {"grpc": {}, "http": {}}}},
            "processors": {"batch": {}},
            "exporters": {
                "prometheus": {"endpoint": "0.0.0.0:8889"},
                "jaeger": {"endpoint": "jaeger-all-in-one:14250", "tls": {"insecure": True}}
            },
            "service": {
                "pipelines": {
                    "traces": {"receivers": ["otlp"], "processors": ["batch"], "exporters": ["jaeger"]},
                    "metrics": {"receivers": ["otlp"], "processors": ["batch"], "exporters": ["prometheus"]}
                }
            }
        }
        return yaml.dump(config, sort_keys=False)

    def add_metrics_to_fastapi(self, code: str) -> str:
        injection = """
from prometheus_fastapi_instrumentator import Instrumentator

# Initialize metrics
Instrumentator().instrument(app).expose(app)
"""
        return code + "\n" + injection

    def add_metrics_to_express(self, code: str) -> str:
        injection = """
const client = require('prom-client');
const collectDefaultMetrics = client.collectDefaultMetrics;
collectDefaultMetrics({ register: client.register });

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});
"""
        return code + "\n" + injection

    def generate_logging_config(self, language: str, log_level: str = 'INFO') -> str:
        if language == 'python':
            return f"""
import logging
import json
import sys

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {{
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module
        }}
        return json.dumps(log_obj)

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.{log_level})
"""
        elif language == 'node':
            return f"""
const winston = require('winston');

const logger = winston.createLogger({{
  level: '{log_level.lower()}',
  format: winston.format.json(),
  transports: [
    new winston.transports.Console()
  ]
}});
"""
        return ""

def inject_monitoring_prompt(system_prompt: str) -> str:
    return system_prompt + "\n[LOT AI Directive]: You have access to a Monitoring Agent to configure Prometheus, Grafana, alerts, and OpenTelemetry instrumentation."
