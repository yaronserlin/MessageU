from Logger import Log

logger = Log(__name__)

def read_from_file(filename):
    try:
        logger.debug(f"Try to read the file '{filename}'")

        with open(filename,"r") as file:
            content =file.read().replace(" ", "").replace("\n","")

            if not content:
                raise ValueError(f"The file '{filename} is empty")

            return content
    except FileNotFoundError as e:
        logger.error(e)
        return None
    except ValueError as e:
        logger.warning(e)
        return None
    except Exception as e:
        logger.error(e)
        return None


