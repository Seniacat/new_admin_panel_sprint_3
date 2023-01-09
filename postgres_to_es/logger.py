import logging

logger = logging.getLogger('ES_Loader')
logger.setLevel(logging.INFO)

fmtstr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
fmtdate = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(format=fmtstr, datefmt=fmtdate)
