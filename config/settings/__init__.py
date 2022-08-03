from .local import LocalConfig
from .production import ProductionConfig
from .testing import TestingConfig

settings = {
    'development': LocalConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': LocalConfig,
}
