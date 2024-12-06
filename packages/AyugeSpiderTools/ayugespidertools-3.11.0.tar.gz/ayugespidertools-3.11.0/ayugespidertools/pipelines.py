from ayugespidertools.scraper.pipelines.download.file import FilesDownloadPipeline
from ayugespidertools.scraper.pipelines.es.asynced import AyuAsyncESPipeline
from ayugespidertools.scraper.pipelines.es.fantasy import AyuFtyESPipeline
from ayugespidertools.scraper.pipelines.mongo.asynced import AyuAsyncMongoPipeline
from ayugespidertools.scraper.pipelines.mongo.fantasy import AyuFtyMongoPipeline
from ayugespidertools.scraper.pipelines.mongo.twisted import AyuTwistedMongoPipeline
from ayugespidertools.scraper.pipelines.msgproducer.kafkapub import AyuKafkaPipeline
from ayugespidertools.scraper.pipelines.msgproducer.mqpub import AyuMQPipeline
from ayugespidertools.scraper.pipelines.mysql.asynced import AyuAsyncMysqlPipeline
from ayugespidertools.scraper.pipelines.mysql.fantasy import AyuFtyMysqlPipeline
from ayugespidertools.scraper.pipelines.mysql.stats import AyuStatisticsMysqlPipeline
from ayugespidertools.scraper.pipelines.mysql.turbo import AyuTurboMysqlPipeline
from ayugespidertools.scraper.pipelines.mysql.twisted import AyuTwistedMysqlPipeline
from ayugespidertools.scraper.pipelines.oracle.fantasy import AyuFtyOraclePipeline
from ayugespidertools.scraper.pipelines.oracle.twisted import AyuTwistedOraclePipeline
from ayugespidertools.scraper.pipelines.oss.ali import AyuAsyncOssPipeline
from ayugespidertools.scraper.pipelines.oss.batch import AyuAsyncOssBatchPipeline
from ayugespidertools.scraper.pipelines.postgres.asynced import AyuAsyncPostgresPipeline
from ayugespidertools.scraper.pipelines.postgres.fantasy import AyuFtyPostgresPipeline
from ayugespidertools.scraper.pipelines.postgres.twisted import (
    AyuTwistedPostgresPipeline,
)

__all__ = [
    "AyuFtyMysqlPipeline",
    "AyuFtyESPipeline",
    "AyuAsyncESPipeline",
    "AyuStatisticsMysqlPipeline",
    "AyuTurboMysqlPipeline",
    "AyuTwistedMysqlPipeline",
    "AyuAsyncMongoPipeline",
    "AyuAsyncMysqlPipeline",
    "AyuFtyMongoPipeline",
    "AyuTwistedMongoPipeline",
    "AyuMQPipeline",
    "AyuKafkaPipeline",
    "FilesDownloadPipeline",
    "AyuFtyOraclePipeline",
    "AyuTwistedOraclePipeline",
    "AyuAsyncOssPipeline",
    "AyuAsyncOssBatchPipeline",
    "AyuAsyncPostgresPipeline",
    "AyuFtyPostgresPipeline",
    "AyuTwistedPostgresPipeline",
]
