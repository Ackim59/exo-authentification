import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)

# TODO: replace the all-zero GUID with your instrumentation key.
logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=393a5c37-b4b6-47e6-87db-2012a7af0e1b'))
# You can also instantiate the exporter directly if you have the environment variable
# `APPLICATIONINSIGHTS_CONNECTION_STRING` configured
# logger.addHandler(AzureLogHandler())

def valuePrompt():
    line = input("Enter a value: ")
    logger.warning(line)

def main():
    while True:
        valuePrompt()

if __name__ == "__main__":
    main()