import yaml
from typing import Dict, List
import os
import subprocess

class KubernetesAgent:
    def generate_deployment(self, app_name: str, image: str, replicas: int = 2, port: int = 8000, env_vars: Dict = {}) -> str:
        env_list = [{"name": k, "value": str(v)} for k, v in env_vars.items()]
        deploy = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": f"{app_name}-deployment"},
            "spec": {
                "replicas": replicas,
                "selector": {"matchLabels": {"app": app_name}},
                "template": {
                    "metadata": {"labels": {"app": app_name}},
                    "spec": {
                        "containers": [{
                            "name": app_name,
                            "image": image,
                            "ports": [{"containerPort": port}],
                            "env": env_list,
                            "resources": {
                                "requests": {"cpu": "100m", "memory": "128Mi"},
                                "limits": {"cpu": "500m", "memory": "512Mi"}
                            }
                        }]
                    }
                }
            }
        }
        return yaml.dump(deploy, default_flow_style=False)

    def generate_service(self, app_name: str, port: int, service_type: str = 'ClusterIP') -> str:
        svc = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": f"{app_name}-service"},
            "spec": {
                "selector": {"app": app_name},
                "ports": [{"protocol": "TCP", "port": port, "targetPort": port}],
                "type": service_type
            }
        }
        return yaml.dump(svc, default_flow_style=False)

    def generate_ingress(self, app_name: str, host: str, port: int, tls: bool = True) -> str:
        ing = {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "Ingress",
            "metadata": {
                "name": f"{app_name}-ingress",
                "annotations": {
                    "kubernetes.io/ingress.class": "nginx"
                }
            },
            "spec": {
                "rules": [{
                    "host": host,
                    "http": {
                        "paths": [{
                            "path": "/",
                            "pathType": "Prefix",
                            "backend": {
                                "service": {
                                    "name": f"{app_name}-service",
                                    "port": {"number": port}
                                }
                            }
                        }]
                    }
                }]
            }
        }
        if tls:
            ing["metadata"]["annotations"]["cert-manager.io/cluster-issuer"] = "letsencrypt-prod"
            ing["spec"]["tls"] = [{"hosts": [host], "secretName": f"{app_name}-tls"}]
            
        return yaml.dump(ing, default_flow_style=False)

    def generate_hpa(self, app_name: str, min_replicas: int = 2, max_replicas: int = 10, cpu_threshold: int = 70) -> str:
        hpa = {
            "apiVersion": "autoscaling/v2",
            "kind": "HorizontalPodAutoscaler",
            "metadata": {"name": f"{app_name}-hpa"},
            "spec": {
                "scaleTargetRef": {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "name": f"{app_name}-deployment"
                },
                "minReplicas": min_replicas,
                "maxReplicas": max_replicas,
                "metrics": [{
                    "type": "Resource",
                    "resource": {
                        "name": "cpu",
                        "target": {
                            "type": "Utilization",
                            "averageUtilization": cpu_threshold
                        }
                    }
                }]
            }
        }
        return yaml.dump(hpa, default_flow_style=False)

    def generate_configmap(self, app_name: str, data: Dict) -> str:
        cm = {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {"name": f"{app_name}-config"},
            "data": data
        }
        return yaml.dump(cm, default_flow_style=False)

    def generate_secret(self, app_name: str, data: Dict) -> str:
        import base64
        encoded = {k: base64.b64encode(str(v).encode()).decode() for k, v in data.items()}
        sec = {
            "apiVersion": "v1",
            "kind": "Secret",
            "metadata": {"name": f"{app_name}-secret"},
            "type": "Opaque",
            "data": encoded
        }
        return yaml.dump(sec, default_flow_style=False)

    def generate_full_stack(self, app_config: Dict) -> str:
        app_name = app_config.get('app_name', 'app')
        image = app_config.get('image', 'nginx:latest')
        port = app_config.get('port', 80)
        
        manifests = [
            self.generate_deployment(app_name, image, port=port, env_vars=app_config.get('env', {})),
            self.generate_service(app_name, port, app_config.get('service_type', 'ClusterIP'))
        ]
        
        if 'host' in app_config:
            manifests.append(self.generate_ingress(app_name, app_config['host'], port))
            
        if app_config.get('hpa', False):
            manifests.append(self.generate_hpa(app_name))
            
        return "---\n".join(manifests)

    def apply_manifests(self, manifests_dir: str, dry_run: bool = True) -> Dict:
        cmd = ["kubectl", "apply", "-f", manifests_dir]
        if dry_run:
            cmd.append("--dry-run=client")
            
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return {"success": True, "resources_created": result.stdout.count('created'), "errors": ""}
            return {"success": False, "resources_created": 0, "errors": result.stderr}
        except Exception as e:
            return {"success": False, "resources_created": 0, "errors": str(e)}

def inject_kubernetes_prompt(system_prompt: str) -> str:
    return system_prompt + "\n[PrismAI Directive]: You have access to a Kubernetes Agent to generate deployments, services, ingress, and HPA configurations."
