import pybreaker
import requests

from discovery.consulprovider import ConsulProvider


class CircuitBreaker:

    consul_provider: ConsulProvider = None
    logger = None
    circuit_breaker : pybreaker.CircuitBreaker= None
    

    @classmethod
    async def create(cls, logger, consul_provider: ConsulProvider):
        self = CircuitBreaker()
        self.logger = logger
        self.consul_provider = consul_provider
        self.circuit_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=10)
        return self

    def breaker_call(self, service_name):
        try:
            return self.circuit_breaker.call(self.check_healthcheck, service_name)
        except pybreaker.CircuitBreakerError as cbe:
            self.logger.error(f"Circuit Breaker abierto para {service_name}: {cbe}")
            raise
        except Exception as e:
            self.logger.error(f"Error en el healthcheck para {service_name}: {e}")
            raise

    def check_healthcheck(self, service_name):
        try:
            ret = self.consul_provider.get_consul_service(service_name)
            if not ret["Address"] or not ret["Port"]:
                raise ValueError(f"Servicio {service_name} no encontrado en Consul")

            response = requests.get(f"http://{ret['Address']}:{ret['Port']}/health", timeout=5)
            response.raise_for_status() 
            return True
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error al realizar healthcheck para {service_name}: {e}")
            raise
